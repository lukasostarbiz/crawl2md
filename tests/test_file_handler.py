"""Tests for file handler."""

import os
import tempfile
import shutil

import pytest

from crawl2md.file_handler import FileHandler


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_url_to_path_root():
    """Test converting root URL to path."""
    handler = FileHandler("https://example.com")
    path = handler.url_to_path("https://example.com/")
    assert path == "index.md"


def test_url_to_path_simple():
    """Test converting simple URL to path."""
    handler = FileHandler("https://example.com")
    path = handler.url_to_path("https://example.com/about")
    assert path == "about.md"


def test_url_to_path_nested():
    """Test converting nested URL to path."""
    handler = FileHandler("https://example.com")
    path = handler.url_to_path("https://example.com/blog/post-1")
    assert path == "blog/post-1.md"


def test_url_to_path_with_html():
    """Test converting URL with .html extension."""
    handler = FileHandler("https://example.com")
    path = handler.url_to_path("https://example.com/page.html")
    assert path == "page.md"


def test_url_to_path_with_trailing_slash():
    """Test converting URL with trailing slash."""
    handler = FileHandler("https://example.com")
    path = handler.url_to_path("https://example.com/docs/")
    assert path == "docs.md"


def test_url_to_path_with_query_params():
    """Test converting URL with query parameters."""
    handler = FileHandler("https://example.com")
    path = handler.url_to_path("https://example.com/search?q=test")
    assert path == "search.md"


def test_get_output_path(temp_dir):
    """Test getting full output path."""
    handler = FileHandler("https://example.com", temp_dir)
    path = handler.get_output_path("https://example.com/about")
    assert path == os.path.join(temp_dir, "about.md")


def test_save_markdown(temp_dir):
    """Test saving markdown file."""
    handler = FileHandler("https://example.com", temp_dir)
    markdown_content = "# Test Heading\n\nTest content"

    saved_path = handler.save_markdown("https://example.com/about", markdown_content)

    expected_path = os.path.join(temp_dir, "about.md")
    assert saved_path == expected_path
    assert os.path.exists(expected_path)

    with open(expected_path, "r", encoding="utf-8") as f:
        assert f.read() == markdown_content


def test_save_markdown_creates_directories(temp_dir):
    """Test that save_markdown creates necessary directories."""
    handler = FileHandler("https://example.com", temp_dir)
    markdown_content = "# Test"

    handler.save_markdown("https://example.com/blog/post-1", markdown_content)

    expected_path = os.path.join(temp_dir, "blog", "post-1.md")
    assert os.path.exists(expected_path)
