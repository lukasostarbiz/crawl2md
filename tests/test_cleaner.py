"""Tests for MarkdownCleaner."""

import re
from datetime import datetime

import pytest

from crawl2md.cleaner import MarkdownCleaner


class TestAddMetadata:
    """Tests for add_metadata method."""

    def test_add_metadata_basic(self):
        """Test adding basic frontmatter with source and date."""
        cleaner = MarkdownCleaner()
        markdown = "# Hello World\n\nSome content here."
        source_url = "https://example.com/docs/page"

        result = cleaner.add_metadata(markdown, source_url)

        assert "source: https://example.com/docs/page" in result
        assert "scrape_date:" in result
        assert result.startswith("---")
        assert "# Hello World" in result
        assert "Some content here." in result

    def test_add_metadata_preserves_original(self):
        """Test that original markdown content is preserved."""
        cleaner = MarkdownCleaner()
        markdown = "# Title\n\n## Section\n\nSome content."
        source_url = "https://example.com/page"

        result = cleaner.add_metadata(markdown, source_url)

        assert "# Title" in result
        assert "## Section" in result
        assert "Some content." in result

    def test_add_metadata_format(self):
        """Test frontmatter format is correct YAML."""
        cleaner = MarkdownCleaner()
        markdown = "# Test"
        source_url = "https://example.com/test"

        result = cleaner.add_metadata(markdown, source_url)

        lines = result.split("\n")
        assert lines[0] == "---"
        assert lines[1].startswith("source:")
        assert lines[2].startswith("scrape_date:")
        assert lines[3] == "---"
        assert lines[4] == ""

    def test_add_metadata_with_url_special_chars(self):
        """Test with URLs containing special characters."""
        cleaner = MarkdownCleaner()
        markdown = "# Test"
        source_url = "https://example.com/docs/page?id=123&lang=en"

        result = cleaner.add_metadata(markdown, source_url)

        assert source_url in result

    def test_add_metadata_empty_content(self):
        """Test with empty markdown content."""
        cleaner = MarkdownCleaner()
        markdown = ""
        source_url = "https://example.com/empty"

        result = cleaner.add_metadata(markdown, source_url)

        assert "source: https://example.com/empty" in result
        assert "scrape_date:" in result


class TestClean:
    """Tests for clean method."""

    def test_clean_returns_unchanged(self):
        """Test that clean returns markdown unchanged (cleanup disabled)."""
        cleaner = MarkdownCleaner()
        markdown = "# Title\n\nSome content."

        result = cleaner.clean(markdown)

        assert result == markdown


class TestRemoveHeadersFootersMenus:
    """Tests for remove_headers_footers_menus method."""

    def test_remove_before_first_header(self):
        """Test removal of content before first header."""
        cleaner = MarkdownCleaner()
        markdown = "Some intro text\n# Title"
        expected = "# Title"

        result = cleaner.remove_headers_footers_menus(markdown)

        assert result == expected

    def test_remove_after_footer_marker(self):
        """Test removal after footer marker."""
        cleaner = MarkdownCleaner()
        markdown = "# Title\n\nContent here\n* * *\nFooter text"
        expected = "# Title\n\nContent here"

        result = cleaner.remove_headers_footers_menus(markdown)

        assert result == expected

    def test_no_header_returns_whole_content(self):
        """Test that content without headers is returned as-is."""
        cleaner = MarkdownCleaner()
        markdown = "No headers here, just text."

        result = cleaner.remove_headers_footers_menus(markdown)

        assert result == markdown


class TestConvertLinksToRelative:
    """Tests for convert_links_to_relative method."""

    def test_convert_kentico_links(self):
        """Test conversion of Kentico documentation links.

        Note: This feature is currently disabled in clean().
        The method is preserved for potential future use.
        """
        cleaner = MarkdownCleaner()
        markdown = "[See here](/documentation/developers/admins/customization)"
        base_url = "https://docs.kentico.com"

        result = cleaner.convert_links_to_relative(markdown, base_url)

        # This feature is disabled, so the result should be unchanged
        assert result == markdown
