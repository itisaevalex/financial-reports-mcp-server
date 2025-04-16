"""
Main entry point for the Financial Reports MCP server.
This file is the main entry point for the MCP server, allowing it to be run
directly or installed via the FastMCP CLI.
"""

from src.financial_reports_mcp import mcp

if __name__ == "__main__":
    mcp.run()
