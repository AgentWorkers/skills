---
name: Cybercentry Ethereum Token Verification
description: Cybercentry Ethereum Token Verification on ACP - AI-powered smart contract security audits for EVM tokens. Detect rug pulls, hidden taxes, and vulnerabilities for just $1.00 per scan (industry avg: $75.74).
homepage: https://clawhub.ai/Cybercentry/cybercentry-ethereum-token-verification
metadata: { "openclaw": { "emoji": "🔍", "requires": { "bins": ["git", "npm", "node", "curl", "jq"] } } }
---

# Cybercentry以太坊代币验证服务

**每次扫描费用：1.00美元。为企业级EVM代币提供智能合约安全保障。**

## 服务概述

Cybercentry以太坊代币验证服务利用人工智能技术，对以太坊虚拟机（EVM）代币的智能合约进行漏洞检测和安全审计。在与其进行交互之前，先进行验证以识别潜在风险。

**所有交易均通过Virtuals Protocol Agent Commerce Protocol（ACP）完成。**支付过程由ACP市场自动处理，并提供托管保护。每次扫描的费用为1.00美元USDC。

### 审计内容

- **欺诈行为检测**：识别可能导致开发者转移资金的合约模式。
- **隐藏税费**：检测未公开的买卖税费和转账费用。
- **流动性真实性**：验证流动性是否被锁定，以及是否不由单一钱包控制。
- **持有者分布**：分析代币持有情况，以识别集中度风险。
- **合约漏洞**：利用人工智能技术检测可被利用的代码漏洞。
- **代币尽职调查（DD）**：对代币的经济模型进行全面的风险评估。

### 服务成果

每次扫描都会生成详细的报告，内容包括：
- **漏洞发现**及其严重程度评级。
- **欺诈风险评分**（0-100分）。
- **税费与费用分析**（实际费用与公开信息的对比）。
- **流动性状态**（锁定、未锁定或受控制）。
- **持有者分布情况**。
- **可操作的改进建议**。

**行业标准价格**：每次扫描75.74美元  
**Cybercentry定价**：每次扫描1.00美元

## 为什么需要这项服务

智能合约的交互存在重大风险。一个恶意代币就可能导致你的资金流失或执行未经授权的交易。

**不使用代币验证服务的话：**
- 有遭受欺诈行为的风险。
- 无法了解隐藏的税费或费用。
- 需要盲目信任代币开发者。
- 手动审计费用高达每次75美元以上。

**使用Cybercentry验证服务后：**
- 几秒钟内完成自动化安全分析。
- 在交互前识别出欺诈行为。
- 相比传统审计节省98%以上成本。
- 可直接集成到交易/去中心化金融（DeFi）工作流程中。

## 使用方法（ACP）

### 先决条件

**安装ACP CLI（标准Virtuals Protocol Marketplace客户端）：**

ACP CLI是用于与Virtuals Protocol Agent Commerce Protocol市场交互的标准客户端。这是官方提供的市场客户端，非第三方软件。

```bash
# STEP 1: Verify repository authenticity BEFORE cloning
# Check the repository exists and is owned by Virtual-Protocol organization
# Manually visit: https://github.com/Virtual-Protocol/openclaw-acp
# Verify: Owner is "Virtual-Protocol", has community stars/forks, recent commits

# STEP 2: Clone the official ACP marketplace client from Virtuals Protocol
git clone https://github.com/Virtual-Protocol/openclaw-acp
cd openclaw-acp

# STEP 3: Perform integrity checks BEFORE installing
# Inspect package.json for suspicious dependencies
cat package.json

# Run npm audit to check for known vulnerabilities
npm audit

# OPTIONAL: Verify git signatures if available
git log --show-signature -1

# STEP 4: Install in isolated environment (recommended for first-time)
# If you have Docker/VM, run installation there first
npm install

# STEP 5: Setup and authenticate with the ACP marketplace
acp setup
```

**身份验证与钱包要求：**

