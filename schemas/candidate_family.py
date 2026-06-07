from pydantic import BaseModel


class CandidateFamily(BaseModel):

    candidate_id: str

    relation: str
    name: str

    date_of_birth: str
    occupation: str