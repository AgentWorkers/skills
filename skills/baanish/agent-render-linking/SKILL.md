---
name: agent-render-linking
description: 为 Markdown、代码、差异文件（diffs）、CSV 或 JSON 格式的数据生成无需保留原始数据的链接（即这些链接不会存储任何敏感信息）。当需要通过浏览器分享格式化后的内容时，可以使用此功能（而非将原始数据粘贴到聊天中）。触发条件包括：用户请求“将此内容分享为链接”、“生成差异链接”、“渲染此 Markdown/代码/CSV/JSON 文件”，或者当聊天平台的渲染效果不佳时。Agent Render 是一个开源项目，托管在 Cloudflare Pages 上，同时也支持自定义部署。请仅在支持相应链接格式的平台上使用特定平台的链接语法（例如 Discord 的 Markdown 链接、Telegram 的 HTML 链接或 Slack 的 mrkdwn 链接）；否则，只需发送内容的简要摘要以及原始 URL 即可。
---
# 代理渲染链接生成

**功能说明：**  
为 `agent-render.com` 生成的文件创建浏览器链接。

## 项目背景  
Agent Render 是一个开源项目，托管在 Cloudflare Pages 上（网址：`agent-render.com`），同时也支持用户自行部署。它的设计目的是为代理共享的文件提供无需存储的浏览器查看功能。  

**源代码仓库：**  
`https://github.com/baanish/agent-render`  

## 核心规则  
- **文件内容存储位置：**  
  文件内容应直接存储在 URL 的片段中，而非常规的查询参数中。  

**链接格式示例：**  
```text
#agent-render=v1.<codec>.<payload>
```  

**支持的编码格式：**  
- **`plain`：** 使用 Base64URL 对 JSON 数据进行编码。  
- **`lz`：** 使用 `lz-string` 对 JSON 数据进行压缩，以适应 URL 的传输要求。  

**推荐使用方式：**  
- 当文件体积较小且对链接简洁性要求较高时，使用 `plain` 格式。  
- 当压缩能显著缩短链接长度时，使用 `lz` 格式。  

**文件封装格式：**  
使用以下 JSON 格式对文件内容进行封装：  
```json
{
  "v": 1,
  "codec": "plain",
  "title": "Artifact bundle title",
  "activeArtifactId": "artifact-1",
  "artifacts": [
    {
      "id": "artifact-1",
      "kind": "markdown",
      "title": "Weekly report",
      "filename": "weekly-report.md",
      "content": "# Report"
    }
  ]
}
```  

**支持的文件类型：**  
- **Markdown**  
- **代码**  
- **差异对比（Diff）**  
- **CSV**  
- **JSON**  

**多文件处理：**  
当用户需要查看多个相关文件时，可以使用以下链接格式：  
  - 摘要 Markdown + 差异对比（Diff）  
  - 报告 Markdown + 原始 CSV 文件  
  - 配置 JSON + 相关代码文件  

**链接构建规则：**  
最终链接的构建方式如下：  
```text
https://agent-render.com/#agent-render=v1.<codec>.<payload>
```  

- **`plain` 格式：**  
  1. 将文件内容序列化为紧凑的 JSON 格式。  
  2. 使用 Base64URL 对其进行编码。  
  3. 将编码后的 JSON 添加到链接字符串的末尾（格式：`v1.plain.`）。  

- **`lz` 格式：**  
  1. 将文件内容序列化为紧凑的 JSON 格式。  
  2. 使用 `lz-string` 对其进行压缩（确保压缩后的数据适合 URL 传输）。  
  3. 将压缩后的 JSON 添加到链接字符串的末尾（格式：`v1.lz.`）。  

**实用限制：**  
- **链接长度限制：**  
  目标链接长度约为 8,000 个字符；解码后的文件内容长度约为 200,000 个字符。  
  如果链接过长，可尝试：  
    - 从 `plain` 格式切换到 `lz` 格式。  
    - 去除不必要的文本或元数据。  
    - 优先选择更简洁的文件格式。  

**链接格式在聊天中的应用：**  
- **Discord：** 推荐使用标准的 Markdown 链接格式。  
  示例：`[每周报告](https://agent-render.com/#agent-render=...)`  
- **Telegram：** 由于 OpenClaw 的 Telegram 发送功能支持 HTML 格式的链接，因此推荐使用 HTML 链接。  
  示例：`[CSV 数据](https://agent-render.com/#agent-render=...)`  
- **Slack：** 推荐使用 Slack 的 `mrkdwn` 链接语法。  
  示例：`[查看报告](https://agent-render.com/mrkdwn#agent-render=...)`  

**其他注意事项：**  
- **通用提示：**  
  - 在支持 Markdown 链接的平台上，优先使用 Markdown 格式。  
  - 在分享链接时，保持摘要简洁，使用易于理解的文件标题。  
  - 除非用户询问，否则无需详细说明文件的传输方式。  

**最佳实践：**  
- 优先选择单一、高质量的文件作为链接内容。  
- 对于差异对比（Diff），推荐使用 `patch` 格式。  
- 为文件设置易于阅读的标题。  
- 在压缩能有效减少链接长度的情况下，优先使用 `lz` 格式。  

**避免的做法：**  
- **避免将文件内容直接放入查询参数中。**  
- **避免将文件内容上传到服务器。**  
- **除非确实需要，否则不要上传体积庞大的文件包。**  
- **除非渲染器提供了相应的字段，否则不要自行添加额外的字段。**