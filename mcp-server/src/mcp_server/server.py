"""
MCP Server implementation for managing datasets, flows, dashboards, and charts.
"""
import argparse
import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ServerConfig:
    """Configuration for the MCP server."""
    base_url: str
    user_email: str
    api_key: str
    app_id: str


# Global configuration variable (set during CLI initialization)
config: ServerConfig | None = None

# Create the MCP server instance
app = Server("mcp-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List all available tools (endpoints) in the MCP server.
    """
    return [
        Tool(
            name="list_datasets",
            description="List all available datasets",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="list_flows",
            description="List all available flows",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="list_dashboards",
            description="List all available dashboards",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="list_charts",
            description="List all available charts",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """
    Handle tool calls for the MCP server.
    """
    if arguments is None:
        arguments = {}

    logger.info("Tool called: %s with arguments: %s", name, arguments)

    if name == "list_datasets":
        return await handle_list_datasets()
    elif name == "list_flows":
        return await handle_list_flows()
    elif name == "list_dashboards":
        return await handle_list_dashboards()
    elif name == "list_charts":
        return await handle_list_charts()
    else:
        raise ValueError(f"Unknown tool: {name}")


async def handle_list_datasets() -> Sequence[TextContent]:
    """
    Stub implementation for listing datasets.
    """
    logger.info("Listing datasets")
    if config:
        logger.info("Using base URL: %s, App ID: %s", config.base_url, config.app_id)
    # TODO: Implement actual dataset listing logic using config
    datasets = [
        {"id": "dataset_1", "name": "Sample Dataset 1", "description": "A sample dataset"},
        {"id": "dataset_2", "name": "Sample Dataset 2", "description": "Another sample dataset"},
    ]
    return [
        TextContent(
            type="text",
            text=f"Found {len(datasets)} datasets:\n" + "\n".join(
                f"- {ds['name']} (ID: {ds['id']}): {ds['description']}"
                for ds in datasets
            )
        )
    ]


async def handle_list_flows() -> Sequence[TextContent]:
    """
    Stub implementation for listing flows.
    """
    logger.info("Listing flows")
    # TODO: Implement actual flow listing logic
    flows = [
        {"id": "flow_1", "name": "Sample Flow 1", "status": "active"},
        {"id": "flow_2", "name": "Sample Flow 2", "status": "inactive"},
    ]
    return [
        TextContent(
            type="text",
            text=f"Found {len(flows)} flows:\n" + "\n".join(
                f"- {flow['name']} (ID: {flow['id']}): Status: {flow['status']}"
                for flow in flows
            )
        )
    ]


async def handle_list_dashboards() -> Sequence[TextContent]:
    """
    Stub implementation for listing dashboards.
    """
    logger.info("Listing dashboards")
    # TODO: Implement actual dashboard listing logic
    dashboards = [
        {"id": "dashboard_1", "name": "Sample Dashboard 1", "widgets": 5},
        {"id": "dashboard_2", "name": "Sample Dashboard 2", "widgets": 3},
    ]
    return [
        TextContent(
            type="text",
            text=f"Found {len(dashboards)} dashboards:\n" + "\n".join(
                f"- {db['name']} (ID: {db['id']}): {db['widgets']} widgets"
                for db in dashboards
            )
        )
    ]


async def handle_list_charts() -> Sequence[TextContent]:
    """
    Stub implementation for listing charts.
    """
    logger.info("Listing charts")
    # TODO: Implement actual chart listing logic
    charts = [
        {"id": "chart_1", "name": "Sample Chart 1", "type": "bar"},
        {"id": "chart_2", "name": "Sample Chart 2", "type": "line"},
    ]
    return [
        TextContent(
            type="text",
            text=f"Found {len(charts)} charts:\n" + "\n".join(
                f"- {chart['name']} (ID: {chart['id']}): Type: {chart['type']}"
                for chart in charts
            )
        )
    ]


@app.list_resources()
async def list_resources() -> list[Resource]:
    """
    List all available resources in the MCP server.
    """
    return [
        Resource(
            uri="datasets://all",
            name="All Datasets",
            description="Resource containing all datasets",
            mimeType="application/json",
        ),
        Resource(
            uri="flows://all",
            name="All Flows",
            description="Resource containing all flows",
            mimeType="application/json",
        ),
        Resource(
            uri="dashboards://all",
            name="All Dashboards",
            description="Resource containing all dashboards",
            mimeType="application/json",
        ),
        Resource(
            uri="charts://all",
            name="All Charts",
            description="Resource containing all charts",
            mimeType="application/json",
        ),
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """
    Read a resource by URI.
    """
    logger.info("Reading resource: %s", uri)
    
    if uri == "datasets://all":
        # TODO: Implement actual dataset retrieval
        return '{"datasets": []}'
    elif uri == "flows://all":
        # TODO: Implement actual flow retrieval
        return '{"flows": []}'
    elif uri == "dashboards://all":
        # TODO: Implement actual dashboard retrieval
        return '{"dashboards": []}'
    elif uri == "charts://all":
        # TODO: Implement actual chart retrieval
        return '{"charts": []}'
    else:
        raise ValueError(f"Unknown resource URI: {uri}")


async def main(server_config: ServerConfig):
    """
    Main entry point for the MCP server.
    
    Args:
        server_config: Configuration object containing server settings
    """
    global config
    config = server_config
    
    logger.info("Starting MCP server with base URL: %s", config.base_url)
    logger.info("User email: %s", config.user_email)
    logger.info("App ID: %s", config.app_id)
    # Don't log API key for security
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


def cli():
    """
    CLI entry point for the MCP server.
    Parses command-line arguments and starts the server.
    """
    parser = argparse.ArgumentParser(
        description="MCP Server for managing datasets, flows, dashboards, and charts"
    )
    parser.add_argument(
        "--base-url",
        type=str,
        required=True,
        help="Base URL for the API",
    )
    parser.add_argument(
        "--user-email",
        type=str,
        required=True,
        help="User email for authentication",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        required=True,
        help="API key for authentication",
    )
    parser.add_argument(
        "--app-id",
        type=str,
        required=True,
        help="Application ID",
    )
    
    args = parser.parse_args()
    
    # Create configuration object
    server_config = ServerConfig(
        base_url=args.base_url,
        user_email=args.user_email,
        api_key=args.api_key,
        app_id=args.app_id,
    )
    
    asyncio.run(main(server_config))


if __name__ == "__main__":
    cli()

