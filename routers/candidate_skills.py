from fastapi import APIRouter, Depends
from sqlalchemy import text

from database import engine
from schemas.candidate_skills import CandidateSkill
from auth_handler import verify_token

router = APIRouter()


# ADD SKILL
@router.post("/")
def add_skill(
    skill: CandidateSkill,
    user=Depends(verify_token)
):

    with engine.connect() as connection:

        connection.execute(
            text("""
                INSERT INTO candidate_skills
                (
                    candidate_id,
                    skill_type,
                    skill_name,
                    experience
                )

                VALUES
                (
                    :candidate_id,
                    :skill_type,
                    :skill_name,
                    :experience
                )
            """),
            skill.model_dump()
        )

        connection.commit()

    return {
        "message": "Skill Added"
    }


# GET SKILLS
@router.get("/{candidate_id}")
def get_skills(
    candidate_id: str,
    user=Depends(verify_token)
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT *
                FROM candidate_skills
                WHERE candidate_id = :candidate_id
            """),
            {
                "candidate_id": candidate_id
            }
        )

        skills = []

        for row in result:
            skills.append(dict(row._mapping))

        return skills


# UPDATE SKILL
@router.put("/{id}")
def update_skill(
    id: int,
    skill: CandidateSkill,
    user=Depends(verify_token)
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                UPDATE candidate_skills

                SET
                    skill_type = :skill_type,
                    skill_name = :skill_name,
                    experience = :experience

                WHERE id = :id
            """),
            {
                **skill.model_dump(),
                "id": id
            }
        )

        connection.commit()

        if result.rowcount > 0:
            return {
                "message": "Skill Updated"
            }

        return {
            "message": "Skill Not Found"
        }


# DELETE SKILL
@router.delete("/{id}")
def delete_skill(
    id: int,
    user=Depends(verify_token)
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                DELETE
                FROM candidate_skills
                WHERE id = :id
            """),
            {
                "id": id
            }
        )

        connection.commit()

        if result.rowcount > 0:
            return {
                "message": "Skill Deleted"
            }

        return {
            "message": "Skill Not Found"
        }