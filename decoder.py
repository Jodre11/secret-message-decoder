"""Module for decoding secret messages from ASCII art grids in Google Docs."""

from dataclasses import dataclass
from typing import Dict, Generator, Tuple

from bs4 import BeautifulSoup
import requests
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
        """Initialize the grid with coordinates and dimensions."""
        self.coordinates = coordinates
        self.max_x = max_x
        self.max_y = max_y

    def get_char(self, x: int, y: int) -> str:
        """Get the character at the specified coordinates, or space if none exists."""
        return self.coordinates.get((x, y), " ")

    def __char_generator(self) -> Generator[str, None, None]:
        """Generator that yields characters row by row, top to bottom."""
        for y in range(self.max_y, -1, -1):
            for x in range(self.max_x + 1):
                yield self.get_char(x, y)
            if y > 0:  # Don't add newline after last row
                yield "\n"

    def to_string(self) -> str:
        """Convert the grid to a string representation."""
        return "".join(self.__char_generator())


def parse_coordinates(doc_url: str) -> Grid:
    """Parse coordinates and characters from a Google Doc URL.

    Args:
        doc_url (str): URL of the Google Doc containing the character coordinates

    Returns:
        Grid: A Grid object containing the parsed coordinates and dimensions

    Raises:
        ValueError: If no table is found in the document or if columns are missing
        RequestException: If there's an error fetching the document
    """
    try:
        # Fetch the document content
        response = requests.get(doc_url)
        response.raise_for_status()  # Raise exception for bad status codes
    except RequestException as e:
        raise RequestException(f"Failed to fetch document: {e}") from e

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the table in the document
    table = soup.find("table")
    if not table:
        raise ValueError("No table found in the document")

    coordinates: Dict[Tuple[int, int], str] = {}
    max_x = 0
    max_y = 0

    # Skip the header row
    rows = table.find_all("tr")[1:]
    for row in rows:
        cols = row.find_all("td")
        if len(cols) != 3:
            raise ValueError("Missing columns in the table")

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
    """Decodes a secret message from a Google Doc containing character coordinates.

    Args:
        doc_url (str): URL of the Google Doc containing the character coordinates

    Returns:
        None: Prints the decoded message to stdout
    """
    grid = parse_coordinates(doc_url)
    print(grid.to_string())


if __name__ == "__main__":
    # Example usage
    example_url = "https//some:url"  # noqa: E501
    decode_secret_message(example_url)
