from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.models import Document, User


def get_accessible_documents(
    db: Session,
    user: User,
) -> list[Document]:

    query = text(
        """
        SELECT DISTINCT d.*
        FROM documents AS d
        JOIN document_permissions AS p ON p.document_id = d.id
        WHERE p.user_id = :user_id
           OR p.allowed_role = :user_role
           OR p.allowed_department = :user_department
        """
    )

    parameters = {
        "user_id": user.id,
        # The database enum stores names (e.g. MANAGER), not values (manager).
        "user_role": user.role.name,
        "user_department": user.department,
    }

    # Map the SQL results to Document objects for the existing API.
    statement = select(Document).from_statement(query)
    return list(db.scalars(statement, parameters).all())
