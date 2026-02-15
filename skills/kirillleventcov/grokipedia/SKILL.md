---
name: Grokipedia
description: 从 Grokipedia.com（xAI 生成的人工智能百科全书，类似于 Wikipedia，但内容由 Grok 编写）中搜索并获取文章。当用户询问可能有关 Grokipedia 文章的主题，或者用户明确提到 Grokipedia 时，可以使用此功能。
---

# Grokipedia 解析器

该工具用于从 [Grokipedia.com](https://grokipedia.com) 搜索并获取文章内容。Grokipedia 是由 xAI 开发的人工智能生成的百科全书。

**来源:** [github.com/kirillleventcov/grokipedia-parser](https://github.com/kirillleventcov/grokipedia-parser)

## 所需环境

- **Node.js** (v18+) 或 **Bun** — 用于运行搜索和获取数据的脚本
- **依赖库:** `jsdom` 和 `@mozilla/readability`（通过 `bun install` 安装）

## 安装

```bash
cd ~/.openclaw/workspace/skills/Grokipedia
bun install --production
```

> **注意:** 安装完成后，会在技能目录（skill folder）下生成一个 `node_modules/` 目录。这些脚本本身仅在运行时将结果输出到标准输出（stdout）。

## 脚本说明

### 搜索文章

```bash
node ~/.openclaw/workspace/skills/Grokipedia/scripts/search.mjs "query" [--limit N]
```

**参数:**
- `query` - 搜索关键词（必填）
- `--limit N` - 最大返回结果数量（1-50，默认值：10）

**输出:** 包含 `slug`、`title`、`snippet` 和 `relevanceScore` 的 JSON 数组

**示例:**
```bash
node ~/.openclaw/workspace/skills/Grokipedia/scripts/search.mjs "artificial intelligence" --limit 5
```

### 获取文章内容

```bash
node ~/.openclaw/workspace/skills/Grokipedia/scripts/fetch.mjs "Article_Slug"
```

**参数:**
- `slug` - 文章的唯一标识符（slug，区分大小写，使用下划线分隔单词）

**输出:** 清晰的 Markdown 格式文章内容

**示例:**
```bash
node ~/.openclaw/workspace/skills/Grokipedia/scripts/fetch.mjs "Helsinki"
node ~/.openclaw/workspace/skills/Grokipedia/scripts/fetch.mjs "Artificial_intelligence"
```

## 该工具的功能

- **网络访问:** 仅从 `grokipedia.com` 获取数据（包括搜索结果和文章页面）
- **无需凭证:** 仅支持公共读取权限，无需 API 密钥或令牌
- **不写入运行时文件:** 所有数据仅输出到标准输出（搜索结果为 JSON 格式，文章内容为 Markdown 格式）
- **无持久化机制:** 不使用后台进程、定时任务（cron）或提升权限的操作
- **依赖库:** `jsdom`（用于 DOM 解析）和 `@mozilla/readability`（用于提取文章内容）

## 注意事项

- 文章的唯一标识符（slug）区分大小写（例如：`Helsinki` 和 `helsinki` 不同）
- 使用下划线来表示单词之间的空格（例如：`Artificial_intelligence`）
- 每次搜索最多返回 50 条结果
- 文章中包含格式为 `[text](/page/Slug)` 的内部链接
- 文章内容由 Grok 人工智能生成