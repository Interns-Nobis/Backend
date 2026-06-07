from fastapi import APIRouter, Depends
from sqlalchemy import text

from database import engine
from schemas.candidate_references import CandidateReference
from auth_handler import verify_token

router = APIRouter()


# ADD REFERENCE
@router.post("/")
def add_reference(
    reference: CandidateReference,
    user=Depends(verify_token)
):

    with engine.connect() as connection:

        connection.execute(
            text("""
                INSERT INTO candidate_references
                (
                    candidate_id,
                    reference_name,
                    relationship,
                    years_known,
                    company_name,
                    designation,
                    phone
                )

                VALUES
                (
                    :candidate_id,
                    :reference_name,
                    :relationship,
                    :years_known,
                    :company_name,
                    :designation,
                    :phone
                )
            """),
            reference.model_dump()
        )

        connection.commit()

    return {
        "message": "Reference Added"
    }


# GET REFERENCES
@router.get("/{candidate_id}")
def get_references(
    candidate_id: str,
    user=Depends(verify_token)
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT *
                FROM candidate_references
                WHERE candidate_id = :candidate_id
            """),
            {
                "candidate_id": candidate_id
            }
        )

        references = []

        for row in result:
            references.append(dict(row._mapping))

        return references


# UPDATE REFERENCE
@router.put("/{id}")
def update_reference(
    id: int,
    reference: CandidateReference,
    user=Depends(verify_token)
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                UPDATE candidate_references

                SET
                    reference_name = :reference_name,
                    relationship = :relationship,
                    years_known = :years_known,
                    company_name = :company_name,
                    designation = :designation,
                    phone = :phone

                WHERE id = :id
            """),
            {
                **reference.model_dump(),
                "id": id
            }
        )

        connection.commit()

        if result.rowcount > 0:
            return {
                "message": "Reference Updated"
            }

        return {
            "message": "Reference Not Found"
        }


# DELETE REFERENCE
@router.delete("/{id}")
def delete_reference(
    id: int,
    user=Depends(verify_token)
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                DELETE
                FROM candidate_references
                WHERE id = :id
            """),
            {
                "id": id
            }
        )

        connection.commit()

        if result.rowcount > 0:
            return {
                "message": "Reference Deleted"
            }

        return {
            "message": "Reference Not Found"
        }