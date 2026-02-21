---
name: 1claw
description: 基于HSM（硬件安全模块）的AI代理密钥管理功能：支持通过1Claw保管库存储、检索、轮换和共享密钥，同时确保密钥不会在传输过程中被泄露。
homepage: https://1claw.xyz
repository: https://github.com/1clawAI/1claw
metadata: {"openclaw":{"requires":{"env":["ONECLAW_AGENT_TOKEN","ONECLAW_VAULT_ID"],"bins":[]},"primaryEnv":"ONECLAW_AGENT_TOKEN","install":[{"id":"npm","kind":"node","package":"@1claw/mcp","bins":["1claw-mcp"],"label":"1Claw MCP Server"}],"credentials":["ONECLAW_AGENT_TOKEN"],"permissions":["vault:read","vault:write","vault:delete","secret:read","secret:write","secret:delete","policy:create","share:create"]}}
---
# 1Claw — 基于硬件安全模块（HSM）的秘密管理

使用此功能，您可以通过 1Claw 保险库安全地存储、检索和共享秘密。1Claw 提供基于硬件安全模块（HSM）的加密机制，确保 AI 代理在运行时能够访问 API 密钥、密码和凭证，而不会在对话过程中泄露这些信息。

## 何时使用此功能

- 当您需要 API 密钥、密码或凭证来完成任务时
- 当您希望安全存储新生成的凭证时
- 当您需要与用户或其他代理共享秘密时
- 当您需要在重新生成凭证后轮换其有效期时
- 当您在使用某个秘密之前想要查看可用的秘密列表时

## 访问控制模型

代理无法无限制地访问保险库中的所有秘密。访问权限由以下策略控制：
- **代理可以访问的路径**（例如 `api-keys/*` 或 `**` 等通配符模式）
- **代理可以执行的操作**（读取、写入、删除）
- **访问条件**（IP 白名单、时间窗口）
- **访问有效期**（策略过期日期）

必须由人工明确创建访问策略才能授予代理访问权限。如果没有匹配的策略，系统会返回 403 错误。

### 加密交易代理

可以通过人工将 `crypto_proxy_enabled` 设置为 `true` 来启用该功能。启用后，会发生以下变化：
1. 代理可以通过签名代理提交链上交易请求——签名密钥始终存储在 HSM 中。
2. 代理无法直接通过常规的秘密读取端点读取 `private_key` 和 `ssh_key` 类型的秘密（此时会返回 403 错误），从而防止密钥泄露。

交易请求的端点为：`POST /v1/agents/{id}/transactions`，参数格式为 `{ to, value, chain }`。后端会从保险库中获取签名密钥，签署 EIP-155 交易，并返回签名后的交易内容及其 keccak 哈希值。密钥会在内存中解密后使用一次，随后被销毁。此功能默认是关闭的，可以随时切换开关。

## 设置

### 先决条件

