from fastmcp import FastMCP, Context
import httpx
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

# Models for Financial Reports
class Company(BaseModel):
    id: int
    name: str
    country: Optional[str] = None
    isin: Optional[str] = None
    lei: Optional[str] = None
    description: Optional[str] = None
    
class Filing(BaseModel):
    id: int
    title: str
    company_id: int
    company_name: str
    release_datetime: str
    filing_type: Optional[str] = None
    language: Optional[str] = None

class Sector(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str] = None

# Create an MCP server
mcp = FastMCP("Financial Reports API")

# API key - will need to be provided correctly when authenticated
API_KEY = "l3t11KuDIhaduGo5saxrVaxRsAT9yV2C2Qjg1Hi7"
BASE_URL = "https://api.financialreports.eu"

# Headers for authentication
headers = {
    "X-API-Key": API_KEY
}

# Helper function for making API requests
async def make_api_request(endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Make a request to the Financial Reports API."""
    url = f"{BASE_URL}/{endpoint}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise error for bad responses
        return response.json()

# Tools for Financial Reports API

@mcp.tool()
async def search_companies(search_term: str, country: Optional[str] = None, page: int = 1, page_size: int = 10) -> List[Dict[str, Any]]:
    """
    Search for companies by name or other identifying information.
    
    Args:
        search_term: Text to search for in company names or descriptions
        country: Optional filter by country code (ISO Alpha-2, e.g., 'US', 'GB', 'DE')
        page: Page number for pagination
        page_size: Number of results per page (max 100)
    
    Returns:
        List of matching companies
    """
    try:
        params = {
            "search": search_term,
            "page": page,
            "page_size": page_size
        }
        if country:
            params["countries"] = country
            
        data = await make_api_request("companies/", params)
        return data.get("results", [])
    except httpx.HTTPStatusError as e:
        return [{"error": f"API error: {str(e)}", "status_code": e.response.status_code}]
    except Exception as e:
        return [{"error": f"Error: {str(e)}"}]

@mcp.tool()
async def get_company_detail(company_id: int) -> Dict[str, Any]:
    """
    Get detailed information about a specific company.
    
    Args:
        company_id: The unique identifier for the company
    
    Returns:
        Detailed company information
    """
    try:
        data = await make_api_request(f"companies/{company_id}/")
        return data
    except httpx.HTTPStatusError as e:
        return {"error": f"API error: {str(e)}", "status_code": e.response.status_code}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}

@mcp.tool()
async def get_latest_filings(
    company_id: Optional[int] = None, 
    country: Optional[str] = None,
    filing_type: Optional[str] = None,
    page: int = 1, 
    page_size: int = 10
) -> List[Dict[str, Any]]:
    """
    Get the latest financial filings, optionally filtered by company or type.
    
    Args:
        company_id: Optional filter by company ID
        country: Optional filter by country code (ISO Alpha-2, e.g., 'US', 'GB', 'DE')
        filing_type: Optional filter by filing type code (e.g., 'ANNREP' for annual reports)
        page: Page number for pagination
        page_size: Number of results per page (max 100)
    
    Returns:
        List of filings
    """
    try:
        params = {
            "page": page,
            "page_size": page_size,
            "ordering": "-release_datetime"  # Most recent first
        }
        
        if company_id:
            params["company"] = company_id
        
        if country:
            params["countries"] = country
            
        if filing_type:
            params["type"] = filing_type
            
        data = await make_api_request("filings/", params)
        return data.get("results", [])
    except httpx.HTTPStatusError as e:
        return [{"error": f"API error: {str(e)}", "status_code": e.response.status_code}]
    except Exception as e:
        return [{"error": f"Error: {str(e)}"}]

@mcp.tool()
async def get_filing_detail(filing_id: int) -> Dict[str, Any]:
    """
    Get detailed information about a specific filing.
    
    Args:
        filing_id: The unique identifier for the filing
    
    Returns:
        Detailed filing information
    """
    try:
        data = await make_api_request(f"filings/{filing_id}/")
        return data
    except httpx.HTTPStatusError as e:
        return {"error": f"API error: {str(e)}", "status_code": e.response.status_code}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}

@mcp.tool()
async def list_sectors() -> List[Dict[str, Any]]:
    """
    List all available GICS sectors.
    
    Returns:
        List of sectors
    """
    try:
        data = await make_api_request("sectors/")
        return data.get("results", [])
    except httpx.HTTPStatusError as e:
        return [{"error": f"API error: {str(e)}", "status_code": e.response.status_code}]
    except Exception as e:
        return [{"error": f"Error: {str(e)}"}]

@mcp.tool()
async def list_filing_types() -> List[Dict[str, Any]]:
    """
    List all available filing types.
    
    Returns:
        List of filing types
    """
    try:
        data = await make_api_request("filing-types/")
        return data.get("results", [])
    except httpx.HTTPStatusError as e:
        return [{"error": f"API error: {str(e)}", "status_code": e.response.status_code}]
    except Exception as e:
        return [{"error": f"Error: {str(e)}"}]

# Resources for common queries

@mcp.resource("financial-reports://sectors")
async def get_sectors_resource() -> str:
    """
    Retrieve a list of all GICS sectors.
    """
    try:
        data = await make_api_request("sectors/")
        sectors = data.get("results", [])
        
        result = "# Global Industry Classification Standard (GICS) Sectors\n\n"
        for sector in sectors:
            result += f"- **{sector.get('name')}** (Code: {sector.get('code')})\n"
            if sector.get('description'):
                result += f"  {sector.get('description')}\n"
                
        return result
    except Exception as e:
        return f"Error retrieving sectors: {str(e)}"

@mcp.resource("financial-reports://filing-types")
async def get_filing_types_resource() -> str:
    """
    Retrieve a list of all filing types.
    """
    try:
        data = await make_api_request("filing-types/")
        types = data.get("results", [])
        
        result = "# Financial Filing Types\n\n"
        for filing_type in types:
            result += f"- **{filing_type.get('name')}** (Code: {filing_type.get('code')})\n"
            if filing_type.get('description'):
                result += f"  {filing_type.get('description')}\n"
                
        return result
    except Exception as e:
        return f"Error retrieving filing types: {str(e)}"

@mcp.resource("financial-reports://companies/{company_id}/profile")
async def get_company_profile(company_id: int) -> str:
    """
    Retrieve a formatted company profile.
    """
    try:
        data = await make_api_request(f"companies/{company_id}/")
        
        result = f"# {data.get('name', 'Company')} Profile\n\n"
        result += f"**ISIN:** {data.get('isin', 'N/A')}\n"
        result += f"**LEI:** {data.get('lei', 'N/A')}\n"
        result += f"**Country:** {data.get('country', 'N/A')}\n"
        
        if data.get('sector'):
            result += f"**Sector:** {data.get('sector', {}).get('name', 'N/A')}\n"
            
        if data.get('industry'):
            result += f"**Industry:** {data.get('industry', {}).get('name', 'N/A')}\n"
            
        if data.get('description'):
            result += f"\n## Description\n\n{data.get('description')}\n"
            
        return result
    except Exception as e:
        return f"Error retrieving company profile: {str(e)}"

@mcp.resource("financial-reports://companies/{company_id}/recent-filings")
async def get_company_recent_filings(company_id: int, limit: int = 5) -> str:
    """
    Retrieve a list of the company's most recent filings.
    """
    try:
        params = {
            "company": company_id,
            "ordering": "-release_datetime",
            "page_size": limit
        }
        
        data = await make_api_request("filings/", params)
        filings = data.get("results", [])
        
        # Get company name
        company_data = await make_api_request(f"companies/{company_id}/")
        company_name = company_data.get("name", "Company")
        
        result = f"# Recent Filings for {company_name}\n\n"
        
        if not filings:
            return result + "No recent filings found."
            
        for filing in filings:
            release_date = filing.get("release_datetime", "").split("T")[0]  # Just the date part
            result += f"- **{filing.get('title')}** ({release_date})\n"
            result += f"  Type: {filing.get('filing_type', {}).get('name', 'N/A')}\n"
            if filing.get("language"):
                result += f"  Language: {filing.get('language', {}).get('name', 'N/A')}\n"
            result += "\n"
                
        return result
    except Exception as e:
        return f"Error retrieving recent filings: {str(e)}"

# Main execution
if __name__ == "__main__":
    mcp.run()
