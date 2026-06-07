from pydantic import BaseModel


class CandidateEducation(BaseModel):

    candidate_id: str

    qualification: str
    university: str

    year_from: int
    year_to: int

    percentage: float

    achievement: str | None = None