1. 在 [1claw.xyz](https://1claw.xyz) 上注册一个 1Claw 账户。
2. 在您的账户下注册一个代理。
3. 创建一个允许代理访问保险库的访问策略。

### MCP 服务器（推荐使用）

将 1Claw MCP 服务器添加到您的客户端配置中：

**Claude Desktop / Cursor**（标准输入输出模式）：

```json
{
    "mcpServers": {
        "1claw": {
            "command": "npx",
            "args": ["-y", "@1claw/mcp"],
            "env": {
                "ONECLAW_AGENT_TOKEN": "<your-agent-jwt>",
                "ONECLAW_VAULT_ID": "<your-vault-uuid>"
            }
        }
    }
}
```

**托管模式**（HTTP 流式传输）：

```
URL: https://mcp.1claw.xyz/mcp
Headers:
  Authorization: Bearer <agent-jwt>
  X-Vault-ID: <vault-uuid>
```

### TypeScript SDK

```bash
npm install @1claw/sdk
```

```ts
import { createClient } from "@1claw/sdk";

const client = createClient({
    baseUrl: "https://api.1claw.xyz",
    agentId: process.env.ONECLAW_AGENT_ID,
    apiKey: process.env.ONECLAW_AGENT_API_KEY,
});
```

## 可用工具

### list_secrets

列出保险库中的所有秘密。返回秘密的路径、类型和版本信息，但不包含秘密的具体值。

```
list_secrets()
list_secrets(prefix: "api-keys/")
```

### get_secret

根据路径获取秘密的解密值。请在需要使用该秘密的 API 调用之前立即执行此操作。切勿将解密后的值存储起来或包含在响应中。

```
get_secret(path: "api-keys/stripe")
```

### put_secret

存储新的秘密或更新现有秘密。每次调用都会创建一个新的版本。

```
put_secret(path: "api-keys/stripe", value: "sk_live_...", type: "api_key")
```

支持的秘密类型：`api_key`、`password`、`private_key`、`certificate`、`file`、`note`、`ssh_key`、`env_bundle`。

### delete_secret

软删除秘密。管理员可以随时恢复该秘密。

```
delete_secret(path: "api-keys/old-key")
```

### describe_secret

获取秘密的元数据（类型、版本、有效期），而无需获取秘密的具体值。可用于检查秘密是否存在或是否有效。

```
describe_secret(path: "api-keys/stripe")
```

### rotate_and_store

为现有秘密更新值，同时创建一个新的版本。请在重新生成密钥后使用此功能。

```
rotate_and_store(path: "api-keys/stripe", value: "sk_live_new...")
```

### get_env_bundle

获取 `env_bundle` 类型的秘密，并将其 KEY=VALUE 的键值对解析为 JSON 格式。

```
get_env_bundle(path: "config/prod-env")
```

### create_vault

创建一个新的保险库以管理秘密。

```
create_vault(name: "project-keys", description: "API keys for the project")
```

### list_vaults

列出您有权访问的所有保险库。

```
list_vaults()
```

### grant_access

授予用户或代理访问保险库的权限。您只能为您自己创建的保险库授予访问权限。

```
grant_access(vault_id: "...", principal_type: "agent", principal_id: "...", permissions: ["read"])
```

### share_secret

可以将秘密共享给创建您的用户（即管理员）、特定用户或代理（通过 ID 指定），或者生成一个公开链接。如果希望与管理员共享，可以使用 `recipient_type: "creator"`。此时无需提供接收者的 ID。

### 接收者处理

接收共享内容的用户或代理必须明确接受共享请求后才能访问秘密。代理无法创建基于电子邮件的共享链接。

## 安全模型

- **凭证由人工配置**，而非代理自行设置。`ONECLAW_AGENT_TOKEN` 和 `ONECLAW_VAULT_ID` 环境变量由拥有该代理的用户在 MCP 服务器配置或 SDK 初始化时设置。
- **代理无法查看自己的凭证**。MCP 服务器会从环境中读取这些凭证，并代表代理进行 API 请求的认证。
- **默认情况下访问是被拒绝的**。即使提供了有效的凭证，代理也只能访问其策略允许访问的秘密。
- **秘密值仅在需要时才被获取**，严禁存储、复制或显示在对话内容中。
- **代理无法创建基于电子邮件的共享链接**。这有助于防止通过共享链接进行钓鱼攻击。
- **加密代理功能是可选的**。只有当人工明确启用 `crypto_proxy_enabled` 时，代理才能使用该功能。启用后，直接读取 `private_key` 和 `ssh_key` 类型的秘密将被禁止；默认情况下该功能是关闭的。

## 最佳实践

1. **仅在需要时获取秘密**。请在真正需要使用秘密之前立即调用 `get_secret`，而不要在对话开始时就获取。
2. **切勿显示秘密值**。不要在回复中直接提供秘密的原始值，而是说明“我已获取 API 密钥并已使用它”。
3. **如果只需要检查秘密是否存在或是否有效，请先使用 `describe_secret`。
4. **在使用路径之前，先使用 `list_secrets` 查看可用的秘密列表**。
5. **重新生成密钥后及时更新**。如果在提供商处重新生成了 API 密钥，请立即使用 `rotate_and_store` 功能更新秘密。
6. **使用 `grant_access` 功能进行共享**。这是推荐的共享方式，因为它允许您根据路径模式和权限设置精细化的访问控制。
7. **对于一次性共享需求，使用 `share_secret` 功能**。例如，向特定用户或代理共享单个秘密。

## 错误处理

| 错误代码 | 错误含义                                      | 处理措施                                      |
| ----- | ------------------------------------------- | ------------------------------------------------------ |
| 404   | 未找到秘密                                      | 使用 `list_secrets` 检查路径                         |
| 410   | 秘密已过期或访问次数达到上限                          | 请求用户重新生成新的秘密                             |
| 402   | 免费使用配额已用尽                                  | 建议用户登录 [1claw.xyz/settings/billing] 升级账户                 |
| 401   | 未通过身份验证                                  | 请用户重新登录或更新令牌                             |
| 403   | 无访问权限                                    | 请求用户通过策略授予访问权限                             |
| 429   | 请求频率受限                                    | 请稍后重试；每次组织内最多只能共享 10 次                         |

## 相关链接

- 仪表板：[1claw.xyz](https://1claw.xyz)
- 文档：[docs.1claw.xyz](https://docs.1claw.xyz)
- SDK：[github.com/1clawAI/1claw-sdk](https://github.com/1clawAI/1claw-sdk)
- MCP 服务器：[npm 上的 @1claw/mcp](https://www.npmjs.com/package/@1claw/mcp)
- API：`https://api.1claw.xyz`