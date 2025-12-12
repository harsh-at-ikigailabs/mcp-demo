"""
MCP Server implementation for managing datasets, flows, dashboards, and charts.
"""

import argparse
import asyncio
import json
import logging
from dataclasses import dataclass
from typing import Any, Sequence

from pydantic import AnyUrl

from ikigai import Ikigai
from ikigai.components import App as IkigaiApp

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
    app_name: str


# Global Ikigai client (initialized at server startup)
ikigai_client: Ikigai
ikigai_app: IkigaiApp

def get_ikigai_raw_request_function():
    """
    Get the raw request function from the Ikigai client.

    Signature of the request function:
    ```
    ikigai._Ikigai__client._Client__session.request(
        method: 'HTTPMethod',
        path: 'str',
        params: 'dict[str, str] | None' = None,
        json: 'dict | None' = None,
        *,
        suppress_logging: 'bool' = False,
    ) -> 'Response'
    ```
    """
    return ikigai_client._Ikigai__client._Client__session.request

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
async def call_tool(
    name: str, arguments: dict[str, Any] | None
) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
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
    List all datasets from the Ikigai app.
    """
    logger.info("Listing datasets")
    try:
        datasets_dict = ikigai_app.datasets()
        if not datasets_dict:
            return [
                TextContent(
                    type="text",
                    text="No datasets found in the app.",
                )
            ]

        dataset_list = []
        for name, dataset in datasets_dict.items():
            dataset_info = f"- {name}"
            if hasattr(dataset, "dataset_id"):
                dataset_info += f" (ID: {dataset.dataset_id})"
            if hasattr(dataset, "size"):
                dataset_info += f": Size: {dataset.size}"
            if hasattr(dataset, "data_types"):
                dataset_info += f": Data Types: {dataset.data_types}"
            dataset_list.append(dataset_info)

        return [
            TextContent(
                type="text",
                text=f"Found {len(datasets_dict)} datasets:\n"
                + "\n\n".join(dataset_list),
            )
        ]
    except Exception as e:
        logger.error("Error listing datasets: %s", e)
        return [
            TextContent(
                type="text",
                text=f"Error listing datasets: {str(e)}",
            )
        ]


async def handle_list_flows() -> Sequence[TextContent]:
    """
    List all flows from the Ikigai app.
    """
    logger.info("Listing flows")
    try:
        flows_dict = ikigai_app.flows()
        if not flows_dict:
            return [
                TextContent(
                    type="text",
                    text="No flows found in the app.",
                )
            ]

        flow_list = []
        for name, flow in flows_dict.items():
            flow_info = f"- {name}"
            if hasattr(flow, "flow_id"):
                flow_info += f" (ID: {flow.flow_id})"
            # Get flow status
            try:
                status = flow.status()
                if hasattr(status, "status"):
                    flow_info += f": Status: {status.status}"
            except Exception:
                pass
            flow_list.append(flow_info)

        return [
            TextContent(
                type="text",
                text=f"Found {len(flows_dict)} flows:\n" + "\n".join(flow_list),
            )
        ]
    except Exception as e:
        logger.error("Error listing flows: %s", e)
        return [
            TextContent(
                type="text",
                text=f"Error listing flows: {str(e)}",
            )
        ]


async def handle_list_dashboards() -> Sequence[TextContent]:
    """
    List all dashboards from the Ikigai app.
    """
    logger.info("Listing dashboards")
    try:
        # Check if dashboards method exists
        if hasattr(ikigai_app, "dashboards"):
            dashboards_dict = ikigai_app.dashboards()
            if not dashboards_dict:
                return [
                    TextContent(
                        type="text",
                        text="No dashboards found in the app.",
                    )
                ]

            dashboard_list = []
            for name, dashboard in dashboards_dict.items():
                dashboard_info = f"- {name}"
                if hasattr(dashboard, "dashboard_id"):
                    dashboard_info += f" (ID: {dashboard.dashboard_id})"
                dashboard_list.append(dashboard_info)

            return [
                TextContent(
                    type="text",
                    text=f"Found {len(dashboards_dict)} dashboards:\n"
                    + "\n".join(dashboard_list),
                )
            ]
        else:
            return [
                TextContent(
                    type="text",
                    text="Dashboards functionality is not available in the current Ikigai API.",
                )
            ]
    except Exception as e:
        logger.error("Error listing dashboards: %s", e)
        return [
            TextContent(
                type="text",
                text=f"Error listing dashboards: {str(e)}",
            )
        ]


async def handle_list_charts() -> Sequence[TextContent]:
    """
    List all charts from the Ikigai app.
    """
    logger.info("Listing charts")
    try:
        # Check if charts method exists
        if hasattr(ikigai_app, "charts"):
            charts_dict = ikigai_app.charts()
            if not charts_dict:
                return [
                    TextContent(
                        type="text",
                        text="No charts found in the app.",
                    )
                ]

            chart_list = []
            for name, chart in charts_dict.items():
                chart_info = f"- {name}"
                if hasattr(chart, "chart_id"):
                    chart_info += f" (ID: {chart.chart_id})"
                if hasattr(chart, "chart_type"):
                    chart_info += f": Type: {chart.chart_type}"
                chart_list.append(chart_info)

            return [
                TextContent(
                    type="text",
                    text=f"Found {len(charts_dict)} charts:\n" + "\n".join(chart_list),
                )
            ]
        else:
            return [
                TextContent(
                    type="text",
                    text="Charts functionality is not available in the current Ikigai API.",
                )
            ]
    except Exception as e:
        logger.error("Error listing charts: %s", e)
        return [
            TextContent(
                type="text",
                text=f"Error listing charts: {str(e)}",
            )
        ]


@app.list_resources()
async def list_resources() -> list[Resource]:
    """
    List all available resources in the MCP server.
    """
    return [
        Resource(
            uri=AnyUrl("datasets://all"),
            name="All Datasets",
            description="Resource containing all datasets",
            mimeType="application/json",
        ),
        Resource(
            uri=AnyUrl("flows://all"),
            name="All Flows",
            description="Resource containing all flows",
            mimeType="application/json",
        ),
        Resource(
            uri=AnyUrl("dashboards://all"),
            name="All Dashboards",
            description="Resource containing all dashboards",
            mimeType="application/json",
        ),
        Resource(
            uri=AnyUrl("charts://all"),
            name="All Charts",
            description="Resource containing all charts",
            mimeType="application/json",
        ),
    ]


@app.read_resource()
async def read_resource(uri: AnyUrl) -> str:
    """
    Read a resource by URI.
    """
    logger.info("Reading resource: %s", uri)

    try:
        uri_str = str(uri)
        if uri_str == "datasets://all":
            datasets_dict = ikigai_app.datasets()
            datasets_data = []
            for name, dataset in datasets_dict.items():
                dataset_info = {"name": name}
                if hasattr(dataset, "dataset_id"):
                    dataset_info["id"] = dataset.dataset_id
                if hasattr(dataset, "model_dump"):
                    dataset_info.update(dataset.model_dump())
                datasets_data.append(dataset_info)

            return json.dumps({"datasets": datasets_data}, default=str)
        elif uri_str == "flows://all":
            flows_dict = ikigai_app.flows()
            flows_data = []
            for name, flow in flows_dict.items():
                flow_info = {"name": name}
                if hasattr(flow, "flow_id"):
                    flow_info["id"] = flow.flow_id
                if hasattr(flow, "model_dump"):
                    flow_info.update(flow.model_dump())
                flows_data.append(flow_info)

            return json.dumps({"flows": flows_data}, default=str)
        elif uri_str == "dashboards://all":
            if hasattr(ikigai_app, "dashboards"):
                dashboards_dict = ikigai_app.dashboards()
                dashboards_data = []
                for name, dashboard in dashboards_dict.items():
                    dashboard_info = {"name": name}
                    if hasattr(dashboard, "dashboard_id"):
                        dashboard_info["id"] = dashboard.dashboard_id
                    if hasattr(dashboard, "model_dump"):
                        dashboard_info.update(dashboard.model_dump())
                    dashboards_data.append(dashboard_info)

                return json.dumps({"dashboards": dashboards_data}, default=str)
            else:
                return '{"dashboards": [], "message": "Dashboards not available"}'
        elif uri_str == "charts://all":
            if hasattr(ikigai_app, "charts"):
                charts_dict = ikigai_app.charts()
                charts_data = []
                for name, chart in charts_dict.items():
                    chart_info = {"name": name}
                    if hasattr(chart, "chart_id"):
                        chart_info["id"] = chart.chart_id
                    if hasattr(chart, "model_dump"):
                        chart_info.update(chart.model_dump())
                    charts_data.append(chart_info)

                return json.dumps({"charts": charts_data}, default=str)
            else:
                return '{"charts": [], "message": "Charts not available"}'
        else:
            raise ValueError(f"Unknown resource URI: {uri_str}")
    except Exception as e:
        logger.error("Error reading resource %s: %s", uri, e)
        return json.dumps({"error": str(e)})


async def main(server_config: ServerConfig):
    """
    Main entry point for the MCP server.

    Args:
        server_config: Configuration object containing server settings
    """
    global ikigai_client, ikigai_app

    logger.info("Starting MCP server with base URL: %s", server_config.base_url)
    logger.info("User email: %s", server_config.user_email)
    logger.info("App name: %s", server_config.app_name)
    # Don't log API key for security

    # Initialize Ikigai client
    try:
        logger.info("Initializing Ikigai client...")
        ikigai_client = Ikigai(
            base_url=AnyUrl(server_config.base_url),
            user_email=server_config.user_email,
            api_key=server_config.api_key,
        )
        logger.info("Ikigai client initialized successfully")

        # Access the app by name
        logger.info("Accessing Ikigai app with name: %s", server_config.app_name)
        ikigai_app = ikigai_client.apps[server_config.app_name]
        logger.info("Successfully accessed Ikigai app: %s", server_config.app_name)
    except Exception as e:
        logger.error("Failed to initialize Ikigai client: %s", e)
        raise

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
        "--app-name",
        type=str,
        required=True,
        help="Application name",
    )

    args = parser.parse_args()

    # Create configuration object
    server_config = ServerConfig(
        base_url=args.base_url,
        user_email=args.user_email,
        api_key=args.api_key,
        app_name=args.app_name,
    )

    asyncio.run(main(server_config))


if __name__ == "__main__":
    cli()
