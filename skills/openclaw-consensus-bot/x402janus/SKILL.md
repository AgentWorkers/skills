---
name: x402janus
description: >
  **x402janus**——专为以太坊虚拟机（EVMs）设计的自主链上钱包安全解决方案：  
  - 扫描交易审批过程；  
  - 追踪资金流动；  
  - 识别恶意行为（如资金盗取）；  
  - 支持撤销交易功能；  
  - 支付方式：使用基于 Base 的 x402 USDC；  
  - 无需 API 密钥，也无需创建账户。
metadata:
  emoji: 🛡️
  homepage: https://x402janus.com
  repository: https://github.com/consensus-hq/agent-pulse
  acp_marketplace: https://app.virtuals.io/acp/agent-details/14804
  requires:
    bins: [node, npx]
    env: [JANUS_API_URL]
  optionalEnv:
    - PRIVATE_KEY
    - THIRDWEB_CLIENT_ID
  tags:
    - security
    - wallet
    - evm
    - base
    - ethereum
    - x402
    - micropayment
    - forensics
    - approvals
    - drainer-detection
    - ai-agent
    - defi
---
# x402janus — 为AI代理提供的钱包安全服务

“没有任何交易能够未经检查就通过。”  
这是AI代理在每次进行金融交易前会调用的安全层服务。该服务会扫描钱包、追踪交易审批流程、检测潜在的安全风险，并生成可撤销的交易记录——所有这些操作都通过x402微支付系统完成。无需API密钥或账户信息，也无需任何额外的设置。

## 为何需要这项服务  

随着AI代理逐渐具备自主管理钱包和进行交易的能力，它们往往无法完全了解自己批准了哪些交易，也不知道哪些行为可能会对自身造成威胁。x402janus就是这样一个“安全关卡”——任何AI代理在做出财务决策前都可以使用它进行详细的审计分析。  

在ClawHub平台上，该服务的安全评分高达3.240，是专为自主代理设计的最高评级安全工具。  

## 快速入门  

```bash
# Install
clawhub install x402janus
cd skills/x402janus && npm install

# Free scan (no wallet required)
JANUS_API_URL=https://x402janus.com \
  npx tsx scripts/scan-wallet.ts 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 --tier free --json

# Paid scan ($0.01 USDC via x402)
JANUS_API_URL=https://x402janus.com PRIVATE_KEY=$PRIVATE_KEY \
  npx tsx scripts/scan-wallet.ts 0xYOUR_TARGET --tier quick --json
```  

**自动化操作的返回代码：**  
- `0` — 安全（健康状况≥75）→ 可继续交易  
- `1` — 中等风险（50–74）→ 需要审核  
- `2` — 高风险（<50）→ 中止交易  
- `3` — 危险（<25）→ 封锁交易并触发警报  

## 设置流程  

```bash
cd skills/x402janus && npm install
```  

| 变量          | 是否必需 | 说明                          |  
|----------------|---------|------------------------------------|  
| `JANUS_API_URL`    | 是       | API地址（https://x402janus.com）                   |  
| `PRIVATE_KEY`     | 仅限付费层级 | 用于x402支付的代理钱包密钥                   |  
| `THIRDWEB_CLIENT_ID` | 否       | Thirdweb客户端ID（默认值：`x402janus-skill`）         |  

## 命令说明  

### 1. 扫描钱包  
该命令用于检测钱包的安全风险、列出所有已批准的交易，并生成可撤销的交易记录。  

```bash
# Free tier — no payment required
JANUS_API_URL=https://x402janus.com \
  npx tsx scripts/scan-wallet.ts <address> --tier free --json

# Quick scan — $0.01 USDC
JANUS_API_URL=https://x402janus.com PRIVATE_KEY=$PRIVATE_KEY \
  npx tsx scripts/scan-wallet.ts <address> --tier quick --json

# Standard scan — $0.05 USDC (AI threat analysis)
JANUS_API_URL=https://x402janus.com PRIVATE_KEY=$PRIVATE_KEY \
  npx tsx scripts/scan-wallet.ts <address> --tier standard --json

# Deep scan — $0.25 USDC (full graph + drainer fingerprinting)
JANUS_API_URL=https://x402janus.com PRIVATE_KEY=$PRIVATE_KEY \
  npx tsx scripts/scan-wallet.ts <address> --tier deep --chain base --json
```  

**输出结果：**  
```json
{
  "address": "0x...",
  "scannedAt": "2026-03-04T...",
  "payer": "0x...",
  "coverageLevel": "basic",
  "summary": {
    "totalTokensApproved": 3,
    "unlimitedApprovals": 2,
    "highRiskApprovals": 0,
    "healthScore": 80
  },
  "approvals": [...],
  "recommendations": [...],
  "revokeTransactions": [...]
}
```  

