"""
Example test script to diagnose filings retrieval for adidas AG.
"""
import asyncio
import sys
import os
import json
from fastmcp import Client
from fastmcp.client.transports import FastMCPTransport

async def test_adidas_filings():
    """Test searching companies, fetching latest filings, and details for adidas AG."""
    # Ensure src is on path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from src.financial_reports_mcp import mcp

    # Helper to convert TextContent to Python objects
    def unwrap(result):
        if hasattr(result, "text"):
            return json.loads(result.text)
        if isinstance(result, list) and result and hasattr(result[0], "text"):
            return json.loads(result[0].text)
        return result

    async with Client(FastMCPTransport(mcp)) as client:
        # 1. Search for adidas
        print("\n=== Search Companies ===")
        raw_companies = await client.call_tool("search_companies", {"params": {"search": "adidas", "page": 1, "page_size": 5}})
        companies = unwrap(raw_companies)
        print("Companies result:", companies)
        if companies:
            company_id = companies[0].get("id")
        else:
            print("No companies found for adidas. Falling back to company_id=14")
            company_id = 14
        print(f"Selected company_id: {company_id}")

        # 2. Get latest filings
        print("\n=== Latest Filings ===")
        raw_filings = await client.call_tool("get_latest_filings", {"params": {"company": company_id, "page": 1, "page_size": 5}})
        filings = unwrap(raw_filings)
        print("Filings result:", filings)
        if not filings:
            print("No filings returned for company.")
            return

        filing_id = filings[0].get("id")
        print(f"Selected filing_id: {filing_id}")

        # 3. Get filing detail
        raw_detail = await client.call_tool("get_filing_detail", {"filing_id": filing_id})
        detail = unwrap(raw_detail)
        print("Filing detail:", detail)

        # 4. Try processed filing content
        processed_id = detail.get("processed_filing_id")
        if processed_id:
            print(f"\n=== Processed Filing (ID {processed_id}) ===")
            try:
                content = await client.call_tool("get_processed_filing", {"processed_filing_id": processed_id})
                print("Processed filing content preview:", repr(content)[:200], "...")
            except Exception as e:
                print(f"Error fetching processed filing: {e}")
        else:
            print("No processed_filing_id available in detail.")

if __name__ == "__main__":
    asyncio.run(test_adidas_filings())