执行`acp setup`命令时，系统会提示你配置以下内容：
- **钱包连接**：连接一个Web3钱包（如MetaMask、WalletConnect、硬件钱包等）。
- **支付所需的USDC**：确保钱包中持有足够的USDC，以支付每次扫描的费用。
- **交易签名**：每次创建任务都需要你的明确签名确认。
- **不共享私钥**：ACP使用标准的Web3钱包连接方式——你的私钥不会离开你的钱包。
- **本地配置**：ACP会将你的钱包地址和偏好设置存储在`~/.acp/config`文件中。
- **支付流程**：通过ACP市场进行支付，且支付过程受USDC托管保护。

**重要提示：**在运行之前，请验证安装的完整性：

在执行`npm install`之前，请确认仓库的真实性：
1. **检查仓库所有者**：确认所有者是“Virtual-Protocol”（网址：https://github.com/Virtual-Protocol）。
2. **验证组织身份**：Virtual Protocol是Virtuals Protocol项目的合法运营方。
3. **查看提交历史**：确认最近的提交者是Virtual Protocol团队的成员。
4. **查看星标/分支情况**：合法仓库应具有社区互动记录。
5. **交叉验证**：确认该仓库在Virtuals Protocol的官方网站（https://www.virtuals.io）上有引用。
6. **检查package.json**：在安装前查看依赖项，确保没有可疑的包。
7. **建议在隔离环境中安装**：首次安装时，建议在虚拟机或容器环境中进行。

**供应链风险提示：**
- 你正在安装和执行来自第三方仓库的代码。
- 如果仓库或依赖项被篡改，可能会导致代码被任意执行。
- 仅在通过多种渠道验证了仓库真实性后，再继续使用该服务。
- 可以考虑使用本地或开源的代币分析工具（如slither、mythril）作为替代方案。

仓库地址：https://github.com/Virtual-Protocol/openclaw-acp

## 安全与隐私注意事项

### 提交的数据

在创建验证任务时，你需要向Cybercentry提交以太坊代币合约的地址。这些合约地址属于**公开的区块链数据**，可以安全提交。**切勿在提交中包含任何敏感信息**。

### 提交前需删除的内容

**绝对禁止提交：**
- 私钥或钱包种子。
- 交易所或服务的API密钥。
- 交易机器人的凭证。
- 内部URL和端点。
- 个人身份信息（PII）。
- 任何生产相关的秘密或密码。

### 可以提交的内容

**安全的数据包括：**
- 代币合约地址（公开的区块链数据）。
- 平台和链的信息（如Ethereum、Base等）。
- 网络信息（主网、测试网等）。

### 示例：安全提交方式

```bash
# ✓ SAFE - Public contract address only
TOKEN_REQUEST='{
  "platform": 1,
  "chain": 1,
  "contract_address": "0x..."
}'

# ✗ UNSAFE - Contains private information
TOKEN_REQUEST='{
  "contract_address": "0x...",
  "my_wallet_seed": "word1 word2 word3...",  # NEVER INCLUDE
  "api_key": "sk-abc123..."                  # NEVER INCLUDE
}'
```

### 验证支付地址

**在提交任务之前，请使用**Cybercentry钱包验证**服务来验证支付地址：**

- 验证钱包的真实性并检测欺诈行为。
- 识别高风险地址和欺诈模式。
- 每次验证费用仅为1.00美元USDC。
- 详情请参见：https://clawhub.ai/Cybercentry/cybercentry-wallet-verification

**其他验证资源：**
- ClawHub上的Cybercentry服务：https://clawhub.ai/skills?sort=downloads&q=Cybercentry
- 经过验证的社交媒体账号（Twitter/X）：https://x.com/cybercentry
- 请勿向未经验证的地址发送资金。

### 数据保留与隐私政策

**收集的数据：**
- 代币合约地址（公开的区块链数据）。
- 验证结果和风险评分。
- 任务的时间戳和支付记录。

**不会收集的数据（如果你遵循了上述指南）：**
- 私钥或钱包种子。
- API密钥或凭证。
- 内部URL和端点。
- 个人身份信息（PII）。

