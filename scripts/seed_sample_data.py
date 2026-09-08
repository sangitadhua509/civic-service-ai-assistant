"""
Run this ONCE after your database tables exist (i.e. after
`alembic upgrade head`) to fill in some fictional starter data.

Run it with:
    python scripts/seed_sample_data.py

Why this exists: Service needs a real department_id, and Citizen needs
a real user_id. Since Phase 4 (login/register) isn't built yet, this
script creates a couple of placeholder User rows so you have something
valid to test Citizen creation against.

NOTE: the "hashed_password" values here are just placeholder text, NOT
real password hashes — that's intentional, since real password hashing
gets built in Phase 4. Don't rely on these accounts for actual login
later; Phase 4 will likely want you to register fresh ones properly.
"""

import sys
import os

sys.path.append(os.getcwd())

from app.db.session import SessionLocal
# Import via app.db.base (not the individual model files directly) so that
# EVERY model — including Citizen — is loaded into SQLAlchemy's registry
# before any query runs. User.citizen_profile refers to "Citizen" by name,
# and SQLAlchemy can only resolve that name if Citizen's module has already
# been imported somewhere in the running process.
from app.db.base import User, Department, Service


def run():
    db = SessionLocal()
    try:
        if db.query(Department).count() > 0:
            print("Sample data already exists — skipping. Delete rows manually if you want to reseed.")
            return

        water_dept = Department(
            name="Water Supply Department",
            code="WSD",
            description="Handles water connections, billing and complaints (fictional/sample department).",
        )
        health_dept = Department(
            name="Municipal Health Department",
            code="MHD",
            description="Handles sanitation and public health certificates (fictional/sample department).",
        )
        db.add_all([water_dept, health_dept])
        db.flush()  # assigns ids without fully committing yet

        new_connection = Service(
            department_id=water_dept.id,
            name="New Water Connection",
            code="WSD-NWC-01",
            requirements={
                "documents": ["ID proof", "Address proof", "Property tax receipt"],
                "eligibility": "Applicant must be the property owner or a registered tenant.",
            },
            status="active",
        )
        health_certificate = Service(
            department_id=health_dept.id,
            name="Sanitation Clearance Certificate",
            code="MHD-SCC-01",
            requirements={
                "documents": ["ID proof", "Premises ownership/rental proof"],
                "eligibility": "Applicant must be the operator of the premises being certified.",
            },
            status="active",
        )
        db.add_all([new_connection, health_certificate])

        sample_officer = User(
            name="Sample Officer",
            email="officer@example.com",
            hashed_password="placeholder-not-a-real-hash",
            role="officer",
        )
        sample_citizen_user = User(
            name="Sample Citizen",
            email="citizen@example.com",
            hashed_password="placeholder-not-a-real-hash",
            role="citizen",
        )
        db.add_all([sample_officer, sample_citizen_user])

        db.commit()
        print("Seed complete:")
        print(f"  Department ids: {water_dept.id} ({water_dept.code}), {health_dept.id} ({health_dept.code})")
        print(f"  Service ids: {new_connection.id}, {health_certificate.id}")
        print(f"  User ids: {sample_officer.id} (officer), {sample_citizen_user.id} (citizen)")
        print(f"  -> Use user_id={sample_citizen_user.id} when testing POST /citizens")
    finally:
        db.close()


if __name__ == "__main__":
    run()
