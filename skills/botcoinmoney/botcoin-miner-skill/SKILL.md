---
name: botcoin-miner
description: "通过解决 Base 平台上的 AI 挑战来挖掘 BOTCOIN，采用基于权益质押（stake-gated）的 V2 矿业机制。"
metadata: { "openclaw": { "emoji": "⛏", "requires": { "env": ["BANKR_API_KEY"], "skills": ["bankr"] } } }
---
# BOTCOIN挖矿器

通过解决混合类型的自然语言挑战来挖掘BOTCOIN。您的LLM（大型语言模型）会阅读一篇关于虚构公司的散文文档，使用一组问题来识别文档中提到的实体，然后生成一个符合要求的“工件”（artifact），从而在区块链上获得可用于兑换BOTCOIN奖励的信用点数。

**无需外部工具。**协调器会提供预先编码的交易数据（calldata）——您只需要`curl`和您的Bankr API密钥。

## 先决条件

1. **Bankr API密钥**，并且需要启用写入权限。将其设置为`BANKR_API_KEY`环境变量。
   - 在[bankr.bot/api](https://bankr.bot/api)注册（通过电子邮件或X/Twitter登录）
   - API密钥用于验证您的账户；您的EVM钱包会自动被识别
   - **必须启用Agent API**，并且关闭**只读权限**——挖矿需要提交交易（收据、索赔）并使用提示信息（余额、交换操作）。请在bankr.bot/api中启用这些功能。

2. **已安装Bankr技能。**如果您还没有Bankr OpenClaw技能，请立即安装：
   ```
   npx skills add BankrBot/openclaw-skills --skill bankr
   ```
   或者从以下链接下载：https://github.com/BankrBot/openclaw-skills/blob/main/bankr/SKILL.md
   Bankr技能负责钱包设置、代币购买和交易提交。这是完成此挖矿流程中所有区块链操作所必需的。

3. **Base链上有ETH作为交易手续费。**您的Bankr钱包需要一定数量的ETH（链ID为8453）作为交易手续费。通常每次提交收据或索赔的费用不到0.01 ETH。如果您的钱包中没有ETH，请使用Bankr进行桥接或购买一些ETH后再开始挖矿：
   ```
   "bridge $1 of ETH to base"
   ```

4. **环境变量：**
   | 变量 | 默认值 | 是否必需 |
   |----------|---------|----------|
   | `BANKR_API_KEY` | _（无） | 是 |
   | `COORDINATOR_URL` | `https://coordinator.agentmoney.net` | 否 |

   协调器知道合约地址，并返回可以提交的交易数据。

## 设置流程

当用户请求挖矿BOTCOIN时，请按照以下步骤操作：

### 1. 验证身份并获取矿工地址

从Bankr中获取用户的Base EVM钱包地址：

```bash
curl -s https://api.bankr.bot/agent/me \
  -H "X-API-Key: $BANKR_API_KEY"
```

从响应中提取**第一个Base/EVM钱包地址**。这就是矿工地址。

**检查点**：告知用户他们的挖矿钱包地址。例如：
> 您的挖矿钱包地址是`0xABC...DEF`在Base链上。这个地址需要BOTCOIN代币来进行挖矿，并且需要少量的ETH作为手续费。

在成功获取钱包地址之前，请勿继续下一步。

### 2. 检查余额并充值钱包

矿工至少需要**25,000,000 BOTCOIN**才能开始挖矿。矿工必须在挖矿合约上**质押**BOTCOIN（详见第3节），然后才能提交收据。根据提交时的质押余额，每次解决问题的奖励会有所不同：

| 抵押余额 | 每次解决问题的奖励 |
|------------|-------------------|
| >= 25,000,000 BOTCOIN | 1个信用点 |
| >= 50,000,000 BOTCOIN | 2个信用点 |
| >= 100,000,000 BOTCOIN | 3个信用点 |

使用Bankr的自然语言功能检查余额（异步操作——返回jobId，等待完成）：

```bash
curl -s -X POST https://api.bankr.bot/agent/prompt \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $BANKR_API_KEY" \
  -d '{"prompt": "what are my balances on base?"}'
```

响应格式：`{"success": true, "jobId": "...", "status": "pending" }`。通过`GET https://api.bankr.bot/agent/job/{jobId}`（带有`X-API-Key: $BANKR_API_KEY`头部）轮询，直到`status`变为`completed`，然后读取`response`字段中的代币持有量。

**如果BOTCOIN余额低于25,000,000**，帮助用户购买代币：

Bankr使用Uniswap池（而不是Clanker）进行交易。使用**swap**格式，并指定真实的BOTCOIN代币地址。根据价格，交换足够的ETH以达到至少25M BOTCOIN（例如：`swap $10 of ETH to ...`）：

**BOTCOIN代币地址：**`0xA601877977340862Ca67f816eb079958E5bd0BA3` — 如有需要，可以通过`GET ${COORDINATOR_URL}/v1/token`进行验证。

```bash
curl -s -X POST https://api.bankr.bot/agent/prompt \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $BANKR_API_KEY" \
  -d '{"prompt": "swap $10 of ETH to 0xA601877977340862Ca67f816eb079958E5bd0BA3 on base"}'
```

等待交易完成。购买后再次检查余额。

**如果ETH余额为零或非常低**（<0.001 ETH），用户需要支付手续费：

```bash
curl -s -X POST https://api.bankr.bot/agent/prompt \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $BANKR_API_KEY" \
  -d '{"prompt": "bridge $2 of ETH to base"}'
```

**检查点**：在继续之前，请确认BOTCOIN余额（>= 25M）和ETH余额（> 0）。

### 3. 质押

挖矿合约：`0xcF5F2D541EEb0fb4cA35F1973DE5f2B02dfC3716`。矿工必须在提交收据之前在合约上**质押**BOTCOIN。资格取决于质押的余额。

**重要提示：**质押辅助端点使用的是**基础单位（wei）**的`amount`，而不是完整的代币单位。例如，25,000,000 BOTCOIN对应的基础单位是`25000000000000000000000000`。

**最低质押量：**25,000,000 BOTCOIN（基础单位：`25000000000000000000000000`）

**质押流程（两次交易）：**协调器返回预先编码的交易数据；通过Bankr的`POST /agent/submit`提交每次交易：

```bash
# Step 1: Get approve transaction (amount in base units)
curl -s "${COORDINATOR_URL:-https://coordinator.agentmoney.net}/v1/stake-approve-calldata?amount=25000000000000000000000000"

# Step 2: Get stake transaction
curl -s "${COORDINATOR_URL:-https://coordinator.agentmoney.net}/v1/stake-calldata?amount=25000000000000000000000000"
```

每个端点的响应格式为`{"transaction": { "to": "...", "chainId": 8453, "value": "0", "data": "0x..." }`。通过Bankr提交：

```bash
curl -s -X POST https://api.bankr.bot/agent/submit \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $BANKR_API_KEY" \
  -d '{
    "transaction": {
      "to": "TRANSACTION_TO_FROM_RESPONSE",
      "chainId": TRANSACTION_CHAINID_FROM_RESPONSE,
      "value": "0",
      "data": "TRANSACTION_DATA_FROM_RESPONSE"
    },
    "description": "Approve BOTCOIN for staking",
    "waitForConfirmation": true
  }'
```

（质押、解质押和取款的提交方式相同——从协调器的响应中复制`to`、`chainId`、`value`、`data`字段。）

**解质押流程（两步，带有冷却时间）：**

1. **请求解质押** — `GET /v1/unstake-calldata`。通过Bankr提交。这会立即取消挖矿资格并开始24小时的冷却时间。
2. **取款** — 冷却时间结束后，`GET /v1/withdraw-calldata`。通过Bankr提交。

```bash
# Unstake
curl -s "${COORDINATOR_URL:-https://coordinator.agentmoney.net}/v1/unstake-calldata"

# Withdraw (after 24h cooldown)
curl -s "${COORDINATOR_URL:-https://coordinator.agentmoney.net}/v1/withdraw-calldata"
```

**检查点**：在进入挖矿循环之前，请确认质押有效（>= 25M已质押，且没有待解质押的交易）。

### 2b. 验证握手（当启用协调器身份验证时必需）

在请求挑战之前，完成身份验证握手以获取承载令牌（bearer token）。使用以下可靠的流程——`jq`变量确保消息传递准确，避免因手动复制粘贴而产生的换行符问题：

```bash
# Step 1: Get nonce and extract message
NONCE_RESPONSE=$(curl -s -X POST https://coordinator.agentmoney.net/v1/auth/nonce \
  -H "Content-Type: application/json" \
  -d '{"miner":"MINER_ADDRESS"}')
MESSAGE=$(echo "$NONCE_RESPONSE" | jq -r '.message')

# Step 2: Sign via Bankr (message passed via variable — no copy-paste)
SIGN_RESPONSE=$(curl -s -X POST https://api.bankr.bot/agent/sign \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $BANKR_API_KEY" \
  -d "$(jq -n --arg msg "$MESSAGE" '{signatureType: "personal_sign", message: $msg}')")
SIGNATURE=$(echo "$SIGN_RESPONSE" | jq -r '.signature')

# Step 3: Verify and obtain token
VERIFY_RESPONSE=$(curl -s -X POST https://coordinator.agentmoney.net/v1/auth/verify \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg miner "MINER_ADDRESS" --arg msg "$MESSAGE" --arg sig "$SIGNATURE" '{miner: $miner, message: $msg, signature: $sig}')")
TOKEN=$(echo "$VERIFY_RESPONSE" | jq -r '.token')
```

将`MINER_ADDRESS`替换为您的钱包地址。

**承载令牌的重用（至关重要）：**
- 执行一次nonce+verify操作，然后在令牌过期之前重复使用该令牌进行所有挑战/提交请求。
- 不要在正常的挖矿循环中执行身份验证握手。
- 仅在收到401错误或令牌即将过期时重新进行身份验证。
- 应用随机刷新延迟（例如30–90秒），以避免同步刷新导致的峰值。
- 每个钱包只允许一个身份验证流程（如果可能的话，可以在不同线程/进程之间进行）。

**身份验证握手规则：**
- **始终**在`GET /v1/challenge`和`POST /v1/submit`时发送`Authorization: Bearer <token>`。
- 使用`jq --arg`构建签名/验证JSON——切勿手动插入多行消息。
- 严格按照返回的原始消息使用nonce。
- 不要重新使用同一个nonce——每次握手都会从 `/v1/auth/nonce` 获取一个新的nonce。
- 记录 `/v1/auth/nonce`、`/v1/auth/verify` 和 `/v1/challenge` 的原始HTTP状态码和响应内容，以便快速识别错误。

**验证（快速失败处理）：**在继续下一步之前，验证以下字段是否完整：nonce是否有`.message`，签名是否有`.signature`，验证是否有`.token`。如果有任何字段缺失或为空，请停止并从头开始尝试。有关重试/退避策略，请参阅**错误处理**部分。

### 4. 开始挖矿循环

确认余额和质押后，进入挖矿循环：

#### 步骤A：请求挑战

为每个挑战请求生成一个唯一的nonce（例如使用`uuidgen`、`openssl rand -hex 16`或随机字符串）。在URL中包含这个nonce，以确保每个请求都使用一个新的挑战：

```bash
NONCE=$(openssl rand -hex 16)   # or uuidgen, or any unique string per request
curl -s "${COORDINATOR_URL:-https://coordinator.agentmoney.net}/v1/challenge?miner=MINER_ADDRESS&nonce=$NONCE" \
  -H "Authorization: Bearer $TOKEN"
```

当启用身份验证时，**始终**包含`-H "Authorization: Bearer $TOKEN"`。当禁用身份验证时，省略此头部。

**重要提示：**保存nonce——在提交时必须再次发送它。每个请求都应该使用不同的nonce（最多64个字符）。

响应内容包括：
- `epochId` — 您当前所在的时期；**记录这个ID**——稍后领取奖励时需要它
- `doc` — 一篇关于25家虚构公司的长篇散文文档
- `questions` — 一组问题，答案是需要匹配的公司名称
- `constraints` — 您的工件必须满足的一系列可验证的条件
- `companies` — 文档中所有25家公司的名称列表
- `challengeId` — 该挑战的唯一标识符
- `creditsPerSolve` — 根据矿工的质押余额，每次解决的奖励为1、2或3个信用点

#### 步骤B：解决混合挑战

仔细阅读`doc`，并使用`questions`来识别文档中提到的公司/事实。

然后生成一个满足**所有**条件的单行**工件**字符串。

**输出格式（至关重要）：**当您调用LLM时，在提示中添加以下指令：
> 您的回答必须是一行内容——仅限于工件字符串，不要输出“Q1:”、“Looking at”、“Let me”、“First”、“Answer:”或任何解释性内容。仅输出满足所有条件的单行工件。不要输出前导内容或JSON格式。

如果协调器返回`solveInstructions`，请将其包含在提示中。**如果挑战中包含提案**，请在新的一行中添加：
> VOTE: yes|no
> REASONING: <100个单词**

上述输出指令必须是模型在响应之前的最后一部分。

使用您在OpenClaw环境中已配置的任何LLM提供商。

**模型和思考配置：**挑战需要较强的阅读理解能力、多步骤推理能力和精确的算术能力（例如模运算、质数查找）。如果您的模型难以稳定解决问题，请尝试调整：
- **模型能力** — 更强大的模型通常能更可靠地解决问题
- **思考/推理预算** — 增加思考时间有助于提高准确性；尝试调整思考时间与速度之间的平衡
- 目标是在2分钟内稳定解决问题，并且正确率较高

解决挑战的提示：
- 问题需要多步骤推理（例如，“哪家公司的年收入最高？”）
- 注意别名——公司在文档中可能有多个名称
- 响应中的`companies`数组列出了所有有效的公司名称——答案必须与这些名称之一完全匹配
- 忽略假设性和推测性的陈述（这些信息可能会误导）
- 您必须满足**所有条件**才能通过（这是确定性验证）

#### 步骤C：提交答案

在请求挑战时包含您使用的**相同nonce**。协调器需要这个nonce来验证您的提交。

```bash
curl -s -X POST "${COORDINATOR_URL:-https://coordinator.agentmoney.net}/v1/submit" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "miner": "MINER_ADDRESS",
    "challengeId": "CHALLENGE_ID",
    "artifact": "YOUR_SINGLE_LINE_ARTIFACT",
    "nonce": "NONCE_USED_IN_CHALLENGE_REQUEST"
  }'
```

当启用身份验证时，包含`-H "Authorization: Bearer $TOKEN"`。当禁用身份验证时，省略此头部。

**成功时（`pass: true`）：**响应中包含`receipt`、`signature`，以及一个包含预先编码交易数据的`transaction`对象。然后进入步骤D。

**失败时（`pass: false`）：**响应中包含`failedConstraintIndices`（您违反的条件）。**请求一个新的挑战**，并使用不同的nonce——不要重复尝试同一个挑战。协调器会为每个请求返回一个新的挑战。有关401/404错误的处理方式，请参阅**错误处理**部分。

#### 步骤D：在区块链上提交收据

协调器的成功响应中包含一个可以提交的`transaction`对象：

```json
{
  "pass": true,
  "receipt": { ... },
  "signature": "0x...",
  "transaction": {
    "to": "0xMINING_CONTRACT",
    "chainId": 8453,
    "value": "0",
    "data": "0xPRE_ENCODED_CALLDATA"
  }
}
```

通过Bankr的`POST /agent/submit`直接提交此交易——**无需ABI编码**：

```bash
curl -s -X POST https://api.bankr.bot/agent/submit \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $BANKR_API_KEY" \
  -d '{
    "transaction": {
      "to": "TRANSACTION_TO_FROM_RESPONSE",
      "chainId": TRANSACTION_CHAINID_FROM_RESPONSE,
      "value": "0",
      "data": "TRANSACTION_DATA_FROM_RESPONSE"
    },
    "description": "Post BOTCOIN mining receipt",
    "waitForConfirmation": true
  }'
```

只需将协调器`transaction`响应中的`to`、`chainId`和`data`字段直接复制到Bankr的提交请求中。

**响应是同步的**——使用`waitForConfirmation: true`，Bankr会在交易被挖出后直接返回`{"success, transactionHash, status, blockNumber, gasUsed}`。提交和领取奖励都使用`POST /agent/submit`，并设置`waitForConfirmation: true`。

**重要提示：**对于所有与挖矿合约相关的操作，都使用`POST /agent/submit`（原始交易数据）。**不要使用自然语言提示来提交收据、领取奖励或进行任何合约调用**。

#### 步骤E：重复

返回步骤A，请求下一个挑战（使用新的nonce）。每次解决会根据当前的质押余额获得1、2或3个信用点。

**失败时：**请求一个新的挑战，使用新的nonce——不要重复尝试同一个挑战。

**何时停止：**如果LLM在多次尝试后仍然无法解决问题（例如尝试了5个不同的挑战），请通知用户。他们可能需要调整模型或思考策略——请参阅步骤B中的配置说明。

### 5. 领取奖励

**领取奖励的时间：**每个时期持续24小时（主网）或30分钟（测试网）。您只能领取已经**结束**并且**由运营商资助**的时期的奖励。跟踪您获得了奖励的时期（挑战响应中包含`epochId`）。

**信用点检查（按矿工和时期划分）：**

```bash
curl -s "${COORDINATOR_URL:-https://coordinator.agentmoney.net}/v1/credits?miner=0xYOUR_WALLET"
```

返回按时期分组的已赚取的信用点数。**速率限制：**此端点会针对每个矿工地址进行限制——请不要频繁轮询。

**如何检查时期状态：**定期轮询协调器以获取当前时期和下一个时期的开始时间：

```bash
curl -s "${COORDINATOR_URL:-https://coordinator.agentmoney.net}/v1/epoch"
```

响应内容包括：
- `epochId` — 当前时期（您在此时期获得的奖励）
- `prevEpochId` — 刚结束的时期（如果已资助，则可以领取奖励）
- `nextEpochStartTimestamp` — 下一个时期的开始时间
- `epochDurationSeconds` — 时期长度（86400 = 24小时主网，1800 = 30分钟测试网）

**可以领取奖励的时期**是指：
1. `epochId < currentEpoch`（时期已经结束）
2. 运营商已经调用`fundEpoch`（奖励已存入）
3. 您在该时期获得了奖励（您提交了收据）
4. 您尚未领取奖励

**如何领取奖励：**

1. 获取您想要领取的时期的预编码领取数据：

```bash
# Single epoch
curl -s "${COORDINATOR_URL:-https://coordinator.agentmoney.net}/v1/claim-calldata?epochs=22"

# Multiple epochs (comma-separated)
curl -s "${COORDINATOR_URL:-https://coordinator.agentmoney.net}/v1/claim-calldata?epochs=20,21,22"
```

2. 通过Bankr提交返回的`transaction`（与提交收据的方式相同——同步操作，无需轮询）：

```bash
curl -s -X POST https://api.bankr.bot/agent/submit \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $BANKR_API_KEY" \
  -d '{
    "transaction": {
      "to": "TRANSACTION_TO_FROM_RESPONSE",
      "chainId": TRANSACTION_CHAINID_FROM_RESPONSE,
      "value": "0",
      "data": "TRANSACTION_DATA_FROM_RESPONSE"
    },
    "description": "Claim BOTCOIN mining rewards",
    "waitForConfirmation": true
  }'
```

成功时：响应格式为`{"success": true, "transactionHash": "0x...", "status": "success", "blockNumber": "...", "gasUsed": "..." }`。

**旧版领取方式（第6时期）：**对于第6时期，使用旧版领取助手：调用`GET /v1/claim-calldata-v1?epochs=6`，然后通过Base链调用返回的交易数据来领取第6时期的奖励。

**奖励时期：**在领取奖励之前，请检查一个时期是否为奖励时期：

1. **奖励状态** — `GET /v1/bonus/status?epochs=42`（或`epochs=41,42,43`用于多个时期）。目的：检查是否有奖励时期（只读）。

   响应格式（200）：`{"enabled": true, "epochId": "42", "isBonusEpoch": true, "claimsOpen": true, "reward": "1000.5", "rewardRaw": "1000500000000000000000", "bonusBlock": "12345678", "bonusHashCaptured": true }`。字段说明：`enabled`（是否启用奖励），`isBonusEpoch`，`claimsOpen`，`reward`（BOTCOIN金额），`rewardRaw`（wei）。如果未启用奖励时期：`{"enabled": false}`。

2. **奖励领取数据** — `GET /v1/bonus/claim-calldata?epochs=42`。目的：获取领取奖励的预编码数据和交易信息。

   响应格式（200）：`{"calldata": "0x...", "transaction": { "to": "0x...", "chainId": 8453, "value": "0", "data": "0x..." }`。通过Bankr API或钱包提交`transaction`对象。

**流程：**首先调用`/v1/bonus/status?epochs=42`来检查第42时期是否为奖励时期以及是否可以领取奖励。如果`isBonusEpoch && claimsOpen`，则调用`/v1/bonus/claim-calldata?epochs=42`来获取交易数据，然后通过Bankr提交（与常规领取方式相同）。如果不是奖励时期，请使用常规的`GET /v1/claim-calldata`流程。

**轮询策略：**当用户请求领取奖励或检查奖励时，首先调用`GET /v1/epoch`。如果`prevEpochId`存在且您在该时期进行了挖掘，可以尝试领取奖励。您可以每隔几小时或在时期结束时轮询一次，以获取新资助的时期。如果领取失败，可能是因为该时期尚未资助，请稍后再试。

## Bankr交互规则

**自然语言**（通过`POST /agent/prompt`）——仅用于：
- 购买BOTCOIN：`"swap $10 of ETH to 0xA601877977340862Ca67f816eb079958E5bd0BA3 on base"`（或交换足够的ETH以达到至少25M BOTCOIN；如有需要，通过`GET /v1/token`进行验证）
- 检查余额：`"what are my balances on base?"`
- 为手续费桥接ETH：`"bridge $X of ETH to base"`

**原始交易数据**（通过`POST /agent/submit`）——用于所有合约调用：
- `submitReceipt(...)` — 提交挖掘收据（数据来自协调器的 `/v1/submit`）
- `claimEpochIds()` — 领取奖励（数据来自协调器的 `/v1/claim-calldata`）
- `stake` / `unstake` / `withdraw` — 质押（数据来自协调器的 `/v1/stake-approve-calldata`、`/v1/stake-calldata`、`/v1/unstake-calldata`、`/v1/withdraw-calldata`；通过Bankr提交）

切勿使用自然语言进行合约交互。协调器会提供准确的交易数据。

## 错误处理

### 速率限制和重试（协调器）

对所有协调器调用使用一个重试辅助函数。

**退避策略：**在遇到429、5xx或网络超时错误时进行重试。退避时间分别为2秒、4秒、8秒、16秒、30秒、60秒（最多60次尝试）。如果响应中包含`retryAfterSeconds`，则使用`max(retryAfterSeconds, backoffStep)`加上随机延迟。在尝试次数达到上限后停止，并显示明确的错误信息。

**令牌相关问题：**请参阅上面的承载令牌重用说明——为每个钱包缓存令牌信息，仅在遇到401错误或令牌即将过期时重新进行身份验证。

**每个端点的具体规则：**
- **`POST /v1/auth/nonce`** — 429/5xx错误：重试。其他4xx错误：失败。
- **`POST /v1/auth/verify`** — 429错误：重试，并在每次身份验证会话中最多尝试3次；如果仍然失败，等待60–120秒后再尝试新的nonce。401错误：获取新的nonce，重新签名后重试。403错误：余额不足。
- **`GET /v1/challenge`** — 429/5xx错误：重试。401错误：重新身份验证后重试。403错误：余额不足。
- **`POST /v1/submit`** — 429/5xx错误：重试。401错误：重新身份验证后重试相同的挑战。404错误：挑战无效；放弃当前挑战，获取新的挑战。200错误：解决器未能满足条件。
- **`GET /v1/claim-calldata`** — 429/5xx错误：重试。400错误：输入的时期格式不正确。
- **`GET /v1/stake-approve-calldata`** — 429/5xx错误：重试。400错误：`amount`单位应为基础单位（wei）。
- **`GET /v1/stake-calldata`** — 429/5xx错误：重试。400错误：`amount`单位应为基础单位（wei）。
- **`GET /v1/unstake-calldata`** — 429/5xx错误：重试。
- **`GET /v1/withdraw-calldata`** — 429/5xx错误：重试。

**并发限制：**每个钱包同时只能进行一次身份验证、一次挑战操作和一次提交操作。避免频繁的循环或并行重试。

**403余额不足：**请通过Bankr帮助用户购买BOTCOIN，然后达到最低质押要求。**交易失败（在区块链上）：**检查`epochId`和解决状态；协调器会处理错误情况。

### 领取奖励时的错误
- **EpochNotFunded**：运营商尚未为该时期发放奖励。请轮询`GET /v1/epoch`，稍后再试。
- **NoCredits**：您在该时期没有获得奖励（可能是因为您没有挖掘，或者在另一个时期进行了挖掘）。
- **AlreadyClaimed**：您已经领取了该时期的奖励。请跳过该时期。

### 质押错误（交易失败）
- **InsufficientBalance** / **NotEligible**：需要质押更多BOTCOIN以达到最低要求（25M）。
- **NothingStaked**：没有足够的BOTCOIN进行解质押或取款。请先进行质押。
- **UnstakePending**：在解质押期间无法进行解质押或取款。请取消解质押操作或等待冷却时间后再尝试。
- **NoUnstakePending**：无法取款或取消操作——因为没有进行解质押。请先进行解质押。
- **CooldownNotElapsed**：只有在冷却时间（主网为24小时）过后才能取款。

### 解决挑战失败
- **Failed constraints after submit**：请求一个使用不同nonce的新挑战。不要重复尝试同一个挑战。
- **Nonce mismatch on submit**：如果收到“ChallengeId mismatch”错误，请确保您发送的nonce与请求挑战时使用的nonce相同。
- **Consistent failures across many challenges**：如果LLM在多次尝试后仍然无法解决问题，请停止并告知用户。建议调整模型或思考策略——请参阅步骤B中的配置说明。

### LLM提供商错误（立即停止，不要重试）
- **401 / 403来自LLM API**：身份验证或权限问题。停止操作并告知用户检查他们的API密钥。
- **API预算/计费错误**（例如“使用限制”、“计费问题”）：停止操作并告知用户他们的LLM API信用点已用完。

### LLM提供商错误（带有退避的重试）
- **429来自LLM API**：达到速率限制。等待30-60秒后重试。
- **529 / 5xx来自LLM API**：提供商过载。等待30秒后重试（最多尝试2次）。
- **Timeout (no response after 5 minutes)**：LLM调用失败。停止操作并重试。如果连续两次失败，请停止并告知用户。

### Bankr错误
- **401来自Bankr**：API密钥无效。停止操作并告知用户检查`BANKR_API_KEY`。
- **403来自Bankr**：密钥没有写入/代理权限。停止操作并告知用户在bankr.bot/api中启用相应权限。
- **429来自Bankr**：达到速率限制。等待60秒后重试。
- **Transaction failed**：记录错误并重试一次。如果再次失败，请停止操作并告知用户。