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

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd financial-reports-mcp

# Install dependencies
pip install -r requirements.txt
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

## Usage

### Running the server directly

```bash
python main.py
```

### Using with Claude Desktop

Install the server in Claude Desktop:

```bash
fastmcp install main.py
```

### Development mode

For testing and development:

```bash
fastmcp dev main.py
```

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

## Mock API Mode

The server can run in mock mode using predefined responses. This is useful for:
- Development and testing without API access
- Demonstrations and presentations
- Offline use

To use the real API, update the `.env` file with your API key and set `USE_MOCK_API=False`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
