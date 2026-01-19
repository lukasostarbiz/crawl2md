# AGENTS.md

## Build, Lint, and Test Commands

### Setup
```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -e .
```

### Build
```bash
# Install in development mode
pip install -e .
```

### Testing
```bash
# Run all tests
pytest

# Run single test file
pytest path/to/test_file.py

# Run single test function
pytest path/to/test_file.py::test_function_name

# Run tests with coverage
pytest --cov=.

# Run tests matching pattern
pytest -k "test_name_pattern"
```

### Linting and Formatting
```bash
# Run linter
ruff check .

# Format code
ruff format .

# Type checking
mypy .

# Fix linting issues
ruff check --fix .
```

## Code Style Guidelines

### Python Version
- Target Python 3.9+ (as specified in pyproject.toml)
- Use type hints where appropriate

### Imports
- Group imports: standard library, third-party, local application
- Separate groups with blank lines
- Use `ruff` for automatic import sorting
- Avoid `from module import *`

```python
import os
import sys

from typing import Optional

import click

from crawl4ai import AsyncWebCrawler
from crawl2md.sitemap import SitemapParser
from crawl2md.file_handler import FileHandler
from crawl2md.cleaner import MarkdownCleaner
```

### Naming Conventions
- **Functions/variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods**: `_leading_underscore`
- **Module names**: `lowercase_with_underscores`

### Type Hints
- Use type hints for function signatures
- Prefer `Optional[T]` over `T | None` for compatibility
- Use `List[T]`, `Dict[K, V]` for collections (or generic `list`, `dict` for Python 3.9+)

```python
def process_data(items: list[dict[str, Any]]) -> Optional[str]:
    ...
```

### Error Handling
- Use specific exceptions (ValueError, KeyError, etc.)
- Avoid bare `except:` clauses
- Provide meaningful error messages
- Use context managers for resources

```python
try:
    result = some_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    raise
```

### Docstrings
- Use Google-style or NumPy-style docstrings
- Document public functions and classes
- Include Args, Returns, and Raises sections

```python
def clean(self, markdown: str, url: Optional[str] = None) -> str:
    """Clean markdown content.

    Args:
        markdown: Raw markdown content
        url: Source URL (for context)

    Returns:
        Cleaned markdown content
    """
    return self.remove_headers_footers_menus(markdown)
```

### Code Formatting
- Line length: 88-100 characters
- Use f-strings for string formatting
- Prefer list comprehensions over `map`/`filter`
- Use `with` statements for file operations
- Add spaces around operators and after commas

### Markdown Cleaning
- `MarkdownCleaner.clean(markdown, url)` removes headers, footers, and navigation menus
- `MarkdownCleaner.convert_links_to_relative(markdown, base_url)` converts absolute URLs to relative paths for local archive portability
- Anchor links (`#section`) are preserved during link conversion
- External links remain unchanged
- Example: `https://docs.kentico.com/api` → `../api`

### Project Structure
```
crawl2md/
├── main.py               # Entry point
├── crawl2md/
│   ├── __init__.py
│   ├── cli.py           # CLI entry point
│   ├── crawler.py       # Async crawl4ai wrapper
│   ├── sitemap.py       # Sitemap parser
│   ├── cleaner.py       # Markdown cleaner
│   └── file_handler.py  # File operations
├── tests/
│   ├── __init__.py
│   ├── test_crawler.py
│   ├── test_sitemap.py
│   └── test_file_handler.py
└── pyproject.toml
```

### General Principles
- Keep functions focused and small (< 50 lines)
- Write self-documenting code with descriptive names
- Add tests for non-trivial functions
- Avoid premature optimization
- Use logging instead of print statements
- Follow PEP 8 guidelines
