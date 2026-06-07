from fastapi import APIRouter, Depends
from sqlalchemy import text

from database import engine
from schemas.employee import Employee
from auth_handler import verify_token

router = APIRouter()


# GET ALL EMPLOYEES
@router.get("/")
def get_employees(
    user=Depends(verify_token)
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT *
                FROM employees
                ORDER BY created_at DESC
            """)
        )

        employees = []

        for row in result:
            employees.append(dict(row._mapping))

        return employees


# GET EMPLOYEE BY ID
@router.get("/{employee_id}")
def get_employee(
    employee_id: str,
    user=Depends(verify_token)
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT *
                FROM employees
                WHERE employee_id = :employee_id
            """),
            {
                "employee_id": employee_id
            }
        )

        employee = result.fetchone()

        if employee:
            return dict(employee._mapping)

        return {
            "message": "Employee Not Found"
        }


# ADD EMPLOYEE
@router.post("/")
def add_employee(
    employee: Employee,
    user=Depends(verify_token)
):

    with engine.connect() as connection:

        connection.execute(
            text("""
                INSERT INTO employees
                (
                    employee_id,
                    name,
                    email,
                    department,
                    designation
                )
                VALUES
                (
                    :employee_id,
                    :name,
                    :email,
                    :department,
                    :designation
                )
            """),
            {
                "employee_id": employee.employee_id,
                "name": employee.name,
                "email": employee.email,
                "department": employee.department,
                "designation": employee.designation
            }
        )

        connection.commit()

    return {
        "message": "Employee Added Successfully"
    }


# UPDATE EMPLOYEE
@router.put("/{employee_id}")
def update_employee(
    employee_id: str,
    employee: Employee,
    user=Depends(verify_token)
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                UPDATE employees

                SET
                    name = :name,
                    email = :email,
                    department = :department,
                    designation = :designation

                WHERE employee_id = :employee_id
            """),
            {
                "employee_id": employee_id,
                "name": employee.name,
                "email": employee.email,
                "department": employee.department,
                "designation": employee.designation
            }
        )

        connection.commit()

        if result.rowcount > 0:
            return {
                "message": "Employee Updated Successfully"
            }

        return {
            "message": "Employee Not Found"
        }


# DELETE EMPLOYEE
@router.delete("/{employee_id}")
def delete_employee(
    employee_id: str,
    user=Depends(verify_token)
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                DELETE
                FROM employees
                WHERE employee_id = :employee_id
            """),
            {
                "employee_id": employee_id
            }
        )

        connection.commit()

        if result.rowcount > 0:
            return {
                "message": "Employee Deleted Successfully"
            }

        return {
            "message": "Employee Not Found"
        }