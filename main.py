from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from datetime import datetime

from database import SessionLocal
from models import User, Attendance, Tenant

app = FastAPI(title="Multi-Tenant SaaS Backend")


# ---------- DB Dependency ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Schemas ----------
class TenantCreate(BaseModel):
    name: str


class TenantOut(BaseModel):
    id: int
    name: str
    created_at: datetime


class UserCreate(BaseModel):
    email: EmailStr


class UserOut(BaseModel):
    id: int
    tenant_id: int
    email: EmailStr
    created_at: datetime


class AttendanceCreate(BaseModel):
    user_id: int
    status: str  # "present" / "absent"


class AttendanceOut(BaseModel):
    id: int
    tenant_id: int
    user_id: int
    attendance_date: datetime
    status: str
    created_at: datetime


# ---------- Helpers ----------
def require_tenant_id(x_tenant_id: int | None):
    if x_tenant_id is None:
        raise HTTPException(
            status_code=400,
            detail="Missing X-Tenant-ID header. Example: X-Tenant-ID: 1"
        )
    return x_tenant_id


def get_tenant_or_404(db: Session, tenant_id: int):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant


# ---------- Health ----------
@app.get("/")
def root():
    return {"message": "Multi-Tenant SaaS Backend API is running"}


# ---------- Tenants ----------
@app.post("/tenants", response_model=TenantOut)
def create_tenant(payload: TenantCreate, db: Session = Depends(get_db)):
    existing = db.query(Tenant).filter(Tenant.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tenant name already exists")

    tenant = Tenant(name=payload.name)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant


@app.get("/tenants", response_model=list[TenantOut])
def list_tenants(db: Session = Depends(get_db)):
    return db.query(Tenant).order_by(Tenant.id.asc()).all()


# ---------- Users (Tenant-wise) ----------
@app.post("/users", response_model=UserOut)
def create_user(
    payload: UserCreate,
    x_tenant_id: int | None = Header(default=None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
):
    tenant_id = require_tenant_id(x_tenant_id)
    get_tenant_or_404(db, tenant_id)

    # Duplicate email within same tenant check (simple)
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(email=payload.email, tenant_id=tenant_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/users", response_model=list[UserOut])
def list_users(
    x_tenant_id: int | None = Header(default=None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
):
    tenant_id = require_tenant_id(x_tenant_id)
    get_tenant_or_404(db, tenant_id)

    return db.query(User).filter(User.tenant_id == tenant_id).order_by(User.id.asc()).all()


# ---------- Attendance (Tenant-wise) ----------
@app.post("/attendance", response_model=AttendanceOut)
def mark_attendance(
    payload: AttendanceCreate,
    x_tenant_id: int | None = Header(default=None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
):
    tenant_id = require_tenant_id(x_tenant_id)
    get_tenant_or_404(db, tenant_id)

    status = payload.status.lower().strip()
    if status not in ("present", "absent"):
        raise HTTPException(status_code=400, detail="status must be 'present' or 'absent'")

    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Ensure tenant isolation
    if user.tenant_id != tenant_id:
        raise HTTPException(status_code=403, detail="User does not belong to this tenant")

    record = Attendance(
        user_id=payload.user_id,
        tenant_id=tenant_id,
        status=status,
        attendance_date=datetime.utcnow(),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@app.get("/attendance", response_model=list[AttendanceOut])
def list_attendance(
    x_tenant_id: int | None = Header(default=None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
):
    tenant_id = require_tenant_id(x_tenant_id)
    get_tenant_or_404(db, tenant_id)

    return (
        db.query(Attendance)
        .filter(Attendance.tenant_id == tenant_id)
        .order_by(Attendance.id.desc())
        .all()
    )