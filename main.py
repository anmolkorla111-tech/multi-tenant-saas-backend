from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import SessionLocal
from models import User, Attendance

app = FastAPI()


class UserCreate(BaseModel):
    email: str


class AttendanceCreate(BaseModel):
    user_id: int
    status: str  # present / absent


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "API Running"}


@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "email": new_user.email}


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id, "email": u.email, "created_at": str(u.created_at)} for u in users]


@app.post("/attendance")
def mark_attendance(data: AttendanceCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    status = data.status.strip().lower()
    if status not in ["present", "absent"]:
        raise HTTPException(status_code=400, detail="status must be 'present' or 'absent'")

    record = Attendance(user_id=data.user_id, status=status)
    db.add(record)
    db.commit()
    db.refresh(record)
    return {
        "id": record.id,
        "user_id": record.user_id,
        "attendance_date": str(record.attendance_date),
        "status": record.status,
        "created_at": str(record.created_at),
    }


@app.get("/attendance")
def get_attendance(db: Session = Depends(get_db)):
    records = db.query(Attendance).all()
    return [
        {
            "id": r.id,
            "user_id": r.user_id,
            "attendance_date": str(r.attendance_date),
            "status": r.status,
            "created_at": str(r.created_at),
        }
        for r in records
    ]