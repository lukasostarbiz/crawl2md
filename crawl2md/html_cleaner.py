"""HTML cleaning module using BeautifulSoup."""

from pathlib import Path
from typing import List, Optional

from bs4 import BeautifulSoup


class HtmlCleaner:
    """Remove HTML elements based on CSS selectors before markdown conversion."""

    def __init__(self, selectors: Optional[List[str]] = None):
        """Initialize the cleaner.

        Args:
            selectors: List of CSS selectors to remove (with their content)
        """
        self.selectors = selectors or []

    @classmethod
    def from_file(cls, file_path: str) -> "HtmlCleaner":
        """Load selectors from a text file.

        Each non-empty, non-comment line is treated as a CSS selector.
        Lines starting with "# " (with space) or "--" are comments.
        Lines starting with "#" without space (e.g., "#header") are ID selectors.

        Args:
            file_path: Path to the selectors file

        Returns:
            HtmlCleaner instance with loaded selectors
        """
        selectors = []
        path = Path(file_path)
        for line in path.read_text().splitlines():
            stripped = line.strip()
            if stripped and not (
                stripped.startswith("# ") or stripped.startswith("--")
            ):
                selectors.append(stripped)
        return cls(selectors=selectors)

    def clean(self, html: str) -> str:
        """Remove elements matching configured selectors from HTML.

        Args:
            html: Raw HTML string

        Returns:
            Cleaned HTML with matching elements removed
        """
        if not self.selectors:
            return html

        soup = BeautifulSoup(html, "html.parser")

        for selector in self.selectors:
            try:
                for element in soup.select(selector):
                    element.decompose()
            except Exception:
                pass

        return str(soup)
