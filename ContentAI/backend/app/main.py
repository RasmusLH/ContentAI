from fastapi import FastAPI
from app.routes import router as generate_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LinkedIn Post Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://localhost:3000"] for stricter control
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate_router)

@app.get("/health")
async def health():
    return {"status": "ok"}
