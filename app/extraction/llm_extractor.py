import ollama


MODEL_NAME = "gemma3:4b"


# =============================================================
# FIELD EXTRACTION INSTRUCTIONS
# =============================================================

FIELD_INSTRUCTIONS = {

    "bid_number": """
Extract the official bid number, RFP number, solicitation number,
or official bid reference number.

Return ONLY the identifier.

Do not:
- combine multiple identifiers
- include the title
- include "Request For Proposal"
- include explanatory text

Return null if no official bid/RFP number is present.
""",

    "title": """
Extract the official title of the RFP or solicitation.

Return ONLY the title.

Do not:
- include the RFP number
- include the bid number
- include "Request For Proposal"
- include page numbers
- include organization metadata
""",

    "due_date": """
Extract the official proposal/bid submission due date and time.

Do NOT return:
- advertisement date
- question deadline
- pre-bid meeting date
- award date
- delivery date
- contract duration

Return the exact date/time stated in the document.
""",

    "bid_submission_type": """
Extract the method or methods used to submit the actual BID/PROPOSAL.

Include all explicitly allowed submission methods if the document
provides more than one.

Examples:
- online/electronic submission
- physical submission
- manual sealed envelope
- sealed bid
- other explicitly stated methods

Do NOT use the method for submitting questions.

Do NOT use instructions saying questions must be submitted in writing.

Do NOT confuse proposal submission with bid opening.

Return the complete applicable submission method(s).
""",

    "term_of_bid": """
Extract the complete contract/bid term.

Include:
- initial contract term
- renewal periods
- extension periods
- maximum total duration

Express the result in natural language.

Example:
"3-year initial term with two 1-year renewal extensions,
not to exceed a total of 5 years."

Do not return only a sequence of numbers such as:
"3 + 1 + 1 + 5".
""",

    "pre_bid_meeting": """
Extract the pre-bid or pre-proposal meeting information.

Include:
- date
- time
- timezone if available
- location or virtual platform if available

Do not confuse it with:
- question deadline
- proposal due date
- bid opening
""",

    "installation": """
Extract ONLY installation, deployment, setup, and
delivery-related implementation requirements for the awarded vendor.

Include relevant requirements such as:
- device deployment
- device setup
- software installation
- asset tagging
- asset etching/decaling
- delivery-related deployment services
- white glove services
- asset reporting related to deployment

Do NOT include:
- warranty duration
- warranty effective date
- warranty repair requirements
- warranty replacement requirements
- general maintenance requirements

Do NOT return a question asking whether the vendor can provide
these services.

Return only the actual installation/deployment requirements
supported by the context.
""",

    "bid_bond_requirement": """
Extract the specific BID BOND or BID SECURITY requirement.

Include:
- amount
- percentage
- type of security
- whether it is required

IMPORTANT:

Do NOT treat general insurance requirements as a bid bond.

Do NOT treat performance bonds or payment bonds as bid bonds.

If the document only says insurance/bond requirements are
described elsewhere without giving a bid bond requirement in
the provided context, return null.
""",

    "delivery_date": """
Extract the actual required delivery date or delivery schedule.

Look for:
- required delivery date
- delivery deadline
- number of days after purchase order
- shipping/delivery schedule

Do NOT return:
- solicitation due date
- award date
- contract duration
- Purchase Order creation date
- office address
- procurement punch-out information

If no actual delivery date or delivery schedule is stated,
return null.

Return ONLY the date or delivery schedule.
Do not explain that the information was not found.
""",

    "payment_terms": """
Extract the payment terms applicable to the DISTRICT paying
the awarded vendor or contractor.

Look for:
- payment terms
- invoice requirements
- payment after delivery
- payment after acceptance
- Net 30
- Net 45
- other explicitly stated vendor payment terms

IMPORTANT:

Do NOT return payment terms between a prime vendor and subcontractor.

Do NOT return M/WBE subcontractor payment requirements.

Do NOT guess a payment term.

Return null if the vendor payment term is not supported.
""",

    "additional_documentation_required": """
Extract the additional documents, forms, certifications,
references, plans, literature, or supporting documentation
that the bidder is required to submit.

Include MULTIPLE required documents when explicitly stated.

Do not return only the first matching document.

Do not include ordinary proposal fields unless they are explicitly
required as separate documentation.
""",

    "mfg_for_registration": """
Extract a manufacturer registration requirement ONLY if the
document explicitly requires registration with a manufacturer,
OEM, or manufacturer program.

Valid examples include:
- manufacturer registration
- OEM registration
- registration with the manufacturer
- manufacturer registration number
- explicit manufacturer registration requirement

Do NOT interpret these as manufacturer registration:
- factory-authorized repair certification
- factory-authorized maintenance certification
- authorized reseller
- manufacturer authorization
- manufacturer certification

Those are different requirements.

If explicit manufacturer registration is not stated,
return null.

Return ONLY the requirement or null.
""",

    "contract_or_cooperative": """
Extract contracts, cooperative purchasing agreements,
or cooperative organizations that may be used with the
resulting contract.

Include names such as cooperative purchasing organizations
if explicitly mentioned.

Do not guess cooperative organizations.
""",

    "model_no": """
Extract the requested or specified model number.

Do not return:
- a part number
- a product name unless it is explicitly the model number
- a generic description
""",

    "part_no": """
Extract the requested or specified part number.

Do not return:
- a model number
- a product name
""",

    "product": """
Extract the main products or goods being requested by the RFP.

Keep the description concise but specific.

Include the major product categories explicitly requested.
""",

    "contact_info": """
Extract the relevant procurement/contact information.

Include:
- contact person's name
- email
- phone

when available.

Prefer the main procurement/contact information rather than
unrelated contacts appearing elsewhere.
""",

    "company_name": """
Extract the organization or company issuing the RFP.

Do not return:
- a vendor responding to the RFP
- a manufacturer
- a subcontractor
- an unrelated organization
""",

    "bid_summary": """
Provide a concise summary of what the RFP is requesting and its purpose.

Mention the major products/services being requested and important
contract information when supported by the context.

If contract duration is mentioned, preserve the exact structure
of the term.

For example, distinguish between:
- two 1-year extensions
and
- one 2-year extension.

Use ONLY information from the provided context.

Do not introduce information that is not present in the context.
""",

    "product_specification": """
Extract the important product specifications and technical
requirements.

Include relevant:
- minimum specifications
- hardware requirements
- configurations
- technical features
- warranties
- performance requirements
- required accessories
- other important technical requirements

Include multiple important specifications when available.

Do not return only one specification.
""",
}


