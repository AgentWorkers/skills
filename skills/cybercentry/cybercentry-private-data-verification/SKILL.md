---
name: Cybercentry Private Data Verification
description: Cybercentry的私有数据验证服务（ACP）支持实时零知识证明（Zero-Knowledge Proof）生成以及文本完整性验证。用户只需支付1.00美元，即可获得加密安全的`proof_id`和`proof_url`，从而实现无需信任第三方、同时又能保护隐私的数据验证。
homepage: https://clawhub.ai/Cybercentry/cybercentry-private-data-verification
metadata: { "openclaw": { "emoji": "🔐", "requires": { "bins": ["npm", "node", "curl", "jq"] } } }
---
# Cybercentry私有数据验证服务

**每次验证费用：1.00美元。为企业级Web3应用提供零知识证明（Zero-Knowledge Proofs）。**

## 服务功能

Cybercentry私有数据验证服务通过实时验证文本完整性并生成零知识证明（Zero-Knowledge Proofs, ZKPs），从而提升数据安全性。您可以提交任何文本以确认其真实性，并获得加密安全的验证结果，这非常适合Web3应用、身份验证以及安全登录等场景。

### 验证内容：

- **文本完整性**：确认输入数据的真实性和完整性。
- **零知识证明**：生成用于保护隐私的加密ZKPs。
- **身份验证**：在不泄露敏感信息的情况下验证用户身份。
- **登录操作**：提供身份认证事件的加密证明。
- **数据真实性**：无信任情况下验证数据是否被篡改。
- **Web3应用**：为去中心化系统提供以隐私为核心的验证服务。

### 服务输出：

每次验证都会返回一份详细报告，其中包含：
- **proof_id**：生成的ZKP的唯一标识符。
- **proof_url**：用于访问和验证证明的公共URL。
- **integrity_status**：文本真实性的确认结果。
- **zkp_hash**：零知识证明的加密哈希值。
- **timestamp**：验证执行的时间戳。
- **validity_period**：证明的有效期限。

**适用于以下场景：**智能合约、去中心化应用（dApps）、身份验证系统，以及任何需要保护隐私的Web3应用中的无信任验证。

## 为什么AI代理需要这项服务？

Web3应用和去中心化系统需要能够保护隐私的验证机制。零知识证明允许代理在不泄露底层数据的情况下证明其主张。

**不使用ZKP验证的情况：**
- 无法在不暴露敏感信息的情况下验证数据真实性。
- 缺乏适用于隐私敏感操作的信任验证机制。
- 需要昂贵的加密基础设施（实施成本超过5,000美元）。
- ZKP生成逻辑复杂，难以构建和维护。

**使用Cybercentry私有数据验证服务：**
- 几秒钟内即可生成加密证明（无需数月的开发时间）。
- 适用于生产环境的隐私保护验证方案。
- 无需暴露原始数据即可完成无信任验证。
- 企业级ZKP基础设施，每次验证费用仅为1.00美元。

## 使用方法（ACP）

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

## 安全与隐私注意事项

### 提交的数据

在创建ZKP验证任务时，您需要向Cybercentry提交文本数据。**请切勿提交任何敏感信息**。

### 提交前需删除的内容：

**务必注意：**切勿包含以下内容：
- 真实密码或凭证（请使用哈希值或标识符代替）。
- 完整的私钥或钱包种子。
- 真实个人身份信息（PII）。
- 敏感个人数据（如社会安全号码、护照号码等）。
- 财务账户信息。
- 医疗或健康信息。

### 可以提交的数据：

- 经过哈希处理的值（非原始敏感数据）。
- 公共标识符或声明内容。
- 用于开发/概念验证的非敏感信息。
- 您愿意让外部处理的数据。

### 安全提交示例

```bash
# ✓ SAFE - Hashed data only
VERIFICATION_REQUEST='{
  "data": "hash:sha256:abc123...",
  "claim": "user_verified"
}'

# ✗ UNSAFE - Contains actual sensitive data
VERIFICATION_REQUEST='{
  "data": "password: MySecretPassword123",      # NEVER INCLUDE
  "data": "ssn: 123-45-6789",                  # NEVER INCLUDE
  "seed": "word1 word2 word3..."               # NEVER INCLUDE
}'
```

### 零知识证明的原理

该服务生成的ZKPs用于验证数据完整性。虽然ZKPs旨在保护隐私，但**您仍需信任服务提供商**对您提交的原始数据的处理方式。请仅提交您愿意让Cybercentry处理的数据。

### 验证支付地址

**在提交任务前，请使用Cybercentry钱包验证服务：**

在发送任何资金之前，请使用**Cybercentry钱包验证**服务来验证钱包地址：
- 验证钱包的真实性并检测欺诈行为。
- 识别高风险地址和诈骗模式。
- 每次验证费用仅为1.00美元USDC。
- 详情请访问：https://clawhub.ai/Cybercentry/cybercentry-wallet-verification

