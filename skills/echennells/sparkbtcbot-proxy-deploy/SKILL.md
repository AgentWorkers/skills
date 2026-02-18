---
name: sparkbtcbot-proxy-deploy
description: 在 Vercel 上部署一个无服务器的 Spark Bitcoin L2 代理，该代理支持消费限额、身份验证功能以及 Redis 日志记录。此文档适用于用户需要设置新的代理、配置环境变量、将代理部署到 Vercel 服务器或管理代理基础设施的场景。
argument-hint: "[Optional: setup, deploy, rotate-token, or configure]"
---
# 部署 sparkbtcbot-proxy

您是部署和管理 sparkbtcbot-proxy 的专家——这是一个无服务器中间件，它将 Spark Bitcoin L2 SDK 包装在 Vercel 上的认证 REST 端点后面。

## 该代理的功能

- 允许 AI 代理访问钱包，同时不暴露助记词：
  - 基于角色的令牌认证（`admin` 有完全访问权限，`invoice` 仅具有读取和创建发票的权限）
  - 通过 API 管理令牌——无需重新部署即可创建、列出和撤销令牌
  - 设置每笔交易的限额和每日支出限额
  - 将活动日志记录到 Redis
  - 拖延检测已支付的 Lightning 发票

## 您需要准备的内容

**请提前向用户索取以下信息：**

- Vercel 账户（免费 hobby 级别即可）
- Upstash 账户的电子邮件和 API 密钥（来自 https://console.upstash.com/account/api）——或者如果他们已经拥有数据库，则提供现有的 `UPSTASH_REDIS_REST_URL` 和 `UPSTASH_REDIS_REST_TOKEN`
- Spark 钱包的 BIP39 助记词（或在第 3 步中生成）
- Node.js 20+ 版本

**在设置过程中自动生成的内容（无需询问）：**

- `UPSTASH_REDIS_REST_URL` 和 `UPSTASH_REDIS_REST_TOKEN`——在第 2 步中通过 Upstash 管理 API 生成
- `API_AUTH_TOKEN`——在第 4 步中生成

## 分步部署

### 1. 克隆并安装

```bash
git clone https://github.com/echennells/sparkbtcbot-proxy.git
cd sparkbtcbot-proxy
npm install
```

### 2. 创建 Upstash Redis 数据库

如果用户已经拥有 `UPSTASH_REDIS_REST_URL` 和 `UPSTASH_REDIS_REST_TOKEN`，请跳到第 3 步。

否则，通过 Upstash API 创建一个数据库。用户需要提供他们的 Upstash 电子邮件和 API 密钥（来自 https://console.upstash.com/account/api）：

```bash
curl -X POST "https://api.upstash.com/v2/redis/database" \
  -u "UPSTASH_EMAIL:UPSTASH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "sparkbtcbot-proxy", "region": "global", "primary_region": "us-east-1"}'
```

**注意：** 区域化数据库创建已过时。必须使用 `"region": "global"` 并设置 `"primary_region"` 字段。Upstash 文档可能尚未更新这一信息。

响应中会包含 `rest_url` 和 `rest_token`——请将这些信息保存下来，以备第 5 步使用。

### 3. 生成钱包助记词（如需要）

当不提供助记词时，调用 `SparkWallet.initialize()` 会返回 `{ mnemonic, wallet }`。以下是简化的命令：

```bash
node -e "import('@buildonspark/spark-sdk').then(({SparkWallet}) => SparkWallet.initialize({mnemonicOrSeed: null, options: {network: 'MAINNET'}}).then(r => { console.log(r.mnemonic); r.wallet.cleanupConnections() }))"
```

请安全地保存这 12 个单词的助记词——它控制着钱包中的所有资金。没有 `getMnemonic()` 方法；您只能在初始化时获取助记词。

或者使用任何 BIP39 助记词生成器来生成 12 个或 24 个单词的助记词。

### 4. 生成 API 认证令牌

```bash
openssl rand -base64 30
```

### 5. 部署到 Vercel

```bash
npx vercel --prod
```

按照提示接受默认设置。然后设置环境变量。所有 7 个变量都是必需的：

