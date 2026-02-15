---
name: ddg-search
description: 使用 DuckDuckGo 在网上搜索。完全免费，无需 API 密钥。当用户要求进行网络搜索、查找信息、研究某个主题，或者当你需要找到训练数据中不存在的当前信息时，都可以使用它。此外，在 `web_search` 工具不可用或未配置 API 密钥的情况下，也可以使用 DuckDuckGo。
---

# DuckDuckGo 网页搜索

使用 `ddgs` Python 库通过 DuckDuckGo 进行网页搜索。无需 API 密钥。

## 快速使用方法

```bash
python3 skills/ddg-search/scripts/search.py "your search query" [count]
```

- `query`（必填）：搜索关键词
- `count`（可选）：结果数量，默认为 5，最大值为 20

## 输出格式

每个搜索结果包含以下信息：
- **标题**：页面标题
- **URL**：直接链接
- **片段**：文本摘录

## 示例

```bash
# Basic search
python3 skills/ddg-search/scripts/search.py "latest AI news"

# More results
python3 skills/ddg-search/scripts/search.py "Python async tutorial" 10
```

## 后续操作

搜索完成后，可以使用 `web_fetch` 从任意结果 URL 中读取完整内容。

## 依赖项

- `ddgs` Python 包（安装方式：`pip install --break-system-packages ddgs`）

## 限制

- 该工具属于非官方的网页抓取工具；如果 DuckDuckGo 更改其前端界面，可能会导致功能失效。
- 在高频率使用的情况下可能会遇到速率限制。
- 默认情况下，搜索结果主要来自英文网站。