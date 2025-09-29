# from fastapi import BackgroundTasks, APIRouter
# from bookings import create_booking # assume function that saves booking
# router = APIRouter()
# def send_confirmation_email(booking_id: int, email: str):
#     # simulated long-running action
#     import time
#     time.sleep(1)
#     print(f"Sent confirmation for booking {booking_id} to {email}")

# @router.post("/bookings_with_email/")
# def book_with_email(payload, background_tasks: BackgroundTasks):
#     booking = create_booking(payload) # synchronous for demo
#     background_tasks.add_task(send_confirmation_email, booking.id, payload.guest_email or "guest@example.com")
#     return {"booking_id": booking.id, "status": "confirmed (email queued)"} 

from fastapi import BackgroundTasks, APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from bookings import create_booking
from models import BookingCreate
from pydantic import BaseModel

router = APIRouter()


def send_confirmation_email(booking_id: int, email: str):
    # simulated long-running action
    import time
    time.sleep(1)
    print(f"Sent confirmation for booking {booking_id} to {email}")


class BookingWithEmailCreate(BookingCreate):
    email: str


@router.post("/bookings_with_email/")
def book_with_email(
    payload: BookingWithEmailCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # create booking in DB
    booking = create_booking(payload, db)

    # queue confirmation email
    background_tasks.add_task(send_confirmation_email, booking.id, payload.email)

    return {"booking_id": booking.id, "status": "confirmed (email queued)"}
