"""
Financial Reports MCP Server
A Model Context Protocol (MCP) server for accessing financial reports, 
company information, and related data from the Financial Reports API.
"""

import os
import argparse
from dotenv import load_dotenv
from fastmcp import FastMCP, Context
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from src.api_client import APIClient

class CompanySearchParams(BaseModel):
    """Parameters for searching companies."""
    search_term: str = Field(..., description="Text to search for in company names or descriptions")
    country: Optional[str] = Field(None, description="Optional filter by country code (ISO Alpha-2, e.g., 'US', 'GB', 'DE')")
    sector: Optional[str] = Field(None, description="Optional filter by GICS sector code")
    industry: Optional[str] = Field(None, description="Optional filter by GICS industry code")
    page: int = Field(1, description="Page number for pagination")
    page_size: int = Field(10, description="Number of results per page (max 100)")

class FilingSearchParams(BaseModel):
    """Parameters for searching filings (matches real API spec)."""
    company: Optional[int] = Field(None, description="Optional filter by company ID (real API: 'company')")
    type: Optional[str] = Field(None, description="Optional filter by filing type code (e.g., 'ANNREP') (real API: 'type')")
    language: Optional[str] = Field(None, description="Optional filter by language code (e.g., 'en', 'de')")
    page: int = Field(1, description="Page number for pagination")
    page_size: int = Field(10, description="Number of results per page (max 100)")

# Create an MCP server
mcp = FastMCP("Financial Reports API")

# Tools for Financial Reports API

@mcp.tool()
async def search_companies(params: CompanySearchParams) -> List[Dict[str, Any]]:
    """
    Search for companies by name or other identifying information.
    
    Args:
        params: Search parameters including search_term, country, sector, industry, page, and page_size
    
    Returns:
        List of matching companies
    """
    api_client = await APIClient.create()
    
    result = await api_client.get_companies(
        search=params.search_term,
        country=params.country,
        sector=params.sector,
        industry=params.industry,
        page=params.page,
        page_size=params.page_size
    )
    
    return result.get("results", [])

@mcp.tool()
async def get_company_detail(company: int) -> Dict[str, Any]:
    """
    Get detailed information about a specific company (real API: 'company').
    
    Args:
        company: The unique identifier for the company
    
    Returns:
        Detailed company information
    """
    api_client = await APIClient.create()
    return await api_client.get_company_detail(company)

@mcp.tool()
async def get_latest_filings(params: FilingSearchParams) -> List[Dict[str, Any]]:
    """
    Get the latest financial filings, optionally filtered by company or type (real API spec).
    
    Args:
        params: Search parameters including company, type, language, page, and page_size
    
    Returns:
        List of filings
    """
    api_client = await APIClient.create()
    
    result = await api_client.get_filings(
        company=params.company,
        type=params.type,
        language=params.language,
        page=params.page,
        page_size=params.page_size
    )
    
    return result.get("results", [])

@mcp.tool()
async def get_filing_detail(filing_id: int) -> Dict[str, Any]:
    """
    Get detailed information about a specific filing.
    
    Args:
        filing_id: The unique identifier for the filing
    
    Returns:
        Detailed filing information
    """
    api_client = await APIClient.create()
    return await api_client.get_filing_detail(filing_id)

@mcp.tool()
async def list_sectors() -> List[Dict[str, Any]]:
    """
    List all available GICS sectors.
    
    Returns:
        List of sectors
    """
    api_client = await APIClient.create()
    result = await api_client.get_sectors()
    return result.get("results", [])

@mcp.tool()
async def list_filing_types() -> List[Dict[str, Any]]:
    """
    List all available filing types.
    
    Returns:
        List of filing types
    """
    api_client = await APIClient.create()
    result = await api_client.get_filing_types()
    return result.get("results", [])

# Resources for common queries

@mcp.resource("financial-reports://sectors")
async def get_sectors_resource() -> str:
    """
    Retrieve a list of all GICS sectors.
    """
    api_client = await APIClient.create()
    result = await api_client.get_sectors()
    sectors = result.get("results", [])
    
    output = "# Global Industry Classification Standard (GICS) Sectors\n\n"
    for sector in sectors:
        output += f"- **{sector.get('name')}** (Code: {sector.get('code')})\n"
        if sector.get('description'):
            output += f"  {sector.get('description')}\n"
            
    return output

@mcp.resource("financial-reports://filing-types")
async def get_filing_types_resource() -> str:
    """
    Retrieve a list of all filing types.
    """
    api_client = await APIClient.create()
    result = await api_client.get_filing_types()
    types = result.get("results", [])
    
    output = "# Financial Filing Types\n\n"
    for filing_type in types:
        output += f"- **{filing_type.get('name')}** (Code: {filing_type.get('code')})\n"
        if filing_type.get('description'):
            output += f"  {filing_type.get('description')}\n"
            
    return output

