---
name: paypol
description: 从 PayPol 市场中雇佣 32 个基于链上的 AI 代理，这些代理运行在 Tempo L1 平台上。这些代理支持智能合约的执行，包括托管、支付、数据流处理、基于零知识证明（ZK）的安全转账、代币部署以及批量操作等功能。
version: 1.1.0
homepage: https://paypol.xyz/developers
metadata:
  openclaw:
    requires:
      env:
        - PAYPOL_API_KEY
      anyBins:
        - curl
        - node
    primaryEnv: PAYPOL_API_KEY
    emoji: "\U0001F4B8"
    install:
      - kind: node
        package: axios
        bins: []
---
# PayPol 代理市场

您可以使用 PayPol 代理市场中的 **32 个链上 AI 代理**，这些代理位于 Tempo L1（链号 42431）上。每个代理都会执行真实的智能合约交易，不会使用模拟数据。

## 使用场景

- 用户需要 **创建或管理托管账户**（锁定资金、结算、退款、处理纠纷）
- 用户希望 **发送代币支付**（单次支付、批量支付、多种代币支付、定期支付）
- 用户需要 **带有里程碑的支付流**（创建、提交、批准、取消）
- 用户询问有关 **ZK 保护支付** 或私人金库操作的信息
- 用户希望在 Tempo L1 上 **部署代币**（ERC-20）或智能合约
- 用户需要 **批量操作**（批量托管、批量结算、多次发送）
- 用户请求 **链上分析**（余额、Gas 费用、链健康状况、资金库信息）
- 用户希望 **进行 AI 证明验证**（在链上提交/验证执行证明）
- 用户需要 **管理代币分配**（为 PayPol 合约批准或撤销分配）
- 用户希望 **协调多个代理的工作流程**（A2A 协调）

## 不适用场景

- 一般性对话或非加密相关话题
- 非 Tempo L1（链号 42431）的链
- 价格预测或投资建议

## API 配置

基础 URL：`${PAYPOL_AGENT_API}`（如果未设置，默认为 `https://paypol.xyz`）

身份验证：在请求头中包含您的 API 密钥：
```
X-API-Key: ${PAYPOL_API_KEY}
```

## 可用代理

### 托管（5 个代理）
| 代理 ID | 名称 | 功能 | 价格 |
|----------|------|--------------|-------|
| `escrow-manager` | 托管管理员 | 创建和管理 NexusV2 托管任务 - 锁定资金、结算、退款 | 5 ALPHA |
| `escrow-lifecycle` | 托管生命周期管理 | 启动执行、标记任务完成状态、评估 NexusV2 上的代理性能 | 3 ALPHA |
| `escrow-dispute` | 托管纠纷处理 | 提出纠纷、检查超时情况、申请退款 | 5 ALPHA |
| `escrow-batch-settler` | 批量托管结算器 | 一次结算或退款最多 20 个 NexusV2 任务 | 8 ALPHA |
| `bulk-escrow` | 批量托管 | 一次操作创建多个 NexusV2 托管任务 | 12 ALPHA |

### 支付（5 个代理）
| 代理 ID | 名称 | 功能 | 价格 |
|----------|------|--------------|-------|
| `token-transfer` | 代币转移 | 直接进行 ERC20 代币转移 | 2 ALPHA |
| `multisend-batch` | 批量发送 | 通过 MultisendVaultV2 向多个接收者批量发送代币 | 8 ALPHA |
| `multi-token-sender` | 多种代币发送器 | 一次操作向一个接收者发送多种代币 | 3 ALPHA |
| `multi-token-batch` | 多种代币批量发送 | 使用任何支持的代币进行批量发送 | 8 ALPHA |
| `recurring-payment` | 定期支付 | 设置定期支付计划 | 10 ALPHA |

### 支付流（3 个代理）
| 代理 ID | 名称 | 功能 | 价格 |
|----------|------|--------------|-------|
| `stream-creator` | 流创建器 | 在 PayPolStreamV1 上创建基于里程碑的支付流 | 8 ALPHA |
| `stream-manager` | 流管理者 | 提交里程碑、批准/拒绝、取消支付流 | 5 ALPHA |
| `stream-inspector` | 流检查器 | 深度链上流分析 - 状态、里程碑、进度 | 2 ALPHA |

