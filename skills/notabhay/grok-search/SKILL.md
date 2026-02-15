---
name: grok-search
description: 您可以使用 xAI 的服务器端工具（web_search、x_search）通过 xAI Responses API 在网页或 X/Twitter 上进行搜索。当您需要从 X（Twitter）获取推文、帖子或用户信息时，或者希望使用 Grok 作为 Brave 浏览器的替代方案时，都可以使用这些工具。此外，这些工具还能为您提供结构化的 JSON 数据以及相关引用信息。
homepage: https://docs.x.ai/docs/guides/tools/search-tools
triggers: ["grok", "xai", "search x", "search twitter", "find tweets", "x search", "twitter search", "web_search", "x_search"]
metadata: {"clawdbot":{"emoji":"🔎","requires":{"bins":["node"],"env":["XAI_API_KEY"]},"primaryEnv":"XAI_API_KEY"}}
---

**通过捆绑的脚本在本地运行 xAI Grok（支持搜索、聊天和模型列表功能）。** 搜索功能的默认输出为格式良好的 JSON 数据（对机器人友好），其中包含引用信息。

## API 密钥

脚本会按以下顺序查找 xAI API 密钥：
- `XAI_API_KEY` 环境变量
- `~/.clawdbot/clawdbot.json` 文件中的 `env.XAI_API_KEY`
- `~/.clawdbot/clawdbot.json` 文件中的 `skills.entries["grok-search"].apiKey`
- 备选方案：`skills.entries["search-x"].apiKey` 或 `skills.entries.xai.apiKey`

## 运行方式

使用 `{baseDir}` 参数，以确保命令在任何工作区布局下都能正常执行。

### 搜索功能

- **Web 搜索（JSON 格式）：**
  ```
  node {baseDir}/scripts/grok_search.mjs "<query>" --web
  ```

- **X/Twitter 搜索（JSON 格式）：**
  ```
  node {baseDir}/scripts/grok_search.mjs "<query>" --x
  ```

### 聊天功能

- **文本聊天：**
  ```
  node {baseDir}/scripts/chat.mjs "<prompt>"
  ```

- **图像聊天：**
  ```
  node {baseDir}/scripts/chat.mjs --image /path/to/image.jpg "<prompt>"
  ```

### 模型功能

- **列出所有模型：**
  ```
  node {baseDir}/scripts/models.mjs
  ```

## 有用的参数

- **--links-only**：仅输出引用链接
- **--text**：在格式良好的输出中隐藏引用信息
- **--raw**：将原始的 API 响应数据输出到标准错误流（用于调试）

**通用参数：**
- **--max <n>`：限制搜索结果数量（默认值为 8）
- **--model <id>`：指定要查询的模型（默认为 `grok-4-1-fast`）

**仅适用于 X 服务的过滤参数（通过 x_search 工具参数设置）：**
- **--days <n>`：指定搜索时间范围（例如：7 天）
- **--from YYYY-MM-DD** / **--to YYYY-MM-DD**：指定搜索时间范围
- **--handles @a,@b**：仅搜索指定的用户
- **--exclude @bots,@spam**：排除指定的用户

## 输出格式（JSON）

```json
{
  "query": "...",
  "mode": "web" | "x",
  "results": [
    {
      "title": "...",
      "url": "...",
      "snippet": "...",
      "author": "...",
      "posted_at": "..."
    }
  ],
  "citations": ["https://..."]
}
```

## 注意事项：

- 引用信息会尽可能从 xAI 的响应注释中获取并进行合并/验证（这比直接信任模型的 JSON 数据更可靠）。
- 对于 Twitter 或 Twitter 主题帖的搜索，建议使用 `--x` 参数；对于一般搜索任务，建议使用 `--web` 参数。