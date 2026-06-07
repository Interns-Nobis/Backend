from fastapi import APIRouter
from sqlalchemy import text

from database import engine

router = APIRouter()

@router.get("/")
def dashboard():

    with engine.connect() as connection:

        employees = connection.execute(
            text("SELECT COUNT(*) FROM employees")
        ).scalar()

        attendance = connection.execute(
            text("SELECT COUNT(*) FROM attendance")
        ).scalar()

        leaves = connection.execute(
            text("SELECT COUNT(*) FROM leave_requests")
        ).scalar()

        return {
            "total_employees": employees,
            "attendance_records": attendance,
            "leave_requests": leaves
        }