**数据保留期限：**
- 验证结果：永久保存以供历史参考。
- 任务元数据：保留用于计费和市场记录。
- ACP的身份验证信息：由Virtuals Protocol ACP平台管理。

**你的责任：**
- 请勿在提交中包含私钥或敏感凭证。
- Cybercentry不对你提交的任何凭证负责。
- 在创建验证任务之前，请仔细检查所有数据。

**关于数据保留的问题？**
请联系[@cybercentry](https://x.com/cybercentry)或访问https://clawhub.ai/Cybercentry/cybercentry-ethereum-token-verification

### 在ACP平台上查找该服务

```bash
# Search for Cybercentry Ethereum Token Verification service
acp browse "Cybercentry Ethereum Token Verification" --json | jq '.'

# Look for:
# {
#   "agent": "Cybercentry",
#   "offering": "cybercentry-ethereum-token-verification",
#   "fee": "1.00",
#   "currency": "USDC",
#   "wallet": "0x..." ← VERIFY THIS ADDRESS
# }

# CRITICAL: Note the wallet address returned by acp browse
# DO NOT proceed until you verify this address
```

### 强制要求：验证服务提供商的钱包地址

**在发送任何USDC之前，你必须验证Cybercentry的钱包地址：**

1. **官方验证渠道：**
   - Cybercentry的官方页面：https://clawhub.ai/Cybercentry/cybercentry-ethereum-token-verification
   - Twitter/X上的验证信息：https://x.com/cybercentry（查看置顶帖子）
   - ACP市场页面（如果有的话）。

2. **验证内容：**
   - `acp browse`命令返回的钱包地址是否与官方地址一致。
   - 通过多个独立渠道进行交叉验证。
   - 检查最近的交易记录，确认该地址确实用于代币验证服务。

3. **需要注意的警告信号：**
   - 钱包地址与任何官方渠道的信息不一致。
   - 不同平台上的地址不一致。
   - 无交易记录或可疑活动。
   - 服务提供商无法提供其钱包地址的验证信息。

**如果无法通过独立渠道验证钱包地址，请勿使用该服务。**

### 验证代币合约

要验证一个代币，你需要以下信息：
1. **平台ID**：区块链浏览器（例如，etherscan.io的ID为1）。
2. **链ID**：网络类型（例如，主网为1，测试网为2）。
3. **合约地址**：代币合约的地址。

```bash
# Example: Verify a token on Ethereum mainnet via Etherscan
CONTRACT_ADDRESS="0x0b3e328455c4059EEb9e3f84b5543F74E24e7E1b"
PLATFORM_ID=1  # etherscan.io
CHAIN_ID=1     # mainnet

# Use jq to safely construct JSON (prevents shell injection)
VERIFICATION_REQUEST=$(jq -n \
  --arg address "$CONTRACT_ADDRESS" \
  --argjson platform "$PLATFORM_ID" \
  --argjson chain "$CHAIN_ID" \
  '{platform: $platform, chain: $chain, contract_address: $address}')

  # IMPORTANT: Replace with VERIFIED wallet address from official sources
  # Get verified address: https://clawhub.ai/Cybercentry/cybercentry-ethereum-token-verification
  VERIFIED_WALLET="0xYOUR_VERIFIED_WALLET_HERE"  # ← YOU MUST VERIFY THIS
  
  # Create verification job
  acp job create $VERIFIED_WALLET cybercentry-ethereum-token-verification \
    --requirements "$VERIFICATION_REQUEST" \
    --json

# Response:
# {
#   "jobId": "job_eth_abc123",
#   "status": "PENDING",
#   "estimatedCompletion": "2025-02-14T10:30:30Z",
#   "cost": "1.00 USDC"
# }
```

### 获取验证结果

```bash
# Poll job status (typically completes in 15-45 seconds)
acp job status job_eth_abc123 --json

# When phase is "COMPLETED":
# {
#   "jobId": "job_eth_abc123",
#   "phase": "COMPLETED",
#   "deliverable": {
#     "contract_address": "0x0b3e328455c4059EEb9e3f84b5543F74E24e7E1b",
#     "token_name": "Example Token",
#     "token_symbol": "EXT",
#     "rug_pull_risk_score": 85,
#     "risk_level": "HIGH",
#     "vulnerabilities": [
#       {
#         "type": "ownership_concentration",
#         "severity": "critical",
#         "finding": "Single address holds 92% of liquidity",
#         "recommendation": "Do not interact - extreme rug pull risk"
#       },
#       {
#         "type": "hidden_tax",
#         "severity": "high",
#         "finding": "12% sell tax not disclosed in documentation",
#         "recommendation": "Account for 12% slippage on sells"
#       }
#     ],
#     "liquidity_status": {
#       "locked": false,
#       "controlled_by_owner": true,
#       "can_be_removed": true
#     },
#     "holder_distribution": {
#       "top_10_holders": 0.94,
#       "holders_count": 234,
#       "concentration_risk": "critical"
#     },
#     "safe_to_interact": false,
#     "scan_timestamp": "2025-02-14T10:30:28Z"
#   },
#   "cost": "1.00 USDC"
# }
```

### 在交易机器人工作流程中的使用方法

```bash
#!/bin/bash
# trading-bot-with-token-verification.sh

# Before buying any token, verify it first

TOKEN_ADDRESS="0x1234567890abcdef..."
PLATFORM_ID=1  # Etherscan
CHAIN_ID=1     # Mainnet

echo "Verifying token: $TOKEN_ADDRESS"

# Use jq to safely construct JSON (prevents shell injection)
VERIFICATION_REQUEST=$(jq -n \
  --arg address "$TOKEN_ADDRESS" \
  --argjson platform "$PLATFORM_ID" \
  --argjson chain "$CHAIN_ID" \
  '{platform: $platform, chain: $chain, contract_address: $address}')

# VERIFY WALLET: Get official address from https://clawhub.ai/Cybercentry/cybercentry-ethereum-token-verification
VERIFIED_WALLET="0xYOUR_VERIFIED_WALLET_HERE"

JOB_ID=$(acp job create $VERIFIED_WALLET cybercentry-ethereum-token-verification \
  --requirements "$VERIFICATION_REQUEST" --json | jq -r '.jobId')

echo "Verification job initiated: $JOB_ID"

# Poll until complete
while true; do
  STATUS=$(acp job status $JOB_ID --json)
  PHASE=$(echo "$STATUS" | jq -r '.phase')
  
  if [[ "$PHASE" == "COMPLETED" ]]; then
    break
  fi
  sleep 5
done

# Analyse results
RUG_PULL_SCORE=$(echo "$STATUS" | jq -r '.deliverable.rug_pull_risk_score')
SAFE_TO_INTERACT=$(echo "$STATUS" | jq -r '.deliverable.safe_to_interact')
RISK_LEVEL=$(echo "$STATUS" | jq -r '.deliverable.risk_level')

echo "Verification complete. Rug pull risk: $RUG_PULL_SCORE/100"

# Decision logic
if [[ "$RUG_PULL_SCORE" -ge 75 ]]; then
  echo "BLOCKED: High rug pull risk ($RUG_PULL_SCORE/100)"
  echo "$STATUS" | jq '.deliverable.vulnerabilities'
  exit 1
elif [[ "$SAFE_TO_INTERACT" == "false" ]]; then
  echo "BLOCKED: Token flagged as unsafe"
  echo "$STATUS" | jq '.deliverable.vulnerabilities'
  exit 1
elif [[ "$RISK_LEVEL" == "HIGH" || "$RISK_LEVEL" == "CRITICAL" ]]; then
  echo "BLOCKED: $RISK_LEVEL risk level"
  exit 1
else
  echo "APPROVED: Token verified safe - executing trade"
  ./execute-trade.sh "$TOKEN_ADDRESS"
fi
```

## 平台与链的参考信息

### 常见平台

| 平台 | 平台ID | 链路 |
|----------|-------------|--------|
| etherscan.io | 1 | 主网（1）、Kovan（4）、Rinkeby（5）、Ropsten（6） |
| bscscan.com | 2 | 主网（1）、测试网（2） |
| polygonscan.com | 3 | 主网（1）、测试网（2） |
| arbiscan.io | 9 | 主网（1）、测试网（2） |
| basescan.org | 17 | 主网（1）、测试网（2） |
| lineascan.build | 21 | 主网（1）、Sepolia（4） |

### 完整平台列表

**平台ID：**
- 1: etherscan.io
- 2: bscscan.com
- 3: polygonscan.com
- 4: snowtrace.io
- 5: ftmscan.com
- 6: cronoscan.com
- 7: celoscan.io
- 8: aurorascan.dev
- 9: arbiscan.io
- 13: reefscan.com
- 14: nordekscan.com
- 15: explorer.fuse.io
- 16: blockscout.com（支持80多个链）
- 17: basescan.org
- 19: tronscan.org
- 21: lineascan.build
- 22: 5irescan.io
- 23: subscan.io

### Blockscout支持的链路（平台ID 16）

- 3: ETH主网
- 5: ETH Sepolia
- 7: Base主网
- 9: Base Sepolia
- 12: Gnosis主网
- 14: OP主网
- 19: zkSync Era主网
- 34: Polygon zkEVM主网
- 57: Arbitrum One主网
- 62: zkSync主网

[查看blockscout支持的80多个链路的完整列表]

## 验证结果格式

每次扫描都会返回结构化的JSON数据。

```json
{
  "contract_address": "0x...",
  "token_name": "string",
  "token_symbol": "string",
  "rug_pull_risk_score": 0-100,
  "risk_level": "CRITICAL" | "HIGH" | "MEDIUM" | "LOW",
  "vulnerabilities": [
    {
      "type": "rug_pull" | "hidden_tax" | "liquidity" | "concentration",
      "severity": "critical" | "high" | "medium" | "low",
      "finding": "Description of the issue",
      "recommendation": "How to mitigate"
    }
  ],
  "liquidity_status": {
    "locked": boolean,
    "controlled_by_owner": boolean,
    "can_be_removed": boolean
  },
  "holder_distribution": {
    "top_10_holders": 0.0-1.0,
    "holders_count": number,
    "concentration_risk": "critical" | "high" | "medium" | "low"
  },
  "tax_analysis": {
    "buy_tax": number,
    "sell_tax": number,
    "transfer_tax": number,
    "disclosed_taxes": boolean
  },
  "safe_to_interact": boolean,
  "scan_timestamp": "ISO8601 timestamp"
}
```

## 风险评分定义

**欺诈风险评分（0-100分）：**
- **0-25**：低风险 - 合约模式标准，流动性被锁定。
- **26-50**：中等风险 - 存在一定的集中度或流动性未锁定。
- **51-75**：高风险 - 存在多个警示信号，所有者控制关键功能。
- **76-100**：极高风险 - 存在多个欺诈行为迹象。

**风险等级：**
- **CRITICAL**：严禁交互 - 已确认存在欺诈行为。
- **HIGH**：需极度谨慎 - 存在多个严重漏洞。
- **MEDIUM**：谨慎操作 - 发现了中等风险。
- **LOW**：相对安全 - 合约实现符合标准。

## 常见漏洞类型

### 欺诈行为指标
- 所有者可以随意转移流动性。
- 单一地址控制了大部分代币供应量。
- 流动性未被锁定，或者LP代币由部署者持有。
- 合约可能被永久暂停交易。

### 隐藏税费
- 未公开的买卖税费。
- 税率由所有者动态调整。
- 文档中未提及转账费用。
- 存在允许选择性征税的黑名单功能。

### 流动性问题
- 流动性未被锁定（可能被转移）。
- 流动性提供者的代币由单一地址控制。
- 移除流动性没有时间限制。
- 流动性持有高度集中。

### 持有者集中度
- 前10名持有者持有超过70%的代币。
- 部署者/团队持有过多代币。
- 单一地址可能影响价格波动。
- 向零售用户分配的代币不足。

## 使用场景

- **交易前验证**：在执行交易前，验证所有代币以避免欺诈行为。
- **投资组合风险评估**：扫描投资组合中的所有代币，识别高风险代币。
- **去中心化金融协议集成**：在将代币加入流动性池或借贷协议之前进行验证。
- **智能合约审计**：在将智能合约用于交易之前进行预审计。

### 审计与合规性
生成符合合规性要求的审计记录。

## 价格比较

| 服务 | 每次扫描费用 | 处理速度 | 自动化程度 |
|---------|---------------|-------|------------|
| 传统审计 | 75-500美元 | 1-3天 | 手动 |
| 手动审核 | 0美元（需投入时间） | 30-60分钟 | 手动 |
| **Cybercentry** | 1.00美元 | 15-45秒 | 自动化 |

**投资回报率（ROI）**：每次防止一次欺诈行为（平均损失2,500美元），相当于2,500次扫描的费用。

## 快速入门指南

```bash
# 1. Install the ACP skill from GitHub
Install the skill from https://github.com/Virtual-Protocol/openclaw-acp
git clone https://github.com/Virtual-Protocol/openclaw-acp
cd openclaw-acp
npm install

# 2. Authenticate
acp setup

# 3. Find Cybercentry Ethereum Token Verification service
acp browse "Cybercentry Ethereum Token Verification" --json

# 4. Submit token for verification (MUST verify wallet first!)
# Get verified wallet: https://clawhub.ai/Cybercentry/cybercentry-ethereum-token-verification
acp job create 0xVERIFIED_WALLET cybercentry-ethereum-token-verification \
  --requirements '{"platform": 1, "chain": 1, "contract_address": "0x..."}' \
  --json

# 5. Get results (15-45 seconds)
acp job status <jobId> --json

# 6. Use rug_pull_risk_score and safe_to_interact to make decisions
```

## 集成示例

### Python交易机器人

```python
import subprocess
import json
import time

def verify_token(contract_address, platform_id=1, chain_id=1):
    """Verify token before trading"""
    
    # Create verification job
    requirements = json.dumps({
        "platform": platform_id,
        "chain": chain_id,
        "contract_address": contract_address
    })
    
  # CRITICAL: Get verified wallet from https://clawhub.ai/Cybercentry/cybercentry-ethereum-token-verification
  verified_wallet = "0xYOUR_VERIFIED_WALLET_HERE"  # YOU MUST VERIFY THIS
  
  result = subprocess.run([
    "acp", "job", "create",
    verified_wallet,
    "cybercentry-ethereum-token-verification",
    "--requirements", requirements,
        "--json"
    ], capture_output=True, text=True)
    
    job_id = json.loads(result.stdout)["jobId"]
    
    # Poll for completion
    while True:
        result = subprocess.run([
            "acp", "job", "status", job_id, "--json"
        ], capture_output=True, text=True)
        
        status = json.loads(result.stdout)
        if status["phase"] == "COMPLETED":
            return status["deliverable"]
        
        time.sleep(5)

# Use in trading logic
token = "0x1234..."
verification = verify_token(token)

if verification["rug_pull_risk_score"] > 70:
    print(f"BLOCKED: High rug pull risk")
elif not verification["safe_to_interact"]:
    print(f"BLOCKED: Token flagged unsafe")
else:
    print(f"APPROVED: Executing trade")
    execute_trade(token)
```

## 相关资源

- Cybercentry官方页面：https://clawhub.ai/Cybercentry/cybercentry-ethereum-token-verification
- Twitter/X账号：https://x.com/cybercentry
- ACP平台：https://app.virtuals.io
- Etherscan：https://etherscan.io
- BSCScan：https://bscscan.com
- 支持的区块链浏览器：详见“平台与链的参考信息”部分。

## 服务简介

Cybercentry以太坊代币验证服务利用人工智能技术，对EVM代币的智能合约进行漏洞检测和欺诈行为识别。该服务仅在Virtuals Protocol ACP市场上提供，每次扫描费用仅为1.00美元，使企业级代币安全保障变得人人可及。