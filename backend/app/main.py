"""
IBM Blueboard API - Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import (
    analytics,
    customers,
    inventory,
    products,
    promotions,
    returns,
    sales,
    satisfaction,
    system,
)

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API for IBM Blueboard - Cosmetics Data Visualization Dashboard",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    products.router, prefix=f"{settings.API_V1_PREFIX}/products", tags=["products"]
)

app.include_router(
    sales.router, prefix=f"{settings.API_V1_PREFIX}/sales", tags=["sales"]
)

app.include_router(
    satisfaction.router,
    prefix=f"{settings.API_V1_PREFIX}/satisfaction",
    tags=["satisfaction"],
)

app.include_router(
    customers.router, prefix=f"{settings.API_V1_PREFIX}/customers", tags=["customers"]
)

app.include_router(
    analytics.router, prefix=f"{settings.API_V1_PREFIX}/analytics", tags=["analytics"]
)

app.include_router(
    system.router, prefix=f"{settings.API_V1_PREFIX}/system", tags=["system"]
)

app.include_router(
    inventory.router, prefix=f"{settings.API_V1_PREFIX}/inventory", tags=["inventory"]
)

app.include_router(
    promotions.router,
    prefix=f"{settings.API_V1_PREFIX}/promotions",
    tags=["promotions"],
)

app.include_router(
    returns.router, prefix=f"{settings.API_V1_PREFIX}/returns", tags=["returns"]
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to IBM Blueboard API",
        "version": settings.VERSION,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "environment": settings.ENVIRONMENT}
