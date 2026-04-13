"""
index.py — Sprint 1: Build RAG Index (HOÀN CHỈNH)
===================================================
Pipeline: Docs → Preprocess → Chunk → Embed → Store (ChromaDB)

Chạy:  python index.py
Output: ChromaDB index tại ./chroma_db/ với đầy đủ metadata
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# CONFIG
# =============================================================================
DOCS_DIR = Path(__file__).parent / "data" / "docs"
CHROMA_DB_DIR = Path(__file__).parent / "chroma_db"
COLLECTION_NAME = "rag_lab"

CHUNK_SIZE = 400        # target tokens (~1600 ký tự)
CHUNK_OVERLAP = 80      # overlap tokens (~320 ký tự)
CHARS_PER_TOKEN = 4     # ước lượng

EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "local")

# Cache embedding model (Singleton) để không load lại mỗi lần gọi
_embedding_model = None


# =============================================================================
# EMBEDDING
# =============================================================================
def get_embedding_model():
    """Load model embedding một lần duy nhất (Singleton pattern)."""
    global _embedding_model
    if _embedding_model is not None:
        return _embedding_model

    if EMBEDDING_PROVIDER == "openai":
        from openai import OpenAI
        _embedding_model = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    else:
        from sentence_transformers import SentenceTransformer
        print("  Loading local embedding model (lần đầu sẽ tải ~130MB)...")
        _embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        print("  ✓ Model loaded!")
    return _embedding_model


def get_embedding(text: str) -> List[float]:
    """
    Tạo embedding vector cho một đoạn text.
    Hỗ trợ cả OpenAI API và Sentence Transformers (local).
    """
    model = get_embedding_model()

    if EMBEDDING_PROVIDER == "openai":
        response = model.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    else:
        # Sentence Transformers — chạy local, miễn phí
        return model.encode(text).tolist()


# =============================================================================
# PREPROCESS
# =============================================================================
def preprocess_document(raw_text: str, filepath: str) -> Dict[str, Any]:
    """
    Tiền xử lý tài liệu:
    1. Extract metadata từ header (Source, Department, Effective Date, Access)
    2. Loại bỏ dòng header metadata khỏi nội dung chính
    3. Normalize khoảng trắng
    """
    lines = raw_text.strip().split("\n")
    metadata = {
        "source": Path(filepath).stem,
        "department": "unknown",
        "effective_date": "unknown",
        "access": "internal",
    }
    content_lines = []
    header_done = False

    for line in lines:
        if not header_done:
            stripped = line.strip()
            if stripped.startswith("Source:"):
                metadata["source"] = stripped.replace("Source:", "").strip()
            elif stripped.startswith("Department:"):
                metadata["department"] = stripped.replace("Department:", "").strip()
            elif stripped.startswith("Effective Date:"):
                metadata["effective_date"] = stripped.replace("Effective Date:", "").strip()
            elif stripped.startswith("Access:"):
                metadata["access"] = stripped.replace("Access:", "").strip()
            elif stripped.startswith("==="):
                header_done = True
                content_lines.append(line)
            elif stripped == "" or stripped.isupper() or stripped.startswith("Ghi chú:"):
                # Dòng tên tài liệu (toàn hoa) hoặc dòng trống trong header → bỏ qua
                continue
        else:
            content_lines.append(line)

    cleaned_text = "\n".join(content_lines)
    # Normalize: tối đa 2 dòng trống liên tiếp
    cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text)

    return {"text": cleaned_text, "metadata": metadata}


# =============================================================================
# CHUNKING
# =============================================================================
def chunk_document(doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Chunk tài liệu theo cấu trúc tự nhiên:
    1. Split theo heading "=== Section ... ===" trước
    2. Nếu section dài → tiếp tục split theo paragraph (\n\n)
    3. Overlap giữa các chunk liên tiếp trong cùng section
    4. Metadata gốc được giữ nguyên cho mỗi chunk
    """
    text = doc["text"]
    base_metadata = doc["metadata"].copy()
    chunks = []

    # Split theo heading pattern "=== ... ==="
    sections = re.split(r"(===\s*.*?\s*===)", text)

    current_section = "General"
    current_text = ""

    for part in sections:
        heading_match = re.match(r"===\s*(.*?)\s*===", part)
        if heading_match:
            # Lưu section trước nếu có nội dung
            if current_text.strip():
                section_chunks = _split_section_by_paragraphs(
                    current_text.strip(), base_metadata, current_section
                )
                chunks.extend(section_chunks)
            # Bắt đầu section mới
            current_section = heading_match.group(1).strip()
            current_text = ""
        else:
            current_text += part

    # Section cuối cùng
    if current_text.strip():
        section_chunks = _split_section_by_paragraphs(
            current_text.strip(), base_metadata, current_section
        )
        chunks.extend(section_chunks)

    return chunks


