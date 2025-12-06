"""Authentication module for Kibana MCP Server."""

import os
import logging
from typing import Annotated
from fastapi import Header, HTTPException, status
from .config.settings import settings

logger = logging.getLogger(__name__)

async def verify_token(x_api_key: Annotated[str | None, Header()] = None, authorization: Annotated[str | None, Header()] = None):
    """Verify the MCP API Key from headers."""
    expected_key = settings.mcp_api_key
    
    if not expected_key:
        # If no key is configured, auth is disabled (or handled elsewhere)
        return
        
    token = None
    if x_api_key:
        token = x_api_key
    elif authorization:
        if authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]
        else:
            token = authorization
            
    if not token or token != expected_key:
        logger.warning("Unauthorized access attempt")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
            headers={"WWW-Authenticate": "Bearer"},
        )
