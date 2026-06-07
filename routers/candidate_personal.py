from fastapi import APIRouter
from sqlalchemy import text

from database import engine
from schemas.candidate_personal import CandidatePersonal

router = APIRouter()


# ADD PERSONAL DETAILS
@router.post("/")
def add_personal_details(details: CandidatePersonal):

    with engine.connect() as connection:

        connection.execute(
            text("""
                INSERT INTO candidate_personal_details
                (
                    candidate_id,
                    first_name,
                    middle_name,
                    last_name,
                    date_of_birth,
                    email,
                    mobile_number,
                    mother_tongue,

                    present_address,
                    present_city,
                    present_state,
                    present_pincode,

                    permanent_address,
                    permanent_city,
                    permanent_state,
                    permanent_pincode,

                    bank_name,
                    branch,
                    ifsc_code,
                    account_number,

                    pan_number,
                    aadhaar_number,

                    passport_number,
                    citizenship,

                    emergency_contact_name,
                    emergency_contact_relation,
                    emergency_contact_mobile
                )

                VALUES
                (
                    :candidate_id,
                    :first_name,
                    :middle_name,
                    :last_name,
                    :date_of_birth,
                    :email,
                    :mobile_number,
                    :mother_tongue,

                    :present_address,
                    :present_city,
                    :present_state,
                    :present_pincode,

                    :permanent_address,
                    :permanent_city,
                    :permanent_state,
                    :permanent_pincode,

                    :bank_name,
                    :branch,
                    :ifsc_code,
                    :account_number,

                    :pan_number,
                    :aadhaar_number,

                    :passport_number,
                    :citizenship,

                    :emergency_contact_name,
                    :emergency_contact_relation,
                    :emergency_contact_mobile
                )
            """),
            details.model_dump()
        )

        connection.commit()

    return {
        "message": "Personal Details Added"
    }


# GET ALL
@router.get("/")
def get_all_personal_details():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT *
                FROM candidate_personal_details
            """)
        )

        data = []

        for row in result:
            data.append(dict(row._mapping))

        return data


# GET BY CANDIDATE ID
@router.get("/{candidate_id}")
def get_personal_details(candidate_id: str):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT *
                FROM candidate_personal_details
                WHERE candidate_id = :candidate_id
            """),
            {
                "candidate_id": candidate_id
            }
        )

        details = result.fetchone()

        if details:
            return dict(details._mapping)

        return {
            "message": "Candidate Not Found"
        }


# UPDATE
@router.put("/{candidate_id}")
def update_personal_details(
    candidate_id: str,
    details: CandidatePersonal
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                UPDATE candidate_personal_details

                SET

                first_name=:first_name,
                middle_name=:middle_name,
                last_name=:last_name,
                date_of_birth=:date_of_birth,
                email=:email,
                mobile_number=:mobile_number,
                mother_tongue=:mother_tongue,

                present_address=:present_address,
                present_city=:present_city,
                present_state=:present_state,
                present_pincode=:present_pincode,

                permanent_address=:permanent_address,
                permanent_city=:permanent_city,
                permanent_state=:permanent_state,
                permanent_pincode=:permanent_pincode,

                bank_name=:bank_name,
                branch=:branch,
                ifsc_code=:ifsc_code,
                account_number=:account_number,

                pan_number=:pan_number,
                aadhaar_number=:aadhaar_number,

                passport_number=:passport_number,
                citizenship=:citizenship,

                emergency_contact_name=:emergency_contact_name,
                emergency_contact_relation=:emergency_contact_relation,
                emergency_contact_mobile=:emergency_contact_mobile

                WHERE candidate_id=:candidate_id
            """),
            {
                **details.model_dump(),
                "candidate_id": candidate_id
            }
        )

        connection.commit()

        if result.rowcount > 0:
            return {
                "message": "Personal Details Updated"
            }

        return {
            "message": "Candidate Not Found"
        }


# DELETE
@router.delete("/{candidate_id}")
def delete_personal_details(candidate_id: str):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                DELETE
                FROM candidate_personal_details
                WHERE candidate_id = :candidate_id
            """),
            {
                "candidate_id": candidate_id
            }
        )

        connection.commit()

        if result.rowcount > 0:
            return {
                "message": "Personal Details Deleted"
            }

        return {
            "message": "Candidate Not Found"
        }