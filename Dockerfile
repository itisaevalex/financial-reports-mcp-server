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
    MCP_TRANSPORT="stdio"

# Run the application 
# Note: When used with Claude Desktop, this will be overridden by the command
# that Claude provides, but for direct docker run commands this is the default
CMD ["python", "main.py", "--transport", "stdio"]
