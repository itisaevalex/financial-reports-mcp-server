FROM python:3.11-slim as base

# Set up environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

# Create a non-root user to run the application
RUN useradd -m appuser

FROM base as builder

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install build dependencies and the application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Build the application package
RUN pip install --no-cache-dir .

FROM base as final

WORKDIR /app

# Copy only the built package from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the app configuration files and mock data
COPY --from=builder /app/.env.example /app/.env
COPY --from=builder /app/src/mock_api/*.json /app/src/mock_api/

# Switch to the non-root user
USER appuser

# Default environment configuration - uses mock API by default
ENV API_KEY="your_api_key_here" \
    API_BASE_URL="https://api.financialreports.eu/" \
    USE_MOCK_API="True" \
    MCP_HOST="0.0.0.0" \
    MCP_PORT="8000"

# Add a health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get(f'http://localhost:{int(\"$MCP_PORT\")}/mcp/ping').raise_for_status()"

# Expose the port the app runs on
EXPOSE ${MCP_PORT}

# Run the application
CMD ["python", "-m", "financial_reports_mcp_server"]
