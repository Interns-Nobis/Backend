from pydantic import BaseModel

class Attendance(BaseModel):
    employee_id: str
    attendance_date: str
    status: str