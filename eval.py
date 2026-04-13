"""
eval.py — Sprint 4: Evaluation & Scorecard (HOÀN CHỈNH)
========================================================
- Chạy 10 test questions qua pipeline
- Chấm 4 metrics: Faithfulness, Relevance, Context Recall, Completeness
- Hỗ trợ cả LLM-as-Judge (tự động) và Manual scoring
- So sánh baseline vs variant (A/B)
- Xuất scorecard markdown

Chạy:  python eval.py
"""

import json
import csv
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from rag_answer import rag_answer, call_llm

# =============================================================================
# CONFIG
# =============================================================================
TEST_QUESTIONS_PATH = Path(__file__).parent / "data" / "test_questions.json"
RESULTS_DIR = Path(__file__).parent / "results"
LOGS_DIR = Path(__file__).parent / "logs"

BASELINE_CONFIG = {
    "retrieval_mode": "dense",
    "top_k_search": 10,
    "top_k_select": 3,
    "use_rerank": False,
    "label": "baseline_dense",
}

VARIANT_CONFIG = {
    "retrieval_mode": "hybrid",
    "top_k_search": 10,
    "top_k_select": 3,
    "use_rerank": True,
    "label": "variant_hybrid_rerank",
}


# =============================================================================
# LLM-AS-JUDGE: Scoring Functions
# =============================================================================
def _judge_prompt(metric: str, query: str, answer: str,
                  chunks_text: str = "", expected: str = "") -> str:
    """Tạo prompt cho LLM-as-Judge để chấm 1 metric."""

    if metric == "faithfulness":
        return f"""Bạn là giám khảo đánh giá RAG pipeline. Hãy chấm điểm FAITHFULNESS (độ trung thực).

TIÊU CHÍ: Mọi thông tin trong câu trả lời có xuất phát từ tài liệu retrieved (context) không?
- 5: Mọi thông tin đều có trong context
- 4: Gần như hoàn toàn grounded, 1 chi tiết nhỏ không chắc
- 3: Phần lớn grounded, một số thông tin có thể từ model knowledge
- 2: Nhiều thông tin không có trong context
- 1: Câu trả lời chủ yếu bịa (hallucination)

Context đã retrieve:
{chunks_text}

Câu trả lời cần chấm:
{answer}

Trả lời ĐÚNG format JSON (không thêm gì khác):
{{"score": <1-5>, "reason": "<giải thích ngắn>"}}"""

    elif metric == "relevance":
        return f"""Bạn là giám khảo đánh giá RAG pipeline. Hãy chấm điểm ANSWER RELEVANCE (độ liên quan).

TIÊU CHÍ: Câu trả lời có giải quyết đúng trọng tâm câu hỏi không?
- 5: Trả lời trực tiếp, đầy đủ
- 4: Đúng nhưng thiếu vài chi tiết phụ
- 3: Có liên quan nhưng chưa đúng trọng tâm
- 2: Lạc đề một phần
- 1: Không trả lời câu hỏi

Câu hỏi: {query}
Câu trả lời: {answer}

Trả lời ĐÚNG format JSON (không thêm gì khác):
{{"score": <1-5>, "reason": "<giải thích ngắn>"}}"""

    elif metric == "completeness":
        return f"""Bạn là giám khảo đánh giá RAG pipeline. Hãy chấm điểm COMPLETENESS (độ đầy đủ).

TIÊU CHÍ: So sánh câu trả lời với expected answer. Có bỏ sót thông tin quan trọng nào không?
- 5: Bao gồm đủ tất cả điểm quan trọng
- 4: Thiếu 1 chi tiết nhỏ
- 3: Thiếu một số thông tin quan trọng
- 2: Thiếu nhiều thông tin
- 1: Thiếu phần lớn nội dung cốt lõi

Câu hỏi: {query}
Câu trả lời: {answer}
Expected answer: {expected}

Trả lời ĐÚNG format JSON (không thêm gì khác):
{{"score": <1-5>, "reason": "<giải thích ngắn>"}}"""

    return ""


def _parse_judge_response(response: str) -> Dict[str, Any]:
    """Parse JSON response từ LLM-as-Judge."""
    try:
        # Tìm JSON trong response (có thể có text bao quanh)
        import re
        json_match = re.search(r'\{[^{}]*\}', response)
        if json_match:
            data = json.loads(json_match.group())
            return {
                "score": int(data.get("score", 0)),
                "notes": data.get("reason", ""),
            }
    except (json.JSONDecodeError, ValueError):
        pass

    return {"score": None, "notes": f"Parse error: {response[:100]}"}