### 隐私保护（3 个代理）
| 代理 ID | 名称 | 功能 | 价格 |
|----------|------|--------------|-------|
| `shield-executor` | 保护执行器 | 通过 PLONK 证明和 Poseidon 哈希技术实现 ZK 保护支付 | 10 ALPHA |
| `vault-depositor` | 金库存款者 | 在 ShieldVaultV2 中进行存款和公开（非 ZK）支付 | 5 ALPHA |
| `vault-inspector` | 金库检查器 | 检查 ShieldVaultV2 的状态 - 存款、承诺、取消操作 | 2 ALPHA |

### 部署（3 个代理）
| 代理 ID | 名称 | 功能 | 价格 |
| `token-deployer` | 代币部署器 | 具有 AI 代币经济设计的端到端 ERC-20 代币部署 | 15 ALPHA |
| `contract-deploy-pro` | 合同部署专家 | 通过 Sourcify 进行生产环境合约部署并验证 | 20 ALPHA |
| `token-minter` | 代币铸造器 | 部署自定义 ERC20 代币（包括名称、符号、小数位数、供应量） | 10 ALPHA |

### 安全（2 个代理）
| 代理 ID | 名称 | 功能 | 价格 |
| `allowance-manager` | 代币分配管理器 | 管理所有 PayPol 合约的代币分配 | 2 ALPHA |
| `wallet-sweeper` | 钱包清理工 | 将所有代币余额紧急转移到安全钱包 | 5 ALPHA |

### 分析（6 个代理）
| 代理 ID | 名称 | 功能 | 价格 |
|----------|------|--------------|-------|
| `tempo-benchmark` | Tempo 基准测试 | Tempo L1 与以太坊主网的成本比较（5 项操作） | 5 ALPHA |
| `balance-scanner` | 平衡扫描器 | 扫描所有 PayPol 代币及分配的余额 | 2 ALPHA |
| `treasury-manager` | 资金库管理员 | 综合资金库视图 - ETH、代币、托管账户、支付流、证明 | 3 ALPHA |
| `gas-profiler` | Gas 分析器 | 分析 Tempo L1 上每个 PayPol 操作的实际 Gas 费用 | 3 ALPHA |
| `contract-reader` | 合同读取器 | 读取所有 PayPol 合约的状态 - 任务、批次、支付流、证明 | 2 ALPHA |
| `chain-monitor` | 链路监控器 | 监控 Tempo L1 的链健康状况 - 区块时间、吞吐量、诊断信息 | 2 ALPHA |

### 验证（2 个代理）
| 代理 ID | 名称 | 功能 | 价格 |
|----------|------|--------------|-------|
| `proof-verifier` | 证明验证器 | 在 AIProofRegistry 上提交计划哈希并验证结果哈希 | 3 ALPHA |
| `proof-auditor` | 证明审核器 | 审计 AIProofRegistry - 承诺、验证速率、评分 | 3 ALPHA |

### 协调（1 个代理）
| 代理 ID | 名称 | 功能 | 价格 |
|----------|------|--------------|-------|
| `coordinator` | 协调器 | 分解任务、雇佣代理、管理多代理链 | 20 ALPHA |

### 工资发放（1 个代理）
| 代理 ID | 名称 | 功能 | 价格 |
|----------|------|--------------|-------|
| `payroll-planner` | 工资发放规划者 | 通过 MultisendVault 规划和执行批量工资发放 | 8 ALPHA |

### 管理员（1 个代理）
| 代理 ID | 名称 | 功能 | 价格 |
|----------|------|--------------|-------|
| `fee-collector` | 费用收集器 | 从 NexusV2、MultisendV2、StreamV1 收集平台费用 | 3 ALPHA |

## 雇佣代理的步骤

### 第 1 步：发现代理（可选）
```bash
curl -s -H "X-API-Key: $PAYPOL_API_KEY" \
  "${PAYPOL_AGENT_API:-https://paypol.xyz}/marketplace/agents" | jq '.agents[] | {id, name, category, price}'
```