| 变量 | 描述 | 示例 |
|----------|-------------|---------|
| `SPARK_MNEMONIC` | 12 个单词的 BIP39 助记词 | `fence connect trigger ...` |
| `SPARK_NETWORK` | Spark 网络 | `MAINNET` |
| `API_AUTH_TOKEN` | 管理员备用令牌 | 第 4 步的输出 |
| `UPSTASH_REDIS_REST_URL` | Redis REST 端点 | `https://xxx.upstash.io` |
| `UPSTASH_REDIS_REST_TOKEN` | Redis 认证令牌 | 来自第 2 步 |
| `MAX_TRANSACTION_SATS` | 每笔交易的支出限额 | `10000` |
| `DAILY_BUDGET_SATS` | 每日支出限额（在 UTC 午夜重置） | `100000` |

**重要提示：** 不要使用 `vercel env add` 和 heredoc/`<<<` 输入方式来设置环境变量——因为这会导致添加换行符，从而破坏 Spark SDK 的正常运行。请使用 Vercel 控制面板或 REST API 来设置环境变量：

```bash
curl -X POST "https://api.vercel.com/v10/projects/<PROJECT_ID>/env?teamId=<TEAM_ID>" \
  -H "Authorization: Bearer <VERCEL_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"type":"encrypted","key":"SPARK_MNEMONIC","value":"your mnemonic here","target":["production","preview","development"]}'
```

设置完环境变量后，重新部署应用：

```bash
npx vercel --prod
```

### 6. 测试

```bash
curl -H "Authorization: Bearer <your-token>" https://<your-deployment>.vercel.app/api/balance
```

测试结果应返回 `{"success": true, "data": {"balance": "0", "tokenBalances": {}}`。

### 7. 创建受限令牌（可选）

使用管理员令牌为代理创建受限令牌：

```bash
curl -X POST -H "Authorization: Bearer <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{"role": "invoice", "label": "my-agent"}' \
  https://<your-deployment>.vercel.app/api/tokens
```

响应中会包含完整的令牌字符串——请保存它，因为这个信息只会显示一次。详情请参阅下面的 **令牌角色** 部分。

## API 路由

