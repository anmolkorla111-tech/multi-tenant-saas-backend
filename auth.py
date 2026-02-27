from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
def login():
    # Simple dummy login, JWT add kar sakte ho later
    return {"access_token": "dummy_token", "token_type": "bearer"}