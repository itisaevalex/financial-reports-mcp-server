"""
Mock API client for Financial Reports API.
This module provides a mock implementation of the Financial Reports API client
that returns predefined responses from JSON files instead of making actual API calls.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

# Path to mock response files
MOCK_DIR = Path(__file__).parent

class MockAPIClient:
    """
    Mock client for Financial Reports API.
    """
    
    def __init__(self, api_key: str, base_url: str = "https://api.financialreports.eu/"):
        """Initialize the mock API client."""
        self.api_key = api_key
        self.base_url = base_url
        
    async def get_companies(self, search: Optional[str] = None, 
                     country: Optional[str] = None, 
                     sector: Optional[str] = None,
                     industry: Optional[str] = None,
                     page: int = 1, 
                     page_size: int = 10) -> Dict[str, Any]:
        """Get a list of companies, optionally filtered."""
        data = self._load_mock_data('companies.json')
        
        # Filter results based on search term
        if search:
            search = search.lower()
            filtered_results = []
            for company in data['results']:
                if (search in company['name'].lower() or 
                    (company.get('description') and search in company['description'].lower())):
                    filtered_results.append(company)
            data['results'] = filtered_results
            data['count'] = len(filtered_results)
        
        # Filter by country
        if country:
            country = country.upper()
            data['results'] = [c for c in data['results'] if c.get('country') == country]
            data['count'] = len(data['results'])
            
        # Filter by sector
        if sector:
            data['results'] = [c for c in data['results'] 
                               if c.get('sector') and str(c['sector'].get('code')) == sector]
            data['count'] = len(data['results'])
            
        # Filter by industry
        if industry:
            data['results'] = [c for c in data['results'] 
                               if c.get('industry') and str(c['industry'].get('code')) == industry]
            data['count'] = len(data['results'])
            
        # Apply pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        data['results'] = data['results'][start_idx:end_idx]
        
        # Update pagination links
        if start_idx + page_size < data['count']:
            data['next'] = f"{self.base_url}companies/?page={page+1}"
        else:
            data['next'] = None
            
        if page > 1:
            data['previous'] = f"{self.base_url}companies/?page={page-1}"
        else:
            data['previous'] = None
            
        return data
    
    async def get_company_detail(self, company_id: int) -> Dict[str, Any]:
        """Get detailed information about a specific company."""
        data = self._load_mock_data('company_detail.json')
        
        # In a real implementation, we would use the company_id to fetch
        # the specific company. For now, we just return the mock data.
        # For demo purposes, let's pretend different IDs return modified data
        
        if company_id != 1:  # Our mock is for Deutsche Bank (ID=1)
            # Get companies data and find the company by ID
            companies = self._load_mock_data('companies.json')
            for company in companies['results']:
                if company['id'] == company_id:
                    # Create a simplified company detail by copying some fields
                    data = {
                        "id": company['id'],
                        "name": company['name'],
                        "isin": company.get('isin', ''),
                        "lei": company.get('lei', ''),
                        "country": company.get('country', ''),
                        "description": company.get('description', ''),
                        "sector": company.get('sector', {}),
                        "industry_group": company.get('industry_group', {}),
                        "industry": company.get('industry', {}),
                        "sub_industry": company.get('sub_industry', {})
                    }
                    break
        
        return data
    
    async def get_filings(self, company_id: Optional[int] = None,
                   filing_type: Optional[str] = None,
                   language: Optional[str] = None,
                   page: int = 1,
                   page_size: int = 10) -> Dict[str, Any]:
        """Get a list of filings, optionally filtered."""
        data = self._load_mock_data('filings.json')
        
        # Filter by company
        if company_id:
            data['results'] = [f for f in data['results'] 
                               if f.get('company') and f['company'].get('id') == company_id]
            data['count'] = len(data['results'])
            
        # Filter by filing type
        if filing_type:
            data['results'] = [f for f in data['results'] 
                               if f.get('filing_type') and f['filing_type'].get('code') == filing_type]
            data['count'] = len(data['results'])
            
        # Filter by language
        if language:
            data['results'] = [f for f in data['results'] 
                               if f.get('language') and f['language'].get('code') == language]
            data['count'] = len(data['results'])
            
        # Apply pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        data['results'] = data['results'][start_idx:end_idx]
        
        # Update pagination links
        if start_idx + page_size < data['count']:
            data['next'] = f"{self.base_url}filings/?page={page+1}"
        else:
            data['next'] = None
            
        if page > 1:
            data['previous'] = f"{self.base_url}filings/?page={page-1}"
        else:
            data['previous'] = None
            
        return data
    
    async def get_filing_detail(self, filing_id: int) -> Dict[str, Any]:
        """Get detailed information about a specific filing."""
        data = self._load_mock_data('filing_detail.json')
        
        # In a real implementation, we would use the filing_id to fetch
        # the specific filing. For now, we just return the mock data.
        # For demo purposes, let's pretend different IDs return modified data
        
        if filing_id != 1001:  # Our mock is for a specific filing (ID=1001)
            # Get filings data and find the filing by ID
            filings = self._load_mock_data('filings.json')
            for filing in filings['results']:
                if filing['id'] == filing_id:
                    # Return the simplified filing info
                    return filing
        
        return data
    
    async def get_sectors(self) -> Dict[str, Any]:
        """Get a list of all GICS sectors."""
        return self._load_mock_data('sectors.json')
    
    async def get_filing_types(self) -> Dict[str, Any]:
        """Get a list of all filing types."""
        return self._load_mock_data('filing_types.json')
    
    def _load_mock_data(self, filename: str) -> Dict[str, Any]:
        """Load mock data from JSON file."""
        file_path = MOCK_DIR / filename
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
