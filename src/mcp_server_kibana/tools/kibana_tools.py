"""Kibana MCP tools implementation."""

import logging
import os
from typing import Any, Dict, List, Optional
from fastmcp import FastMCP
from ..clients.kibana_client import KibanaClient
from ..models import DataViewRequest, SavedObjectRequest, FindRequest

logger = logging.getLogger(__name__)

# Global client instance
kibana_client: Optional[KibanaClient] = None


def get_client() -> KibanaClient:
    global kibana_client
    if not kibana_client:
        base_url = os.getenv("KIBANA_URL", "http://localhost:5601")
        api_key = os.getenv("KIBANA_API_KEY")
        logger.info(f"Initializing Kibana client with URL: {base_url}")
        kibana_client = KibanaClient(base_url, api_key)
    return kibana_client


# Initialize MCP server
mcp = FastMCP("Kibana API Server")

# Register all tools
@mcp.tool()
async def get_all_data_views(space: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get all data views from Kibana.
    
    Args:
        space: Optional Kibana Space ID (e.g., 'default', 'marketing').
    """
    client = get_client()
    data_views = await client.get_all_data_views(space=space)
    return [dv.model_dump() for dv in data_views]

@mcp.tool()
async def get_data_view(id: str, space: Optional[str] = None) -> Dict[str, Any]:
    """Get a specific data view by ID.
    
    Args:
        id: Data View ID
        space: Optional Kibana Space ID
    """
    client = get_client()
    data_view = await client.get_data_view(id, space=space)
    return data_view.model_dump()

@mcp.tool()
async def create_data_view(data_view: Dict[str, Any], override: bool = False, space: Optional[str] = None) -> Dict[str, Any]:
    """Create a new data view.
    
    Args:
        data_view: Data View definition
        override: Whether to override existing data view
        space: Optional Kibana Space ID
    """
    client = get_client()
    request = DataViewRequest(data_view=data_view, override=override)
    result = await client.create_data_view(request, space=space)
    return result.model_dump()

@mcp.tool()
async def update_data_view(id: str, data_view: Dict[str, Any], override: bool = False, space: Optional[str] = None) -> Dict[str, Any]:
    """Update an existing data view.
    
    Args:
        id: Data View ID
        data_view: Data View definition
        override: Whether to override if exists
        space: Optional Kibana Space ID
    """
    client = get_client()
    request = DataViewRequest(data_view=data_view, override=override)
    result = await client.update_data_view(id, request, space=space)
    return result.model_dump()

@mcp.tool()
async def find_saved_objects(
    type: Optional[str] = None,
    per_page: int = 20,
    page: int = 1,
    search: Optional[str] = None,
    search_fields: Optional[List[str]] = None,
    sort_field: Optional[str] = None,
    sort_order: str = "desc",
    fields: Optional[List[str]] = None,
    filter: Optional[str] = None,
    space: Optional[str] = None
) -> Dict[str, Any]:
    """Find saved objects with search criteria. Use type='visualization' to list all visualizations, type='dashboard' for dashboards, etc.
    
    Args:
        type: Object type (e.g., 'dashboard', 'visualization', 'index-pattern')
        per_page: Number of items per page
        page: Page number
        search: Search query string
        search_fields: Fields to search in
        sort_field: Field to sort by
        sort_order: 'asc' or 'desc'
        fields: Specific fields to return
        filter: Kuery filter string
        space: Optional Kibana Space ID
    """
    client = get_client()
    request = FindRequest(
        type=type, per_page=per_page, page=page, search=search,
        search_fields=search_fields, sort_field=sort_field, 
        sort_order=sort_order, fields=fields, filter=filter
    )
    result = await client.find_saved_objects(request, space=space)
    return {
        "saved_objects": [obj.model_dump() for obj in result["saved_objects"]],
        "total": result["total"],
        "per_page": result["per_page"],
        "page": result["page"]
    }

@mcp.tool()
async def create_saved_object(
    type: str, 
    attributes: Dict[str, Any],
    references: Optional[List[Dict[str, Any]]] = None,
    space: Optional[str] = None
) -> Dict[str, Any]:
    """Create a new saved object.
    
    Args:
        type: Object type
        attributes: Object attributes
        references: Object references
        space: Optional Kibana Space ID
    """
    client = get_client()
    request = SavedObjectRequest(attributes=attributes, references=references)
    result = await client.create_saved_object(type, request, space=space)
    return result.model_dump()

@mcp.tool()
async def get_saved_object(type: str, id: str, space: Optional[str] = None) -> Dict[str, Any]:
    """Get a saved object by type and ID.
    
    Args:
        type: Object type
        id: Object ID
        space: Optional Kibana Space ID
    """
    client = get_client()
    result = await client.get_saved_object(type, id, space=space)
    return result.model_dump()

@mcp.tool()
async def update_saved_object(
    type: str, 
    id: str, 
    attributes: Dict[str, Any],
    references: Optional[List[Dict[str, Any]]] = None,
    space: Optional[str] = None
) -> Dict[str, Any]:
    """Update an existing saved object.
    
    Args:
        type: Object type
        id: Object ID
        attributes: Attributes to update
        references: References to update
        space: Optional Kibana Space ID
    """
    client = get_client()
    request = SavedObjectRequest(attributes=attributes, references=references)
    result = await client.update_saved_object(type, id, request, space=space)
    return result.model_dump()

# Spaces Tools

@mcp.tool()
async def get_all_spaces() -> List[Dict[str, Any]]:
    """Get all Kibana spaces."""
    client = get_client()
    spaces = await client.get_all_spaces()
    return [space.model_dump() for space in spaces]

@mcp.tool()
async def get_space(id: str) -> Dict[str, Any]:
    """Get a specific Kibana space.
    
    Args:
        id: Space ID
    """
    client = get_client()
    space = await client.get_space(id)
    return space.model_dump()

@mcp.tool()
async def create_space(
    id: str, 
    name: str, 
    description: Optional[str] = None,
    color: Optional[str] = None,
    initials: Optional[str] = None,
    disabledFeatures: Optional[List[str]] = None,
    imageUrl: Optional[str] = None
) -> Dict[str, Any]:
    """Create a new Kibana space.
    
    Args:
        id: Space ID (e.g. 'marketing')
        name: Display name
        description: Description
        color: Hex color code
        initials: Initials (max 2 chars)
        disabledFeatures: List of disabled features
        imageUrl: Data-URL encoded image
    """
    client = get_client()
    # SpaceRequest requires id and name
    from ..models import SpaceRequest
    request = SpaceRequest(
        id=id, name=name, description=description, 
        color=color, initials=initials, 
        disabledFeatures=disabledFeatures, imageUrl=imageUrl
    )
    result = await client.create_space(request)
    return result.model_dump()

@mcp.tool()
async def update_space(
    id: str, 
    name: str, 
    description: Optional[str] = None,
    color: Optional[str] = None,
    initials: Optional[str] = None,
    disabledFeatures: Optional[List[str]] = None,
    imageUrl: Optional[str] = None
) -> Dict[str, Any]:
    """Update a Kibana space.
    
    Args:
        id: Space ID
        name: new Display name
        description: new Description
        color: new Hex color code
        initials: new Initials
        disabledFeatures: new List of disabled features
        imageUrl: new Data-URL encoded image
    """
    client = get_client()
    from ..models import SpaceRequest
    request = SpaceRequest(
        id=id, name=name, description=description, 
        color=color, initials=initials, 
        disabledFeatures=disabledFeatures, imageUrl=imageUrl
    )
    result = await client.update_space(id, request)
    return result.model_dump()

@mcp.tool()
async def delete_space(id: str) -> str:
    """Delete a Kibana space.
    
    Args:
        id: Space ID
    """
    client = get_client()
    await client.delete_space(id)
    return f"Space '{id}' deleted successfully"