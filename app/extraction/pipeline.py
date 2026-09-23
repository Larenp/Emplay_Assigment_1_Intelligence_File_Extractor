from app.rag.retriever import retrieve
from app.extraction.llm_extractor import extract_rfp_information


def extract_from_rfp(
    chunks: list[str],
    index
):
    """
    Retrieve relevant chunks for each RFP field
    and extract structured information using the local LLM.
    """

    queries = [
        "RFP number or solicitation number",
        "proposal due date solicitation due bid due submission deadline",
        "contract duration contract term extensions",
        "scope goods services requested by the RFP",
        "vendor requirements minimum requirements specifications",
        "vendor eligibility requirements qualifications",
        "proposal evaluation criteria scoring points",
        "proposal submission requirements documents forms information"
    ]

    retrieved_chunks = []

    for query in queries:
        results = retrieve(
            query=query,
            chunks=chunks,
            index=index,
            top_k=3
        )

        retrieved_chunks.extend(results)

    # Remove duplicate chunks while preserving order
    unique_chunks = list(dict.fromkeys(retrieved_chunks))

    context = "\n\n".join(unique_chunks)

    return extract_rfp_information(context)