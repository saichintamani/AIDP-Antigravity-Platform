# Stage 1: Base Python Environment
FROM python:3.11-slim as backend

# Set runtime metadata
LABEL maintainer="AIDP Team"
LABEL version="1.0.0"
LABEL description="AIDP Zero-Cloud Local Inference Image"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
RUN groupadd -r aidpuser && useradd -r -g aidpuser aidpuser

# Install Python dependencies
# In a real environment, we would use requirements.txt, but for zero-cloud deployment:
RUN pip install fastapi uvicorn requests pydantic numpy

# Copy core AIDP engine and API
COPY --chown=aidpuser:aidpuser ./src /app/src
COPY --chown=aidpuser:aidpuser ./data /app/data

# Set the active user
USER aidpuser

# Expose FastAPI Port
EXPOSE 8000

# Container healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Start FastAPI server
CMD ["uvicorn", "src.aidp.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
