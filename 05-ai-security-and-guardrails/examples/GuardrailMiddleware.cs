// ============================================================================
// File: EnterpriseAiGuardrailFilter.cs
// Target: .NET 9.0 / Microsoft Semantic Kernel 1.x
// Enterprise Guardrail Filter and ASP.NET Core AI Interceptor
// ============================================================================

using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Security.Cryptography;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel;

namespace Enterprise.Ai.Security.Guardrails;

/// <summary>
/// Status of security guardrail evaluation.
/// </summary>
public enum GuardrailStatus
{
    Passed,
    RejectedInjection,
    RejectedPiiDisclosure,
    RejectedCanaryLeak,
    RejectedPolicyViolation
}

public sealed record GuardrailEvaluation(bool IsSafe, GuardrailStatus Status, string? Message, string ProcessedContent);

/// <summary>
/// Enterprise PII Redactor for .NET 9 using compiled Regex source generators for high throughput.
/// </summary>
public sealed partial class EnterprisePiiRedactor
{
    [GeneratedRegex(@"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", RegexOptions.Compiled)]
    private static partial Regex EmailRegex();

    [GeneratedRegex(@"\b\d{3}-\d{2}-\d{4}\b", RegexOptions.Compiled)]
    private static partial Regex SsnRegex();

    [GeneratedRegex(@"\b(?:\d{4}[-\s]?){3}\d{4}\b", RegexOptions.Compiled)]
    private static partial Regex CreditCardRegex();

    public (string RedactedText, Dictionary<string, string> Vault) Redact(string input)
    {
        var vault = new Dictionary<string, string>();
        string result = input;

        result = EmailRegex().Replace(result, match =>
        {
            string token = $"<ENTITY_EMAIL_{Convert.ToHexString(SHA256.HashData(System.Text.Encoding.UTF8.GetBytes(match.Value)))[..8]}>";
            vault[token] = match.Value;
            return token;
        });

        result = SsnRegex().Replace(result, match =>
        {
            string token = $"<ENTITY_SSN_{Convert.ToHexString(SHA256.HashData(System.Text.Encoding.UTF8.GetBytes(match.Value)))[..8]}>";
            vault[token] = match.Value;
            return token;
        });

        return (result, vault);
    }
}

/// <summary>
/// Semantic Kernel Filter that intercepts prompt rendering and function execution.
/// Adheres to IPromptRenderFilter and IFunctionInvocationFilter.
/// </summary>
public sealed class SecurityGuardrailKernelFilter : IPromptRenderFilter, IFunctionInvocationFilter
{
    private readonly ILogger<SecurityGuardrailKernelFilter> _logger;
    private readonly EnterprisePiiRedactor _piiRedactor;
    private static readonly Regex InjectionPattern = new(
        @"(?i)(ignore\s+(all\s+)?(previous|prior)\s+instructions|system\s+prompt\s+override|you\s+are\s+now\s+dan|developer\s+mode)",
        RegexOptions.Compiled);

    // Context tracking for ephemeral session canaries
    private static readonly ConcurrentDictionary<string, string> ActiveCanaryVault = new();

    public SecurityGuardrailKernelFilter(ILogger<SecurityGuardrailKernelFilter> logger)
    {
        _logger = logger;
        _piiRedactor = new EnterprisePiiRedactor();
    }

    /// <summary>
    /// Intercepts the prompt BEFORE it is rendered and sent to the LLM backend.
    /// </summary>
    public async Task OnPromptRenderAsync(PromptRenderContext context, Func<PromptRenderContext, Task> next)
    {
        string rawPrompt = context.RenderedPrompt ?? string.Empty;

        // 1. Fast Regex Injection Scan
        if (InjectionPattern.IsMatch(rawPrompt))
        {
            _logger.LogWarning("Prompt injection attempt intercepted in OnPromptRenderAsync.");
            throw new SecurityException("Security Guardrail Rejection: Detected adversarial prompt pattern.");
        }

        // 2. PII Redaction
        var (redactedPrompt, vault) = _piiRedactor.Redact(rawPrompt);
        context.RenderedPrompt = redactedPrompt;

        // 3. Canary Token Generation
        string canary = $"CANARY_SEC_{Convert.ToHexString(RandomNumberGenerator.GetBytes(12))}";
        string correlationId = context.Function.Name + "_" + Guid.NewGuid().ToString("N")[..8];
        ActiveCanaryVault[correlationId] = canary;

        // Inject Canary into execution context arguments
        context.Arguments["ActiveCanaryToken"] = canary;
        context.Arguments["CanaryCorrelationId"] = correlationId;

        await next(context);
    }

    /// <summary>
    /// Intercepts the response AFTER the function or model completes execution.
    /// </summary>
    public async Task OnFunctionInvocationAsync(FunctionInvocationContext context, Func<FunctionInvocationContext, Task> next)
    {
        await next(context);

        // Post-Inference Canary Leakage Check
        if (context.Arguments.TryGetValue("ActiveCanaryToken", out object? canaryObj) && canaryObj is string canary)
        {
            string output = context.Result.ToString() ?? string.Empty;
            if (output.Contains(canary, StringComparison.OrdinalIgnoreCase))
            {
                _logger.LogCritical("CRITICAL SECURITY BREACH: Model leaked active canary token {Canary}!", canary);
                
                // Overwrite result before it leaves the kernel boundary
                context.Result = new FunctionResult(
                    context.Function, 
                    "Security Alert: The generated response violated confidentiality policies and was redacted.");
            }
        }
    }
}

/// <summary>
/// ASP.NET Core Middleware intercepting raw HTTP AI requests at the network edge.
/// </summary>
public sealed class AiGuardrailMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<AiGuardrailMiddleware> _logger;

    public AiGuardrailMiddleware(RequestDelegate next, ILogger<AiGuardrailMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        // Only inspect endpoints routed to AI inference services
        if (context.Request.Path.StartsWithSegments("/api/v1/ai", StringComparison.OrdinalIgnoreCase))
        {
            context.Request.EnableBuffering();
            using var reader = new System.IO.StreamReader(context.Request.Body, leaveOpen: true);
            string body = await reader.ReadToEndAsync();
            context.Request.Body.Position = 0;

            // Inspect body for dangerous raw control sequences
            if (body.Contains("</system>", StringComparison.OrdinalIgnoreCase) ||
                body.Contains("<!-- override -->", StringComparison.OrdinalIgnoreCase))
            {
                _logger.LogWarning("AI Edge Middleware blocked malformed delimiter payload from IP: {Ip}", context.Connection.RemoteIpAddress);
                context.Response.StatusCode = StatusCodes.Status400BadRequest;
                context.Response.ContentType = "application/json";
                await context.Response.WriteAsync("{\"error\": \"Invalid request: Malformed delimiter detected.\"}");
                return;
            }
        }

        await _next(context);
    }
}
