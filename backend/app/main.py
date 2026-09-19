from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import models
from app.database import Base, engine, get_db
from app.models import User
from app.services.audit import log_document_access
from app.services.permissions import get_accessible_documents


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Permission-Aware Enterprise Knowledge System",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {"message": "Permission-Aware Knowledge API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/db")
async def database_health():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"database": "connected"}


@app.get("/users/{user_id}/documents")
def user_documents(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    documents = get_accessible_documents(
        db=db,
        user=user,
    )

    response = {
        "user": {
            "id": user.id,
            "name": user.name,
            "role": user.role,
            "department": user.department,
        },
        "documents": [
            {
                "id": document.id,
                "title": document.title,
                "classification": document.classification,
            }
            for document in documents
        ],
    }

    try:
        log_document_access(db, user.id, [document.id for document in documents])
        db.commit()
    except Exception:
        db.rollback()
        raise

    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
