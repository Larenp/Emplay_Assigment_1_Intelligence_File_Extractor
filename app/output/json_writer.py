import json
from pathlib import Path

from app.extraction.schema import RFPExtraction


OUTPUT_DIR = Path("data/output")


def save_extraction(
    extraction: RFPExtraction,
    document_id: str,
) -> Path:
    """
    Save the final RFP extraction as formatted JSON.
    """

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = OUTPUT_DIR / f"{document_id}.json"

    data = extraction.model_dump(
        exclude_none=False
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )

    return output_path