---
name: web-search
description: Search the web and fetch web pages. Use when user wants to look up information, find answers, or search for anything online. Supports multiple free methods: Jina AI reader, DuckDuckGo Lite, and Python ddgs fallback. No API keys required for basic use.
metadata:
  {
    "openclaw": {
      "emoji": "🔍",
      "homepage": "https://github.com/openclaw/openclaw",
      "requires": {}
    }
  }
---

# 网页搜索技能

提供全面的网页搜索和内容提取服务——完全免费，无需使用API密钥。

## 快速入门

**仅需要搜索？** 使用 DuckDuckGo Lite：
```
web_fetch url="https://lite.duckduckgo.com/lite/?q=YOUR+QUERY"
```

**需要获取整个页面的内容？** 使用 Jina Reader：
```
web_fetch url="https://r.jina.ai/http://TARGET_URL"
```

---

## 方法 1：Jina AI Reader（免费 - 推荐用于内容提取）

使用 Jina 的免费 API 提取整个页面的内容。

### 阅读一个 URL
```
web_fetch url="https://r.jina.ai/http://example.com"
```

### 在网页上搜索
```
web_fetch url="https://r.jina.ai/http://duckduckgo.com/?q=YOUR+QUERY"
```

**示例：**
| 任务 | 命令 |
|------|---------|
| 获取 Next.js 文档 | `web_fetch url="https://r.jina.ai/http://nextjs.org"` |
| 获取 React 文档 | `web_fetch url="https://r.jina.ai/http://react.dev"` |
| 获取 Python 文档 | `web_fetch url="https://r.jina.ai/http://docs.python.org"` |

### 高级 Jina Reader（需 API 密钥）

如需使用高级功能，请从 [jina.ai/reader](https://jina.ai/reader) 获取免费 API 密钥：

```bash
export JINA_API_KEY="jina_..."
```

然后使用捆绑的脚本：
```
{baseDir}/scripts/reader.sh "https://example.com"
{baseDir}/scripts/reader.sh --mode search "AI news 2025"
{baseDir}/scripts/reader.sh --mode ground "OpenAI founded 2015"
```

可选参数：`--mode`、`--selector`、`--remove`、`--format`、`--json`

---

## 方法 2：DuckDuckGo Lite（免费 - 推荐用于搜索）

无需 API 密钥，即可使用 DuckDuckGo Lite 进行搜索。

### 基本搜索
```
web_fetch url="https://lite.duckduckgo.com/lite/?q=YOUR+QUERY"
```

### 地区搜索
```
web_fetch url="https://lite.duckduckgo.com/lite/?q=QUERY&kl=us-en"
```

可用地区：`au-en`、`us-en`、`uk-en`、`de-de`、`fr-fr`

### 搜索技巧：
- 使用 `+` 来表示空格：`python+tutorial`
- 使用引号来搜索精确短语：`%22exact+phrase%22`
- 跳过前 1-2 个搜索结果（广告）

---

## 方法 3：Python ddgs（备用方案）

如果 `web_fetch` 被阻止，可以使用 Python 的 `ddgs` 包：

```bash
pip install ddgs
```

```python
from ddgs import DDGS
ddgs = DDGS()
results = ddgs.text("search query", max_results=5)
for r in results:
    print(f"{r['title']}: {r['url']}")
```

---

## 工作流程：搜索 → 提取

1. **搜索** → 使用 DDG Lite 找到相关 URL
2. **选择** → 确定最佳结果
3. **提取** → 使用 Jina Reader 提取完整内容

示例：
```
# Step 1: Find info about Next.js auth
web_fetch url="https://lite.duckduckgo.com/lite/?q=nextjs+authentication+docs"

# Step 2: Fetch the official docs
web_fetch url="https://r.jina.ai/http://nextjs.org/docs/app/..."
```

---

## 快速参考

| 需求 | 方法 | 命令 |
|------|--------|---------|
| 查找 URL | DDG Lite | `?q=search+terms` |
| 获取页面内容 | Jina Reader | `r.jina.ai/http://URL` |
| 高级提取 | Jina API | `--mode search --json` |
| 使用 Python 备用方案 | ddgs | `ddgs.text()` |
| （如果可用）浏览器（无头模式） | `browser action=navigate` |

---

## 限制

- Google 搜索可能被阻止（需要验证码）
- DuckDuckGo Lite 不支持日期过滤
- Jina 的免费版本有使用次数限制