// Program.cs - .NET 9 Enterprise RAG Pipeline
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;
using Azure;
using Azure.Search.Documents;
using Azure.Search.Documents.Models;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;

namespace EnterpriseRag.AzureSearch
{
    public record DocumentChunk(
        string ChunkId,
        string DocumentId,
        string Title,
        string Content,
        string TenantId,
        int PageNumber
    );

    public class AzureSearchRetrievalService
    {
        private readonly SearchClient _searchClient;

        public AzureSearchRetrievalService(string endpointUri, string indexName, string apiKey)
        {
            var endpoint = new Uri(endpointUri);
            var credential = new AzureKeyCredential(apiKey);
            _searchClient = new SearchClient(endpoint, indexName, credential);
        }

        /// <summary>
        /// Executes Multi-Stage Hybrid Search with Native Semantic Reranking and RBAC Tenant Filtering.
        /// </summary>
        public async Task<List<DocumentChunk>> RetrieveGroundedContextAsync(
            string userQuery,
            ReadOnlyMemory<float> queryEmbedding,
            string tenantId,
            int topK = 5)
        {
            var searchOptions = new SearchOptions
            {
                Size = topK,
                // Strict Pre-Filtering: Ensure zero cross-tenant information leakage
                Filter = $"tenantId eq '{tenantId}'",
                // Enable Azure AI Search Semantic Reranker (Turing Cross-Encoder)
                QueryType = SearchQueryType.Semantic,
                SemanticSearch = new SemanticSearchOptions
                {
                    SemanticConfigurationName = "my-semantic-config",
                    QueryCaption = new QueryCaption(QueryCaptionType.Extractive),
                    QueryAnswer = new QueryAnswer(QueryAnswerType.Extractive)
                }
            };

            // Configure Hybrid Vector Query
            searchOptions.VectorSearch = new VectorSearchOptions();
            searchOptions.VectorSearch.Queries.Add(new VectorizedQuery(queryEmbedding)
            {
                KNearestNeighborsCount = 50,
                Fields = { "contentVector" }
            });

            // Execute Hybrid Search: userQuery drives BM25; VectorizedQuery drives HNSW
            SearchResults<SearchDocument> response = await _searchClient.SearchAsync<SearchDocument>(
                userQuery,
                searchOptions);

            var retrievedChunks = new List<DocumentChunk>();

            await foreach (SearchResult<SearchDocument> result in response.GetResultsAsync())
            {
                var doc = result.Document;
                retrievedChunks.Add(new DocumentChunk(
                    ChunkId: doc["chunkId"].ToString()!,
                    DocumentId: doc["documentId"].ToString()!,
                    Title: doc["title"].ToString()!,
                    Content: doc["content"].ToString()!,
                    TenantId: doc["tenantId"].ToString()!,
                    PageNumber: Convert.ToInt32(doc["pageNumber"])
                ));
            }

            return retrievedChunks;
        }
    }

    public class GroundedRAGSynthesizer
    {
        private readonly Kernel _kernel;
        private readonly IChatCompletionService _chatService;

        public GroundedRAGSynthesizer(string openAiApiKey, string modelId = "gpt-4o")
        {
            var builder = Kernel.CreateBuilder();
            builder.AddOpenAIChatCompletion(modelId, openAiApiKey);
            _kernel = builder.Build();
            _chatService = _kernel.GetRequiredService<IChatCompletionService>();
        }

        public async Task<string> GenerateGroundedAnswerAsync(
            string userQuery,
            List<DocumentChunk> evidenceChunks)
        {
            var chatHistory = new ChatHistory();

            // Strict Anti-Hallucination System Prompt
            chatHistory.AddSystemMessage(
                "You are an enterprise AI knowledge assistant. You must answer the user's query " +
                "STRICTLY using the provided context documents inside the <context> block.\n" +
                "RULES:\n" +
                "1. Every factual statement you make must be attributed to a chunk using inline format [ChunkId:Page].\n" +
                "2. If the answer cannot be directly deduced from the provided context, you MUST state: " +
                "'I do not have sufficient authoritative evidence to answer this question.'\n" +
                "3. Do not extrapolate, assume, or leverage ungrounded outside knowledge.");

            // Construct Context Block
            var contextBuilder = new StringBuilder();
            contextBuilder.AppendLine("<context>");
            foreach (var chunk in evidenceChunks)
            {
                contextBuilder.AppendLine($"  <document_chunk id=\"{chunk.ChunkId}\" doc=\"{chunk.DocumentId}\" page=\"{chunk.PageNumber}\">");
                contextBuilder.AppendLine($"    Title: {chunk.Title}");
                contextBuilder.AppendLine($"    Body: {chunk.Content}");
                contextBuilder.AppendLine("  </document_chunk>");
            }
            contextBuilder.AppendLine("</context>");

            chatHistory.AddUserMessage($"{contextBuilder}\n\nUser Question: {userQuery}");

            var response = await _chatService.GetChatMessageContentAsync(
                chatHistory,
                kernel: _kernel);

            return response.Content ?? string.Empty;
        }
    }
}
