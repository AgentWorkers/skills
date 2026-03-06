---
name: Vincent - Brave Search for agents
description: 该技能基于Brave Search技术，提供网页搜索和新闻搜索服务。当用户需要浏览网页、查找新闻文章或查询当前信息时，可以使用此技能。搜索服务采用按次计费的方式，费用通过Vincent信用系统收取。触发该技能的指令包括：“search the web”、“web search”、“brave search”、“search news”、“find information”以及“look up”、“current events”。
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
# Vincent – 使用 Brave Search 进行代理搜索

使用此技能，您可以通过 Brave Search 在网页和新闻中搜索信息。所有请求都会通过 Vincent 后端进行代理处理，该后端负责与 Brave Search API 进行身份验证、执行速率限制、记录每次请求的费用，并自动从您的信用余额中扣除费用。

**无需管理 API 密钥。** 代理使用由 Vincent API 密钥进行身份验证，该密钥的权限范围限定为 `DATA_SOURCES` 秘密信息。Vincent 在服务器端处理与 Brave Search API 相关的认证信息——代理从未看到或管理过 Brave API 密钥。

所有命令都依赖于 `@vincentai/cli` 包。API 密钥的存储和解析都是自动完成的——您无需直接处理原始密钥或文件路径。

## 安全模型

此技能专为**具有按次计费功能且受人工监督的自主代理操作**而设计。

**无需环境变量**，因为该技能采用“代理优先”的接入方式：代理在运行时通过调用 Vincent API 生成一个 `DATA_SOURCES` 秘密信息，该 API 会返回一个权限范围有限的 API 密钥。CLI 会在创建过程中自动存储返回的 API 密钥。密钥的存储路径（`${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/credentials/datasources/` 或 `./datasources/`）在技能的元数据中进行了声明。

**代理的 API 密钥并非 Brave Search 的 API 密钥**。它是一个用于 Vincent 代理的权限范围有限的令牌。Vincent 服务器会代表代理与 Brave Search 进行身份验证。代理无法直接访问上游 API，也无法绕过代理的信用限制和速率限制。

**有意启用模型调用**。该技能的目的是让 AI 代理具备自主的网页搜索能力。代理应自行在网页和新闻中搜索信息。用户可以通过 `https://heyvincent.ai` 管理信用余额和支付方式来控制支出。

**所有 API 请求都通过 HTTPS/TLS 协议发送到 `heyvincent.ai`**。Vincent 服务器随后会调用 Brave Search API。代理不会直接与 Brave 进行通信。

**密钥生命周期：**
- **创建**：代理运行 `secret create` 命令并指定 `--type DATA_SOURCES` 参数——CLI 会自动存储 API 密钥，并返回一个 `keyId` 和 `claimUrl`。
- **声明所有权**：操作员使用 `claimUrl` 在 `https://heyvincent.ai` 网站上声明所有权、添加信用并管理支付。
- **信用消耗**：每次 API 请求都会消耗少量信用（详见下方定价信息）。用户需要通过前端添加信用。如果信用余额耗尽且未设置支付方式，请求将被拒绝。
- **撤销**：密钥的所有者可以随时通过 Vincent 前端撤销代理的 API 密钥。

## 定价

| API 端点 | 每次请求费用 |
| --- | --- |
| 网页搜索 | 0.005 美元 |
| 新闻搜索 | 0.005 美元 |

每次请求都会自动扣除信用余额。响应中会包含 `_vincent.creditRemainingUsd` 字段，以便代理可以查看剩余余额。

## 快速入门

### 1. 检查是否存在现有密钥

在创建新密钥之前，请先检查是否已经存在密钥：

```bash
npx @vincentai/cli@latest secret list --type DATA_SOURCES
```

如果返回了密钥，请将其 `id` 作为后续命令的 `--key-id` 参数。如果不存在密钥，请创建一个新的密钥。

### 2. 创建数据源密钥

```bash
npx @vincentai/cli@latest secret create --type DATA_SOURCES --memo "My agent data sources"
```

创建完成后，将返回 `keyId`（用于后续所有命令）和 `claimUrl`（与用户共享）。

创建完成后，告知用户：
> “这是您的数据源声明 URL：`<claimUrl>`。请使用此 URL 在 `https://heyvincent.ai` 网站上声明所有权并添加用于 Brave Search 和其他数据源的信用。”

**重要提示：** 在进行 API 请求之前，必须先声明所有权并确保有足够的信用或已设置支付方式。

### 3. 网页搜索

```bash
npx @vincentai/cli@latest brave web --key-id <KEY_ID> --q "latest AI news" --count 10
```

参数：
- `--q`（必填）：搜索查询（1-400 个字符）
- `--count`（可选）：结果数量（1-20，默认值：10）
- `--offset`（可选）：分页偏移量（0-9）
- `--freshness`（可选）：时间筛选条件（`pd`：过去一天，`pw`：过去一周，`pm`：过去一个月，`py`：过去一年）
- `--country`（可选）：用于显示本地化结果的 2 位国家代码（例如 `us`、`gb`、`de`）

