import ollama

from app.extraction.schema import RFPExtraction


MODEL_NAME = "gemma3:4b"


def extract_rfp_information(context: str) -> RFPExtraction:
    """
    Extract structured RFP information using a local Ollama model.
    """

    prompt = f"""
You are an RFP information extraction system.

Extract the following fields from the document context.

FIELD INSTRUCTIONS:

1. rfp_number
   Extract the RFP or solicitation number.

2. proposal_due_date
   Extract the date and time when the proposal/solicitation is due.
   Look specifically for phrases such as:
   - Solicitation Due
   - Proposal Due
   - Bid Due
   - Submission Deadline

3. contract_duration
   Extract the complete contract term, including extensions.
   Preserve the wording from the document.

4. scope
   Extract the description of what goods or services the RFP is requesting.

5. requirements
   Extract important requirements that vendors must satisfy.

6. eligibility_requirements
   Extract requirements that determine whether a vendor is eligible to participate.

7. evaluation_criteria
   Extract criteria used to evaluate proposals.

8. submission_requirements
   Extract documents, information, plans, forms, or other items that vendors must submit.

IMPORTANT RULES:
- Use ONLY information contained in the context.
- Do not invent information.
- If a field is not supported by the context, leave it empty.
- Preserve important wording from the source.
- Extract complete information rather than short fragments.

DOCUMENT CONTEXT:
{context}
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format=RFPExtraction.model_json_schema()
    )

    return RFPExtraction.model_validate_json(
        response["message"]["content"]
    )
    