# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt* pyproject.toml* ./

# Try to install from requirements.txt if it exists, otherwise install minimal deps
RUN if [ -f requirements.txt ]; then \
      pip install --user --no-cache-dir -r requirements.txt; \
    else \
      pip install --user --no-cache-dir flask requests python-dotenv uvicorn fastapi websockets; \
    fi

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Set PATH to use user-installed packages
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create necessary directories
RUN mkdir -p state mycelium/logs mycelium/memory

# Expose ports
EXPOSE 8000 8082 7001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/status || exit 1

# Start daemon server
CMD ["python", "-m", "uvicorn", "mycelium-hub.daemon.server:app", "--host", "0.0.0.0", "--port", "8000"]
