"""
Simplified entry point for the Financial Reports MCP server.
This file provides a simplified, single-file entry point for running the 
Financial Reports MCP server with uv or directly with Python.
"""

import os
import httpx
import logging
import sys
import json
from fastmcp import FastMCP
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("financial-reports-mcp")

# Create an MCP server
mcp = FastMCP("Financial Reports API")

# API client configuration
API_KEY = os.getenv("API_KEY", "your_api_key_here")
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.financialreports.eu/")
USE_MOCK_API = os.getenv("USE_MOCK_API", "True").lower() == "true"

class CompanySearchParams(BaseModel):
    """Parameters for searching companies."""
    search_term: str = Field(..., description="Text to search for in company names or descriptions")
    country: Optional[str] = Field(None, description="Optional filter by country code (ISO Alpha-2, e.g., 'US', 'GB', 'DE')")
    sector: Optional[str] = Field(None, description="Optional filter by GICS sector code")
    industry: Optional[str] = Field(None, description="Optional filter by GICS industry code")
    page: int = Field(1, description="Page number for pagination")
    page_size: int = Field(10, description="Number of results per page (max 100)")

class FilingSearchParams(BaseModel):
    """Parameters for searching filings."""
    company_id: Optional[int] = Field(None, description="Optional filter by company ID")
    filing_type: Optional[str] = Field(None, description="Optional filter by filing type code (e.g., 'ANNREP')")
    language: Optional[str] = Field(None, description="Optional filter by language code (e.g., 'en', 'de')")
    page: int = Field(1, description="Page number for pagination")
    page_size: int = Field(10, description="Number of results per page (max 100)")

# API client class
class APIClient:
    """API client for Financial Reports API."""
    
    @staticmethod
    async def create():
        """Create and return either a mock or real API client based on configuration."""
        if USE_MOCK_API:
            return MockAPIClient(API_KEY, API_BASE_URL)
        else:
            # In a real implementation, we would create a real API client
            # For now, just return the mock client
            return MockAPIClient(API_KEY, API_BASE_URL)

