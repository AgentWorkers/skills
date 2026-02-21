---
name: Vincent - Twitter / X.com for agents
description: 使用此技能可以搜索推文、查看用户资料，并从 X.com（Twitter）获取最近的推文。费用按调用次数计费，通过 Vincent 信用系统进行结算。
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

使用此工具可以搜索推文、查询用户信息以及从 X.com（Twitter）获取最新推文。所有请求均通过 Vincent 后端进行代理处理，该后端负责与 Twitter API 的身份验证、执行速率限制、记录每次调用的费用，并自动从您的信用余额中扣除费用。

**无需管理 API 密钥。** 代理使用由 `DATA_SOURCES` 秘密配置的 Vincent API 密钥进行身份验证。Vincent 在服务器端处理与 Twitter API 相关的认证信息——代理从未看到或管理过 Twitter API 密钥。

所有命令均依赖于 `@vincentai/cli` 包。API 密钥的存储和解析过程是自动完成的——您无需手动处理原始密钥或文件路径。

## 安全模型

此工具专为**具有按次计费机制且受人类监督的自主代理操作**而设计。

**无需环境变量**，因为该工具采用“代理优先”的接入方式：代理在运行时通过调用 Vincent API 生成一个 `DATA_SOURCES` 秘密，从而获得一个限定范围的 API 密钥。CLI 会在创建代理时自动保存该 API 密钥。密钥的存储路径（`${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/credentials/datasources/` 或 `./datasources/`）在工具的元数据中进行了指定。

**代理的 API 密钥并非 Twitter 的 API 密钥**，而是用于访问 Vincent 代理的限定范围令牌。Vincent 服务器会代表代理与 Twitter 进行身份验证。代理无法直接访问上游 API，也无法绕过代理的信用限制和速率限制。

**故意启用了模型调用功能**。该工具的目的是让 AI 代理能够自主访问 Twitter 数据。代理应自行执行推文搜索和用户信息查询操作。人类用户可通过 `https://heyvincent.ai` 管理代理的信用余额和支付方式。

**所有 API 调用均通过 HTTPS/TLS 协议发送至 `heyvincent.ai`。** Vincent 服务器随后会向 Twitter API 发送请求。代理本身不会直接与 Twitter 进行交互。

**密钥生命周期：**
- **创建**：代理运行 `secret create` 命令并指定 `--type DATA_SOURCES` 参数——CLI 会自动保存 API 密钥，并返回 `keyId` 和 `claimUrl`。
- **认领**：操作员使用 `claimUrl` 在 `https://heyvincent.ai` 进行认领操作，以获取访问权限并充值。
- **费用**：每次 API 调用会产生少量费用（详见下方定价信息）。操作员需通过前端界面为代理充值。当信用余额耗尽且未设置支付方式时，调用将被拒绝。
- **撤销**：密钥的所有者可以随时通过 Vincent 前端撤销代理的 API 密钥。

## 定价

| API 端点 | 每次调用费用 |
| --- | --- |
| 搜索推文 | 0.01 美元 |
| 根据 ID 获取推文 | 0.005 美元 |
| 获取用户信息 | 0.005 美元 |
| 获取用户的推文列表 | 0.01 美元 |

每次调用都会自动扣除相应的费用。响应中会包含 `_vincent.creditRemainingUsd` 字段，以便代理能够实时了解剩余信用余额。

## 快速入门

### 1. 检查现有密钥

在创建新密钥之前，请先确认是否已存在密钥：

```bash
npx @vincentai/cli@latest secret list --type DATA_SOURCES
```

如果找到密钥，请将其 `id` 作为后续命令的 `--key-id` 参数使用。如果没有密钥，则需要创建一个新的密钥。

### 2. 创建数据源密钥

```bash
npx @vincentai/cli@latest secret create --type DATA_SOURCES --memo "My agent data sources"
```

该操作会返回 `keyId`（用于后续所有命令）和 `claimUrl`（需告知用户）。创建完成后，告知用户：
> “这是您的数据源访问 URL：`<claimUrl>`。请使用此 URL 在 `https://heyvincent.ai` 进行认领操作并充值。”

**重要提示：** 在进行 API 调用之前，必须先完成密钥的认领并确保有足够的信用余额或已设置支付方式。

### 3. 搜索推文

```bash
npx @vincentai/cli@latest twitter search --key-id <KEY_ID> --q bitcoin --max-results 10
```

参数：
- `--q`（必填）：搜索查询内容（1-512 个字符）
- `--max-results`（可选）：返回的结果数量（10-100 条，默认为 10 条）
- `--start-time`（可选）：ISO 8601 格式的日期时间范围，指定返回最早的时间戳
- `--end-time`（可选）：ISO 8601 格式的日期时间范围，指定返回最新的时间戳

返回内容包括推文文本、创建时间、作者 ID 以及公开数据（点赞数、转发数、回复数）。

### 4. 获取特定推文

```bash
npx @vincentai/cli@latest twitter tweet --key-id <KEY_ID> --tweet-id <TWEET_ID>
```

### 5. 获取用户信息

根据用户名查询 Twitter 用户信息。

```bash
npx @vincentai/cli@latest twitter user --key-id <KEY_ID> --username elonmusk
```

返回用户的简介、关注者/被关注者数量、个人资料图片以及账户认证状态。

### 6. 获取用户的最新推文

```bash
npx @vincentai/cli@latest twitter user-tweets --key-id <KEY_ID> --user-id <USER_ID> --max-results 10
```

**注意：** 此命令需要使用用户的数字 ID（来自用户信息响应），而非用户名。

## 响应元数据

所有成功的响应都会包含一个 `_vincent` 对象，其中包含以下信息：

```json
{
  "_vincent": {
    "costUsd": 0.01,
    "creditRemainingUsd": 4.99
  }
}
```

通过 `_vincent.creditRemainingUsd` 字段，可以提醒用户剩余的信用余额。

## 速率限制

- 每个 API 密钥每分钟最多可发送 60 次请求（涵盖所有数据源，包括 Twitter 和 Brave Search）。
- 如果超出速率限制，系统会返回 `429` 错误代码。请稍后重试。

## 重新链接（恢复 API 访问权限）

如果代理丢失了 API 密钥，密钥的所有者可以通过前端生成一个**重新链接令牌**。代理可以使用此令牌获取新的 API 密钥。

```bash
npx @vincentai/cli@latest secret relink --token <TOKEN_FROM_USER>
```

CLI 会使用该令牌获取新的 API 密钥，自动保存新密钥并返回 `keyId`。重新链接令牌仅限一次性使用，有效期为 10 分钟。

## 重要说明：
- 单个 `DATA_SOURCES` API 密钥适用于**所有**数据源（Twitter、Brave Search 等）。无需为每个数据源分别配置密钥。
- 创建密钥后，请务必将访问 URL 告知用户。
- 如果调用因信用不足而被拒绝，请告知用户在 `https://heyvincent.ai` 充值。
- Twitter 的搜索接口仅返回过去 7 天内的推文（这是 X API v2 的限制规定）。