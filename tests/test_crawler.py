"""Tests for crawler."""

import pytest
from unittest.mock import AsyncMock, Mock, patch

from crawl2md.crawler import Crawler, MAX_CONCURRENT_CRAWLS


@pytest.mark.asyncio
async def test_crawl_single_success():
    """Test crawling a single URL successfully."""
    with patch("crawl2md.crawler.AsyncWebCrawler") as mock_crawler_class:
        mock_crawler = AsyncMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_crawler

        mock_result = Mock()
        mock_result.success = True
        mock_result.markdown = "# Test Content\n\nSome text"
        mock_crawler.arun.return_value = mock_result

        crawler = Crawler()
        result = await crawler.crawl_single("https://example.com/about")

        assert result["success"] is True
        assert result["url"] == "https://example.com/about"
        assert result["markdown"] == "# Test Content\n\nSome text"


@pytest.mark.asyncio
async def test_crawl_single_failure():
    """Test crawling a single URL with failure."""
    with patch("crawl2md.crawler.AsyncWebCrawler") as mock_crawler_class:
        mock_crawler = AsyncMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_crawler

        mock_result = Mock()
        mock_result.success = False
        mock_result.error_message = "Network error"
        mock_crawler.arun.return_value = mock_result

        crawler = Crawler()
        result = await crawler.crawl_single("https://example.com/about")

        assert result["success"] is False
        assert result["url"] == "https://example.com/about"
        assert result["markdown"] is None
        assert result["error"] == "Network error"


@pytest.mark.asyncio
async def test_crawl_many():
    """Test crawling multiple URLs."""
    with patch("crawl2md.crawler.AsyncWebCrawler") as mock_crawler_class:
        mock_crawler = AsyncMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_crawler

        def create_mock_result(markdown):
            mock_result = Mock()
            mock_result.success = True
            mock_result.markdown = markdown
            return mock_result

        mock_crawler.arun.side_effect = [
            create_mock_result("# Page 1"),
            create_mock_result("# Page 2"),
            create_mock_result("# Page 3"),
        ]

        urls = [
            "https://example.com/page1",
            "https://example.com/page2",
            "https://example.com/page3",
        ]

        crawler = Crawler()
        results = await crawler.crawl_many(urls)

        assert len(results) == 3
        assert all(r["success"] for r in results)
        assert results[0]["markdown"] == "# Page 1"
        assert results[1]["markdown"] == "# Page 2"
        assert results[2]["markdown"] == "# Page 3"


def test_default_max_concurrent():
    """Test default max concurrent value."""
    crawler = Crawler()
    assert crawler.max_concurrent == MAX_CONCURRENT_CRAWLS


def test_custom_max_concurrent():
    """Test custom max concurrent value."""
    crawler = Crawler(max_concurrent=10)
    assert crawler.max_concurrent == 10
