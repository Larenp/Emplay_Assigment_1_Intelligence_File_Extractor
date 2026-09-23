from pydantic import BaseModel, Field


class Document(BaseModel):
    document_id: str
    filename: str
    source_folder: str
    file_type: str
    text: str
    metadata: dict = Field(default_factory=dict)