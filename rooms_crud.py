# from fastapi import FastAPI, HTTPException, APIRouter
# from models import Room, RoomCreate
# #app = FastAPI()
# router = APIRouter()
# rooms = []
# next_id = 1

# @router.post("/rooms/", response_model=Room)
# def create_room(room: RoomCreate):
#     global next_id
#     new = room.dict()
#     new['id'] = next_id
#     next_id += 1
#     rooms.append(new)
#     return new

# @router.get("/rooms/", response_model=list[Room])
# def list_rooms():
#     return rooms

# @router.get("/rooms/{room_id}", response_model=Room)
# def get_room(room_id: int):
#     for r in rooms:
#         if r['id'] == room_id:
#             return r
#     raise HTTPException(status_code=404, detail="Room not found")
# @router.put("/rooms/{room_id}", response_model=Room)
# def update_room(room_id: int, room: RoomCreate):
#     for r in rooms:
#         if r['id'] == room_id:
#             r.update(room.dict())
#             return r
#     raise HTTPException(status_code=404, detail="Room not found")

# @router.delete("/rooms/{room_id}")
# def delete_room(room_id: int):
#     for i, r in enumerate(rooms):
#         if r['id'] == room_id:
#             rooms.pop(i)
#             return {"ok": True}
#     raise HTTPException(status_code=404, detail="Room not found") 

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db, Room  # SQLAlchemy model
from pydantic import BaseModel
from rbac import staff_required  # import the staff check

router = APIRouter()

# ---------------------------
# Pydantic models for FastAPI
# ---------------------------

class RoomBase(BaseModel):
    number: str
    type: str
    price: int

class RoomCreate(RoomBase):
    pass

class RoomRead(RoomBase):
    id: int

    class Config:
        from_attributes = True  # v2 Pydantic: read SQLAlchemy ORM objects


# ---------------------------
# CRUD Endpoints
# ---------------------------

# Create room (staff only)
@router.post("/rooms/", response_model=RoomRead, dependencies=[Depends(staff_required)])
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    new_room = Room(**room.dict())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


# List all rooms (open to all)
@router.get("/rooms/", response_model=list[RoomRead])
def list_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()


# Get room by ID (open to all)
@router.get("/rooms/{room_id}", response_model=RoomRead)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


# Update room (staff only)
@router.put("/rooms/{room_id}", response_model=RoomRead, dependencies=[Depends(staff_required)])
def update_room(room_id: int, room: RoomCreate, db: Session = Depends(get_db)):
    db_room = db.query(Room).filter(Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")

    for key, value in room.dict().items():
        setattr(db_room, key, value)

    db.commit()
    db.refresh(db_room)
    return db_room


# Delete room (staff only)
@router.delete("/rooms/{room_id}", dependencies=[Depends(staff_required)])
def delete_room(room_id: int, db: Session = Depends(get_db)):
    db_room = db.query(Room).filter(Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")

    db.delete(db_room)
    db.commit()
    return {"ok": True}
