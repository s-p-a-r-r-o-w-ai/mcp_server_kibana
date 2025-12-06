"""Kibana HTTP client for REST API operations."""

import httpx
from typing import Any, Dict, List, Optional
from ..models import (
    DataViewResponse, DataViewRequest, SavedObjectResponse, 
    SavedObjectRequest, FindRequest, SpaceResponse, SpaceRequest
)


class KibanaClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Content-Type": "application/json",
            "kbn-xsrf": "true"
        }
        if api_key:
            self.headers["Authorization"] = f"ApiKey {api_key}"
    
    async def _request(self, method: str, endpoint: str, space: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Make a request to Kibana API.
        
        Args:
            method: HTTP method
            endpoint: API endpoint (must start with /)
            space: Optional Kibana space ID. If provided, URL will be /s/{space}{endpoint}
        """
        if space:
            # Ensure we don't double-slash or construct invalid paths
            # endpoint starts with / e.g., /api/data_views
            url_path = f"/s/{space}{endpoint}"
        else:
            url_path = endpoint
            
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method, f"{self.base_url}{url_path}", 
                headers=self.headers, **kwargs
            )
            response.raise_for_status()
            return response.json()
    
    # Data Views
    async def get_all_data_views(self, space: Optional[str] = None) -> List[DataViewResponse]:
        data = await self._request("GET", "/api/data_views", space=space)
        return [DataViewResponse(**dv) for dv in data.get("data_view", [])]
    
    async def get_data_view(self, id: str, space: Optional[str] = None) -> DataViewResponse:
        data = await self._request("GET", f"/api/data_views/data_view/{id}", space=space)
        return DataViewResponse(**data["data_view"])
    
    async def create_data_view(self, request: DataViewRequest, space: Optional[str] = None) -> DataViewResponse:
        data = await self._request("POST", "/api/data_views/data_view", 
                                 json=request.model_dump(by_alias=True), space=space)
        return DataViewResponse(**data["data_view"])
    
    async def update_data_view(self, id: str, request: DataViewRequest, space: Optional[str] = None) -> DataViewResponse:
        data = await self._request("PUT", f"/api/data_views/data_view/{id}", 
                                 json=request.model_dump(by_alias=True), space=space)
        return DataViewResponse(**data["data_view"])
    
    # Saved Objects
    async def find_saved_objects(self, request: FindRequest, space: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        # Only add non-None, non-default values
        if request.type:
            params["type"] = request.type
        if request.per_page != 20:
            params["per_page"] = request.per_page
        if request.page != 1:
            params["page"] = request.page
        if request.search:
            params["search"] = request.search
        if request.sort_field:
            params["sort_field"] = request.sort_field
        if request.sort_order != "desc":
            params["sort_order"] = request.sort_order
        if request.search_fields:
            params["search_fields"] = request.search_fields
        if request.fields:
            params["fields"] = request.fields
        if request.filter:
            params["filter"] = request.filter
        
        data = await self._request("GET", "/api/saved_objects/_find", params=params, space=space)
        return {
            "saved_objects": [SavedObjectResponse(**obj) for obj in data.get("saved_objects", [])],
            "total": data.get("total", 0),
            "per_page": data.get("per_page", 20),
            "page": data.get("page", 1)
        }
    
    async def create_saved_object(self, type: str, request: SavedObjectRequest, space: Optional[str] = None) -> SavedObjectResponse:
        endpoint = f"/api/saved_objects/{type}"
        payload = request.model_dump(exclude_none=True)
        data = await self._request("POST", endpoint, json=payload, space=space)
        return SavedObjectResponse(**data)
    
    async def get_saved_object(self, type: str, id: str, space: Optional[str] = None) -> SavedObjectResponse:
        data = await self._request("GET", f"/api/saved_objects/{type}/{id}", space=space)
        return SavedObjectResponse(**data)
    
    async def update_saved_object(self, type: str, id: str, request: SavedObjectRequest, space: Optional[str] = None) -> SavedObjectResponse:
        payload = request.model_dump(exclude_none=True)
        data = await self._request("PUT", f"/api/saved_objects/{type}/{id}", json=payload, space=space)
        return SavedObjectResponse(**data)

    # Spaces
    async def get_all_spaces(self) -> List[SpaceResponse]:
        data = await self._request("GET", "/api/spaces/space")
        return [SpaceResponse(**space) for space in data]

    async def get_space(self, id: str) -> SpaceResponse:
        data = await self._request("GET", f"/api/spaces/space/{id}")
        return SpaceResponse(**data)

    async def create_space(self, request: SpaceRequest) -> SpaceResponse:
        # Provide by_alias=True if necessary via Config, but standard model_dump is fine
        data = await self._request("POST", "/api/spaces/space", json=request.model_dump(exclude_none=True))
        return SpaceResponse(**data)

    async def update_space(self, id: str, request: SpaceRequest) -> SpaceResponse:
        data = await self._request("PUT", f"/api/spaces/space/{id}", json=request.model_dump(exclude_none=True))
        return SpaceResponse(**data)

    async def delete_space(self, id: str) -> None:
        await self._request("DELETE", f"/api/spaces/space/{id}")