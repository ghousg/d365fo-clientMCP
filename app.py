#!/usr/bin/env python3
"""
Azure Web App entry point for D365FO FastMCP Server.
This module provides an HTTP server interface compatible with Azure Web Apps.
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# Add the src directory to the Python path
src_path = str(Path(__file__).parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Also add the current directory to path
current_path = str(Path(__file__).parent)
if current_path not in sys.path:
    sys.path.insert(0, current_path)

try:
    from d365fo_client.mcp.fastmcp_main import main as fastmcp_main
except ImportError as e:
    print(f"Failed to import d365fo_client: {e}")
    print(f"Python path: {sys.path}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Files in current directory: {list(Path('.').iterdir())}")
    sys.exit(1)


def setup_azure_environment():
    """Configure environment variables for Azure Web Apps."""
    # Set default values for Azure Web Apps
    os.environ.setdefault("MCP_HTTP_HOST", "0.0.0.0")
    os.environ.setdefault("MCP_HTTP_PORT", os.environ.get("PORT", "8000"))
    os.environ.setdefault("D365FO_LOG_LEVEL", "INFO")
    
    # Force HTTP transport for Azure Web Apps
    sys.argv.extend(["--transport", "http", 
                     "--host", os.environ.get("MCP_HTTP_HOST", "0.0.0.0"),
                     "--port", os.environ.get("MCP_HTTP_PORT", "8000")])


def main():
    """Main entry point for Azure Web Apps."""
    # Setup Azure-specific environment
    setup_azure_environment()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Starting D365FO FastMCP Server for Azure Web Apps")
    logger.info(f"Host: {os.environ.get('MCP_HTTP_HOST', '0.0.0.0')}")
    logger.info(f"Port: {os.environ.get('MCP_HTTP_PORT', '8000')}")
    
    # Handle Windows event loop policy for Azure
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # Start the FastMCP server
    fastmcp_main()


if __name__ == "__main__":
    main()