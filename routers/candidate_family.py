from fastapi import APIRouter
from sqlalchemy import text

from database import engine
from schemas.candidate_family import CandidateFamily

router = APIRouter()


# ADD FAMILY MEMBER
@router.post("/")
def add_family_member(member: CandidateFamily):

    with engine.connect() as connection:

        connection.execute(
            text("""
                INSERT INTO candidate_family
                (
                    candidate_id,
                    relation,
                    name,
                    date_of_birth,
                    occupation
                )

                VALUES
                (
                    :candidate_id,
                    :relation,
                    :name,
                    :date_of_birth,
                    :occupation
                )
            """),
            member.model_dump()
        )

        connection.commit()

    return {
        "message": "Family Member Added"
    }


# GET ALL FAMILY MEMBERS OF A CANDIDATE
@router.get("/{candidate_id}")
def get_family_members(candidate_id: str):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT *
                FROM candidate_family
                WHERE candidate_id = :candidate_id
            """),
            {
                "candidate_id": candidate_id
            }
        )

        members = []

        for row in result:
            members.append(dict(row._mapping))

        return members


# UPDATE FAMILY MEMBER
@router.put("/{id}")
def update_family_member(
    id: int,
    member: CandidateFamily
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                UPDATE candidate_family

                SET
                    relation = :relation,
                    name = :name,
                    date_of_birth = :date_of_birth,
                    occupation = :occupation

                WHERE id = :id
            """),
            {
                **member.model_dump(),
                "id": id
            }
        )

        connection.commit()

        if result.rowcount > 0:
            return {
                "message": "Family Member Updated"
            }

        return {
            "message": "Family Member Not Found"
        }


# DELETE FAMILY MEMBER
@router.delete("/{id}")
def delete_family_member(id: int):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                DELETE
                FROM candidate_family
                WHERE id = :id
            """),
            {
                "id": id
            }
        )

        connection.commit()

        if result.rowcount > 0:
            return {
                "message": "Family Member Deleted"
            }

        return {
            "message": "Family Member Not Found"
        }