def score_faithfulness(answer: str, chunks_used: List[Dict]) -> Dict[str, Any]:
    """Chấm Faithfulness bằng LLM-as-Judge."""
    chunks_text = "\n---\n".join([c.get("text", "") for c in chunks_used])
    prompt = _judge_prompt("faithfulness", "", answer, chunks_text=chunks_text)

    try:
        response = call_llm(prompt)
        return _parse_judge_response(response)
    except Exception as e:
        return {"score": None, "notes": f"LLM Judge error: {e}"}


def score_answer_relevance(query: str, answer: str) -> Dict[str, Any]:
    """Chấm Answer Relevance bằng LLM-as-Judge."""
    prompt = _judge_prompt("relevance", query, answer)

    try:
        response = call_llm(prompt)
        return _parse_judge_response(response)
    except Exception as e:
        return {"score": None, "notes": f"LLM Judge error: {e}"}


def score_context_recall(
    chunks_used: List[Dict], expected_sources: List[str]
) -> Dict[str, Any]:
    """
    Chấm Context Recall — đo bằng rule-based (không cần LLM).
    recall = (số expected source được retrieve) / (tổng expected sources)
    """
    if not expected_sources:
        return {"score": None, "recall": None, "notes": "No expected sources (abstain question)"}

    retrieved_sources = set()
    for c in chunks_used:
        src = c.get("metadata", {}).get("source", "")
        retrieved_sources.add(src.lower())

    found = 0
    missing = []
    for expected in expected_sources:
        # Partial match: tìm tên file (bỏ path, bỏ extension)
        expected_clean = expected.split("/")[-1].replace(".pdf", "").replace(".md", "").replace(".txt", "").lower()
        matched = any(expected_clean in r for r in retrieved_sources)
        if matched:
            found += 1
        else:
            missing.append(expected)

    recall = found / len(expected_sources)

    return {
        "score": max(1, round(recall * 5)),  # Scale to 1-5
        "recall": round(recall, 2),
        "found": found,
        "total": len(expected_sources),
        "missing": missing,
        "notes": f"Recall={recall:.0%} ({found}/{len(expected_sources)})"
                 + (f" Missing: {missing}" if missing else ""),
    }


def score_completeness(query: str, answer: str, expected_answer: str) -> Dict[str, Any]:
    """Chấm Completeness bằng LLM-as-Judge."""
    if not expected_answer:
        return {"score": None, "notes": "No expected answer provided"}

    prompt = _judge_prompt("completeness", query, answer, expected=expected_answer)

    try:
        response = call_llm(prompt)
        return _parse_judge_response(response)
    except Exception as e:
        return {"score": None, "notes": f"LLM Judge error: {e}"}


# =============================================================================
# SCORECARD
# =============================================================================
def run_scorecard(
    config: Dict[str, Any],
    test_questions: Optional[List[Dict]] = None,
    verbose: bool = True,
) -> List[Dict[str, Any]]:
    """
    Chạy toàn bộ test questions và chấm 4 metrics.
    Returns list of scorecard rows.
    """
    if test_questions is None:
        with open(TEST_QUESTIONS_PATH, "r", encoding="utf-8") as f:
            test_questions = json.load(f)

    label = config.get("label", "unnamed")
    results = []

    print(f"\n{'='*70}")
    print(f"📝 Scorecard: {label}")
    print(f"   Config: mode={config.get('retrieval_mode')}, "
          f"rerank={config.get('use_rerank')}, "
          f"top_k={config.get('top_k_select')}")
    print('='*70)

    for q in test_questions:
        qid = q["id"]
        query = q["question"]
        expected_answer = q.get("expected_answer", "")
        expected_sources = q.get("expected_sources", [])
        category = q.get("category", "")

        if verbose:
            print(f"\n[{qid}] {query}")

        # --- Gọi pipeline ---
        try:
            result = rag_answer(
                query=query,
                retrieval_mode=config.get("retrieval_mode", "dense"),
                top_k_search=config.get("top_k_search", 10),
                top_k_select=config.get("top_k_select", 3),
                use_rerank=config.get("use_rerank", False),
                verbose=False,
            )
            answer = result["answer"]
            chunks_used = result["chunks_used"]
            sources = result["sources"]

        except Exception as e:
            answer = f"PIPELINE_ERROR: {e}"
            chunks_used = []
            sources = []

        # --- Chấm 4 metrics ---
        if verbose:
            print(f"  Answer: {answer[:150]}...")

        faith = score_faithfulness(answer, chunks_used)
        relevance = score_answer_relevance(query, answer)
        recall = score_context_recall(chunks_used, expected_sources)
        complete = score_completeness(query, answer, expected_answer)

        row = {
            "id": qid,
            "category": category,
            "query": query,
            "answer": answer,
            "expected_answer": expected_answer,
            "sources": sources,
            "faithfulness": faith.get("score"),
            "faithfulness_notes": faith.get("notes", ""),
            "relevance": relevance.get("score"),
            "relevance_notes": relevance.get("notes", ""),
            "context_recall": recall.get("score"),
            "context_recall_notes": recall.get("notes", ""),
            "completeness": complete.get("score"),
            "completeness_notes": complete.get("notes", ""),
            "config_label": label,
        }
        results.append(row)

        if verbose:
            print(f"  Scores → F:{faith.get('score')} R:{relevance.get('score')} "
                  f"Rc:{recall.get('score')} C:{complete.get('score')}")

    # Summary
    print(f"\n{'─'*50}")
    print(f"📊 Summary: {label}")
    for metric in ["faithfulness", "relevance", "context_recall", "completeness"]:
        scores = [r[metric] for r in results if r[metric] is not None]
        avg = sum(scores) / len(scores) if scores else None
        if avg:
            print(f"  {metric:<20} {avg:.2f}/5  (n={len(scores)})")
        else:
            print(f"  {metric:<20} N/A")

    return results


