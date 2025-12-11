from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import db
from app.routers import auth, organization

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db.connect()
    yield
    # Shutdown
    db.close()

app = FastAPI(
    title="Organization Management Service",
    description="Backend Assignment for Multi-tenant Organization Management",
    version="1.0.0",
    lifespan=lifespan
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Runtime Error", "error": str(exc)},
    )

# CORS (Optional but good for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["Auth"])
app.include_router(organization.router, tags=["Organizations"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "db": "connected" if db.client else "disconnected"}

@app.get("/")
async def root():
    return {"message": "Welcome to the Organization Management Service API"}
