---
name: crawl4ai
description: Web crawling, scraping, and clean markdown extraction tool powered by Crawl4AI. Use this skill whenever you need to crawl web pages, extract AI-friendly Markdown, inspect links/media, or run Crawl4AI via CLI/MCP server.
---

# Crawl4AI Skill

High-performance, LLM-friendly web crawling & scraping skill built on top of [Crawl4AI](https://github.com/unclecode/crawl4ai).

## Capabilities
- **Web Crawling**: Crawls static and dynamic (JS-rendered) web pages.
- **Clean Markdown Output**: Automatically strips ads, popups, headers/footers to produce token-efficient Markdown for LLM consumption.
- **Link & Media Inspection**: Extracts internal/external links and image/video metadata.
- **MCP Server Integration**: Can be run as a standard FastMCP server (`mcp_server.py`).

## Quick CLI Usage

Run the Python CLI helper script:

```bash
python C:\Users\JIN\.gemini\config\skills\crawl4ai\scripts\crawl_cli.py "https://example.com"
```

## FastMCP Server Usage

To launch the MCP server via stdio:

```bash
python C:\Users\JIN\.gemini\config\skills\crawl4ai\scripts\mcp_server.py
```

### MCP Client Config (`mcpServers`)

Add to your MCP client config file (e.g. Claude Desktop, VSCode MCP, Antigravity MCP settings):

```json
{
  "mcpServers": {
    "crawl4ai": {
      "command": "python",
      "args": [
        "C:\\Users\\JIN\\.gemini\\config\\skills\\crawl4ai\\scripts\\mcp_server.py"
      ]
    }
  }
}
```

## Exposed MCP Tools

1. **`crawl_webpage(url: str, bypass_cache: bool = True)`**
   - Crawls the URL and returns cleaned Markdown content.
2. **`crawl_and_extract_links(url: str)`**
   - Crawls the URL and returns a summary of internal/external links and media along with markdown snippets.