# =============================================================================
# A/B COMPARISON
# =============================================================================
def compare_ab(
    baseline_results: List[Dict],
    variant_results: List[Dict],
    output_csv: Optional[str] = None,
) -> None:
    """So sánh baseline vs variant: tổng thể + per-question."""
    metrics = ["faithfulness", "relevance", "context_recall", "completeness"]

    print(f"\n{'='*70}")
    print("📊 A/B Comparison: Baseline vs Variant")
    print('='*70)
    print(f"{'Metric':<22} {'Baseline':>10} {'Variant':>10} {'Delta':>8}")
    print("─" * 55)

    for metric in metrics:
        b_scores = [r[metric] for r in baseline_results if r[metric] is not None]
        v_scores = [r[metric] for r in variant_results if r[metric] is not None]

        b_avg = sum(b_scores) / len(b_scores) if b_scores else None
        v_avg = sum(v_scores) / len(v_scores) if v_scores else None
        delta = (v_avg - b_avg) if (b_avg and v_avg) else None

        b_str = f"{b_avg:.2f}" if b_avg else "N/A"
        v_str = f"{v_avg:.2f}" if v_avg else "N/A"
        d_str = f"{delta:+.2f}" if delta is not None else "N/A"

        print(f"  {metric:<20} {b_str:>10} {v_str:>10} {d_str:>8}")

    # Per-question
    print(f"\n{'ID':<6} {'Category':<20} {'Base':>6} {'Var':>6} {'Winner':<10}")
    print("─" * 55)

    b_by_id = {r["id"]: r for r in baseline_results}
    for v_row in variant_results:
        qid = v_row["id"]
        b_row = b_by_id.get(qid, {})
        cat = v_row.get("category", "")

        b_total = sum(b_row.get(m, 0) or 0 for m in metrics)
        v_total = sum(v_row.get(m, 0) or 0 for m in metrics)
        winner = "Variant ✓" if v_total > b_total else ("Baseline" if b_total > v_total else "Tie")

        print(f"  {qid:<6} {cat:<20} {b_total:>4}/20 {v_total:>4}/20 {winner:<10}")

    # Export CSV
    if output_csv:
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        csv_path = RESULTS_DIR / output_csv
        combined = baseline_results + variant_results
        if combined:
            keys = [k for k in combined[0].keys() if k != "chunks_used"]
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(combined)
            print(f"\n  ✓ CSV saved: {csv_path}")


# =============================================================================
# SCORECARD EXPORT (Markdown)
# =============================================================================
def generate_scorecard_md(results: List[Dict], label: str) -> str:
    """Tạo scorecard dạng Markdown."""
    metrics = ["faithfulness", "relevance", "context_recall", "completeness"]
    averages = {}
    for m in metrics:
        scores = [r[m] for r in results if r[m] is not None]
        averages[m] = sum(scores) / len(scores) if scores else None

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    md = f"""# Scorecard: {label}

**Generated:** {ts}
**Config:** {label}

## Average Scores

| Metric | Score |
|--------|-------|
"""
    for m, avg in averages.items():
        avg_str = f"{avg:.2f}/5" if avg else "N/A"
        md += f"| {m.replace('_', ' ').title()} | {avg_str} |\n"

    md += "\n## Per-Question Results\n\n"
    md += "| ID | Category | F | R | Rc | C | Answer Preview |\n"
    md += "|---|---|---|---|---|---|---|\n"

    for r in results:
        ans_preview = r.get("answer", "")[:80].replace("|", "\\|").replace("\n", " ")
        md += (f"| {r['id']} | {r.get('category','')} "
               f"| {r.get('faithfulness', '-')} "
               f"| {r.get('relevance', '-')} "
               f"| {r.get('context_recall', '-')} "
               f"| {r.get('completeness', '-')} "
               f"| {ans_preview} |\n")

    md += "\n## Detailed Notes\n\n"
    for r in results:
        md += f"### [{r['id']}] {r.get('query','')}\n\n"
        md += f"**Answer:** {r.get('answer','')}\n\n"
        md += f"- Faithfulness ({r.get('faithfulness','-')}): {r.get('faithfulness_notes','')}\n"
        md += f"- Relevance ({r.get('relevance','-')}): {r.get('relevance_notes','')}\n"
        md += f"- Context Recall ({r.get('context_recall','-')}): {r.get('context_recall_notes','')}\n"
        md += f"- Completeness ({r.get('completeness','-')}): {r.get('completeness_notes','')}\n\n"

    return md


