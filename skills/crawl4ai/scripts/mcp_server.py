import asyncio
import sys
from fastmcp import FastMCP
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

mcp = FastMCP("crawl4ai-mcp", description="Crawl4AI MCP Server for web scraping and clean markdown extraction")

@mcp.tool()
async def crawl_webpage(url: str, bypass_cache: bool = True) -> str:
    """
    Crawls a target webpage URL using Crawl4AI and returns cleaned Markdown content suitable for LLMs.
    
    Args:
        url: Target web page URL to crawl (e.g. 'https://docs.crawl4ai.com')
        bypass_cache: Whether to bypass cached result (default: True)
    """
    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS if bypass_cache else CacheMode.ENABLED,
        remove_overlay_elements=True,
        word_count_threshold=10
    )
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url, config=config)
        if result.success:
            return result.markdown
        else:
            return f"Error crawling {url}: {result.error_message}"

@mcp.tool()
async def crawl_and_extract_links(url: str) -> str:
    """
    Crawls a webpage URL and extracts internal/external links and media assets.
    
    Args:
        url: Target web page URL
    """
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        if result.success:
            links_summary = {
                "internal_links_count": len(result.links.get("internal", [])),
                "external_links_count": len(result.links.get("external", [])),
                "internal_sample": [link["href"] for link in result.links.get("internal", [])[:10]],
                "external_sample": [link["href"] for link in result.links.get("external", [])[:10]],
                "media_images_count": len(result.media.get("images", []))
            }
            return f"Markdown (Truncated):\n{result.markdown[:500]}\n\nLinks & Media Summary:\n{links_summary}"
        else:
            return f"Error: {result.error_message}"

if __name__ == "__main__":
    mcp.run()
