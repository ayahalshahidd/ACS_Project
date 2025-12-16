from database import SessionLocal, engine, Base
# IMPORTANT: You MUST import all models so SQLAlchemy "sees" them
from models.user import User, UserRole
from models.course import Course
from models.enrollment import Enrollment, EnrollmentStatus
from models.audit import AuditRecord
from passlib.context import CryptContext # <--- CHANGED: Use Passlib instead of hashlib
from datetime import datetime

# --- SECURITY CONFIGURATION ---
# We use the same configuration as auth.py to ensure compatibility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def reset_and_seed():
    # 1. This line creates the actual .db file and all tables
    print("[*] Initializing database and creating tables...")
    Base.metadata.drop_all(bind=engine) # Clear existing (if any)
    Base.metadata.create_all(bind=engine) # Create new ones
    
    db = SessionLocal()

    print("[*] Seeding data...")
    
    # 2. Create Admin (SECURE: Bcrypt)
    # The backend will now recognize this hash format ($2b$...)
    admin = User(
        email="admin@university.edu",
        password_hash=get_password_hash("admin123"), 
        role=UserRole.ADMIN
    )
    db.add(admin)
    db.flush() # Get admin ID

    # 3. Create Student (SECURE: Bcrypt)
    student = User(
        email="student@university.edu",
        password_hash=get_password_hash("password123"),
        role=UserRole.STUDENT,
        student_id="STU001"
    )
    db.add(student)
    db.flush()

    # 4. Create Courses
    c1 = Course(code="CS101", title="Intro to Cyber", capacity=30)
    c2 = Course(code="CS102", title="Web Vulnerabilities", capacity=2)
    db.add_all([c1, c2])
    db.flush()

    # 5. Create an initial Audit Log
    log = AuditRecord(
        actor_id=admin.id,
        action="SYSTEM_INIT",
        target="Database",
        details="Database reset and seeded with Secure Bcrypt Hashes."
    )
    db.add(log)

    db.commit()
    db.close()
    print("[+] Success! Database is now ready and aligned with Auth Patch.")

if __name__ == "__main__":
    reset_and_seed()