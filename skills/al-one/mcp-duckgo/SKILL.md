---
name: mcp-duckgo
description:
  Skills for web search and content scraping.
  Used when users need online searching and web scraping.
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": {"bins": ["npx", "uvx"]}
      }
  }
---

# 技能：执行 Shell 命令

## 网页搜索
- `npx -y mcporter call --stdio 'uvx duckduckgo-mcp-server' search query="{keyword}" max_results=10`

## 网页内容获取
- `npx -y mcporter call --stdio 'uvx duckduckgo-mcp-server' fetch_content url="https://..."`