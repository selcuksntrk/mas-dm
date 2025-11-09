"""
Main FastAPI Application

This is the entry point for the Multi-Agent Decision Making API.
It configures the FastAPI app with all routes, middleware, and settings.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.api.routes import health, graph, decisions


# Get application settings
settings = get_settings()


# Create FastAPI application
app = FastAPI(
    title="Multi-Agent Decision Making API",
    description="""
    A sophisticated multi-agent system for structured decision-making.
    
    This API orchestrates multiple AI agents through a graph-based workflow to help
    users make informed decisions. The system:
    
    - Identifies decision triggers and analyzes root causes
    - Defines scope and establishes SMART goals
    - Generates and evaluates alternatives
    - Provides reasoned recommendations with alternatives
    
    ## Features
    
    - **Synchronous Execution**: Get immediate results with `/decisions/run`
    - **Asynchronous Execution**: Start long-running processes with `/decisions/start`
    - **Process Tracking**: Monitor progress with `/decisions/status/{id}`
    - **Graph Visualization**: View workflow with `/graph/mermaid`
    - **Persistence Mode**: Debug with `/decisions/cli`
    
    ## Workflow Phases
    
    1. **Analysis**: Trigger identification, root cause analysis, scope definition
    2. **Drafting**: Initial decision draft and goal establishment
    3. **Information Gathering**: Identify and retrieve needed information
    4. **Alternatives**: Generate and evaluate alternatives
    5. **Decision**: Select best option with justification
    
    Each phase includes agent execution and evaluator validation with feedback loops.
    """,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(health.router)
app.include_router(graph.router)
app.include_router(decisions.router)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors.
    
    Returns a JSON response with error details.
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc),
            "type": type(exc).__name__
        }
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Startup event handler.
    
    Performs initialization tasks when the application starts.
    """
    print("=" * 60)
    print("Multi-Agent Decision Making API")
    print("=" * 60)
    print(f"Version: {app.version}")
    print(f"Docs: http://localhost:8001/docs")
    print(f"Model: {settings.model_name}")
    print(f"Evaluation Model: {settings.evaluation_model}")
    print("=" * 60)


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event handler.
    
    Performs cleanup tasks when the application shuts down.
    """
    print("\nShutting down Multi-Agent Decision Making APP...")


if __name__ == "__main__":
    import uvicorn
    
    # Run the FastAPI app
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
