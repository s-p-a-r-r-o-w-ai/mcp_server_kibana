#!/usr/bin/env python3
"""
Kibana MCP Server

MCP server providing tools for Kibana REST API endpoints using FastMCP and Pydantic.
Supports stdio, HTTP, and ASGI app modes with token verification.
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
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # stdio command
    subparsers.add_parser("stdio", help="Start a stdio server")
    
    # http command  
    http_parser = subparsers.add_parser("http", help="Start HTTP server with /mcp endpoint")
    http_parser.add_argument("--port", type=int, default=8080, help="Port to listen on")
    
    # asgi command
    subparsers.add_parser("asgi", help="Create ASGI app (for production deployment)")
    
    return parser


def create_app():
    """Create ASGI application for production deployment."""
    # Auto-generate token if not provided
    api_key = settings.mcp_api_key
    if not api_key:
        api_key = generate_token()
        print(f"\n🔑 Generated Bearer Token: {api_key}")
        print(f"Use this token in client requests: Authorization: Bearer {api_key}\n")
    
    # Setup authentication
    def validate_token(token: str):
        return token == api_key
    
    auth = DebugTokenVerifier(validate=validate_token)
    
    # Create MCP server with auth
    from .tools.kibana_tools import get_mcp_with_auth
    mcp = get_mcp_with_auth(auth)
    
    # Return ASGI app with /mcp endpoint
    return mcp.http_app(path="/mcp")


def main():
    """Main entry point matching official server interface"""
    # Setup logging
    logger = setup_logger("mcp-kibana", settings.log_level)
    
    parser = create_parser()
    
    # Handle no arguments - default to stdio mode
    if len(sys.argv) == 1:
        # Default to stdio mode for MCP inspector compatibility
        class Args:
            command = "stdio"
        args = Args()
    else:
        args = parser.parse_args()
    
    logger.info(f"Starting Kibana MCP Server in {args.command} mode")
    
    try:
        if args.command == "stdio":
            # No auth for stdio mode
            from .tools.kibana_tools import get_mcp_with_auth
            mcp = get_mcp_with_auth(None)
            logger.info("Starting stdio server")
            mcp.run()
            
        elif args.command == "http":
            # Auto-generate token if not provided
            api_key = settings.mcp_api_key
            if not api_key:
                api_key = generate_token()
                print(f"\n🔑 Generated Bearer Token: {api_key}")
                print(f"Use this token in client requests: Authorization: Bearer {api_key}")
                print(f"MCP Endpoint: http://localhost:{args.port}/mcp\n")
            else:
                print(f"\n🔑 Using configured Bearer Token from MCP_API_KEY")
                print(f"MCP Endpoint: http://localhost:{args.port}/mcp\n")
            
            # Setup authentication
            def validate_token(token: str):
                return token == api_key
            
            auth = DebugTokenVerifier(validate=validate_token)
            
            # Create and run server
            from .tools.kibana_tools import get_mcp_with_auth
            mcp = get_mcp_with_auth(auth)
            
            logger.info(f"Starting HTTP server on port {args.port} with /mcp endpoint")
            mcp.run(transport="http", port=args.port, host="0.0.0.0", path="/mcp")
            
        elif args.command == "asgi":
            print("ASGI app created. Use with: uvicorn mcp_server_kibana.server:app")
            
        else:
            parser.print_help()
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)


# ASGI app for production deployment
# Use: uvicorn mcp_server_kibana.server:create_app --factory
app = create_app

if __name__ == "__main__":
    main()