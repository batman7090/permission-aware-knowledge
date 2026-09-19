from sqlalchemy import select

from app.database import SessionLocal
from app.models import (
    Document,
    DocumentChunk,
    DocumentClassification,
    DocumentPermission,
    User,
    UserRole,
)


def seed():
    db = SessionLocal()

    try:
        # Avoid inserting duplicate seed data
        existing_user = db.scalar(
            select(User).where(User.email == "alice@company.com")
        )

        if existing_user:
            print("Database already seeded.")
            return

        # -------------------------
        # Users
        # -------------------------
        alice = User(
            name="Alice",
            email="alice@company.com",
            role=UserRole.EMPLOYEE,
            department="engineering",
        )

        bob = User(
            name="Bob",
            email="bob@company.com",
            role=UserRole.HR,
            department="hr",
        )

        charlie = User(
            name="Charlie",
            email="charlie@company.com",
            role=UserRole.FINANCE,
            department="finance",
        )

        db.add_all([alice, bob, charlie])
        db.flush()

        # -------------------------
        # Documents
        # -------------------------
        engineering_doc = Document(
            title="Engineering Architecture",
            source="engineering_architecture.txt",
            department="engineering",
            classification=DocumentClassification.CONFIDENTIAL,
        )

        salary_doc = Document(
            title="Salary Report 2026",
            source="salary_report_2026.txt",
            department="hr",
            classification=DocumentClassification.RESTRICTED,
        )

        finance_doc = Document(
            title="Finance Budget 2026",
            source="finance_budget_2026.txt",
            department="finance",
            classification=DocumentClassification.CONFIDENTIAL,
        )

        db.add_all(
            [
                engineering_doc,
                salary_doc,
                finance_doc,
            ]
        )

        # Flush so documents receive their database IDs
        db.flush()

        # -------------------------
        # Document chunks
        # -------------------------
        chunks = [
            DocumentChunk(
                document_id=engineering_doc.id,
                chunk_index=0,
                content=(
                    "The engineering platform uses FastAPI "
                    "for backend services."
                ),
            ),
            DocumentChunk(
                document_id=engineering_doc.id,
                chunk_index=1,
                content=(
                    "PostgreSQL is used as the primary "
                    "transactional database."
                ),
            ),
            DocumentChunk(
                document_id=engineering_doc.id,
                chunk_index=2,
                content=(
                    "Production services are containerized "
                    "using Docker and deployed to Kubernetes."
                ),
            ),

            DocumentChunk(
                document_id=salary_doc.id,
                chunk_index=0,
                content=(
                    "The average software engineer salary "
                    "is 85000 EUR per year."
                ),
            ),
            DocumentChunk(
                document_id=salary_doc.id,
                chunk_index=1,
                content=(
                    "Senior software engineers earn between "
                    "95000 and 115000 EUR per year."
                ),
            ),

            DocumentChunk(
                document_id=finance_doc.id,
                chunk_index=0,
                content=(
                    "The engineering department has a 2026 "
                    "annual budget of 2.5 million EUR."
                ),
            ),
            DocumentChunk(
                document_id=finance_doc.id,
                chunk_index=1,
                content=(
                    "The company plans to allocate 600000 EUR "
                    "to cloud infrastructure in 2026."
                ),
            ),
        ]

        db.add_all(chunks)

        # -------------------------
        # Permissions
        # -------------------------
        permissions = [
            # Engineering Architecture:
            # anyone in Engineering can access it
            DocumentPermission(
                document_id=engineering_doc.id,
                allowed_department="engineering",
            ),

            # Salary Report:
            # HR role only
            DocumentPermission(
                document_id=salary_doc.id,
                allowed_role=UserRole.HR,
            ),

            # Finance Budget:
            # Finance role only
            DocumentPermission(
                document_id=finance_doc.id,
                allowed_role=UserRole.FINANCE,
            ),
        ]

        db.add_all(permissions)

        # Save everything
        db.commit()

        print("Seed completed successfully.")
        print()
        print("Users created:")
        print(f"  Alice   -> id={alice.id}")
        print(f"  Bob     -> id={bob.id}")
        print(f"  Charlie -> id={charlie.id}")
        print()
        print("Documents created:")
        print(f"  {engineering_doc.title} -> id={engineering_doc.id}")
        print(f"  {salary_doc.title} -> id={salary_doc.id}")
        print(f"  {finance_doc.title} -> id={finance_doc.id}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()