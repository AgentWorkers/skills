---
name: prospairrow-websites-mcp
description: 通过高质量的销售线索来增加收入。让您的AI代理直接访问Prospairrow平台：提取潜在客户信息，深入了解这些公司的具体情况，发现竞争对手，并生成适合内容营销的材料。利用这些丰富的客户信息（如公司概况、技术栈和关键联系人数据），为您的销售团队提供有力支持，从而加速销售流程的完成。
metadata: {"openclaw":{"requires":{"bins":["bash","node"],"config":["skills.entries.mcporter.config.servers.websites-mcp.url"],"env":["PROSPAIRROW_API_KEY"]},"primaryEnv":"PROSPAIRROW_API_KEY"}}
---
# Prospairrow Websites MCP

该技能允许您的人工智能代理直接访问 Prospairrow 的智能商机挖掘平台。它提供的信息远超基本资料，包括深入的公司概况、技术栈、关键联系人、竞争对手情报以及内容营销数据，帮助销售团队避免浪费时间在不符合条件的潜在客户上，从而更快地促成交易。

当用户希望通过 MCP/API 执行 Prospairrow 相关操作时，可以使用此技能。

## 运行时环境

完整的运行时源代码托管在这个仓库中。您可以在本地安装该仓库的代码，并运行 `npm install --ignore-scripts` 命令来获取所需的 npm 依赖项（其中包含 Playwright，该工具会在首次使用时下载浏览器二进制文件）。

```bash
bash {baseDir}/scripts/install-runtime.sh
```

## 商业价值

- **更快地促成交易**：通过获取详细的公司信息和关键联系人数据，制定出能够打动决策者的个性化销售方案。
- **精准定位目标客户**：避免在不符合条件的潜在客户上浪费时间，通过丰富公司数据来最大化销售机会。
- **发现竞争对手**：自动为每个潜在客户提取竞争对手信息。
- **生成内容营销素材**：直接根据潜在客户数据生成有针对性的营销内容。
- **无需外部 Git 仓库**：运行时所需的代码已包含在技能包中，npm 依赖项会在安装时从 npm 仓库下载。

## 支持的任务

- `extract_prospects`（仅读取）
- `list_icp_qualified_companies`（仅读取）
- `get_icp_score`（仅读取）
- `get_company_score`（仅读取）
- `apollo_enrich`（写入）
- `add_prospects`（写入）
- `enrich_prospects`（写入）
- `get_prospect_detail`（仅读取）
- `generate_content_marketing`（写入）
- `generate_position_solution`（写入；通过 `/api/v1/prospects/{id}/position-solution` 路径发送请求，支持 `prospect_id`、`company` 或 `website` 作为参数）
- `discover_competitors`（仅读取；如果未直接提供参数，会通过搜索来确定相关公司的 ID）

## 安装运行时环境

运行时环境的安装路径为：
```
$HOME/.openclaw/runtime/websites-mcp
```

## OpenClaw 配置

请在 `~/.openclaw/openclaw.json` 文件中配置以下内容：
```json
"skills.entries.mcporter.config.defaultServer = "websites-mcp"
"skills.entries.mcporter.config.servers.websites-mcp.url = "http://127.0.0.1:8799"
```

**关于 `mcporter` 的说明**：这个配置键用于存储 MCP 服务器的路由信息，与用于 API 认证的 Prospairrow 配置键是分开的。

## API 密钥的获取顺序

API 密钥的获取顺序如下：
1. 从请求头（`Authorization` 或 `X-API-Key`）中获取。
2. 如果没有找到密钥，则从环境变量 `PROSPAIRROW_API_KEY` 中获取。
3. （可选）如果启用了 OpenClaw 的相关配置（默认关闭），则从以下配置中获取：
   - `skills.entries.prospairrow-websites-mcp.apiKey`
   - `skills.entries.prospairrow-websites-mcp.env.PROSPAIRROW_API_KEY`

## 安全设置

- `WEBSITES_ALLOW_OPENCLAW_CONFIG_API_KEY=1`：允许在需要时从 `~/.openclaw/openclaw.json` 文件中读取 API 密钥。
- `WEBSITES_LOG_INVOCATIONS=1`：启用日志记录（默认关闭）。
- `WEBSITES_DISABLE_STORAGE_STATE_WRITE=1`：禁止将浏览器存储状态写入 `secrets/<site>/auth.json` 文件。

## MCP 请求格式

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

- 确保 `websites-mcp` 服务器可用（默认地址为 `127.0.0.1:8799`）。
- 执行写入操作时，运行时环境必须处于允许写操作的模式。
- 运行时环境必须通过配置或环境变量设置 API 密钥。