from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks: list[str]):
    """
    Convert text chunks into embedding vectors.
    """
    return model.encode(chunks)



