import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.real_api.real_client import RealAPIClient

API_KEY = os.getenv("API_KEY")

async def test_get_industry_groups():
    client = RealAPIClient(api_key=API_KEY)
    print("\nTest 1: No parameters (all industry groups)")
    result = await client.get_industry_groups()
    print(result)

    print("\nTest 2: Valid sector (sector=40, Financials)")
    result = await client.get_industry_groups(sector=40)
    print(result)

    print("\nTest 3: Invalid sector (sector=999)")
    result = await client.get_industry_groups(sector=999)
    print(result)

    print("\nTest 4: Sector as string (sector='40')")
    result = await client.get_industry_groups(sector="40")
    print(result)

    print("\nTest 4b: Lower sector code (sector=1)")
    result = await client.get_industry_groups(sector=1)
    print(result)

    print("\nTest 5: With search term (search='bank')")
    result = await client.get_industry_groups(search='bank')
    print(result)

    print("\nTest 6: Valid sector with search (sector=40, search='bank')")
    result = await client.get_industry_groups(sector=40, search='bank')
    print(result)

    print("\nTest 7: Pagination (page=2, page_size=2)")
    result = await client.get_industry_groups(page=2, page_size=2)
    print(result)

if __name__ == "__main__":
    asyncio.run(test_get_industry_groups())
