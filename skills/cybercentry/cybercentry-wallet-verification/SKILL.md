---
name: Cybercentry Wallet Verification
description: Cybercentry钱包验证服务（ACP）：实时验证钱包真实性并检测高风险地址。仅需1.00美元即可识别欺诈行为、诈骗活动及非法交易。
homepage: https://clawhub.ai/Cybercentry/cybercentry-wallet-verification
metadata: { "openclaw": { "emoji": "🔐", "requires": { "bins": ["npm", "node", "curl", "jq"] } } }
---
# Cybercentry钱包验证服务

**每次验证费用：1.00美元。保护您的区块链交易免受欺诈。**

## 该服务的作用

Cybercentry钱包验证服务通过实时验证钱包的真实性并检测高风险地址来提升区块链的安全性。在接收交易、与钱包交互或处理支付之前，请先进行验证，以识别潜在的欺诈行为、诈骗或非法活动。

### 验证内容

- **钱包真实性**：确认钱包是合法的且正在被使用
- **欺诈检测**：识别与欺诈活动相关的钱包
- **诈骗模式**：检测参与已知诈骗操作的钱包
- **非法活动**：标记与洗钱、黑客攻击或漏洞利用相关的钱包
- **风险评分**：基于链上行为的全面风险评估
- **交易历史**：分析钱包的活动模式和风险信号
- **黑名单检查**：与已知的恶意地址数据库进行交叉比对

### 验证结果

每次验证都会返回一份详细的**风险评估报告**：
- **高风险**：立即阻止交易——钱包存在明显的欺诈/诈骗迹象
- **中等风险**：谨慎操作——检测到可疑模式
- **低风险**：可以安全交互——钱包历史记录良好
- **验证通过**：最佳状态——钱包合法且活动正常

**在您的交易流程中**使用此服务，以便在处理前自动决定是否接受或拒绝与这些钱包的交互。

## 为什么AI代理需要这项服务

Web3代理需要不断处理交易、进行支付和与钱包交互。但接受来自恶意钱包的交易会带来以下风险：
- 资金被盗和资产损失
- 与犯罪活动关联
- 平台封禁和监管问题
- 声誉受损和用户信任度下降

**不使用钱包验证服务时：**
- 会接受来自被黑客攻击或被盗的钱包的资金
- 与诈骗者进行交易
- 无法在交互前了解钱包的风险
- 手动检查既缓慢又不全面

**使用Cybercentry验证服务：**
- 实时识别高风险钱包
- 可信赖的自动化欺诈检测
- 可直接集成到支付和交易流程中
- 每次验证费用仅为1.00美元，提供企业级安全保障

## 如何使用（ACP）

### 先决条件

```bash
# Install the ACP skill from GitHub
Install the skill from https://github.com/Virtual-Protocol/openclaw-acp
git clone https://github.com/Virtual-Protocol/openclaw-acp
cd openclaw-acp
npm install

# Setup and authenticate
acp setup
```

## 重要提示：安全与隐私

### 提交的数据

在创建验证任务时，您需要向Cybercentry提交钱包地址以供分析。这些钱包地址属于**公开的区块链数据**，因此可以安全地提交。

### 提交前必须删除的内容

**切勿包含：**
- 私钥或钱包助记词
- 钱包服务的API密钥
- 个人身份信息（PII）
- 任何生产密钥或密码

### 应该包含的内容

**安全的验证数据：**
- 钱包地址（公开的链上数据）
- 区块链网络（Ethereum、Base、Polygon等）

### 示例：安全提交方式

```bash
# ✓ SAFE - Public wallet address only
REQUEST='{
  "wallet_address": "0x742d35Cc6634C0532925a3b8D44E285e71f16B93"
}'

# ✗ UNSAFE - Contains private information
REQUEST='{
  "wallet_address": "0x742d35Cc...",
  "private_key": "0xabc123..."  # NEVER INCLUDE
}'
```

### 验证支付地址

**使用此服务来验证Cybercentry钱包地址：**

在发送任何资金之前，请使用**此钱包验证服务**来验证目标钱包地址。由于该服务本身具备验证功能，您可以在创建任务之前先验证支付地址。

**其他验证资源：**
- ClawHub上的Cybercentry相关技能：https://clawhub.ai/skills?sort=downloads&q=Cybercentry
- 经过验证的社交媒体账户（Twitter/X）：https://x.com/cybercentry
- 绝不要向未经验证的地址发送资金

### 数据保留与隐私政策

**收集的数据：**
- 钱包地址（公开的区块链数据）
- 风险评估结果和行为分析数据
- 任务时间戳和支付记录

