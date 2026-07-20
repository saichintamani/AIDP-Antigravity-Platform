# Stage 1: Base Python Environment
FROM python:3.11-slim as backend

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# In a real environment, we would use requirements.txt, but for zero-cloud deployment:
RUN pip install fastapi uvicorn requests pydantic numpy

# Copy core AIDP engine and API
COPY ./src /app/src
COPY ./data /app/data

# Expose FastAPI Port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "src.aidp.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
