"""Configuration settings for Kibana MCP server."""

import os
from typing import Optional


class Settings:
    """Application settings."""
    
    def __init__(self):
        self.kibana_url = os.getenv("KIBANA_URL", "http://localhost:5601")
        self.kibana_api_key = os.getenv("KIBANA_API_KEY")
        self.mcp_api_key = os.getenv("MCP_API_KEY")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
    
    @property
    def has_api_key(self) -> bool:
        """Check if Kibana API key is configured."""
        return bool(self.kibana_api_key)


settings = Settings()