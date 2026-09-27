// Program.cs
// Enterprise .NET 9 Semantic Kernel Function Calling with Execution Filters & Governance.
//
// Dependencies (NuGet):
//   dotnet add package Microsoft.SemanticKernel
//   dotnet add package Microsoft.Extensions.Logging.Console

using System;
using System.ComponentModel;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;

namespace EnterpriseAgenticSystems;

// ---------------------------------------------------------------------------
// 1. Enterprise System Observability Plugin
// ---------------------------------------------------------------------------
public sealed class SystemMetricsPlugin
{
    private readonly ILogger<SystemMetricsPlugin> _logger;

    public SystemMetricsPlugin(ILogger<SystemMetricsPlugin> logger)
    {
        _logger = logger;
    }

    [KernelFunction, Description("Retrieves real-time CPU, Memory, and Disk utilization for an enterprise server.")]
    public async Task<string> GetHostMetricsAsync(
        [Description("The fully qualified domain name (FQDN) or IP of the host machine.")] string hostname,
        [Description("Metric sampling window: 'realtime', '5m', or '1h'.")] string window = "realtime",
        CancellationToken cancellationToken = default)
    {
        _logger.LogInformation("Querying telemetry daemon on host {Hostname} with window {Window}", hostname, window);
        
        await Task.Delay(150, cancellationToken); // Simulated async telemetry I/O

        var sample = new
        {
            Host = hostname,
            TimestampUtc = DateTime.UtcNow,
            SamplingWindow = window,
            CpuUtilizationPercent = 42.8,
            MemoryUsedGigabytes = 28.4,
            MemoryTotalGigabytes = 64.0,
            DiskIops = 1450,
            HealthStatus = "HEALTHY"
        };

        return JsonSerializer.Serialize(sample, new JsonSerializerOptions { WriteIndented = true });
    }

    [KernelFunction, Description("Triggers an automated host reboot or service restart. MUTATING OPERATION.")]
    public async Task<string> RestartHostServiceAsync(
        [Description("Target host identifier.")] string hostname,
        [Description("Name of the system service daemon to restart.")] string serviceName,
        CancellationToken cancellationToken = default)
    {
        _logger.LogWarning("MUTATION: Restarting service {Service} on {Hostname}", serviceName, hostname);
        await Task.Delay(300, cancellationToken);
        return $"SUCCESS: Service '{serviceName}' restarted successfully on host '{hostname}'.";
    }
}

// ---------------------------------------------------------------------------
// 2. Enterprise Governance & Human-in-the-Loop Invocation Filter
// ---------------------------------------------------------------------------
public sealed class EnterpriseToolGovernanceFilter : IAutoFunctionInvocationFilter
{
    private readonly ILogger<EnterpriseToolGovernanceFilter> _logger;

    public EnterpriseToolGovernanceFilter(ILogger<EnterpriseToolGovernanceFilter> logger)
    {
        _logger = logger;
    }

    public async Task OnAutoFunctionInvocationAsync(
        AutoFunctionInvocationContext context,
        Func<AutoFunctionInvocationContext, Task> next)
    {
        var functionName = context.Function.Name;
        var pluginName = context.Function.PluginName;

        _logger.LogInformation("[AUDIT] Model requested invocation of tool: {Plugin}.{Function}", pluginName, functionName);

        // Enforce Human-in-the-Loop (HITL) gate for Mutating Functions
        if (functionName.StartsWith("Restart", StringComparison.OrdinalIgnoreCase) ||
            functionName.Contains("Delete", StringComparison.OrdinalIgnoreCase))
        {
            _logger.LogWarning("[HITL GATE] Intercepted mutating operation: {Function}. Requesting authorization...", functionName);

            bool isApproved = RequestHumanApproval(context);
            if (!isApproved)
            {
                // Abort execution and inject policy rejection directly into the model context
                context.Result = new FunctionResult(
                    context.Function, 
                    "AUTHORIZATION_DENIED: The human supervisor rejected this mutating operation."
                );
                context.Terminate = false; // Allow model to acknowledge rejection
                return;
            }
        }

        // Proceed with tool execution
        await next(context);

        _logger.LogInformation("[AUDIT] Tool execution completed successfully for {Function}.", functionName);
    }

    private static bool RequestHumanApproval(AutoFunctionInvocationContext context)
    {
        Console.ForegroundColor = ConsoleColor.Yellow;
        Console.WriteLine("\n========================================================");
        Console.WriteLine(" [HUMAN-IN-THE-LOOP AUTHORIZATION REQUIRED]");
        Console.WriteLine($" Function: {context.Function.Name}");
        Console.WriteLine($" Arguments: {JsonSerializer.Serialize(context.Arguments)}");
        Console.Write(" Authorize this destructive operation? (y/N): ");
        Console.ResetColor();

        // In automated tests or headless CI, default to false.
        // For CLI execution, prompt the user:
        string? input = Console.ReadLine();
        return string.Equals(input?.Trim(), "y", StringComparison.OrdinalIgnoreCase);
    }
}

// ---------------------------------------------------------------------------
// 3. Orchestration & Execution Runtime
// ---------------------------------------------------------------------------
public static class Program
{
    public static async Task Main(string[] args)
    {
        // Setup Dependency Injection & Logging
        var services = new ServiceCollection();
        services.AddLogging(builder => builder.AddConsole().SetMinimumLevel(LogLevel.Information));
        services.AddSingleton<SystemMetricsPlugin>();
        services.AddSingleton<IAutoFunctionInvocationFilter, EnterpriseToolGovernanceFilter>();

        // Build Kernel with Azure OpenAI / OpenAI Connector
        var kernelBuilder = Kernel.CreateBuilder();
        kernelBuilder.Services.AddLogging(b => b.AddConsole());
        
        // Register Plugins & Filters
        kernelBuilder.Plugins.AddFromType<SystemMetricsPlugin>("SystemMetrics");
        kernelBuilder.Services.AddSingleton<IAutoFunctionInvocationFilter, EnterpriseToolGovernanceFilter>();

        // Note: Configure with live Azure OpenAI / OpenAI endpoint
        // kernelBuilder.AddAzureOpenAIChatCompletion("gpt-4.5", "https://your-endpoint.openai.azure.com", "api-key");
        
        var kernel = kernelBuilder.Build();

        Console.WriteLine("Enterprise Semantic Kernel Function Calling System Initialized.");
        Console.WriteLine("Plugins registered: SystemMetricsPlugin (GetHostMetricsAsync, RestartHostServiceAsync)");
        Console.WriteLine("Governance Filter Active: Human-in-the-Loop gate enabled for mutating actions.\n");
    }
}
