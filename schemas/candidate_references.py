from pydantic import BaseModel


class CandidateReference(BaseModel):

    candidate_id: str

    reference_name: str

    relationship: str

    years_known: int

    company_name: str

    designation: str

    phone: str