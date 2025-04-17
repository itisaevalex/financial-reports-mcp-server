"""
Financial Reports MCP Server
A Model Context Protocol (MCP) server for accessing financial reports, 
company information, and related data from the Financial Reports API.
"""

import os
import argparse
from dotenv import load_dotenv
from fastmcp import FastMCP, Context
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field

from src.api_client import APIClient

print("[DEBUG] MCP Server API_KEY at startup:", os.getenv("API_KEY"), "repr:", repr(os.getenv("API_KEY")))

class CompanySearchParams(BaseModel):
    """Parameters for searching companies (matches real API spec)."""
    search: Optional[str] = Field(None, description="Text to search for in company names, ISINs, or LEI")
    countries: Optional[Union[str, List[str]]] = Field(None, description="Filter by one or more country codes (ISO Alpha-2, comma-separated string or list)")
    sector: Optional[str] = Field(None, description="Optional filter by GICS sector code")
    industry_group: Optional[str] = Field(None, description="Optional filter by GICS industry group code")
    industry: Optional[str] = Field(None, description="Optional filter by GICS industry code")
    sub_industry: Optional[str] = Field(None, description="Optional filter by GICS sub-industry code")
    page: int = Field(1, description="Page number for pagination")
    page_size: int = Field(10, description="Number of results per page (max 100)")

class FilingSearchParams(BaseModel):
    """Parameters for searching filings (matches real API spec)."""
    company: Optional[int] = Field(None, description="Optional filter by company ID (real API: 'company')")
    company_isin: Optional[str] = Field(None, description="Optional filter by company ISIN")
    countries: Optional[Union[str, List[str]]] = Field(None, description="Filter by one or more country codes")
    type: Optional[str] = Field(None, description="Optional filter by filing type code (e.g., 'ANNREP') (real API: 'type')")
    language: Optional[str] = Field(None, description="Optional filter by language code (e.g., 'en', 'de')")
    page: int = Field(1, description="Page number for pagination")
    page_size: int = Field(10, description="Number of results per page (max 100)")

# Create an MCP server
mcp = FastMCP("Financial Reports API")

# Tools for Financial Reports API

@mcp.tool()
async def get_filing_type(filing_type_id: int) -> dict:
    """
    Get detailed information about a filing type by its ID.
    
    Args:
        filing_type_id (int): The ID of the filing type.
    Returns:
        dict: Filing type details.
    """
    api_client = await APIClient.create()
    return await api_client.get_filing_type(filing_type_id)

@mcp.tool()
async def list_industries(industry_group: int = None, page: int = 1, page_size: int = 100, search: str = None) -> list:
    """
    List all available GICS industries, optionally filtered by industry group.
    
    Args:
        industry_group (int, optional): Filter by industry group ID.
        page (int, optional): Page number for pagination.
        page_size (int, optional): Number of results per page.
        search (str, optional): Search text.
    Returns:
        list: List of industry dicts.
    """
    api_client = await APIClient.create()
    result = await api_client.get_industries(industry_group=industry_group, page=page, page_size=page_size, search=search)
    return result.get("results", [])

@mcp.tool()
async def get_industry(industry_id: int) -> dict:
    """
    Get detailed information about a GICS industry by its ID.
    
    Args:
        industry_id (int): The industry ID.
    Returns:
        dict: Industry details.
    """
    api_client = await APIClient.create()
    return await api_client.get_industry(industry_id)

@mcp.tool()
async def list_industry_groups(sector: int = None, page: int = 1, page_size: int = 100, search: str = None) -> list:
    """
    List all available GICS industry groups, optionally filtered by sector.
    
    Args:
        sector (int, optional): Filter by sector ID.
        page (int, optional): Page number for pagination.
        page_size (int, optional): Number of results per page.
        search (str, optional): Search text.
    Returns:
        list: List of industry group dicts.
    """
    api_client = await APIClient.create()
    result = await api_client.get_industry_groups(sector=sector, page=page, page_size=page_size, search=search)
    return result.get("results", [])

@mcp.tool()
async def get_industry_group(group_id: int) -> dict:
    """
    Get detailed information about a GICS industry group by its ID.
    
    Args:
        group_id (int): The industry group ID.
    Returns:
        dict: Industry group details.
    """
    api_client = await APIClient.create()
    return await api_client.get_industry_group(group_id)

@mcp.tool()
async def get_sector(sector_id: int) -> dict:
    """
    Get detailed information about a GICS sector by its ID.
    
    Args:
        sector_id (int): The sector ID.
    Returns:
        dict: Sector details.
    """
    api_client = await APIClient.create()
    return await api_client.get_sector(sector_id)

@mcp.tool()
async def list_sub_industries(industry: int = None, page: int = 1, page_size: int = 100, search: str = None) -> list:
    """
    List all available GICS sub-industries, optionally filtered by industry.
    
    Args:
        industry (int, optional): Filter by industry ID.
        page (int, optional): Page number for pagination.
        page_size (int, optional): Number of results per page.
        search (str, optional): Search text.
    Returns:
        list: List of sub-industry dicts.
    """
    api_client = await APIClient.create()
    result = await api_client.get_sub_industries(industry=industry, page=page, page_size=page_size, search=search)
    return result.get("results", [])

