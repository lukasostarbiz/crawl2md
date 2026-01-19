"""Crawler module using crawl4ai."""

import asyncio
from typing import List

from crawl4ai import AsyncWebCrawler, CacheMode, CrawlerRunConfig


MAX_CONCURRENT_CRAWLS = 10


class Crawler:
    """Async web crawler using crawl4ai."""

    def __init__(
        self,
        max_concurrent: int = MAX_CONCURRENT_CRAWLS,
        html_cleaner=None,
    ):
        """Initialize the crawler.

        Args:
            max_concurrent: Maximum number of concurrent crawl operations
            html_cleaner: Optional HtmlCleaner instance for preprocessing HTML
        """
        self.max_concurrent = max_concurrent
        self.html_cleaner = html_cleaner

    async def crawl_single(self, url: str) -> dict:
        """Crawl a single URL and extract markdown.

        Args:
            url: URL to crawl

        Returns:
            Dictionary with 'url', 'markdown', and 'success' keys
        """
        try:
            async with AsyncWebCrawler() as crawler:
                result = await crawler.arun(
                    url=url, config=CrawlerRunConfig(cache_mode=CacheMode.BYPASS)
                )

                if result.success:
                    raw_html = result.html
                    if self.html_cleaner and raw_html:
                        cleaned_html = self.html_cleaner.clean(raw_html)
                        raw_result = await crawler.arun(
                            url=f"raw:{cleaned_html}",
                            config=CrawlerRunConfig(cache_mode=CacheMode.BYPASS),
                        )
                        if raw_result.success:
                            markdown = (
                                raw_result.markdown
                                if isinstance(raw_result.markdown, str)
                                else raw_result.markdown.raw_markdown
                            )
                            return {"url": url, "markdown": markdown, "success": True}
                    markdown = (
                        result.markdown
                        if isinstance(result.markdown, str)
                        else result.markdown.raw_markdown
                    )
                    return {"url": url, "markdown": markdown, "success": True}
                else:
                    return {
                        "url": url,
                        "markdown": None,
                        "success": False,
                        "error": result.error_message,
                    }
        except Exception as e:
            return {"url": url, "markdown": None, "success": False, "error": str(e)}

    async def crawl_many(self, urls: List[str]) -> List[dict]:
        """Crawl multiple URLs concurrently.

        Args:
            urls: List of URLs to crawl

        Returns:
            List of result dictionaries
        """
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def crawl_with_limit(url: str) -> dict:
            async with semaphore:
                return await self.crawl_single(url)

        tasks = [crawl_with_limit(url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results
