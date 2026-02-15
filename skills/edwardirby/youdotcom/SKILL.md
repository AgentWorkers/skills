---
name: youdotcom-cli
description: |
  Web search with livecrawl (search+extract) and content extraction for bash agents using You.com's @youdotcom-oss/api CLI.
  - MANDATORY TRIGGERS: You.com, youdotcom, YDC, @youdotcom-oss/api, web search CLI, livecrawl
  - Use when: web search needed, content extraction, URL crawling, real-time web data
license: MIT
compatibility: Requires Bun 1.3+ or Node.js 18+, and access to the internet
allowed-tools: Bash(bunx:@youdotcom-oss/api) Bash(npx:@youdotcom-oss/api) Bash(bunx:ydc) Bash(npx:ydc) Bash(jq:*)
metadata:
  author: youdotcom-oss
  version: "2.0.5"
  category: web-search-tools
  keywords: you.com,bash,cli,ai-agents,web-search,content-extraction,livecrawl,claude-code,codex,cursor
---

# 将 You.com 与基于 Bash 的 AI 代理集成

使用 You.com 的 `@youdotcom-oss/api` CLI，通过 `livecrawl`（搜索+提取）功能进行网页搜索，并提取内容，以供 Bash 代理使用。

## 安装

```bash
# Check prerequisites
node -v  # Requires Node.js 18+ or Bun 1.3+
# or
bun -v

# Recommended: Global installation (available system-wide)
npm install -g @youdotcom-oss/api
# or
bun add -g @youdotcom-oss/api

# Verify installation
ydc --version
```

## 快速入门

1. 从 https://you.com/platform/api-keys 获取 API 密钥。
2. 设置环境变量：
   ```bash
   export YDC_API_KEY="your-api-key-here"
   ```
3. 使用 `ydc` 命令执行操作：
   ```bash
   # Basic search
   ydc search --json '{"query":"AI news"}' --client YourAgentName
   
   # Search with livecrawl (get full page content instantly)
   ydc search --json '{
     "query":"documentation",
     "livecrawl":"web",
     "livecrawl_formats":"markdown"
   }' --client YourAgentName
   
   # Extract content from URL
   ydc contents --json '{
     "urls":["https://example.com"],
     "formats":["markdown"]
   }' --client YourAgentName
   ```

## 更新

```bash
# Update to latest version
npm update -g @youdotcom-oss/api
# or
bun update -g @youdotcom-oss/api
```

## 工作流程

### 1. 使用 `--client` 标志

* 在所有命令中都必须包含 `--client YourAgentName`。
* 使用您的代理标识符（例如：“ClaudeCode”、“Cursor”、“Codex”）。
* 这有助于支持错误报告的处理（错误报告包含在邮件链接中）。
* 示例：`ydc search --json '{"query":"..."}' --client ClaudeCode`

### 2. 验证 API 密钥

* 检查 `YDC_API_KEY` 环境变量是否已设置。
* 如果未设置，引导用户从 https://you.com/platform/api-keys 获取密钥。
* 提供命令：`export YDC_API_KEY="your-key"`

### 3. 使用 `--schema` 进行参数发现

* 使用 `ydc search --schema` 动态发现可用的参数。
* 使用 `ydc contents --schema` 查看内容提取选项。
* 解析 JSON 架构以编程方式构建查询。
* 示例：`ydc search --schema | jq '.properties | keys'`

### 4. 工具选择与执行

**如果** 用户提供了 URL → 使用 `ydc contents` 并设置 `"urls"` 参数。
**否则如果** 用户需要搜索并获取完整内容 → 使用 `ydc search` 并设置 `"livecrawl":"web"`。
**否则** → 直接使用 `ydc search`（不启用 `livecrawl` 功能）。

**注意事项：** 必须始终包含 `--json` 标志和 `--client YourAgentName`。
**退出代码：** 0=成功，1=API 错误，2=参数无效。
**常用过滤条件：** `freshness`、`site`、`country` 参数。

## 示例

### 架构发现
```bash
# Discover search parameters
ydc search --schema | jq '.properties | keys'

# See full schema for search
ydc search --schema | jq

# Discover contents parameters
ydc contents --schema | jq '.properties | keys'
```

### 搜索
```bash
# Basic search
ydc search --json '{"query":"AI news"}' --client YourAgent

# Search + extract full content (livecrawl)
ydc search --json '{"query":"docs","livecrawl":"web","livecrawl_formats":"markdown"}' --client YourAgent

# With filters
ydc search --json '{"query":"news","freshness":"week","site":"github.com"}' --client YourAgent

# Parse results
ydc search --json '{"query":"AI"}' --client YourAgent | jq -r '.results.web[] | "\(.title): \(.url)"'
```

### 提取内容
```bash
# Extract from URL
ydc contents --json '{"urls":["https://example.com"],"formats":["markdown"]}' --client YourAgent

# Multiple URLs
ydc contents --json '{"urls":["https://a.com","https://b.com"],"formats":["markdown"]}' --client YourAgent | jq -r '.[0].markdown'
```

## 故障排除

**退出代码：** 0=成功，1=API 错误，2=参数无效。

**常见解决方法：**
- “命令未找到：ydc” → `npm install -g @youdotcom-oss/api`
- “必须使用 `--json` 标志” → 确保总是使用 `--json '{"query":"..."}'`
- “需要 YDC_API_KEY” → 设置 `export YDC_API_KEY="your-key"`
- “401 错误” → 在 https://you.com/platform/api-keys 重新生成密钥。
- “429 速率限制” → 使用指数退避策略添加重试逻辑。

## 资源

* 包：https://github.com/youdotcom-oss/dx-toolkit/tree/main/packages/api
* API 密钥：https://you.com/platform/api-keys