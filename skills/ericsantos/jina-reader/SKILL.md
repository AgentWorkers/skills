---
name: jina-reader
description: "通过 Jina AI Reader API 提取网页内容。提供三种模式：  
1. **读取模式（Read Mode）**：将 URL 转换为 Markdown 格式。  
2. **搜索模式（Search Mode）**：结合网页搜索功能提取完整内容。  
3. **事实核查模式（Ground Mode）**：用于对提取的内容进行事实核查。  
该工具能够安全地提取网页内容，同时不会暴露服务器的 IP 地址。"
homepage: https://jina.ai/reader
metadata: {"clawdbot":{"emoji":"📖","requires":{"bins":["curl","jq"]},"primaryEnv":"JINA_API_KEY"}}
---

# Jina Reader

通过 Jina AI 提取干净的网络内容——无需暴露您的服务器 IP。

## 阅读一个 URL

```bash
{baseDir}/scripts/reader.sh "https://example.com/article"
```

## 在网页中搜索（显示前 5 个结果及完整内容）

```bash
{baseDir}/scripts/reader.sh --mode search "latest AI news 2025"
```

## 核实某个陈述的真实性

```bash
{baseDir}/scripts/reader.sh --mode ground "OpenAI was founded in 2015"
```

## 选项

| 标志 | 描述 | 默认值 |
|------|-------------|---------|
| `--mode` | `read`（阅读）、`search`（搜索）、`ground`（验证） | `read` |
| `--selector` | 用于提取特定内容的 CSS 选择器 | — |
| `--wait` | 在提取内容前需要等待的 CSS 选择器 | — |
| `--remove` | 需要移除的 CSS 选择器（用逗号分隔） | — |
| `--proxy` | 地理代理的国家代码（如 `br`、`us` 等） | — |
| `--nocache` | 强制获取最新内容（跳过缓存） | 关闭 |
| `--format` | 输出格式：`markdown`、`html`、`text`、`screenshot` | `markdown` |
| `--json` | 原始 JSON 格式输出 | 关闭 |

## 示例

```bash
# Extract article content
{baseDir}/scripts/reader.sh "https://blog.example.com/post"

# Extract specific section via CSS selector
{baseDir}/scripts/reader.sh --selector "article.main" "https://example.com"

# Remove nav and ads before extraction
{baseDir}/scripts/reader.sh --remove "nav,footer,.ads" "https://example.com"

# Search with JSON output
{baseDir}/scripts/reader.sh --mode search --json "AI enterprise trends"

# Read via Brazil proxy
{baseDir}/scripts/reader.sh --proxy br "https://example.com.br"

# Fact-check a claim
{baseDir}/scripts/reader.sh --mode ground "Tesla is the most valuable car company"
```

## API 密钥

```bash
export JINA_API_KEY="jina_..."
```

免费 tier：提供 1000 万个令牌（无需注册）。获取密钥请访问：https://jina.ai/reader/

## 价格

- **阅读**：每页约 0.005 美元（标准价格） | ReaderLM-v2 的价格为每页 0.15 美元 |
- **搜索**：固定费用为 1 万个令牌，每个搜索结果额外收取费用 |
- **验证**：每次请求消耗约 30 万个令牌（延迟约 30 秒）

## 为什么选择 Jina Reader？

- **IP 保护**：请求通过 Jina 的基础设施传输，而非您的服务器 |
- **易于阅读的格式**：提取的内容为格式良好的 Markdown 格式，支持可选的 ReaderLM-v2 处理 |
- **动态内容处理**：使用无头 Chrome 浏览器执行 JavaScript 动作 |
- **结构化提取**：支持使用 JSON 模式进行数据提取