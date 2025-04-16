"""
Main entry point for the Financial Reports MCP server.
This file is the main entry point for the MCP server, allowing it to be run
directly or installed via the FastMCP CLI.
"""

import os
import argparse
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
    return parser.parse_args()

def run_cli():
    """Entry point for CLI execution."""
    # Load environment variables
    load_dotenv()
    
    # Parse arguments
    args = parse_args()
    
    # Print startup information
    print(f"Starting Financial Reports MCP Server on {args.host}:{args.port}")
    print(f"Mock API mode: {os.getenv('USE_MOCK_API', 'True')}")
    
    # Run the server
    mcp.run(host=args.host, port=args.port)

if __name__ == "__main__":
    run_cli()
