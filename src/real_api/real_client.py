import os
from typing import Optional, Any, Dict, Union
import httpx

class RealAPIClient:
    """
    Real client for Financial Reports API, fully aligned with the OpenAPI spec. Uses direct HTTP requests for all endpoints.
    """
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.financialreports.eu/"):
        self.api_key = api_key or os.getenv("API_KEY")
        
        self.base_url = base_url.rstrip("/")
        self.headers = {"x-api-key": self.api_key}

    @staticmethod
    def _format_error(error: Any) -> dict:
        """
        Format errors for user-friendly, ASCII-only output.
        """
        if hasattr(error, 'status_code'):
            # HTTP error
            code = error.status_code
            try:
                detail = error.json()
            except Exception:
                detail = error.text if hasattr(error, 'text') else str(error)
            msg = f"Error: HTTP status {code}."
            if code == 404:
                msg += " Resource not found. This may be due to an incorrect or outdated code. Try searching by name or listing available options."
            elif code == 400:
                msg += " Bad request. Please check your parameters."
            elif code == 401:
                msg += " Unauthorized. Check your API key."
            elif code == 500:
                msg += " Server error. Please try again later."
            else:
                msg += f" {detail}"
            return {"error": msg}
        else:
            # General exception
            msg = f"Error: {str(error)}"
            return {"error": msg}

    async def get_companies(
        self,
        search: Optional[str] = None,
        countries: Optional[Union[str, list]] = None,
        industry: Optional[str] = None,
        industry_group: Optional[str] = None,
        sector: Optional[str] = None,
        sub_industry: Optional[str] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """
        Retrieve a paginated list of companies.
        """
        params = {}
        if countries:
            params['countries'] = ','.join(countries) if isinstance(countries, list) else countries
        if industry is not None:
            params['industry'] = industry
        if industry_group is not None:
            params['industry_group'] = industry_group
        if sector is not None:
            params['sector'] = sector
        if sub_industry is not None:
            params['sub_industry'] = sub_industry
        if search is not None:
            params['search'] = search
        params['page'] = page
        params['page_size'] = page_size
        url = f"{self.base_url}/companies/"
        async with httpx.AsyncClient() as client:
            try:
                
                resp = await client.get(url, headers=self.headers, params=params)
                
                resp.raise_for_status()
                data = resp.json()
                
                return data
            except httpx.HTTPStatusError as e:
                return self._format_error(e.response)
            except Exception as e:
                return self._format_error(e)

    async def get_company_detail(self, company_id: int) -> Dict[str, Any]:
        """
        Retrieve detailed information for a single company by its ID.
        """
        url = f"{self.base_url}/companies/{company_id}/"
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(url, headers=self.headers)
                
                resp.raise_for_status()
                data = resp.json()
                
                return data
            except httpx.HTTPStatusError as e:
                return self._format_error(e.response)
            except Exception as e:
                return self._format_error(e)

    async def get_filings(
        self,
        added_to_platform_from: Optional[str] = None,
        added_to_platform_to: Optional[str] = None,
        company: Optional[int] = None,
        company_isin: Optional[str] = None,
        countries: Optional[Union[str, list]] = None,
        dissemination_datetime_from: Optional[str] = None,
        dissemination_datetime_to: Optional[str] = None,
        language: Optional[str] = None,
        languages: Optional[Union[str, list]] = None,
        lei: Optional[str] = None,
        ordering: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
        release_datetime_from: Optional[str] = None,
        release_datetime_to: Optional[str] = None,
        search: Optional[str] = None,
        source: Optional[int] = None,
        type: Optional[str] = None,
        **extra_filters
    ) -> Dict[str, Any]:
        """
        Retrieve a paginated list of filings with full filtering support.
        """
        params = {}
        if added_to_platform_from: params['added_to_platform_from'] = added_to_platform_from
        if added_to_platform_to: params['added_to_platform_to'] = added_to_platform_to
        if company: params['company'] = company
        if company_isin: params['company_isin'] = company_isin
        if countries: params['countries'] = ','.join(countries) if isinstance(countries, list) else countries
        if dissemination_datetime_from: params['dissemination_datetime_from'] = dissemination_datetime_from
        if dissemination_datetime_to: params['dissemination_datetime_to'] = dissemination_datetime_to
        if language: params['language'] = language
        if languages: params['languages'] = ','.join(languages) if isinstance(languages, list) else languages
        if lei: params['lei'] = lei
        if ordering: params['ordering'] = ordering
        params['page'] = page
        params['page_size'] = page_size
        if release_datetime_from: params['release_datetime_from'] = release_datetime_from
        if release_datetime_to: params['release_datetime_to'] = release_datetime_to
        if search: params['search'] = search
        if source: params['source'] = source
        if type: params['type'] = type
        params.update({k: v for k, v in extra_filters.items() if v is not None})
        url = f"{self.base_url}/filings/"
        async with httpx.AsyncClient() as client:
            try:
                
                resp = await client.get(url, headers=self.headers, params=params)
                
                resp.raise_for_status()
                data = resp.json()
                
                return data
            except httpx.HTTPStatusError as e:
                return self._format_error(e.response)
            except Exception as e:
                return self._format_error(e)

    async def get_filing_detail(self, filing_id: int) -> Dict[str, Any]:
        """
        Retrieve detailed information for a single filing by its ID.
        """
        url = f"{self.base_url}/filings/{filing_id}/"
        async with httpx.AsyncClient() as client:
            try:
                print(f"[API REQUEST] GET {url}")
                resp = await client.get(url, headers=self.headers)
                
                resp.raise_for_status()
                data = resp.json()
                
                return data
            except httpx.HTTPStatusError as e:
                return self._format_error(e.response)
            except Exception as e:
                return self._format_error(e)

    async def get_filing_types(self, page: int = 1, page_size: int = 100, search: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve a list of all available filing types.
        """
        params = {'page': page, 'page_size': page_size}
        if search:
            params['search'] = search
        url = f"{self.base_url}/filing-types/"
        async with httpx.AsyncClient() as client:
            try:
                
                resp = await client.get(url, headers=self.headers, params=params)
                resp.raise_for_status()
                data = resp.json()
                
                return data
            except httpx.HTTPStatusError as e:
                return self._format_error(e.response)
            except Exception as e:
                return self._format_error(e)

    async def get_filing_type(self, filing_type_id: int) -> Dict[str, Any]:
        """
        Retrieve details for a single filing type by its primary key.
        """
        url = f"{self.base_url}/filing-types/{filing_type_id}/"
        async with httpx.AsyncClient() as client:
            try:
                print(f"[API REQUEST] GET {url}")
                resp = await client.get(url, headers=self.headers)
                

                resp.raise_for_status()
                data = resp.json()
                
                return data
            except httpx.HTTPStatusError as e:
                return self._format_error(e.response)
            except Exception as e:
                return self._format_error(e)

    async def get_industries(self, industry_group_code: Optional[str] = None, page: int = 1, page_size: int = 100, search: Optional[str] = None) -> Dict[str, Any]:
        params = {'page': page, 'page_size': page_size}
        if industry_group_code is not None:
            params['industry_group_code'] = str(industry_group_code)
        if search:
            params['search'] = search
        url = f"{self.base_url}/industries/"
        async with httpx.AsyncClient() as client:
            try:
                
                resp = await client.get(url, headers=self.headers, params=params)
                
                
                resp.raise_for_status()
                data = resp.json()
                
                return data
            except httpx.HTTPStatusError as e:
                return self._format_error(e.response)
            except Exception as e:
                return self._format_error(e)

    async def get_industry(self, industry_id: int) -> Dict[str, Any]:
        """
        Retrieve details for a single GICS Industry by its primary key.
        """
        url = f"{self.base_url}/industries/{industry_id}/"
        async with httpx.AsyncClient() as client:
            try:
                print(f"[API REQUEST] GET {url}")
                resp = await client.get(url, headers=self.headers)
                

                resp.raise_for_status()
                data = resp.json()
                
                return data
            except httpx.HTTPStatusError as e:
                return self._format_error(e.response)
            except Exception as e:
                return self._format_error(e)

    async def get_industry_by_code(self, code: str) -> dict:
        url = f"{self.base_url}/industries/"
        params = {"code": code}
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=self.headers, params=params)
            resp.raise_for_status()
            data = resp.json()
            results = data.get("results", [])
            if not results:
                return {"error": f"Industry with code {code} not found."}
            return results[0]

    async def get_industry_groups(self, sector_code: Optional[str] = None, page: int = 1, page_size: int = 100, search: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve a list of all available GICS Industry Groups. Can be filtered by parent sector code.
        """
        params = {'page': page, 'page_size': page_size}
        if sector_code is not None:
            params['sector_code'] = sector_code
        if search:
            params['search'] = search
        url = f"{self.base_url}/industry-groups/"
        async with httpx.AsyncClient() as client:
            try:
                
                resp = await client.get(url, headers=self.headers, params=params)
                resp.raise_for_status()
                data = resp.json()
                
                return data
            except httpx.HTTPStatusError as e:
                return self._format_error(e.response)
            except Exception as e:
                return self._format_error(e)

    async def get_industry_group(self, group_id: int) -> Dict[str, Any]:
        """
        Retrieve details for a single GICS Industry Group by its primary key.
        """
        url = f"{self.base_url}/industry-groups/{group_id}/"
        async with httpx.AsyncClient() as client:
            try:
                print(f"[API REQUEST] GET {url}")
                resp = await client.get(url, headers=self.headers)
                resp.raise_for_status()
                data = resp.json()
                
                return data
            except httpx.HTTPStatusError as e:
                return self._format_error(e.response)
            except Exception as e:
                return self._format_error(e)

    async def get_industry_group_by_code(self, code: str) -> dict:
        url = f"{self.base_url}/industry-groups/"
        params = {"code": code}
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=self.headers, params=params)
            resp.raise_for_status()
            data = resp.json()
            results = data.get("results", [])
            if not results:
                return {"error": f"Industry group with code {code} not found."}
            return results[0]
    
    async def get_sectors(self, page: int = 1, page_size: int = 100, search: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve a list of all available GICS Sectors.
        """
        params = {'page': page, 'page_size': page_size}
        if search:
            params['search'] = search
        url = f"{self.base_url}/sectors/"
        async with httpx.AsyncClient() as client:
            try:
                
                resp = await client.get(url, headers=self.headers, params=params)
                resp.raise_for_status()
                data = resp.json()
                
                return data
            except httpx.HTTPStatusError as e:
                return self._format_error(e.response)
            except Exception as e:
                return self._format_error(e)

    async def get_sector(self, sector_code: str) -> Dict[str, Any]:
        """
        Retrieve details for a single GICS Sector by its code.
        """
        url = f"{self.base_url}/sectors/"
        params = {'code': sector_code}
        async with httpx.AsyncClient() as client:
            try:
                print(f"[API REQUEST] GET {url} params={params}")
                resp = await client.get(url, headers=self.headers, params=params)
                resp.raise_for_status()
                data = resp.json()
                # The API returns a paginated list, so extract the first result
                results = data.get("results", [])
                if not results:
                    return {"error": f"Sector with code {sector_code} not found."}
                return results[0]
            except httpx.HTTPStatusError as e:
                return self._format_error(e.response)
            except Exception as e:
                return self._format_error(e)

    async def get_sub_industries(self, industry_code: Optional[str] = None, page: int = 1, page_size: int = 100, search: Optional[str] = None) -> Dict[str, Any]:
        params = {'page': page, 'page_size': page_size}
        if industry_code is not None:
            params['industry_code'] = str(industry_code)
        if search:
            params['search'] = search
        url = f"{self.base_url}/sub-industries/"
        async with httpx.AsyncClient() as client:
            try:
                
                resp = await client.get(url, headers=self.headers, params=params)
                resp.raise_for_status()
                data = resp.json()
                
                return data
            except httpx.HTTPStatusError as e:
                return self._format_error(e.response)
            except Exception as e:
                return self._format_error(e)

    async def get_sub_industry(self, sub_industry_id: int) -> Dict[str, Any]:
        """
        Retrieve details for a single GICS Sub-Industry by its primary key.
        """
        url = f"{self.base_url}/sub-industries/{sub_industry_id}/"
        async with httpx.AsyncClient() as client:
            try:
                print(f"[API REQUEST] GET {url}")
                resp = await client.get(url, headers=self.headers)
                resp.raise_for_status()
                data = resp.json()
                
                return data
            except httpx.HTTPStatusError as e:
                return self._format_error(e.response)
            except Exception as e:
                return self._format_error(e)

    async def get_sub_industry_by_code(self, code: str) -> dict:
        url = f"{self.base_url}/sub-industries/"
        params = {"code": code}
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=self.headers, params=params)
            resp.raise_for_status()
            data = resp.json()
            results = data.get("results", [])
            if not results:
                return {"error": f"Sub-industry with code {code} not found."}
            return results[0]
    
    async def get_sources(self, page: int = 1, page_size: int = 100) -> Dict[str, Any]:
        """
        Retrieve a list of all available data sources.
        """
        params = {'page': page, 'page_size': page_size}
        url = f"{self.base_url}/sources/"
        async with httpx.AsyncClient() as client:
            try:
                
                resp = await client.get(url, headers=self.headers, params=params)
                resp.raise_for_status()
                data = resp.json()
                
                return data
            except httpx.HTTPStatusError as e:
                return self._format_error(e.response)
            except Exception as e:
                return self._format_error(e)

    async def get_source(self, source_id: int) -> Dict[str, Any]:
        """
        Retrieve details for a single data source by its primary key.
        """
        url = f"{self.base_url}/sources/{source_id}/"
        async with httpx.AsyncClient() as client:
            try:
                print(f"[API REQUEST] GET {url}")
                resp = await client.get(url, headers=self.headers)
                resp.raise_for_status()
                data = resp.json()
                
                return data
            except httpx.HTTPStatusError as e:
                return self._format_error(e.response)
            except Exception as e:
                return self._format_error(e)

    async def get_processed_filing(self, processed_filing_id: int) -> Dict[str, Any]:
        """
        Retrieve the processed content for a single filing by the ProcessedFiling ID.
        """
        url = f"{self.base_url}/processed-filings/{processed_filing_id}/"
        async with httpx.AsyncClient() as client:
            try:
                print(f"[API REQUEST] GET {url}")
                resp = await client.get(url, headers=self.headers)
                resp.raise_for_status()
                data = resp.json()
                
                return data
            except httpx.HTTPStatusError as e:
                return self._format_error(e.response)
            except Exception as e:
                return self._format_error(e)

    async def get_schema(self, format: Optional[str] = None, lang: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve the OpenAPI3 schema for this API. Format and language can be selected via query params.
        """
        params = {}
        if format:
            params['format'] = format
        if lang:
            params['lang'] = lang
        url = f"{self.base_url}/schema/"
        async with httpx.AsyncClient() as client:
            try:
                
                resp = await client.get(url, headers=self.headers, params=params)
                resp.raise_for_status()
                data = resp.json()
                
                return data
            except Exception as e:
                import logging
                return {"error": str(e)}
