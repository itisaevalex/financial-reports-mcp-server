# Financial Reports MCP Server

## 🎬 Demo

<div align="center">
  <img src="data/deutsche-bank-analysis.gif" alt="Demo: Deutsche Bank Analysis" style="border-radius: 16px; box-shadow:0 2px 8px #0003; max-width: 50%; height: auto;">
</div>


An MCP (Model Context Protocol) server for accessing the Financial Reports API, providing tools and resources to access company financial filings, industry classifications, and related data.

## Features

- Search for companies by name, country, or sector
- Get detailed company information
- Access latest financial filings
- Look up industry classifications
- Get filing details and content

## Prerequisites

- Python 3.9+
- Docker (recommended)
- FastMCP (if running locally)
- dotenv for environment variable management (if running locally)

**Note:** The server now uses only the real Financial Reports API. All mock API logic and configuration has been removed for simplicity and reliability.

## 🚀 Getting Started

There are multiple ways to get up and running with this MCP server:

### 🚀 Option 1: Docker (Recommended)

**Docker is the recommended way** to run this MCP server for reproducibility, ease of setup, and isolation from your system Python. This is ideal for Claude Desktop, CI, and onboarding.

```bash
# Clone the repository
git clone <repository-url>
cd financial-reports-mcp

# Build the Docker image
docker build -t financial-reports-mcp .

# Run with Docker
docker run -i financial-reports-mcp
```

For Claude Desktop, add the following configuration:

```json
{
  "mcpServers": {
    "financial-reports": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "financial-reports-mcp:latest"
      ],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```

---

### 🚀 Option 2: Smithery CLI (Claude)

[![smithery badge](https://smithery.ai/badge/@itisaevalex/financial-reports-mcp-server)](https://smithery.ai/server/@itisaevalex/financial-reports-mcp-server)

For Claude:
```bash
npx -y @smithery/cli@latest install @itisaevalex/financial-reports-mcp-server --client claude --key smithery_api_key
```

---

## Examples

All example scripts and configs are now located in the `examples/` directory, e.g.:

- `examples/test_server.py` — Run the full MCP test suite
- `examples/docker_claude_config.json` — Example Claude Desktop config for Docker
- `examples/uvx_claude_config.json` — Example Claude Desktop config for uv
- `examples/python_client_example.py` — Example Python client usage

Run the test suite:
```bash
python examples/test_server.py
```

---

### Option 2: Quick Start with uv (For advanced users or dev)

You can also use the `uv` package manager if you prefer a local Python environment:

```bash
# Install uv if you don't have it
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
curl -LsSf https://astral.sh/uv/install.ps1 | powershell

# Clone the repository
git clone <repository-url>
cd financial-reports-mcp

# Run with uv
uv run server.py
```

For Claude Desktop, add the following configuration:

```json
{
  "mcpServers": {
    "financial-reports": {
      "command": "/path/to/uv",
      "args": [
        "--directory",
        "/absolute/path/to/financial-reports-mcp",
        "run",
        "server.py"
      ]
    }
  }
}
```

### Option 2: Docker (Recommended for Reproducibility)

For reproducible environments across systems:

```bash
# Clone the repository
git clone <repository-url>
cd financial-reports-mcp

# Build the Docker image
docker build -t financial-reports-mcp .

# Run with Docker
docker run -i financial-reports-mcp
```

For Claude Desktop, add the following configuration:

```json
{
  "mcpServers": {
    "financial-reports": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "financial-reports-mcp:latest"
      ],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Option 3: Run Directly (For development or testing)

```bash
# Clone the repository
git clone <repository-url>
cd financial-reports-mcp

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m src.financial_reports_mcp
# or
python src/financial_reports_mcp.py
```

### Option 4: Use FastMCP CLI

The FastMCP CLI provides tools for development and installation of MCP servers.

```bash
# Install FastMCP globally
pip install fastmcp

# Then install the Financial Reports MCP server
# From the project directory:
fastmcp install server.py --name "Financial Reports API"

# Or run in development mode
fastmcp dev server.py
```

## Configuration

Create a `.env` file in the root directory with the following variables:

```
API_KEY="your_api_key_here"
API_BASE_URL="https://api.financialreports.eu/"
USE_MOCK_API=True
```

- Set `USE_MOCK_API=True` to use mock data (default)
- Set `USE_MOCK_API=False` to use the real API (requires valid API key)

## Project Structure

- `server.py` - Simple single-file implementation (recommended for uv)
- `main.py` - Main entry point for more customizable usage
- `src/` - Source code directory
  - `financial_reports_mcp.py` - MCP server implementation
  - `api_client.py` - API client factory
  - `mock_api/` - Mock API implementation
    - `mock_client.py` - Mock API client
    - JSON files with mock responses
- `.env` - Environment variables (not in git)
- `requirements.txt` - Project dependencies
- `Dockerfile` & `docker-compose.yml` - Docker configuration
- `setup.py` - Package installation configuration
- `install.py` - Helper for Claude Desktop installation
- `examples/` - Example scripts and configs
- `scripts/` - Install scripts

## Available Tools

- `search_companies`: Search for companies by name or other identifying information
- `get_company_detail`: Get detailed information about a specific company
- `get_latest_filings`: Get the latest financial filings
- `get_filing_detail`: Get detailed information about a specific filing
- `list_sectors`: List all available GICS sectors
- `list_filing_types`: List all available filing types

## Available Resources

- `financial-reports://sectors`: List of all GICS sectors
- `financial-reports://filing-types`: List of all filing types
- `financial-reports://companies/{company_id}/profile`: Company profile
- `financial-reports://companies/{company_id}/recent-filings`: Recent filings for a company

## Examples

### Example 1: Search for a company and get its profile

```
I want to search for information about Deutsche Bank. Please help me find:
1. Basic company details like country, sector and industry
2. Recent financial filings
3. Key financial metrics if available
```

### Example 2: Find the latest annual reports for banks

```
I'd like to see the latest annual reports from major European banks. 
Please help me:
1. Find companies in the banking sector
2. Get their latest annual reports
3. Summarize key financial metrics from these reports if available
```

## Cross-Platform Compatibility

The server can be run on:

- **Linux**: All methods supported
- **macOS**: All methods supported 
- **Windows**: All methods supported, but using `uv` is recommended for Claude Desktop

For Windows users specifically:
- For Claude Desktop, uv-based installation is recommended
- Docker requires Docker Desktop for Windows

## Troubleshooting

### Common Issues

1. **Communication Issues with Claude Desktop**: 
   - Ensure you're using stdio transport when configuring for Claude Desktop
   - For Docker, make sure to include the `-i` flag for interactive mode

2. **"Module not found" errors**: 
   - Make sure all dependencies are installed with `pip install -r requirements.txt`
   
3. **Cannot connect to the MCP server**: 
   - Check if the server is running and accessible from the client

4. **Authentication errors with the API**: 
   - Verify your API key in the `.env` file

### Logs

When running directly, logs are output to the console. For Docker, you can view logs with:

```bash
docker logs <container-id>
```

## License

This project is licensed under the MIT License with an attribution requirement for Data Alchemy Labs. See [LICENSE](LICENSE) for details.