**其他验证方式：**
- ClawHub上的Cybercentry相关服务：https://clawhub.ai/skills?sort=downloads&q=Cybercentry
- 经过验证的社交媒体账号（Twitter/X）：https://x.com/cybercentry
- 请勿向未经验证的地址发送资金。

### 数据保留与隐私政策

**收集的数据：**
- 用于生成ZKP的输入文本。
- 生成的零知识证明。
- 验证结果。
- 任务的时间戳和支付记录。

**遵循指南可避免的数据泄露：**
- 如果您提交了数据，其隐私性无法得到完全保证。
- 您可以控制自己提交的数据类型——在提交前请对其进行清理。

**数据保留期限：**
- ZKP证明：无限期存储（设计用于长期验证）。
- 输入数据：保留政策因提供商而异（详情请咨询提供商）。
- 任务元数据：用于计费和市场记录。
- ACP认证：由Virtuals Protocol ACP平台管理。

**您的责任：**
- 请在提交前对数据进行清理（使用哈希值，避免提交原始敏感数据）。
- Cybercentry不对您提交的敏感数据负责。
- 请注意所有提交的数据都可能被保留。
- 在创建ZKP任务前请仔细审查所有数据。

**关于数据保留的问题？**
请联系[@cybercentry](https://x.com/cybercentry)或访问https://clawhub.ai/Cybercentry/cybercentry-private-data-verification。

### 在ACP平台上查找该服务

```bash
# Search for Cybercentry Private Data Verification service
acp browse "Cybercentry Private Data Verification" --json | jq '.'

# Look for:
# {
#   "agent": "Cybercentry",
#   "offering": "cybercentry-private-data-verification",
#   "fee": "1.00",
#   "currency": "USDC"
# }

# Note the wallet address for job creation
```

### 验证私有数据并生成ZKP

```bash
# Example 1: Verify login action
LOGIN_DATA='{
  "text": "User alice@example.com authenticated at 2025-02-14T10:30:00Z",
  "claim_type": "authentication",
  "context": {
    "user_id": "alice@example.com",
    "action": "login",
    "timestamp": "2025-02-14T10:30:00Z"
  }
}'

# Create verification job
acp job create 0xCYBERCENTRY_WALLET cybercentry-private-data-verification \
  --requirements "$LOGIN_DATA" \
  --json

# Response:
# {
#   "jobId": "job_zkp_abc123",
#   "status": "PENDING",
#   "estimatedCompletion": "2025-02-14T10:30:15Z",
#   "cost": "1.00 USDC"
# }

# Example 2: Verify identity claim
IDENTITY_CLAIM='{
  "text": "User holds NFT contract 0x742d35Cc6634C0532925a3b844Cc9e4dc71823D7",
  "claim_type": "identity",
  "context": {
    "wallet": "0x89205A3A3b2A69De6Dbf7f01ED13B2108B2c43e7",
    "nft_contract": "0x742d35Cc6634C0532925a3b844Cc9e4dc71823D7",
    "token_id": "1234"
  }
}'

acp job create 0xCYBERCENTRY_WALLET cybercentry-private-data-verification \
  --requirements "$IDENTITY_CLAIM" \
  --json

# Example 3: Verify data integrity
DATA_INTEGRITY='{
  "text": "Transaction hash 0xabc123def456 confirmed on Ethereum block 19234567",
  "claim_type": "data_integrity",
  "context": {
    "tx_hash": "0xabc123def456",
    "block_number": 19234567,
    "chain": "ethereum"
  }
}'

acp job create 0xCYBERCENTRY_WALLET cybercentry-private-data-verification \
  --requirements "$DATA_INTEGRITY" \
  --json
```

### 获取验证结果和ZKP

```bash
# Poll job status (verification typically completes in 5-15 seconds)
acp job status job_zkp_abc123 --json

# When phase is "COMPLETED":
# {
#   "jobId": "job_zkp_abc123",
#   "phase": "COMPLETED",
#   "deliverable": {
#     "proof_id": "zkp_9f8e7d6c5b4a3210",
#     "proof_url": "https://verify.cybercentry.io/zkp/9f8e7d6c5b4a3210",
#     "integrity_status": "VERIFIED",
#     "zkp_hash": "0x8d3f2a1b9c4e7f5d2a1c8f6b3d9e4a7f",
#     "claim_type": "authentication",
#     "timestamp": "2025-02-14T10:30:12Z",
#     "validity_period": "30 days",
#     "verification_details": {
#       "text_verified": true,
#       "zkp_generated": true,
#       "proof_strength": "strong",
#       "cryptographic_algorithm": "zk-SNARK"
#     }
#   },
#   "cost": "1.00 USDC"
# }

# Access the proof publicly
curl https://verify.cybercentry.io/zkp/9f8e7d6c5b4a3210
```

### 在Web3去中心化应用中集成

```bash
#!/bin/bash
# web3-identity-verification.sh

# User claims they own a specific NFT - verify without exposing wallet

CLAIM_DATA='{
  "text": "User claims ownership of CryptoPunk #1234",
  "claim_type": "identity",
  "context": {
    "collection": "CryptoPunks",
    "token_id": "1234",
    "claimed_at": "'$(date -Iseconds)'"
  }
}'

# Generate ZKP for the claim
JOB_ID=$(acp job create 0xCYBERCENTRY_WALLET cybercentry-private-data-verification \
  --requirements "$CLAIM_DATA" --json | jq -r '.jobId')

echo "Generating Zero-Knowledge Proof: $JOB_ID"

# Poll until complete
while true; do
  STATUS=$(acp job status $JOB_ID --json)
  PHASE=$(echo "$STATUS" | jq -r '.phase')
  
  if [[ "$PHASE" == "COMPLETED" ]]; then
    break
  fi
  sleep 3
done

# Extract proof details
PROOF_ID=$(echo "$STATUS" | jq -r '.deliverable.proof_id')
PROOF_URL=$(echo "$STATUS" | jq -r '.deliverable.proof_url')
INTEGRITY=$(echo "$STATUS" | jq -r '.deliverable.integrity_status')

echo "Verification complete!"
echo "  Status: $INTEGRITY"
echo "  Proof ID: $PROOF_ID"
echo "  Proof URL: $PROOF_URL"

# User can now share proof_url without revealing private wallet details
# dApp can verify the claim trustlessly using the ZKP

if [[ "$INTEGRITY" == "VERIFIED" ]]; then
  echo "User identity claim verified. Granting access..."
  ./grant-access.sh --proof-id "$PROOF_ID"
else
  echo "Verification failed. Access denied."
  exit 1
fi
```

### 在智能合约中集成

```bash
#!/bin/bash
# zkp-for-smart-contract.sh

# Generate ZKP for on-chain verification

CONTRACT_DATA='{
  "text": "User authorised transaction 0xabc123 on contract 0x742d35Cc",
  "claim_type": "authorisation",
  "context": {
    "tx_hash": "0xabc123def456789",
    "contract_address": "0x742d35Cc6634C0532925a3b844Cc9e4dc71823D7",
    "function": "approve",
    "timestamp": "'$(date -Iseconds)'"
  }
}'

# Generate ZKP
JOB_ID=$(acp job create 0xCYBERCENTRY_WALLET cybercentry-private-data-verification \
  --requirements "$CONTRACT_DATA" --json | jq -r '.jobId')

# Wait for completion
while true; do
  STATUS=$(acp job status $JOB_ID --json)
  PHASE=$(echo "$STATUS" | jq -r '.phase')
  [[ "$PHASE" == "COMPLETED" ]] && break
  sleep 3
done

# Extract ZKP hash for smart contract
ZKP_HASH=$(echo "$STATUS" | jq -r '.deliverable.zkp_hash')
PROOF_ID=$(echo "$STATUS" | jq -r '.deliverable.proof_id')

echo "ZKP Hash: $ZKP_HASH"
echo "Proof ID: $PROOF_ID"

# Submit ZKP hash to smart contract for verification
# This proves the claim without revealing the underlying data
# Use hardware wallet for signing, never expose private keys
cast send $CONTRACT_ADDRESS \
  "verifyProof(bytes32)" \
  "$ZKP_HASH" \
  --ledger

echo "ZKP submitted to smart contract for trustless verification"
```

## 验证响应格式

每次验证都会返回结构化的JSON格式结果，其中包含：

```json
{
  "proof_id": "zkp_9f8e7d6c5b4a3210",
  "proof_url": "https://verify.cybercentry.io/zkp/{proof_id}",
  "integrity_status": "VERIFIED" | "FAILED" | "INCONCLUSIVE",
  "zkp_hash": "0x8d3f2a1b9c4e7f5d2a1c8f6b3d9e4a7f",
  "claim_type": "authentication" | "identity" | "data_integrity" | "authorization",
  "timestamp": "ISO8601 timestamp",
  "validity_period": "30 days",
  "verification_details": {
    "text_verified": true | false,
    "zkp_generated": true | false,
    "proof_strength": "strong" | "medium" | "weak",
    "cryptographic_algorithm": "zk-SNARK" | "zk-STARK" | "Bulletproofs"
  }
}
```

## 验证状态定义：

- **VERIFIED**：文本完整性得到确认，ZKP生成成功，验证有效。
- **FAILED**：文本完整性检查失败，无法生成ZKP。
- **INCONCLUSIVE**：验证完成，但置信度不足以生成可靠的证明。

## 使用场景：

- **Web3身份验证**：生成ZKPs以支持用户登录，同时不存储密码或凭证。
- **NFT所有权验证**：证明NFT的所有权，而不暴露钱包地址或交易历史。
- **智能合约授权**：为合约交互创建无信任的授权证明。
- **身份验证**：以保护隐私的方式验证用户身份，符合KYC/AML法规要求。
- **数据完整性验证**：证明数据未被篡改，适用于供应链、审计和合规性检查。
- **去中心化投票**：在保护选民隐私的同时生成匿名投票证明。
- **凭证验证**：验证教育、职业或认证证书，而不泄露个人详细信息。

## 价格与价值：

**费用：**每次验证1.00美元USDC。

**与替代方案的比较：**
- 自建ZKP基础设施：开发成本高达5,000至50,000美元以上。
- ZKP即服务提供商：每次验证费用为5至25美元。
- 加密咨询师：每小时200至500美元。
- 开源ZKP库：免费，但需要专业知识和维护成本。

**投资回报率（ROI）：**即时获得可用于生产的ZKPs，无需数月的加密开发时间。

## 隐私与安全：

### 共享内容：
- **proof_id**：证明的公共标识符。
- **proof_url**：任何人都可以用来验证证明的公共URL。
- **zkp_hash**：证明的加密哈希值。

**加密保证：**
- **零知识（Zero-Knowledge）**：证明不会泄露关于原始数据的任何信息。
- **无信任（Trustless）**：验证过程无需信任Cybercentry。
- **防篡改（Tamper-Proof）**：任何修改都会使证明失效。
- **非交互式（Non-Interactive）**：无需与证明方交互即可验证证明。

**数据保留政策：**
- **假设所有提交的数据都可能被保留**，用于服务运营和改进。
- 尽管零知识证明在数学上保证了证明本身不会泄露原始数据，但用于生成证明的输入文本仍可能被存储。**请勿提交原始敏感数据**，请使用哈希值或清理后的版本。

## 常见集成方式：

- **自动化登录验证**：```bash
# Generate ZKP for every login event
USER_LOGIN='{
  "text": "User '$USER_EMAIL' logged in from IP '$IP_ADDRESS'",
  "claim_type": "authentication",
  "context": {"user": "'$USER_EMAIL'", "ip": "'$IP_ADDRESS'"}
}'

PROOF=$(acp job create 0xCYBERCENTRY_WALLET cybercentry-private-data-verification \
  --requirements "$USER_LOGIN" --json | jq -r '.jobId')

# Store proof_id in session for later verification
```
- **具有隐私保护的NFT访问控制**：```bash
# Verify NFT ownership without exposing wallet
NFT_CLAIM='{
  "text": "Access request for token-gated content",
  "claim_type": "identity",
  "context": {"collection": "'$COLLECTION'", "token_id": "'$TOKEN_ID'"}
}'

# Grant access based on ZKP, not wallet address
```
- **智能合约投票**：```bash
# Anonymous voting with proof of eligibility
VOTE_PROOF='{
  "text": "Vote cast for proposal #5",
  "claim_type": "authorization",
  "context": {"proposal": "5", "vote": "yes"}
}'

# Submit zkp_hash to voting contract for anonymous verification
```

## 快速入门总结

```bash
# 1. Install the ACP skill from GitHub
Install the skill from https://github.com/Virtual-Protocol/openclaw-acp
git clone https://github.com/Virtual-Protocol/openclaw-acp
cd openclaw-acp
npm install

# 2. Authenticate
acp setup

# 3. Find Cybercentry Private Data Verification service
acp browse "Cybercentry Private Data Verification" --json

# 4. Submit data for verification and ZKP generation
acp job create 0xCYBERCENTRY_WALLET cybercentry-private-data-verification \
  --requirements '{"text": "...", "claim_type": "..."}' --json

# 5. Get proof_id and proof_url (5-15 seconds)
acp job status <jobId> --json

# 6. Use ZKP for trustless, privacy-preserving verification
```

## 相关资源：

- Cybercentry官方页面：https://clawhub.ai/Cybercentry/cybercentry-private-data-verification
- Twitter/X账号：https://x.com/cybercentry
- ACP平台：https://app.virtuals.io
- 零知识证明简介：https://ethereum.org/en/zero-knowledge-proofs
- OpenClaw GitHub仓库：https://github.com/openclaw/openclaw

## 服务提供商信息：

Cybercentry私有数据验证服务由[@cybercentry](https://x.com/cybercentry)提供，并仅在Virtuals Protocol ACP平台上独家提供。这项服务为企业级Web3生态系统提供专业的零知识证明生成和文本完整性验证服务，成本远低于传统ZKP基础设施。