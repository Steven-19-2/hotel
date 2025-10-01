from fastapi import FastAPI, Request
app = FastAPI()
REQUEST_COUNT = 0
@app.middleware("http")
async def count_requests(request: Request, call_next):
 global REQUEST_COUNT
 REQUEST_COUNT += 1
 return await call_next(request)
@app.get("/health")
def health():
 return {"status": "ok"}
@app.get("/metrics")
def metrics():
 return {"requests_total": REQUEST_COUNT}