from pydantic import BaseModel

class Leave(BaseModel):
    employee_id: str
    leave_type: str
    start_date: str
    end_date: str
    reason: str
    status: str