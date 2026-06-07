from pydantic import BaseModel


class CandidateSkill(BaseModel):

    candidate_id: str

    skill_type: str
    skill_name: str

    experience: float