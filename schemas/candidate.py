from pydantic import BaseModel

class Candidate(BaseModel):
    candidate_id: str
    position: str
    status: str
    remarks: str | None = None
    