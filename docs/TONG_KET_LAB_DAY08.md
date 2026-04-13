# 🏆 TỔNG KẾT LAB DAY 08 — RAG PIPELINE

## Mục tiêu bài lab

Xây dựng **hệ thống RAG (Retrieval-Augmented Generation)** hoàn chỉnh qua 4 Sprint, trả lời câu hỏi chính sách nội bộ doanh nghiệp dựa trên tài liệu thực — không bịa đặt (hallucination), có trích dẫn nguồn, và đánh giá được chất lượng bằng số liệu.

### Mục tiêu cụ thể (theo SCORING.md)

| # | Mục tiêu | Trọng số | Đạt? |
|---|----------|---------|------|
| 1 | Code chạy end-to-end (index → retrieval → generation → eval) | 20 điểm | ✅ |
| 2 | Tài liệu kỹ thuật (architecture.md + tuning-log.md) | 10 điểm | ✅ |
| 3 | Grading Questions — chạy 10 câu ẩn + log | 30 điểm | ⏳ 17:00 |
| 4 | Báo cáo cá nhân — 5 người × 500-800 từ | 30 điểm | ✅ |
| 5 | Code Contribution Evidence | 10 điểm | ✅ |
| **Bonus** | LLM-as-Judge + gq06 Full + timestamp hợp lệ | +5 điểm | ✅ LLM-as-Judge đã implement |

---

## Kết quả đạt được

### Sprint 1: Indexing Pipeline ✅
- **5 tài liệu** chính sách nội bộ (SLA, Hoàn tiền, Access Control, IT FAQ, Nghỉ phép)
- **29 chunks** được index vào ChromaDB (cosine similarity)
- **5 metadata fields** mỗi chunk: `source`, `department`, `effective_date`, `access`, `section`
- **Embedding model**: `paraphrase-multilingual-MiniLM-L12-v2` (384 dimensions, chạy local)
- **Chunking strategy**: Heading-based splitting theo `=== Section ===` + paragraph overlap ~80 tokens

### Sprint 2: Retrieval + Generation ✅
- **Dense retrieval**: ChromaDB cosine similarity → top-10 candidates
- **Grounded prompt**: 4 quy tắc (evidence-only, abstain, citation, short/clear)
- **LLM**: GPT-4o-mini (temperature=0)
- **Citation**: Tự động gắn [1], [2], [3] vào câu trả lời

### Sprint 3: Tuning — Hybrid + Rerank ✅
- **Sparse retrieval**: BM25Okapi cho keyword matching
- **Hybrid**: Reciprocal Rank Fusion (RRF) với dense_weight=0.6, sparse_weight=0.4
- **Cross-Encoder Rerank**: `ms-marco-MiniLM-L-6-v2` → funnel top-10 → top-3
- **Kết quả A/B**: Faithfulness **+0.40** (ít bịa hơn), Relevance −0.30 (abstain nhiều hơn)

### Sprint 4: Evaluation ✅
- **LLM-as-Judge**: GPT-4o-mini chấm 4 metrics (Faithfulness, Relevance, Context Recall, Completeness)
- **Baseline scorecard**: F=3.80, R=4.10, Rc=5.00, C=4.10
- **Variant scorecard**: F=4.20, R=3.80, Rc=5.00, C=3.80
- **A/B Comparison**: CSV + per-question analysis
- **Grading Log**: JSON format chuẩn theo SCORING.md

### Bonus: Web UI — Gemini-style Chat Interface ✅
- Dark mode, gradient logo, typing animation
- Chuyển đổi Dense / Hybrid / Hybrid+Rerank bằng 1 click
- Source chips, chunks inspector, config badge

---

## Bảng điểm 10 câu hỏi test (nội bộ)

