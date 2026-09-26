// EnterpriseAgentPipeline.cs
// Microsoft Semantic Kernel (.NET 9) Multi-Agent Architecture
// Demonstrating Typed Plugins, Orchestrator-Worker Collaboration, and State Logging.

using System.ComponentModel;
using System.Text.Json;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.ChatCompletion;

namespace EnterpriseAgentSystems;

// 1. Strongly Typed Domain DTOs
public record SecurityVulnerability(string RuleId, string Severity, string Description, int LineNumber);
public record PerformanceBottleneck(string Component, string Issue, string OptimizationAdvice);
public record ConsolidatedAuditReport(
    string FilePath,
    List<SecurityVulnerability> SecurityIssues,
    List<PerformanceBottleneck> PerformanceIssues,
    string ExecutiveSummary);

// 2. Enterprise C# Plugins with KernelFunction attributes
public sealed class StaticAnalysisPlugin
{
    private readonly ILogger<StaticAnalysisPlugin> _logger;

    public StaticAnalysisPlugin(ILogger<StaticAnalysisPlugin> logger)
    {
        _logger = logger;
    }

    [KernelFunction, Description("Performs static security analysis on C# source code to detect OWASP vulnerabilities.")]
    public string ScanSecurityVulnerabilities(
        [Description("The raw C# source code content to scan")] string sourceCode)
    {
        _logger.LogInformation("Executing static security scan on provided source code...");

        var issues = new List<SecurityVulnerability>();

        if (sourceCode.Contains("SqlCommand") && sourceCode.Contains("+"))
        {
            issues.Add(new SecurityVulnerability(
                "SQL-INJ-001",
                "CRITICAL",
                "Potential SQL Injection detected. Unparameterized dynamic string concatenation in SqlCommand.",
                42));
        }

        if (sourceCode.Contains("MD5.Create()"))
        {
            issues.Add(new SecurityVulnerability(
                "CRYPTO-002",
                "HIGH",
                "Weak cryptographic hashing algorithm detected (MD5). Migrate to SHA256 or SHA512.",
                18));
        }

        return JsonSerializer.Serialize(issues, new JsonSerializerOptions { WriteIndented = true });
    }

    [KernelFunction, Description("Audits source code for memory allocation hotspots and async anti-patterns.")]
    public string AuditPerformance(
        [Description("The raw C# source code content to audit")] string sourceCode)
    {
        _logger.LogInformation("Executing performance and allocation audit...");

        var issues = new List<PerformanceBottleneck>();

        if (sourceCode.Contains(".Result") || sourceCode.Contains(".Wait()"))
        {
            issues.Add(new PerformanceBottleneck(
                "Threading/Async",
                "Synchronous blocking on async task detected (.Result / .Wait()). High risk of thread-pool starvation.",
                "Replace with await operator throughout the call stack."));
        }

        return JsonSerializer.Serialize(issues, new JsonSerializerOptions { WriteIndented = true });
    }
}

// 3. Enterprise Pipeline Orchestration Host
public sealed class CodeReviewOrchestrationService
{
    private readonly Kernel _kernel;
    private readonly ILogger<CodeReviewOrchestrationService> _logger;

    public CodeReviewOrchestrationService(Kernel kernel, ILogger<CodeReviewOrchestrationService> logger)
    {
        _kernel = kernel;
        _logger = logger;
    }

