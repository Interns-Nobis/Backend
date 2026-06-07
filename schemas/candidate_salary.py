from pydantic import BaseModel


class CandidateSalary(BaseModel):

    candidate_id: str

    basic: float
    hra: float
    medical: float
    pf: float
    bonus: float

    monthly_gross: float
    annual_gross: float