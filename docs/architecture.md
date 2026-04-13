# Architecture Document — RAG Pipeline Lab Day 08

## 1. Tổng quan kiến trúc

```
┌─────────────────────────────────────────────────────────────────┐
│                     RAG PIPELINE ARCHITECTURE                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  OFFLINE PHASE (Sprint 1)                                       │
│  ┌──────┐   ┌────────────┐   ┌──────────┐   ┌───────────────┐ │
│  │ Docs │──▶│ Preprocess │──▶│ Chunking │──▶│  Embedding    │ │
│  │ (.txt)│   │ (metadata) │   │ (heading) │   │ (MiniLM-L12) │ │
│  └──────┘   └────────────┘   └──────────┘   └──────┬────────┘ │
│                                                      │          │
│                                              ┌───────▼────────┐ │
│                                              │   ChromaDB     │ │
│                                              │ (29 chunks)    │ │
│                                              └───────┬────────┘ │
│                                                      │          │
│  ONLINE PHASE (Sprint 2+3)                           │          │
│  ┌──────┐   ┌──────────────┐   ┌────────────┐       │          │
│  │Query │──▶│ Dense Search │──▶│  Rerank    │◀──────┘          │
│  └──────┘   │ + BM25 (RRF) │   │ (CrossEnc) │                  │
│             └──────────────┘   └─────┬──────┘                  │
│                                      │                          │
│                              ┌───────▼────────┐                 │
│                              │ Grounded Prompt │                 │
│                              │  + GPT-4o-mini  │                 │
│                              └───────┬────────┘                 │
│                                      │                          │
│                              ┌───────▼────────┐                 │
│                              │ Answer + [1][2] │                 │
│                              │ (with citation) │                 │
│                              └────────────────┘                 │
│                                                                 │
│  EVALUATION (Sprint 4)                                          │
│  LLM-as-Judge → 4 Metrics → Scorecard → A/B Comparison         │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Component Details

### 2.1 Indexing (index.py)
- **Documents:** 5 tài liệu chính sách nội bộ (.txt)
- **Preprocess:** Extract metadata (source, department, effective_date, access, section) từ header → loại bỏ ký tự lỗi
- **Chunking:** Heading-based splitting (theo `=== Section ===`) + paragraph overlap (~80 tokens)
- **Embedding:** `paraphrase-multilingual-MiniLM-L12-v2` (Sentence Transformers, 384 dimensions, chạy local)
- **Storage:** ChromaDB PersistentClient, cosine similarity, 29 chunks indexed

### 2.2 Retrieval (rag_answer.py)
- **Dense:** ChromaDB cosine similarity search → top-10 candidates
- **Sparse:** BM25Okapi (rank-bm25) → keyword matching cho mã lỗi/tên riêng
- **Hybrid:** Reciprocal Rank Fusion (RRF) với dense_weight=0.6, sparse_weight=0.4, K=60
- **Rerank:** Cross-Encoder `ms-marco-MiniLM-L-6-v2` → funnel top-10 → top-3

### 2.3 Generation (rag_answer.py)
- **LLM:** OpenAI GPT-4o-mini (temperature=0)
- **Prompt:** Grounded prompt 4 quy tắc: Evidence-only, Abstain, Citation [1][2], Short/Clear
- **Context Block:** Đánh số [1], [2], [3] — mỗi chunk gồm source | section | score

### 2.4 Evaluation (eval.py)
- **Metrics:** Faithfulness, Relevance, Context Recall, Completeness (1-5 scale)
- **Judge:** LLM-as-Judge (GPT-4o-mini chấm GPT-4o-mini)
- **Context Recall:** Rule-based (source matching)
- **Output:** Scorecard markdown + CSV + Grading log JSON

## 3. Metadata Fields (5 fields/chunk)

| Field | Ví dụ | Mục đích |
|-------|-------|---------|
| source | `policy/refund-v4.pdf` | Trích dẫn nguồn trong answer |
| department | `CS`, `IT`, `HR` | Pre-filtering theo phòng ban |
| effective_date | `2026-02-01` | Lọc tài liệu hết hiệu lực |
| access | `internal` | Kiểm soát quyền truy cập |
| section | `Điều 2: Điều kiện hoàn tiền` | Trích dẫn cụ thể vị trí trong tài liệu |

## 4. Kết quả Evaluation

### Baseline (Dense)
| Metric | Score |
|--------|-------|
| Faithfulness | 3.80/5 |
| Relevance | 4.10/5 |
| Context Recall | 5.00/5 |
| Completeness | 4.10/5 |

### Variant (Hybrid + Rerank)
| Metric | Score |
|--------|-------|
| Faithfulness | 4.20/5 |
| Relevance | 3.80/5 |
| Context Recall | 5.00/5 |
| Completeness | 3.80/5 |

### A/B Delta
| Metric | Delta |
|--------|-------|
| Faithfulness | **+0.40** ✓ |
| Relevance | -0.30 |
| Context Recall | 0.00 |
| Completeness | -0.30 |

> **Kết luận:** Hybrid+Rerank cải thiện Faithfulness (+0.40) — giảm hallucination. Relevance giảm nhẹ do Reranker ưu tiên chunk chính xác hơn nhưng có thể bỏ sót context bổ sung.
