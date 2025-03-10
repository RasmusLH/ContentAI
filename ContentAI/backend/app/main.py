from fastapi import FastAPI
from app.routes import router as generate_router
from fastapi.middleware.cors import CORSMiddleware
from .database import connect_to_mongo, close_mongo_connection

app = FastAPI(title="LinkedIn Post Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://localhost:3000"] for stricter control
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Update the router inclusion to remove the prefix
app.include_router(generate_router, prefix="")

@app.on_event("startup")
async def startup():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown():
    await close_mongo_connection()

@app.get("/health")
async def health():
    return {"status": "ok"}
