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

### Basic Usage

```bash
crawl2md https://example.com
```

This will:
1. Fetch `https://example.com/sitemap.xml`
2. Extract all URLs
3. Crawl pages concurrently (max 10 by default)
4. Save markdown files to `./output/` preserving the website structure

### Removing Unwanted Elements (Navigation, Footer, etc.)

Many websites have navigation menus, footers, and sidebars that you don't want in your markdown. You can remove these:

**Step 1: Create a file called `selectors.txt`**

Put this in the same folder where you'll run the command:

```
# Lines starting with # are comments - they get ignored
nav           # Navigation menus
footer        # Site footer
header        # Site header
.sidebar      # Sidebar content (note the dot before sidebar)
#header       # Element with id="header" (note the # before header)
```

**Step 2: Run the crawl with cleanup**

```bash
crawl2md https://example.com --clean-selectors-file selectors.txt
```

### Other Options

```bash
# Custom output directory
crawl2md https://example.com --output ./my-docs

# Custom sitemap URL
crawl2md https://example.com --sitemap https://example.com/custom-sitemap.xml

# Adjust how many pages crawl at once
crawl2md https://example.com --concurrency 5
```

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
├── pyproject.toml         # Package configuration
├── README.md
├── AGENTS.md
├── crawl2md/              # Main package
│   ├── __init__.py
│   ├── cli.py             # Command-line interface
│   ├── crawler.py         # Web crawler
│   ├── sitemap.py         # Sitemap parser
│   ├── html_cleaner.py    # Remove unwanted HTML elements
│   ├── cleaner.py         # Markdown cleaner
│   └── file_handler.py    # Save markdown files
└── tests/                 # Tests
    ├── test_crawler.py
    ├── test_sitemap.py
    └── test_file_handler.py
```

## Roadmap

- [x] HTML preprocessing with CSS selector-based cleanup
- [x] Markdown cleaning (headers, footers, menus)
- [ ] Fix code element rendering issues
- [ ] Progress bar for crawling
- [ ] Resume interrupted crawls
- [ ] Retry failed URLs
- [ ] Sitemap index support
