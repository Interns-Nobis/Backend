from fastapi import APIRouter, Depends
from sqlalchemy import text

from database import engine
from schemas.candidate_salary import CandidateSalary
from auth_handler import verify_token

router = APIRouter()


# ADD SALARY
@router.post("/")
def add_salary(
    salary: CandidateSalary,
    user=Depends(verify_token)
):

    with engine.connect() as connection:

        connection.execute(
            text("""
                INSERT INTO candidate_salary
                (
                    candidate_id,
                    basic,
                    hra,
                    medical,
                    pf,
                    bonus,
                    monthly_gross,
                    annual_gross
                )

                VALUES
                (
                    :candidate_id,
                    :basic,
                    :hra,
                    :medical,
                    :pf,
                    :bonus,
                    :monthly_gross,
                    :annual_gross
                )
            """),
            salary.model_dump()
        )

        connection.commit()

    return {
        "message": "Salary Added"
    }


# GET SALARY
@router.get("/{candidate_id}")
def get_salary(
    candidate_id: str,
    user=Depends(verify_token)
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT *
                FROM candidate_salary
                WHERE candidate_id = :candidate_id
            """),
            {
                "candidate_id": candidate_id
            }
        )

        salary = result.fetchone()

        if salary:
            return dict(salary._mapping)

        return {
            "message": "Salary Record Not Found"
        }


# UPDATE SALARY
@router.put("/{candidate_id}")
def update_salary(
    candidate_id: str,
    salary: CandidateSalary,
    user=Depends(verify_token)
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                UPDATE candidate_salary

                SET
                    basic = :basic,
                    hra = :hra,
                    medical = :medical,
                    pf = :pf,
                    bonus = :bonus,
                    monthly_gross = :monthly_gross,
                    annual_gross = :annual_gross

                WHERE candidate_id = :candidate_id
            """),
            {
                **salary.model_dump(),
                "candidate_id": candidate_id
            }
        )

        connection.commit()

        if result.rowcount > 0:
            return {
                "message": "Salary Updated"
            }

        return {
            "message": "Salary Record Not Found"
        }


# DELETE SALARY
@router.delete("/{candidate_id}")
def delete_salary(
    candidate_id: str,
    user=Depends(verify_token)
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                DELETE
                FROM candidate_salary
                WHERE candidate_id = :candidate_id
            """),
            {
                "candidate_id": candidate_id
            }
        )

        connection.commit()

        if result.rowcount > 0:
            return {
                "message": "Salary Deleted"
            }

        return {
            "message": "Salary Record Not Found"
        }