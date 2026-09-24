from app.extraction.llm_extractor import (
    FIELD_QUERIES,
    extract_single_field,
)
from app.extraction.rule_extractor import extract_rule_based
from app.extraction.schema import RFPExtraction
from app.rag.retriever import retrieve


FIELD_TOP_K = {
    "bid_number": 2,
    "title": 2,
    "due_date": 2,
    "bid_submission_type": 3,
    "term_of_bid": 2,
    "pre_bid_meeting": 2,
    "installation": 3,
    "bid_bond_requirement": 3,
    "delivery_date": 3,
    "payment_terms": 3,
    "additional_documentation_required": 3,
    "mfg_for_registration": 2,
    "contract_or_cooperative": 3,
    "model_no": 2,
    "part_no": 2,
    "product": 2,
    "contact_info": 2,
    "company_name": 2,
    "bid_summary": 3,
    "product_specification": 4,
}


def retrieve_field_context(
    field_name: str,
    chunks: list[str],
    index,
    top_k: int = 2,
) -> str:
    """
    Retrieve relevant RAG chunks for a specific extraction field.
    """

    queries = FIELD_QUERIES[field_name]

    retrieved = []

    for query in queries:
        results = retrieve(
            query=query,
            chunks=chunks,
            index=index,
            top_k=top_k,
        )

        retrieved.extend(results)

    # Remove duplicate chunks while preserving order.
    unique_results = list(dict.fromkeys(retrieved))

    return "\n\n".join(unique_results)


def normalize_multivalue_fields(results: dict) -> dict:
    """
    Convert multiline LLM responses into lists for fields
    that naturally contain multiple values.
    """

    fields = [
        "bid_submission_type",
        "installation",
        "additional_documentation_required",
        "product_specification",
    ]

    for field in fields:

        value = results.get(field)

        if not value:
            continue

        # Already normalized.
        if isinstance(value, list):
            continue

        if isinstance(value, str):

            items = []

            for line in value.splitlines():

                line = line.strip()

                if not line:
                    continue

                # Remove common bullet characters.
                line = line.lstrip("-•*").strip()

                if line:
                    items.append(line)

            results[field] = items

    return results


def extract_test_fields(
    text: str,
    chunks: list[str],
    index,
) -> dict:

    print("\n" + "=" * 60)
    print("RULE-BASED EXTRACTION")
    print("=" * 60)

    rule_results = extract_rule_based(text)

    for field, values in rule_results.items():
        print(f"{field}: {values}")

    results = {}

    fields = list(FIELD_QUERIES.keys())

    for field_name in fields:

        print("\n" + "=" * 60)
        print(f"FIELD: {field_name}")
        print("=" * 60)

        field_top_k = FIELD_TOP_K.get(field_name, 2)

        print(
            f"Retrieving relevant chunks (top_k={field_top_k})..."
        )

        context = retrieve_field_context(
            field_name=field_name,
            chunks=chunks,
            index=index,
            top_k=field_top_k,
        )

        print("\nRetrieved context:")
        print(context)

        print("\nRunning Gemma...")

        value = extract_single_field(
            field_name=field_name,
            context=context,
        )

        results[field_name] = value

        print(f"\nRESULT: {value}")

    # ---------------------------------------------------------
    # Deterministic rule-based overrides
    # ---------------------------------------------------------

    if rule_results["rfp_numbers"]:
        results["bid_number"] = rule_results["rfp_numbers"][0]

    # ---------------------------------------------------------
    # Build contact information from deterministic extraction
    # ---------------------------------------------------------

    contact_parts = []

    if rule_results["emails"]:
        contact_parts.append(
            "Email: " + ", ".join(rule_results["emails"])
        )

    if rule_results["phone_numbers"]:
        contact_parts.append(
            "Phone: " + ", ".join(rule_results["phone_numbers"])
        )

    if contact_parts:
        results["contact_info"] = " | ".join(contact_parts)

    # ---------------------------------------------------------
    # Clean title
    # ---------------------------------------------------------

    if results.get("title"):

        title = results["title"]

        prefixes = [
            "Request For Proposal",
            "Request for Proposal",
            "REQUEST FOR PROPOSAL",
        ]

        for prefix in prefixes:

            if title.startswith(prefix):
                title = title[len(prefix):].strip()

        if results.get("bid_number"):
            title = title.replace(
                results["bid_number"],
                "",
            ).strip()

        results["title"] = title

    # ---------------------------------------------------------
    # Normalize fields that contain multiple values
    # ---------------------------------------------------------

    results = normalize_multivalue_fields(results)

    return results


def build_final_extraction(results: dict) -> RFPExtraction:
    """
    Validate the extracted data against the RFP schema.
    """

    results = normalize_multivalue_fields(results)

    return RFPExtraction(**results)