# Financial Reports MCP Server

An MCP (Model Context Protocol) server for accessing the Financial Reports API, providing tools and resources to access company financial filings, industry classifications, and related data.

## Features

- Search for companies by name, country, or sector
- Get detailed company information
- Access latest financial filings
- Look up industry classifications
- Get filing details and content

## Prerequisites

- Python 3.9+
- FastMCP
- dotenv for environment variable management

## 🚀 Getting Started

There are multiple ways to get up and running with this MCP server:

### Option 1: Install and Run Locally

```bash
# Clone the repository
git clone <repository-url>
cd financial-reports-mcp

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up configuration
cp .env.example .env  # Then edit .env with your settings

# Run the server directly
python main.py
```

### Option 2: Use with FastMCP CLI

The FastMCP CLI provides tools for development and installation of MCP servers.

```bash
# Install FastMCP globally
pip install fastmcp

# Then install the Financial Reports MCP server
# From the project directory:
fastmcp install main.py --name "Financial Reports API"

# Or run in development mode
fastmcp dev main.py
```

### Option 3: Install with Python Script

We provide a helper script that handles the installation process:

```bash
# Run the installation script
python install.py
```

### Option 4: Docker

We provide Docker support for easy deployment across environments:

```bash
# Build and run with Docker Compose
docker-compose up

# Or build and run the Docker container directly
docker build -t financial-reports-mcp .
docker run -p 8000:8000 financial-reports-mcp
```

### Option 5: Install as Python Package

```bash
# Install directly from the directory
pip install .

# Or in development mode
pip install -e .
```

## Using an MCP Client

### Claude Desktop Configuration

Add the following configuration to Claude Desktop:

```json
{
  "mcpServers": {
    "financial-reports": {
      "command": "python",
      "args": ["-m", "financial-reports-mcp-server"]
    }
  }
}
```

### Using with uvx

If you have `uv` / `uvx` installed (recommended for cross-platform compatibility):

```json
{
  "mcpServers": {
    "financial-reports": {
      "command": "uvx",
      "args": ["financial-reports-mcp-server"]
    }
  }
}
```

### Using with Docker

```json
{
  "mcpServers": {
    "financial-reports": {
      "command": "docker",
      "args": ["run", "--rm", "-p", "8000:8000", "financial-reports-mcp"],
      "env": {
        "API_KEY": "your_api_key_here",
        "USE_MOCK_API": "True" 
      }
    }
  }
}
```

## Cross-Platform Compatibility

The server can be run on:

- **Linux**: All methods supported
- **macOS**: All methods supported 
- **Windows**: All methods supported, but using `uvx` is recommended for the most consistent experience

For Windows users specifically:
- Make sure to use the correct path notation in configurations (`\` vs `/`)
- If using PowerShell, you may need to adjust environment variable syntax
- Docker Desktop for Windows works well for containerized usage

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

- `main.py` - Main entry point
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

## Mock API Mode

The server can run in mock mode using predefined responses. This is useful for:
- Development and testing without API access
- Demonstrations and presentations
- Offline use

To use the real API, update the `.env` file with your API key and set `USE_MOCK_API=False`.

## Troubleshooting

### Common Issues

1. **"Module not found" errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
   
2. **Cannot connect to the MCP server**: Check if the server is running and accessible from the client

3. **Authentication errors with the API**: Verify your API key in the `.env` file

4. **Port already in use**: Change the port in the Docker configuration or when running the server

### Logs

When running directly, logs are output to the console. For Docker, you can view logs with:

```bash
docker logs <container-id>
```

## Development

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Development Setup

```bash
# Clone the repository
git clone <repo-url>
cd financial-reports-mcp

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dev dependencies
pip install -r requirements.txt
pip install -e .
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
