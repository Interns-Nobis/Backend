from fastapi import FastAPI
from routers import employee
from routers import attendance
from routers import leave
from routers import dashboard
from routers import candidate
from routers import document
from routers import auth
from routers import candidate_personal
from routers import candidate_family
from routers import candidate_education
from routers import notifications
from routers import candidate_skills
from routers import candidate_certifications
from routers import candidate_references
from routers import candidate_salary

app = FastAPI()

app.include_router(
    employee.router,
    prefix="/employees",
    tags=["Employees"]
)

app.include_router(
    attendance.router,
    prefix="/attendance",
    tags=["Attendance"]
)

app.include_router(
    leave.router,
    prefix="/leave",
    tags=["Leave"]
)

app.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"] # once the db is created change the return of dashboard 
)

app.include_router(
    candidate.router,
    prefix="/candidate",
    tags=["Candidate"]
)

app.include_router(
    document.router,
    prefix="/documents",
    tags=["Documents"]
)

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    candidate_personal.router,
    prefix="/candidate-personal",
    tags=["Candidate Personal Details"]
)

app.include_router(
    candidate_family.router,
    prefix="/candidate-family",
    tags=["Candidate Family"]
)

app.include_router(
    candidate_education.router,
    prefix="/candidate-education",
    tags=["Candidate Education"]
)

app.include_router(
    notifications.router,
    prefix="/notifications",
    tags=["Notifications"]
)

app.include_router(
    candidate_skills.router,
    prefix="/candidate-skills",
    tags=["Candidate Skills"]
)

app.include_router(
    candidate_certifications.router,
    prefix="/candidate-certifications",
    tags=["Candidate Certifications"]
)

app.include_router(
    candidate_references.router,
    prefix="/candidate-references",
    tags=["Candidate References"]
)

app.include_router(
    candidate_salary.router,
    prefix="/candidate-salary",
    tags=["Candidate Salary"]
)

@app.get("/")
def home():
    return {"message": "HRMS Backend Running"}