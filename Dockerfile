FROM python:3.13.15-slim-bookworm

WORKDIR /app

# Python runtime settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Copy dependency file first
# This allows Docker to cache the dependency layer
COPY requirements.txt .

# Install Python dependencies
RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

# Copy application
COPY . .

# Application port
EXPOSE 8000

# Start FastAPI
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]