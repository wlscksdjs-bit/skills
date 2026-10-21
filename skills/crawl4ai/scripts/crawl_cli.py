import sys
import asyncio
import json
import argparse
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

async def crawl_webpage(url: str, cache_bypass: bool = True):
    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS if cache_bypass else CacheMode.ENABLED,
        remove_overlay_elements=True,
        word_count_threshold=10
    )
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url, config=config)
        if result.success:
            return result.markdown
        else:
            raise Exception(f"Crawl failed: {result.error_message}")

def main():
    parser = argparse.ArgumentParser(description="Crawl4AI CLI Tool")
    parser.add_argument("url", type=str, help="Target URL to crawl")
    parser.add_argument("--bypass-cache", action="store_true", default=True, help="Bypass cache")
    args = parser.parse_args()

    try:
        markdown_output = asyncio.run(crawl_webpage(args.url, args.bypass_cache))
        print(markdown_output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
