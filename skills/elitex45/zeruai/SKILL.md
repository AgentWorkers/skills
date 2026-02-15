---
name: zeruai
description: 在 Zeru ERC-8004 身份注册表上注册代理节点，管理钱包和元数据，并读取链上的状态信息。当代理节点需要在链上注册、查询费用、读取代理信息、设置元数据或在 Base Mainnet 或 Base Sepolia 上管理代理钱包时，可使用该功能。
user-invocable: true
metadata: {"openclaw":{"requires":{"env":["PRIVATE_KEY"],"bins":["node","npx"]},"primaryEnv":"PRIVATE_KEY"}}
---

# Zeru ERC-8004 身份注册系统

在 Zeru 身份注册系统中，您可以注册和管理 AI 代理。默认使用 Base Mainnet（注册费用为 0.0025 ETH）。若需使用 Base Sepolia 测试网，请使用 `--chain 84532` 参数。

## 一次性设置

只需运行一次命令即可安装所有依赖项：

```bash
cd {baseDir} && npm install
```

## 代理 JSON 结构（ERC-8004 注册规范-v1）

在注册代理时，需要提供一个 JSON 文件来描述该代理。SDK 会自动填充 `type` 和 `registrations` 字段；如果省略了 `x402Support`、`active` 或 `image` 字段，也会使用默认值。

**最小 JSON 结构（仅包含名称、描述和一项服务）：**

```json
{
  "name": "My AI Agent",
  "description": "A helpful AI agent that does X",
  "services": [
    { "name": "web", "endpoint": "https://myagent.example.com" }
  ]
}
```

**完整 JSON 结构（支持 MCP、A2A、OASF 和 x402 支付）：**

```json
{
  "name": "DataAnalyst Pro",
  "description": "Enterprise-grade blockchain data analysis agent. Performs on-chain forensics, wallet profiling, and transaction pattern detection.",
  "image": "https://cdn.example.com/agents/analyst.png",
  "services": [
    {
      "name": "MCP",
      "endpoint": "https://api.dataanalyst.ai/mcp",
      "version": "2025-06-18",
      "mcpTools": ["analyze_wallet", "trace_transactions", "detect_anomalies"],
      "capabilities": []
    },
    {
      "name": "A2A",
      "endpoint": "https://api.dataanalyst.ai/.well-known/agent-card.json",
      "version": "0.3.0",
      "a2aSkills": ["analytical_skills/data_analysis/blockchain_analysis"]
    },
    {
      "name": "OASF",
      "endpoint": "https://github.com/agntcy/oasf/",
      "version": "0.8.0",
      "skills": ["analytical_skills/data_analysis/blockchain_analysis"],
      "domains": ["technology/blockchain"]
    },
    {
      "name": "web",
      "endpoint": "https://dataanalyst.ai"
    },
    {
      "name": "agentWallet",
      "endpoint": "eip155:8453:0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb7"
    }
  ],
  "x402Support": true,
  "active": true,
  "supportedTrust": ["reputation", "ERC-8004"]
}
```

**所有字段说明：**

| 字段 | 类型 | 是否必填 | 默认值 | 描述 |
|-------|------|----------|---------|-------------|
| `name` | string | 是 | — | 代理名称（1–256 个字符） |
| `description` | string | 是 | — | 代理的功能（最多 2048 个字符） |
| `image` | string | 否 | 占位符 | 代理头像的 URL（支持 HTTPS、IPFS 或 Arweave） |
| `services` | array | 是 | — | 代理提供的服务端点（最多 64 个） |
| `x402Support` | boolean | 否 | `false` | 是否支持 x402 支付协议 |
| `active` | boolean | 否 | `true` | 代理是否正在接受请求 |
| `supportedTrust` | string[] | 否 | — | 支持的信任模型：`"reputation"`、`"crypto-economic"`、`"tee-attestation"`、`"ERC-8004"` |
| `owner` | string | 否 | 所有者地址（从 `PRIVATE_KEY` 自动生成） |

**服务类型：**

| `name` | `endpoint` | 额外字段 |
|--------|-----------|--------------|
| `"web"` | 网站 URL | — |
| `"MCP"` | MCP 服务器 URL | `version`、`mcpTools[]`、`mcpPrompts[]`、`mcpResources[]`、`capabilities[]` |
| `"A2A"` | 代理卡片 URL (`/.well-known/agent-card.json`) | `version`、`a2aSkills[]` |
| `"OASF"` | OASF 仓库 URL | `version`、`skills[]`、`domains[]` |
| `"agentWallet"` | CAIP-10 地址（格式：`eip155:{chainId}:{address}`） | — |
| `"ENS"` | ENS 名称（例如 `myagent.eth`） | — |
| `"email"` | 电子邮件地址 | — |
| `custom` | 任意 URL | `description` |

