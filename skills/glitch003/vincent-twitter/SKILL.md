---
name: Vincent - Twitter / X.com for agents
description: >
  **用于代理程序的 Twitter/X.com 数据访问功能**  
  当用户需要搜索推文、查看用户资料或获取最新推文时，可以使用此功能。该服务采用按次计费的方式，通过 Vincent 信用系统进行结算。  
  触发条件包括：  
  - “search tweets”（搜索推文）  
  - “twitter”  
  - “X.com”  
  - “look up user”（查看用户资料）  
  - “tweet search”（推文搜索）  
  - “twitter profile”（查看用户资料）  
  - “recent tweets”（最新推文）
allowed-tools: Read, Write, Bash(npx:@vincentai/cli*), Bash(jq:*), Bash(bc:*)
version: 1.0.0
author: HeyVincent <contact@heyvincent.ai>
license: MIT
homepage: https://heyvincent.ai
source: https://github.com/HeyVincent-ai/Vincent
metadata:
  clawdbot:
    homepage: https://heyvincent.ai
    requires:
      config:
        - ${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/credentials/datasources
        - ./datasources
---
# Vincent – 用于代理的 Twitter/X.com 工具

使用此工具可以搜索推文、查询用户资料以及从 X.com（Twitter）获取最新推文。所有请求均通过 Vincent 后端进行代理处理，该后端负责与 Twitter API 的身份验证、执行请求速率限制、记录每次请求的费用，并自动从您的信用余额中扣除费用。

**无需管理 API 密钥。** 代理使用一个属于 `DATA_SOURCES` 秘密的 Vincent API 密钥进行身份验证。Vincent 在服务器端处理与 Twitter API 相关的认证信息——代理永远不会看到或管理 Twitter API 密钥。

所有命令均使用 `@vincentai/cli` 包。API 密钥的存储和解析过程是自动完成的——您无需直接处理原始密钥或文件路径。

## 安全模型

此工具专为**具有按次计费功能且需人工监督的自主代理操作**而设计。

**无需环境变量**，因为该工具采用“代理优先”的接入方式：代理在运行时通过调用 Vincent API 生成一个 `DATA_SOURCES` 秘密，从而获得一个受限范围的 API 密钥。CLI 会在创建过程中自动存储该 API 密钥。密钥的存储路径（`${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/credentials/datasources/` 或 `./datasources/`）在工具的元数据中进行了指定。

**代理的 API 密钥并非 Twitter 的 API 密钥**，而是用于访问 Vincent 代理的受限范围令牌。Vincent 服务器会代表代理与 Twitter 进行身份验证。代理无法直接访问上游 API，也无法绕过代理的信用限制和速率限制。

**故意启用了模型调用功能**。该工具的目的是让 AI 代理能够自主访问 Twitter 数据。代理应自行执行推文搜索和用户资料查询操作。人工可以通过 `https://heyvincent.ai` 管理代理的信用余额和支付方式。

**所有 API 请求均通过 HTTPS/TLS 协议发送至 `heyvincent.ai`。** Vincent 服务器随后会调用 Twitter API。代理不会直接与 Twitter 进行通信。

**密钥生命周期：**
- **创建**：代理运行 `secret create` 命令并指定 `--type DATA_SOURCES` 参数——CLI 会自动存储 API 密钥，并返回 `keyId` 和 `claimUrl`。
- **认领**：人工操作员使用 `claimUrl` 在 `https://heyvincent.ai` 进行认领操作，以获取使用权限并充值信用。
- **信用消耗**：每次 API 请求都会产生少量费用（详见下文定价信息）。人工需要通过前端为代理充值信用。当信用余额耗尽且未设置支付方式时，请求将被拒绝。
- **撤销**：密钥的所有者可以随时通过 Vincent 前端撤销代理的 API 密钥。

## 定价

| API 端点 | 每次请求费用 |
| --- | --- |
| 搜索推文 | 0.01 美元 |
| 根据 ID 获取推文 | 0.005 美元 |
| 获取用户资料 | 0.005 美元 |
| 获取用户的推文 | 0.01 美元 |

每次请求的费用会自动从您的信用余额中扣除。响应中会包含 `_vincent.creditRemainingUsd`，以便代理可以随时查看剩余余额。

## 快速入门

### 1. 检查是否存在现有密钥

在创建新密钥之前，请先检查是否已有密钥存在：

```bash
npx @vincentai/cli@latest secret list --type DATA_SOURCES
```

如果找到密钥，请将其 `id` 作为后续命令的 `--key-id` 参数使用。如果没有密钥，则需要创建一个新的密钥。

### 2. 创建数据源密钥

```bash
npx @vincentai/cli@latest secret create --type DATA_SOURCES --memo "My agent data sources"
```

创建完成后，将 `keyId`（用于后续命令）和 `claimUrl`（需告知用户）返回给用户。

创建完成后，告知用户：
> “这是您的数据源认领 URL：`<claimUrl>`。请使用此 URL 在 `https://heyvincent.ai` 进行认领操作并充值信用。”

**重要提示：** 在进行 API 请求之前，必须先认领密钥并确保有足够的信用或已设置支付方式。

### 3. 搜索推文

```bash
npx @vincentai/cli@latest twitter search --key-id <KEY_ID> --q bitcoin --max-results 10
```

参数：
- `--q`（必填）：搜索查询内容（1-512 个字符）
- `--max-results`（可选）：返回结果数量（10-100 条，默认为 10 条）
- `--start-time`（可选）：ISO 8601 格式的日期时间，指定返回最早的时间范围的推文
- `--end-time`（可选）：ISO 8601 格式的日期时间，指定返回最新时间范围的推文

返回推文内容、创建时间、作者 ID 以及公开数据（点赞数、转发数、回复数）。

### 4. 获取特定推文

```bash
npx @vincentai/cli@latest twitter tweet --key-id <KEY_ID> --tweet-id <TWEET_ID>
```

### 5. 获取用户资料

根据用户名查询 Twitter 用户的资料。

```bash
npx @vincentai/cli@latest twitter user --key-id <KEY_ID> --username elonmusk
```

返回用户的描述、关注者/被关注者数量、个人资料图片以及账号的认证状态。

### 6. 获取用户的最新推文

```bash
npx @vincentai/cli@latest twitter user-tweets --key-id <KEY_ID> --user-id <USER_ID> --max-results 10
```

**注意：** 此命令需要使用用户的数字 ID（来自用户资料响应），而非用户名。

## 响应元数据

每个成功的响应都会包含一个 `_vincent` 对象，其中包含以下信息：

```json
{
  "_vincent": {
    "costUsd": 0.01,
    "creditRemainingUsd": 4.99
  }
}
```

通过 `_vincent.creditRemainingUsd` 变量，可以提醒用户信用余额即将耗尽。

## 输出格式

推文搜索结果：

```json
{
  "data": [
    {
      "id": "123456789",
      "text": "Tweet content here",
      "created_at": "2026-02-26T12:00:00.000Z",
      "author_id": "987654321",
      "public_metrics": {
        "like_count": 42,
        "retweet_count": 10,
        "reply_count": 5
      }
    }
  ],
  "_vincent": {
    "costUsd": 0.01,
    "creditRemainingUsd": 4.99
  }
}
```

用户资料响应包括 `description`（描述）、`public_metrics`（关注者/被关注者数量）、`profile_image_url`（个人资料图片链接）以及 `verified`（账号认证状态）。

## 错误处理

| 错误代码 | 原因 | 解决方案 |
| ------- | ------- | ------------ |
| `401 Unauthorized` | API 密钥无效或缺失 | 确认 `key-id` 是否正确；如有必要，请重新链接 |
| `402 Insufficient Credit` | 信用余额为零且未设置支付方式 | 用户需在 `heyvincent.ai` 充值 |
| `429 Rate Limited` | 每分钟请求次数超过限制（60 次） | 等待片刻后重试 |
| `Key not found` | API 密钥已被撤销或从未创建 | 请向密钥所有者申请新的令牌 |
| `User not found` | 用户在 Twitter 上不存在 | 请检查用户名的拼写是否正确 |

## 速率限制

- 每个 API 密钥每分钟最多可发起 60 次请求（涵盖所有数据源端点，包括 Twitter 和 Brave Search）。
- 如果超出速率限制，系统会返回 `429` 错误代码。请等待片刻后重试。

## 重新链接（恢复 API 访问权限）

如果代理丢失了 API 密钥，密钥所有者可以通过前端生成一个新的 **令牌**。代理可以使用该令牌获取新的 API 密钥。

```bash
npx @vincentai/cli@latest secret relink --token <TOKEN_FROM_USER>
```

CLI 会使用新令牌获取新的 API 密钥，自动存储该密钥，并返回新的 `keyId`。重新链接的令牌仅限一次性使用，有效期为 10 分钟。

## 充值

当信用余额不足时，您可以通过 x402 支付协议使用 USDC 自动充值。可选充值金额：1 美元、5 美元、10 美元、25 美元、50 美元、100 美元。

### 检查余额

```bash
npx @vincentai/cli@latest credits balance --key-id <KEY_ID>
```

### 通过 x402（Base 上的 USDC）充值

```bash
npx @vincentai/cli@latest credits add --key-id <KEY_ID> --amount 10
```

**操作步骤：**
1. CLI 向 x402 充值端点发送 POST 请求。
2. 服务器返回包含 Base 上 USDC 存款地址的 HTTP 402 响应。
3. CLI 使用代理的钱包完成支付。
4. CLI 重新发送请求并附上支付凭证。
5. 服务器验证支付信息后，将信用添加到您的账户中。

**所需条件：**
- 支持 x402 协议的钱包，且钱包中需有 USDC（链 ID 为 8453）。
- 拥有 Vincent 的 `DATA_SOURCES` API 密钥。

### 通过信用卡充值（人工操作）

```bash
npx @vincentai/cli@latest credits checkout --key-id <KEY_ID>
```

系统会返回一个 Stripe 结账 URL，用户可以使用该 URL 通过信用卡完成支付。

### MCP 工具

| 工具 | 功能描述 |
| --- | --- |
| `vincent_credit_balance` | 查看当前信用余额及充值选项 |
| `vincent_add_credits` | 获取 x402 充值指令 |

### 自动充值机制

对于长时间运行的代理，建议在执行高成本操作前检查余额，并在余额不足时及时充值：

```bash
BALANCE=$(npx @vincentai/cli@latest credits balance --key-id <KEY_ID> --json | jq -r '.balance')
if (( $(echo "$BALANCE < 2.00" | bc -l) )); then
  npx @vincentai/cli@latest credits add --key-id <KEY_ID> --amount 10
fi
```

## 重要提示：
- 单个 `DATA_SOURCES` API 密钥适用于所有数据源（Twitter、Brave Search 等）。无需为每个数据源分别创建密钥。
- 创建密钥后，请务必将认领 URL 告知用户。
- 如果请求因信用不足被拒绝，请告知用户在 `https://heyvincent.ai` 充值。
- Twitter 搜索端点仅返回最近 7 天内的推文（这是 X API v2 的限制规定）。