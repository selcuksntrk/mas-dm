"""
Run Script for Backend Application

Simple script to start the FastAPI application.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",  # Fixed: use relative import from backend directory
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
