---
name: Vincent - Twitter / X.com for agents
description: 使用此技能可以搜索推文、查询用户资料，并从 X.com（Twitter）获取最近的推文。费用按调用次数计费，通过 Vincent 信用系统进行结算。
homepage: https://heyvincent.ai
source: https://github.com/HeyVincent-ai/Vincent
metadata:
  clawdbot:
    homepage: https://heyvincent.ai
    requires:
      config:
        - ~/.openclaw/credentials/datasources
        - ./datasources
---
# Vincent – 用于代理的 Twitter/X.com 接口

使用此技能可以搜索推文、查询用户资料以及从 X.com（Twitter）获取最新推文。所有请求均通过 Vincent 后端进行代理处理，该后端负责与 Twitter API 的身份验证、执行速率限制、记录每次调用的费用，并自动从您的信用余额中扣除费用。

**无需管理 API 密钥。** 代理使用由 Vincent 提供的、范围限定在 `DATA_SOURCES` 秘密配置项中的 API 密钥进行身份验证。Vincent 在服务器端处理与 Twitter API 的交互——代理无法直接访问或管理 Twitter 的 API 密钥。

## 安全模型

此技能专为**具有按次计费功能且需人工监控的自主代理操作**而设计。

**无需环境变量**，因为该技能采用“代理优先”的接入方式：代理在运行时通过调用 Vincent API 来创建 `DATA_SOURCES` 秘密配置项，从而获取一个范围限定的 API 密钥。代理将返回的 API 密钥存储在指定的配置路径中（`~/.openclaw/credentials/datasources/` 或 `./datasources/`）。

**代理的 API 密钥并非 Twitter 的 API 密钥**，而是用于访问 Vincent 代理的承载令牌（Bearer token）。Vincent 服务器会代表代理与 Twitter 进行身份验证。代理无法直接访问上游 API，也无法绕过代理的信用限制和速率限制机制。

**故意启用了模型调用功能**。该技能的目的是让 AI 代理能够自主访问 Twitter 数据。代理应自行执行推文搜索和用户资料查询操作。人工可以通过 `https://heyvincent.ai` 管理代理的信用余额和支付方式。

**所有 API 调用均通过 HTTPS/TLS 协议发送到 `heyvincent.ai`。** Vincent 服务器随后会向 Twitter API 发起请求。代理不会直接与 Twitter 进行通信。

## 密钥生命周期：

- **创建**：代理通过发送 `POST /api/secrets` 请求（`type: "DATA_SOURCES"`）来创建数据源密钥。API 会返回一个范围限定的 API 密钥和一个声明 URL。
- **声明所有权**：操作员需使用声明 URL 在 `https://heyvincent.ai` 网站上声明所有权、添加信用额度并进行支付。
- **费用**：每次 API 调用都会产生少量费用（详见下方定价信息）。操作员需通过前端界面添加信用额度；当信用额度耗尽且未设置支付方式时，调用将被拒绝。
- **撤销**：密钥所有者可以随时通过 Vincent 前端界面撤销代理的 API 密钥。

## 定价

| API 端点 | 每次调用费用 |
| --- | --- |
| 搜索推文 | 0.01 美元 |
| 根据 ID 获取推文 | 0.005 美元 |
| 获取用户资料 | 0.005 美元 |
| 获取用户的推文列表 | 0.01 美元 |

每次调用都会自动扣除相应的费用。响应中会包含 `_vincent.creditRemainingUsd` 字段，以便代理能够实时了解剩余信用额度。

## 配置

所有 API 请求都需要使用承载令牌（即在创建 `DATA_SOURCES` 密钥时获得的 API 密钥）。

创建密钥后，请将其存储在指定的配置路径中。如果是 OpenClaw 实例，请将其保存在 `~/.openclaw/credentials/datasources/<API_KEY_ID>.json` 文件中；否则，请保存在当前工作目录下的 `datasources/<API_KEY_ID>.json` 文件中。

```
Authorization: Bearer <API_KEY>
```

## 快速入门

### 1. 创建数据源密钥

