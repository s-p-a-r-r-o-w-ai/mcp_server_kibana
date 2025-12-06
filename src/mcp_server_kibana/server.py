#!/usr/bin/env python3
"""
Kibana MCP Server

MCP server providing tools for Kibana REST API endpoints using FastMCP and Pydantic.
Supports stdio, SSE, and streamable-HTTP protocols.
"""

import sys
import os
import argparse
import logging
from pathlib import Path
from .tools.kibana_tools import mcp
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

def create_parser():
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Kibana MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # stdio command
    stdio_parser = subparsers.add_parser("stdio", help="Start a stdio server")
    
    # http command  
    http_parser = subparsers.add_parser("http", help="Start a streamable-HTTP server with optional SSE support")
    http_parser.add_argument("--port", type=int, default=8080, help="Port to listen on")
    
    # sse command
    sse_parser = subparsers.add_parser("sse", help="Start an SSE server")
    sse_parser.add_argument("--port", type=int, default=8080, help="Port to listen on")
    return parser


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
    
    # Note: Authentication is handled by reverse proxy (Caddy/Nginx)
    # See docker-compose.yml for configuration
    
    try:
        if args.command == "stdio":
            logger.info("Starting stdio server")
            mcp.run()
        elif args.command == "http":
            logger.info(f"Starting HTTP server on port {args.port}")
            mcp.run(transport="http", port=args.port, host="0.0.0.0")
        elif args.command == "sse":
            logger.info(f"Starting SSE server on port {args.port}")
            mcp.run(transport="sse", port=args.port, host="0.0.0.0")
        else:
            parser.print_help()
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()