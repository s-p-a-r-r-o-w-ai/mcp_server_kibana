#!/usr/bin/env python3
"""
Kibana MCP Server

MCP server providing tools for Kibana REST API endpoints using FastMCP and Pydantic.
Supports stdio, HTTP, and SSE modes with token verification.
"""

import sys
import os
import argparse
import secrets
import string
from pathlib import Path
from fastmcp.server.auth.providers.debug import DebugTokenVerifier
from .utils.logger import setup_logger
from .config.settings import settings

# Load environment variables from .env file
def load_env_file():
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

load_env_file()

def generate_token(length: int = 32) -> str:
    """Generate a cryptographically secure API key."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def create_parser():
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Kibana MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Optional argument to override transport mode
    parser.add_argument("transport", nargs="?", choices=["stdio", "http", "sse"], help="Transport mode (stdio, http, sse)")
    parser.add_argument("--port", type=int, default=8080, help="Port to listen on (for http/sse)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to listen on")
    
    return parser


def create_app():
    """Create ASGI application for production deployment."""
    # Use the shared setup logic, defaulting to http/sse auth requirements
    return get_configured_mcp(auth_required=True).http_app(path="/mcp")


def get_configured_mcp(auth_required: bool):
    """Factory to create the MCP server with appropriate auth."""
    auth = None
    
    if auth_required:
        # Auto-generate token if not provided
        api_key = settings.mcp_api_key
        if not api_key:
            api_key = generate_token()
            print(f"\n🔑 Generated Bearer Token: {api_key}")
            print(f"Use this token in client requests: Authorization: Bearer {api_key}\n")
        else:
            print(f"\n🔑 Using configured Bearer Token from MCP_API_KEY")

        # Setup authentication
        def validate_token(token: str):
            return token == api_key
        
        auth = DebugTokenVerifier(validate=validate_token)

    from .tools.kibana_tools import get_mcp_with_auth
    return get_mcp_with_auth(auth)


def main():
    """Main entry point matching official server interface"""
    # Setup logging
    logger = setup_logger("mcp-kibana", settings.log_level)
    
    parser = create_parser()
    args = parser.parse_args()

    # Determine transport mode: Arg > Env Var > Default (stdio)
    transport = args.transport
    if not transport:
        transport = os.getenv("MCP_TRANSPORT", "").lower()
    if not transport:
        transport = "stdio"

    # Validate transport
    if transport not in ["stdio", "http", "sse"]:
        logger.warning(f"Unknown transport '{transport}', defaulting to stdio")
        transport = "stdio"

    logger.info(f"Starting Kibana MCP Server in {transport} mode")

    if transport == "stdio":
        # No auth for stdio
        mcp = get_configured_mcp(auth_required=False)
        mcp.run(transport="stdio")
        
    elif transport in ["http", "sse"]:
        # Auth required for network transports
        mcp = get_configured_mcp(auth_required=True)
        
        port = args.port
        host = args.host
        
        logger.info(f"Starting {transport.upper()} server on http://{host}:{port}/mcp")
        # For 'http' transport, FastMCP serves SSE at the endpoint by default if I recall correctly, 
        # or we might need to specify transport="sse" explicitly if available.
        # Passing strict transport string to mcp.run
        mcp.run(transport=transport, port=port, host=host, path="/mcp")

if __name__ == "__main__":
    main()