"""
Enrollment model
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base


class EnrollmentStatus(enum.Enum):
    ENROLLED = "enrolled"
    DROPPED = "dropped"
    WAITLISTED = "waitlisted"


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(EnrollmentStatus), nullable=False, default=EnrollmentStatus.ENROLLED)
    timestamp = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    course = relationship("Course", back_populates="enrollments")
    user = relationship("User", back_populates="enrollments")

    # Unique constraint
    __table_args__ = (UniqueConstraint('course_id', 'user_id', name='unique_enrollment'),)

class AuditRecord(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer) # Who did it?
    action = Column(String)    # What happened?
    target = Column(String)    # Which course/user?
    details = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)