from pydantic import BaseModel

class Employee(BaseModel):
    employee_id: str
    name: str
    email: str
    department: str
    designation: str