@mcp.tool()
async def get_sub_industry(sub_industry_id: int) -> dict:
    """
    Get detailed information about a GICS sub-industry by its ID.
    
    Args:
        sub_industry_id (int): The sub-industry ID.
    Returns:
        dict: Sub-industry details.
    """
    api_client = await APIClient.create()
    return await api_client.get_sub_industry(sub_industry_id)

@mcp.tool()
async def list_sources(page: int = 1, page_size: int = 100) -> list:
    """
    List all available data sources.
    
    Args:
        page (int, optional): Page number for pagination.
        page_size (int, optional): Number of results per page.
    Returns:
        list: List of data source dicts.
    """
    api_client = await APIClient.create()
    result = await api_client.get_sources(page=page, page_size=page_size)
    return result.get("results", [])

@mcp.tool()
async def get_source(source_id: int) -> dict:
    """
    Get detailed information about a data source by its ID.
    
    Args:
        source_id (int): The source ID.
    Returns:
        dict: Source details.
    """
    api_client = await APIClient.create()
    return await api_client.get_source(source_id)

@mcp.tool()
async def get_processed_filing(processed_filing_id: int) -> dict:
    """
    Get processed content for a filing by its ProcessedFiling ID.
    
    Args:
        processed_filing_id (int): The processed filing ID.
    Returns:
        dict: Processed filing content.
    """
    api_client = await APIClient.create()
    return await api_client.get_processed_filing(processed_filing_id)

@mcp.tool()
async def get_schema(format: str = None, lang: str = None) -> dict:
    """
    Get the OpenAPI3 schema for the Financial Reports API.
    
    Args:
        format (str, optional): Format of the schema (e.g. 'json').
        lang (str, optional): Language of the schema.
    Returns:
        dict: OpenAPI3 schema.
    """
    api_client = await APIClient.create()
    return await api_client.get_schema(format=format, lang=lang)

@mcp.tool()
async def search_companies(params: CompanySearchParams) -> List[Dict[str, Any]]:
    """
    Search for companies by name, ISIN, or LEI, with advanced filtering.
    
    Args:
        params (CompanySearchParams): Search parameters (search, countries, sector, industry_group, industry, sub_industry, page, page_size)
    Returns:
        List[Dict[str, Any]]: List of matching companies.
    """
    api_client = await APIClient.create()
    result = await api_client.get_companies(
        search=params.search,
        countries=params.countries,
        sector=params.sector,
        industry_group=params.industry_group,
        industry=params.industry,
        sub_industry=params.sub_industry,
        page=params.page,
        page_size=params.page_size
    )
    return result.get("results", [])


@mcp.tool()
async def get_company_detail(company_id: int) -> Dict[str, Any]:
    """
    Get detailed information about a company by its unique numeric ID.
    
    Args:
        company_id (int): The integer ID of the company to retrieve.
    Returns:
        Dict[str, Any]: Company details (fields include name, sector, country_code, etc).
    """
    api_client = await APIClient.create()
    return await api_client.get_company_detail(company_id)


@mcp.tool()
async def get_latest_filings(params: FilingSearchParams) -> List[Dict[str, Any]]:
    """
    Get the latest financial filings, optionally filtered by company, ISIN, type, language, etc.
    
    Args:
        params (FilingSearchParams): Search parameters (company, company_isin, countries, type, language, page, page_size)
    Returns:
        List[Dict[str, Any]]: List of filings.
    """
    api_client = await APIClient.create()
    result = await api_client.get_filings(
        company=params.company,
        company_isin=params.company_isin,
        countries=params.countries,
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
        filing_id (int): The unique identifier for the filing.
    Returns:
        Dict[str, Any]: Detailed filing information.
    """
    api_client = await APIClient.create()
    return await api_client.get_filing_detail(filing_id)

@mcp.tool()
async def list_sectors() -> List[Dict[str, Any]]:
    """
    List all available GICS sectors.
    
    Args:
        None
    Returns:
        List[Dict[str, Any]]: List of sectors.
    """
    api_client = await APIClient.create()
    result = await api_client.get_sectors()
    return result.get("results", [])

@mcp.tool()
async def list_filing_types() -> List[Dict[str, Any]]:
    """
    List all available filing types.
    
    Args:
        None
    Returns:
        List[Dict[str, Any]]: List of filing types.
    """
    api_client = await APIClient.create()
    result = await api_client.get_filing_types()
    return result.get("results", [])

# Resources for common queries

@mcp.resource("financial-reports://sectors")
async def get_sectors_resource() -> str:
    """
    Retrieve a list of all GICS sectors as formatted Markdown text.
    
    Args:
        None
    Returns:
        str: Markdown-formatted list of GICS sectors.
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
    Retrieve a list of all filing types as formatted Markdown text.
    
    Args:
        None
    Returns:
        str: Markdown-formatted list of filing types.
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
    Retrieve a formatted company profile for a given company ID as Markdown text.
    
    Args:
        company (int): The unique company ID.
    Returns:
        str: Markdown-formatted company profile.
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
    Retrieve a list of the company's most recent filings as Markdown text.
    
    Args:
        company (int): The unique ID of the company.
        limit (int): Maximum number of filings to return.
    Returns:
        str: Markdown-formatted list of recent filings.
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
    Retrieve a list of the company's 5 most recent filings as Markdown text.
    
    Args:
        company (int): The unique ID of the company.
    Returns:
        str: Markdown-formatted list of 5 recent filings.
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

