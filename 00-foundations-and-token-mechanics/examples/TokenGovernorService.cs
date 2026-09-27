// Program.cs - Enterprise Token Budgeting and VRAM Estimation Service in .NET 9
using Microsoft.ML.Tokenizers;
using System.Text.Json;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddSingleton<ITokenGovernorService, TokenGovernorService>();

var app = builder.Build();

app.MapPost("/api/v1/governance/check-budget", async (HttpContext context, ITokenGovernorService governor) =>
{
    using var reader = new StreamReader(context.Request.Body);
    var body = await reader.ReadToEndAsync();
    var request = JsonSerializer.Deserialize<PromptBudgetRequest>(body);

    if (request == null)
        return Results.BadRequest(new { Error = "Malformed payload" });

    var report = governor.EvaluateRequest(request);
    if (!report.IsPermitted)
    {
        context.Response.StatusCode = StatusCodes.Status429TooManyRequests;
        return Results.Json(report);
    }

    return Results.Ok(report);
});

app.Run();

public record PromptBudgetRequest(string Model, string SystemPrompt, string UserPrompt, int ExpectedOutputTokens, int ConcurrentBatchSize);

public record BudgetReport(
    bool IsPermitted,
    int TotalInputTokens,
    double EstimatedCostUsd,
    double KvCacheMemoryMb,
    string RejectionReason
);

public interface ITokenGovernorService
{
    BudgetReport EvaluateRequest(PromptBudgetRequest request);
}

public class TokenGovernorService : ITokenGovernorService
{
    private readonly TiktokenTokenizer _tokenizer = TiktokenTokenizer.CreateForModel("gpt-4.5");
    private const int HARD_MAX_INPUT_TOKENS = 32_000;
    private const double MAX_DOLLAR_LIMIT_PER_REQUEST = 0.50;

    public BudgetReport EvaluateRequest(PromptBudgetRequest request)
    {
        var sysCount = _tokenizer.CountTokens(request.SystemPrompt);
        var userCount = _tokenizer.CountTokens(request.UserPrompt);
        var totalInput = sysCount + userCount;

        // Cost estimation: $2.50 / 1M in, $10.00 / 1M out
        var cost = ((totalInput / 1_000_000.0) * 2.50) + ((request.ExpectedOutputTokens / 1_000_000.0) * 10.00);

        // Hardware KV Cache calculation for GQA (80 layers, 8 KV heads, head dim 128, FP16 = 2 bytes)
        // Formula: 2 * 2 * L * H_kv * D_head * Batch * SeqLen
        double totalSeqLen = totalInput + request.ExpectedOutputTokens;
        double kvCacheBytes = 2.0 * 2.0 * 80 * 8 * 128 * request.ConcurrentBatchSize * totalSeqLen;
        double kvCacheMb = kvCacheBytes / (1024 * 1024);

        if (totalInput > HARD_MAX_INPUT_TOKENS)
        {
            return new BudgetReport(false, totalInput, cost, kvCacheMb, $"Input tokens ({totalInput}) exceeds hard ceiling of {HARD_MAX_INPUT_TOKENS}");
        }

        if (cost > MAX_DOLLAR_LIMIT_PER_REQUEST)
        {
            return new BudgetReport(false, totalInput, cost, kvCacheMb, $"Estimated cost (${cost:F4}) exceeds single request ceiling of ${MAX_DOLLAR_LIMIT_PER_REQUEST}");
        }

        return new BudgetReport(true, totalInput, cost, kvCacheMb, string.Empty);
    }
}
