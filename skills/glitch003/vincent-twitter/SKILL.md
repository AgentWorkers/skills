---
name: Vincent - Twitter / X.com for agents
description: >
  **用于代理程序的 Twitter/X.com 数据访问功能**  
  当用户需要搜索推文、查询用户资料或获取最新推文时，可使用此功能。该服务采用按次计费的模式，通过 Vincent 信用系统进行结算。  
  触发条件包括：  
  - “search tweets”（搜索推文）  
  - “twitter”  
  - “X.com”  
  - “look up user”（查询用户资料）  
  - “tweet search”（推文搜索）  
  - “twitter profile”（查看用户资料）  
  - “recent tweets”（获取最新推文）
allowed-tools: Read, Write, Bash(npx:*, curl:*)
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

使用此工具可以搜索推文、查询用户资料以及从 X.com（Twitter）获取最新推文。所有请求均通过 Vincent 后端进行代理处理，该后端负责与 Twitter API 的身份验证、限制请求频率、记录每次请求的成本，并自动从用户的信用余额中扣除费用。

**无需管理 API 密钥。** 代理使用由 `DATA_SOURCES` 秘密配置文件指定的 Vincent API 密钥进行身份验证。Vincent 在服务器端处理与 Twitter API 相关的认证信息——代理无需直接接触或管理 Twitter API 密钥。

所有命令均依赖于 `@vincentai/cli` 包。API 密钥的存储和解析过程由系统自动完成，用户无需处理原始密钥或文件路径。

## 安全模型

此工具专为**具有按次计费机制的自主代理操作**设计，并接受人工监督。

**无需设置环境变量**，因为该工具采用“代理优先”的接入方式：代理在运行时通过调用 Vincent API 生成一个 `DATA_SOURCES` 秘密配置文件，从而获取到相应的 API 密钥。CLI 会在创建代理时自动保存该密钥。密钥的存储路径（`${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/credentials/datasources/` 或 `./datasources/`）会在工具的元数据中明确指定。

**代理的 API 密钥并非 Twitter 的官方 API 密钥**，而是用于访问 Vincent 代理的临时令牌。Vincent 服务器会代表代理与 Twitter 进行身份验证。代理无法直接访问 Twitter API，也无法绕过代理的信用限制和请求频率限制。

**故意允许直接调用相关接口**：该工具的目的是让 AI 代理能够自主访问 Twitter 数据。代理应自行完成推文搜索和用户资料查询等操作，人工则通过 `https://heyvincent.ai` 管理代理的信用余额和支付方式。

**所有 API 请求均通过 HTTPS/TLS 协议发送至 `heyvincent.ai`，再由 Vincent 服务器转发至 Twitter API**。代理本身不会直接与 Twitter 进行交互。

**密钥生命周期：**
- **创建**：代理通过 `secret create` 命令（参数 `--type DATA_SOURCES`）生成 API 密钥，CLI 会自动保存该密钥并返回 `keyId` 和 `claimUrl`。
- **获取密钥权限**：人工操作员需使用 `claimUrl` 在 `https://heyvincent.ai` 进行权限申请、添加信用额度并完成支付操作。
- **费用计算**：每次 API 请求会产生少量费用（详见下方定价信息）。用户需通过指定方式补充信用额度；若信用额度不足或未设置支付方式，请求将被拒绝。
- **密钥撤销**：密钥所有者可随时通过 Vincent 界面撤销代理的 API 密钥。

## 定价规则

| API 功能 | 每次请求费用 |
| --- | --- |
| 搜索推文 | 0.01 美元 |
| 根据 ID 获取推文 | 0.005 美元 |
| 获取用户资料 | 0.005 美元 |
| 获取用户的全部推文 | 0.01 美元 |

每次请求的费用会自动从用户的信用余额中扣除。响应结果中会包含 `_vincent.creditRemainingUsd` 字段，以便代理随时了解剩余信用额度。

## 快速入门

### 1. 检查现有密钥

在创建新密钥之前，请先确认是否已有可用密钥：

```bash
npx @vincentai/cli@latest secret list --type DATA_SOURCES
```

如果找到现有密钥，请将其 `id` 作为后续命令的 `--key-id` 参数使用；如果没有密钥，则需要创建新的密钥。

### 2. 创建数据源密钥

