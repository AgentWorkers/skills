---
name: intel-asrai
description: 通过 Base 平台上的 x402 微支付技术实现的人工智能驱动的网络搜索功能。搜索结果会包含带有引用来源的合成答案。每次搜索的费用为 0.005 美元（USDC），费用直接从您的钱包中扣除。无需 API 密钥或订阅服务，只需连接网络后即可开始搜索。
license: MIT
metadata: {"openclaw":{"emoji":"🔍","requires":{"env":["INTEL_PRIVATE_KEY"]}},"clawdbot":{"emoji":"🔍","requires":{"env":["INTEL_PRIVATE_KEY"]}}}
---
# Intel — 通过 x402 实现的 AI 网络搜索

## 安装

```bash
npx -y -p intel-asrai-mcp install-skill
```

系统会自动检测 OpenClaw、Cursor、Cline 等智能代理。然后请设置您的密钥：

```
INTEL_PRIVATE_KEY=0x<your_private_key>  # add to ~/.env
```

对于 MCP 代理（Cursor、Cline、Claude Desktop），还需将其添加到配置文件中：

```json
{
  "mcpServers": {
    "intel-search": { "command": "npx", "args": ["-y", "intel-asrai-mcp"] }
  }
}
```

---

当用户询问当前事件、最新新闻、实时价格或任何需要超出您训练数据范围的最新信息时，可以使用 Intel 搜索功能。

## 适用场景

- 当前事件、突发新闻、最新进展 → 使用搜索功能
- 实时价格、比分、实时数据 → 使用搜索功能
- 需要最新资料的研究 → 使用搜索功能
- 您已经非常熟悉的一般性知识 → 不需要使用搜索功能（每次搜索费用为 0.005 美元）

## 搜索方法

### 如果 intel_search 工具可用（MCP 已连接）

```
intel_search(query, mode, sources)
```

### 如果没有 MCP 工具 — 使用 bash（OpenClaw 及其他代理）

```bash
npx -y -p intel-asrai-mcp intel-search "<query>" <mode> <sources>
```

示例：
```bash
npx -y -p intel-asrai-mcp intel-search "bitcoin price today" speed web
npx -y -p intel-asrai-mcp intel-search "latest AI research" quality academic
npx -y -p intel-asrai-mcp intel-search "what people think about X" balanced discussions
```

请确保在 `~/.env` 文件中设置了 `INTEL_PRIVATE_KEY`。搜索费用（0.005 美元）会自动从用户的钱包中扣除。

## 参数

- **query** — 搜索内容
- **mode** — `speed`（快速）、`balanced`（默认）、`quality`（深度研究）
- **sources** — `web`（默认）、`academic`（论文）、`discussions`（Reddit/论坛）

## 输出规则

- 以合成后的答案开头，无需前言
- 将信息来源以编号链接的形式列在答案之后
- 对于事实性问题：先给出直接答案，再提供详细信息
- 对于新闻：先列出关键内容，再提供来源
- 回答中切勿提及工具名称、API 调用或支付细节
- 保持简洁：仅提供合成后的结果，避免冗长信息

## 费用

每次搜索费用为 0.005 美元，费用会从用户位于 Base 主网的钱包中自动扣除。如有需要，请告知用户。