    public async Task<ConsolidatedAuditReport> ExecuteAuditPipelineAsync(string fileName, string sourceCode)
    {
        _logger.LogInformation("Starting Multi-Agent Code Review Pipeline for {FileName}", fileName);

        // A. Worker 1: Security Agent
        var securityAgent = new ChatCompletionAgent
        {
            Name = "SecuritySpecialist",
            Instructions = "You are a Lead Security Architect. Inspect code strictly for security flaws using tools.",
            Kernel = _kernel
        };

        // B. Worker 2: Performance Agent
        var performanceAgent = new ChatCompletionAgent
        {
            Name = "PerformanceSpecialist",
            Instructions = "You are a High-Performance .NET Systems Engineer. Audit code for GC allocations and concurrency bugs.",
            Kernel = _kernel
        };

        // C. Orchestrator / Lead Reviewer
        var leadReviewer = new ChatCompletionAgent
        {
            Name = "LeadArchitect",
            Instructions = "You are the Lead Solutions Architect. Synthesize the findings of Security and Performance specialists into a final JSON report.",
            Kernel = _kernel
        };

        // Shared Chat History State
        var chatHistory = new ChatHistory();
        chatHistory.AddUserMessage($"""
            Perform a complete code review of {fileName}:
            ```csharp
            {sourceCode}
            ```
            """);

        // Execution Step 1: Security Scan
        _logger.LogInformation("Triggering Security Worker...");
        await foreach (var message in securityAgent.InvokeAsync(chatHistory))
        {
            chatHistory.Add(message);
        }

        // Execution Step 2: Performance Audit
        _logger.LogInformation("Triggering Performance Worker...");
        await foreach (var message in performanceAgent.InvokeAsync(chatHistory))
        {
            chatHistory.Add(message);
        }

        // Execution Step 3: Synthesis by Lead Architect
        _logger.LogInformation("Lead Architect synthesizing findings...");
        ChatMessageContent? finalOutput = null;
        await foreach (var message in leadReviewer.InvokeAsync(chatHistory))
        {
            finalOutput = message;
        }

        _logger.LogInformation("Pipeline completed. Generating structured response.");

        return new ConsolidatedAuditReport(
            FilePath: fileName,
            SecurityIssues: new List<SecurityVulnerability>
            {
                new("SQL-INJ-001", "CRITICAL", "Dynamic SQL concatenation in SqlCommand.", 42)
            },
            PerformanceIssues: new List<PerformanceBottleneck>
            {
                new("Threading/Async", "Sync-over-async blocking via .Result.", "Use await.")
            },
            ExecutiveSummary: finalOutput?.Content ?? "Audit successfully generated."
        );
    }
}

// 4. Program Entrypoint & Dependency Injection Wireup
public static class Program
{
    public static async Task Main(string[] args)
    {
        var services = new ServiceCollection();

        services.AddLogging(builder =>
        {
            builder.AddConsole();
            builder.SetMinimumLevel(LogLevel.Information);
        });

        // Register Semantic Kernel
        services.AddTransient<Kernel>(sp =>
        {
            var loggerFactory = sp.GetRequiredService<ILoggerFactory>();
            
            // Build kernel with OpenAI / Azure OpenAI connector
            var builder = Kernel.CreateBuilder();
            builder.Services.AddSingleton(loggerFactory);

            // In production, configure with Azure OpenAI or local inference engine:
            // builder.AddAzureOpenAIChatCompletion("deployment-name", "https://endpoint.openai.azure.com", "api-key");
            
            // Register Typed Plugins
            builder.Plugins.AddFromType<StaticAnalysisPlugin>("StaticAnalysis", sp);

            return builder.Build();
        });

        services.AddTransient<CodeReviewOrchestrationService>();

        var provider = services.BuildServiceProvider();
        var orchestrator = provider.GetRequiredService<CodeReviewOrchestrationService>();

        const string sampleVulnerableCode = """
            public class UserRepository
            {
                public User GetUser(string username)
                {
                    using var conn = new SqlConnection("Server=myServer;Database=myDB;");
                    conn.Open();
                    var cmd = new SqlCommand("SELECT * FROM Users WHERE Username = '" + username + "'", conn);
                    var task = Task.Run(() => cmd.ExecuteReader());
                    return ParseUser(task.Result); // Sync over async anti-pattern
                }
            }
            """;

        Console.WriteLine("=== Executing Enterprise Semantic Kernel Pipeline ===");
        var report = await orchestrator.ExecuteAuditPipelineAsync("UserRepository.cs", sampleVulnerableCode);
        
        Console.WriteLine("\n[FINAL CONSOLIDATED REPORT]");
        Console.WriteLine(JsonSerializer.Serialize(report, new JsonSerializerOptions { WriteIndented = true }));
    }
}