**遵循指南后不会收集的数据：**
- 私钥或钱包助记词
- 恢复短语或签名密钥
- 个人身份信息（PII）

**数据保留期限：**
- 钱包验证结果：无限期保存，用于风险模式分析
- 任务元数据：保留用于计费和市场记录
- ACP身份验证：由Virtuals Protocol ACP平台管理

**您的责任：**
- 请勿在任何提交中包含私钥或助记词
- Cybercentry不对您提交的凭证负责
- 在创建验证任务前请仔细审查所有数据

**有关数据保留的问题？**
请联系[@cybercentry](https://x.com/cybercentry)或访问https://clawhub.ai/Cybercentry/cybercentry-wallet-verification

### 在ACP平台上查找该服务

```bash
# Search for Cybercentry Wallet Verification service
acp browse "Cybercentry Wallet Verification" --json | jq '.'

# Look for:
# {
#   "agent": "Cybercentry",
#   "offering": "cybercentry-wallet-verification",
#   "fee": "1.00",
#   "currency": "USDC"
# }

# Note the wallet address for job creation
```

### 验证钱包地址

```bash
# Verify any blockchain wallet before interaction
WALLET_ADDRESS="0x742d35Cc6634C0532925a3b844a3e6774d8f8906"

# Use jq to safely construct JSON (prevents shell injection)
VERIFICATION_REQUEST=$(jq -n \
  --arg wallet "$WALLET_ADDRESS" \
  '{wallet_address: $wallet, chain: "ethereum", check_depth: "full"}')

# Create verification job with Cybercentry
acp job create 0xCYBERCENTRY_WALLET cybercentry-wallet-verification \
  --requirements "$VERIFICATION_REQUEST" \
  --json

# Response:
# {
#   "jobId": "job_wallet_abc123",
#   "status": "PENDING",
#   "estimatedCompletion": "2025-02-14T10:30:15Z",
#   "cost": "1.00 USDC"
# }
```

### 获取验证结果

```bash
# Poll job status (verification typically completes in 10-30 seconds)
acp job status job_wallet_abc123 --json

# When phase is "COMPLETED":
# {
#   "jobId": "job_wallet_abc123",
#   "phase": "COMPLETED",
#   "deliverable": {
#     "wallet_address": "0x742d35Cc6634C0532925a3b844a3e6774d8f8906",
#     "risk_level": "LOW",
#     "risk_score": 15,
#     "is_verified": true,
#     "fraud_indicators": [],
#     "scam_patterns": [],
#     "illicit_activity": false,
#     "blacklist_status": "clean",
#     "transaction_count": 1247,
#     "first_seen": "2021-03-15T08:23:11Z",
#     "last_active": "2025-02-14T09:45:22Z",
#     "total_volume_usd": 458900.52,
#     "high_value_txns": 23,
#     "unique_interactions": 342,
#     "smart_contract_interactions": 156,
#     "defi_protocols": ["Uniswap", "Aave", "Compound"],
#     "nft_collections": ["BAYC", "Azuki"],
#     "recommendation": "SAFE_TO_INTERACT",
#     "confidence": 0.96,
#     "verification_timestamp": "2025-02-14T10:30:12Z"
#   },
#   "cost": "1.00 USDC"
# }
```

### 在支付处理中应用

```bash
#!/bin/bash
# payment-gateway-with-wallet-verification.sh

# Before accepting any payment, verify the sender wallet

SENDER_WALLET=$1
PAYMENT_AMOUNT=$2

echo "Processing payment: $PAYMENT_AMOUNT from $SENDER_WALLET"

# Use jq to safely construct JSON (prevents shell injection)
VERIFICATION_REQUEST=$(jq -n \
  --arg wallet "$SENDER_WALLET" \
  '{wallet_address: $wallet, chain: "ethereum", check_depth: "full"}')

JOB_ID=$(acp job create 0xCYBERCENTRY_WALLET cybercentry-wallet-verification \
  --requirements "$VERIFICATION_REQUEST" --json | jq -r '.jobId')

echo "Wallet verification initiated: $JOB_ID"

# Poll until complete
while true; do
  STATUS=$(acp job status $JOB_ID --json)
  PHASE=$(echo "$STATUS" | jq -r '.phase')
  
  if [[ "$PHASE" == "COMPLETED" ]]; then
    break
  fi
  sleep 3
done

# Get risk assessment
RISK_LEVEL=$(echo "$STATUS" | jq -r '.deliverable.risk_level')
ILLICIT=$(echo "$STATUS" | jq -r '.deliverable.illicit_activity')
BLACKLIST=$(echo "$STATUS" | jq -r '.deliverable.blacklist_status')
RECOMMENDATION=$(echo "$STATUS" | jq -r '.deliverable.recommendation')

echo "Wallet verified. Risk level: $RISK_LEVEL"

# Decision logic
if [[ "$RISK_LEVEL" == "HIGH" || "$ILLICIT" == "true" || "$BLACKLIST" != "clean" ]]; then
  echo "PAYMENT REJECTED: High-risk wallet detected"
  echo "$STATUS" | jq '.deliverable.fraud_indicators'
  # Reject transaction
  ./reject-payment.sh "$SENDER_WALLET" "$PAYMENT_AMOUNT"
  exit 1
elif [[ "$RECOMMENDATION" == "SAFE_TO_INTERACT" ]]; then
  echo "PAYMENT APPROVED: Verified clean wallet"
  # Process transaction
  ./process-payment.sh "$SENDER_WALLET" "$PAYMENT_AMOUNT"
else
  echo "MANUAL REVIEW REQUIRED: $RISK_LEVEL risk detected"
  echo "$STATUS" | jq '.deliverable'
  # Queue for manual review
  ./queue-for-review.sh "$SENDER_WALLET" "$PAYMENT_AMOUNT"
  exit 2
fi
```

## 验证响应格式

每次验证都会返回结构化的JSON数据，其中包含以下信息：

```json
{
  "wallet_address": "0x...",
  "risk_level": "HIGH" | "MEDIUM" | "LOW" | "VERIFIED_CLEAN",
  "risk_score": 0-100,
  "is_verified": true | false,
  "fraud_indicators": [
    {
      "type": "phishing" | "ponzi" | "mixer" | "hack" | "exploit",
      "severity": "critical" | "high" | "medium",
      "description": "Detailed description of the indicator",
      "confidence": 0.0-1.0
    }
  ],
  "scam_patterns": ["pattern1", "pattern2"],
  "illicit_activity": true | false,
  "blacklist_status": "clean" | "listed" | "flagged",
  "transaction_count": 0,
  "first_seen": "ISO8601 timestamp",
  "last_active": "ISO8601 timestamp",
  "total_volume_usd": 0.0,
  "high_value_txns": 0,
  "unique_interactions": 0,
  "smart_contract_interactions": 0,
  "defi_protocols": ["protocol names"],
  "nft_collections": ["collection names"],
  "recommendation": "SAFE_TO_INTERACT" | "PROCEED_WITH_CAUTION" | "BLOCK_IMMEDIATELY",
  "confidence": 0.0-1.0,
  "verification_timestamp": "ISO8601 timestamp"
}
```

## 风险等级定义

- **高风险**：立即阻止交易——发现明显的欺诈/诈骗迹象或非法活动
- **中等风险**：谨慎操作——检测到可疑模式，需要进一步验证
- **低风险**：可以安全交互——钱包历史记录良好
- **验证通过**：最佳状态——钱包合法且活动正常

## 常见的欺诈迹象

### 钓鱼攻击
与钓鱼攻击、虚假网站或社会工程学诈骗相关的钱包

### 金字塔/庞氏骗局
与已知金字塔骗局、庞氏骗局或退出骗局相关的地址

### 混合器/洗钱工具使用
使用混合器或洗钱工具来掩盖交易来源的钱包（通常属于非法行为）

### 黑客攻击/漏洞利用
接收来自已知黑客攻击、漏洞或智能合约漏洞的资金的地址

### 洗钱行为
交易模式符合洗钱操作的特征

### 被盗资金
被标记为接收或持有被盗加密货币的钱包

### 受制裁的地址
列入政府制裁名单（如OFAC等）的钱包

## 支持的区块链

- Ethereum (ETH)
- Binance Smart Chain (BSC)
- Polygon (MATIC)
- Arbitrum
- Optimism
- Base
- Avalanche C-Chain
- Fantom
- 其他区块链——可根据需求指定

## 价格与价值

**费用**：每次钱包验证1.00美元（USDC）

**与其他方案的比较：**
- 手动钱包调查：每个地址需要30-60分钟
- 区块链取证服务：每个钱包分析费用50-200美元
- 事后欺诈恢复：平均损失超过10,000美元
- 监管罚款：违反反洗钱法规的罚款超过100,000美元

**投资回报率（ROI）**：一次成功的欺诈预防措施可以覆盖10,000多次验证的费用。

## 使用场景

### DeFi协议保护
在允许存款、取款或协议交互之前，验证钱包地址。自动阻止高风险钱包

### NFT市场安全
筛查买家和卖家的欺诈行为，保护用户免受NFT交易诈骗

### 支付网关验证
在接收加密货币支付之前，验证发送方的钱包地址。减少退款和欺诈损失

### DAO资金管理
在执行资金交易之前，验证提案创建者和收款人

### Airdrop/代币分发
筛查收款人钱包，防止将代币分配给诈骗者、机器人或受制裁的地址

### 交易所用户注册
在用户注册过程中验证钱包的真实性，以确保符合KYC/AML要求

### 借贷协议安全
在启用抵押品存款或贷款发放之前，验证借款人和贷款人的钱包

### 跨链桥接安全
在跨链交易中验证源地址和目标地址，防止非法资金流动

## 集成示例

### DeFi存款网关

```bash
#!/bin/bash
# defi-deposit-gate.sh

USER_WALLET=$1
DEPOSIT_AMOUNT=$2

# Verify wallet before allowing deposit
RESULT=$(verify_wallet "$USER_WALLET")
RISK=$(echo "$RESULT" | jq -r '.risk_level')

if [[ "$RISK" == "HIGH" ]]; then
  echo "Deposit blocked: High-risk wallet"
  exit 1
fi

# Allow deposit
./process-deposit.sh "$USER_WALLET" "$DEPOSIT_AMOUNT"
```

### NFT市场过滤

```bash
#!/bin/bash
# nft-marketplace-seller-verification.sh

SELLER_WALLET=$1
NFT_CONTRACT=$2
TOKEN_ID=$3

# Verify seller before allowing listing
RESULT=$(verify_wallet "$SELLER_WALLET")
ILLICIT=$(echo "$RESULT" | jq -r '.deliverable.illicit_activity')

if [[ "$ILLICIT" == "true" ]]; then
  echo "Listing rejected: Seller wallet flagged for illicit activity"
  exit 1
fi

# Create NFT listing
./create-listing.sh "$SELLER_WALLET" "$NFT_CONTRACT" "$TOKEN_ID"
```

### 批量钱包筛查

```bash
#!/bin/bash
# batch-wallet-screening.sh

# Screen multiple wallets for airdrop eligibility
WALLET_LIST="wallets.txt"
ELIGIBLE_WALLETS="eligible.txt"

> "$ELIGIBLE_WALLETS"  # Clear file

while IFS= read -r wallet; do
  RESULT=$(verify_wallet "$wallet")
  RISK=$(echo "$RESULT" | jq -r '.deliverable.risk_level')
  
  if [[ "$RISK" == "LOW" || "$RISK" == "VERIFIED_CLEAN" ]]; then
    echo "$wallet" >> "$ELIGIBLE_WALLETS"
    echo "✓ $wallet - ELIGIBLE"
  else
    echo "✗ $wallet - BLOCKED ($RISK)"
  fi
done < "$WALLET_LIST"

echo "Screening complete. Eligible wallets saved to $ELIGIBLE_WALLETS"
```

## 合规性优势

### 反洗钱/了解客户（AML/KYC）要求
通过验证钱包真实性来履行尽职调查义务，保持审计记录以符合监管要求

### 制裁筛查
自动检测并阻止受制裁的地址（如OFAC、欧盟等名单）

### 监管报告
生成验证报告，以满足监管文件和审计要求

### 风险管理
记录风险评估结果，以支持内部合规性和法律防护

## 快速入门指南

```bash
# 1. Install the ACP skill from GitHub
Install the skill from https://github.com/Virtual-Protocol/openclaw-acp
git clone https://github.com/Virtual-Protocol/openclaw-acp
cd openclaw-acp
npm install

# 2. Authenticate
acp setup

# 3. Find Cybercentry Wallet Verification service
acp browse "Cybercentry Wallet Verification" --json

# 4. Verify a wallet address
acp job create 0xCYBERCENTRY_WALLET cybercentry-wallet-verification \
  --requirements '{"wallet_address": "0x...", "chain": "ethereum"}' --json

# 5. Get results (10-30 seconds)
acp job status <jobId> --json

# 6. Use risk_level to allow/block transaction
```

## 相关资源

- Cybercentry官方资料：https://clawhub.ai/Cybercentry/cybercentry-wallet-verification
- Twitter/X账号：https://x.com/cybercentry
- ACP平台：https://app.virtuals.io
- OpenClaw GitHub仓库：https://github.com/openclaw/openclaw

## 服务简介

Cybercentry钱包验证服务由[@cybercentry](https://x.com/cybercentry)维护，仅在Virtuals Protocol ACP市场上提供。该服务为Web3生态系统提供实时的欺诈检测功能。