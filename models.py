from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


# ✅ NEW: Tenant (Organization/Company)
class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="tenant")


# ✅ Users table (now tenant-aware)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # Each user belongs to one tenant
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)

    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant = relationship("Tenant", back_populates="users")
    attendance_records = relationship("Attendance", back_populates="user")


# ✅ Attendance table (now tenant-aware)
class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)

    # Each attendance belongs to one tenant + one user
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    attendance_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=False)  # present / absent
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="attendance_records")