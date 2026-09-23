from pydantic import BaseModel, Field


class RFPExtraction(BaseModel):
    rfp_number: str | None = None
    proposal_due_date: str | None = None
    contract_duration: str | None = None

    scope: str | None = None
    requirements: list[str] = Field(default_factory=list)
    eligibility_requirements: list[str] = Field(default_factory=list)
    evaluation_criteria: list[str] = Field(default_factory=list)
    submission_requirements: list[str] = Field(default_factory=list)