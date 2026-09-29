# ADR-001: PostgreSQL `pgvector 0.7+` vs. Dedicated Vector Engines (Qdrant / Milvus)

## Status
`ACCEPTED` (Universal Enterprise Default up to 10M Vectors)

---

## Context & Problem Statement
As our engineering division scales retrieval-augmented generation (RAG) and semantic search workflows, we must establish a standard vector database primitive. 

The team is divided between two schools of thought:
1. **The Specialized Vector DB Camp:** Proponents argue that dedicated vector databases (e.g., Qdrant, Milvus, Pinecone) offer superior approximate nearest neighbor (ANN) recall, native scalar filtering, and distributed clustering.
2. **The Relational Co-location Camp:** Proponents argue that adopting PostgreSQL with the `pgvector 0.7+` extension eliminates dual-write synchronization bugs, allows unified ACID transactions, and simplifies operations on existing managed cloud infrastructure (AWS Aurora / Azure Database for PostgreSQL).

---

## Decision Drivers
1. **Operational Simplicity & Total Cost of Ownership (TCO):** Minimize the number of stateful distributed databases that require on-call rotations, security patching, backup configurations, and network peering.
2. **Data Consistency & Relational Joins:** The ability to perform atomic transactions where document metadata, user access control lists (RBAC), and vector embeddings are updated simultaneously.
3. **Query Latency & Concurrency:** Maintain P99 search latency < 40ms under 500 concurrent read queries per second.
4. **Scale Horizon:** Support our 3-year projected data footprint of **2.5 million document chunks (1536-dimensional embeddings)** without requiring cluster re-architecting.

---

## Considered Alternatives

### Alternative 1: Dedicated Vector Database (Qdrant / Milvus)
* **Pros:** Highly tuned Rust/Go distributed engines; native hybrid search (dense + sparse SPLADE); specialized hardware offloading; advanced quantization (Scalar & Product Quantization).
* **Cons:** Introduces a second distributed database; requires building dual-write synchronization pipelines (Kafka/CDC) to mirror relational metadata; independent RBAC and compliance surface.

### Alternative 2: PostgreSQL with `pgvector 0.7+` (HNSW Indexing + `halfvec`)
* **Pros:** Single database for relational data, full-text search, and vector embeddings; strict ACID guarantees; zero ETL synchronization delay; supported natively in managed cloud engines; `halfvec` (16-bit float) and FP8 quantization reduce RAM by 50–75%.
* **Cons:** Memory intensive for large graphs; HNSW index builds require significant CPU/RAM; non-optimal for massive scale (>20M vectors) without horizontal sharding (Citus).

### Alternative 3: Managed Serverless Vector Index (Pinecone)
* **Pros:** Zero cluster maintenance; auto-scaling throughput.
* **Cons:** High variable cost (\$0.04 to \$0.10 per 1k searches at scale); vendor lock-in; data leaves enterprise VPC boundary, requiring complex security approvals.

---

## Decision Outcome
* **Chosen Option:** **Alternative 2: PostgreSQL with `pgvector 0.7+` as the enterprise default**, with a documented threshold to migrate to **Qdrant** only if scale exceeds **10 million vectors** or sustained query QPS exceeds **1,500 req/sec**.

### Architectural Decision Threshold Formula
```text
Storage Target <= 10,000,000 vectors AND QPS <= 1,500 ⟹ PostgreSQL (pgvector)
Storage Target >  10,000,000 vectors OR  QPS >  1,500 ⟹ Dedicated Qdrant Cluster
```

---

## Architectural Trade-Off Scorecard

| Evaluation Criterion | PostgreSQL `pgvector 0.7+` | Dedicated Qdrant | Serverless Pinecone |
| :--- | :---: | :---: | :---: |
| **ACID Metadata Consistency** | **Superior (Same DB)** | Weak (Requires CDC) | Weak (External Sync) |
| **P99 Latency (at 2M vectors)** | **28ms (HNSW)** | 18ms (Native Rust) | 45ms (Network Hop) |
| **Operational Overhead** | **Near Zero (Existing Aurora)** | High (New Cluster) | Low (SaaS Managed) |
| **Monthly Infrastructure TCO** | **~$450 (Included in DB)** | ~$1,800 (Managed VMs) | ~$2,400 (Usage Based) |
| **Memory Efficiency** | **High (`halfvec` / 16-bit)** | Extreme (Int8 PQ) | High (Opaque) |
| **VPC Data Privacy** | **100% In-VPC** | 100% In-VPC | External SaaS |

---

## Implementation Policy & Mandatory Rules

1. **Mandatory Indexing Standard:** Always use **HNSW (`m=16, ef_construction=64`)** rather than `ivfflat`. Never run production queries without an active index:
   ```sql
   CREATE INDEX CONCURRENTLY idx_documents_embedding_hnsw 
   ON enterprise_documents 
   USING hnsw (embedding vector_cosine_ops) 
   WITH (m = 16, ef_construction = 64);
   ```
2. **Quantization with `halfvec`:** For embeddings with dimension D >= 1536, use the `halfvec` data type to cut VRAM consumption by 50%:
   ```sql
   ALTER TABLE enterprise_documents ADD COLUMN embedding_fp16 halfvec(1536);
   ```
3. **RAM Sizing Rule of Thumb:** Ensure PostgreSQL `shared_buffers` plus OS cache can hold the entire HNSW index in memory:
   ```text
   RAM_Index ≈ Vectors × Dimensions × 2 bytes (halfvec) × 1.25 (Graph Overhead)
   ```
   *For 2.5M vectors at 1536-dim:* `2,500,000 × 1536 × 2 × 1.25 ≈ 9.6 GB RAM`.

---

## Negative Consequences & Mitigations

* **Consequence 1: High Index Build Times:** Building HNSW on millions of rows can lock CPU cores.  
  → **Mitigation:** Always use `CREATE INDEX CONCURRENTLY` and scale `maintenance_work_mem` to 4 GB during backfill operations.
* **Consequence 2: Vector Cache Eviction under Heavy OLTP Load:** Transactional table writes competing with vector searches can cause cache thrashing.  
  → **Mitigation:** Route all vector searches to a dedicated **Aurora Read Replica** isolated from OLTP write traffic.
