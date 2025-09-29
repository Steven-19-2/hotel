from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
class RoomBase(BaseModel):
    number: str = Field(..., example="101")
    type: str = Field(..., example="double")
    price: int = Field(..., ge=0)
    capacity: int = Field(..., ge=1)
class RoomCreate(RoomBase):
    pass
class Room(RoomBase):
    id: int
    class Config:
        orm_mode = True
class Guest(BaseModel):
    name: str
    email: Optional[str] = None
class BookingCreate(BaseModel):
    room_id: int
    guest_name: str
    start_date: date
    end_date: date 