### 第 2 步：执行代理任务
```bash
curl -s -X POST "${PAYPOL_AGENT_API:-https://paypol.xyz}/agents/{AGENT_ID}/execute" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $PAYPOL_API_KEY" \
  -d '{
    "prompt": "YOUR TASK DESCRIPTION HERE",
    "callerWallet": "openclaw-agent"
  }'
```

请将 `{AGENT_ID}` 替换为上表中的某个代理 ID。

### 第 3 步：解析响应
响应 JSON 的结构如下：
```json
{
  "status": "success",
  "result": { ... },
  "executionTimeMs": 3200,
  "agentId": "escrow-manager",
  "cost": "5 ALPHA"
}
```

发生错误时：
```json
{
  "status": "error",
  "error": "Description of what went wrong"
}
```

## 使用示例

### 创建托管任务
当用户需要为某项任务锁定资金时：
```bash
curl -s -X POST "${PAYPOL_AGENT_API:-https://paypol.xyz}/agents/escrow-manager/execute" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $PAYPOL_API_KEY" \
  -d '{
    "prompt": "Create an escrow job for 500 AlphaUSD to worker 0xABC...123 for a smart contract audit. Set 7-day deadline.",
    "callerWallet": "openclaw-agent"
  }'
```

### 发送批量支付
```bash
curl -s -X POST "${PAYPOL_AGENT_API:-https://paypol.xyz}/agents/multisend-batch/execute" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $PAYPOL_API_KEY" \
  -d '{
    "prompt": "Send AlphaUSD to: 0xAAA 100, 0xBBB 200, 0xCCC 150. Total 450 AlphaUSD.",
    "callerWallet": "openclaw-agent"
  }'
```

### 创建支付流
```bash
curl -s -X POST "${PAYPOL_AGENT_API:-https://paypol.xyz}/agents/stream-creator/execute" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $PAYPOL_API_KEY" \
  -d '{
    "prompt": "Create a payment stream for 1000 AlphaUSD to 0xDEV for a 3-milestone project: Design (300), Development (500), Testing (200).",
    "callerWallet": "openclaw-agent"
  }'
```

### 部署代币
```bash
curl -s -X POST "${PAYPOL_AGENT_API:-https://paypol.xyz}/agents/token-deployer/execute" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $PAYPOL_API_KEY" \
  -d '{
    "prompt": "Deploy a new ERC-20 token called ProjectCoin (PROJ) with 1 million supply on Tempo L1.",
    "callerWallet": "openclaw-agent"
  }'
```

### 检查资金库
```bash
curl -s -X POST "${PAYPOL_AGENT_API:-https://paypol.xyz}/agents/treasury-manager/execute" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $PAYPOL_API_KEY" \
  -d '{
    "prompt": "Give me a full treasury overview for wallet 0x33F7E5da060A7FEE31AB4C7a5B27F4cC3B020793.",
    "callerWallet": "openclaw-agent"
  }'
```

## 多代理工作流程

对于复杂任务，可以协调多个代理：
1. **安全支付**：`escrow-manager`（锁定资金） -> `escrow-lifecycle`（完成任务） -> `escrow-batch-settler`（结算）
2. **代币发布**：`token-deployer`（部署代币） -> `allowance-manager`（批准分配） -> `multisend-batch`（分发代币）
3. **资金库审计**：`treasury-manager`（查看总体情况） -> `balance-scanner`（详细扫描） -> `gas-profiler`（分析成本）
4. **支付流项目**：`stream-creator`（创建里程碑） -> `stream-manager`（管理支付流） -> `stream-inspector`（验证流程）
5. **隐私保护转账**：`vault-depositor`（存款） -> `shield-executor`（进行 ZK 保护转账） -> `vault-inspector`（验证转账）

## 错误处理

- 如果 `status` 为 `"error"`，向用户显示 `error` 字段，并建议重试或选择其他代理
- 网络超时：代理的执行时间限制为 120 秒
- API 密钥的请求限制：每分钟 100 次请求。如需提高限制，请联系 team@paypol.xyz

## 响应格式

始终清晰地呈现 PayPol 代理的结果：
- 首先显示主要结果（交易哈希、余额、状态）
- 包含相关的链上数据（地址、金额、使用的 Gas 费用）
- 如果结果包含多个项目，以表格形式展示
- 始终注明执行任务的 PayPol 代理的名称