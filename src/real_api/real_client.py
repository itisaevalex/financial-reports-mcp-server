import os
from typing import Optional, Any, Dict
import financial_reports_generated_client
from financial_reports_generated_client.rest import ApiException

class RealAPIClient:
    """
    Real client for Financial Reports API using the official generated SDK.
    Mirrors the MockAPIClient interface for compatibility.
    """
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.financialreports.eu/"):
        self.api_key = api_key or os.getenv("API_KEY")
        self.base_url = base_url
        self.configuration = financial_reports_generated_client.Configuration(host=self.base_url)
        # Set API Key for header authentication
        self.configuration.api_key['X-API-Key'] = self.api_key

    async def get_companies(self, search: Optional[str] = None, 
                     country: Optional[str] = None, 
                     sector: Optional[str] = None,
                     industry: Optional[str] = None,
                     industry_group: Optional[str] = None,
                     sub_industry: Optional[str] = None,
                     page: int = 1, 
                     page_size: int = 10) -> Dict[str, Any]:
        async with financial_reports_generated_client.ApiClient(self.configuration) as api_client:
            api_instance = financial_reports_generated_client.CompaniesApi(api_client)
            try:
                response = await api_instance.companies_list(
                    search=search,
                    countries=country,
                    sector=sector,
                    industry=industry,
                    industry_group=industry_group,
                    sub_industry=sub_industry,
                    page=page,
                    page_size=page_size
                )
                return response.to_dict() if hasattr(response, 'to_dict') else response
            except ApiException as e:
                return {"error": str(e)}

    # Mirror: async def get_company_detail(self, company_id: int) -> Dict[str, Any]
    async def get_company_detail(self, company_id: int) -> Dict[str, Any]:
        """Get detailed information about a specific company."""
        async with financial_reports_generated_client.ApiClient(self.configuration) as api_client:
            api_instance = financial_reports_generated_client.CompaniesApi(api_client)
            try:
                response = await api_instance.companies_retrieve(company_id)
                return response.to_dict() if hasattr(response, 'to_dict') else response
            except ApiException as e:
                return {"error": str(e)}

    # Mirror: async def get_filings(self, company_id: Optional[int] = None, filing_type: Optional[str] = None, language: Optional[str] = None, page: int = 1, page_size: int = 10) -> Dict[str, Any]
    async def get_filings(self, *args, **kwargs) -> Dict[str, Any]:
        """Get a list of filings, optionally filtered. Accepts both company_id and company for compatibility."""
        # Extract known arguments from kwargs or positional args
        company_id = kwargs.pop('company_id', None)
        company = kwargs.pop('company', None)
        filing_type = kwargs.pop('filing_type', None)
        language = kwargs.pop('language', None)
        page = kwargs.pop('page', 1)
        page_size = kwargs.pop('page_size', 10)
        # Accept legacy positional args (for compatibility)
        if len(args) > 0 and company_id is None:
            company_id = args[0]
        if len(args) > 1 and filing_type is None:
            filing_type = args[1]
        if len(args) > 2 and language is None:
            language = args[2]
        if len(args) > 3 and page == 1:
            page = args[3]
        if len(args) > 4 and page_size == 10:
            page_size = args[4]
        filters = {}
        filters['company'] = company if company is not None else company_id
        if filing_type is not None:
            filters['type'] = filing_type
        if language is not None:
            filters['language'] = language
        filters['page'] = page
        filters['page_size'] = page_size
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        # Only pass valid SDK args, discard any extra kwargs
        async with financial_reports_generated_client.ApiClient(self.configuration) as api_client:
            api_instance = financial_reports_generated_client.FilingsApi(api_client)
            try:
                response = await api_instance.filings_list(**filters)
                return response.to_dict() if hasattr(response, 'to_dict') else response
            except ApiException as e:
                return {"error": str(e)}

    # Mirror: async def get_filing_detail(self, filing_id: int) -> Dict[str, Any]
    async def get_filing_detail(self, filing_id: int) -> Dict[str, Any]:
        """Get detailed information about a specific filing."""
        async with financial_reports_generated_client.ApiClient(self.configuration) as api_client:
            api_instance = financial_reports_generated_client.FilingsApi(api_client)
            try:
                response = await api_instance.filings_retrieve(filing_id)
                return response.to_dict() if hasattr(response, 'to_dict') else response
            except ApiException as e:
                return {"error": str(e)}

    # Mirror: async def get_sectors(self) -> Dict[str, Any]
    async def get_sectors(self) -> Dict[str, Any]:
        """Get a list of all GICS sectors."""
        async with financial_reports_generated_client.ApiClient(self.configuration) as api_client:
            api_instance = financial_reports_generated_client.SectorsApi(api_client)
            try:
                response = await api_instance.sectors_list()
                return response.to_dict() if hasattr(response, 'to_dict') else response
            except ApiException as e:
                return {"error": str(e)}

    # Mirror: async def get_filing_types(self) -> Dict[str, Any]
    async def get_filing_types(self) -> Dict[str, Any]:
        """Get a list of all filing types."""
        async with financial_reports_generated_client.ApiClient(self.configuration) as api_client:
            api_instance = financial_reports_generated_client.FilingTypesApi(api_client)
            try:
                response = await api_instance.filing_types_list()
                return response.to_dict() if hasattr(response, 'to_dict') else response
            except ApiException as e:
                return {"error": str(e)}


    async def get_filings(self, **filters) -> Dict[str, Any]:
        async with financial_reports_generated_client.ApiClient(self.configuration) as api_client:
            api_instance = financial_reports_generated_client.FilingsApi(api_client)
            try:
                response = await api_instance.filings_list(**filters)
                return response.to_dict() if hasattr(response, 'to_dict') else response
            except ApiException as e:
                return {"error": str(e)}

    async def get_filing(self, filing_id: Any) -> Dict[str, Any]:
        async with financial_reports_generated_client.ApiClient(self.configuration) as api_client:
            api_instance = financial_reports_generated_client.FilingsApi(api_client)
            try:
                response = await api_instance.filings_retrieve(filing_id)
                return response.to_dict() if hasattr(response, 'to_dict') else response
            except ApiException as e:
                return {"error": str(e)}

    async def get_filing_types(self, **filters) -> Dict[str, Any]:
        async with financial_reports_generated_client.ApiClient(self.configuration) as api_client:
            api_instance = financial_reports_generated_client.FilingTypesApi(api_client)
            try:
                response = await api_instance.filing_types_list(**filters)
                return response.to_dict() if hasattr(response, 'to_dict') else response
            except ApiException as e:
                return {"error": str(e)}

    async def get_filing_type(self, filing_type_id: Any) -> Dict[str, Any]:
        async with financial_reports_generated_client.ApiClient(self.configuration) as api_client:
            api_instance = financial_reports_generated_client.FilingTypesApi(api_client)
            try:
                response = await api_instance.filing_types_retrieve(filing_type_id)
                return response.to_dict() if hasattr(response, 'to_dict') else response
            except ApiException as e:
                return {"error": str(e)}

    async def get_sectors(self, **filters) -> Dict[str, Any]:
        async with financial_reports_generated_client.ApiClient(self.configuration) as api_client:
            api_instance = financial_reports_generated_client.SectorsApi(api_client)
            try:
                response = await api_instance.sectors_list(**filters)
                return response.to_dict() if hasattr(response, 'to_dict') else response
            except ApiException as e:
                return {"error": str(e)}

    async def get_sector(self, sector_id: Any) -> Dict[str, Any]:
        async with financial_reports_generated_client.ApiClient(self.configuration) as api_client:
            api_instance = financial_reports_generated_client.SectorsApi(api_client)
            try:
                response = await api_instance.sectors_retrieve(sector_id)
                return response.to_dict() if hasattr(response, 'to_dict') else response
            except ApiException as e:
                return {"error": str(e)}

    async def get_industry_groups(self, **filters) -> Dict[str, Any]:
        async with financial_reports_generated_client.ApiClient(self.configuration) as api_client:
            api_instance = financial_reports_generated_client.IndustryGroupsApi(api_client)
            try:
                response = await api_instance.industry_groups_list(**filters)
                return response.to_dict() if hasattr(response, 'to_dict') else response
            except ApiException as e:
                return {"error": str(e)}

    async def get_industry_group(self, group_id: Any) -> Dict[str, Any]:
        async with financial_reports_generated_client.ApiClient(self.configuration) as api_client:
            api_instance = financial_reports_generated_client.IndustryGroupsApi(api_client)
            try:
                response = await api_instance.industry_groups_retrieve(group_id)
                return response.to_dict() if hasattr(response, 'to_dict') else response
            except ApiException as e:
                return {"error": str(e)}

    async def get_industries(self, **filters) -> Dict[str, Any]:
        async with financial_reports_generated_client.ApiClient(self.configuration) as api_client:
            api_instance = financial_reports_generated_client.IndustriesApi(api_client)
            try:
                response = await api_instance.industries_list(**filters)
                return response.to_dict() if hasattr(response, 'to_dict') else response
            except ApiException as e:
                return {"error": str(e)}

    async def get_industry(self, industry_id: Any) -> Dict[str, Any]:
        async with financial_reports_generated_client.ApiClient(self.configuration) as api_client:
            api_instance = financial_reports_generated_client.IndustriesApi(api_client)
            try:
                response = await api_instance.industries_retrieve(industry_id)
                return response.to_dict() if hasattr(response, 'to_dict') else response
            except ApiException as e:
                return {"error": str(e)}

    async def get_sub_industries(self, **filters) -> Dict[str, Any]:
        async with financial_reports_generated_client.ApiClient(self.configuration) as api_client:
            api_instance = financial_reports_generated_client.SubIndustriesApi(api_client)
            try:
                response = await api_instance.sub_industries_list(**filters)
                return response.to_dict() if hasattr(response, 'to_dict') else response
            except ApiException as e:
                return {"error": str(e)}

    async def get_sub_industry(self, sub_industry_id: Any) -> Dict[str, Any]:
        async with financial_reports_generated_client.ApiClient(self.configuration) as api_client:
            api_instance = financial_reports_generated_client.SubIndustriesApi(api_client)
            try:
                response = await api_instance.sub_industries_retrieve(sub_industry_id)
                return response.to_dict() if hasattr(response, 'to_dict') else response
            except ApiException as e:
                return {"error": str(e)}

    async def get_sources(self, **filters) -> Dict[str, Any]:
        async with financial_reports_generated_client.ApiClient(self.configuration) as api_client:
            api_instance = financial_reports_generated_client.SourcesApi(api_client)
            try:
                response = await api_instance.sources_list(**filters)
                return response.to_dict() if hasattr(response, 'to_dict') else response
            except ApiException as e:
                return {"error": str(e)}

    async def get_source(self, source_id: Any) -> Dict[str, Any]:
        async with financial_reports_generated_client.ApiClient(self.configuration) as api_client:
            api_instance = financial_reports_generated_client.SourcesApi(api_client)
            try:
                response = await api_instance.sources_retrieve(source_id)
                return response.to_dict() if hasattr(response, 'to_dict') else response
            except ApiException as e:
                return {"error": str(e)}

    async def get_schema(self) -> Dict[str, Any]:
        async with financial_reports_generated_client.ApiClient(self.configuration) as api_client:
            api_instance = financial_reports_generated_client.SchemaApi(api_client)
            try:
                response = await api_instance.schema_retrieve()
                return response.to_dict() if hasattr(response, 'to_dict') else response
            except ApiException as e:
                return {"error": str(e)}
