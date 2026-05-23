from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.domains import router as domain_routers

app = FastAPI(
    title="Computer Science Daily Trivia API",
    description="API for serving computer science daily trivia questions and answers.",
    version="1.0.0",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (configure as needed for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(
    domain_routers,
)
