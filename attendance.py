from pydantic import BaseModel

class Attendance(BaseModel):
    employee_id: str
    date: str
    status: str