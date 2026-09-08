"""
Run this ONCE after your database tables exist (i.e. after
`alembic upgrade head`) to fill in fictional starter data — including
three real, working login accounts (admin, officer, citizen) so you
can test role-based access without registering a dozen accounts by
hand.

Run it with:
    python scripts/seed_sample_data.py

IMPORTANT: if you ran this script back in Phase 3 (before auth
existed), your database already has an "officer" and "citizen" user
with FAKE, unusable passwords. This script will detect existing data
and skip — you need to clear those old rows first. Easiest way: open
pgAdmin -> civic_db -> Query Tool, and run:

    TRUNCATE citizens, services, departments, users RESTART IDENTITY CASCADE;

Then run this script again.
"""

import sys
import os

sys.path.append(os.getcwd())

from app.db.session import SessionLocal
from app.db.base import User, Department, Service
from app.core.security import hash_password


# These are PLAINTEXT passwords, used only to create test accounts.
# In a real deployment these would never appear in source code.
SAMPLE_ADMIN_PASSWORD = "AdminPass123"
SAMPLE_OFFICER_PASSWORD = "OfficerPass123"
SAMPLE_CITIZEN_PASSWORD = "CitizenPass123"


def run():
    db = SessionLocal()
    try:
        if db.query(Department).count() > 0:
            print("Sample data already exists — skipping.")
            print("See the note at the top of this file if you need to reset and reseed.")
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
        db.flush()

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

        admin_user = User(
            name="Sample Admin",
            email="admin@example.com",
            hashed_password=hash_password(SAMPLE_ADMIN_PASSWORD),
            role="admin",
        )
        officer_user = User(
            name="Sample Officer",
            email="officer@example.com",
            hashed_password=hash_password(SAMPLE_OFFICER_PASSWORD),
            role="officer",
        )
        citizen_user = User(
            name="Sample Citizen",
            email="citizen@example.com",
            hashed_password=hash_password(SAMPLE_CITIZEN_PASSWORD),
            role="citizen",
        )
        db.add_all([admin_user, officer_user, citizen_user])

        db.commit()
        print("Seed complete. Test accounts (use these in POST /auth/login):")
        print(f"  ADMIN    email=admin@example.com    password={SAMPLE_ADMIN_PASSWORD}")
        print(f"  OFFICER  email=officer@example.com  password={SAMPLE_OFFICER_PASSWORD}")
        print(f"  CITIZEN  email=citizen@example.com  password={SAMPLE_CITIZEN_PASSWORD}")
        print(f"Department ids: {water_dept.id} ({water_dept.code}), {health_dept.id} ({health_dept.code})")
        print(f"Service ids: {new_connection.id}, {health_certificate.id}")
    finally:
        db.close()


if __name__ == "__main__":
    run()
