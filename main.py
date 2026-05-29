from fastapi import FastAPI
from routers import employee
from routers import attendance
from routers import leave
from routers import dashboard

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

@app.get("/")
def home():
    return {"message": "HRMS Backend Running"}