import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import asyncio
from src.api_client import APIClient

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
print("[DEBUG] API_KEY from env:", API_KEY)

# Direct requests test
print("\n[DEBUG] Testing direct requests.get to API...")
try:
    resp = requests.get(
        "https://api.financialreports.eu/companies/1/",
        headers={"x-api-key": API_KEY}
    )
    print("[DEBUG] Status:", resp.status_code)
    print("[DEBUG] Body:", resp.text)
except Exception as e:
    print("[DEBUG] Exception during requests.get:", e)

TEST_IDS = [1, 10, 100, 1000, 1234, 9999]

async def main():
    api_client = await APIClient.create()
    for cid in TEST_IDS:
        print(f"\nTesting get_company_detail with company_id={cid}...")
        try:
            detail = await api_client.get_company_detail(cid)
            print(detail)
        except Exception as e:
            print(f"Error for id {cid}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
