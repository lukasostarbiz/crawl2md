"""File handler module for saving markdown files."""

import os
from urllib.parse import urlparse



class FileHandler:
    """Handle conversion of URLs to file paths and saving markdown files."""

    def __init__(self, base_url: str, output_dir: str = "./output"):
        """Initialize the file handler.

        Args:
            base_url: Base URL of the website
            output_dir: Directory to save markdown files
        """
        self.base_url = base_url.rstrip("/")
        self.output_dir = output_dir

    def url_to_path(self, url: str) -> str:
        """Convert a URL to a relative file path.

        Args:
            url: Absolute URL to convert

        Returns:
            Relative path from base URL, with .md extension
        """
        parsed = urlparse(url)
        path = parsed.path

        path = path.rstrip("/")

        if not path:
            path = "/index"
        elif path.endswith(".html") or path.endswith(".htm"):
            path = path[:-5]

        path = path.lstrip("/")

        return f"{path}.md"

    def get_output_path(self, url: str) -> str:
        """Get the full output path for a URL.

        Args:
            url: Absolute URL

        Returns:
            Absolute path where the markdown file should be saved
        """
        relative_path = self.url_to_path(url)
        return os.path.join(self.output_dir, relative_path)

    def save_markdown(self, url: str, markdown: str) -> str:
        """Save markdown content to a file.

        Args:
            url: Source URL
            markdown: Markdown content to save

        Returns:
            Path where the file was saved

        Raises:
            OSError: If unable to create directories or write file
        """
        output_path = self.get_output_path(url)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown)

        return output_path