## 命令

### `/zeruai register --json <file>`

使用完整的 JSON 文件注册新代理。系统会生成代理的 URI，在链上 mint NFT，并将 URI 更新为实际的代理 ID。

```
/zeruai register --json agent.json
/zeruai register --json agent.json --chain 84532
```

**注册步骤：**
1. 创建符合上述结构的 JSON 文件（例如 `agent.json`）。
2. 运行命令：`npx tsx {baseDir}/scripts/zeru.ts register --json agent.json`

SDK 会自动添加 `type` 和 `registrations` 字段（其中 `agentId` 为占位符），并填充缺失的可选字段。注册完成后，系统会用实际的代理 ID 更新 JSON 文档。

### `/zeruai register --name <name> --description <desc> --endpoint <url>`

简化注册流程（仅使用单个 API 端点）。如需更复杂的代理配置，请使用 `--json` 选项。

```
/zeruai register --name "Trading Bot" --description "AI-powered trading agent" --endpoint "https://mybot.com/api"
/zeruai register --name "Data Analyzer" --description "Analyzes datasets" --endpoint "https://analyzer.ai/api" --image "https://example.com/icon.png"
/zeruai register --name "Test Bot" --description "Testing" --endpoint "https://test.com" --chain 84532
```

**注意：** 需要设置 `PRIVATE_KEY` 环境变量。钱包中必须包含足够的费用（例如，在 Mainnet 上至少需要 0.003 ETH）。
运行命令：`npx tsx {baseDir}/scripts/zeru.ts register --name "..." --description "..." --endpoint "..."`

### `/zeruai read <agentId>`

查询代理的链上信息：所有者、URI、钱包地址和名称。

```
/zeruai read 16
```

运行命令：`npx tsx {baseDir}/scripts/zeru.ts read 16`

### `/zeruai fee`

查看当前的注册费用以及注册是否可用。

```
/zeruai fee
```

运行命令：`npx tsx {baseDir}/scripts/zeru.ts fee`

### `/zeruai set-metadata <agentId> --key <key> --value <value>`

为代理设置自定义元数据。仅所有者可以执行此操作。

```
/zeruai set-metadata 16 --key "category" --value "trading"
```

**注意：** 需要 `PRIVATE_KEY`。
运行命令：`npx tsx {baseDir}/scripts/zeru.ts set-metadata 16 --key "category" --value "trading"`

### `/zeruai unset-wallet <agentId>`

清除代理的钱包信息。仅所有者可以执行此操作。

```
/zeruai unset-wallet 16
```

**注意：** 需要 `PRIVATE_KEY`。
运行命令：`npx tsx {baseDir}/scripts/zeru.ts unset-wallet 16`

## 设置

### 仅读模式（无需额外设置）

`read` 和 `fee` 命令无需私钥即可使用。

### 使用钱包（进行注册和数据操作）

将以下配置添加到您的 OpenClaw 配置文件（`~/.openclaw/openclaw.json`）：

```json
{
  "skills": {
    "entries": {
      "zeruai": {
        "enabled": true,
        "env": {
          "PRIVATE_KEY": "0xYourFundedPrivateKey"
        }
      }
    }
  }
}
```

**可选环境变量：**
- `RPC_URL` — 替换默认的 RPC 地址
- `CHAIN_ID` — 更改链ID（默认为 Base Mainnet 的 8453，Base Sepolia 为 84532）

## 合约信息

### Base Mainnet（默认，chainId 8453）
- **身份注册系统合约地址：** `0xFfE9395fa761e52DBC077a2e7Fd84f77e8abCc41`
- **声誉注册系统合约地址：** `0x187d72a58b3BF4De6432958fc36CE569Fb15C237`
- **注册费用：** 0.0025 ETH
- **RPC 地址：** https://mainnet.base.org

### Base Sepolia（测试网，chainId 84532）
- **身份注册系统合约地址：** `0xF0682549516A4BA09803cCa55140AfBC4e5ed2E0`
- **声誉注册系统合约地址：** `0xaAC7557475023AEB581ECc8bD6886d1742382421`
- **注册费用：** 0.001 ETH
- **RPC 地址：** https://sepolia.base.org
- **来源：** `zeru`

## 工作原理：

1. 使用 `/zeruai register` 命令通过代理 URI API 创建 JSON 文档（符合 ERC-8004 注册规范-v1），在身份注册系统上 mint NFT（需支付费用），然后使用实际的代理 ID 更新文档。
2. 使用 `/zeruai read` 命令查询链上的代理信息（所有者、URI 和钱包地址）。
3. 使用 `/zeruai fee` 命令获取当前的注册费用和注册状态。
4. 使用 `/zeruai set-metadata` 命令为代理设置自定义元数据。
5. 使用 `/zeruai unset-wallet` 命令清除代理的钱包信息。