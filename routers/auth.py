from fastapi import APIRouter
from sqlalchemy import text
from database import engine

from schemas.user import User

from passlib.context import CryptContext
from jose import jwt

router = APIRouter()

SECRET_KEY = "HRMS_SECRET_KEY"
ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

@router.post("/register")
def register(user: User):

    hashed_password = pwd_context.hash(
        user.password
    )

    with engine.connect() as connection:

        connection.execute(
            text("""
                INSERT INTO users
                (
                    username,
                    password,
                    role
                )
                VALUES
                (
                    :username,
                    :password,
                    :role
                )
            """),
            {
                "username": user.username,
                "password": hashed_password,
                "role": user.role
            }
        )

        connection.commit()

    return {
        "message": "User Registered"
    }

@router.post("/login")
def login(user: User):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT *
                FROM users
                WHERE username = :username
            """),
            {
                "username": user.username
            }
        )

        db_user = result.fetchone()

        if not db_user:
            return {
                "message": "Invalid Username"
            }

        db_user = dict(db_user._mapping)

        if not pwd_context.verify(
            user.password,
            db_user["password"]
        ):
            return {
                "message": "Invalid Password"
            }

        token = jwt.encode(
            {
                "username": db_user["username"],
                "role": db_user["role"]
            },
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return {
            "access_token": token,
            "role": db_user["role"]
        }