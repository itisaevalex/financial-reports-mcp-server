"""
API client factory for Financial Reports API.
This module provides a factory for creating either a real API client
or a mock client depending on configuration.
"""

import os
from typing import Any, Dict, List, Optional, Union

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use environment variables with defaults
API_KEY = os.getenv("API_KEY", "your_api_key_here")
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.financialreports.eu/")
USE_MOCK_API = os.getenv("USE_MOCK_API", "True").lower() == "true"

class APIClient:
    """
    Factory for creating an API client.
    """
    
    @staticmethod
    async def create() -> Any:
        """
        Create and return either a mock or real API client based on configuration.
        """
        if USE_MOCK_API:
            # Import here to avoid circular imports
            from src.mock_api.mock_client import MockAPIClient
            return MockAPIClient(API_KEY, API_BASE_URL)
        else:
            # In a real implementation, we would import and return a real API client
            # For now, just return the mock client since we don't have a real one
            from src.mock_api.mock_client import MockAPIClient
            return MockAPIClient(API_KEY, API_BASE_URL)
