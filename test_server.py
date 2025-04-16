"""
Test script for the Financial Reports MCP server.
"""

import asyncio
from fastmcp import Client
from pydantic import BaseModel

# Define the same model as in the MCP server for testing
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

async def test_mcp_server():
    """Test the Financial Reports MCP server."""
    print("Testing Financial Reports MCP Server...")
    
    # Connect to the server
    async with Client("main.py:mcp") as client:
        print("\n=== Testing Tools ===")
        
        # Test list_sectors
        print("\nTesting list_sectors...")
        try:
            result = await client.call_tool("list_sectors")
            print(f"Success! Found {len(result.content[0].data)} sectors")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test list_filing_types
        print("\nTesting list_filing_types...")
        try:
            result = await client.call_tool("list_filing_types")
            print(f"Success! Found {len(result.content[0].data)} filing types")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test search_companies
        print("\nTesting search_companies...")
        try:
            search_params = CompanySearchParams(search_term="bank")
            result = await client.call_tool("search_companies", {"params": search_params.dict()})
            print(f"Success! Found {len(result.content[0].data)} companies matching 'bank'")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test get_company_detail
        print("\nTesting get_company_detail...")
        try:
            result = await client.call_tool("get_company_detail", {"company_id": 1})
            company = result.content[0].data
            print(f"Success! Got details for {company.get('name', 'unknown company')}")
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n=== Testing Resources ===")
        
        # Test sectors resource
        print("\nTesting financial-reports://sectors resource...")
        try:
            result = await client.read_resource("financial-reports://sectors")
            content = result[0].content
            print(f"Success! Resource returned {len(content.splitlines())} lines")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test company profile resource
        print("\nTesting financial-reports://companies/1/profile resource...")
        try:
            result = await client.read_resource("financial-reports://companies/1/profile")
            content = result[0].content
            print(f"Success! Resource returned {len(content.splitlines())} lines")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
