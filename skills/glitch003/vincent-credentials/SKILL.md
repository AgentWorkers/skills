---
name: Vincent - Credentials for agents
description: 使用此技能可以安全地存储凭据（API密钥、密码、令牌），并将它们写入 `.env` 文件中，从而避免在代理程序的上下文中泄露这些敏感信息。
homepage: https://heyvincent.ai
source: https://github.com/HeyVincent-ai/Vincent
metadata:
  clawdbot:
    homepage: https://heyvincent.ai
    requires:
      config:
        - ${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/credentials/credentials
        - ./credentials
---
# Vincent – 代理的凭证管理功能

使用此功能可以安全地管理应用程序所需的凭证，包括 API 密钥、密码、OAuth 令牌、SSH 密钥或结构化的用户名/密码对。代理会生成一个秘密值，用户（或代理本身）设置该值，然后通过 CLI 将其直接写入 `.env` 文件中。**凭证值永远不会出现在代理的上下文中或标准输出（stdout）中。**

当代理需要使用凭证（例如第三方 API 密钥）时，这一功能非常有用。用户无需将凭证信息粘贴到聊天框中（这样凭证信息就会进入代理的上下文），而是通过 Vincent 仪表板进行设置，代理再通过 CLI 将其写入 `.env` 文件。

所有命令都依赖于 `@vincentai/cli` 包。API 密钥会自动存储和解析——您无需直接处理原始密钥或文件路径。

## 安全模型

此功能的设计目的是**确保凭证不会被暴露在代理的上下文中**。

**工作原理：** `secret env` CLI 命令从 Vincent 服务器获取凭证信息，并将其直接写入磁盘上的 `.env` 文件中。该值永远不会被打印到标准输出中，也不会出现在代理的对话框中。许多代理框架会禁止读取 `.env` 文件，因此即使文件存在于磁盘上，代理也无法读取其中的内容。应用程序在运行时可以正常读取 `.env` 文件中的凭证信息。

**无需环境变量**，因为此功能采用“代理优先”的认证机制：代理在运行时通过调用 Vincent API 生成自己的凭证密钥，API 会返回一个具有特定权限范围的 API 密钥。CLI 会在创建过程中自动存储该密钥。密钥的存储路径（`${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/credentials/credentials/` 或 `./credentials/`）在功能的元数据中进行了指定。

**重写保护机制：** 一旦某个凭证值被某个代理的 API 密钥设置，只有相同的 API 密钥才能覆盖该值。这一机制在数据库层面得到原子级执行，防止其他代理或密钥篡改凭证。

**所有 API 调用都通过 HTTPS/TLS 协议发送到 `heyvincent.ai`**，不会访问其他端点、服务或外部主机。

**密钥生命周期：**

- **创建**：代理运行 `secret create` 命令，并指定 `--type CREDENTIALS` 参数——CLI 会自动存储 API 密钥，并返回一个 `keyId` 和 `claimUrl`。
- **设置值**：用户通过仪表板设置凭证值，或者代理通过 REST API 设置该值。
- **写入 `.env` 文件**：代理运行 `secret env` 命令将值写入 `.env` 文件，同时不会暴露该值。
- **声明所有权**：操作员可以通过仪表板使用提供的链接来声明对该凭证的所有权并进行管理。
- **撤销**：凭证的所有者可以随时通过 `https://heyvincent.ai` 撤销代理的 API 密钥。

## 密钥类型

| 类型 | 值格式 | 使用场景 |
|---|---|---|
| `API_KEY` | 非空字符串 | 第三方 API 密钥 |
| `SSH_KEY` | 非空字符串 | SSH 私钥 |
| `OAUTH_TOKEN` | 非空字符串 | OAuth 访问/刷新令牌 |
| `CREDENTIALS` | 包含 `password` 或 `secret` 的 JSON 对象 | 用户名/密码、密钥/秘密对 |

所有四种类型的密钥都支持相同的创建、设置和写入 `.env` 文件的流程。

### `CREDENTIALS` 的值格式

`CREDENTIALS` 的值必须是一个 JSON 对象，其中至少包含以下一项：

- `password`（字符串）——例如 `{"username": "alice", "password": "hunter2"}`
- `secret`（字符串）——例如 `{"accountId": "acct-1", "secret": "top-secret"}`

其他字段会原样保留。所有值的大小限制为 16KB。

## 快速入门

### 1. 检查是否存在现有密钥

在创建新密钥之前，先检查是否已经存在密钥：

```bash
npx @vincentai/cli@latest secret list --type CREDENTIALS
```

如果找到密钥，请使用其 `id` 作为后续命令的 `--key-id` 参数。如果没有密钥，则创建一个新的密钥。

### 2. 创建凭证

```bash
npx @vincentai/cli@latest secret create --type CREDENTIALS --memo "Acme API credentials"
```

创建新密钥后，系统会返回 `keyId`（用于后续命令）、`claimUrl`（用于与用户共享）和 `secretId`。

创建完成后，告知用户：

> “这是您的凭证声明链接：`<claimUrl>`。请使用该链接在 `https://heyvincent.ai` 上声明所有权并设置凭证值。”

### 3. 设置凭证值

**选项 A：用户通过仪表板设置（推荐）**

用户使用声明链接声明对凭证的所有权，然后通过仪表板设置凭证值。这样可以确保凭证值完全不在代理的控制范围内。

**选项 B：代理通过 REST API 设置**

对于那些由代理自己管理凭证的工作流程（例如代理从服务获取 API 密钥的情况）：

```bash
curl -X PATCH https://heyvincent.ai/api/secrets/<SECRET_ID>/value/agent \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"value": {"username": "alice", "password": "hunter2"}}'
```

对于简单的字符串类型（`API_KEY`、`SSH_KEY`、`OAUTH_TOKEN`）：

```bash
curl -X PATCH https://heyvincent.ai/api/secrets/<SECRET_ID>/value/agent \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"value": "sk-my-third-party-api-key"}'
```

### 4. 将值写入 `.env` 文件

设置好凭证值后，使用 CLI 将其写入 `.env` 文件。**该值永远不会被打印到标准输出中。**

```bash
# Write an API_KEY secret as an env var
npx @vincentai/cli@latest secret env --key-id <KEY_ID> --env-var ACME_API_KEY

# For CREDENTIALS: extract a specific field
npx @vincentai/cli@latest secret env --key-id <KEY_ID> --env-var DB_PASSWORD --field password

# Write to a specific path (default: ./.env)
npx @vincentai/cli@latest secret env --key-id <KEY_ID> --env-var SERVICE_TOKEN --path ./config/.env
```

命令会输出一个确认信息（不包含具体值），以便代理知道操作成功：

```json
{
  "written": "ACME_API_KEY",
  "path": "/path/to/.env",
  "type": "API_KEY"
}
```

**命令参数：**

| 参数 | 是否必填 | 说明 |
|---|---|---|
| `--env-var` | 是 | 环境变量名称（例如 `MY_API_KEY`） |
| `--path` | 否 | `.env` 文件的路径（默认：`./.env`） |
| `--key-id` | 否 | API 密钥 ID（如果只存在一个密钥，则会自动识别） |
| `--field` | 否 | 对于 `CREDENTIALS` 类型：仅提取特定的 JSON 字段，而不是写入整个 JSON 对象 |

**行为：**

- 如果 `.env` 文件不存在，会创建该文件（权限设置为 `0600`）。
- 如果文件中已存在该变量，会直接更新其值。
- 如果变量不存在，会在文件中添加新的一行。
- 包含特殊字符的值会自动加上引号。

### 5. 在应用程序中使用凭证

您的应用程序可以正常读取 `.env` 文件中的凭证信息：

```bash
# Node.js with dotenv
require('dotenv').config()
const apiKey = process.env.ACME_API_KEY

# Python with python-dotenv
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('ACME_API_KEY')
```

## 完整工作流程示例

```bash
# 1. Agent creates a CREDENTIALS secret
npx @vincentai/cli@latest secret create --type CREDENTIALS --memo "Acme service credentials"
# → keyId: abc-123, claimUrl: https://heyvincent.ai/claim/...

# 2. Tell the user to claim and set the value via the dashboard

# 3. Once set, write individual fields to .env
npx @vincentai/cli@latest secret env --key-id abc-123 --env-var ACME_USERNAME --field username
npx @vincentai/cli@latest secret env --key-id abc-123 --env-var ACME_PASSWORD --field password

# Result in .env:
# ACME_USERNAME=alice
# ACME_PASSWORD=hunter2
```

## 重新链接（恢复 API 访问权限）

如果代理丢失了 API 密钥，凭证的所有者可以通过前端生成一个**重新链接令牌**。代理可以使用这个令牌获取新的 API 密钥。

```bash
npx @vincentai/cli@latest secret relink --token <TOKEN_FROM_USER>
```

CLI 会使用该令牌获取新的 API 密钥，并自动将其存储起来，同时返回新的 `keyId`。重新链接令牌仅限一次性使用，有效期为 10 分钟。

## 重要说明：

- **凭证值永远不会进入代理的上下文中。** `secret env` 命令会直接将凭证信息写入文件，不会将其打印到标准输出中。
- 许多代理框架（如 OpenClaw、Claude Code 等）禁止读取 `.env` 文件，从而提供了额外的安全保障。
- 创建凭证后，请务必将声明链接告知用户。
- 所有值的大小限制为 16KB。
- 如果尝试覆盖凭证值时收到 403 错误，说明有其他 API 密钥设置了该值。凭证的所有者可以通过仪表板进行管理。