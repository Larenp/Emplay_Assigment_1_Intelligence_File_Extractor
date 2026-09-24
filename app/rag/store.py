from pathlib import Path
import pickle

import faiss


CACHE_DIR = Path("data/cache")


def get_cache_paths(document_id: str):
    document_cache_dir = CACHE_DIR / document_id
    document_cache_dir.mkdir(parents=True, exist_ok=True)

    return {
        "chunks": document_cache_dir / "chunks.pkl",
        "index": document_cache_dir / "faiss.index",
    }


def save_rag_data(
    document_id: str,
    chunks: list[str],
    index
):
    paths = get_cache_paths(document_id)

    with open(paths["chunks"], "wb") as file:
        pickle.dump(chunks, file)

    faiss.write_index(
        index,
        str(paths["index"])
    )


def load_rag_data(document_id: str):
    paths = get_cache_paths(document_id)

    if not paths["chunks"].exists():
        return None

    if not paths["index"].exists():
        return None

    with open(paths["chunks"], "rb") as file:
        chunks = pickle.load(file)

    index = faiss.read_index(
        str(paths["index"])
    )

    return chunks, index