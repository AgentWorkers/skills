---
name: markdown-browser
description: "OpenClaw 的 `web_fetch` 结果封装技能。当您需要对获取到的页面进行 MECE（Measurable, Efficient, Complete, and Explicit）后处理时，可以使用此技能：根据 Content-Signal 进行策略决策、进行隐私数据屏蔽、提供可选的 Markdown 标准化功能（作为备用方案），以及生成稳定的输出格式，而无需重新实现网络数据获取逻辑。"
---
# Markdown浏览器技能（Markdown Browser Skills）

该技能主要起到协调作用，并不替代官方的页面获取机制；它始终以官方的 `web_fetch` 作为数据获取的来源。

## MECE架构（MECE Architecture）

1. **获取层（Fetch Layer, 官方专有）**  
   - 使用 OpenClaw 的 `web_fetch` 功能来获取网页内容。  
   - 在正常操作过程中，严禁在此技能内部直接发起 HTTP 请求。

2. **策略层（Policy Layer, 该技能所属）**  
   - 解析 `Content-Signal` 标头信息，并据此计算出相应的 `policy_action`（策略操作）。  
   - 当前策略操作主要关注 `ai-input` 的语义，包括 `allow_input`（允许输入）、`block_input`（阻止输入）和 `needs_review`（需要审核）等。

3. **隐私保护层（Privacy Layer, 该技能所属）**  
   - 在生成的输出 URL 中屏蔽路径、片段或查询参数等敏感信息，  
   - 同时保持 URL 的格式以便于调试，避免泄露敏感数据。

4. **规范化层（Normalization Layer, 该技能所属）**  
   - 如果页面的 `contentType` 为 `text/markdown`，则直接保留原始内容；  
   - 如果 `contentType` 为 `text/html`，则使用 `turndown` 工具进行转换（作为备用方案）；  
   - 对于其他类型的页面内容，直接以原始文本形式传递。

## 执行顺序（Execution Order）  
1. 调用官方的 `web_fetch` 功能。  
2. 将获取到的 JSON 数据传递给该技能的封装层（wrapper）。  
3. （可选）如果有的话，同时传递 `Content-Signal` 标头信息和 `x-markdown-tokens` 标头值。  
4. 使用处理后的规范化数据作为后续处理流程的输入。

## 封装工具（Wrapper Tool）  
`process_web_fetch_result({ web_fetch_result, content_signal_header, markdown_tokens_header })`

**输入参数：**  
- `web_fetch_result`（必填）：由 OpenClaw `web_fetch` 返回的 JSON 数据。  
- `content_signal_header`（可选）：原始的 `Content-Signal` 标头字符串。  
- `markdown_tokens_header`（可选）：原始的 `x-markdown-tokens` 标头值。  

**输出参数：**  
- `content`：处理后的页面内容。  
- `format`：输出格式（`markdown`、`html-fallback` 或 `text`）。  
- `token_estimate`：标记化过程中使用的标记数量（数字类型，或缺失时为 `null`）。  
- `content_signal`：解析后的 `Content-Signal` 标头信息。  
- `policy_action`：根据解析结果确定的策略操作。  
- `source_url`：经过处理的 URL（已屏蔽敏感信息）。  
- `status_code`：请求执行的状态码。  
- `fallback_used`：是否使用了备用转换方案（`html-fallback`）。  

## 命令行接口（CLI Usage）  
```bash
# Install runtime dependency once inside the skill directory
npm install --omit=dev

# 1) Obtain a web_fetch payload first (from OpenClaw runtime)
# 2) Save it as /tmp/web_fetch.json
# 3) Run wrapper post-processing
node browser.js \
  --input /tmp/web_fetch.json \
  --content-signal "ai-input=yes, search=yes, ai-train=no" \
  --markdown-tokens "1820"
```