| # | Câu hỏi | Đáp án pipeline | Điểm |
|---|---------|----------------|------|
| q01 | SLA P1 bao lâu? | 15 phút phản hồi + 4 giờ xử lý [1] | **Full** ✅ |
| q02 | Hoàn tiền mấy ngày? | 7 ngày làm việc [1] | **Full** ✅ |
| q03 | Phê duyệt Level 3? | Line Manager + IT Admin + IT Security [2] | **Full** ✅ |
| q04 | KTS có hoàn tiền? | Không — ngoại lệ license key [1] | **Full** ✅ |
| q05 | Khóa bao nhiêu lần? | 5 lần, reset qua SSO [1] | **Full** ✅ |
| q06 | Escalation P1? | 10 phút → Senior Engineer [2] | **Partial** ⚠️ |
| q07 | Approval Matrix? | Baseline partial / Variant abstain | **Partial** ⚠️ |
| q08 | Remote mấy ngày? | 2 ngày/tuần, phê duyệt HR Portal [1] | **Full** ✅ |
| q09 | ERR-403-AUTH? | "Không đủ dữ liệu" — abstain đúng ✓ | **Full** ✅ |
| q10 | VIP hoàn tiền khác? | "Không đủ dữ liệu" — abstain đúng ✓ | **Full** ✅ |

**Tổng: 8 Full + 2 Partial = 90/100 ước tính**
**Hallucination: 0/10 câu** — Không có trường hợp bịa thông tin

---

## Phân công nhóm (5 thành viên)

| # | Vai trò | Code phụ trách | Báo cáo cá nhân |
|---|---------|---------------|-----------------|
| TV1 | **Tech Lead** | `index.py` (Sprint 1) + kiến trúc | Phân tích q07 (alias matching) |
| TV2 | Retrieval Owner | `rag_answer.py` (Sprint 2+3) | Phân tích q01 (Reranker fix) |
| TV3 | Eval Owner — Baseline | `eval.py` (Faithfulness + Relevance) | Phân tích q09 (abstain) |
| TV4 | Eval Owner — Variant | `eval.py` (Context Recall + A/B) | Phân tích q10 (partial context) |
| TV5 | Documentation Owner | `docs/` + `test_questions.json` | Phân tích q04 (exception) |

---

## RAG UI Demo — Giao diện Gemini-style

### Cách chạy

```powershell
cd "d:\Antigravity\AI_thucchien\Day-08-RAG Pipeline"
$env:PYTHONIOENCODING="utf-8"
python app.py
# Mở trình duyệt: http://localhost:5000
```

### Screenshot 1: Trang chào mừng

Giao diện dark mode với gradient logo, 4 câu hỏi gợi ý, selector chế độ retrieval (Dense/Hybrid/Hybrid+Rerank):

![Trang chào mừng RAG Assistant](docs/screenshots/01_welcome.png)

### Screenshot 2: Chat trả lời có citation

Pipeline nhận câu hỏi "SLA xử lý ticket P1 là bao lâu?" → trả lời "4 giờ khắc phục, 15 phút phản hồi ban đầu **[1]**" với source chips hiện rõ tài liệu trích dẫn (`sla-p1-2026.pdf`):

![Chat trả lời với citation](docs/screenshots/02_chat_answer.png)

### Screenshot 3: Chunks Inspector + Abstain

Mở rộng xem 3 chunks retrieved với điểm score. Câu hỏi không có đáp án trong docs → pipeline abstain đúng ("Không đủ dữ liệu trong tài liệu hiện có"):

![Chunks inspector và abstain](docs/screenshots/03_chunks_abstain.png)

### Tính năng giao diện

| Tính năng | Mô tả |
|-----------|-------|
| 🌙 Dark mode | Gemini-style dark theme với gradient accent |
| 💬 Chat UI | Bubble messages, typing animation dots |
| 🔄 Mode selector | Chuyển Dense / Hybrid / Hybrid+Rerank bằng 1 click |
| 📎 Source chips | Hiển thị tên tài liệu trích dẫn dạng tag |
| 🔍 Chunks inspector | Xem chi tiết chunks retrieved + cosine score |
| ⚙️ Config badge | Hiện retrieval_mode, rerank, top_k cho mỗi response |
| 💡 Suggestions | 4 câu hỏi gợi ý nhanh trên trang chào |

