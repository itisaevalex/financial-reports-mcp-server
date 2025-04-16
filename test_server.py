"""
Test script for the Financial Reports MCP server.
"""

import asyncio
import json
from fastmcp import Client
from pydantic import BaseModel

# Define the same models as in the MCP server for testing
class CompanySearchParams(BaseModel):
    search_term: str
    country: str = None
    sector: str = None
    industry: str = None
    page: int = 1
    page_size: int = 10

class FilingSearchParams(BaseModel):
    company_id: int = None
    filing_type: str = None
    language: str = None
    page: int = 1
    page_size: int = 10

async def test_mcp_server_direct():
    """Test the Financial Reports MCP server directly."""
    print("Testing Financial Reports MCP Server using direct import...")
    
    # Import the server directly
    from src.financial_reports_mcp import mcp
    
    # Create a simple transport directly to the MCP object
    from fastmcp.client.transports import FastMCPTransport
    
    # Connect to the server directly
    async with Client(FastMCPTransport(mcp)) as client:
        print("\n=== Testing Tools ===")
        
        # Test list_sectors
        print("\nTesting list_sectors...")
        try:
            result = await client.call_tool("list_sectors")
            print(f"Success! Got sectors list")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test list_filing_types
        print("\nTesting list_filing_types...")
        try:
            result = await client.call_tool("list_filing_types")
            print(f"Success! Got filing types list")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test search_companies
        print("\nTesting search_companies...")
        try:
            search_params = CompanySearchParams(search_term="bank")
            result = await client.call_tool("search_companies", {"params": search_params.model_dump()})
            print(f"Success! Found companies matching 'bank'")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test get_company_detail
        print("\nTesting get_company_detail...")
        try:
            result = await client.call_tool("get_company_detail", {"company_id": 1})
            print(f"Success! Got company details")
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n=== Testing Resources ===")
        
        # Test sectors resource
        print("\nTesting financial-reports://sectors resource...")
        try:
            result = await client.read_resource("financial-reports://sectors")
            print(f"Success! Got sectors resource")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test company profile resource
        print("\nTesting financial-reports://companies/1/profile resource...")
        try:
            result = await client.read_resource("financial-reports://companies/1/profile")
            print(f"Success! Got company profile resource")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test company recent filings resource
        print("\nTesting financial-reports://companies/1/recent-filings resource...")
        try:
            result = await client.read_resource("financial-reports://companies/1/recent-filings")
            print(f"Success! Got company recent filings resource")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_mcp_server_direct())
