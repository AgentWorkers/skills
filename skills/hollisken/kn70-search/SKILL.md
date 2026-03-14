---
name: search
description: 使用多个搜索引擎（如 Tavily、multi-search-engine 或 SearXNG）在网络上进行搜索。
---
提供使用 Tavily（基于人工智能优化）、多搜索引擎（支持 17 个搜索引擎，无需 API 密钥）或 SearXNG（可自行托管）进行网络搜索的工具。

**使用方法**：
```typescript
// Use Tavily (recommended)
search_web({ query: "AI news", engine: "tavily", max_results: 10 })

// Use multi-search-engine (no API key needed)
search_web({ query: "AI news", engine: "multi", max_results: 10 })

// Use SearXNG (Windows Docker Desktop required)
search_web({ query: "AI news", engine: "searxng", max_results: 10 })
```

**搜索引擎对比**：
| 搜索引擎 | 速度 | 质量 | 成本 | 备注 |
|--------|-------|---------|------|-------|
| tavily | ⚡ 非常快 | ⭐⭐⭐⭐⭐ | 免费（开发者版） | 基于人工智能优化，支持代码片段显示 |
| multi | ⚡ 非常快 | ⭐⭐⭐⭐ | 免费 | 支持 17 个搜索引擎（如百度、必应、谷歌等） |
| searxng | 🐌 速度中等 | ⭐⭐⭐⭐⭐ | 免费 | 需要 Docker Desktop 来运行 |