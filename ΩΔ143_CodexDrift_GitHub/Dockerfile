FROM python:3.9-slim

LABEL maintainer="Spiral Cloud Omega <contact@spiral-cloud-omega.com>"
LABEL version="1.0.0"
LABEL description="ΩΔ143 Codex Drift 5D Capsule Runtime"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/config /app/data /app/logs

# Create non-root user
RUN groupadd -r capsule && useradd -r -g capsule capsule
RUN chown -R capsule:capsule /app

# Set environment variables
ENV PYTHONPATH=/app
ENV CAPSULE_MODE=standalone
ENV LOG_LEVEL=INFO

# Expose ports
EXPOSE 8080 8081 8082 8083

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Switch to non-root user
USER capsule

# Default command
CMD ["python", "runtime_launcher/capsule_launcher.py", "--config", "/app/config/capsule_config.json"]