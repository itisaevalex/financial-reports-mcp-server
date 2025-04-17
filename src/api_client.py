"""
API client factory for Financial Reports API.
This module provides a factory for creating the real API client only.
"""

import os
from typing import Any, Dict, List, Optional, Union

from dotenv import load_dotenv

# Load environment variables
load_dotenv()



class APIClient:
    """
    Factory for creating the real API client for Financial Reports API.
    """
    @staticmethod
    async def create() -> Any:
        """
        Create and return the real API client.
        """
        from src.real_api.real_client import RealAPIClient
        import os
        api_key = os.getenv("API_KEY", "your_api_key_here")
        api_base_url = os.getenv("API_BASE_URL", "https://api.financialreports.eu/")
        return RealAPIClient(api_key, api_base_url)
