"""Demo: Chay toan bo RAG Pipeline end-to-end"""
from index import build_index
from rag_answer import rag_answer, compare_retrieval_strategies

print("=" * 60)
print("DEMO: RAG Pipeline End-to-End")
print("=" * 60)

# Sprint 1
print("\n[SPRINT 1] Building Index...")
total = build_index()

# Sprint 2
print("\n\n[SPRINT 2] Dense Retrieval + Grounded Answer")
print("=" * 60)
queries = [
    "SLA xu ly ticket P1 la bao lau?",
    "Khach hang co the yeu cau hoan tien trong bao nhieu ngay?",
    "Ai phai phe duyet de cap quyen Level 3?",
    "Nhan vien duoc lam remote toi da may ngay moi tuan?",
]
for q in queries:
    result = rag_answer(q, retrieval_mode="dense")
    print(f"\nQ: {q}")
    print(f"A: {result['answer']}")
    print(f"Sources: {result['sources']}")

# Sprint 3
print("\n\n[SPRINT 3] Hybrid + Rerank Comparison")
compare_retrieval_strategies("SLA xu ly ticket P1 la bao lau?")

print("\n\n" + "=" * 60)
print("[DONE] Pipeline chay thanh cong!")
print("Luc 17:00 se chay lai voi grading_questions.json")
print("=" * 60)
