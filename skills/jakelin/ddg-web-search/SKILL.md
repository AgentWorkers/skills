---
name: ddg-search
description: >
  **使用 DuckDuckGo Lite 和 web_fetch 进行无 API 密钥的网页搜索**  
  当 `web_search` 出现 “missing_brave_api_key” 错误时，或者在没有配置搜索 API 的情况下，可以将其作为备用方案。该方法能够获取搜索结果中的标题、URL 和内容片段。完全无需依赖任何外部库，仅依赖内置的 `web_fetch` 工具即可实现。
---
# 使用 `web_fetch` 通过 DuckDuckGo 进行搜索

您可以使用 DuckDuckGo Lite 的 HTML 界面进行网络搜索，该界面通过 `web_fetch` 功能进行解析。无需安装任何 API 密钥或相关软件包。

## 搜索方法

```
web_fetch(url="https://lite.duckduckgo.com/lite/?q=QUERY", extractMode="text", maxChars=8000)
```

- 对查询字符串进行 URL 编码——使用 `+` 来表示空格
- 设置 `extractMode="text"`（而非 markdown 格式）以获得更清晰的结果
- 增加 `maxChars` 的值可以获取更多搜索结果

## 地区过滤

添加 `&kl=REGION` 参数可过滤特定地区的搜索结果：
- `au-en` — 澳大利亚
- `us-en` — 美国
- `uk-en` — 英国
- `de-de` — 德国
- `fr-fr` — 法国

完整地区列表：https://duckduckgo.com/params

### 示例 — 澳大利亚搜索

```
web_fetch(url="https://lite.duckduckgo.com/lite/?q=best+coffee+melbourne&kl=au-en", extractMode="text", maxChars=8000)
```

## 查看搜索结果

搜索结果会以编号的形式显示，包括标题、摘要和链接。请跳过标记为“Sponsored link”（广告）的条目，这些是自然搜索结果。

## “搜索后获取内容”的使用流程

1. **搜索**：在 DuckDuckGo Lite 中输入查询词以获取结果列表。
2. **筛选**：挑选出最相关的链接。
3. **获取内容**：使用 `web_fetch` 功能获取这些链接的完整内容。

## 使用技巧

- 前 1-2 个结果可能是广告，请跳过它们，直接查看自然搜索结果。
- 对于精确的短语，请使用引号括起来：`q=%22exact+phrase%22`。
- 通过添加特定关键词（如网站名称、年份、地点）来缩小搜索范围。

## 限制事项

- 不支持时间/日期过滤（DuckDuckGo Lite 无法通过 `web_fetch` 功能可靠地实现该功能）。
- 仅返回文本结果，不包含图片或视频。
- 搜索结果来自 Bing（可能与 Google 的结果有所不同）。
- 无法通过 `web_fetch` 功能使用 Google 搜索功能（因为 Google 使用了验证码）。