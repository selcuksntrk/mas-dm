# ==============================================================================
# DOCKERFILE EXPLANATION FOR BACKEND API
# ==============================================================================
# This Dockerfile creates a containerized environment for running the backend API.
# Docker containers are lightweight, isolated environments that package your app
# with all its dependencies, ensuring it runs the same everywhere.
#
# Key Concepts:
# - Image: A template/blueprint for creating containers (like a class in OOP)
# - Container: A running instance of an image (like an object/instance)
# - Layer: Each instruction creates a cached layer for faster rebuilds
# - Multi-stage: Use multiple FROM statements to create smaller final images
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Builder Stage
# ------------------------------------------------------------------------------
# Purpose: Install dependencies and prepare the application
# Why separate stage? Keeps the final image small by not including build tools
FROM python:3.13-slim as builder

# Set working directory inside the container
# All subsequent commands will run from this directory
WORKDIR /app

# Install system dependencies needed for Python packages
# - curl: for downloading files (uv installer)
# - build-essential: C compiler for building Python packages with C extensions
# - git: some Python packages need git to install from repos
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install UV (fast Python package installer)
# UV is much faster than pip and handles dependencies better
# The installer puts binaries in /root/.local/bin by default
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/uv && \
    mv /root/.local/bin/uvx /usr/local/bin/uvx

# Copy only dependency files first (optimization technique)
# Why? Docker caches each layer. If pyproject.toml doesn't change,
# Docker reuses the cached layer instead of reinstalling everything
COPY pyproject.toml ./

# Install Python dependencies
# --system: install packages globally (not in a virtual env)
# --no-cache: don't store downloaded packages (saves space)
RUN uv pip install --system --no-cache -r pyproject.toml

# ------------------------------------------------------------------------------
# Stage 2: Runtime Stage
# ------------------------------------------------------------------------------
# Purpose: Create the minimal final image with only what's needed to run
# This stage is much smaller because it doesn't include build tools
FROM python:3.13-slim

# Create a non-root user for security
# Running as root inside containers is a security risk
# If someone breaks into your container, they have limited permissions
RUN useradd -m -u 1000 appuser

# Set working directory
WORKDIR /app

# Copy installed packages from builder stage
# This copies the Python packages but not the build tools
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
# We copy backend/app into /app/backend/app to preserve the import structure
COPY --chown=appuser:appuser ./app /app/backend/app

# Switch to non-root user
USER appuser

# Expose port 8001 (tells Docker which port the app listens on)
# This doesn't actually publish the port; it's documentation
# You still need -p 8001:8001 when running docker run
EXPOSE 8001

# Health check: Docker will periodically check if the app is healthy
# If health checks fail, Docker can restart the container
# --interval: how often to check (30s)
# --timeout: how long to wait for response (10s)
# --start-period: grace period during startup (40s)
# --retries: how many failures before marking unhealthy (3)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8001/health').read()" || exit 1

# Set environment variables
# PYTHONUNBUFFERED: Print logs immediately (don't buffer)
# PYTHONDONTWRITEBYTECODE: Don't create .pyc files (cleaner container)
# PYTHONPATH: Add parent directory so 'backend.app' imports work correctly
#   Inside container: /app/app/main.py can import as 'backend.app.main'
#   This is because /app is added to PYTHONPATH, making /app/app = backend/app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app:$PYTHONPATH

# Default command to run when container starts
# Uses exec form (list) which is better than shell form (string)
# --host 0.0.0.0: listen on all network interfaces (required for Docker)
# --port 8001: the port to listen on
# Now using backend.app.main:app since we preserved the directory structure
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8001"]