@mcp.resource("financial-reports://companies/{company}/profile")
async def get_company_profile(company: int) -> str:
    """
    Retrieve a formatted company profile (real API: 'company').
    """
    api_client = await APIClient.create()
    data = await api_client.get_company_detail(company)
    
    output = f"# {data.get('name', 'Company')} Profile\n\n"
    output += f"**ISIN:** {data.get('isin', 'N/A')}\n"
    output += f"**LEI:** {data.get('lei', 'N/A')}\n"
    output += f"**Country:** {data.get('country', 'N/A')}\n"
    
    if data.get('sector'):
        output += f"**Sector:** {data.get('sector', {}).get('name', 'N/A')}\n"
        
    if data.get('industry'):
        output += f"**Industry:** {data.get('industry', {}).get('name', 'N/A')}\n"
        
    if data.get('description'):
        output += f"\n## Description\n\n{data.get('description')}\n"
        
    # Add additional details if available
    if data.get('website'):
        output += f"\n**Website:** {data.get('website')}\n"
        
    if data.get('stock_exchange'):
        output += f"**Exchange:** {data.get('stock_exchange')}\n"
        
    if data.get('market_cap_eur_millions'):
        output += f"**Market Cap (EUR millions):** {data.get('market_cap_eur_millions')}\n"
        
    if data.get('employees'):
        output += f"**Employees:** {data.get('employees')}\n"
        
    return output

@mcp.resource("financial-reports://companies/{company}/recent-filings/{limit}")
async def get_company_recent_filings(company: int, limit: int) -> str:
    """
    Retrieve a list of the company's most recent filings.
    
    Args:
        company: The unique ID of the company
        limit: Maximum number of filings to return
    """
    api_client = await APIClient.create()
    
    # Get company info to display name
    company_data = await api_client.get_company_detail(company)
    company_name = company_data.get("name", "Company")
    
    # Get filings
    result = await api_client.get_filings(company=company, page_size=limit)
    filings = result.get("results", [])
    
    output = f"# Recent Filings for {company_name}\n\n"
    
    if not filings:
        return output + "No recent filings found."
        
    for filing in filings:
        release_date = filing.get("release_datetime", "").split("T")[0]  # Just the date part
        output += f"- **{filing.get('title')}** ({release_date})\n"
        output += f"  Type: {filing.get('filing_type', {}).get('name', 'N/A')}\n"
        if filing.get("language"):
            output += f"  Language: {filing.get('language', {}).get('name', 'N/A')}\n"
        output += "\n"
            
    return output

# Add a simpler version that uses a default limit
@mcp.resource("financial-reports://companies/{company}/recent-filings")
async def get_company_recent_filings_default(company: int) -> str:
    """
    Retrieve a list of the company's 5 most recent filings (real API: 'company').
    
    Args:
        company: The unique ID of the company
    """
    # Call the other resource with default limit of 5
    return await get_company_recent_filings(company, 5)

# Prompts for common tasks

@mcp.prompt()
def search_company_by_name() -> str:
    """Prompt for searching a company by name."""
    return """
I want to search for information about a specific company. Please help me find:
1. Basic company details like country, sector and industry
2. Recent financial filings
3. Key financial metrics if available

Please use the search_companies tool to find the company first, 
then use get_company_detail to get detailed information about it,
and finally get_latest_filings to retrieve their recent filings.
"""

@mcp.prompt()
def find_latest_annual_reports() -> str:
    """Prompt for finding the latest annual reports."""
    return """
I'd like to see the latest annual reports from major European banks. 
Please help me:
1. Find companies in the banking sector
2. Get their latest annual reports
3. Summarize key financial metrics from these reports if available

First, you'll need to list_sectors to find the correct sector code for financials,
then search for banking companies using search_companies,
and finally use get_latest_filings with filing_type="ANNREP" to find annual reports.
"""

def run_cli():
    """
    Command-line entry point for the Financial Reports MCP server.
    This function is used as the entry point in setup.py.
    """
    # Load environment variables
    load_dotenv()
    
    # Parse arguments
    parser = argparse.ArgumentParser(description="Financial Reports MCP Server")
    parser.add_argument(
        "--host", 
        default=os.getenv("MCP_HOST", "127.0.0.1"),
        help="Host address to bind the server to (default: 127.0.0.1 or MCP_HOST env var)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=int(os.getenv("MCP_PORT", "8000")),
        help="Port to run the server on (default: 8000 or MCP_PORT env var)"
    )
    args = parser.parse_args()
    
    # Print startup information
    print(f"Starting Financial Reports MCP Server on {args.host}:{args.port}")
    print(f"Mock API mode: {os.getenv('USE_MOCK_API', 'True')}")
    
    # Set environment variables for FastMCP (it uses these internally)
    os.environ["MCP_HOST"] = args.host
    os.environ["MCP_PORT"] = str(args.port)
    
    # Run the server
    mcp.run()

# Main execution - this allows running the server directly
if __name__ == "__main__":
    run_cli()
