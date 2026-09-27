// ============================================================================
// File: AgentEvaluationTests.cs
// Framework: .NET 9 / xUnit / Microsoft.SemanticKernel / FluentAssertions
// Description: Automated Level 1 & Level 2 CI/CD evaluation test harness.
// ============================================================================

using System;
using System.IO;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading.Tasks;
using FluentAssertions;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Embeddings;
using Xunit;
using Xunit.Abstractions;

namespace EnterpriseAgent.Evaluations.Tests;

// ---------------------------------------------------------------------------
// Strongly Typed Agent Response Models (Level 1 Target)
// ---------------------------------------------------------------------------
public record SupportTicketPayload(
    [property: JsonPropertyName("ticket_id")] string TicketId,
    [property: JsonPropertyName("urgency")] string Urgency,
    [property: JsonPropertyName("assigned_queue")] string AssignedQueue,
    [property: JsonPropertyName("action_summary")] string ActionSummary
);

public class AgentEvaluationTestSuite
{
    private readonly ITestOutputHelper _output;
    private readonly Kernel _kernel;

    public AgentEvaluationTestSuite(ITestOutputHelper output)
    {
        _output = output;

        // Initialize Semantic Kernel with OpenAI / Azure OpenAI connectors
        var builder = Kernel.CreateBuilder();
        builder.AddOpenAIChatCompletion("gpt-4o", Environment.GetEnvironmentVariable("OPENAI_API_KEY") ?? "mock-key");
        builder.AddOpenAITextEmbeddingGeneration("text-embedding-3-small", Environment.GetEnvironmentVariable("OPENAI_API_KEY") ?? "mock-key");
        _kernel = builder.Build();
    }

    [Fact(DisplayName = "Level 1: Agent Output Conforms to Strict JSON Schema")]
    public void Test_Agent_Output_Strict_Schema_Adherence()
    {
        // Arrange: Simulated Agent Raw Output String
        string rawAgentOutput = """
        {
            "ticket_id": "TICK-9081",
            "urgency": "High",
            "assigned_queue": "DatabaseEngineering",
            "action_summary": "Identified deadlocks on cluster node 3; triggered automated failover."
        }
        """;

        // Act & Assert (Level 1 Deterministic Verification)
        Action parseAction = () =>
        {
            var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = false };
            var payload = JsonSerializer.Deserialize<SupportTicketPayload>(rawAgentOutput, options);

            payload.Should().NotBeNull();
            payload!.TicketId.Should().MatchRegex(@"^TICK-[0-9]{4,6}$");
            payload.Urgency.Should().BeOneOf("Low", "Medium", "High", "Critical");
            payload.AssignedQueue.Should().NotBeNullOrWhiteSpace();
            payload.ActionSummary.Length.Should().BeInRange(10, 300);
        };

        parseAction.Should().NotThrow("Because agent output must adhere strictly to SupportTicketPayload schema");
        _output.WriteLine("Level 1 Schema validation passed successfully.");
    }

    [Theory(DisplayName = "Level 2: Semantic Similarity Exceeds Golden Threshold")]
    [InlineData(
        "How do I reset my multi-factor authentication?",
        "To reset MFA, navigate to Security Settings > Authentication Devices, and click 'Re-enroll'.",
        "You can re-enroll your multi-factor device by visiting your account's Security Settings page.",
        0.82 // Minimum acceptable Cosine Similarity threshold
    )]
    public async Task Test_Agent_Semantic_Similarity_Against_Golden_Answer(
        string userPrompt,
        string goldenTruthAnswer,
        string actualAgentOutput,
        double minSimilarityThreshold)
    {
        // Arrange: Obtain Embedding Generator from Kernel
        var embeddingGenerator = _kernel.GetRequiredService<ITextEmbeddingGenerationService>();

        // Act: Generate embedding vectors for both golden answer and actual response
        var embeddings = await embeddingGenerator.GenerateEmbeddingsAsync([goldenTruthAnswer, actualAgentOutput]);
        var vectorGolden = embeddings[0];
        var vectorActual = embeddings[1];

        // Calculate Cosine Similarity
        double similarity = ComputeCosineSimilarity(vectorGolden.Span, vectorActual.Span);
        _output.WriteLine($"Computed Cosine Similarity: {similarity:F4} (Threshold: {minSimilarityThreshold:F2})");

        // Assert: Ensure semantic alignment without keyword brittleness
        similarity.Should().BeGreaterThanOrEqualTo(
            minSimilarityThreshold, 
            $"Agent output must maintain semantic fidelity to golden answer for query: '{userPrompt}'"
        );
    }

    // ---------------------------------------------------------------------------
    // Mathematical Vector Cosine Distance Utility
    // ---------------------------------------------------------------------------
    private static double ComputeCosineSimilarity(ReadOnlySpan<float> vectorA, ReadOnlySpan<float> vectorB)
    {
        if (vectorA.Length != vectorB.Length)
            throw new ArgumentException("Vector dimensions must match identically.");

        double dotProduct = 0.0;
        double magnitudeA = 0.0;
        double magnitudeB = 0.0;

        for (int i = 0; i < vectorA.Length; i++)
        {
            dotProduct += vectorA[i] * vectorB[i];
            magnitudeA += vectorA[i] * vectorA[i];
            magnitudeB += vectorB[i] * vectorB[i];
        }

        if (magnitudeA <= 0.0 || magnitudeB <= 0.0) return 0.0;
        return dotProduct / (Math.Sqrt(magnitudeA) * Math.Sqrt(magnitudeB));
    }
}
