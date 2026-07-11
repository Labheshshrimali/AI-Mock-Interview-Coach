from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.api.health_routes import router as health_router
from app.api.session_routes import router as session_router

app = FastAPI(title="AI Mock Interview Coach API")

# Initialize DB on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(health_router)
app.include_router(session_router)
