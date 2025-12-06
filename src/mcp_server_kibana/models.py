"""Pydantic models for Kibana API requests and responses."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DataViewResponse(BaseModel):
    id: str
    version: Optional[str] = None
    title: str
    type: Optional[str] = None
    typeMeta: Optional[Dict[str, Any]] = None
    timeFieldName: Optional[str] = None
    sourceFilters: Optional[List[Dict[str, Any]]] = None
    fields: Optional[Dict[str, Any]] = None
    fieldFormats: Optional[Dict[str, Any]] = None
    runtimeFieldMap: Optional[Dict[str, Any]] = None
    fieldAttrs: Optional[Dict[str, Any]] = None
    allowNoIndex: Optional[bool] = None
    namespaces: Optional[List[str]] = None


class DataViewRequest(BaseModel):
    data_view: Dict[str, Any] = Field(..., alias="data_view")
    override: Optional[bool] = False


class SavedObjectResponse(BaseModel):
    id: str
    type: str
    version: str
    attributes: Dict[str, Any]
    references: Optional[List[Dict[str, Any]]] = None
    migrationVersion: Optional[Dict[str, Any]] = None
    coreMigrationVersion: Optional[str] = None
    typeMigrationVersion: Optional[str] = None
    updated_at: Optional[str] = None
    created_at: Optional[str] = None
    namespaces: Optional[List[str]] = None


class SavedObjectRequest(BaseModel):
    attributes: Dict[str, Any]
    references: Optional[List[Dict[str, Any]]] = None
    initialNamespaces: Optional[List[str]] = None


class FindRequest(BaseModel):
    type: Optional[str] = None
    per_page: Optional[int] = 20
    page: Optional[int] = 1
    search: Optional[str] = None
    search_fields: Optional[List[str]] = None
    sort_field: Optional[str] = None
    sort_order: Optional[str] = "desc"
    fields: Optional[List[str]] = None
    filter: Optional[str] = None
    aggs: Optional[str] = None
    namespaces: Optional[List[str]] = None


class SpaceResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    initials: Optional[str] = None
    disabledFeatures: Optional[List[str]] = None
    imageUrl: Optional[str] = None


class SpaceRequest(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    initials: Optional[str] = None
    disabledFeatures: Optional[List[str]] = None
    imageUrl: Optional[str] = None