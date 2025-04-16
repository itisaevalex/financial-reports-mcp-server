import os
import asyncio
import financial_reports_generated_client
from financial_reports_generated_client.rest import ApiException
from pprint import pprint

async def test_api():
    # API key to use for authentication
    api_key = "l3t11KuDIhaduGo5saxrVaxRsAT9yV2C2Qjg1Hi7"
    
    # Create configuration
    configuration = financial_reports_generated_client.Configuration(
        host="https://api.financialreports.eu"
    )
    
    # Try different authentication methods
    
    # Method 1: API key in header (custom header)
    print("\n--- Testing with API key in X-API-Key header ---")
    configuration.api_key_prefix['X-API-Key'] = ''
    configuration.api_key['X-API-Key'] = api_key
    
    try:
        async with financial_reports_generated_client.ApiClient(configuration) as api_client:
            api_instance = financial_reports_generated_client.CompaniesApi(api_client)
            api_response = await api_instance.companies_list(page_size=5)
            print("Success! First 5 companies:")
            for company in api_response.results[:5]:
                print(f"- {company.name}")
            return
    except ApiException as e:
        print(f"API Exception: {e}")
    
    # Method 2: API key as cookie auth (as mentioned in the SDK docs)
    print("\n--- Testing with API key as cookieAuth ---")
    configuration.api_key_prefix.pop('X-API-Key', None)
    configuration.api_key.pop('X-API-Key', None)
    configuration.api_key['cookieAuth'] = api_key
    
    try:
        async with financial_reports_generated_client.ApiClient(configuration) as api_client:
            api_instance = financial_reports_generated_client.CompaniesApi(api_client)
            api_response = await api_instance.companies_list(page_size=5)
            print("Success! First 5 companies:")
            for company in api_response.results[:5]:
                print(f"- {company.name}")
            return
    except ApiException as e:
        print(f"API Exception: {e}")
    
    # Method 3: API key in sessionid cookie
    print("\n--- Testing with API key as sessionid cookie ---")
    configuration.api_key.pop('cookieAuth', None)
    configuration.api_key['sessionid'] = api_key
    
    try:
        async with financial_reports_generated_client.ApiClient(configuration) as api_client:
            api_instance = financial_reports_generated_client.CompaniesApi(api_client)
            api_response = await api_instance.companies_list(page_size=5)
            print("Success! First 5 companies:")
            for company in api_response.results[:5]:
                print(f"- {company.name}")
            return
    except ApiException as e:
        print(f"API Exception: {e}")
    
    # Method 4: Basic auth - if the API key is actually a username:password
    print("\n--- Testing with Basic Auth ---")
    configuration.api_key.pop('sessionid', None)
    # Try if the API key is actually formatted as username:password
    if ":" in api_key:
        username, password = api_key.split(":", 1)
    else:
        username, password = api_key, ""
    
    configuration.username = username
    configuration.password = password
    
    try:
        async with financial_reports_generated_client.ApiClient(configuration) as api_client:
            api_instance = financial_reports_generated_client.CompaniesApi(api_client)
            api_response = await api_instance.companies_list(page_size=5)
            print("Success! First 5 companies:")
            for company in api_response.results[:5]:
                print(f"- {company.name}")
            return
    except ApiException as e:
        print(f"API Exception: {e}")
    
    print("\nAll authentication methods failed.")
    print("Consider contacting support at support@financialreports.eu for assistance with API access.")

if __name__ == "__main__":
    asyncio.run(test_api())
