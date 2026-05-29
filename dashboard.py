from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_dashboard():

    return {
        "total_employees": 3,
        "present_employees": 2,
        "employees_on_leave": 1
    }