# Secret Message Decoder

A Python tool that decodes secret messages from ASCII art grids defined in Google Docs.

## Features

- Parses ASCII art coordinates from Google Docs
- Efficient character grid generation
- Preserves exact spacing and formatting
- Memory-efficient implementation using generators

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Jodre11/secret-message-decoder.git
cd secret-message-decoder
```

2. Install dependencies:
```bash
poetry install
```

## Usage

```python
from decoder import decode_secret_message

# Decode a message from a Google Doc URL
decode_secret_message("https://docs.google.com/document/d/your-doc-id")
```

## Development

### Running Tests

```bash
poetry run pytest
```

To update test snapshots:
```bash
poetry run pytest pytest --snapshot-update
```

### Project Structure

- `decoder.py`: Main implementation
- `test_decoder.py`: Test suite
- `__snapshots__/`: Test snapshots

## Implementation Details

The decoder uses a memory-efficient approach:
- Generator-based character grid construction
- Minimal string allocations
- Preserves exact spacing and formatting
- Handles large grids efficiently

## License

MIT License 