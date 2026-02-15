---
name: zscore
description: 在 Zeru ERC-8004 身份注册表上注册代理节点，管理钱包和元数据，并读取链上的状态信息。当代理节点需要在线上注册、查询费用、读取代理信息、设置元数据或管理 Base Mainnet 或 Base Sepolia 上的代理钱包时，请使用该功能。
user-invocable: true
metadata: {"openclaw":{"requires":{"env":["PRIVATE_KEY"],"bins":["node","npx"]},"primaryEnv":"PRIVATE_KEY"}}
---

# Zeru ERC-8004 身份注册系统

在 Zeru 身份注册系统中注册和管理 AI 代理。默认使用 Base Mainnet（注册费用为 0.0025 ETH）。若需使用 Base Sepolia 测试网，请使用 `--chain 84532` 参数。

## 一次性设置

运行一次即可完成依赖项的安装：

```bash
cd {baseDir} && npm install
```

## 代理 JSON 结构（ERC-8004 注册-v1）

在注册代理时，需要提供一个描述代理的 JSON 文件。SDK 会自动填充 `type` 和 `registrations` 字段；如果省略了 `x402Support`、`active` 或 `image` 字段，也会使用默认值。

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
| `image` | string | 否 | 占位符 | 头像 URL（支持 HTTPS、IPFS 或 Arweave） |
| `services` | array | 是 | — | 代理提供的服务端点（最多 64 个） |
| `x402Support` | boolean | 否 | `false` | 是否支持 x402 支付协议 |
| `active` | boolean | 否 | `true` | 代理是否正在接受请求 |
| `supportedTrust` | string[] | 否 | — | 支持的信任模型：`"reputation"`、`"crypto-economic"`、`"tee-attestation"`、`"ERC-8004"` |
| `owner` | string | 否 | 所有者地址（从 `PRIVATE_KEY` 自动获取） |

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

### `/zscore register --json <file>`

使用完整的 JSON 文件注册新代理。系统会生成代理的 URI，在链上铸造 NFT，并将 URI 更新为代理的实际 ID。

```
/zscore register --json agent.json
/zscore register --json agent.json --chain 84532
```

**注册步骤：**
1. 创建符合上述结构的 JSON 文件（例如 `agent.json`）。
2. 运行命令：`npx tsx {baseDir}/scripts/zeru.ts register --json agent.json`

SDK 会自动添加 `type` 和 `registrations` 字段（其中 `agentId` 为占位符），并填充缺失的可选字段。铸造完成后，系统会用实际的代理 ID 更新 JSON 文档。

### `/zscore register --name <name> --description <desc> --endpoint <url>`

简化注册流程（仅使用单个 API 端点）。对于功能更丰富的代理，请使用 `--json` 选项。

```
/zscore register --name "Trading Bot" --description "AI-powered trading agent" --endpoint "https://mybot.com/api"
/zscore register --name "Data Analyzer" --description "Analyzes datasets" --endpoint "https://analyzer.ai/api" --image "https://example.com/icon.png"
/zscore register --name "Test Bot" --description "Testing" --endpoint "https://test.com" --chain 84532
```

需要 `PRIVATE_KEY` 环境变量。钱包中必须包含足够的费用和 Gas（例如，在 Mainnet 上约为 0.003 ETH）。

运行命令：`npx tsx {baseDir}/scripts/zeru.ts register --name "..." --description "..." --endpoint "..."`

### `/zscore read <agentId>`

读取代理的链上信息：所有者、URI、钱包地址和名称。

```
/zscore read 16
```

运行命令：`npx tsx {baseDir}/scripts/zeru.ts read 16`

### `/zscore fee`

查询当前的注册费用以及注册是否开放。

```
/zscore fee
```

运行命令：`npx tsx {baseDir}/scripts/zeru.ts fee`

### `/zscore set-metadata <agentId> --key <key> --value <value>`

为代理设置自定义元数据。仅所有者可以执行此操作。

```
/zscore set-metadata 16 --key "category" --value "trading"
```

需要 `PRIVATE_KEY`。

运行命令：`npx tsx {baseDir}/scripts/zeru.ts set-metadata 16 --key "category" --value "trading"`

### `/zscore unset-wallet <agentId>`

清空代理的钱包信息。仅所有者可以执行此操作。

```
/zscore unset-wallet 16
```

需要 `PRIVATE_KEY`。

运行命令：`npx tsx {baseDir}/scripts/zeru.ts unset-wallet 16`

## 设置

### 仅读模式（无需设置）

`read` 和 `fee` 命令无需私钥即可使用。

### 使用钱包（进行注册和数据操作）

将以下配置添加到您的 OpenClaw 配置文件（`~/.openclaw/openclaw.json`）：

```json
{
  "skills": {
    "entries": {
      "zscore": {
        "enabled": true,
        "env": {
          "PRIVATE_KEY": "0xYourFundedPrivateKey"
        }
      }
    }
  }
}
```

可选环境变量：
- `RPC_URL` — 替换默认的 RPC 地址
- `CHAIN_ID` — 更改链ID（默认为 Base Mainnet 的 8453，Base Sepolia 为 84532）

## 合约信息

### Base Mainnet（默认，链 ID 8453）
- **身份注册系统合约地址：** `0xFfE9395fa761e52DBC077a2e7Fd84f77e8abCc41`
- **声誉注册系统合约地址：** `0x187d72a58b3BF4De6432958fc36CE569Fb15C237`
- **注册费用：** 0.0025 ETH
- **RPC 地址：** https://mainnet.base.org

### Base Sepolia（测试网，链 ID 84532）
- **身份注册系统合约地址：** `0xF0682549516A4BA09803cCa55140AfBC4e5ed2E0`
- **声誉注册系统合约地址：** `0xaAC7557475023AEB581ECc8bD6886d1742382421`
- **注册费用：** 0.001 ETH
- **RPC 地址：** https://sepolia.base.org`
- **来源：** `zeru`

## 工作原理：
1. 使用 `register` 命令通过代理 URI API 创建一个符合 ERC-8004 标准的 JSON 文档，在身份注册系统上铸造 NFT（支付相关费用），然后使用代理的实际 ID 更新文档。
2. `read` 命令查询链上合约以获取代理的所有者信息、URI 和钱包地址。
3. `fee` 命令从合约中获取当前的注册费用和注册状态。
4. `set-metadata` 命令用于设置代理的元数据。
5. `unset-wallet` 命令用于清除代理的钱包信息。