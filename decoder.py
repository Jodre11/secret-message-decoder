import requests
from bs4 import BeautifulSoup
from typing import Dict, Tuple
from dataclasses import dataclass
from requests.exceptions import RequestException

@dataclass
class Coordinate:
    """Represents a single coordinate in the ASCII art grid."""
    x: int
    y: int
    char: str

class Grid:
    """Represents the ASCII art grid with its dimensions and characters."""
    def __init__(self, coordinates: Dict[Tuple[int, int], str], max_x: int, max_y: int):
        self.coordinates = coordinates
        self.max_x = max_x
        self.max_y = max_y
    
    def get_char(self, x: int, y: int) -> str:
        """Get the character at the specified coordinates, or space if none exists."""
        return self.coordinates.get((x, y), ' ')
    
    def to_string(self) -> str:
        """Convert the grid to a string representation."""
        rows = []
        for y in range(self.max_y, -1, -1):
            row = ''.join(self.get_char(x, y) for x in range(self.max_x + 1))
            # Only strip trailing spaces from the first and last rows
            if y == self.max_y or y == 0:
                row = row.rstrip()
            rows.append(row)
        return '\n'.join(rows)

def parse_coordinates(doc_url: str) -> Grid:
    """
    Parse coordinates and characters from a Google Doc URL.
    
    Args:
        doc_url (str): URL of the Google Doc containing the character coordinates
        
    Returns:
        Grid: A Grid object containing the parsed coordinates and dimensions
        
    Raises:
        ValueError: If no table is found in the document
        RequestException: If there's an error fetching the document
        
    Example:
        >>> grid = parse_coordinates("https://example.com/doc")
    """
    try:
        # Fetch the document content
        response = requests.get(doc_url)
        response.raise_for_status()  # Raise exception for bad status codes
    except RequestException as e:
        raise RequestException(f"Failed to fetch document: {e}") from e
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table in the document
    table = soup.find('table')
    if not table:
        raise ValueError("No table found in the document")
    
    coordinates: Dict[Tuple[int, int], str] = {}
    max_x = 0
    max_y = 0
    
    # Skip the header row
    rows = table.find_all('tr')[1:]
    for row in rows:
        cols = row.find_all('td')
        if len(cols) != 3:
            continue
            
        try:
            x = int(cols[0].text.strip())
            char = cols[1].text.strip()
            y = int(cols[2].text.strip())
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid coordinate data in row: {e}") from e
        
        coordinates[(x, y)] = char
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    
    return Grid(coordinates, max_x, max_y)

def decode_secret_message(doc_url: str) -> None:
    """
    Decodes a secret message from a Google Doc containing character coordinates.
    
    Args:
        doc_url (str): URL of the Google Doc containing the character coordinates
        
    Example:
        >>> decode_secret_message("https://example.com/doc")
        █▀▀▀
        █▀▀ 
        █
    """
    grid = parse_coordinates(doc_url)
    print(grid.to_string())

if __name__ == "__main__":
    # Example usage
    example_url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
    decode_secret_message(example_url) 