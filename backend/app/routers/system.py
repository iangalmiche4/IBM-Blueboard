"""
System information router
"""

import platform
import sys
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.startup import APP_START_TIME

router = APIRouter()


@router.get("/info")
async def get_system_info(db: Session = Depends(get_db)):
    """
    Get system information including API status, database info, and versions
    """
    # Get database version
    try:
        result = db.execute(text("SELECT version()"))
        db_version = result.scalar()
        # Extract PostgreSQL version number
        db_version_short = db_version.split()[1] if db_version else "Unknown"
        db_status = "connected"
    except Exception as e:
        db_version_short = "Unknown"
        db_status = "disconnected"

    # Get database statistics
    try:
        # Count total records across main tables
        tables_count = {}
        for table in ["products", "sales", "customers", "satisfaction"]:
            result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
            tables_count[table] = result.scalar()

        total_records = sum(tables_count.values())
    except Exception:
        total_records = 0
        tables_count = {}

    return {
        "version": settings.VERSION,
        "build_date": APP_START_TIME.strftime("%Y-%m-%d"),
        "api_status": "connected",
        "database": {
            "type": "PostgreSQL",
            "version": db_version_short,
            "status": db_status,
            "total_records": total_records,
            "tables": tables_count,
        },
        "environment": settings.ENVIRONMENT,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "platform": platform.system(),
        "last_updated": datetime.utcnow().isoformat(),
    }
