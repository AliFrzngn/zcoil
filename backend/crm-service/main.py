"""
CRM Service - FastAPI application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="CRM Service",
    description="Microservice for managing customers, leads, and deals",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "CRM Service is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "crm-service"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
