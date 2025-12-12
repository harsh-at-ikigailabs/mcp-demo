"""
Tests for the MCP server.
"""

import pytest
from mcp_server.server import (
    handle_list_datasets,
    handle_list_flows,
    handle_list_dashboards,
    handle_list_charts,
)


@pytest.mark.asyncio
async def test_list_datasets():
    """Test listing datasets."""
    result = await handle_list_datasets()
    assert len(result) > 0
    assert result[0].type == "text"


@pytest.mark.asyncio
async def test_list_flows():
    """Test listing flows."""
    result = await handle_list_flows()
    assert len(result) > 0
    assert result[0].type == "text"


@pytest.mark.asyncio
async def test_list_dashboards():
    """Test listing dashboards."""
    result = await handle_list_dashboards()
    assert len(result) > 0
    assert result[0].type == "text"


@pytest.mark.asyncio
async def test_list_charts():
    """Test listing charts."""
    result = await handle_list_charts()
    assert len(result) > 0
    assert result[0].type == "text"
