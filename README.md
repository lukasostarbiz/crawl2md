# crawl2md

A Python CLI tool that crawls websites using sitemap.xml and converts pages to markdown files.

## Features

- Fetches URLs from sitemap.xml
- Crawls pages concurrently using crawl4ai
- Converts HTML to markdown
- Saves markdown files preserving relative path structure
- HTML preprocessing with CSS selector-based cleanup
- Adds frontmatter metadata (source URL, scrape date) for RAG compatibility
- Writes crawl results to CSV file (OK/ERROR status per URL)
- Incremental file saving and progress output (Ctrl+C safe)

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
# Pass the sitemap URL directly as the main argument
crawl2md https://example.com/sitemap.xml
```

This will:
1. Fetch the sitemap from `https://example.com/sitemap.xml`
2. Extract all URLs
3. Crawl pages concurrently (max 10 by default)
4. Save markdown files to `./output/` preserving the website structure
5. Write results to `result.csv`

### Output Files

Each crawled page is saved as a markdown file with frontmatter metadata:

```markdown
---
source: https://example.com/docs/page
scrape_date: 2025-01-22

---

# Page Title

Page content here...
```

A `result.csv` file is also created with crawl status:

```csv
status,url
OK,https://example.com/docs/page1
ERROR,https://example.com/docs/page2
OK,https://example.com/docs/page3
```

### Removing Unwanted Elements (Navigation, Footer, etc.)

Many websites have navigation menus, footers, and sidebars that you don't want in your markdown. You can remove these:

**Step 1: Create a file called `selectors.txt`**

Put this in the same folder where you'll run the command.

- Use standard CSS selectors to select elements to remove
- Lines starting with `#` (with space) or `--` are comments
- Lines starting with `#` without space are ID selectors (e.g., `#header`)

Example `selectors.txt`:
```
# This is a comment
nav           # Navigation menus
footer        # Site footer
.sidebar      # Sidebar content
#header       # Element with id="header"
```

**Step 2: Run the crawl with cleanup**

```bash
crawl2md https://example.com/sitemap.xml --clean-selectors-file ./selectors.txt
```

### Other Options

```bash
# Custom output directory
crawl2md https://example.com/sitemap.xml --output ./my-docs

# Custom result CSV file
crawl2md https://example.com/sitemap.xml --result-file ./crawl-results.csv

# Adjust how many pages crawl at once
crawl2md https://example.com/sitemap.xml --concurrency 5

# Combine multiple options
crawl2md https://example.com/sitemap.xml \
  --clean-selectors-file ./selectors.txt \
  --output ./docs \
  --result-file ./results.csv \
  --concurrency 5
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
├── selectors_kentico.txt  # Kentico-specific selectors (example)
├── crawl2md/              # Main package
│   ├── __init__.py
│   ├── cli.py             # Command-line interface
│   ├── crawler.py         # Web crawler
│   ├── sitemap.py         # Sitemap parser
│   ├── html_cleaner.py    # Remove unwanted HTML elements
│   ├── cleaner.py         # Markdown cleaner and metadata
│   └── file_handler.py    # Save markdown files
└── tests/                 # Tests
    ├── test_crawler.py
    ├── test_sitemap.py
    ├── test_file_handler.py
    └── test_cleaner.py
```

## Roadmap

yeah, as if.

- [x] HTML preprocessing with CSS selector-based cleanup
- [x] Markdown cleaning (headers, footers, menus)
- [x] Frontmatter metadata for RAG compatibility
- [x] Result CSV file with OK/ERROR status
- [ ] Fix code element rendering issues
- [ ] Progress bar for crawling
- [ ] Resume interrupted crawls
- [ ] Retry failed URLs
- [ ] Sitemap index support