| 方法 | 路由 | 描述 |
|--------|-------|-------------|
| GET | `/llms.txt` | 机器人的 API 文档（无需认证） |
| GET | `/api/balance` | 钱包余额（sat 和令牌） |
| GET | `/api/info` | Spark 地址和身份公钥 |
| GET | `/api/transactions` | 转账历史记录 (`?limit=&offset=`) |
| GET | `/api/deposit-address` | Bitcoin L1 存款地址 |
| GET | `/api/fee-estimate` | Lightning 发票费用估算 (`?invoice=`) |
| GET | `/api/logs` | 最近的活动日志 (`?limit=`) |
| POST | `/api/invoice/create` | 创建 Lightning 发票 (`{amountSats, memo?, expirySeconds?}`) |
| POST | `/api/invoice/spark` | 创建 Spark 发票 (`{amount?, memo?}`) |
| POST | `/api/pay` | 支付 Lightning 发票——仅限管理员 (`{invoice, maxFeeSats}`) |
| POST | `/api/transfer` | Spark 转账——仅限管理员 (`{receiverSparkAddress, amountSats}`) |
| POST | `/api/l402` | 支付 L402 支付墙——仅限管理员 (`{url, method?, headers?, body?, maxFeeSats?}`) |
| GET | `/api/l402/status` | 检查/完成待处理的 L402 请求 (`?id=<pendingId>`) |
| GET | `/api/tokens` | 列出 API 令牌——仅限管理员 |
| POST | `/api/tokens` | 创建新令牌——仅限管理员 (`{role, label}` |
| DELETE | `/api/tokens` | 撤销令牌——仅限管理员 (`{token}` |

## 令牌角色

有两种令牌角色：

| 角色 | 权限 |
|------|------------|
| `admin` | 所有权限——读取、创建发票、支付、转账、管理令牌 |
| `invoice` | 读取（余额、信息、交易记录、费用估算、存款地址）+ 创建发票。无法支付或转账。 |

`API_AUTH_TOKEN` 环境变量是硬编码的管理员备用令牌——即使在 Redis 故障或令牌丢失的情况下也能正常使用。使用它来初始化代理，并通过 API 创建受限令牌，然后分发给代理。

### 管理令牌

为商家机器人创建仅用于创建发票的令牌：

```bash
curl -X POST -H "Authorization: Bearer <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{"role": "invoice", "label": "merchant-bot"}' \
  https://<deployment>/api/tokens
```

列出所有令牌（显示前缀、标签和角色——不包括完整的令牌字符串）：

```bash
curl -H "Authorization: Bearer <admin-token>" https://<deployment>/api/tokens
```

撤销令牌：

```bash
curl -X DELETE -H "Authorization: Bearer <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{"token": "<full-token-string>"}' \
  https://<deployment>/api/tokens
```

令牌存储在 Redis 中（哈希键为 `spark:tokens`）。它们在重新部署时不会丢失，但 Redis 数据被清除时令牌也会丢失。

## L402 支付墙支持

该代理可以自动支付 [L402](https://docs.lightning.engineering/the-lightning-network/l402) 支付墙。只需提供一个 URL，代理就会：

1. 获取该 URL
2. 如果返回 402 状态码，解析发票和 macaroon
3. 支付 Lightning 发票
4. 带有 L402 授权头重新发送请求
5. 返回受保护的内容

### 基本使用方法

```bash
curl -X POST -H "Authorization: Bearer <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://lightningfaucet.com/api/l402/joke"}' \
  https://<deployment>/api/l402
```

### 处理待处理的支付（对代理很重要）

通过 Spark 进行的 Lightning 支付是异步的。代理会尝试获取支付信息最多 7.5 秒，但如果预图像未能及时获取，它会返回 **pending** 状态：

```json
{
  "success": true,
  "data": {
    "status": "pending",
    "pendingId": "a1b2c3d4e5f6...",
    "message": "Payment sent but preimage not yet available. Poll GET /api/l402/status?id=<pendingId> to complete.",
    "priceSats": 21
  }
}
```

**您的代理必须处理这种情况。** 支付已经完成——如果您不检查完成情况，将会丢失已支付的资金。

**重试循环（伪代码）：**

```
response = POST /api/l402 { url: "..." }

if response.data.status == "pending":
    pendingId = response.data.pendingId
    for attempt in 1..10:
        sleep(3 seconds)
        status = GET /api/l402/status?id={pendingId}
        if status.data.status != "pending":
            return status.data  # Success or failure
    # Give up after ~30 seconds
    raise "L402 payment timed out"
else:
    return response.data  # Immediate success
```

**关键点：**
- **令牌缓存**：已支付的 L402 令牌按域名缓存（最长 24 小时）。对同一域名的后续请求会重用缓存的令牌而无需再次支付。如果令牌过期，代理会自动重新生成新的令牌。
- 待处理的记录在 1 小时后失效
- `/api/l402/status` 端点每次请求最多检查 5 秒
- 如果 Spark 侧支付失败，状态会返回错误信息
- 一旦支付完成，待处理的记录将从 Redis 中删除
- 如果响应为空，代理会自动重试最多 3 次（每次间隔 200 毫秒）——因为某些服务器在支付后不会立即返回内容

## 常见操作

### 更换管理员备用令牌

1. 生成新令牌：`openssl rand -base64 30`
2. 更新 Vercel 环境变量中的 `API_AUTH_TOKEN`
3. 重新部署应用：`npx vercel --prod`
4. 更新所有使用旧令牌的代理

存储在 Redis 中的令牌不受此操作影响——它们会继续正常工作。

### 调整支出限额

更新 Vercel 环境变量中的 `MAX_TRANSACTION_SATS` 和 `DAILY_BUDGET_SATS`，然后重新部署应用。预算在 UTC 午夜重置。

### 查看日志

```bash
curl -H "Authorization: Bearer <token>" https://<deployment>/api/logs?limit=20
```

## 架构

- **Vercel 无服务器函数**——每个请求都会启动一个新的函数实例，初始化 Spark SDK（约 1.5 秒），处理请求后关闭。没有持续运行的进程，空闲时不会产生费用。
- **Upstash Redis**——存储每日支出计数器、活动日志、待处理发票跟踪和 API 令牌。通过 HTTP REST 访问（无需持久连接）。免费级别限制使用一个数据库。
- **Spark SDK**——`@buildonspark/spark-sdk` 通过 HTTP/2 使用 gRPC 连接到 Spark 签名操作符。纯 JavaScript 实现，无需安装任何插件。
- **延迟检查发票**——每次请求时，中间件会检查 Redis 中的待处理发票，并与最近的转账记录进行比对。过期的发票会被清除，已支付的发票会被记录下来。每次请求最多检查 5 次，使用 try/catch 机制确保失败不会影响主请求的处理。