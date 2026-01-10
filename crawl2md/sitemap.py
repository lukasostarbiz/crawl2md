"""Sitemap parser module."""

import xml.etree.ElementTree as ET
from typing import List

import requests


class SitemapParser:
    """Parse sitemap.xml files to extract URLs."""

    def __init__(self, sitemap_url: str):
        """Initialize the sitemap parser.

        Args:
            sitemap_url: URL of the sitemap.xml file
        """
        self.sitemap_url = sitemap_url

    def get_urls(self) -> List[str]:
        """Extract all URLs from the sitemap.

        Returns:
            List of absolute URLs found in the sitemap

        Raises:
            requests.RequestException: If fetching the sitemap fails
            ET.ParseError: If parsing the XML fails
        """
        response = requests.get(self.sitemap_url, timeout=30)
        response.raise_for_status()

        root = ET.fromstring(response.content)

        urls = []
        namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

        for url_element in root.findall(".//ns:url/ns:loc", namespace):
            if url_element.text:
                urls.append(url_element.text.strip())

        return urls
