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

### Recommended Tools to Add
Add these to `pyproject.toml` for development:
```toml
[project.optional-dependencies]
dev = ["pytest", "pytest-cov", "ruff", "mypy"]
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
# Run linter (if using ruff)
ruff check .

# Format code (if using ruff)
ruff format .

# Type checking (if using mypy)
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
- Use `isort` or `ruff` for automatic import sorting
- Avoid `from module import *`

```python
import os
import sys

from typing import Optional

import requests

from crawl2md.utils import helper_func
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
def calculate_total(prices: list[float]) -> float:
    """Calculate the sum of all prices.

    Args:
        prices: List of prices to sum.

    Returns:
        The total sum.

    Raises:
        ValueError: If prices list is empty.
    """
```

### Code Formatting
- Line length: 88-100 characters
- Use f-strings for string formatting
- Prefer list comprehensions over `map`/`filter`
- Use `with` statements for file operations
- Add spaces around operators and after commas

### Project Structure
```
crawl2md/
├── main.py           # Entry point
├── crawl2md/
│   ├── __init__.py
│   ├── core.py
│   └── utils/
├── tests/
│   ├── __init__.py
│   └── test_core.py
└── pyproject.toml
```

### General Principles
- Keep functions focused and small (< 50 lines)
- Write self-documenting code with descriptive names
- Add tests for non-trivial functions
- Avoid premature optimization
- Use logging instead of print statements
- Follow PEP 8 guidelines
