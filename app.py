"""
app.py — Web Server cho RAG Pipeline (Gemini-style UI)
Chạy: python app.py → mở http://localhost:5000
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from rag_answer import rag_answer

app = Flask(__name__, template_folder="web", static_folder="web/static")
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.json
    query = data.get("query", "")
    mode = data.get("mode", "hybrid")
    use_rerank = data.get("use_rerank", True)

    if not query.strip():
        return jsonify({"error": "Cau hoi trong"}), 400

    try:
        result = rag_answer(
            query=query,
            retrieval_mode=mode,
            use_rerank=use_rerank,
            top_k_search=10,
            top_k_select=3,
            verbose=False,
        )
        chunks_info = []
        for i, c in enumerate(result["chunks_used"]):
            chunks_info.append({
                "index": i + 1,
                "source": c["metadata"].get("source", "unknown"),
                "section": c["metadata"].get("section", ""),
                "score": c.get("score", 0),
                "preview": c["text"][:200],
            })

        return jsonify({
            "answer": result["answer"],
            "sources": result["sources"],
            "chunks": chunks_info,
            "config": result["config"],
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("RAG Pipeline — Gemini-style UI")
    print("Mo trinh duyet: http://localhost:5000")
    print("=" * 50 + "\n")
    app.run(debug=False, port=5000)