# =============================================================
# FIELD-SPECIFIC RAG QUERIES
# =============================================================

FIELD_QUERIES = {

    "bid_number": [
        "official RFP number bid number solicitation number",
        "Request For Proposal number reference number",
    ],

    "title": [
        "official RFP title solicitation title proposal title",
        "Request For Proposal title project title",
    ],

    "due_date": [
        "Solicitation Due proposal due date bid due date",
        "proposal submission deadline receipt opening date time",
    ],

    "bid_submission_type": [
        "submit proposal bid submission method electronic online portal",
        "proposal submission instructions response submission",
        "bid submission electronic system online submission",
    ],

    "term_of_bid": [
        "initial term renewal extension contract duration",
        "contract term total years renewal options",
    ],

    "pre_bid_meeting": [
        "pre-proposal meeting pre-bid meeting date time location",
        "preproposal conference Teams meeting",
    ],

    "installation": [
        "installation software installation device setup deployment",
        "asset tagging asset etching deployment services",
        "white glove services device deployment",
    ],

    "bid_bond_requirement": [
        "bid bond bid security required amount percentage",
        "bid security requirement bid bond",
    ],

    "delivery_date": [
        "required delivery date delivery deadline",
        "delivery schedule days after purchase order",
        "shipping delivery timeline delivery period",
    ],

    "payment_terms": [
        "District payment to awarded vendor invoice payment terms",
        "vendor payment terms payment after delivery acceptance",
        "District shall pay vendor invoice",
        "Net 30 Net 45 payment terms vendor",
    ],

    "additional_documentation_required": [
        "required documentation forms certifications supporting documents",
        "documents bidder must submit proposal",
    ],

    "mfg_for_registration": [
        "manufacturer registration OEM registration authorized reseller",
        "manufacturer authorization certification",
    ],

    "contract_or_cooperative": [
        "cooperative purchasing contract cooperative agreement",
        "cooperative organization purchasing alliance",
    ],

    "model_no": [
        "model number model no requested product",
        "proposed device make and model",
    ],

    "part_no": [
        "part number part no product",
        "manufacturer part number",
    ],

    "product": [
        "products goods equipment devices requested",
        "scope products being purchased",
    ],

    "contact_info": [
        "procurement contact buyer email phone contact information",
        "procurement services buyer contact",
    ],

    "company_name": [
        "issuing organization district agency company name",
        "RFP issuing organization",
    ],

    "bid_summary": [
        "purpose of request for proposal scope",
        "what goods services are being requested",
    ],

    "product_specification": [
        "minimum product specifications technical requirements",
        "equipment requirements hardware specifications",
        "device specifications required features",
    ],
}


# =============================================================
# CLEAN LLM OUTPUT
# =============================================================

def clean_llm_value(
    value: str | None,
) -> str | None:
    """
    Normalize the raw LLM response.

    Converts common 'not found' explanations into None.
    """

    if value is None:
        return None

    value = value.strip()

    null_values = {
        "null",
        "none",
        "not found",
        "not specified",
        "not mentioned",
        "n/a",
    }

    if value.lower() in null_values:
        return None

    lower_value = value.lower()

    negative_phrases = [
        "there is no specific",
        "no specific delivery date",
        "no delivery date",
        "no delivery schedule",
        "not stated in this context",
        "not specified in this context",
        "not mentioned in this context",
    ]

    if any(
        phrase in lower_value
        for phrase in negative_phrases
    ):
        return None

    return value


# =============================================================
# SINGLE FIELD EXTRACTION
# =============================================================

def extract_single_field(
    field_name: str,
    context: str,
) -> str | None:
    """
    Extract one RFP field from the retrieved context using Gemma.
    """

    instruction = FIELD_INSTRUCTIONS[field_name]

    prompt = f"""
You are an RFP information extraction system.

{instruction}

STRICT RULES:

- Use ONLY the provided context.
- Do NOT use outside knowledge.
- Do NOT guess.
- Do NOT infer information that is not explicitly supported.
- Return null if the requested information is not supported.
- Return ONLY the extracted value.
- Do not provide explanations.
- Do not describe your reasoning.

FIELD:
{field_name}

CONTEXT:
{context}
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    value = response["message"]["content"].strip()

    return clean_llm_value(value)