# crawl2md

A Python CLI tool that crawls websites using sitemap.xml and converts pages to markdown files.

## Features

- Fetches URLs from sitemap.xml
- Crawls pages concurrently using crawl4ai
- Converts HTML to markdown
- Saves markdown files preserving relative path structure
- Configurable concurrency
- HTML preprocessing with CSS selector-based cleanup

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd crawl2md

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev]"
```

## Usage

Basic usage:

```bash
crawl2md https://example.com
```

This will:
1. Fetch `https://example.com/sitemap.xml`
2. Extract all URLs
3. Crawl pages concurrently (max 5 by default)
4. Save markdown files to `./output/` with the same relative structure

Advanced usage:

```bash
# Custom sitemap URL
crawl2md https://example.com --sitemap https://example.com/custom-sitemap.xml

# Custom output directory
crawl2md https://example.com --output ./my-output

# Adjust concurrency
crawl2md https://example.com --concurrency 10

# HTML preprocessing - remove unwanted elements before conversion
crawl2md https://example.com --clean-selectors-file selectors.txt
```

### HTML Preprocessing

Remove navigation, footer, sidebar, and other unwanted elements before markdown conversion using CSS selectors:

```bash
# Create selectors file (one selector per line, # for comments)
$ cat selectors.txt
# Remove common navigation and footer elements
nav
footer
header
# Remove sidebar by class
.sidebar
# Remove by ID
#nav-header

# Crawl with cleanup
crawl2md https://example.com --clean-selectors-file selectors.txt
```

Supported selectors:
- Tags: `nav`, `footer`, `header`
- Classes: `.sidebar`, `.menu-item`
- IDs: `#header`, `#footer`
- Compound: `article > .content`, `.sidebar li`

## Development

Run tests:

```bash
pytest
pytest tests/test_file_handler.py -v  # Run specific test file
pytest tests/test_file_handler.py::test_url_to_path_root -v  # Run specific test
```

Lint and format code:

```bash
ruff check .
ruff check --fix .
ruff format .
```

Type checking:

```bash
mypy .
```

## Project Structure

```
crawl2md/
├── crawl2md/
│   ├── __init__.py
│   ├── cli.py           # CLI entry point
│   ├── crawler.py       # Async crawl4ai wrapper
│   ├── sitemap.py       # Sitemap parser
│   ├── html_cleaner.py  # HTML preprocessing with CSS selectors
│   ├── cleaner.py       # Markdown cleaner
│   └── file_handler.py  # File operations
├── tests/
│   ├── test_crawler.py
│   ├── test_sitemap.py
│   └── test_file_handler.py
├── main.py
└── pyproject.toml
```

## Roadmap

- [x] HTML preprocessing with CSS selector-based cleanup
- [x] Markdown cleaning (headers, footers, menus)
- [ ] Fix code element rendering issues
- [ ] Progress bar for crawling
- [ ] Resume interrupted crawls
- [ ] Retry failed URLs
- [ ] Sitemap index support