### Kiến trúc Web

```
┌─────────────────────┐     POST /api/ask      ┌──────────────────┐
│   Browser (HTML/JS)  │ ──────────────────────▶ │   Flask (app.py)  │
│   Gemini-style UI    │ ◀────────────────────── │   JSON response   │
└─────────────────────┘                         └────────┬─────────┘
                                                         │
                                                         ▼
                                                ┌──────────────────┐
                                                │  rag_answer()     │
                                                │  ChromaDB + LLM   │
                                                └──────────────────┘
```

---

## Cấu trúc thư mục hoàn chỉnh

```
Day-08-RAG Pipeline/
├── index.py                          # Sprint 1: Indexing pipeline
├── rag_answer.py                     # Sprint 2+3: Retrieval + Generation
├── eval.py                           # Sprint 4: Evaluation + A/B
├── app.py                            # Web server (Flask)
├── demo.py                           # CLI demo script
├── requirements.txt                  # Dependencies
├── .env                              # API keys (không push)
├── .gitignore                        # Loại trừ .env, chroma_db
│
├── data/
│   ├── docs/                         # 5 tài liệu chính sách
│   │   ├── access_control_sop.txt
│   │   ├── hr_leave_policy.txt
│   │   ├── it_helpdesk_faq.txt
│   │   ├── policy_refund_v4.txt
│   │   └── sla_p1_2026.txt
│   └── test_questions.json           # 10 câu test + expected answers
│
├── chroma_db/                        # ChromaDB index (local, không push)
│
├── web/
│   └── index.html                    # Gemini-style chat UI
│
├── logs/
│   └── grading_run.json              # Log chạy 10 câu
│
├── results/
│   ├── scorecard_baseline.md         # Điểm Dense baseline
│   ├── scorecard_variant.md          # Điểm Hybrid+Rerank
│   └── ab_comparison.csv             # So sánh A/B chi tiết
│
├── docs/
│   ├── architecture.md               # Thiết kế pipeline
│   ├── tuning-log.md                 # Nhật ký A/B experiment
│   └── screenshots/                  # Screenshots giao diện
│       ├── 01_welcome.png
│       ├── 02_chat_answer.png
│       └── 03_chunks_abstain.png
│
├── reports/
│   ├── group_report.md               # Báo cáo nhóm
│   └── individual/
│       ├── template.md               # Template gốc
│       ├── 2A202600500_Trinh-Ke-Tien.md  # Tech Lead
│       ├── thanh_vien_2.md           # Retrieval Owner
│       ├── thanh_vien_3.md           # Eval Owner (Baseline)
│       ├── thanh_vien_4.md           # Eval Owner (Variant)
│       └── thanh_vien_5.md           # Documentation Owner
│
├── BAO_CAO_LY_THUYET_DAY08.md       # Báo cáo lý thuyết
├── README.md                         # Hướng dẫn sử dụng
└── SCORING.md                        # Rubric chấm điểm
```

---

## Kết luận

Bài lab Day 08 đã hoàn thành **100% yêu cầu kỹ thuật** với kết quả vượt kỳ vọng:

1. **Zero hallucination** trên 10 câu test — pipeline chỉ trả lời từ tài liệu hoặc abstain
2. **Context Recall 5.0/5** — retriever luôn tìm đúng tài liệu cần thiết
3. **A/B Testing có số liệu** — Faithfulness tăng +0.40 khi dùng Hybrid+Rerank
4. **Giao diện demo** — Gemini-style chat giúp trình bày trực quan trước lớp
5. **LLM-as-Judge** — đánh giá tự động thay vì chấm thủ công (bonus +2 điểm)
