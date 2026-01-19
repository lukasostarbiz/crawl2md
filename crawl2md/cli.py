"""CLI module for crawl2md."""

import asyncio
from typing import Optional

import click

from crawl2md.crawler import Crawler, MAX_CONCURRENT_CRAWLS
from crawl2md.file_handler import FileHandler
from crawl2md.html_cleaner import HtmlCleaner
from crawl2md.sitemap import SitemapParser
from crawl2md.cleaner import MarkdownCleaner


@click.command()
@click.argument("base_url")
@click.option(
    "--sitemap",
    default=None,
    help="Custom sitemap URL (default: BASE_URL/sitemap.xml)",
)
@click.option(
    "--output",
    default="./output",
    help="Output directory (default: ./output)",
)
@click.option(
    "--concurrency",
    default=MAX_CONCURRENT_CRAWLS,
    help=f"Max concurrent crawls (default: {MAX_CONCURRENT_CRAWLS})",
)
@click.option(
    "--clean-selectors-file",
    default=None,
    help="File with CSS selectors to remove (one per line, # for comments)",
)
def main(
    base_url: str,
    sitemap: Optional[str],
    output: str,
    concurrency: int,
    clean_selectors_file: Optional[str],
) -> None:
    """Crawl a website and convert pages to markdown.

    Downloads all pages from a website's sitemap.xml and saves them as markdown files.
    """
    if not sitemap:
        sitemap = f"{base_url.rstrip('/')}/sitemap.xml"

    click.echo(f"Crawling {base_url}")
    click.echo(f"Sitemap: {sitemap}")
    click.echo(f"Output: {output}")
    click.echo(f"Concurrency: {concurrency}")
    if clean_selectors_file:
        click.echo(f"Clean selectors file: {clean_selectors_file}")
    click.echo("-" * 50)

    sitemap_parser = SitemapParser(sitemap)
    html_cleaner = (
        HtmlCleaner.from_file(clean_selectors_file) if clean_selectors_file else None
    )
    crawler = Crawler(max_concurrent=concurrency, html_cleaner=html_cleaner)
    file_handler = FileHandler(base_url, output)
    cleaner = MarkdownCleaner()

    try:
        click.echo("Fetching sitemap...")
        urls = sitemap_parser.get_urls()
        # urls = [
        #     "https://docs.kentico.com/documentation/developers-and-admins/customization/handle-global-events/handle-object-events",
        #     "https://docs.kentico.com/documentation/developers-and-admins/customization/handle-global-events/handle-form-events",
        #     "https://docs.kentico.com/documentation/developers-and-admins/customization/object-types/extend-system-object-types",
        #     "https://docs.kentico.com/documentation/developers-and-admins/api/objectquery-api",
        #     "https://docs.kentico.com/documentation/developers-and-admins/development/content-types/reusable-field-schemas",
        #     "https://docs.kentico.com/documentation/developers-and-admins/development/content-types/management-api",
        #     "https://docs.kentico.com/documentation/developers-and-admins/development/routing/content-tree-based-routing/set-up-content-tree-based-routing",
        # ]
        click.echo(f"Found {len(urls)} URLs in sitemap")
        click.echo("-" * 50)

        click.echo("Crawling pages...")
        results = asyncio.run(crawler.crawl_many(urls))

        success_count = 0
        fail_count = 0

        for result in results:
            if result["success"]:
                markdown = result["markdown"]
                cleaned_markdown = cleaner.clean(markdown, base_url)
                file_handler.save_markdown(result["url"], cleaned_markdown)
                click.echo(f"✓ {result['url']}")
                success_count += 1
            else:
                click.echo(
                    f"✗ {result['url']} - {result.get('error', 'Unknown error')}"
                )
                fail_count += 1

        click.echo("-" * 50)
        click.echo(f"Complete! Success: {success_count}, Failed: {fail_count}")
        click.echo(f"Markdown files saved to: {output}")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise


if __name__ == "__main__":
    main()
