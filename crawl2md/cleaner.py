"""Markdown cleaner module."""

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
        return self.remove_headers_footers_menus(markdown)

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

    def fix_code_elements(self, markdown: str) -> str:
        """Fix issues with code element rendering.

        Args:
            markdown: Markdown content

        Returns:
            Markdown with fixed code elements
        """
        return markdown