如果您还没有 `DATA_SOURCES` API 密钥，请先创建一个：

```bash
curl -X POST "https://heyvincent.ai/api/secrets" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "DATA_SOURCES",
    "memo": "My agent data sources"
  }'
```

响应内容包括：
- `apiKey`：一个范围限定的 API 密钥，需妥善保管并作为所有数据源请求的承载令牌使用。
- `claimUrl`：用于让用户声明所有权并添加信用额度的链接。

创建完成后，告知用户：
> “这是您的数据源声明 URL：`<claimUrl>`。请使用此链接在 `https://heyvincent.ai` 网站上声明所有权并添加信用额度。”

**重要提示：** 在进行 API 调用之前，必须先声明所有权并确保有足够的信用额度或已设置支付方式。

### 2. 搜索推文

根据关键词搜索最新推文。

```bash
curl -X GET "https://heyvincent.ai/api/data-sources/twitter/search?q=bitcoin&max_results=10" \
  -H "Authorization: Bearer <API_KEY>"
```

参数：
- `q`（必填）：搜索查询内容（1-512 个字符）
- `max_results`（可选）：返回结果数量（10-100 条，默认值：10 条）
- `start_time`（可选）：ISO 861 格式的日期时间，指定返回最早的推文时间
- `end_time`（可选）：ISO 861 格式的日期时间，指定返回最新的推文时间

返回内容包含推文文本、创建时间、作者 ID 以及公开数据（点赞数、转发数、回复数）。

### 3. 获取特定推文

```bash
curl -X GET "https://heyvincent.ai/api/data-sources/twitter/tweets/<TWEET_ID>" \
  -H "Authorization: Bearer <API_KEY>"
```

### 4. 获取用户资料

根据用户名查询 Twitter 用户信息。

```bash
curl -X GET "https://heyvincent.ai/api/data-sources/twitter/users/<USERNAME>" \
  -H "Authorization: Bearer <API_KEY>"
```

返回用户的简介、关注者/被关注者数量、个人资料图片以及账号认证状态。

### 5. 获取用户的最新推文

```bash
curl -X GET "https://heyvincent.ai/api/data-sources/twitter/users/<USER_ID>/tweets?max_results=10" \
  -H "Authorization: Bearer <API_KEY>"
```

参数：
- `max_results`（可选）：返回结果数量（5-100 条，默认值：10 条）

**注意：** 此接口需要使用用户的唯一 ID（来自用户资料信息），而非用户名。

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

当信用额度较低时，可以使用 `_vincent.creditRemainingUsd` 字段提醒用户。

## 速率限制

- 每个 API 密钥每分钟最多允许发起 60 次请求（涵盖所有数据源接口，包括 Twitter 和 Brave Search）。
- 如果达到速率限制，系统会返回 `429` 错误代码。请稍后重试。

## 重新关联（恢复 API 访问权限）

如果代理丢失了 API 密钥，密钥所有者可以通过前端界面生成一个新的**重新关联令牌**。代理可以使用该令牌获取新的 API 密钥。

```bash
curl -X POST "https://heyvincent.ai/api/secrets/relink" \
  -H "Content-Type: application/json" \
  -d '{
    "relinkToken": "<TOKEN_FROM_USER>",
    "apiKeyName": "Re-linked API Key"
  }'
```

重新关联令牌为一次性使用，有效期为 10 分钟。

## 重要注意事项：

- 在创建新的数据源密钥之前，请务必先在指定的配置路径中查找现有的 API 密钥。如果是 OpenClaw 实例，请在 `~/.openclaw/credentials/datasources/` 中查找；否则，请在 `./datasources/` 中查找。
- 一个 `DATA_SOURCES` API 密钥适用于所有数据源（Twitter、Brave Search 等）。无需为每个数据源单独配置密钥。
- 创建密钥后，请务必将声明 URL 分发给用户。
- 如果调用因信用额度不足而被拒绝，请告知用户通过 `https://heyvincent.ai` 添加信用额度。
- Twitter 搜索接口仅返回过去 7 天内的推文（这是 X API v2 的限制规定）。