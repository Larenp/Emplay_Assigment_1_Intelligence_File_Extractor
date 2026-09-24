from pathlib import Path

from app.parsers.parser import parse_document
from app.rag.store import load_rag_data
from app.extraction.pipeline import (
    extract_test_fields,
    build_final_extraction,
)
from app.output.json_writer import save_extraction


FILE_PATH = Path(
    "data/input/Bid1/"
    "JA-207652 Student and Staff Computing Devices FINAL.pdf"
)


def main():
    print("=" * 60)
    print("RFP EXTRACTION TEST")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. Parse document
    # ---------------------------------------------------------

    print("\n1. Parsing document...")

    document = parse_document(FILE_PATH)

    print(f"Document loaded: {document.filename}")

    # ---------------------------------------------------------
    # 2. Load RAG cache
    # ---------------------------------------------------------

    print("\n2. Checking RAG cache...")

    cached_data = load_rag_data(
        document.document_id
    )

    if cached_data is None:
        raise RuntimeError(
            "RAG cache not found. "
            "Run the indexing process first."
        )

    chunks, index = cached_data

    print("Cached RAG data found.")
    print(f"Chunks loaded: {len(chunks)}")

    # ---------------------------------------------------------
    # 3. Hybrid extraction
    # ---------------------------------------------------------

    print("\n3. Starting hybrid extraction...")

    results = extract_test_fields(
        text=document.text,
        chunks=chunks,
        index=index,
    )

    # ---------------------------------------------------------
    # 4. Validate against Pydantic schema
    # ---------------------------------------------------------

    final_result = build_final_extraction(
        results
    )

    # ---------------------------------------------------------
    # 5. Save JSON
    # ---------------------------------------------------------

    output_path = save_extraction(
        extraction=final_result,
        document_id=document.document_id,
    )

    print(f"\nJSON saved to: {output_path}")

    # ---------------------------------------------------------
    # 6. Display final results
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)

    for field, value in final_result.model_dump().items():
        print(f"{field}: {value}")


if __name__ == "__main__":
    main()