"""Tests for sitemap parser."""

import pytest
from unittest.mock import Mock, patch

from crawl2md.sitemap import SitemapParser


@pytest.fixture
def sample_sitemap_xml():
    """Sample sitemap XML content."""
    return """<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>https://example.com/</loc>
        </url>
        <url>
            <loc>https://example.com/about</loc>
        </url>
        <url>
            <loc>https://example.com/blog/post-1</loc>
        </url>
    </urlset>
    """


@pytest.fixture
def sample_sitemap_index_xml():
    """Sample sitemap index XML content (should be ignored)."""
    return """<?xml version="1.0" encoding="UTF-8"?>
    <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <sitemap>
            <loc>https://example.com/sitemap1.xml</loc>
        </sitemap>
    </sitemapindex>
    """


def test_get_urls(sample_sitemap_xml):
    """Test extracting URLs from sitemap."""
    with patch("crawl2md.sitemap.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.content = sample_sitemap_xml.encode("utf-8")
        mock_get.return_value = mock_response

        parser = SitemapParser("https://example.com/sitemap.xml")
        urls = parser.get_urls()

        assert len(urls) == 3
        assert "https://example.com/" in urls
        assert "https://example.com/about" in urls
        assert "https://example.com/blog/post-1" in urls


def test_get_urls_empty_sitemap():
    """Test handling empty sitemap."""
    with patch("crawl2md.sitemap.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.content = b"""<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>"""
        mock_get.return_value = mock_response

        parser = SitemapParser("https://example.com/sitemap.xml")
        urls = parser.get_urls()

        assert len(urls) == 0