```bash
npx @vincentai/cli@latest secret create --type DATA_SOURCES --memo "My agent data sources"
```

创建完成后，系统会返回 `keyId`（用于后续命令）和 `claimUrl`（需告知用户）。完成后告诉用户：
> “这是您的数据源访问 URL：`<claimUrl>`。请使用此 URL 在 `https://heyvincent.ai` 进行权限申请并添加信用额度。”

**重要提示：** 在进行 API 请求之前，必须先申请权限并确保有足够的信用额度或已设置支付方式。

### 3. 搜索推文

```bash
npx @vincentai/cli@latest twitter search --key-id <KEY_ID> --q bitcoin --max-results 10
```

参数说明：
- `--q`（必填）：搜索查询内容（1-512 个字符）
- `--max-results`（可选）：返回结果数量（10-100 条，默认为 10 条）
- `--start-time`（可选）：ISO 8601 格式的开始时间，用于指定返回最早的时间范围的推文
- `--end-time`（可选）：ISO 8601 格式的结束时间，用于指定返回最新时间范围的推文

返回内容包括推文文本、创建时间、作者 ID 以及公开数据（点赞数、转发数、回复数）。

### 4. 获取特定推文

```bash
npx @vincentai/cli@latest twitter tweet --key-id <KEY_ID> --tweet-id <TWEET_ID>
```

### 5. 获取用户资料

根据用户名查询 Twitter 用户的详细信息。

```bash
npx @vincentai/cli@latest twitter user --key-id <KEY_ID> --username elonmusk
```

返回用户的简介、关注者/被关注者数量、个人资料图片以及账号认证状态。

### 6. 获取用户的最新推文

```bash
npx @vincentai/cli@latest twitter user-tweets --key-id <KEY_ID> --user-id <USER_ID> --max-results 10
```

**注意：** 此命令需要使用用户的唯一 ID（来自用户资料信息），而非用户名。

## 响应数据结构

所有成功的响应都会包含一个 `_vincent` 对象，其中包含相关元数据：

```json
{
  "_vincent": {
    "costUsd": 0.01,
    "creditRemainingUsd": 4.99
  }
}
```

当信用余额较低时，系统会通过 `creditRemainingUsd` 字段提醒用户。

## 输出格式

- 推文搜索结果会以特定格式显示。
- 用户资料信息会包含简介、公开数据（关注者/被关注者数量）、个人资料图片以及账号认证状态。

## 错误处理

| 错误代码 | 原因 | 解决方案 |
| --- | --- | --- |
| `401 Unauthorized` | API 密钥无效或缺失 | 确认 `key-id` 是否正确；如有需要请重新获取密钥 |
| `402 Insufficient Credit` | 信用余额为零且未设置支付方式 | 用户需在 `heyvincent.ai` 补充信用额度 |
| `429 Rate Limited` | 每分钟请求次数超过限制（60 次） | 等待片刻后重试 |
| `Key not found` | API 密钥已被撤销或从未生成 | 请向密钥所有者申请新的令牌 |
| `User not found` | 用户在 Twitter 上不存在 | 请核对用户名的正确性 |

## 请求频率限制

- 每个 API 密钥每分钟最多允许发送 60 次请求（涵盖所有数据源，包括 Twitter 和 Brave Search）。
- 如果超出限制，系统会返回 `429` 错误代码，此时请等待片刻后重试。

## 重新获取 API 访问权限

如果代理丢失了 API 密钥，密钥所有者可以通过前端界面生成新的访问令牌。代理可以使用该令牌重新获取 API 密钥：

```bash
npx @vincentai/cli@latest secret relink --token <TOKEN_FROM_USER>
```

CLI 会使用新令牌替换旧的 API 密钥，并自动保存新的 `keyId`。重新生成的令牌仅限一次性使用，有效期为 10 分钟。

## 重要提示：
- 单个 `DATA_SOURCES` API 密钥适用于所有数据源（Twitter、Brave Search 等）。无需为每个数据源单独配置密钥。
- 创建密钥后务必将访问 URL 告知用户。
- 如果请求因信用不足被拒绝，请告知用户前往 `https://heyvincent.ai` 补充信用额度。
- Twitter 搜索接口仅返回过去 7 天内的推文（这是 X API v2 的限制规定）。