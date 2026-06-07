from fastapi import APIRouter, UploadFile, File, Form
from sqlalchemy import text
from database import engine

import os
import shutil

router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_document(
    candidate_id: str = Form(...),
    document_type: str = Form(...),
    file: UploadFile = File(...)
):

    try:

        print("Candidate ID:", candidate_id)
        print("Document Type:", document_type)
        print("Filename:", file.filename)

        file_path = f"{UPLOAD_DIR}/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        with engine.connect() as connection:

            connection.execute(
                text("""
                    INSERT INTO candidate_documents
                    (
                        candidate_id,
                        document_type,
                        file_name,
                        file_path
                    )
                    VALUES
                    (
                        :candidate_id,
                        :document_type,
                        :file_name,
                        :file_path
                    )
                """),
                {
                    "candidate_id": candidate_id.strip(),
                    "document_type": document_type,
                    "file_name": file.filename,
                    "file_path": file_path
                }
            )

            connection.commit()

        return {
            "message": "Document Uploaded",
            "file_name": file.filename
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}
    
@router.get("/{candidate_id}")
def get_documents(candidate_id: str):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT *
                FROM candidate_documents
                WHERE candidate_id = :candidate_id
            """),
            {"candidate_id": candidate_id}
        )

        documents = []

        for row in result:
            documents.append(dict(row._mapping))

        return documents