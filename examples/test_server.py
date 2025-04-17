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
    company: int = None
    type: str = None
    language: str = None
    page: int = 1
    page_size: int = 10

async def test_mcp_server_direct():
    """Test the Financial Reports MCP server directly."""
    print("Testing Financial Reports MCP Server using direct import...")
    
    # Import the server directly
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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
            print(f"Success! Got sectors list: {result}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test list_filing_types
        print("\nTesting list_filing_types...")
        try:
            result = await client.call_tool("list_filing_types")
            print(f"Success! Got filing types list: {result}")
        except Exception as e:
            print(f"Error: {e}")

        # Test get_filing_type
        print("\nTesting get_filing_type...")
        try:
            result = await client.call_tool("get_filing_type", {"filing_type_id": 1})
            print(f"Success! Got filing type detail: {result}")
        except Exception as e:
            print(f"Error: {e}")

        # Test list_industries
        print("\nTesting list_industries...")
        try:
            result = await client.call_tool("list_industries")
            print(f"Success! Got industries list: {result}")
        except Exception as e:
            print(f"Error: {e}")

        # Test get_industry
        print("\nTesting get_industry...")
        try:
            result = await client.call_tool("get_industry", {"industry_id": 1})
            print(f"Success! Got industry detail: {result}")
        except Exception as e:
            print(f"Error: {e}")

        # Test list_industry_groups
        print("\nTesting list_industry_groups...")
        try:
            result = await client.call_tool("list_industry_groups")
            print(f"Success! Got industry groups list: {result}")
        except Exception as e:
            print(f"Error: {e}")

        # Test get_industry_group
        print("\nTesting get_industry_group...")
        try:
            result = await client.call_tool("get_industry_group", {"group_id": 1})
            print(f"Success! Got industry group detail: {result}")
        except Exception as e:
            print(f"Error: {e}")

        # Test get_sector
        print("\nTesting get_sector...")
        try:
            result = await client.call_tool("get_sector", {"sector_id": 1})
            print(f"Success! Got sector detail: {result}")
        except Exception as e:
            print(f"Error: {e}")

        # Test list_sub_industries
        print("\nTesting list_sub_industries...")
        try:
            result = await client.call_tool("list_sub_industries")
            print(f"Success! Got sub-industries list: {result}")
        except Exception as e:
            print(f"Error: {e}")

        # Test get_sub_industry
        print("\nTesting get_sub_industry...")
        try:
            result = await client.call_tool("get_sub_industry", {"sub_industry_id": 1})
            print(f"Success! Got sub-industry detail: {result}")
        except Exception as e:
            print(f"Error: {e}")

        # Test list_sources
        print("\nTesting list_sources...")
        try:
            result = await client.call_tool("list_sources")
            print(f"Success! Got sources list: {result}")
        except Exception as e:
            print(f"Error: {e}")

        # Test get_source
        print("\nTesting get_source...")
        try:
            result = await client.call_tool("get_source", {"source_id": 1})
            print(f"Success! Got source detail: {result}")
        except Exception as e:
            print(f"Error: {e}")

        # Test get_processed_filing
        print("\nTesting get_processed_filing...")
        try:
            result = await client.call_tool("get_processed_filing", {"processed_filing_id": 1})
            print(f"Success! Got processed filing detail: {result}")
        except Exception as e:
            print(f"Error: {e}")

        # Test get_schema
        print("\nTesting get_schema...")
        try:
            result = await client.call_tool("get_schema")
            print(f"Success! Got schema: {result}")
        except Exception as e:
            print(f"Error: {e}")

        # Test search_companies
        print("\nTesting search_companies...")
        try:
            search_params = CompanySearchParams(search_term="bank")
            result = await client.call_tool("search_companies", {"params": search_params.model_dump()})
            print(f"Success! Found companies matching 'bank': {result}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test get_company_detail
        print("\nTesting get_company_detail...")
        try:
            result = await client.call_tool("get_company_detail", {"company_id": 1})
            print(f"Success! Got company details: {result}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test get_latest_filings
        print("\nTesting get_latest_filings...")
        try:
            filing_params = FilingSearchParams(company=1)
            result = await client.call_tool("get_latest_filings", {"params": filing_params.model_dump()})
            print(f"Success! Got latest filings: {result}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test get_filing_detail
        print("\nTesting get_filing_detail...")
        try:
            result = await client.call_tool("get_filing_detail", {"filing_id": 1})
            print(f"Success! Got filing detail: {result}")
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n=== Testing Resources ===")
        
        # Test sectors resource
        print("\nTesting financial-reports://sectors resource...")
        try:
            result = await client.read_resource("financial-reports://sectors")
            print(f"Success! Got sectors resource: {result}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test filing types resource
        print("\nTesting financial-reports://filing-types resource...")
        try:
            result = await client.read_resource("financial-reports://filing-types")
            print(f"Success! Got filing types resource: {result}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test company profile resource
        print("\nTesting financial-reports://companies/1/profile resource...")
        try:
            result = await client.read_resource("financial-reports://companies/1/profile")
            print(f"Success! Got company profile resource: {result}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test company recent filings resource
        print("\nTesting financial-reports://companies/1/recent-filings resource...")
        try:
            result = await client.read_resource("financial-reports://companies/1/recent-filings")
            print(f"Success! Got company recent filings resource: {result}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test company recent filings with limit resource
        print("\nTesting financial-reports://companies/1/recent-filings/3 resource...")
        try:
            result = await client.read_resource("financial-reports://companies/1/recent-filings/3")
            print(f"Success! Got company recent filings (limit) resource: {result}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_mcp_server_direct())
