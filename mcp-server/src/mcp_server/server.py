"""
MCP Server implementation for managing datasets, flows, dashboards, and charts.
"""

import argparse
import json
import logging
from dataclasses import dataclass
from typing import Any

import pandas as pd
from pydantic import AnyUrl

from ikigai import Ikigai
from ikigai.components import App as IkigaiApp

from fastmcp import FastMCP

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
mcp = FastMCP("mcp-server")


@mcp.tool()
def list_datasets() -> str:
    """
    List all available datasets.
    """
    logger.info("Listing datasets")
    try:
        datasets_dict = ikigai_app.datasets()
        if not datasets_dict:
            return "No datasets found in the app."

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

        return f"Found {len(datasets_dict)} datasets:\n" + "\n\n".join(dataset_list)
    except Exception as e:
        logger.error("Error listing datasets: %s", e)
        return f"Error listing datasets: {str(e)}"


@mcp.tool()
def download_dataset(dataset_name: str) -> str:
    """
    Download the data of a dataset given its name.
    
    Args:
        dataset_name: The name of the dataset to download
        
    Returns:
        A JSON string containing the dataset data as records
    """
    logger.info("Downloading dataset: %s", dataset_name)
    try:
        # Get all datasets from the app
        datasets_dict = ikigai_app.datasets()
        
        if not datasets_dict:
            return "No datasets found in the app."
        
        # Check if the dataset exists
        if dataset_name not in datasets_dict:
            available_datasets = ", ".join(datasets_dict.keys())
            return f"Dataset '{dataset_name}' not found. Available datasets: {available_datasets}"
        
        # Get the specific dataset
        dataset = datasets_dict[dataset_name]
        
        # Download the dataset as a pandas DataFrame
        df = dataset.df().head(10)
        
        # Convert DataFrame to JSON records format
        # Using orient='records' to get a list of dictionaries
        data_records = df.to_dict(orient='records')
        
        # Create response with metadata
        result = {
            "dataset_name": dataset_name,
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": list(df.columns),
            "data": data_records
        }
        
        logger.info("Successfully downloaded dataset '%s' with %d rows and %d columns", 
                   dataset_name, len(df), len(df.columns))
        
        return json.dumps(result, default=str, indent=2)
        
    except Exception as e:
        logger.error("Error downloading dataset '%s': %s", dataset_name, e)
        return f"Error downloading dataset '{dataset_name}': {str(e)}"


@mcp.tool()
def list_flows() -> str:
    """
    List all available flows.
    """
    logger.info("Listing flows")
    try:
        flows_dict = ikigai_app.flows()
        if not flows_dict:
            return "No flows found in the app."

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

        return f"Found {len(flows_dict)} flows:\n" + "\n".join(flow_list)
    except Exception as e:
        logger.error("Error listing flows: %s", e)
        return f"Error listing flows: {str(e)}"


@mcp.tool()
def list_dashboards() -> str:
    """
    List all available dashboards.
    """
    logger.info("Listing dashboards")
    try:
        # Check if dashboards method exists
        if hasattr(ikigai_app, "dashboards"):
            dashboards_dict = ikigai_app.dashboards()
            if not dashboards_dict:
                return "No dashboards found in the app."

            dashboard_list = []
            for name, dashboard in dashboards_dict.items():
                dashboard_info = f"- {name}"
                if hasattr(dashboard, "dashboard_id"):
                    dashboard_info += f" (ID: {dashboard.dashboard_id})"
                dashboard_list.append(dashboard_info)

            return f"Found {len(dashboards_dict)} dashboards:\n" + "\n".join(dashboard_list)
        else:
            return "Dashboards functionality is not available in the current Ikigai API."
    except Exception as e:
        logger.error("Error listing dashboards: %s", e)
        return f"Error listing dashboards: {str(e)}"


@mcp.tool()
def list_charts() -> str:
    """
    List all available charts.
    """
    logger.info("Listing charts")
    try:
        # Check if charts method exists
        if hasattr(ikigai_app, "charts"):
            charts_dict = ikigai_app.charts()
            if not charts_dict:
                return "No charts found in the app."

            chart_list = []
            for name, chart in charts_dict.items():
                chart_info = f"- {name}"
                if hasattr(chart, "chart_id"):
                    chart_info += f" (ID: {chart.chart_id})"
                if hasattr(chart, "chart_type"):
                    chart_info += f": Type: {chart.chart_type}"
                chart_list.append(chart_info)

            return f"Found {len(charts_dict)} charts:\n" + "\n".join(chart_list)
        else:
            return "Charts functionality is not available in the current Ikigai API."
    except Exception as e:
        logger.error("Error listing charts: %s", e)
        return f"Error listing charts: {str(e)}"


@mcp.resource("datasets://all")
def get_datasets_resource() -> str:
    """
    Resource containing all datasets.
    """
    logger.info("Reading resource: datasets://all")
    try:
        datasets_dict = ikigai_app.datasets()
        datasets_data = []
        for name, dataset in datasets_dict.items():
            dataset_info = {
                "name": name,
                "id": dataset.dataset_id,
                "size": dataset.size,
                "columns": dataset.data_types.keys(),
            }
            datasets_data.append(dataset_info)

        return json.dumps({"datasets": datasets_data}, default=str)
    except Exception as e:
        logger.error("Error reading resource datasets://all: %s", e)
        return json.dumps({"error": str(e)})


@mcp.resource("flows://all")
def get_flows_resource() -> str:
    """
    Resource containing all flows.
    """
    logger.info("Reading resource: flows://all")
    try:
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
    except Exception as e:
        logger.error("Error reading resource flows://all: %s", e)
        return json.dumps({"error": str(e)})


@mcp.resource("dashboards://all")
def get_dashboards_resource() -> str:
    """
    Resource containing all dashboards.
    """
    logger.info("Reading resource: dashboards://all")
    try:
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
    except Exception as e:
        logger.error("Error reading resource dashboards://all: %s", e)
        return json.dumps({"error": str(e)})


@mcp.resource("charts://all")
def get_charts_resource() -> str:
    """
    Resource containing all charts.
    """
    logger.info("Reading resource: charts://all")
    try:
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
    except Exception as e:
        logger.error("Error reading resource charts://all: %s", e)
        return json.dumps({"error": str(e)})


def initialize_ikigai(server_config: ServerConfig):
    """
    Initialize the Ikigai client and app.

    Args:
        server_config: Configuration object containing server settings
    """
    global ikigai_client, ikigai_app

    logger.info("Initializing Ikigai client with base URL: %s", server_config.base_url)
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

    # Initialize Ikigai client
    initialize_ikigai(server_config)

    # Start the HTTP server
    mcp.run()


if __name__ == "__main__":
    cli()
