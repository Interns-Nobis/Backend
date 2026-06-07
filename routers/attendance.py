from fastapi import APIRouter, Depends
from sqlalchemy import text

from database import engine
from schemas.attendance import Attendance
from auth_handler import verify_token

router = APIRouter()

# GET ALL ATTENDANCE

@router.get("/")
def get_attendance(
user=Depends(verify_token)):
    with engine.connect() as connection:
        result = connection.execute(
        text("SELECT * FROM attendance")
    )

    attendance = []

    for row in result:
        attendance.append(dict(row._mapping))

    return attendance

# GET ATTENDANCE BY EMPLOYEE ID

@router.get("/{employee_id}")
def get_employee_attendance(
employee_id: str,
user=Depends(verify_token)):
    with engine.connect() as connection:
        result = connection.execute(
        text("""
            SELECT *
            FROM attendance
            WHERE employee_id = :employee_id
            ORDER BY attendance_date DESC
        """),
        {
            "employee_id": employee_id
        }
    )

    attendance = []

    for row in result:
        attendance.append(dict(row._mapping))

    return attendance

# ADD ATTENDANCE

@router.post("/")
def add_attendance(
attendance: Attendance,
user=Depends(verify_token)):
    with engine.connect() as connection:
        connection.execute(
        text("""
            INSERT INTO attendance
            (
                employee_id,
                attendance_date,
                status
            )

            VALUES
            (
                :employee_id,
                :attendance_date,
                :status
            )
        """),
        {
            "employee_id": attendance.employee_id,
            "attendance_date": attendance.attendance_date,
            "status": attendance.status
        }
    )

    connection.commit()
    return {
    "message": "Attendance Added"
}

# UPDATE ATTENDANCE

@router.put("/{attendance_id}")
def update_attendance(
attendance_id: int,
attendance: Attendance,
user=Depends(verify_token)):
    with engine.connect() as connection:
        result = connection.execute(
        text("""
            UPDATE attendance

            SET
                employee_id = :employee_id,
                attendance_date = :attendance_date,
                status = :status

            WHERE id = :attendance_id
        """),
        {
            "attendance_id": attendance_id,
            "employee_id": attendance.employee_id,
            "attendance_date": attendance.attendance_date,
            "status": attendance.status
        }
    )

    connection.commit()

    if result.rowcount > 0:
        return {
            "message": "Attendance Updated"
        }

    return {
        "message": "Attendance Not Found"
    }

# DELETE ATTENDANCE

@router.delete("/{attendance_id}")
def delete_attendance(
attendance_id: int,
user=Depends(verify_token)):
    with engine.connect() as connection:
        result = connection.execute(
        text("""
            DELETE
            FROM attendance
            WHERE id = :attendance_id
        """),
        {
            "attendance_id": attendance_id
        }
    )

    connection.commit()

    if result.rowcount > 0:
        return {
            "message": "Attendance Deleted"
        }

    return {
        "message": "Attendance Not Found"
    }

# ATTENDANCE SUMMARY

@router.get("/summary/{employee_id}")
def attendance_summary(
employee_id: str,
user=Depends(verify_token)):
    with engine.connect() as connection:
        present_count = connection.execute(
        text("""
            SELECT COUNT(*) as total
            FROM attendance
            WHERE employee_id = :employee_id
            AND status = 'Present'
        """),
        {
            "employee_id": employee_id
        }
    ).fetchone()

    absent_count = connection.execute(
        text("""
            SELECT COUNT(*) as total
            FROM attendance
            WHERE employee_id = :employee_id
            AND status = 'Absent'
        """),
        {
            "employee_id": employee_id
        }
    ).fetchone()

    return {
        "employee_id": employee_id,
        "present_days": present_count.total,
        "absent_days": absent_count.total
    }

