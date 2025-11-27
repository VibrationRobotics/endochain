# ENDOCHAIN-VIDUYA-2025 Docker Image
# Viduya Family Legacy Glyph © 2025 – All Rights Reserved

FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production image
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY core/ ./core/
COPY backend/ ./backend/
COPY ai_integrations/ ./ai_integrations/
COPY hardware/ ./hardware/

# Copy configuration
COPY endochain_mvp_v2/config/ ./config/

# Create non-root user for security
RUN useradd -m -u 1000 endochain
USER endochain

# Environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose API port
EXPOSE 8000

# Run with uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

LABEL maintainer="IAMVC Holdings LLC"
LABEL version="1.0.0"
LABEL description="ENDOCHAIN-VIDUYA-2025 - Geometrically-Anchored Endometriosis Diagnostic System"
LABEL citation="Viduya Family Legacy Glyph © 2025"

