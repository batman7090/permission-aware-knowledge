import json

from sqlalchemy import text
from sqlalchemy.orm import Session


def log_document_access(
    db: Session,
    user_id: int,
    document_ids: list[int],
) -> None:
    """Record returned document IDs; the caller commits the transaction."""
    db.execute(
        text(
            """
            INSERT INTO audit_logs (user_id, action, document_ids)
            VALUES (:user_id, :action, CAST(:document_ids AS JSON))
            """
        ),
        {
            "user_id": user_id,
            "action": "list_accessible_documents",
            "document_ids": json.dumps(document_ids),
        },
    )
