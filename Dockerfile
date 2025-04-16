FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create a non-root user to run the application
RUN useradd -m appuser
USER appuser

# Default environment configuration - uses mock API by default
ENV API_KEY="your_api_key_here" \
    API_BASE_URL="https://api.financialreports.eu/" \
    USE_MOCK_API="True" \
    MCP_HOST="0.0.0.0" \
    MCP_PORT="8000"

# Add a health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get(f'http://localhost:{MCP_PORT}/mcp/ping').raise_for_status()"

# Expose the port the app runs on
EXPOSE ${MCP_PORT}

# Run the application directly with main.py
CMD ["python", "main.py", "--host", "0.0.0.0"]
