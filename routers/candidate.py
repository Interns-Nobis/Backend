from fastapi import APIRouter
from sqlalchemy import text

from database import engine

router = APIRouter()


# GET ALL CANDIDATES
@router.get("/")
def get_candidates():

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT * FROM candidates")
        )

        candidates = []

        for row in result:
            candidates.append(dict(row._mapping))

        return candidates


# GET CANDIDATE BY ID
@router.get("/{candidate_id}")
def get_candidate(candidate_id: str):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT *
                FROM candidates
                WHERE candidate_id = :candidate_id
            """),
            {
                "candidate_id": candidate_id
            }
        )

        candidate = result.fetchone()

        if candidate:
            return dict(candidate._mapping)

        return {
            "message": "Candidate Not Found"
        }


# SUBMIT CANDIDATE
@router.put("/submit/{candidate_id}")
def submit_candidate(candidate_id: str):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                UPDATE candidates
                SET status = 'Submitted'
                WHERE candidate_id = :candidate_id
            """),
            {
                "candidate_id": candidate_id
            }
        )

        connection.commit()

        if result.rowcount > 0:
            return {
                "message": "Candidate Submitted"
            }

        return {
            "message": "Candidate Not Found"
        }


# MOVE TO REVIEW
@router.put("/review/{candidate_id}")
def review_candidate(candidate_id: str):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                UPDATE candidates
                SET status = 'Under Review'
                WHERE candidate_id = :candidate_id
            """),
            {
                "candidate_id": candidate_id
            }
        )

        connection.commit()

        if result.rowcount > 0:
            return {
                "message": "Candidate Under Review"
            }

        return {
            "message": "Candidate Not Found"
        }


# REJECT CANDIDATE
@router.put("/reject/{candidate_id}")
def reject_candidate(
    candidate_id: str,
    remarks: str
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                UPDATE candidates
                SET
                    status = 'Rejected',
                    remarks = :remarks
                WHERE candidate_id = :candidate_id
            """),
            {
                "candidate_id": candidate_id,
                "remarks": remarks
            }
        )

        connection.commit()
        connection.execute(
    text("""
        INSERT INTO notifications
        (
            candidate_id,
            message,
            notification_type,
            status
        )
        VALUES
        (
            :candidate_id,
            'Your profile has been rejected',
            'Rejection',
            'Unread'
        )
    """),
    {
        "candidate_id": candidate_id
    }
)
        connection.commit()

        if result.rowcount > 0:
            return {
                "message": "Candidate Rejected"
            }

        return {
            "message": "Candidate Not Found"
        }


# HR APPROVAL
@router.put("/hr-approve/{candidate_id}")
def hr_approve(candidate_id: str):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                UPDATE candidates
                SET status = 'HR Manager Approved'
                WHERE candidate_id = :candidate_id
            """),
            {
                "candidate_id": candidate_id
            }
        )

        connection.commit()

        if result.rowcount > 0:
            return {
                "message": "HR Approval Completed"
            }

        return {
            "message": "Candidate Not Found"
        }


# HOD APPROVAL
@router.put("/hod-approve/{candidate_id}")
def hod_approve(candidate_id: str):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                UPDATE candidates
                SET status = 'HoD Approved'
                WHERE candidate_id = :candidate_id
            """),
            {
                "candidate_id": candidate_id
            }
        )

        connection.commit()

        if result.rowcount > 0:
            return {
                "message": "HoD Approval Completed"
            }

        return {
            "message": "Candidate Not Found"
        }


# RELEASE OFFER
@router.put("/release-offer/{candidate_id}")
def release_offer(candidate_id: str):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                UPDATE candidates
                SET status = 'Offer Released'
                WHERE candidate_id = :candidate_id
            """),
            {
                "candidate_id": candidate_id
            }
        )

        connection.commit()
        connection.execute(
    text("""
        INSERT INTO notifications
        (
            candidate_id,
            message,
            notification_type,
            status
        )
        VALUES
        (
            :candidate_id,
            'Offer letter has been released',
            'offer',
            'Unread'
        )
    """),
    {
        "candidate_id": candidate_id
    }
)
        connection.commit()

        if result.rowcount > 0:
            return {
                "message": "Offer Released"
            }

        return {
            "message": "Candidate Not Found"
        }


# DELETE CANDIDATE
@router.delete("/{candidate_id}")
def delete_candidate(candidate_id: str):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                DELETE FROM candidates
                WHERE candidate_id = :candidate_id
            """),
            {
                "candidate_id": candidate_id
            }
        )

        connection.commit()

        if result.rowcount > 0:
            return {
                "message": "Candidate Deleted"
            }

        return {
            "message": "Candidate Not Found"
        }
    
    @router.put("/hr-approve/{candidate_id}")
    def hr_approve(candidate_id: str):
        with engine.connect() as connection:
            result = connection.execute(
            text("""
                UPDATE candidates
                SET status = 'HR Manager Approved'
                WHERE candidate_id = :candidate_id
            """),
            {
                "candidate_id": candidate_id
            }
        )

        connection.commit()
        connection.execute(
    text("""
        INSERT INTO notifications
        (
            candidate_id,
            message,
            notification_type,
            status
        )
        VALUES
        (
            :candidate_id,
            'Your profile has been approved by HR Manager',
            'Approval',
            'Unread'
        )
    """),
    {
        "candidate_id": candidate_id
    }
)
        connection.commit()
        return {
            "message": "HR Approval Completed"
        }