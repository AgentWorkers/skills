---
name: prospairrow-websites-mcp
description: 通过高质量的销售线索来增加收入。让您的AI代理直接访问Prospairrow——提取潜在客户信息，深入了解这些公司的详细情况，发现竞争对手，并生成适合内容营销的材料。利用这些丰富的客户资料（如公司概况、技术栈和关键联系人信息）来推动销售流程，帮助您的团队更快地完成交易。
metadata: {"openclaw":{"requires":{"bins":["bash","node"],"config":["skills.entries.mcporter.config.servers.websites-mcp.url"],"env":["PROSPAIRROW_API_KEY"]},"primaryEnv":"PROSPAIRROW_API_KEY"}}
---
# Prospairrow Websites MCP

该技能允许您的人工智能代理直接访问 Prospairrow 的人工智能驱动的潜在客户开发平台。它提供的信息远不止基本的公司概况：还包括详细的公司信息、技术栈、关键联系人、竞争对手情报以及内容营销数据，从而帮助销售团队避免浪费时间在不符合要求的潜在客户身上，更快地促成交易。

当用户希望通过 MCP/API 执行 Prospairrow 的相关操作时，可以使用此技能。

## 运行时环境

完整的运行时代码源代码包含在这个技能包中（`runtime/` 目录）。无需外部 git 克隆。只需将代码包安装到本地，然后运行 `npm install --ignore-scripts` 来获取 npm 依赖项（其中包括 Playwright，Playwright 会在首次使用时下载浏览器二进制文件）。

```bash
bash {baseDir}/scripts/install-runtime.sh
```

## 商业价值

- **更快地达成交易**：通过获取详细的公司信息和技术栈数据，制定出能够打动决策者的个性化销售方案。
- **精准定位目标客户**：避免在不符合要求的潜在客户上浪费时间，利用丰富的数据提高销售机会。
- **发现竞争对手**：自动为每个潜在客户提供竞争对手的相关信息。
- **生成内容营销素材**：直接根据潜在客户的数据生成有针对性的内容营销材料。
- **无需外部 git 克隆**：运行时代码已包含在技能包中，依赖项会在安装时从 npm 注册表中自动下载。

## 支持的任务

- `extract_prospects`（只读）
- `add_prospects`（写入）
- `enrich_prospects`（写入）
- `get_prospect_detail`（只读）
- `generate_content_marketing`（写入）
- `discover_competitors`（写入；需要提供 `prospect_id`、`company` 或 `website` 参数；若未提供，则通过搜索确定相关 ID）

## 安装运行时环境

运行时环境的安装路径为：

- `$HOME/.openclaw/runtime/websites-mcp`

## OpenClaw 配置

在 `~/.openclaw/openclaw.json` 文件中配置如下：

- `skills.entries.mcporter.config.defaultServer = "websites-mcp"`
- `skills.entries.mcporter.config.servers.websites-mcp.url = "http://127.0.0.1:8799"`

**为什么使用 `mcporter`？**：这个键用于存储 MCP 服务器的路由配置信息，与用于 API 认证信息的 Prospairrow 配置是分开的。

## API 密钥的获取顺序

1. 请求头中的 `Authorization` 或 `X-API-Key`；
2. OpenClaw 的技能配置文件中的 `skills.entries.prospairrow-websites-mcp.apiKey` 或 `skills.entries.prospairrow-websites-mcp.env.PROSPAIRROW_API_KEY`；
3. 如果上述方式都无效，则使用环境变量 `PROSPAIRROW_API_KEY`。

## MCP 请求的格式

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "websites.run_task",
  "params": {
    "siteId": "prospairrow",
    "taskId": "generate_content_marketing",
    "params": {
      "positioning_intensity": 6
    }
  }
}
```

## 前提条件

- 确保 `websites-mcp` 服务器可访问（默认地址为 `127.0.0.1:8799`）；
- 执行写入操作需要启用写入功能的运行时环境；
- 运行时环境必须通过配置文件或环境变量提供 API 密钥。