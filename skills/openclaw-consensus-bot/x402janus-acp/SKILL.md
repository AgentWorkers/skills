---
name: x402janus-acp
description: ACP购买者技能：通过Virtuals ACP市场雇佣x402janus进行钱包安全扫描。在ACP市场上创建一个针对x402janus代理的任务，等待任务完成，然后获取扫描结果。支付方式使用$VIRTUAL代币。
metadata:
  emoji: 🔗
  homepage: https://x402janus.com
  requires:
    bins: [node, npx]
    env: [ACP_API_KEY]
---
# x402janus-acp — 通过ACP市场雇佣Janus服务

您可以通过Virtuals Agent Commerce Protocol从x402janus购买钱包安全扫描服务。

## 何时使用此服务（而非直接使用x402janus）  

| 场景 | 使用方式 |
|----------|-----|
| 您的代理持有USDC | 使用`x402janus`（直接通过x402支付，速度更快） |
| 您的代理持有$VIRTUAL代币 | 使用`x402janus-acp`（ACP市场） |
| 您需要代理之间的交易 | 使用`x402janus-acp` |

## 设置  

```bash
SKILL_DIR="$PWD/skills/x402janus-acp"
cd "$SKILL_DIR" && npm install
```

**必需的环境变量：**  

| 变量 | 描述 |
|----------|-------------|
| `ACP_API_KEY` | 用于代理的Virtuals ACP API密钥（买家密钥） |

您可以在以下链接获取ACP密钥：  
https://app.virtuals.io/acp

**可选设置：**  

| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| `ACP_BASE_URL` | `https://claw-api.virtuals.io` | ACP API基础URL |
| `ACP_AGENT_WALLET` | — | 您代理的钱包地址 |

## 命令  

### 列出可用服务  

查看x402janus在ACP市场上提供的扫描服务类型。  

```bash
ACP_API_KEY=$KEY npx tsx scripts/list-offerings.ts --json
```

### 通过ACP扫描钱包  

在ACP市场上创建一个扫描任务，等待x402janus完成扫描，并获取结果。  

```bash
# Basic scan
ACP_API_KEY=$KEY npx tsx scripts/scan-wallet-acp.ts 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045

# With JSON output
ACP_API_KEY=$KEY npx tsx scripts/scan-wallet-acp.ts 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 --json

# Specific offering tier
ACP_API_KEY=$KEY npx tsx scripts/scan-wallet-acp.ts 0x... --offering janus_scan_deep

# Custom timeout
ACP_API_KEY=$KEY npx tsx scripts/scan-wallet-acp.ts 0x... --timeout 180

# Check status of existing job
ACP_API_KEY=$KEY npx tsx scripts/scan-wallet-acp.ts --job-id 42
```

## 可用服务及价格  

以下价格以$VIRTUAL为单位：  

| 服务类型 | 价格 | 服务等级 | 服务描述 |
|----------|-------|-----|-------------|
| `janus_scan_quick` | 0.01 VIRTUAL | 5分钟 | 交易前的安全检查 |
| `janus_scan_standard` | 0.05 VIRTUAL | 5分钟 | 标准扫描，包含审批分析 |
| `janus_scan_deep` | 0.25 VIRTUAL | 5分钟 | 深度法医级扫描 |
| `janus_approvals` | 0.01 VIRTUAL | 5分钟 | 显示存在风险的活跃审批记录 |
| `janus_revoke` | 0.05 VIRTUAL | 5分钟 | 创建撤销交易请求 |
| `janus_revoke_batch` | 0.10 VIRTUAL | 5分钟 | 批量撤销所有危险交易请求 |

## 工作流程：  

1. 您的代理使用钱包地址调用扫描脚本。  
2. 脚本在ACP市场上创建一个针对x402janus的扫描任务。  
3. x402janus接收任务并执行扫描，随后返回结果。  
4. 脚本持续检查扫描进度并最终返回结果。  
5. 支付通过ACP协议以$VIRTUAL代币完成。