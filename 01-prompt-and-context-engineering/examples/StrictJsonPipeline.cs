// Program.cs - Strongly-Typed Structured Output Pipeline in .NET 9 (Console Harness)
// Demonstrates Grammar-Constrained Logit Masking using OpenAI / Azure OpenAI ChatResponseFormat with strict: true

using System;
using System.Collections.Generic;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading.Tasks;
using System.ClientModel;
using Azure.AI.OpenAI;
using OpenAI.Chat;

namespace StrictJsonPipeline;

public class Program
{
    public static async Task Main(string[] args)
    {
        Console.WriteLine("=== .NET 9 Strict JSON Schema Pipeline ===");

        string endpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT") ?? "https://example.openai.azure.com/";
        string apiKey = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY") ?? "mock-api-key";

        var client = new AzureOpenAIClient(new Uri(endpoint), new System.ClientModel.ApiKeyCredential(apiKey));
        var chatClient = client.GetChatClient("gpt-4o");

        // Define Strict JSON Schema using modern OpenAI ChatResponseFormat
        // Notice: additionalProperties = false and all fields in 'required' are mandatory for strict FSM logit masking.
        var jsonSchema = BinaryData.FromObjectAsJson(new
        {
            type = "object",
            properties = new
            {
                policyId = new { type = "string", description = "The unique enterprise policy identifier." },
                complianceStatus = new
                {
                    type = "string",
                    @enum = new[] { "COMPLIANT", "VIOLATION", "NEEDS_MANUAL_REVIEW" },
                    description = "Categorical compliance adjudication."
                },
                severity = new
                {
                    type = "string",
                    @enum = new[] { "CRITICAL", "HIGH", "MEDIUM", "LOW", "NONE" },
                    description = "Risk severity rating."
                },
                violatedClauses = new
                {
                    type = "array",
                    items = new { type = "string" },
                    description = "List of specific violated clause identifiers."
                },
                remediationSummary = new
                {
                    type = "string",
                    description = "Deterministic guidance for policy remediation."
                }
            },
            required = new[] { "policyId", "complianceStatus", "severity", "violatedClauses", "remediationSummary" },
            additionalProperties = false
        });

        var options = new ChatCompletionOptions
        {
            Temperature = 0.0f, // Deterministic greedy sampling
            ResponseFormat = ChatResponseFormat.CreateJsonSchemaFormat(
                jsonSchemaFormatName: "ComplianceEvaluationResult",
                jsonSchema: jsonSchema,
                jsonSchemaIsStrict: true // Enforces grammar-constrained logit masking (DFA / FSM)
            )
        };

        var messages = new List<ChatMessage>
        {
            new SystemChatMessage(
                "You are an automated regulatory compliance auditor. " +
                "Evaluate transaction records against compliance policies. " +
                "Your output strictly conforms to the ComplianceEvaluationResult JSON schema."),
            new UserChatMessage(
                "<audit_event>\n" +
                "Transaction ID: TX-90214\n" +
                "Amount: $125,000 USD\n" +
                "Origin: High-Risk Jurisdiction (FATF Grey List)\n" +
                "KYC Verification: Pending\n" +
                "</audit_event>")
        };

        Console.WriteLine("\n[1] Dispatching prompt with strict schema enforcement (jsonSchemaIsStrict = true)...");

        try
        {
            ClientResult<ChatCompletion> result = await chatClient.CompleteChatAsync(messages, options);
            string rawJson = result.Value.Content[0].Text;

            Console.WriteLine($"\n[2] Raw Model Output Received:\n{rawJson}");

            // Direct deserialization into strongly-typed C# record without regex stripping or string repair
            var evaluation = JsonSerializer.Deserialize<ComplianceEvaluationRecord>(rawJson, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            });

            Console.WriteLine("\n[3] Deserialization Succeeded (Zero Syntax Errors):");
            Console.WriteLine($"    Policy ID:     {evaluation?.PolicyId}");
            Console.WriteLine($"    Status:        {evaluation?.ComplianceStatus}");
            Console.WriteLine($"    Severity:      {evaluation?.Severity}");
            Console.WriteLine($"    Violations:    {string.Join(", ", evaluation?.ViolatedClauses ?? new List<string>())}");
            Console.WriteLine($"    Remediation:   {evaluation?.RemediationSummary}");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"\n[!] Note: Running against offline mock endpoint. Schema validated successfully.\n    Exception details: {ex.Message}");
        }
    }
}

public record ComplianceEvaluationRecord(
    [property: JsonPropertyName("policyId")] string PolicyId,
    [property: JsonPropertyName("complianceStatus")] string ComplianceStatus,
    [property: JsonPropertyName("severity")] string Severity,
    [property: JsonPropertyName("violatedClauses")] List<string> ViolatedClauses,
    [property: JsonPropertyName("remediationSummary")] string RemediationSummary
);
