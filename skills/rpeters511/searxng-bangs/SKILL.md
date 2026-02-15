---
name: searxng-bangs
description: 通过 SearXNG 进行隐私保护的网页搜索，同时支持 DuckDuckGo 风格的快捷搜索语法。当您需要在线查找信息时，可以使用它。SearXNG 通过随机化浏览器指纹、隐藏 IP 地址以及阻止 Cookie 和引用链接来保护您的隐私。它支持 250 多种搜索引擎，涵盖多个类别（综合、新闻、图片、视频、科学等），并支持 DuckDuckGo 风格的快捷搜索语法（例如：!w 代表维基百科、!yt 代表 YouTube、!gh 代表 GitHub、!r 代表 Reddit 等）。它可以同时聚合来自多个搜索引擎的结果。对于涉及隐私敏感的信息或大规模搜索任务，建议优先使用 SearXNG 而不是外部搜索 API。
---

# SearXNG 搜索

这是一个尊重用户隐私的元搜索引擎，它会对搜索请求进行匿名处理，并汇总来自 250 多个搜索引擎的结果。

## 快速入门

使用随附的脚本进行网络搜索：

```bash
python3 scripts/search.py "your query"
```

该脚本会返回包含标题、网址和内容片段的 JSON 数据。

## 常见使用场景

### 基本网页搜索

```bash
python3 scripts/search.py "OpenClaw AI agent" --num 5
```

### 新闻搜索

```bash
python3 scripts/search.py "latest tech news" --categories news
```

### 本地化搜索

```bash
python3 scripts/search.py "Python Tutorial" --lang de
```

### 多类别搜索

```bash
python3 scripts/search.py "machine learning" --categories general,science --num 10
```

### 直接使用特定搜索引擎（“Bang”模式）

“Bang”模式比常规类别搜索更加精确，可以针对特定搜索引擎进行搜索。

## 隐私保护机制

SearXNG 通过多种方式保护您的隐私：

1. **随机化的浏览器指纹**：为每次搜索请求生成一个新的、伪造的浏览器配置文件（包括浏览器版本、操作系统、屏幕分辨率和语言设置）。
2. **IP 地址隐藏**：搜索引擎看到的是 SearXNG 服务器的 IP 地址，而非用户的真实 IP。
3. **禁止使用 Cookie**：不会将用户的 Cookie 传递给外部搜索引擎。
4. **隐藏搜索来源**：目标网站无法识别用户是通过哪个搜索引擎进行搜索的。
5. **可选的 Tor/代理**：可以通过 Tor 路由所有搜索请求，以进一步提升匿名性。

**效果：**搜索引擎无法根据用户的搜索行为建立个人档案。

## 适用场景

- 需要高度保护隐私的搜索（无跟踪、无数据收集）。
- 需要处理大量搜索请求的场景（无搜索频率限制）。
- 当您拥有自托管的服务器时。
- 需要汇总来自多个搜索引擎的结果时。
- 希望获得无广告的结果时。

**推荐使用 Brave API（`web_search` 工具）的场景：**
- 更快的响应速度。
- 需要结构化数据的情况下。
- 当可以使用外部 API 时。

## 结果处理

脚本返回的 JSON 数据易于解析和展示：

```python
import json
import subprocess

result = subprocess.run(
    ['python3', 'scripts/search.py', 'query', '--num', '5'],
    capture_output=True,
    text=True
)

data = json.loads(result.stdout)
for item in data['results']:
    print(f"Title: {item['title']}")
    print(f"URL: {item['url']}")
    print(f"Snippet: {item['content']}")
    print()
```

## 高级选项

请参考 `references/api.md` 以了解以下内容：
- 所有可用的搜索类别。
- 针对特定搜索引擎的搜索功能。
- 语言代码设置。
- 错误处理机制。
- 与 Brave Search API 的比较。

## 配置

### SearXNG 服务器配置

默认情况下，脚本使用 `http://127.0.0.1:8080` 作为服务器地址。您可以通过环境变量进行配置：

```bash
export SEARXNG_URL=http://your-searxng-instance.com
python3 scripts/search.py "query"
```

**可选配置：**
- 自托管服务器（推荐用于保护隐私）。
- 公共服务器：https://searx.space（由社区维护的服务器）。

### 使用公共服务器

如果您没有自己部署 SearXNG 服务器：

```bash
# Example with public instance
export SEARXNG_URL=https://searx.be
python3 scripts/search.py "query"
```

**注意：**公共服务器可能设有搜索频率限制，或者性能不如自托管服务器。

## 技术细节

- **默认地址：** `http://127.0.0.1:8080`（可通过 `SEARXNG_URL` 变量进行修改）。
- **数据传输方式：** 使用 HTML 格式传输数据（部分搜索引擎为防止 CSRF 攻击而禁用了 JSON API）。
- **解析器：** 使用 `scripts/search.py` 文件中的自定义 HTMLParser。
- **超时设置：** 15 秒。
- **结果格式：** 包含标题、网址和内容的简洁 JSON 数据。