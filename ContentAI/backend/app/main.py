from fastapi import FastAPI
from app.routes import router as generate_router

app = FastAPI(title="Danish Social Media Post Generator MVP")

app.include_router(generate_router)

@app.get("/health")
async def health():
    return {"status": "ok"}