def _split_section_by_paragraphs(
    text: str,
    base_metadata: Dict,
    section: str,
    max_chars: int = None,
    overlap_chars: int = None,
) -> List[Dict[str, Any]]:
    """
    Split section theo paragraph boundaries với overlap.
    Ưu tiên cắt tại dấu xuống dòng kép (\n\n) — ranh giới tự nhiên.
    """
    if max_chars is None:
        max_chars = CHUNK_SIZE * CHARS_PER_TOKEN
    if overlap_chars is None:
        overlap_chars = CHUNK_OVERLAP * CHARS_PER_TOKEN

    # Nếu toàn bộ section vừa 1 chunk → trả về luôn
    if len(text) <= max_chars:
        return [{
            "text": text,
            "metadata": {**base_metadata, "section": section},
        }]

    # Split theo paragraph
    paragraphs = text.split("\n\n")

    chunks = []
    current_chunk_parts = []
    current_length = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        para_len = len(para) + 2  # +2 cho "\n\n" nối lại

        if current_length + para_len > max_chars and current_chunk_parts:
            # Lưu chunk hiện tại
            chunk_text = "\n\n".join(current_chunk_parts)
            chunks.append({
                "text": chunk_text,
                "metadata": {**base_metadata, "section": section},
            })

            # Overlap: giữ lại paragraph cuối để tạo ngữ cảnh chuyển tiếp
            overlap_parts = []
            overlap_len = 0
            for p in reversed(current_chunk_parts):
                if overlap_len + len(p) > overlap_chars:
                    break
                overlap_parts.insert(0, p)
                overlap_len += len(p)

            current_chunk_parts = overlap_parts
            current_length = overlap_len

        current_chunk_parts.append(para)
        current_length += para_len

    # Chunk cuối cùng
    if current_chunk_parts:
        chunk_text = "\n\n".join(current_chunk_parts)
        chunks.append({
            "text": chunk_text,
            "metadata": {**base_metadata, "section": section},
        })

    return chunks


# =============================================================================
# BUILD INDEX
# =============================================================================
def build_index(docs_dir: Path = DOCS_DIR, db_dir: Path = CHROMA_DB_DIR) -> int:
    """
    Pipeline hoàn chỉnh: đọc docs → preprocess → chunk → embed → store vào ChromaDB.
    Returns: Tổng số chunks đã index.
    """
    import chromadb

    print(f"\n{'='*60}")
    print("Sprint 1: Build RAG Index")
    print(f"{'='*60}")
    print(f"  Docs dir: {docs_dir}")
    print(f"  DB dir:   {db_dir}")
    print(f"  Embedding: {EMBEDDING_PROVIDER}")

    db_dir.mkdir(parents=True, exist_ok=True)

    # Khởi tạo ChromaDB
    client = chromadb.PersistentClient(path=str(db_dir))

    # Xóa collection cũ nếu tồn tại (re-index sạch)
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"  ✓ Đã xóa collection cũ '{COLLECTION_NAME}'")
    except Exception:
        pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )
    print(f"  ✓ Tạo collection '{COLLECTION_NAME}' (cosine similarity)")

    doc_files = sorted(docs_dir.glob("*.txt"))
    if not doc_files:
        print(f"  ✗ Không tìm thấy file .txt trong {docs_dir}")
        return 0

    print(f"\n  Tìm thấy {len(doc_files)} tài liệu:")
    for f in doc_files:
        print(f"    - {f.name}")

    # Load embedding model
    print(f"\n  Loading embedding model...")
    get_embedding_model()

    total_chunks = 0
    all_chunks_info = []

    for filepath in doc_files:
        print(f"\n  Processing: {filepath.name}")
        raw_text = filepath.read_text(encoding="utf-8")

        # Preprocess
        doc = preprocess_document(raw_text, str(filepath))
        print(f"    Metadata: source={doc['metadata']['source']}, "
              f"dept={doc['metadata']['department']}, "
              f"date={doc['metadata']['effective_date']}")

        # Chunk
        chunks = chunk_document(doc)
        print(f"    Chunks: {len(chunks)} đoạn")

        # Embed và upsert vào ChromaDB
        for i, chunk in enumerate(chunks):
            chunk_id = f"{filepath.stem}_chunk_{i:03d}"
            embedding = get_embedding(chunk["text"])

            collection.upsert(
                ids=[chunk_id],
                embeddings=[embedding],
                documents=[chunk["text"]],
                metadatas=[chunk["metadata"]],
            )

            all_chunks_info.append({
                "id": chunk_id,
                "source": chunk["metadata"]["source"],
                "section": chunk["metadata"]["section"],
                "chars": len(chunk["text"]),
            })

        total_chunks += len(chunks)
        print(f"    ✓ {len(chunks)} chunks embedded và upsert vào ChromaDB")

    print(f"\n{'='*60}")
    print(f"✓ HOÀN THÀNH! Tổng: {total_chunks} chunks từ {len(doc_files)} tài liệu")
    print(f"  Database: {db_dir}")
    print(f"{'='*60}")

    return total_chunks