# Mock API client class (simplified)
class MockAPIClient:
    """Mock API client that returns predefined responses."""
    
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self._mock_data = {
            "companies": [
                {"id": 1, "name": "Deutsche Bank", "country": "DE", "isin": "DE0005140008", 
                 "sector": {"name": "Financials", "code": "40"}, "industry": {"name": "Banking", "code": "4010"}},
                {"id": 2, "name": "Apple Inc.", "country": "US", "isin": "US0378331005", 
                 "sector": {"name": "Technology", "code": "45"}, "industry": {"name": "Consumer Electronics", "code": "4520"}},
            ],
            "company_detail": {
                "id": 1, "name": "Deutsche Bank", "country": "DE", "isin": "DE0005140008", 
                "lei": "7LTWFZYICNSX8D621K86", "description": "Deutsche Bank AG is a German multinational investment bank and financial services company.",
                "sector": {"name": "Financials", "code": "40"}, 
                "industry_group": {"name": "Banks", "code": "4010"},
                "industry": {"name": "Banking", "code": "401010"},
                "sub_industry": {"name": "Diversified Banks", "code": "40101010"},
                "website": "https://www.db.com",
                "stock_exchange": "XETRA",
                "market_cap_eur_millions": 25000,
                "employees": 87000
            },
            "filings": [
                {"id": 1001, "company": {"id": 1, "name": "Deutsche Bank"}, "title": "Annual Report 2024", 
                 "filing_type": {"name": "Annual Report", "code": "ANNREP"}, "release_datetime": "2025-03-15T09:00:00Z",
                 "language": {"name": "English", "code": "en"}},
                {"id": 1002, "company": {"id": 1, "name": "Deutsche Bank"}, "title": "Q1 2025 Report", 
                 "filing_type": {"name": "Quarterly Report", "code": "QTRREP"}, "release_datetime": "2025-04-01T09:00:00Z",
                 "language": {"name": "English", "code": "en"}}
            ],
            "filing_detail": {
                "id": 1001, "company": {"id": 1, "name": "Deutsche Bank"}, "title": "Annual Report 2024",
                "filing_type": {"name": "Annual Report", "code": "ANNREP"}, "release_datetime": "2025-03-15T09:00:00Z",
                "language": {"name": "English", "code": "en"},
                "url": "https://www.db.com/ir/en/annual-reports.htm",
                "content_summary": "Annual Report for the financial year 2024 with detailed financial statements and business overview."
            },
            "sectors": [
                {"id": 10, "name": "Energy", "code": "10", "description": "The Energy Sector comprises companies engaged in exploration, production, refining, marketing, storage and transportation of energy sources."},
                {"id": 40, "name": "Financials", "code": "40", "description": "The Financials Sector contains companies involved in banking, mortgage finance, consumer finance, specialized finance, investment banking and brokerage, asset management and custody, corporate lending, insurance, and financial investment."}
            ],
            "filing_types": [
                {"id": 1, "name": "Annual Report", "code": "ANNREP", "description": "A comprehensive report on a company's activities throughout the preceding year."},
                {"id": 2, "name": "Quarterly Report", "code": "QTRREP", "description": "A report filed quarterly by public companies to provide financial updates."}
            ]
        }
    
    async def get_companies(self, search=None, country=None, sector=None, industry=None, page=1, page_size=10):
        """Get a list of companies."""
        data = {"results": self._mock_data["companies"], "count": len(self._mock_data["companies"])}
        
        # Filter by search term
        if search:
            search = search.lower()
            data["results"] = [c for c in data["results"] if search in c["name"].lower()]
            
        # Filter by country
        if country:
            data["results"] = [c for c in data["results"] if c["country"] == country]
            
        # Filter by sector
        if sector:
            data["results"] = [c for c in data["results"] if c["sector"]["code"] == sector]
            
        # Filter by industry
        if industry:
            data["results"] = [c for c in data["results"] if c["industry"]["code"] == industry]
            
        # Update count after filtering
        data["count"] = len(data["results"])
        
        # Pagination
        start = (page - 1) * page_size
        end = start + page_size
        data["results"] = data["results"][start:end]
        
        return data
        
    async def get_company_detail(self, company_id):
        """Get detailed information about a company."""
        return self._mock_data["company_detail"] if company_id == 1 else {"error": "Company not found"}
    
    async def get_filings(self, company_id=None, filing_type=None, language=None, page=1, page_size=10):
        """Get a list of filings."""
        data = {"results": self._mock_data["filings"], "count": len(self._mock_data["filings"])}
        
        # Filter by company
        if company_id:
            data["results"] = [f for f in data["results"] if f["company"]["id"] == company_id]
            
        # Filter by filing type
        if filing_type:
            data["results"] = [f for f in data["results"] if f["filing_type"]["code"] == filing_type]
            
        # Filter by language
        if language:
            data["results"] = [f for f in data["results"] if f["language"]["code"] == language]
            
        # Update count after filtering
        data["count"] = len(data["results"])
        
        # Pagination
        start = (page - 1) * page_size
        end = start + page_size
        data["results"] = data["results"][start:end]
        
        return data
    
    async def get_filing_detail(self, filing_id):
        """Get detailed information about a filing."""
        return self._mock_data["filing_detail"] if filing_id == 1001 else {"error": "Filing not found"}
    
    async def get_sectors(self):
        """Get a list of all sectors."""
        return {"results": self._mock_data["sectors"], "count": len(self._mock_data["sectors"])}
    
    async def get_filing_types(self):
        """Get a list of all filing types."""
        return {"results": self._mock_data["filing_types"], "count": len(self._mock_data["filing_types"])}

# MCP tools

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
async def get_company_detail(company_id: int) -> Dict[str, Any]:
    """
    Get detailed information about a specific company.
    
    Args:
        company_id: The unique identifier for the company
    
    Returns:
        Detailed company information
    """
    api_client = await APIClient.create()
    return await api_client.get_company_detail(company_id)

@mcp.tool()
async def get_latest_filings(params: FilingSearchParams) -> List[Dict[str, Any]]:
    """
    Get the latest financial filings, optionally filtered by company or type.
    
    Args:
        params: Search parameters including company_id, filing_type, language, page, and page_size
    
    Returns:
        List of filings
    """
    api_client = await APIClient.create()
    
    result = await api_client.get_filings(
        company_id=params.company_id,
        filing_type=params.filing_type,
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

# Main execution
if __name__ == "__main__":
    # Log server startup
    logger.info("Starting Financial Reports MCP Server...")
    print(f"Starting Financial Reports MCP Server using stdio transport")
    print(f"Mock API mode: {USE_MOCK_API}")
    
    # Run the server with stdio transport
    mcp.run(transport="stdio")
