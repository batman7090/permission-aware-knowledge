from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models import Document, DocumentPermission, User


def get_accessible_documents(
    db: Session,
    user: User,
) -> list[Document]:

    statement = (
        select(Document)
        .join(
            DocumentPermission,
            DocumentPermission.document_id == Document.id,
        )
        .where(
            or_(
                DocumentPermission.user_id == user.id,
                DocumentPermission.allowed_role == user.role,
                DocumentPermission.allowed_department == user.department,
            )
        )
        .distinct()
    )

    return list(db.scalars(statement).all())