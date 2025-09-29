from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db import get_db, Room
router = APIRouter()

@router.get("/rooms/")
def list_rooms(skip: int = 0, limit: int = 10, min_price: int | None = None,
    max_price: int | None = None, type: str | None = None,
    db: Session = Depends(get_db)):
    q = db.query(Room)
    if min_price is not None:
        q = q.filter(Room.price >= min_price)
    if max_price is not None:
        q = q.filter(Room.price <= max_price)
    if type:
        q = q.filter(Room.type == type)
    total = q.count()
    items = q.offset(skip).limit(limit).all()
    return {"total": total, "skip": skip, "limit": limit, "items": items} 