// Program.cs - Strongly-Typed Structured Output Pipeline in .NET 9
using Azure.AI.OpenAI;
using OpenAI.Chat;
using System.Text.Json;
using System.Text.Json.Serialization;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

var client = new AzureOpenAIClient(
    new Uri(builder.Configuration["AzureOpenAI:Endpoint"]!),
    new System.ClientModel.ApiKeyCredential(builder.Configuration["AzureOpenAI:ApiKey"]!));

var chatClient = client.GetChatClient("gpt-4o");

app.MapPost("/api/v1/compliance/verify", async (AuditLogRequest request) =>
{
    // Define Strict JSON Schema using modern OpenAI ChatResponseFormat
    var jsonSchema = BinaryData.FromObjectAsJson(new
    {
        type = "object",
        properties = new
        {
            policyId = new { type = "string" },
            complianceStatus = new { type = "string", @enum = new[] { "COMPLIANT", "VIOLATION", "NEEDS_MANUAL_REVIEW" } },
            severity = new { type = "string", @enum = new[] { "CRITICAL", "HIGH", "MEDIUM", "LOW", "NONE" } },
            violatedClauses = new { type = "array", items = new { type = "string" } },
            remediationSummary = new { type = "string" }
        },
        required = new[] { "policyId", "complianceStatus", "severity", "violatedClauses", "remediationSummary" },
        additionalProperties = false
    });

    var options = new ChatCompletionOptions
    {
        Temperature = 0.0f,
        ResponseFormat = ChatResponseFormat.CreateJsonSchemaFormat(
            jsonSchemaFormatName: "ComplianceEvaluationResult",
            jsonSchema: jsonSchema,
            jsonSchemaIsStrict: true // Enforces Grammar-Constrained Logit Masking
        )
    };

    var messages = new List<ChatMessage>
    {
        new SystemChatMessage("You are an automated compliance auditor. Output strictly conforms to the JSON schema."),
        new UserChatMessage($"<audit_event>{request.RawLog}</audit_event>")
    };

    ClientResult<ChatCompletion> result = await chatClient.CompleteChatAsync(messages, options);
    var jsonOutput = result.Value.Content[0].Text;

    // Direct deserialization into strongly-typed C# record
    var evaluation = JsonSerializer.Deserialize<ComplianceEvaluationRecord>(jsonOutput, new JsonSerializerOptions
    {
        PropertyNameCaseInsensitive = true
    });

    return Results.Ok(evaluation);
});

app.Run();

public record AuditLogRequest(string RawLog);

public record ComplianceEvaluationRecord(
    [property: JsonPropertyName("policyId")] string PolicyId,
    [property: JsonPropertyName("complianceStatus")] string ComplianceStatus,
    [property: JsonPropertyName("severity")] string Severity,
    [property: JsonPropertyName("violatedClauses")] List<string> ViolatedClauses,
    [property: JsonPropertyName("remediationSummary")] string RemediationSummary
);
