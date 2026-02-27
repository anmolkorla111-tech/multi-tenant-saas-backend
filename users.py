from fastapi import APIRouter, Header, HTTPException
from typing import List

router = APIRouter()

# Dummy storage
users_db: List[dict] = []

@router.get("/")
def get_users(authorization: str = Header(None)):
    if not authorization or "Bearer" not in authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return users_db

@router.post("/")
def create_user(user: dict, authorization: str = Header(None)):
    if not authorization or "Bearer" not in authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    users_db.append(user)
    return {"message": f"User {user['username']} created"}