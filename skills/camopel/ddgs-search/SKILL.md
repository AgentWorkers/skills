---
name: ddgs-search
description: 通过 ddgs CLI（DuckDuckGo、Google、Bing、Brave、Yandex、Yahoo、Wikipedia）实现免费的多引擎网络搜索功能，并支持 arXiv API 的搜索。无需使用 API 密钥。适用于用户进行网络搜索、研究论文查找，或为其他工具提供搜索后端支持。可作为 web-search-plus 的替代方案直接使用。
metadata: {"openclaw":{"requires":{"bins":["python3"]}}}
---
# ddgs-search

## 为什么选择这个工具？

🆓 **完全免费** — 无需API密钥、无需订阅、无需限制使用次数，也无需担心账单问题。

🔍 **集成8种搜索引擎** — Google、Bing、DuckDuckGo、Brave、Yandex、Yahoo、Wikipedia和Mojeek。只需一个参数即可切换搜索引擎。大多数搜索工具仅支持其中一种。

🎓 **内置arXiv研究搜索功能** — 可通过arXiv的免费API直接搜索学术论文，返回作者信息、论文类别、摘要和发表日期。非常适合研究人员、学生以及AI/ML领域的从业者。

🔌 **易于集成** — 输出符合web-search-plus标准的JSON格式，因此可以与其他任何支持该格式的工具或技能无缝配合使用，无需进行任何配置调整。

⚡ **轻量级** — 仅需一个pip包即可安装，无需浏览器自动化或额外的Chrome环境。搜索过程通常在1-3秒内完成。

## 安装

```bash
python3 scripts/install.py
```

该工具支持**macOS、Linux和Windows**系统。安装完成后，会验证命令行（CLI）的可用性，并运行一个简单的搜索测试。

### 手动安装
```bash
pip install ddgs
```

## 网页搜索

### 推荐的CLI封装方式

`ddgs-search`的CLI封装版本会以纯JSON格式将搜索结果输出到标准输出（stdout），无需任何交互式提示或异常终止情况：

```bash
# Google (default)
ddgs-search "your query" 5 google

# Other engines
ddgs-search "your query" 3 duckduckgo
ddgs-search "your query" 5 brave
ddgs-search "your query" 10 yandex
```

### Python脚本（输出符合web-search-plus标准的JSON）

```bash
# Google (default)
python3 scripts/search.py -q "your query" -m 5

# Other engines
python3 scripts/search.py -q "your query" -b duckduckgo
python3 scripts/search.py -q "your query" -b brave
python3 scripts/search.py -q "your query" -b yandex
python3 scripts/search.py -q "your query" -b yahoo
python3 scripts/search.py -q "your query" -b wikipedia
```

**搜索结果（符合web-search-plus标准的JSON格式）：**
```json
{
  "provider": "ddgs",
  "results": [
    {"title": "...", "url": "...", "snippet": "...", "published_date": "..."}
  ]
}
```

## arXiv搜索

```bash
# Search by topic
python3 scripts/arxiv_search.py -q "3D gaussian splatting" -m 10

# Field-specific search (title, abstract, category)
python3 scripts/arxiv_search.py -q "ti:transformer AND cat:cs.CV" -m 5

# Sort by relevance instead of date
python3 scripts/arxiv_search.py -q "reinforcement learning" --sort-by relevance
```

搜索结果同样以JSON格式返回，包含作者信息、论文类别和摘要。

## 直接使用CLI

> ⚠️ 原生的`ddgs text` CLI存在分页问题（在非TTY环境下使用`input()`函数时可能会导致“Aborted!”错误并退出程序）。建议使用`ddgs-search`封装版本或`-o file.json`选项进行搜索。

```bash
ddgs text -q "query" -m 5 -b google -o /tmp/results.json
```

## 集成

通过设置`WEB_SEARCH_PLUS_PATH`环境变量，可以将`ddgs-search`作为其他工具的搜索后端：

```bash
export WEB_SEARCH_PLUS_PATH="path/to/ddgs-search/scripts/search.py"
```