### 2. 列出已批准的交易  
该命令用于查看代理已批准的所有金融交易。  

```bash
# All approvals with risk flags
JANUS_API_URL=https://x402janus.com PRIVATE_KEY=$PRIVATE_KEY \
  npx tsx scripts/list-approvals.ts <address> --format json

# High-risk only
npx tsx scripts/list-approvals.ts <address> --risk high,critical --format json

# Unlimited approvals only
npx tsx scripts/list-approvals.ts <address> --unlimited-only --format json
```  

### 3. 撤销已批准的交易  
该命令可用于撤销代理之前批准的任何交易。  

**注意：** 使用`--execute`命令执行实际交易前，请务必先获得用户确认。  

### 4. 启动监控  
该命令可设置自动监控功能，持续检测钱包的安全状况。  

```bash
# Webhook alerts
JANUS_API_URL=https://x402janus.com PRIVATE_KEY=$PRIVATE_KEY \
  npx tsx scripts/start-monitoring.ts <address> --webhook https://your-webhook.com --json

# Telegram alerts
npx tsx scripts/start-monitoring.ts <address> --telegram @username --json
```  

## 代理集成方式  
```bash
#!/bin/bash
# Pre-transaction security gate
RESULT=$(JANUS_API_URL=https://x402janus.com PRIVATE_KEY=$PRIVATE_KEY \
  npx tsx scripts/scan-wallet.ts "$TARGET_WALLET" --tier quick --json 2>/dev/null)
EXIT=$?

if [ $EXIT -eq 0 ]; then
  echo "✅ Wallet safe — proceeding with transaction"
  # ... execute your trade/transfer/approval
elif [ $EXIT -eq 1 ]; then
  echo "⚠️ Medium risk — requesting human review"
  # ... alert human operator
else
  echo "🚫 High risk detected — blocking transaction"
  # ... halt and report
fi
```  

## 价格体系  

| 价格层级 | 费用（USDC） | 处理速度 | 支持的功能             |  
|---------|---------|------------------|------------------|  
| **免费** | $0.00    | <5秒      | 地址验证、基本校验            |  
| **快速** | $0.01    | <3秒      | 确定性风险评分、交易列表          |  
| **标准** | $0.05    | <10秒      | AI威胁分析、更深入的历史数据查询    |  
| **高级** | $0.25    | <30秒      | 全面图谱分析、异常行为检测        |  

所有费用均通过x402微支付系统（基于EIP-3009的TransferWithAuthorization协议）结算。代理只需支付相应的费用，Thirdweb平台会负责在区块链上完成支付。  

## x402微支付的工作原理  
1. AI代理调用扫描接口；  
2. 服务器返回包含支付细节的HTTP 402响应；  
3. Thirdweb的x402 SDK使用代理的钱包密钥完成支付授权；  
4. SDK会自动尝试再次发起支付请求；  
5. Thirdweb平台验证后会在区块链上完成USDC的结算；  
6. 最后将扫描结果返回给代理。  

**注意：** 所有支付费用均由Thirdweb平台承担，代理的钱包中只需持有USDC即可。  

## ACP市场  
该服务也可在Virtuals的ACP市场平台上购买（适用于代理之间的合作）：  
**https://app.virtuals.io/acp/agent-details/14804**  
提供的服务包括：快速/标准/高级版本的扫描服务、已批准交易列表以及单次/批量撤销交易的功能。  

## API接口（直接使用）  
对于偏好直接使用HTTP接口的代理，可参考以下信息：  

```bash
# Free scan
curl -X POST "https://x402janus.com/api/guardian/scan/0xADDRESS?tier=free"

# Paid scan (x402 handles payment automatically via SDK)
# Or manually: server returns 402 → sign payment → retry with header

# Health check
curl "https://x402janus.com/api/guardian/status"

# Skill documentation (machine-readable)
curl "https://x402janus.com/api/skill-md"
```  

## 账户要求  
付费层级需要提供以下信息：  
- **JANUS_API_URL** 和 `PRIVATE_KEY`：用于访问x402服务；  
- **USDC**：用于支付（免费层级无需支付）。  

**安全性保障：**  
- 免费层级无需提供私钥；  
- 付费层级使用Thirdweb的x402签名机制，私钥不会被记录或泄露；  
- 所有脚本在处理请求前都会验证地址的合法性；  
- 撤销交易功能默认为模拟操作（实际执行前需使用`--execute`命令）；  
- x402支付的金额必须精确无误，平台不会多收费用；  
- 每个IP地址每窗口内仅允许免费扫描10次。  

## 相关链接：  
- **产品官网**：https://x402janus.com  
- **ACP市场**：https://app.virtuals.io/acp/agent-details/14804  
- **GitHub仓库**：https://github.com/consensus-hq/agent-pulse  
- **社交媒体账号**：[@x402janus](https://x.com/x402janus)