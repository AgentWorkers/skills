---
name: anydocs
description: 通用文档索引与搜索功能：能够对任何类型的文档网站（单页应用/静态网站）进行索引，并实现即时搜索。
tools:
  - name: anydocs_search
    description: Search indexed documentation profiles. Returns ranked results with snippets.
    parameters:
      type: object
      properties:
        query:
          type: string
          description: Search query (keyword or phrase)
        profile:
          type: string
          description: Profile name (e.g. 'discord', 'openclaw')
        limit:
          type: number
          description: Max results to return (default 5)
      required: [query]
  - name: anydocs_index
    description: Build or update the search index for a documentation profile.
    parameters:
      type: object
      properties:
        profile:
          type: string
          description: Profile name to index
        use_browser:
          type: boolean
          description: Use browser rendering for SPAs (requires gateway token)
      required: [profile]
  - name: anydocs_config
    description: Configure a new documentation profile.
    parameters:
      type: object
      properties:
        profile:
          type: string
          description: Profile name
        base_url:
          type: string
          description: Base URL of the docs
        sitemap_url:
          type: string
          description: URL to sitemap.xml
      required: [profile, base_url, sitemap_url]
---

# anydocs - 通用文档索引与搜索工具

anydocs 是一个功能强大且可重用的工具，用于索引和搜索 **任何** 文档网站。

## 主要功能

anydocs 解决了一个实际问题：让用户能够从代码或命令行（CLI）直接访问文档。无需每次都打开浏览器，用户可以：
- **索引** 任何文档网站（如 Discord、OpenClaw、内部文档等）；
- **立即从命令行或 Python API 进行搜索**；
- **在本地缓存页面内容，以避免重复的网络请求**；
- **为不同的文档网站配置多个搜索设置**。

## 使用场景

当您需要以下场景时，可以使用 anydocs：
- 在不离开终端的情况下快速查找 API 文档；
- 构建需要引用文档的自动化脚本（agents）；
- 从文档中提取特定信息；
- 在多个文档网站之间进行搜索；
- 将文档集成到您的工作流程中。

## 关键特性

### 🔍 多种搜索方式
- **关键词搜索**：基于 BM25 算法的快速匹配；
- **混合搜索**：结合关键词和短语相似度来提高搜索准确性；
- **正则表达式搜索**：为高级用户提供强大的模式匹配功能。

### 🌐 支持任意文档网站
- 通过标准 XML 网站地图（sitemap）发现文档内容；
- 在无法访问网站地图时，从基础 URL 进行爬取；
- 能够智能地提取 HTML 内容；
- 实施自动速率限制，以保护服务器资源。

### 💾 智能缓存
- 页面内容以 JSON 格式本地缓存，缓存有效期为 7 天（可配置）；
- 搜索索引也被缓存，以便快速再次搜索；
- 提供缓存统计信息和清除缓存的功能；
- 支持缓存失效机制。

### ⚙️ 基于配置文件的设置
- 可同时支持多个文档网站；
- 每个网站可以配置不同的搜索方法和缓存策略；
- 配置信息存储在 `~/.anydocs/config.json` 文件中；
- 提供了针对 Discord、OpenClaw 和自定义网站的配置示例。

### 🌐 JavaScript 渲染（可选）
- 使用 Playwright 渲染客户端单页应用（SPA）；
- 能够自动识别依赖 JavaScript 的网站（如 Discord 文档）；
- 当 Playwright 无法使用时，会自动切换到标准 HTTP 请求方式；
- 可以针对每次搜索会话或整个配置文件进行个性化设置。

## 安装

```bash
cd /path/to/skills/anydocs
pip install -r requirements.txt
chmod +x anydocs.py
```

### （可选）：针对依赖 JavaScript 的网站的浏览器渲染

对于使用客户端渲染的网站（如 Discord），请安装 Playwright：

```bash
pip install playwright==1.40.0
playwright install  # Downloads Chromium
```

如果 Playwright 无法使用，anydocs 会自动切换到标准 HTTP 请求方式。

## 快速入门

### 1. 配置文档网站
```bash
python anydocs.py config vuejs \
  https://vuejs.org \
  https://vuejs.org/sitemap.xml
```

### 2. 构建索引
```bash
python anydocs.py index vuejs
```

anydocs 会通过网站地图发现所有页面，抓取内容并构建可搜索的索引。

### 3. 进行搜索
```bash
python anydocs.py search "composition api" --profile vuejs
python anydocs.py search "reactivity" --profile vuejs --limit 5
```

### 4. 获取特定页面
```bash
python anydocs.py fetch "guide/introduction" --profile vuejs
```

## 命令行接口（CLI）

### 配置
```bash
# Add or update a profile
anydocs config <profile> <base_url> <sitemap_url> [--search-method hybrid] [--ttl-days 7]

# List configured profiles
anydocs list-profiles
```

### 索引构建
```bash
# Build index for a profile
anydocs index <profile>

# Force re-index (skip cache)
anydocs index <profile> --force
```