# =============================================================================
# INSPECT / DEBUG
# =============================================================================
def list_chunks(db_dir: Path = CHROMA_DB_DIR, n: int = 5) -> None:
    """In ra n chunk đầu tiên để kiểm tra chất lượng index."""
    import chromadb
    client = chromadb.PersistentClient(path=str(db_dir))

    try:
        collection = client.get_collection(COLLECTION_NAME)
    except Exception as e:
        print(f"✗ Chưa có index. Chạy build_index() trước. ({e})")
        return

    results = collection.get(limit=n, include=["documents", "metadatas"])

    print(f"\n=== Top {n} chunks trong index ===\n")
    for i, (doc_id, doc, meta) in enumerate(
        zip(results["ids"], results["documents"], results["metadatas"])
    ):
        print(f"[Chunk {i+1}] ID: {doc_id}")
        print(f"  Source:    {meta.get('source', 'N/A')}")
        print(f"  Section:   {meta.get('section', 'N/A')}")
        print(f"  Date:      {meta.get('effective_date', 'N/A')}")
        print(f"  Dept:      {meta.get('department', 'N/A')}")
        print(f"  Text [{len(doc)} chars]: {doc[:150]}...")
        print()


def inspect_metadata_coverage(db_dir: Path = CHROMA_DB_DIR) -> None:
    """Phân tích phân bố metadata trong toàn bộ index."""
    import chromadb
    client = chromadb.PersistentClient(path=str(db_dir))

    try:
        collection = client.get_collection(COLLECTION_NAME)
    except Exception:
        print("✗ Chưa có index.")
        return

    results = collection.get(include=["metadatas"])
    total = len(results["metadatas"])
    print(f"\n=== Metadata Coverage ({total} chunks) ===\n")

    departments = {}
    sources = {}
    sections = {}
    missing_date = 0

    for meta in results["metadatas"]:
        dept = meta.get("department", "unknown")
        departments[dept] = departments.get(dept, 0) + 1

        src = meta.get("source", "unknown")
        sources[src] = sources.get(src, 0) + 1

        sec = meta.get("section", "N/A")
        sections[sec] = sections.get(sec, 0) + 1

        if meta.get("effective_date") in ("unknown", "", None):
            missing_date += 1

    print("Phân bố theo Department:")
    for dept, count in sorted(departments.items()):
        print(f"  {dept}: {count} chunks")

    print(f"\nPhân bố theo Source:")
    for src, count in sorted(sources.items()):
        print(f"  {src}: {count} chunks")

    print(f"\nPhân bố theo Section:")
    for sec, count in sorted(sections.items()):
        print(f"  {sec}: {count} chunks")

    print(f"\nChunks thiếu effective_date: {missing_date}/{total}")


# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    # Sprint 1: Build full index
    total = build_index()

    if total > 0:
        print("\n")
        list_chunks(n=5)
        inspect_metadata_coverage()
