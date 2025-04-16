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
- Financial Reports API key (contact support@financialreports.eu for access)

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd financial-reports-mcp

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Edit the `financial_reports_mcp.py` file to update your API key:

```python
# API key - will need to be provided correctly when authenticated
API_KEY = "your-api-key-here"
```

## Usage

### Running the server directly

```bash
python financial_reports_mcp.py
```

### Using with Claude Desktop

Install the server in Claude Desktop:

```bash
fastmcp install financial_reports_mcp.py
```

### Development mode

For testing and development:

```bash
fastmcp dev financial_reports_mcp.py
```

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

## Troubleshooting

If you encounter "Forbidden" errors, check that your API key is valid and correctly configured in the server.

## Future Work

- Add caching for frequently accessed data
- Implement additional filtering options
- Add support for downloading filing documents
- Create additional specialized resources for industry data

## License

This project is licensed under the MIT License - see the LICENSE file for details.
