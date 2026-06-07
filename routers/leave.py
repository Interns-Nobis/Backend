from fastapi import APIRouter, Depends
from sqlalchemy import text

from database import engine
from schemas.leave import Leave
from auth_handler import verify_token

router = APIRouter()

# GET ALL LEAVES

@router.get("/")
def get_leaves(
user=Depends(verify_token)):
    with engine.connect() as connection:
        result = connection.execute(
        text("SELECT * FROM leave_requests")
    )

    leaves = []

    for row in result:
        leaves.append(dict(row._mapping))

    return leaves

# GET LEAVE HISTORY

@router.get("/{employee_id}")
def get_leave_history(
employee_id: str,
user=Depends(verify_token)):
    with engine.connect() as connection:
        result = connection.execute(
        text("""
            SELECT *
            FROM leave_requests
            WHERE employee_id = :employee_id
        """),
        {
            "employee_id": employee_id
        }
    )

    leaves = []

    for row in result:
        leaves.append(dict(row._mapping))

    return leaves


# APPLY LEAVE

@router.post("/")
def apply_leave(
leave: Leave,
user=Depends(verify_token)):
    with engine.connect() as connection:
        connection.execute(
        text("""
            INSERT INTO leave_requests
            (
                employee_id,
                leave_type,
                start_date,
                end_date,
                reason,
                status
            )

            VALUES
            (
                :employee_id,
                :leave_type,
                :start_date,
                :end_date,
                :reason,
                'Pending'
            )
        """),
        {
            "employee_id": leave.employee_id,
            "leave_type": leave.leave_type,
            "start_date": leave.start_date,
            "end_date": leave.end_date,
            "reason": leave.reason
        }
    )

    connection.commit()
    return {
    "message": "Leave Applied"
}

# APPROVE LEAVE

@router.put("/approve/{leave_id}")
def approve_leave(
leave_id: int,
user=Depends(verify_token)):
    with engine.connect() as connection:
        result = connection.execute(
        text("""
            UPDATE leave_requests
            SET status = 'Approved'
            WHERE id = :leave_id
        """),
        {
            "leave_id": leave_id
        }
    )

    connection.commit()

    if result.rowcount > 0:
        return {
            "message": "Leave Approved"
        }

    return {
        "message": "Leave Not Found"
    }

# REJECT LEAVE

@router.put("/reject/{leave_id}")
def reject_leave(
leave_id: int,
user=Depends(verify_token)):
    with engine.connect() as connection:
        result = connection.execute(
        text("""
            UPDATE leave_requests
            SET status = 'Rejected'
            WHERE id = :leave_id
        """),
        {
            "leave_id": leave_id
        }
    )

    connection.commit()

    if result.rowcount > 0:
        return {
            "message": "Leave Rejected"
        }

    return {
        "message": "Leave Not Found"
    }

# DELETE LEAVE

@router.delete("/{leave_id}")
def delete_leave(
leave_id: int,
user=Depends(verify_token)):
    with engine.connect() as connection:
        result = connection.execute(
        text("""
            DELETE
            FROM leave_requests
            WHERE id = :leave_id
        """),
        {
            "leave_id": leave_id
        }
    )

    connection.commit()

    if result.rowcount > 0:
        return {
            "message": "Leave Deleted"
        }

    return {
        "message": "Leave Not Found"
    }
