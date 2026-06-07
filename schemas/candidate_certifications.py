from pydantic import BaseModel


class CandidateCertification(BaseModel):

    candidate_id: str

    certification_name: str

    year: int