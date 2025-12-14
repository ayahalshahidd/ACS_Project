"""
Enrollment routes
VULNERABLE: CSRF - No token validation
"""

from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from database import get_db
from models.enrollment import Enrollment, EnrollmentStatus
from models.course import Course
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class EnrollmentRequest(BaseModel):
    course_id: int
    student_id: int


@router.post("")
async def create_enrollment(
    course_id: int = Form(...),    # Changed from Pydantic model to Form
    student_id: int = Form(...),   # Changed from Pydantic model to Form
    db: Session = Depends(get_db)
):
    """
    VULNERABLE: CSRF
    Now accepts standard HTML Form data, making it easy to exploit.
    """
    # ... keep your existing logic below (checking course, capacity, etc.) ...
    
    # Example logic using the new variables:
    enrollment = Enrollment(
        course_id=course_id,
        user_id=student_id,
        status=EnrollmentStatus.ENROLLED
    )
    db.add(enrollment)
    db.commit()
    return {"message": "Enrollment successful"}

@router.delete("/{enrollment_id}")
async def drop_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db)
):
    """Drop enrollment"""
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    enrollment.status = EnrollmentStatus.DROPPED
    db.commit()
    
    return {"message": "Enrollment dropped successfully"}


@router.get("")
async def get_enrollments(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get enrollments"""
    query = db.query(Enrollment)
    
    if user_id:
        query = query.filter(Enrollment.user_id == user_id)
    
    enrollments = query.all()
    
    return [
        {
            "id": e.id,
            "course_id": e.course_id,
            "user_id": e.user_id,
            "status": e.status.value,
            "timestamp": e.timestamp.isoformat()
        }
        for e in enrollments
    ]