# =============================================================================
# GRADING LOG
# =============================================================================
def generate_grading_log(
    test_questions: List[Dict],
    config: Dict[str, Any],
    output_path: Path = None,
) -> List[Dict]:
    """
    Chạy pipeline cho grading questions và xuất log JSON.
    Format theo yêu cầu SCORING.md.
    """
    log = []

    for q in test_questions:
        print(f"  Running [{q['id']}] {q['question'][:50]}...")
        try:
            result = rag_answer(
                q["question"],
                retrieval_mode=config.get("retrieval_mode", "hybrid"),
                top_k_search=config.get("top_k_search", 10),
                top_k_select=config.get("top_k_select", 3),
                use_rerank=config.get("use_rerank", True),
                verbose=False,
            )
            entry = {
                "id": q["id"],
                "question": q["question"],
                "answer": result["answer"],
                "sources": result["sources"],
                "chunks_retrieved": len(result["chunks_used"]),
                "retrieval_mode": result["config"]["retrieval_mode"],
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            entry = {
                "id": q["id"],
                "question": q["question"],
                "answer": f"PIPELINE_ERROR: {e}",
                "sources": [],
                "chunks_retrieved": 0,
                "retrieval_mode": config.get("retrieval_mode", "unknown"),
                "timestamp": datetime.now().isoformat(),
            }
        log.append(entry)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(log, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Log saved: {output_path}")

    return log


# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Sprint 4: Evaluation & Scorecard")
    print("=" * 60)

    # Load test questions
    print(f"\nLoading test questions...")
    with open(TEST_QUESTIONS_PATH, "r", encoding="utf-8") as f:
        test_questions = json.load(f)
    print(f"  ✓ {len(test_questions)} câu hỏi loaded")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # ─── Baseline ───
    print("\n\n" + "=" * 60)
    print("PHASE 1: Baseline Scorecard (Dense)")
    print("=" * 60)

    baseline_results = run_scorecard(BASELINE_CONFIG, test_questions, verbose=True)

    baseline_md = generate_scorecard_md(baseline_results, BASELINE_CONFIG["label"])
    (RESULTS_DIR / "scorecard_baseline.md").write_text(baseline_md, encoding="utf-8")
    print(f"\n  ✓ Saved: results/scorecard_baseline.md")

    # ─── Variant ───
    print("\n\n" + "=" * 60)
    print("PHASE 2: Variant Scorecard (Hybrid + Rerank)")
    print("=" * 60)

    variant_results = run_scorecard(VARIANT_CONFIG, test_questions, verbose=True)

    variant_md = generate_scorecard_md(variant_results, VARIANT_CONFIG["label"])
    (RESULTS_DIR / "scorecard_variant.md").write_text(variant_md, encoding="utf-8")
    print(f"\n  ✓ Saved: results/scorecard_variant.md")

    # ─── A/B Comparison ───
    print("\n\n" + "=" * 60)
    print("PHASE 3: A/B Comparison")
    print("=" * 60)

    compare_ab(baseline_results, variant_results, output_csv="ab_comparison.csv")

    # ─── Grading Log ───
    print("\n\n" + "=" * 60)
    print("PHASE 4: Grading Run Log")
    print("=" * 60)

    # Dùng config tốt nhất (variant) cho grading
    grading_log = generate_grading_log(
        test_questions,
        config=VARIANT_CONFIG,
        output_path=LOGS_DIR / "grading_run.json",
    )

    print(f"\n\n{'='*60}")
    print("✓ Sprint 4 HOÀN THÀNH!")
    print(f"{'='*60}")
    print(f"  results/scorecard_baseline.md")
    print(f"  results/scorecard_variant.md")
    print(f"  results/ab_comparison.csv")
    print(f"  logs/grading_run.json")
