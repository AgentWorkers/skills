---
name: pond3r-skill
description: 通过Pond3r MCP查询加密情报——该平台提供精选的数据集、SQL查询工具、协议指标、收益数据以及市场分析功能。当代理需要DeFi相关数据、稳定币的收益信息、代币投资机会、Polymarket的交易记录、跨协议比较结果或区块链分析报告时，可使用该服务。
---

# Pond3r 加密情报技能

当代理需要查询加密/去中心化金融（DeFi）数据时，可以使用此技能：收益数据、协议指标、代币投资机会、市场分析或区块链分析。Pond3r 提供了一个具有只读 SQL 访问权限的 MCP 服务器，用于访问精心筛选的数据集。

## 先决条件

- **API 密钥**：请在 [makeit.pond3r.xyz/api-keys](https://makeit.pond3r.xyz/api-keys) 获取。
- **MCP 配置**：必须在运行时环境中将 Pond3r 配置为 MCP 服务器（支持 Claude Code、Cursor、Claude Desktop 等平台）。

## 设置：代理运行在哪里？

代理需要 **MCP 工具**（`list_datasets`、`get_schema`、`query`）来使用 Pond3r。这些工具来自执行代理的 **运行时环境**，而不仅仅来自该技能或环境变量。

| 运行时环境 | 启用 Pond3r 的方法 |
|---------|------------------------|
| **Cursor** | 在 Cursor 设置中 → “MCP 服务器” → 添加服务器（URL + 授权头）。请参阅下面的 [MCP 连接](#mcp-connection)。 |
| **Claude Desktop** | 在 `claude_desktop_config.json` 的 `mcpServers` 下添加 Pond3r。然后重启 Claude。 |
| **Claude Code** | 运行 `claude mcp add pond3r-data ...`（具体命令请参见下文）。 |
| **OpenClaw (Docker/Telegram)** | 使用下面的 **CLI 脚本**。这些脚本通过 HTTP 调用 Pond3r MCP。在 `.env` 文件中设置 `POND3R_API_KEY`；代理会运行脚本并解析 JSON 输出。 |

**代理无需额外配置**——该技能已包含所有必要信息。对于支持原生 MCP 的运行时环境，只需在 MCP 服务器配置中添加 API 密钥。对于 OpenClaw，使用 CLI 脚本并在 `.env` 中设置 `POND3R_API_KEY`。

## MCP 连接

| 设置 | 值 |
|---------|-------|
| URL | `https://mcp.pond3r.xyz/mcp` |
| 传输方式 | Streamable HTTP |
| 授权方式 | `Authorization: Bearer <API_KEY>` |

### Cursor

1. 打开 **Cursor** → **设置**（⌘+）→ **MCP**
2. 单击 **添加新的 MCP 服务器**
3. 配置：
   - **URL**：`https://mcp.pond3r.xyz/mcp`
   - **授权头**：`Authorization: Bearer <YOUR_POND3R_API_KEY>`
     - 将 `<YOUR_POND3R_API_KEY>` 替换为从 [makeit.pond3r.xyz/api-keys](https://makeit.pond3r.xyz/api-keys) 获取的密钥
     - 如果设置了环境变量 `POND3R_API_KEY`，某些客户端也支持 `Authorization: Bearer ${POND3R_API_KEY`
4. 保存设置并 **重启 Cursor**，以便工具能够加载
5. 验证：启动一个新的聊天会话并请求稳定币的收益数据——代理应能够调用 `list_datasets`、`get_schema`、`query` 函数。

### Claude Code

```bash
claude mcp add pond3r-data \
  --transport http \
  https://mcp.pond3r.xyz/mcp \
  --header "Authorization: Bearer <API_KEY>"
```

### Claude Desktop (claude_desktop_config.json)

```json
{
  "mcpServers": {
    "pond3r": {
      "type": "http",
      "url": "https://mcp.pond3r.xyz/mcp",
      "headers": {
        "Authorization": "Bearer <API_KEY>"
      }
    }
  }
}
```

## CLI 脚本（OpenClaw / 任何运行时环境）

当无法使用 MCP 工具时（例如在 OpenClaw/Telegram 中），可以使用这些脚本。它们通过 HTTP 调用 Pond3r MCP。**需要在环境变量中设置 `POND3R_API_KEY`**（例如在 docker-compose 配置文件中）。

脚本位于 Docker 镜像的 `/opt/pond3r-skill-scripts/` 目录下。在本地运行时，可以使用 `ceo-agent/skills/pond3r-skill/scripts/` 或工作区相对路径。

### 1) 列出所有数据集

```bash
node /opt/pond3r-skill-scripts/list-datasets.mjs
```

输出：包含所有数据集和表格的 JSON 数据。

### 2) 获取数据集的架构信息

```bash
node /opt/pond3r-skill-scripts/get-schema.mjs --dataset-id <dataset_id>
```

### 3) 运行 SQL 查询

```bash
node /opt/pond3r-skill-scripts/query.mjs --dataset-id <dataset_id> --sql "SELECT * FROM stablecoin_yields LIMIT 10"
```

或者通过文件执行：

```bash
node /opt/pond3r-skill-scripts/query.mjs --sql-file /tmp/query.sql
```

### 脚本工作流程

1. 运行 `list-datasets.mjs` 以获取数据集和表格名称。
2. 运行 `get-schema.mjs --dataset-id <id>` 以查看列名和数据类型。
3. 运行 `query.mjs --dataset-id <id> --sql "SELECT ..."`，并使用有效的 SQL 语句（仅支持 SELECT 语句，使用简化的表格名称，必要时使用 LIMIT 限制）。
4. 解析 JSON 输出结果并向用户展示。

### 错误处理

- **缺少必要的环境变量：POND3R_API_KEY** → 在 `.env` 文件中添加 `POND3R_API_KEY` 并确保其已被正确加载（例如通过 docker-compose 的 `env_file: .env` 配置）。
- **Pond3r MCP 返回 401 错误** → API 密钥无效或已过期；请在 [makeit.pond3r.xyz/api-keys] 更新密钥。
- **Pond3r MCP 报错**：检查 SQL 语法、表格名称和行数限制。

## 可用的工具（原生 MCP）

| 工具 | 功能 |
|------|---------|
| `list_datasets` | 列出所有数据集及其对应的表格 |
| `get_schema` | 获取数据集的列名、数据类型和描述 |
| `query` | 对数据集执行只读 SQL 操作 |

## 查询规则

- **仅支持 SELECT 操作** — 不允许写入数据 |
- **使用简化的表格名称** — 例如使用 `SELECT * FROM stablecoin_yields`，而不是完整的路径 |
- **结果限制为 10,000 行** — 对于大型数据集，请使用 `LIMIT` 或 `WHERE` 过滤条件 |
- **成本估算** — 超过规定限制的查询请求会被拒绝

## 使用场景

1. **协议情报**：
   - 监控 AI 代理的启动情况、代币的发行、协议指标
   - 收集 Aave、Compound、Convex 等平台的每日收益报告

2. **市场机会检测**：
   - 在 Uniswap 上发现流动性上升的新代币
   - 市值低于 500 万美元且流动性上升的代币
   - 在 Polymarket 上交易量最大的代币

3. **风险调整分析**：
   - 多维度风险评分（波动性、流动性、市场结构）
   - 监控去中心化金融头寸的清算风险
   - 跟踪大型投资者的交易活动

4. **跨协议和跨链分析**：
   - 比较 Arbitrum 平台上 Aave 和 Compound 的 USDC 收益情况
   - 分析桥接平台的交易量、生态系统健康状况
   - 发现套利机会

5. **用于决策的结构化数据**：
   - 统计分析、趋势识别
   - 交易量模式分析、异常交易行为
   - 情感分析（使用 Farcaster 或其他工具评估用户情绪）

## 示例查询（自然语言 → SQL）

代理以自然语言提问；MCP 工具会解析查询并执行相应的 SQL 语句。示例问题包括：

- “当前以太坊上收益最高的 5 种稳定币是什么？”
- “显示过去 24 小时内 Polymarket 上交易量最大的交易记录。”
- “比较 Arbitrum 平台上 Aave 和 Compound 的 USDC 收益情况。”

## 工作流程

1. **发现可用数据**：调用 `list_datasets` 以获取数据集和表格列表。
2. **了解数据集架构**：使用 `get_schema` 获取所需数据集的详细信息。
3. **编写并执行查询**：使用有效的 SQL 语句（仅支持 SELECT 操作，使用简化的表格名称，必要时使用 LIMIT 限制）。
4. **解析结果**：利用返回的数据进行分析、制定决策或生成报告。

## 运行时环境要求（强制执行）

在使用 Pond3r 提供的数据之前，请确保：

1. **当 MCP 工具不可用时优先使用脚本**：
   - 如果运行时环境不提供 `list_datasets`、`get_schema`、`query` 等工具，请使用 [CLI 脚本](#cli-scripts-openclaw--any-runtime)。
   - 运行 `node /opt/pond3r-skill-scripts/list-datasets.mjs`（或工作区路径），并在环境变量中设置 `POND3R_API_KEY`。
2. **如果 MCP 和脚本都无法使用**：
   - 停止操作并返回错误信息：`Pond3r 无法使用：MCP 工具缺失或脚本执行失败（请检查环境变量中的 `POND3R_API_KEY`）。
3. **不要自动切换到其他数据源**：
   - 除非用户明确同意，否则不要切换到 `web_search`、`web_fetch` 等替代方案。
4. **提供执行日志**：
   - 包括实际执行的命令以及返回的数据集/查询结果。
   - 如果查询失败，请提供详细的错误信息和后续处理步骤。

## 故障排除

| 故障现象 | 解决方案 |
|---------|-----|
| “Pond3r MCP 未配置” | 在运行时环境中添加 MCP 服务器（Cursor/Claude），并设置正确的 URL 和授权头。然后重启应用。 |
| 配置完成后工具仍然无法使用** | 重启应用（Cursor/Claude）。MCP 服务器应在启动时自动加载。 |
| 代理在 OpenClaw/Telegram 中运行** | 使用 CLI 脚本，并在 `.env` 文件中设置 `POND3R_API_KEY`。请参阅 [CLI 脚本](#cli-scripts-openclaw--any-runtime)。 |
| 出现授权错误（例如 401 错误）** | 确保 API 密钥有效且未过期。如有需要，请更新密钥。 |

## 备用方案

- 如果 MCP 工具不可用，仅提供以下信息：
  - 缺失的工具名称
  - 必需的服务器 URL（`https://mcp.pond3r.xyz/mcp`）
  - 正确的授权头格式（`Authorization: Bearer <API_KEY>`）
- 如果 SQL 查询被拒绝（由于权限或资源限制），请调整查询条件（使用更严格的 `WHERE`/`LIMIT`）并重试。
- 如果访问或授权失败，请报告错误原因并请求验证 API 密钥或服务器配置。

## 报告功能（替代方案）

对于定期报告和结构化 JSON 数据的交付，可以使用 REST API：

- **创建报告**：`POST https://api.pond3r.xyz/v1/api/reports`，并提供 `description`、`schedule`、`delivery_format` 参数
- **获取最新报告**：`GET https://api.pond3r.xyz/v1/api/reports/{reportId}/latest`
- **请求头**：`x-api-key: <API_KEY>`

报告格式包含 `executiveSummary`、`analysis`、`opportunities` 等字段。有关完整的 API 详情和响应结构，请参阅 [reference.md](reference.md)。

## 安全注意事项

- **切勿在客户端代码或公共仓库中暴露 API 密钥**  
- 使用环境变量来存储 API 密钥  
- MCP 工具仅支持读取操作，不允许对 Pond3r 的数据集进行写入  
- 严禁在日志、聊天记录或命令输出中显示敏感信息（仅报告 API 是否可用）  
- 如果敏感信息被泄露，请立即更新 API 密钥。