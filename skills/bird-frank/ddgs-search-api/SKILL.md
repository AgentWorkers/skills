---
name: ddgs-web-search
description: >
  **使用说明：**  
  当需要在 AI 编码工具或 OpenClaw 中进行网络搜索时，请使用该功能。该功能通过 DuckDuckGo API 实现搜索功能，无需使用 API 密钥。
---
# DuckDuckGo 网页搜索技能

这是一个用于通过 DuckDuckGo 进行网页内容搜索的代理技能。

## 概述

该技能提供了一个命令行工具，通过 `ddgs` Python 包来实现网页搜索功能。适用于以下场景：

- 人工智能编程工具中的实时网页信息需求
- 在 OpenClaw 工作流中获取搜索结果

## 核心功能

- **网页搜索**：通用网页搜索
- **新闻搜索**：专门针对新闻内容的搜索
- **多种输出格式**：文本或 JSON 格式
- **灵活的配置选项**：地区设置、时间限制和安全搜索级别

## 安装

该项目使用 `uv` 作为 Python 包管理器。

### 方式 1：使用 `uv` 安装（推荐）

```bash
# Run the script directly (uv will auto-install dependencies)
uv run scripts/ddgs_search.py "Python programming"

# Or navigate to the directory first
cd skills/ddgs-search
uv run scripts/ddgs_search.py "machine learning"
```

### 方式 2：手动安装依赖项

```bash
# Install dependencies using uv
uv pip install ddgs

# Or use pip
pip install ddgs
```

## 快速入门

### 基本用法

```bash
# Run with uv (recommended)
uv run scripts/ddgs_search.py "Python programming"

# Limit the number of results
uv run scripts/ddgs_search.py "machine learning" --max-results 5

# Search news
uv run scripts/ddgs_search.py "tech news" --news

# JSON output (for programmatic parsing)
uv run scripts/ddgs_search.py "API documentation" --json

# Time limit (today)
uv run scripts/ddgs_search.py "breaking news" --timelimit d
```

## 完整参数参考

| 参数 | 缩写 | 描述 | 默认值 |
| --------- | ----- | ----------- | ------- |
| `query` | - | 搜索关键词 | 必填 |
| `--max-results` | `-n` | 最大结果数量 | 10 |
| `--region` | `-r` | 地区代码 | `wt-wt` |
| `--safesearch` | `-s` | 安全搜索模式（开启/关闭） | `moderate` |
| `--timelimit` | `-t` | 时间限制（天/周/月/年） | - |
| `--backend` | `-b` | 搜索后端（自动/HTML/简化版） | `auto` |
| `--news` | - | 搜索新闻 | - |
| `--json` | `-j` | 输出格式为 JSON | - |
| `--verbose` | `-v` | 显示详细信息 | - |

### 地区代码示例

- `wt-wt` - 全球（默认）
- `us-en` - 美国英语
- `cn-zh` - 中国中文
- `jp-jp` - 日本
- `uk-en` - 英国

### 时间限制

- `d` - 过去一天
- `w` - 过去一周
- `m` - 过去一个月
- `y` - 过去一年

## 在 OpenClaw 中的使用

在 OpenClaw 工作流中，您可以通过 `bash` 工具调用该技能：

```yaml
# Example workflow step
- name: search_web
  tool: bash
  command: cd skills/ddgs-search && uv run scripts/ddgs_search.py "{{ query }}" --json
```

或者使用 Python 工具调用：

```python
# Assuming the current directory is the project root
import subprocess
import json

result = subprocess.run(
    ["uv", "run", "skills/ddgs-search/scripts/ddgs_search.py", "Python tips", "--json"],
    capture_output=True,
    text=True
)
data = json.loads(result.stdout)
```

## 返回结果格式

### 网页搜索结果

```json
[
  {
    "title": "Result Title",
    "href": "https://example.com/page",
    "body": "Page snippet/description..."
  }
]
```

### 新闻搜索结果

```json
[
  {
    "title": "News Headline",
    "href": "https://news.example.com/article",
    "body": "Article summary...",
    "date": "2024-01-15",
    "source": "News Source Name"
  }
]
```

## 使用示例

### 示例 1：搜索技术文档

```bash
uv run scripts/ddgs_search.py "FastAPI documentation" -n 5
```

### 示例 2：获取最新新闻

```bash
uv run scripts/ddgs_search.py "artificial intelligence" --news -t d -n 3
```

### 示例 3：中文搜索

```bash
uv run scripts/ddgs_search.py "机器学习教程" -r cn-zh -n 8
```

### 示例 4：处理 JSON 格式输出

```bash
uv run scripts/ddgs_search.py "python tips" --json | jq '.[0].href'
```

## 常见问题解答

### 未安装 `uv`？

请确保已安装 `uv` 作为 Python 包管理器。

### 报错：`No module named 'ddgs'`

请检查是否正确安装了 `ddgs` 包。

### 搜索结果为空？

- 检查网络连接是否正常
- 尝试更改 `--backend` 参数（自动/HTML/简化版）
- 某些地区可能需要使用代理服务器

## 速率限制

DuckDuckGo 具有内置的速率限制机制。如果频繁请求失败，请尝试以下方法：

- 减少请求频率
- 在请求之间添加延迟
- 更换搜索后端

## 所需依赖项

- Python 3.9 或更高版本
- `uv`（包管理器）
- `ddgs` 版本 >= 8.0.0