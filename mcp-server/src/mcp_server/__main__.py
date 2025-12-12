"""
Entry point for running the MCP server as a module.
Allows running with: python -m mcp_server
"""

from mcp_server.server import cli

if __name__ == "__main__":
    cli()
