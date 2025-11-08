"""
Run Script for Backend Application

Simple script to start the FastAPI application.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8001,  # Use different port from old app
        reload=True,
        log_level="info"
    )
