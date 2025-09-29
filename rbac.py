from fastapi import Depends, HTTPException, APIRouter, FastAPI
from auth import get_current_user
# app = FastAPI()
# router = APIRouter()

#app.include_router(rout)
def staff_required(current_user = Depends(get_current_user)):
    if current_user.get("role") != "staff":
        raise HTTPException(status_code=403, detail="staff role required")
    return current_user

#@router.post("/rauth", dependencies=[Depends(staff_required)])
def read_root():
    return {"message": "Welcome to the Hotel API!"}