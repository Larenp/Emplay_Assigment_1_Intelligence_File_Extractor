import faiss
import numpy as np

from app.rag.embedder import create_embeddings


def create_index(chunks: list[str]):
    embeddings = create_embeddings(chunks)

    embeddings = np.array(
        embeddings
    ).astype("float32")

    index = faiss.IndexFlatL2(
        embeddings.shape[1]
    )

    index.add(embeddings)

    return index


def retrieve(
    query: str,
    chunks: list[str],
    index,
    top_k: int = 5,
) -> list[str]:

    query_embedding = create_embeddings(
        [query]
    )

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    top_k = min(
        top_k,
        len(chunks)
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for i in indices[0]:
        if 0 <= i < len(chunks):
            results.append(chunks[i])

    return results