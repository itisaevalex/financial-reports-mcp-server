import requests
import json

# API key
API_KEY = "l3t11KuDIhaduGo5saxrVaxRsAT9yV2C2Qjg1Hi7"

# Base URL for the API
BASE_URL = "https://api.financialreports.eu/"

# Try different header formats
headers_options = [
    {"X-API-Key": API_KEY},
    {"x-api-key": API_KEY},
    {"Api-Key": API_KEY},
    {"api-key": API_KEY},
    {"Authorization": f"Bearer {API_KEY}"},
    {"Authorization": f"ApiKey {API_KEY}"}
]

# Test endpoint - let's try to get a list of companies
endpoint = "companies/"
url = BASE_URL + endpoint

print("Testing different authentication header formats...")

for i, headers in enumerate(headers_options):
    print(f"\nTrying header format {i+1}: {headers}")
    # Make the request
    response = requests.get(url, headers=headers)
    
    # Check the response
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}...")  # Show first 200 chars
    
    if response.status_code == 200:
        data = response.json()
        print("\nSuccess! First few companies:")
        for company in data.get("results", [])[:5]:
            print(f"- {company.get('name', 'Unknown')}")
        print(f"Total companies: {data.get('count', 'Unknown')}")
        print("\nSuccessful header format found!")
        break
