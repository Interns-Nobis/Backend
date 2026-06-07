from fastapi import APIRouter
from sqlalchemy import text

from database import engine
from schemas.candidate_education import CandidateEducation

router = APIRouter()


# ADD EDUCATION
@router.post("/")
def add_education(education: CandidateEducation):

    with engine.connect() as connection:

        connection.execute(
            text("""
                INSERT INTO candidate_education
                (
                    candidate_id,
                    qualification,
                    university,
                    year_from,
                    year_to,
                    percentage,
                    achievement
                )

                VALUES
                (
                    :candidate_id,
                    :qualification,
                    :university,
                    :year_from,
                    :year_to,
                    :percentage,
                    :achievement
                )
            """),
            education.model_dump()
        )

        connection.commit()

    return {
        "message": "Education Added"
    }


# GET ALL EDUCATION OF CANDIDATE
@router.get("/{candidate_id}")
def get_education(candidate_id: str):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT *
                FROM candidate_education
                WHERE candidate_id = :candidate_id
            """),
            {
                "candidate_id": candidate_id
            }
        )

        education = []

        for row in result:
            education.append(dict(row._mapping))

        return education


# UPDATE EDUCATION
@router.put("/{id}")
def update_education(
    id: int,
    education: CandidateEducation
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                UPDATE candidate_education

                SET
                    qualification = :qualification,
                    university = :university,
                    year_from = :year_from,
                    year_to = :year_to,
                    percentage = :percentage,
                    achievement = :achievement

                WHERE id = :id
            """),
            {
                **education.model_dump(),
                "id": id
            }
        )

        connection.commit()

        if result.rowcount > 0:
            return {
                "message": "Education Updated"
            }

        return {
            "message": "Education Record Not Found"
        }


# DELETE EDUCATION
@router.delete("/{id}")
def delete_education(id: int):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                DELETE
                FROM candidate_education
                WHERE id = :id
            """),
            {
                "id": id
            }
        )

        connection.commit()

        if result.rowcount > 0:
            return {
                "message": "Education Deleted"
            }

        return {
            "message": "Education Record Not Found"
        }