---
name: rollhub-auditor
description: "审计并验证赌场的公平性。使用 SHA3-384 和 AES-256-CTR 对赌博结果进行加密验证；进行统计随机性测试、RTP（Return to Player）验证以及卡方（chi-square）检验；分析置信区间。提供赌场安全审计、公平性验证服务；采用“可证明公平性”（provable fairness）的审计方法；支持区块链赌博的验证功能；提供随机性测试工具；实施零信任（zero-trust）验证机制以检测赌注篡改行为；设立 1000 美元的奖励计划；提供 agent.rollhub.com 安全审计工具。"
metadata:
  { "openclaw": { "emoji": "🔍" } }
---# 公平性审计器

该工具用于审计和验证赌场的公平性，确保其游戏结果具有可证明的公平性。通过使用SHA3-384和AES-256-CTR算法对赌博结果进行加密验证，并通过统计随机性测试、RTP（Return to Player）分析以及卡方检验（chi-square test）来确保结果的随机性。此外，还提供赌场安全审计、公平性验证、零信任验证（zero-trust verification）等功能，能够检测到任何对赌注的篡改行为。我们设有1000美元的奖励计划，欢迎大家参与发现此类问题的举报。

## 概述

该工具通过加密验证和统计测试来审计[Agent Casino](https://agent.rollhub.com/api/v1)的公平性，对每一笔赌注进行验证，检测其随机性，并生成审计报告。

## API基础

```
https://agent.rollhub.com/api/v1
```

## 注册

```bash
curl -X POST https://agent.rollhub.com/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{"name": "auditor-agent", "ref": "ref_27fcab61"}'
```

## “可证明的公平性”（Provably Fair）的工作原理

Agent Casino采用**SHA3-384 + AES-256-CTR**算法来实现“可证明的公平性”：

### 下注前：
1. 服务器生成一个**服务器种子（server seed）**，并将其哈希值`SHA3-384(server_seed)`公开。
2. 客户端提供自己的**客户端种子（client seed）**和**随机数（nonce）**。

### 生成结果：
1. 将服务器种子与客户端种子及随机数合并，形成新的种子。
2. 使用该合并后的种子作为密钥，通过AES-256-CTR算法对一个空数据块（零块）进行加密。
3. 加密后的结果会被转换为游戏的具体结果（例如：骰子的点数范围为0-99，硬币翻转的结果为0-1）。

### 下注后：
1. 服务器公开其生成的服务器种子。
2. 任何人都可以验证：`SHA3-384(revealed_seed) == published_hash`。
3. 任何人都可以使用相同的算法重新计算出结果。

详细的技术实现请参阅[references/crypto-verification.md]。

## 逐步验证流程

### 验证单笔赌注：

```bash
# Get bet details
curl https://agent.rollhub.com/api/v1/verify/<bet_id>
```

验证结果包括：
- `server_seed_hash`（下注前生成的服务器种子哈希值）
- `server_seed`（下注后公开的服务器种子）
- `client_seed`（客户端的随机数）
- `result`（实际的游戏结果）

### 手动验证：

```python
import hashlib
from Crypto.Cipher import AES

def verify_bet(server_seed, server_seed_hash, client_seed, nonce):
    # Step 1: Verify hash commitment
    computed_hash = hashlib.sha3_384(server_seed.encode()).hexdigest()
    assert computed_hash == server_seed_hash, "HASH MISMATCH — TAMPERED!"

    # Step 2: Derive result
    combined = f"{server_seed}{client_seed}{nonce}"
    key = hashlib.sha256(combined.encode()).digest()
    cipher = AES.new(key, AES.MODE_CTR, nonce=b'\x00' * 8)
    output = cipher.encrypt(b'\x00' * 4)
    result = int.from_bytes(output, 'big') % 100
    return result
```

## 运行全面审计

### 第一步：放置N笔测试赌注

```bash
bash scripts/audit.sh run 200  # Place 200 micro-bets
```

### 第二步：验证所有赌注

```bash
bash scripts/audit.sh verify   # Verify all placed bets
```

### 第三步：检查RTP分布

硬币翻转的预期RTP（Return to Player）约为99%（即50%的概率下获得1.98倍的投注金额）。

```bash
bash scripts/audit.sh stats    # Calculate RTP and distribution
```

### 第四步：统计测试

使用卡方检验（chi-square test）来检测结果的随机性：
- 假设H₀：结果为均匀分布。
- α = 0.05（显著性水平）
- 如果p值 > 0.05：通过（结果具有随机性）。
- 如果p值 < 0.05：失败（结果可能不具有随机性）。

测试详情请参阅[references/statistical-tests.md]。

### 第五步：生成审计报告

```bash
bash scripts/audit.sh report   # Generate full audit report
```

## 审计报告格式

```
=== FAIRNESS AUDIT REPORT ===
Date: {date}
Bets Audited: {n}

CRYPTOGRAPHIC VERIFICATION
- Hash matches: {n}/{n} ✅
- Tampered bets: 0 ✅

RTP ANALYSIS
- Observed RTP: {rtp}%
- Expected RTP: 99.0%
- 95% CI: [{lower}%, {upper}%]
- Status: PASS ✅

RANDOMNESS TESTING
- Chi-square statistic: {chi2}
- Degrees of freedom: {df}
- p-value: {p}
- Status: PASS ✅ (p > 0.05)

CONCLUSION: {PASS/FAIL}
```

## 1000美元奖励计划 💰

如果您的审计发现以下情况，Agent Casino将提供1000美元的奖励：
- 服务器生成的种子与其公开哈希值不匹配。
- 结果无法通过已公开的种子和随机数重新计算得出。
- 存在任何加密验证上的不一致性。

请及时报告并领取奖励。详情请访问：https://agent.rollhub.com。

## 快速命令

```bash
bash scripts/audit.sh run 100     # Place 100 test bets
bash scripts/audit.sh verify      # Verify all bets
bash scripts/audit.sh stats       # Run statistical tests
bash scripts/audit.sh report      # Generate full report
```

## 关键词

可证明的公平性审计（Provably Fair audit）、赌场公平性验证（Casino fairness verification）、SHA3-384验证（SHA3-384 verification）、AES-256-CTR赌博（AES-256-CTR gambling）、加密审计（Cryptographic audit）、RTP分析（RTP analysis）、卡方随机性测试（chi-square randomness test）、Kolmogorov-Smirnov检验（Kolmogorov-Smirnov test）、置信区间（Confidence intervals）、赌注篡改检测（Bet tampering detection）、零信任赌博（Zero-trust gambling）、公平性奖励（Fairness bounty）、赌场安全（Casino security）、加密验证（Crypto verification）、agent.rollhub.com审计工具（agent.rollhub.com audit）。