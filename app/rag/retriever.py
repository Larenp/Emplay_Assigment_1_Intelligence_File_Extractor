import faiss
import numpy as np

from app.rag.embedder import create_embeddings


def create_index(chunks: list[str]):
    """
    Create a FAISS index from text chunks.
    """

    embeddings = create_embeddings(chunks)

    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])

    index.add(embeddings)

    return index


def retrieve(
    query: str,
    chunks: list[str],
    index,
    top_k: int = 5
) -> list[str]:
    """
    Retrieve the most relevant chunks for a query.
    """

    query_embedding = create_embeddings([query])

    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    return [chunks[i] for i in indices[0]]