### 搜索
```bash
# Basic keyword search
anydocs search "query" --profile discord

# Limit results
anydocs search "query" --profile discord --limit 5

# Regex search
anydocs search "^API" --profile discord --regex
```

### 获取页面内容
```bash
# Fetch a specific page (URL or path)
anydocs fetch "https://discord.com/developers/docs/resources/webhook"
anydocs fetch "resources/webhook" --profile discord
```

### 缓存管理
```bash
# Show cache statistics
anydocs cache status

# Clear all cache
anydocs cache clear

# Clear specific profile's cache
anydocs cache clear --profile discord
```

## Python API

anydocs 提供 Python API，可用于自动化脚本和工具中：

```python
from lib.config import ConfigManager
from lib.scraper import DiscoveryEngine
from lib.indexer import SearchIndex

# Load configuration
config_mgr = ConfigManager()
config = config_mgr.get_profile("discord")

# Scrape documentation
scraper = DiscoveryEngine(config["base_url"], config["sitemap_url"])
pages = scraper.fetch_all()

# Build search index
index = SearchIndex()
index.build(pages)

# Search
results = index.search("webhooks", limit=10)
for result in results:
    print(f"{result['title']} ({result['relevance_score']})")
    print(f"  {result['url']}")
```

## 配置文件格式

配置信息存储在 `~/.anydocs/config.json` 文件中：

```json
{
  "discord": {
    "name": "discord",
    "base_url": "https://discord.com/developers/docs",
    "sitemap_url": "https://discord.com/developers/docs/sitemap.xml",
    "search_method": "hybrid",
    "cache_ttl_days": 7
  },
  "openclaw": {
    "name": "openclaw",
    "base_url": "https://docs.openclaw.ai",
    "sitemap_url": "https://docs.openclaw.ai/sitemap.xml",
    "search_method": "hybrid",
    "cache_ttl_days": 7
  }
}
```

## 搜索方法

### 关键词搜索
- **速度**：快速；
- **适用场景**：常见术语和精确匹配；
- **工作原理**：根据关键词在标题、标签和内容中的位置进行匹配；
- **示例**：`anydocs search "webhooks"`。

### 混合搜索（默认）
- **速度**：快速；
- **适用场景**：自然语言查询；
- **工作原理**：结合关键词搜索和短语相似度评分；
- **示例**：`anydocs search "how to set up webhooks"`。

### 正则表达式搜索
- **速度**：中等；
- **适用场景**：复杂模式匹配；
- **工作原理**：在所有内容中搜索匹配的正则表达式；
- **示例**：`anydocs search "^(GET|POST)" --regex`。

## 缓存机制
- **页面内容**：以 JSON 格式缓存，缓存有效期为 7 天（可配置）；
- **索引**：构建完成后会被缓存，过期后失效；
- **缓存位置**：`~/.anydocs/cache/`；
- **手动刷新**：使用 `--force` 标志或清除缓存。

## 性能说明
- 首次构建索引需要 2-10 分钟（取决于网站规模）；
- 后续搜索非常快速（利用缓存）；
- 为保护服务器，每页请求的频率限制为 0.5 秒；
- 通常搜索可在 100 毫秒内返回约 100 个结果。

## 常见问题解决方法

- **“找不到 'profile' 的索引”错误**：先运行 `anydocs index <profile>` 命令构建索引。
- **找不到网站地图**：检查网站地图的 URL；如果找不到，则从基础 URL 进行爬取。
- **索引构建缓慢**：对于大型网站来说这是正常的现象，速率限制有助于防止服务器负担过重。
- **缓存占用过多空间**：运行 `anydocs cache clear` 命令或调整 `--ttl-days` 参数以减小缓存大小。

## 示例

- **Vue.js 框架文档（单页应用示例）**
```bash
anydocs config vuejs \
  https://vuejs.org \
  https://vuejs.org/sitemap.xml
anydocs index vuejs
anydocs search "composition api"
```

- **Next.js API 文档**
```bash
anydocs config nextjs \
  https://nextjs.org \
  https://nextjs.org/sitemap.xml
anydocs index nextjs
anydocs search "app router" --profile nextjs
```

- **公司内部文档**
```bash
anydocs config internal \
  https://docs.company.local \
  https://docs.company.local/sitemap.xml
anydocs index internal --force
anydocs search "deployment" --profile internal
```

## 架构
- **scraper.py**：通过网站地图发现 URL，获取并解析 HTML 内容；
- **indexer.py**：构建可搜索的索引，实现多种搜索策略；
- **config.py**：管理配置文件；
- **cache.py**：实现基于 TTL 的页面和索引缓存；
- **cli.py**：提供命令行接口。

## 贡献方式

要添加新的文档网站，请运行：
```bash
anydocs config <profile> <base_url> <sitemap_url>
```

要扩展搜索功能，请修改 `lib/indexer.py` 文件。

## 许可证

anydocs 是 OpenClaw 系统的一部分。