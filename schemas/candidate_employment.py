from pydantic import BaseModel


class CandidateEmployment(BaseModel):

    candidate_id: str

    organization: str
    designation: str

    from_date: str
    to_date: str

    responsibilities: str

    compensation: float