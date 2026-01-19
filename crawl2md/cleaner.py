"""Markdown cleaner module."""

import re
from typing import Optional


class MarkdownCleaner:
    """Clean markdown content by removing unwanted elements."""

    def clean(self, markdown: str, url: Optional[str] = None) -> str:
        """Clean markdown content.

        Args:
            markdown: Raw markdown content
            url: Source URL (for context)

        Returns:
            Cleaned markdown content
        """
        markdown = self.remove_headers_footers_menus(markdown)
        if url:
            markdown = self.convert_links_to_relative(markdown, url)
        return markdown

    def remove_headers_footers_menus(self, markdown: str) -> str:
        """Remove headers, footers, and navigation menus.

        Args:
            markdown: Markdown content

        Returns:
            Markdown with headers/footers/menus removed
        """
        first_header = markdown.find("#")

        if first_header == -1:
            content = markdown
        else:
            content = markdown[first_header:].lstrip()

        footer_pos = content.find("* * *")
        if footer_pos != -1:
            content = content[:footer_pos]

        return content.rstrip()

    def convert_links_to_relative(self, markdown: str, base_url: str) -> str:
        """Convert absolute URLs to relative paths for local archive support.

        Args:
            markdown: Raw markdown content
            base_url: Base URL of the website (e.g., https://docs.kentico.com/)

        Returns:
            Markdown with absolute URLs converted to relative paths
        """
        base_url = base_url.rstrip("/")
        pattern = r"\[([^\]]+)\]\(https://docs\.kentico\.com/([^\)]+)\)"

        def replace_link(match):
            text = match.group(1)
            url = match.group(2)
            relative_path = url.replace(f"https://{base_url}/", "", 1)
            return f"[{text}]({relative_path})"

        result = re.sub(pattern, replace_link, markdown)

        return result
