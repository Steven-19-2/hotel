from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

# Routers
from bookings import router as bookings_router
from availability import router as hotel_router
from auth import router as auth_router
from images import router as images_router
from pagination import router as r_list
from rooms_crud import router as rooms_crud_router
from background_tasks import router as background_router
from ws import app as ws_app 
from ws import websocket_endpoint
from cache_example import expensive_stats
#from rbac import router as rbac_router
from settings import get_settings

app = FastAPI(title="Hotel API", version="0.1")

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Hotel API!"}

@app.get("/")
def read_root(settings = Depends(get_settings)):
    return {"message": f"Welcome to {settings.app_name}!"}
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev: http://localhost:3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Include Routers
# ---------------------------

# Availability / hotel rooms (legacy or temporary router)
app.include_router(hotel_router, tags=["Rooms"])

# CRUD for rooms (with staff-only endpoints protected inside the router)
app.include_router(rooms_crud_router, tags=["Rooms"])

# Bookings
app.include_router(bookings_router, prefix="/api", tags=["Bookings"])

# Background tasks for bookings with email
app.include_router(background_router, tags=["Bookings"])

# Auth
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
#app.include_router(rbac_router, tags=["Auth"])
# Images
app.include_router(images_router, tags=["Images"])

# Pagination / listing
app.include_router(r_list, prefix="/rooms", tags=["Rooms"])

@app.get("/stats/{year}")
def stats(year: int):
    return expensive_stats(year) 
