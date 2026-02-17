# markdown-extract 技能

使用 `markdown.new` API 从任何 URL 中提取干净的 Markdown 内容。

## 描述

该技能通过 `markdown.new` API 将网页转换为干净的 Markdown 格式。它支持多种提取方法，并能优雅地处理错误。

## 使用方法

```
!markdown-extract <url> [method]
```

### 参数

- `url`（必填）：需要提取 Markdown 的 URL
- `method`（可选）：提取方法：`auto`、`ai` 或 `browser`。默认值：`auto`

### 示例

```bash
# Extract using default method (auto)
!markdown-extract https://example.com

# Extract using AI method
!markdown-extract https://example.com ai

# Extract using browser method
!markdown-extract https://example.com browser
```

## API

- GET `https://markdown.new/<url>` - 返回干净的 Markdown 内容（使用 `auto` 方法）
- 使用 POST 请求并传递 JSON 数据：`{url: "...", method: "browser|ai"}` - 指定提取方法

## 提取方法

- **auto**：通过 `Accept: text/markdown` 请求头进行内容协商（最快，默认方法）
- **ai**：使用 Cloudflare Workers 的 AI `toMarkdown()` 功能进行转换
- **browser**：使用无头浏览器渲染 JavaScript 密集的页面（最慢，但信息最完整）

## 错误处理

- 无效的 URL：返回错误信息
- 网络故障：返回可重试的错误提示
- API 错误：返回错误详情
- Cloudflare 的访问限制检测及备用方案处理