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

Lists all available datasets in the app.

Datasets are data files stored in the Ikigai platform. They can be CSV files, Excel files, or Pandas DataFrames that have been uploaded to Ikigai.

**Input**: None

**Output**: A formatted list showing:
- Dataset name
- Dataset ID
- Size (number of records)
- Data types for each column

**Reference**: [Ikigai Library - Finding a Dataset from an App](https://github.com/ikigailabs-io/ikigai?tab=readme-ov-file#finding-a-dataset-from-an-app)

### download_dataset

Downloads the data of a dataset given its name.

Downloads the dataset as a pandas DataFrame and returns the first 10 rows as JSON records. This is useful for inspecting dataset contents without downloading the entire dataset. The dataset can be any data file stored in Ikigai (CSV, Excel, etc.) that has been uploaded to the platform.

**Input**: 
- `dataset_name` (str): The name of the dataset to download. Use `list_datasets` to see available dataset names.

**Output**: A JSON string containing:
- `dataset_name`: The name of the dataset
- `row_count`: Number of rows returned (limited to 10 for context size)
- `column_count`: Number of columns in the dataset
- `columns`: List of column names
- `data`: Array of records, where each record is a dictionary mapping column names to values

**Example**:
```json
{
  "dataset_name": "My Dataset",
  "row_count": 10,
  "column_count": 5,
  "columns": ["col1", "col2", "col3", "col4", "col5"],
  "data": [
    {"col1": "value1", "col2": 123, "col3": "text", "col4": 45.6, "col5": "2024-01-01"},
    {"col1": "value2", "col2": 456, "col3": "text2", "col4": 78.9, "col5": "2024-01-02"},
    ...
  ]
}
```

**Reference**: [Ikigai Library - Downloading Your Existing Dataset](https://github.com/ikigailabs-io/ikigai?tab=readme-ov-file#downloading-your-existing-dataset)

### list_flows

Lists all available flows in the app.

A Flow is a component in an Ikigai app that enables you to perform analysis or computation. Each Flow contains a Flow Definition that specifies the sequence of Facet Types that perform actions like ingesting data, transforming data, machine learning with models, and outputting data.

**Input**: None

**Output**: A formatted list showing:
- Flow name
- Flow ID
- Current status (IDLE, RUNNING, SUCCESS, FAILED, etc.)

**Reference**: [Ikigai Library - Finding a Flow from an App](https://github.com/ikigailabs-io/ikigai?tab=readme-ov-file#finding-a-flow-from-an-app)

### run_flow

Runs a flow given its name.

Executes a flow on the Ikigai platform. When a flow runs, it executes all the facets defined in the flow definition in sequence, performing operations like data ingestion, transformation, machine learning, and data output. A RunLog is created that stores the run's details including status, timestamp, and any error information. The flow must exist in the app and be properly configured before it can be run.

**Input**: 
- `flow_name` (str): The name of the flow to run. Use `list_flows` to see available flow names.

**Output**: A JSON string containing the run log information:
- `flow_name`: Name of the flow that was executed
- `status`: Status of the flow run (SUCCESS, FAILED, etc.)
- `log_id`: Unique identifier for this run log
- `user`: Email of the user who ran the flow
- `erroneous_facet_id`: ID of the facet that caused an error (if any)
- `data`: Additional data from the run
- `timestamp`: When the flow was executed (ISO format)

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

Lists all available dashboards in the app.

Dashboards are visualization components in Ikigai that display data and insights. They can contain multiple charts and widgets to provide a comprehensive view of your data.

**Note**: Dashboards functionality may not be available in all Ikigai API versions.

**Input**: None

**Output**: A formatted list of dashboards with their IDs and names, or a message indicating dashboards are not available.

### list_charts

Lists all available charts in the app.

Charts are visualization components in Ikigai that display data in various formats (bar charts, line charts, pie charts, etc.). Charts are typically associated with datasets and can be embedded in dashboards.

**Note**: Charts functionality may not be available in all Ikigai API versions.

**Input**: None

**Output**: A formatted list of charts with their IDs, names, and chart types, or a message indicating charts are not available.

## Resources

The server also exposes the following resources that provide programmatic access to Ikigai components:

### datasets://all

Resource containing all datasets in the app as JSON. Each dataset entry includes:
- `name`: Dataset name
- `id`: Dataset ID
- `size`: Number of records
- `columns`: List of column names (from data_types)

**Reference**: [Ikigai Library - Finding a Dataset from an App](https://github.com/ikigailabs-io/ikigai?tab=readme-ov-file#finding-a-dataset-from-an-app)

### flows://all

Resource containing all flows in the app as JSON. Each flow entry includes:
- `name`: Flow name
- `id`: Flow ID
- Additional flow definition details (facets, arrows, arguments, variables)

**Reference**: [Ikigai Library - Finding a Flow from an App](https://github.com/ikigailabs-io/ikigai?tab=readme-ov-file#finding-a-flow-from-an-app)

### dashboards://all

Resource containing all dashboards in the app as JSON. Each dashboard entry includes:
- `name`: Dashboard name
- `id`: Dashboard ID
- Additional dashboard configuration details

**Note**: Dashboards functionality may not be available in all Ikigai API versions.

### charts://all

Resource containing all charts in the app as JSON. Each chart entry includes:
- `name`: Chart name
- `id`: Chart ID
- Additional chart configuration details (chart_type, dataset_id, etc.)

**Note**: Charts functionality may not be available in all Ikigai API versions.

This project follows modern Python best practices:

- Uses Hatch for project management and builds
- Type hints throughout
- Async/await for all I/O operations
- Structured logging
- Modular design

## License

`mcp-server` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
