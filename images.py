import os
from fastapi import UploadFile, File, APIRouter, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

router = APIRouter()
os.makedirs('static/images', exist_ok=True)

@router.post("/rooms/{room_id}/upload-image")
async def upload_image(room_id: int, file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ('.jpg', '.jpeg', '.png'):
        raise HTTPException(status_code=400, detail="image must be jpg or png")
    dest = f"static/images/room_{room_id}{ext}"
    with open(dest, "wb") as f:
        content = await file.read()
        f.write(content)
    return {"url": f"/static/images/room_{room_id}{ext}"} 
