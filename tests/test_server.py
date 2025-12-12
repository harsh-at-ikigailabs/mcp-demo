"""
Tests for the MCP server.
"""

from mcp_server.server import (
    list_datasets,
    list_flows,
    list_dashboards,
    list_charts,
)


def test_list_datasets():
    """Test listing datasets."""
    # Note: This test requires Ikigai client to be initialized
    # In a real scenario, you would mock the ikigai_app
    result = list_datasets()
    assert isinstance(result, str)
    assert len(result) > 0


def test_list_flows():
    """Test listing flows."""
    # Note: This test requires Ikigai client to be initialized
    # In a real scenario, you would mock the ikigai_app
    result = list_flows()
    assert isinstance(result, str)
    assert len(result) > 0


def test_list_dashboards():
    """Test listing dashboards."""
    # Note: This test requires Ikigai client to be initialized
    # In a real scenario, you would mock the ikigai_app
    result = list_dashboards()
    assert isinstance(result, str)
    assert len(result) > 0


def test_list_charts():
    """Test listing charts."""
    # Note: This test requires Ikigai client to be initialized
    # In a real scenario, you would mock the ikigai_app
    result = list_charts()
    assert isinstance(result, str)
    assert len(result) > 0
