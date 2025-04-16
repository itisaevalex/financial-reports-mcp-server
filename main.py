"""
Main entry point for the Financial Reports MCP server.
This file is the main entry point for the MCP server, allowing it to be run
directly or installed via the FastMCP CLI.
"""

import os
import argparse
import sys
from dotenv import load_dotenv
from src.financial_reports_mcp import mcp

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Financial Reports MCP Server")
    parser.add_argument(
        "--host", 
        default=os.getenv("MCP_HOST", "127.0.0.1"),
        help="Host address to bind the server to (default: 127.0.0.1 or MCP_HOST env var)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=int(os.getenv("MCP_PORT", "8000")),
        help="Port to run the server on (default: 8000 or MCP_PORT env var)"
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "http", "ws", "fastmcp"],
        default=os.getenv("MCP_TRANSPORT", "stdio"),
        help="Transport protocol to use (default: stdio or MCP_TRANSPORT env var)"
    )
    return parser.parse_args()

def run_cli():
    """Entry point for CLI execution."""
    # Load environment variables
    load_dotenv()
    
    # Parse arguments
    args = parse_args()
    
    # If using stdio transport, print simplified startup message
    if args.transport == "stdio":
        print(f"Starting Financial Reports MCP Server using stdio transport")
        print(f"Mock API mode: {os.getenv('USE_MOCK_API', 'True')}")
        mcp.run(transport="stdio")
    else:
        # For other transports, we need to set environment variables
        print(f"Starting Financial Reports MCP Server on {args.host}:{args.port} using {args.transport} transport")
        print(f"Mock API mode: {os.getenv('USE_MOCK_API', 'True')}")
        
        # Set environment variables for FastMCP (it uses these internally)
        os.environ["MCP_HOST"] = args.host
        os.environ["MCP_PORT"] = str(args.port)
        
        # Run the server with the specified transport
        mcp.run(transport=args.transport)

if __name__ == "__main__":
    run_cli()
