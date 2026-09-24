from pathlib import Path

from app.ingestion.file_scanner import scan_input_folders
from app.parsers.parser import parse_document
from app.processing.text_cleaner import process_text

from app.rag.chunker import create_chunks
from app.rag.retriever import create_index
from app.rag.store import load_rag_data, save_rag_data

from app.extraction.pipeline import (
    extract_test_fields,
    build_final_extraction,
)

from app.output.json_writer import save_extraction


INPUT_DIR = Path("data/input")


def prepare_rag_data(document):
    """
    Create or load the RAG data for a document.

    RAG data consists of:
    - text chunks
    - embeddings
    - FAISS index
    """

    cached_data = load_rag_data(document.document_id)

    if cached_data is not None:
        print("      RAG cache .......... loaded")
        chunks, index = cached_data
        print(f"      Chunks ............. {len(chunks)}")
        return chunks, index

    print("      RAG cache .......... not found")
    print("      Creating chunks...")

    processed = process_text(document.text)
    cleaned_text = processed["cleaned_text"]

    if not cleaned_text.strip():
        raise ValueError(
            "Document contains no extractable text."
        )

    # Use the complete cleaned document for RAG.
    # We do not depend on automatic section detection.
    sections = [
        {
            "title": "Document",
            "content": cleaned_text.splitlines(),
        }
    ]

    chunks = create_chunks(
        sections=sections,
        chunk_size=250,
        overlap=50,
    )

    if not chunks:
        raise ValueError(
            "No RAG chunks could be created."
        )

    print(f"      Chunks created ...... {len(chunks)}")
    print("      Creating embeddings and FAISS index...")

    index = create_index(chunks)

    save_rag_data(
        document_id=document.document_id,
        chunks=chunks,
        index=index,
    )

    print("      RAG cache .......... saved")

    return chunks, index
def process_single_document(
    file_path: Path,
    document_number: int,
    total_documents: int,
):
    """
    Process one HTML/PDF document from start to finish.
    """

    print("\n" + "=" * 80)
    print(
        f"[{document_number}/{total_documents}] "
        f"{file_path.name}"
    )
    print("=" * 80)

    try:

        # --------------------------------------------------
        # 1. Parse document
        # --------------------------------------------------

        print("      Parsing ............", end=" ")

        document = parse_document(file_path)

        print("✓")

        print(f"      Type ............... {document.file_type}")
        print(
            f"      Characters ......... {len(document.text):,}"
        )

        if not document.text.strip():
            raise ValueError(
                "No text could be extracted from document."
            )

        # --------------------------------------------------
        # 2. Prepare RAG
        # --------------------------------------------------

        chunks, index = prepare_rag_data(document)

        # --------------------------------------------------
        # 3. Run hybrid extraction
        # --------------------------------------------------

        print("      Extraction ......... starting")

        results = extract_test_fields(
            text=document.text,
            chunks=chunks,
            index=index,
        )

        print("      Extraction ......... ✓")

        # --------------------------------------------------
        # 4. Validate result
        # --------------------------------------------------

        final_result = build_final_extraction(results)

        print("      Validation ......... ✓")

        # --------------------------------------------------
        # 5. Save JSON
        # --------------------------------------------------

        output_path = save_extraction(
            extraction=final_result,
            document_id=document.document_id,
        )

        print("      JSON ............... ✓")
        print(f"      Output ............. {output_path}")

        return {
            "success": True,
            "file": file_path,
            "output": output_path,
            "document": document,
        }

    except Exception as error:

        print("      ✗ FAILED")

        print(
            f"      Error: {type(error).__name__}: {error}"
        )

        return {
            "success": False,
            "file": file_path,
            "error": error,
        }


def main():
    """
    Process every supported document under data/input/.
    """

    print("=" * 80)
    print("RFP INTELLIGENCE EXTRACTOR")
    print("BATCH DOCUMENT PROCESSING")
    print("=" * 80)

    # ------------------------------------------------------
    # Discover documents
    # ------------------------------------------------------

    print("\nScanning input directory...")

    documents = scan_input_folders(
        str(INPUT_DIR)
    )

    if not documents:
        print("\nNo supported documents found.")
        return

    total_documents = len(documents)

    print(
        f"Found {total_documents} supported documents."
    )

    for file_path in documents:
        print(f"  - {file_path}")

    # ------------------------------------------------------
    # Process documents
    # ------------------------------------------------------

    results = []

    for document_number, file_path in enumerate(
        documents,
        start=1,
    ):

        result = process_single_document(
            file_path=file_path,
            document_number=document_number,
            total_documents=total_documents,
        )

        results.append(result)

    # ------------------------------------------------------
    # Final summary
    # ------------------------------------------------------

    successful = [
        result
        for result in results
        if result["success"]
    ]

    failed = [
        result
        for result in results
        if not result["success"]
    ]

    print("\n" + "=" * 80)
    print("BATCH PROCESSING COMPLETE")
    print("=" * 80)

    print(
        f"\nTotal documents : {total_documents}"
    )

    print(
        f"Successful      : {len(successful)}"
    )

    print(
        f"Failed          : {len(failed)}"
    )

    if successful:

        print("\nSuccessful outputs:")

        for result in successful:
            print(
                f"  ✓ {result['output']}"
            )

    if failed:

        print("\nFailed documents:")

        for result in failed:
            print(
                f"  ✗ {result['file']}"
            )
            print(
                f"    {type(result['error']).__name__}: "
                f"{result['error']}"
            )

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()