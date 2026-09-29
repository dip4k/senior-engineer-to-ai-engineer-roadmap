# Refactoring Report: Phase 00 (Foundations & Token Mechanics)

*Phase*: `00-foundations-and-token-mechanics`  
*Executed by*: AI Curriculum Architect  
*Operating Mode*: `REFACTOR MODE`  
*Date*: September 2026  

---

## 1. Curriculum Changes
- **Decomposition of Monolith**: Decomposed the monolithic 982-line (8,102 words) `README.md` into an Orientation Hub (`README.md`, ~450 words) and 5 focused, modular lessons (`01` through `05`), aligned with the 4-Tier Depth Model.
- **Relocation of Fine-Tuning**: Relocated Parameter-Efficient Fine-Tuning (LoRA / QLoRA) from Phase 00 to Phase 07 (`04-dynamic-multi-lora-adapter-serving.md`), eliminating premature cognitive overload before prompt engineering and RAG.
- **Harmonized Learning Progression**: Structured the learning journey logically: Hardware Physics → Tokenization Mechanics → KV-Cache Dynamics → Test-Time Reasoning Compute → Small Language Models & Quantization → Capstone Lab.

---

## 2. Content Changes
- **Zero-LaTeX Enforcement**: Replaced all raw LaTeX equations (`$$...$$`, `\text{...}`, `\frac{...}{...}`) across all lessons and the capstone lab with standard GitHub Flavored Markdown (GFM) text blocks or Unicode formulas (`→`, `×`, `Σ`, `≈`).
- **Senior Systems Metaphors**: Grounded all AI primitives in traditional systems concepts (e.g. FlashAttention as SRAM cache tiling; PagedAttention as OS virtual memory paging; BPE as Huffman byte compaction; test-time compute as exam scratchpad).
- **Conciseness & High Signal**: Eliminated marketing hype, repetitive conversational padding, and passive prose, achieving tight word budgets (1,200 to 2,000 words per lesson).

---

## 3. Advanced Content
- **Roofline Model & Arithmetic Intensity**: Detailed mathematical formulation of the memory bandwidth wall, showing why decode generation on an H100 spends 99.8% of clock cycles waiting for HBM memory bus transfers.
- **Exact KV-Cache Derivation**: Provided step-by-step mathematical derivation for GQA memory footprints (`2 × 2 × Layers × H_KV × d_k × Batch × SeqLen`).
- **50:1 Thinking Token Asymmetry**: Detailed economic analysis of reasoning models (o3, Claude 3.7 Thinking, DeepSeek-R1), demonstrating how a 28-token answer can generate 5,240 hidden tokens billed as output.
- **AWQ & GPTQ Algorithms**: Documented activation-aware outlier protection (top 1% salient channels) and second-order Taylor expansion inverse Hessian compensation.

---

## 4. Diagram Changes
- Created 7 crisp Mermaid diagrams across the phase:
  1. `README.md`: Phase 00 Learning Progression flowchart with a 6-step walkthrough.
  2. `01-transformer-and-hardware-physics.md`: Scaled Dot-Product Attention Pipeline with a 4-step walkthrough.
  3. `01-transformer-and-hardware-physics.md`: Standard Attention Thrashing vs. FlashAttention Tiling with a step-by-step memory traffic comparison.
  4. `02-tokenization-and-bpe-mechanics.md`: BPE Merge Tree with a 4-step walkthrough.
  5. `02-tokenization-and-bpe-mechanics.md`: Logits to Probability Sampling Pipeline with parameter explanations.
  6. `03-kv-cache-vram-and-bandwidth-physics.md`: Prefill vs. Decode Lifecycle Sequence Diagram with step-by-step walkthrough.
  7. `03-kv-cache-vram-and-bandwidth-physics.md`: PagedAttention Virtual Page Table Mapping with frame allocation walkthrough.
  8. `04-test-time-compute-and-reasoning-models.md`: Test-Time Search & Verification Loop with PRM scoring walkthrough.
  9. `04-test-time-compute-and-reasoning-models.md`: Architectural Decision Tree for model routing.
  10. `05-slms-and-quantization-mechanics.md`: AWQ vs. GPTQ Quantization Mapping with activation analysis walkthrough.
- **Compliance**: 100% of Mermaid diagrams feature an explicit, numbered step-by-step prose walkthrough.

---

## 5. Duplication Removed
- Removed duplicated prompt caching explanations (consolidated into Phase 01).
- Removed LoRA and QLoRA fine-tuning details from the introductory phase (consolidated into Phase 07).
- Eliminated redundant definitions of temperature and sampling scattered between sections.

---

## 6. Files Changed
- **Created**:
  - `00-foundations-and-token-mechanics/01-transformer-and-hardware-physics.md` (New modular lesson)
  - `00-foundations-and-token-mechanics/02-tokenization-and-bpe-mechanics.md` (New modular lesson)
  - `00-foundations-and-token-mechanics/03-kv-cache-vram-and-bandwidth-physics.md` (New modular lesson)
  - `00-foundations-and-token-mechanics/04-test-time-compute-and-reasoning-models.md` (New modular lesson)
  - `00-foundations-and-token-mechanics/05-slms-and-quantization-mechanics.md` (New modular lesson)
  - `00-foundations-and-token-mechanics/REFACTORING_REPORT.md` (This report)
- **Modified**:
  - `00-foundations-and-token-mechanics/README.md` (Rewritten as Orientation & Navigation Hub)
  - `00-foundations-and-token-mechanics/labs/capstone-token-economics-analyzer.md` (Cleaned raw LaTeX and updated navigation link)

---

## 7. Link Changes
- Updated all intra-phase lesson navigation links (`Previous Lesson` and `Next Lesson`).
- Connected all lessons to the `capstone-token-economics-analyzer.md` lab.
- Updated root Phase 00 navigation to connect cleanly to `01-prompt-and-context-engineering/README.md`.
- Normalized all anchor links to eliminate double hyphens.

---

## 8. Cross-Phase Changes
- Flagged PEFT / LoRA content for integration into `07-production-deployment-and-llmops/04-dynamic-multi-lora-adapter-serving.md`.
- Set up clean handoff to Phase 01 (`01-prompt-and-context-engineering`) for Context Abstract Syntax Trees and Token Compaction.

---

## 9. Remaining Recommendations
- During Milestone 4 (Phase 07 refactoring), integrate the LoRA parameter reduction math and multi-adapter memory pooling mechanics extracted from Phase 00.
- Ensure `examples/token_profiler.py` and `examples/adaptation_decision_matrix.py` maintain automated test coverage in CI.
