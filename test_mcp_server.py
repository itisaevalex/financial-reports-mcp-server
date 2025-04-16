import asyncio
from fastmcp import Client

async def test_mcp_server():
    print("Testing Financial Reports MCP Server...")
    
    # Connect to the server
    async with Client("financial_reports_mcp.py:mcp") as client:
        print("\n=== Testing Tools ===")
        
        # Test list_filing_types
        print("\nTesting list_filing_types...")
        try:
            result = await client.call_tool("list_filing_types")
            if 'error' in str(result):
                print(f"Error: {result}")
            else:
                print(f"Success! Found {len(result.content[0].data)} filing types")
        except Exception as e:
            print(f"Exception: {e}")
        
        # Test list_sectors
        print("\nTesting list_sectors...")
        try:
            result = await client.call_tool("list_sectors")
            if 'error' in str(result):
                print(f"Error: {result}")
            else:
                print(f"Success! Found {len(result.content[0].data)} sectors")
        except Exception as e:
            print(f"Exception: {e}")
        
        print("\n=== Testing Resources ===")
        
        # Test sectors resource
        print("\nTesting financial-reports://sectors resource...")
        try:
            result = await client.read_resource("financial-reports://sectors")
            content = result[0].content
            print(f"Resource returned {len(content.splitlines())} lines")
            print("First few lines:")
            for line in content.splitlines()[:3]:
                print(f"  {line}")
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
