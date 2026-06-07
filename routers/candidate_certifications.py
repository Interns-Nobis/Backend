from fastapi import APIRouter, Depends
from sqlalchemy import text

from database import engine
from schemas.candidate_certifications import CandidateCertification
from auth_handler import verify_token

router = APIRouter()


# ADD CERTIFICATION
@router.post("/")
def add_certification(
    certification: CandidateCertification,
    user=Depends(verify_token)
):

    with engine.connect() as connection:

        connection.execute(
            text("""
                INSERT INTO candidate_certifications
                (
                    candidate_id,
                    certification_name,
                    year
                )

                VALUES
                (
                    :candidate_id,
                    :certification_name,
                    :year
                )
            """),
            certification.model_dump()
        )

        connection.commit()

    return {
        "message": "Certification Added"
    }


# GET CERTIFICATIONS
@router.get("/{candidate_id}")
def get_certifications(
    candidate_id: str,
    user=Depends(verify_token)
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT *
                FROM candidate_certifications
                WHERE candidate_id = :candidate_id
            """),
            {
                "candidate_id": candidate_id
            }
        )

        certifications = []

        for row in result:
            certifications.append(dict(row._mapping))

        return certifications


# UPDATE CERTIFICATION
@router.put("/{id}")
def update_certification(
    id: int,
    certification: CandidateCertification,
    user=Depends(verify_token)
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                UPDATE candidate_certifications

                SET
                    certification_name = :certification_name,
                    year = :year

                WHERE id = :id
            """),
            {
                **certification.model_dump(),
                "id": id
            }
        )

        connection.commit()

        if result.rowcount > 0:
            return {
                "message": "Certification Updated"
            }

        return {
            "message": "Certification Not Found"
        }


# DELETE CERTIFICATION
@router.delete("/{id}")
def delete_certification(
    id: int,
    user=Depends(verify_token)
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                DELETE
                FROM candidate_certifications
                WHERE id = :id
            """),
            {
                "id": id
            }
        )

        connection.commit()

        if result.rowcount > 0:
            return {
                "message": "Certification Deleted"
            }

        return {
            "message": "Certification Not Found"
        }