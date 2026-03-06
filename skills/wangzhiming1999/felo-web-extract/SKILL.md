---
name: felo-web-extract
description: "使用 Felo Web Extract API 从 URL 中提取网页内容。适用于用户需要抓取/获取网页内容、从 URL 中提取文章文本、将页面转换为 Markdown 或文本格式的情况，或者当使用类似 `/felo-web-extract` 的明确命令时。支持 HTML、文本、Markdown 格式以及可读性模式作为输出结果。"
---
# Felo Web Extract 技能

## 使用场景

当用户需要执行以下操作时，可以使用此技能：

- 从网页 URL 中提取或抓取内容
- 从链接中获取文章或主要文本
- 将网页转换为 Markdown 或纯文本
- 从 URL 中提取可读内容以用于摘要或处理

**触发关键词示例**：
- extract webpage、scrape URL、fetch page content、web extract、url to markdown
- 明确指令：`/felo-web-extract`、`use felo web extract`
- 其他语言中的类似指令（如：网页抓取、提取网页内容）也会触发此技能

**不适用场景**：
- 实时搜索或问答（使用 `felo-search`）
- 生成幻灯片（使用 `felo-slides`）
- 本地文件内容（直接读取文件）

## 设置

### 1. 获取 API 密钥

1. 访问 [felo.ai](https://felo.ai)
2. 进入设置 -> API 密钥
3. 创建并复制您的 API 密钥

### 2. 配置环境变量

**Linux/macOS**：
```bash
export FELO_API_KEY="your-api-key-here"
```

**Windows PowerShell**：
```powershell
$env:FELO_API_KEY="your-api-key-here"
```

## 使用方法

### 选项 A：使用捆绑的脚本或打包的 CLI

**脚本**（来自仓库）：
```bash
node felo-web-extract/scripts/run_web_extract.mjs --url "https://example.com/article" [options]
```

**打包的 CLI**（安装 `felo-ai` 后）：
- 命令相同，支持简写形式：
```bash
felo web-extract -u "https://example.com" [options]
# 简写形式：-u （URL），-f （格式），-t （超时，秒），-j （JSON）
```

**参数说明**：

| 参数 | 默认值 | 说明 |
|--------|---------|-------------|
| `--url` | （必填） | 需要提取的网页 URL |
| `--format` | markdown | 输出格式：`html`、`text`、`markdown` |
| `--target-selector` | - | CSS 选择器：仅提取该元素（例如 `article.main`、`#content`） |
| `--wait-for-selector` | - | 在提取前等待该选择器（例如动态内容） |
| `--readability` | false | 启用可读性处理（仅提取主要内容） |
| `--crawl-mode` | fast | `fast` 或 `fine` |
| `--timeout` | 60000 （脚本）/ 60 （CLI） | 请求超时：脚本使用毫秒，CLI 使用秒（例如 `-t 90`） |
| `--json` / `-j` | false | 以 JSON 格式输出完整 API 响应 |

### 指令编写方法

当用户需要提取页面的特定部分或特定格式的输出时，可使用以下命令：

- **输出格式**：`--format text` / `--format markdown` / `--format html`
- **提取特定元素**：`--target-selector "article.main"` 或其他选择器（例如 `#main`、`.main-content`）

**示例**：
- **提取纯文本**：`--url "..." --format text`
- **提取主要内容**：`--url "..." --target-selector "main"`
- **提取 id=content 的 div 内容为 Markdown**：`--url "..." --target-selector "#content" --format markdown`
- **提取文章正文（HTML）**：`--url "..." --target-selector "article.body" --format html`

**使用示例**：
```bash
# 基本用法：提取为 Markdown
node felo-web-extract/scripts/run_web_extract.mjs --url "https://example.com"

# 带有可读性的文章格式
node felo-web-extract/scripts/run_web_extract.mjs --url "https://example.com/article" --readability --format markdown

# 原始 HTML
node felo-web-extract/scripts/run_web_extract.mjs --url "https://example.com" --format html --json

# 提取匹配 CSS 选择器的元素（例如文章正文）
node felo-web-extract/scripts/run_web_extract.mjs --url "https://example.com" --target-selector "article.main" --format markdown

### 选项 B：使用 curl 调用 API

```bash
curl -X POST "https://openapi.felo.ai/v2/web/extract" \
  -H "Authorization: Bearer $FELO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "output_format": "markdown", "with_readability": true}'
```

## API 参考

- **端点**：`POST /v2/web/extract`
- **基础 URL**：`https://openapi.felo.ai`（可根据需要使用 `FELO_API_BASE` 环境变量覆盖）
- **认证**：`Authorization: Bearer YOUR_API_KEY`

**请求体（JSON）**：
| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|---------|------|---------|-------------|
| url | string | 是 | 需要提取的网页 URL |
| crawl_mode | string | 否 | `fast` 或 `fine` |
| output_format | string | 否 | `html`、`text`、`markdown` |
| with_readability | boolean | 否 | 是否启用可读性处理（仅提取主要内容） |
| with_links_summary | boolean | 否 | 是否包含链接摘要 |
| with_images_summary | boolean | 否 | 是否包含图片摘要 |
| target_selector | string | 否 | 目标元素的 CSS 选择器 |
| wait_for_selector | string | 否 | 是否在提取前等待指定选择器 |
| timeout | integer | 否 | 超时时间（毫秒） |
| with_cache | boolean | 否 | 是否使用缓存 |

**响应**

**成功情况（状态码 200）**：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "content": { ... }
}
```

提取的内容存储在 `data.content` 中；具体结构取决于 `output_format`。

**错误代码**：
- **400**：参数验证失败
- **401**：API 密钥无效或已吊销
- **500/502**：提取失败（服务器或页面错误）

**输出格式**：

- **成功时（未使用 `--json`）**：仅输出提取的内容。
- **使用 `--json` 时**：输出完整的 API 响应（包括 `code`、`message`、`data`）。

**错误提示**：
```markdown
## Web Extract 失败

- 错误：<错误代码或消息>
- URL：<请求的 URL>
- 建议：<例如：检查 URL、重试或使用 `--timeout>`
```

**重要提示**：
- 在调用 API 之前请务必检查 `FELO_API_KEY`；如果缺失，请返回设置指南。
- 对于长篇文章或响应速度较慢的网站，请考虑设置 `--timeout` 或在请求体中指定超时时间。
- 使用 `output_format: "markdown"` 和 `with_readability: true` 可获得更清晰的文章文本。
- API 可能会缓存结果；仅在需要最新内容时使用 `with_cache: false`（脚本默认不显示此选项）。

**参考资料**：
- [Felo Web Extract API](https://openapi.felo.ai/docs/api-reference/v2/web-extract.html)
- [Felo Open Platform](https://openapi.felo.ai/docs/)
```