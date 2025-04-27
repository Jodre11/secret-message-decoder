import pytest
from decoder import decode_secret_message, parse_coordinates, Grid
from requests.exceptions import RequestException

class MockResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code
    
    def raise_for_status(self):
        if self.status_code >= 400:
            raise RequestException(f"HTTP {self.status_code}")

def test_parse_coordinates():
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
            (0, 0): '█',
            (0, 1): '█',
            (0, 2): '█',
            (1, 1): '▀',
            (1, 2): '▀',
            (2, 1): '▀',
            (2, 2): '▀',
            (3, 2): '▀'
        }
        
        # Verify max coordinates
        assert grid.max_x == 3
        assert grid.max_y == 2
        
        # Verify string representation
        assert grid.to_string() == "█▀▀▀\n█▀▀ \n█"
    finally:
        # Restore the original requests.get
        requests.get = original_get

def test_parse_coordinates_empty_document():
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

def test_parse_coordinates_http_error():
    # Mock the requests.get function to raise an error
    import requests
    original_get = requests.get
    requests.get = lambda url: MockResponse("", status_code=404)
    
    try:
        # Verify that the function raises RequestException for HTTP error
        with pytest.raises(RequestException):
            parse_coordinates("https://example.com")
    finally:
        # Restore the original requests.get
        requests.get = original_get

def test_parse_coordinates_invalid_data():
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

def test_decode_secret_message(capsys, snapshot):
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