"""
Admin routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.course import Course
from models.enrollment import Enrollment, EnrollmentStatus
from pydantic import BaseModel
from typing import Optional, List

# --- KEY FIXES: Add these two imports ---
from models.user import User
from auth.dependencies import get_current_user 
# ----------------------------------------

router = APIRouter()

class CourseCreateRequest(BaseModel):
    code: str
    title: str
    description: Optional[str] = None
    capacity: int
    prereq_ids: Optional[List[int]] = None
    schedule: Optional[dict] = None
    instructor_id: Optional[int] = None


@router.post("/courses")
async def create_course(
    course_data: CourseCreateRequest,
    db: Session = Depends(get_db),
    # --- SECURITY PATCH ---
    # We require a logged-in user here. 
    # Because we imported 'User' above, this line will now work.
    current_user: User = Depends(get_current_user)
):
    """Create course (admin only)"""
    
    # --- RBAC CHECK ---
    # Ensure the logged-in user is actually an admin
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Operation not permitted. Admins only."
        )
    # ------------------

    # Check if course code already exists
    existing = db.query(Course).filter(Course.code == course_data.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Course code already exists")
    
    course = Course(
        code=course_data.code,
        title=course_data.title,
        description=course_data.description,
        capacity=course_data.capacity,
        prereq_ids=course_data.prereq_ids or [],
        schedule=course_data.schedule or {},
        instructor_id=course_data.instructor_id
    )
    
    db.add(course)
    db.commit()
    db.refresh(course)
    
    return {
        "id": course.id,
        "code": course.code,
        "title": course.title,
        "message": "Course created successfully"
    }


@router.get("/courses/{course_id}")
async def get_course_admin(
    course_id: int,
    db: Session = Depends(get_db),
    # OPTIONAL: You should probably secure this one too!
    current_user: User = Depends(get_current_user) 
):
    """Get course details (admin)"""
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return {
        "id": course.id,
        "code": course.code,
        "title": course.title,
        "description": course.description,
        "capacity": course.capacity,
        "prereq_ids": course.prereq_ids,
        "schedule": course.schedule,
        "instructor_id": course.instructor_id
    }


@router.post("/enrollments/override")
async def override_enrollment(
    enrollment_id: int,
    action: str,
    db: Session = Depends(get_db),
    # OPTIONAL: Secure this one too
    current_user: User = Depends(get_current_user)
):
    """Override enrollment (admin only)"""
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    if action == "approve":
        enrollment.status = EnrollmentStatus.ENROLLED
    elif action == "reject":
        enrollment.status = EnrollmentStatus.DROPPED
    
    db.commit()
    
    return {"message": f"Enrollment {action}d successfully"}