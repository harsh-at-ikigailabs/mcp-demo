# MCP Server

A Model Context Protocol (MCP) server for managing datasets, flows, dashboards, and charts.

## Features

This MCP server provides the following tools:

- **list_datasets**: List all available datasets
- **download_dataset**: Download the data of a dataset given its name
- **list_flows**: List all available flows
- **run_flow**: Run a flow given its name
- **list_dashboards**: List all available dashboards
- **list_charts**: List all available charts

## Installation

### Development Installation

This project uses [Hatch](https://hatch.pypa.io/) for project management. To set up the development environment:

```bash
# Install hatch (if not already installed)
pip install hatch

# Create and activate the development environment
hatch env create
hatch shell

# Install the project in development mode
hatch build
```

## Usage

### Running the MCP Server

The MCP server communicates over HTTP using FastMCP's Streamable HTTP transport. To run it, you must provide the required CLI arguments:

```bash
hatch run dev -- --base-url https://api.example.com --user-email user@example.com --api-key your-api-key --app-name your-app-name
```

Or directly:

```bash
python -m mcp_server.server --base-url https://api.example.com --user-email user@example.com --api-key your-api-key --app-name your-app-name
```

Or using the installed script:

```bash
mcp-server --base-url https://api.example.com --user-email user@example.com --api-key your-api-key --app-name your-app-name
```

#### Required CLI Arguments

- `--base-url`: Base URL for the API
- `--user-email`: User email for authentication
- `--api-key`: API key for authentication
- `--app-name`: Application name

#### Optional CLI Arguments

- `--host`: Host to bind the HTTP server to (default: 127.0.0.1)
- `--port`: Port to bind the HTTP server to (default: 8000)
- `--path`: Path for the HTTP endpoint (default: /mcp)

The server will be accessible at `http://<host>:<port><path>` (e.g., `http://127.0.0.1:8000/mcp`).

### Development

Run tests:

```bash
hatch run test
```

Type checking:

```bash
hatch run types:check
```

## Project Structure

```text
mcp-server/
├── src/
│   └── mcp_server/
│       ├── __init__.py
│       ├── __about__.py
│       └── server.py          # Main MCP server implementation
├── tests/
│   └── __init__.py
├── pyproject.toml              # Project configuration
└── README.md
```

## MCP Tools

### list_datasets

Lists all available datasets.

**Input**: None

**Output**: A formatted list of datasets with their IDs, names, and descriptions.

### download_dataset

Downloads the data of a dataset given its name.

**Input**: 
- `dataset_name` (str): The name of the dataset to download

**Output**: A JSON string containing:
- `dataset_name`: The name of the dataset
- `row_count`: Number of rows in the dataset
- `column_count`: Number of columns in the dataset
- `columns`: List of column names
- `data`: Array of records, where each record is a dictionary mapping column names to values

**Example**:
```json
{
  "dataset_name": "My Dataset",
  "row_count": 100,
  "column_count": 5,
  "columns": ["col1", "col2", "col3", "col4", "col5"],
  "data": [
    {"col1": "value1", "col2": 123, "col3": "text", ...},
    ...
  ]
}
```

### list_flows

Lists all available flows.

**Input**: None

**Output**: A formatted list of flows with their IDs, names, and status.

### run_flow

Runs a flow given its name.

**Input**: 
- `flow_name` (str): The name of the flow to run

**Output**: A JSON string containing:
- `flow_name`: The name of the flow that was run
- `status`: The status of the flow run (e.g., SUCCESS, FAILED)
- `log_id`: The unique identifier for the run log
- `user`: The user who ran the flow
- `erroneous_facet_id`: ID of the facet that caused an error (if any)
- `data`: Additional data from the run
- `timestamp`: When the flow was run

**Example**:
```json
{
  "flow_name": "My Flow",
  "status": "SUCCESS",
  "log_id": "4545454lllllll",
  "user": "bob@example.com",
  "erroneous_facet_id": null,
  "data": "",
  "timestamp": "2025-01-01 11:00:05+00:00"
}
```

**Reference**: [Ikigai Library - Running a Flow](https://github.com/ikigailabs-io/ikigai?tab=readme-ov-file#running-a-flow)

### list_dashboards

Lists all available dashboards.

**Input**: None

**Output**: A formatted list of dashboards with their IDs, names, and widget counts.

### list_charts

Lists all available charts.

**Input**: None

**Output**: A formatted list of charts with their IDs, names, and types.

## Resources

The server also exposes the following resources:

- `datasets://all` - All datasets
- `flows://all` - All flows
- `dashboards://all` - All dashboards
- `charts://all` - All charts

This project follows modern Python best practices:

- Uses Hatch for project management and builds
- Type hints throughout
- Async/await for all I/O operations
- Structured logging
- Modular design

## License

`mcp-server` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
