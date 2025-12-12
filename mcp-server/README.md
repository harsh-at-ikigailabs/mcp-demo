# MCP Server

A Model Context Protocol (MCP) server for managing datasets, flows, dashboards, and charts via the Ikigai platform.

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
hatch run dev -- --base-url https://api.ikigailabs.io --user-email user@example.com --api-key your-api-key --app-name your-app-name
```

Or directly:

```bash
python -m mcp_server.server --base-url https://api.ikigailabs.io --user-email user@example.com --api-key your-api-key --app-name your-app-name
```

Or using the installed script:

```bash
mcp-server --base-url https://api.ikigailabs.io --user-email user@example.com --api-key your-api-key --app-name your-app-name
```

#### Required CLI Arguments

- `--base-url`: Base URL for the Ikigai API
- `--user-email`: User email for authentication
- `--api-key`: API key for authentication
- `--app-name`: Name of the Ikigai app to connect to

### Development

Run tests:

```bash
hatch run test
```

Type checking:

```bash
hatch run types:check
```

Format code:

```bash
hatch run fmt
```

Lint code:

```bash
hatch run lint
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
│   └── test_server.py
├── pyproject.toml              # Project configuration
└── README.md
```

## MCP Tools

### list_datasets

Lists all available datasets in the app.

Datasets are data files stored in the Ikigai platform. They can be CSV files, Excel files, or Pandas DataFrames that have been uploaded to Ikigai.

**Input**: None

**Output**: A formatted string listing all datasets. Example:

```
Found 3 datasets:
- Sales Data (ID: abc123): Size: 1500: Data Types: {'date': 'datetime', 'amount': 'float', 'product': 'str'}

- Customer Info (ID: def456): Size: 500: Data Types: {'name': 'str', 'email': 'str', 'signup_date': 'datetime'}

- Inventory (ID: ghi789): Size: 2000: Data Types: {'sku': 'str', 'quantity': 'int', 'warehouse': 'str'}
```

**Reference**: [Ikigai Library - Finding a Dataset from an App](https://github.com/ikigailabs-io/ikigai?tab=readme-ov-file#finding-a-dataset-from-an-app)

### download_dataset

Downloads the data of a dataset given its name.

Downloads the dataset as a pandas DataFrame and returns the first 10 rows as JSON. This is useful for inspecting dataset contents without downloading the entire dataset. The dataset can be any data file stored in Ikigai (CSV, Excel, etc.) that has been uploaded to the platform.

**Input**: 
- `dataset_name` (str): The name of the dataset to download. Use `list_datasets` to see available dataset names.

**Output**: A JSON string containing:
- `dataset_name`: The name of the dataset
- `row_count`: Number of rows returned (limited to 10)
- `visible_row_index`: List of row indices that are visible in the response
- `column_count`: Number of columns in the dataset
- `columns`: List of column names
- `data`: Array of rows, where each row is an array of values

**Example**:
```json
{
  "dataset_name": "Sales Data",
  "row_count": 10,
  "visible_row_index": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
  "column_count": 5,
  "columns": ["date", "product", "quantity", "price", "total"],
  "data": [
    ["2024-01-01", "Widget A", 10, 25.99, 259.90],
    ["2024-01-02", "Widget B", 5, 15.50, 77.50],
    ["2024-01-03", "Widget A", 8, 25.99, 207.92]
  ]
}
```

**Reference**: [Ikigai Library - Downloading Your Existing Dataset](https://github.com/ikigailabs-io/ikigai?tab=readme-ov-file#downloading-your-existing-dataset)

### list_flows

Lists all available flows in the app.

A Flow is a component in an Ikigai app that enables you to perform analysis or computation. Each Flow contains a Flow Definition that specifies the sequence of Facet Types that perform actions like ingesting data, transforming data, machine learning with models, and outputting data.

**Input**: None

**Output**: A formatted string listing all flows. Example:

```
Found 2 flows:
- Data Processing Flow (ID: flow123): Status: SUCCESS
- ML Training Flow (ID: flow456): Status: IDLE
```

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
- `erroneous_facet_id`: ID of the facet that caused an error (if any, otherwise null)
- `data`: Additional data from the run
- `timestamp`: When the flow was executed (ISO format)

**Example**:
```json
{
  "flow_name": "Data Processing Flow",
  "status": "SUCCESS",
  "log_id": "log_abc123xyz",
  "user": "user@example.com",
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

**Output**: A formatted string listing all dashboards. Example:

```
Found 2 dashboards:
- Sales Dashboard (ID: dash123)
- Analytics Overview (ID: dash456)
```

Or if not available: `"Dashboards functionality is not available in the current Ikigai API."`

### list_charts

Lists all available charts in the app.

Charts are visualization components in Ikigai that display data in various formats (bar charts, line charts, pie charts, etc.). Charts are typically associated with datasets and can be embedded in dashboards.

**Note**: Charts functionality may not be available in all Ikigai API versions.

**Input**: None

**Output**: A formatted string listing all charts. Example:

```
Found 3 charts:
- Revenue Chart (ID: chart123): Type: bar
- Trends Chart (ID: chart456): Type: line
- Distribution (ID: chart789): Type: pie
```

Or if not available: `"Charts functionality is not available in the current Ikigai API."`

## Resources

The server also exposes the following resources that provide programmatic access to Ikigai components:

### datasets://all

Resource containing all datasets in the app as JSON.

**Output**:
```json
{
  "datasets": [
    {
      "name": "Sales Data",
      "id": "abc123",
      "size": 1500,
      "columns": ["date", "amount", "product"]
    },
    {
      "name": "Customer Info",
      "id": "def456",
      "size": 500,
      "columns": ["name", "email", "signup_date"]
    }
  ]
}
```

**Reference**: [Ikigai Library - Finding a Dataset from an App](https://github.com/ikigailabs-io/ikigai?tab=readme-ov-file#finding-a-dataset-from-an-app)

### flows://all

Resource containing all flows in the app as JSON.

**Output**:
```json
{
  "flows": [
    {
      "name": "Data Processing Flow",
      "id": "flow123"
    },
    {
      "name": "ML Training Flow",
      "id": "flow456"
    }
  ]
}
```

**Reference**: [Ikigai Library - Finding a Flow from an App](https://github.com/ikigailabs-io/ikigai?tab=readme-ov-file#finding-a-flow-from-an-app)

### dashboards://all

Resource containing all dashboards in the app as JSON.

**Output**:
```json
{
  "dashboards": [
    {
      "name": "Sales Dashboard",
      "id": "dash123"
    }
  ]
}
```

Or if dashboards are not available:
```json
{
  "dashboards": [],
  "message": "Dashboards not available"
}
```

**Note**: Dashboards functionality may not be available in all Ikigai API versions.

### charts://all

Resource containing all charts in the app as JSON.

**Output**:
```json
{
  "charts": [
    {
      "name": "Revenue Chart",
      "id": "chart123"
    }
  ]
}
```

Or if charts are not available:
```json
{
  "charts": [],
  "message": "Charts not available"
}
```

**Note**: Charts functionality may not be available in all Ikigai API versions.

## Architecture

This project follows modern Python best practices:

- Uses Hatch for project management and builds
- Type hints throughout
- Structured logging with the `logging` module
- FastMCP for MCP server implementation
- Synchronous tool handlers for simplicity

## License

`mcp-server` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