返回包含标题、URL、描述和元数据的网页搜索结果。

### 4. 新闻搜索

```bash
npx @vincentai/cli@latest brave news --key-id <KEY_ID> --q bitcoin --count 10
```

参数：
- `--q`（必填）：搜索查询（1-400 个字符）
- `--count`（可选）：结果数量（1-20，默认值：10）
- `--freshness`（可选）：时间筛选条件（`pd`：过去一天，`pw`：过去一周，`pm`：过去一个月，`py`：过去一年）

返回包含标题、URL、描述和发布日期的新闻文章。

## 响应元数据

每个成功的响应都会包含一个 `_vincent` 对象，其中包含以下信息：

```json
{
  "_vincent": {
    "costUsd": 0.005,
    "creditRemainingUsd": 4.99
  }
}
```

使用 `creditRemainingUsd` 字段来提醒用户信用余额不足。

## 输出格式

网页搜索结果的结构如下：

```json
{
  "web": {
    "results": [
      {
        "title": "Article Title",
        "url": "https://example.com/article",
        "description": "A brief description of the article content."
      }
    ]
  },
  "_vincent": {
    "costUsd": 0.005,
    "creditRemainingUsd": 4.99
  }
}
```

新闻搜索结果的结构相同，但每条结果还会包含 `age` 和 `source` 字段。

## 错误处理

| 错误代码 | 原因 | 解决方案 |
| ------- | ------- | ------------|
| `401 Unauthorized` | API 密钥无效或缺失 | 确保 `key-id` 正确；如有需要，请重新链接 |
| `402 Insufficient Credit` | 信用余额为零且未设置支付方式 | 用户需要在 `heyvincent.ai` 网站上添加信用 |
| `429 Rate Limited` | 每分钟请求次数超过限制（60 次） | 等待片刻后重试 |
| `Key not found` | API 密钥已被撤销或从未创建 | 请向密钥所有者请求新的令牌 |

## 速率限制

- 每个 API 密钥每分钟最多允许 60 次请求（Twitter 和 Brave Search 合计）
- 如果超出限制，系统会返回 `429` 错误代码。请等待片刻后重试。

## 重新链接（恢复 API 访问权限）

如果代理丢失了 API 密钥，密钥所有者可以通过前端生成一个新的**重新链接令牌**。代理可以使用此令牌获取新的 API 密钥。

```bash
npx @vincentai/cli@latest secret relink --token <TOKEN_FROM_USER>
```

CLI 会使用该令牌获取新的 API 密钥，并自动将其存储，同时返回新的 `keyId`。重新链接令牌仅限一次性使用，有效期为 10 分钟。

## 添加信用

当信用余额不足时，您可以使用 x402 支付协议通过 Base 平台自主购买更多信用（支持 USDC）——无需人工干预。

**可选信用额度：** $1、$5、$10、$25、$50、$100

### 检查余额

```bash
npx @vincentai/cli@latest credits balance --key-id <KEY_ID>
```

### 通过 x402（Base 平台上的 USDC）购买信用

```bash
npx @vincentai/cli@latest credits add --key-id <KEY_ID> --amount 10
```

**操作步骤：**
1. CLI 向 x402 信用端点发送 POST 请求。
2. 服务器返回包含 Base 平台上动态 USDC 存款地址的 HTTP 402 响应。
3. CLI 使用代理的钱包完成支付。
4. CLI 重新发送请求并附上支付凭证。
5. 服务器验证支付后，将信用添加到您的账户中。

**所需条件：**
- 支持 x402 协议的钱包，并且钱包中需要有 USDC（链 ID 为 8453）。
- 拥有 Vincent 的 `DATA_SOURCES` API 密钥。

### 通过信用卡购买信用（人工操作）

```bash
npx @vincentai/cli@latest credits checkout --key-id <KEY_ID>
```

系统会返回一个 Stripe 结账 URL。请将此 URL 分发给用户，以便他们使用信用卡完成支付。

### MCP 工具

| 工具 | 功能描述 |
| --- | --- |
| `vincent_credit_balance` | 查看当前信用余额和充值选项 |
| `vincent_add_credits` | 获取购买信用的 x402 支付说明 |

### 自动补充信用

对于长时间运行的代理，在执行高成本操作前请检查余额，余额不足时及时补充：

```bash
BALANCE=$(npx @vincentai/cli@latest credits balance --key-id <KEY_ID> --json | jq -r '.balance')
if (( $(echo "$BALANCE < 2.00" | bc -l) )); then
  npx @vincentai/cli@latest credits add --key-id <KEY_ID> --amount 10
fi
```

## 重要说明：
- 单个 `DATA_SOURCES` API 密钥适用于**所有** 数据源（Twitter、Brave Search 等）。您无需为每个数据源分别创建密钥。
- 创建密钥后，请务必将声明 URL 分发给用户。
- 如果请求因信用问题被拒绝，请告知用户在 `https://heyvincent.ai` 网站上添加信用。