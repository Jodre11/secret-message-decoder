"""Tests for the secret message decoder module."""

from decoder import decode_secret_message, parse_coordinates
import pytest
from requests.exceptions import RequestException


class MockResponse:
    """Mock response object for testing HTTP requests."""

    def __init__(self, text, status_code=200):
        """Initialize a mock response with text and status code."""
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        """Raise RequestException if status code indicates an error."""
        if self.status_code >= 400:
            raise RequestException(f"HTTP {self.status_code}")


def test_parse_coordinates_valid():
    """Test parsing coordinates from a valid document."""
    # Mock HTML content that represents the letter 'F'
    mock_html = """
    <table>
        <tr><td>x-coordinate</td><td>Character</td><td>y-coordinate</td></tr>
        <tr><td>0</td><td>█</td><td>0</td></tr>
        <tr><td>0</td><td>█</td><td>1</td></tr>
        <tr><td>0</td><td>█</td><td>2</td></tr>
        <tr><td>1</td><td>▀</td><td>1</td></tr>
        <tr><td>1</td><td>▀</td><td>2</td></tr>
        <tr><td>2</td><td>▀</td><td>1</td></tr>
        <tr><td>2</td><td>▀</td><td>2</td></tr>
        <tr><td>3</td><td>▀</td><td>2</td></tr>
    </table>
    """

    # Mock the requests.get function
    import requests

    original_get = requests.get
    requests.get = lambda url: MockResponse(mock_html)

    try:
        # Call the function
        grid = parse_coordinates("https://example.com")

        # Verify the coordinates
        assert grid.coordinates == {
            (0, 0): "█",
            (0, 1): "█",
            (0, 2): "█",
            (1, 1): "▀",
            (1, 2): "▀",
            (2, 1): "▀",
            (2, 2): "▀",
            (3, 2): "▀",
        }

        # Verify max coordinates
        assert grid.max_x == 3
        assert grid.max_y == 2

        # Verify string representation
        assert grid.to_string() == "█▀▀▀\n█▀▀ \n█   "
    finally:
        # Restore the original requests.get
        requests.get = original_get


def test_parse_coordinates_no_table():
    """Test parsing coordinates when no table is found."""
    # Mock empty HTML content
    mock_html = "<html><body></body></html>"

    # Mock the requests.get function
    import requests

    original_get = requests.get
    requests.get = lambda url: MockResponse(mock_html)

    try:
        # Verify that the function raises ValueError for empty document
        with pytest.raises(ValueError, match="No table found in the document"):
            parse_coordinates("https://example.com")
    finally:
        # Restore the original requests.get
        requests.get = original_get


def test_parse_coordinates_invalid_data():
    """Test parsing coordinates with invalid data."""
    # Mock HTML content with invalid coordinate data
    mock_html = """
    <table>
        <tr><td>x-coordinate</td><td>Character</td><td>y-coordinate</td></tr>
        <tr><td>not a number</td><td>█</td><td>0</td></tr>
    </table>
    """

    # Mock the requests.get function
    import requests

    original_get = requests.get
    requests.get = lambda url: MockResponse(mock_html)

    try:
        # Verify that the function raises ValueError for invalid data
        with pytest.raises(ValueError, match="Invalid coordinate data"):
            parse_coordinates("https://example.com")
    finally:
        # Restore the original requests.get
        requests.get = original_get


def test_parse_coordinates_missing_columns():
    """Test parsing coordinates with missing columns."""
    # Mock HTML content with missing columns
    mock_html = """
    <table>
        <tr><td>x-coordinate</td><td>Character</td></tr>
        <tr><td>0</td><td>█</td></tr>
        <tr><td>0</td><td>█</td></tr>
        <tr><td>0</td><td>█</td></tr>
        <tr><td>1</td><td>▀</td></tr>
        <tr><td>1</td><td>▀</td></tr>
        <tr><td>2</td><td>▀</td></tr>
        <tr><td>2</td><td>▀</td></tr>
        <tr><td>3</td><td>▀</td></tr>
    </table>
    """

    # Mock the requests.get function
    import requests

    original_get = requests.get
    requests.get = lambda url: MockResponse(mock_html)

    try:
        # Verify that the function raises ValueError for missing columns
        with pytest.raises(ValueError, match="Missing columns in the table"):
            parse_coordinates("https://example.com")
    finally:
        # Restore the original requests.get
        requests.get = original_get


def test_decode_secret_message(capsys, snapshot):
    """Test decoding and printing a secret message."""
    # Mock URL for testing
    test_url = "https://docs.google.com/document/d/test"

    # Mock HTML content that represents the letter 'F'
    mock_html = """
    <table>
        <tr><td>x-coordinate</td><td>Character</td><td>y-coordinate</td></tr>
        <tr><td>0</td><td>█</td><td>0</td></tr>
        <tr><td>0</td><td>█</td><td>1</td></tr>
        <tr><td>0</td><td>█</td><td>2</td></tr>
        <tr><td>1</td><td>▀</td><td>1</td></tr>
        <tr><td>1</td><td>▀</td><td>2</td></tr>
        <tr><td>2</td><td>▀</td><td>1</td></tr>
        <tr><td>2</td><td>▀</td><td>2</td></tr>
        <tr><td>3</td><td>▀</td><td>2</td></tr>
    </table>
    """

    # Mock the requests.get function
    import requests

    original_get = requests.get
    requests.get = lambda url: MockResponse(mock_html)

    try:
        # Call the function
        decode_secret_message(test_url)

        # Capture the output
        captured = capsys.readouterr()
        output = captured.out.strip()

        # Verify against snapshot
        assert output == snapshot
    finally:
        # Restore the original requests.get
        requests.get = original_get


def test_empty_document():
    # Mock URL for testing
    test_url = "https://docs.google.com/document/d/test"

    # Mock empty HTML content
    mock_html = "<html><body></body></html>"

    # Mock the requests.get function
    import requests

    original_get = requests.get
    requests.get = lambda url: MockResponse(mock_html)

    try:
        # Verify that the function raises ValueError for empty document
        with pytest.raises(ValueError, match="No table found in the document"):
            decode_secret_message(test_url)
    finally:
        # Restore the original requests.get
        requests.get = original_get
