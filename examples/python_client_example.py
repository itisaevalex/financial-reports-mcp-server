"""
Example Python client for interacting with the Financial Reports MCP server.
This example shows how to use an MCP client to interact with the Financial Reports 
MCP server programmatically from Python.
"""

import asyncio
import json
from fastmcp import Client

async def main():
    """Main function to demonstrate using the Financial Reports MCP server."""
    
    print("Connecting to Financial Reports MCP server...")
    
    # Connect to the server - assumes it's running locally on port 8000
    # For a different connection, change the URL
    async with Client("http://localhost:8000/mcp") as client:
        
        # Check server connectivity
        await client.ping()
        print("Server connection established.")
        
        # List available tools
        tools = await client.list_tools()
        print(f"\nAvailable tools: {[t.name for t in tools]}")
        
        # List available resources
        resources = await client.list_resources()
        print(f"\nAvailable resources: {[r.uri for r in resources]}")
        
        # Example 1: Get all sectors
        print("\n--- Getting sectors ---")
        sector_response = await client.call_tool("list_sectors")
        sectors = sector_response.content[0].text
        sectors_data = json.loads(sectors)
        
        print(f"Found {len(sectors_data)} sectors:")
        for sector in sectors_data:
            print(f"- {sector['name']} (Code: {sector['code']})")
        
        # Example 2: Search for a specific company
        print("\n--- Searching for Deutsche Bank ---")
        search_params = {
            "params": {
                "search_term": "Deutsche Bank",
                "page": 1,
                "page_size": 3
            }
        }
        
        search_response = await client.call_tool("search_companies", search_params)
        search_results = search_response.content[0].text
        companies = json.loads(search_results)
        
        if companies:
            company = companies[0]  # Take the first result
            company_id = company['id']
            print(f"Found company: {company['name']} (ID: {company_id})")
            
            # Example 3: Get company details
            print("\n--- Getting company details ---")
            detail_response = await client.call_tool("get_company_detail", {"company_id": company_id})
            company_details = detail_response.content[0].text
            details = json.loads(company_details)
            
            print(f"Company: {details['name']}")
            print(f"Country: {details.get('country', 'N/A')}")
            if details.get('sector'):
                print(f"Sector: {details['sector'].get('name', 'N/A')}")
            
            # Example 4: Read a company profile resource
            print("\n--- Reading company profile resource ---")
            profile_resource = await client.read_resource(f"financial-reports://companies/{company_id}/profile")
            profile = profile_resource[0].content
            print(profile[:500] + "..." if len(profile) > 500 else profile)
            
            # Example 5: Get recent filings
            print("\n--- Getting recent filings ---")
            filings_params = {
                "params": {
                    "company_id": company_id,
                    "page": 1,
                    "page_size": 3
                }
            }
            
            filings_response = await client.call_tool("get_latest_filings", filings_params)
            filings_results = filings_response.content[0].text
            filings = json.loads(filings_results)
            
            if filings:
                print(f"Found {len(filings)} recent filings:")
                for filing in filings:
                    filing_date = filing.get("release_datetime", "").split("T")[0]
                    filing_title = filing.get("title", "Untitled")
                    filing_type = filing.get("filing_type", {}).get("name", "Unknown")
                    print(f"- {filing_date}: {filing_title} ({filing_type})")
            else:
                print("No filings found.")
        else:
            print("No companies found matching the search criteria.")

if __name__ == "__main__":
    asyncio.run(main())
