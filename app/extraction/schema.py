from pydantic import BaseModel


class RFPExtraction(BaseModel):
    bid_number: str | None = None
    title: str | None = None
    due_date: str | None = None
    bid_submission_type: list[str] | None = None
    term_of_bid: str | None = None
    pre_bid_meeting: str | None = None
    installation: list[str] | None = None
    bid_bond_requirement: str | None = None
    delivery_date: str | None = None
    payment_terms: str | None = None
    additional_documentation_required: list[str] | None = None
    mfg_for_registration: str | None = None
    contract_or_cooperative: str | None = None
    model_no: str | None = None
    part_no: str | None = None
    product: str | None = None
    contact_info: str | None = None
    company_name: str | None = None
    bid_summary: str | None = None
    product_specification: list[str] | None = None