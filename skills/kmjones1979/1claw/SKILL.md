---
name: 1claw
description: 基于HSM（硬件安全模块）的AI代理秘密管理功能：允许通过1Claw保管库存储、检索、轮换和共享秘密，同时确保这些秘密不会在上下文中被泄露。
homepage: https://1claw.xyz
repository: https://github.com/1clawAI/1claw
metadata:
    {
        "openclaw":
            {
                "requires":
                    {
                        "env": ["ONECLAW_AGENT_TOKEN", "ONECLAW_VAULT_ID"],
                        "bins": [],
                    },
                "primaryEnv": "ONECLAW_AGENT_TOKEN",
                "install":
                    [
                        {
                            "id": "npm",
                            "kind": "node",
                            "package": "@1claw/mcp",
                            "bins": ["1claw-mcp"],
                            "label": "1Claw MCP Server",
                        },
                    ],
                "credentials": ["ONECLAW_AGENT_TOKEN"],
                "permissions":
                    [
                        "vault:read",
                        "vault:write",
                        "vault:delete",
                        "secret:read",
                        "secret:write",
                        "secret:delete",
                        "policy:create",
                        "share:create",
                    ],
            },
    }
---
# 1Claw — 基于硬件安全模块（HSM）的秘密管理工具

使用此功能，您可以通过1Claw安全地存储、检索和共享秘密。1Claw提供了基于硬件安全模块（HSM）的加密机制，确保AI代理在运行时能够访问API密钥、密码和凭证，而不会在通信过程中泄露这些信息。

## 适用场景

- 当您需要API密钥、密码或凭证来完成任务时
- 您希望安全地存储新生成的凭证
- 您需要与用户或其他代理共享秘密
- 在重新生成凭证后，您需要更新其存储方式
- 在使用秘密之前，您想查看可用的秘密列表

## 访问控制模型

代理无法无限制地访问 vault 中的所有秘密。访问权限由以下策略控制：
- **代理可以访问的路径**（例如 `api-keys/*` 或其他路径模式）
- **代理的权限**（读取、写入、删除）
- **访问条件**（IP白名单、时间窗口）
- **权限的有效期限**

必须由人工创建相应的策略才能授予代理访问权限。如果找不到匹配的策略，系统将返回 403 错误。在控制台（Vaults → [vault] → Policies）中，您可以创建策略（选择 vault 和代理），编辑权限/条件/有效期，并删除策略。当代理通过 `POST /v1/auth/agent-token` 接收到 JWT 令牌时，令牌的 `scopes` 会根据这些策略来确定代理的访问权限。如果代理的记录中没有设置 `scopes`，则令牌会自动反映当前的访问策略。

### 加密交易代理

您可以手动将 `crypto_proxy_enabled` 设置为 `true`。启用该功能后：
1. 代理可以通过签名代理提交链上交易请求（签名密钥始终存储在 HSM 中）。
2. 代理将无法直接通过常规的秘密读取接口访问 `private_key` 和 `ssh_key` 类型的秘密（此时会返回 403 错误），从而防止密钥泄露。

交易接口：`POST /v1/agents/{id}/transactions`，参数格式为 `{ to, value, chain }`。后端会从 vault 中获取签名密钥，对交易数据进行签名，并返回签名后的交易数据（十六进制格式）及其 keccak 哈希值。签名密钥会在内存中解密后仅使用一次，随后会被销毁。此功能默认是关闭的，可以随时开启或关闭。

## 设置要求

### 先决条件

1. 在 [1claw.xyz](https://1claw.xyz) 上注册一个 1Claw 账户。
2. 在您的账户下注册一个代理。
3. 为代理配置相应的访问策略。

**人工使用的 CLI：** 对于持续集成/持续部署（CI/CD）和服务器环境，可以使用官方 CLI：`npm install -g @1claw/cli`，然后通过浏览器登录或设置 `ONECLAW_TOKEN` / `ONECLAW_API_KEY`。详细信息请参阅 [文档 — CLI](https://docs.1claw.xyz/docs/guides/cli)。

**API 密钥认证：** `1ck_` 类型的密钥（个人或代理 API 密钥）可以用作所有 API 端点的令牌。无需单独生成 JWT 令牌。

### 推荐使用 MCP 服务器

建议将 1Claw 的 MCP 服务器添加到您的客户端配置中。

**推荐做法：自动刷新代理凭证**：使用 `ONECLAW_AGENT_ID` + `ONECLAW_AGENT_API_KEY` 代替静态 JWT 令牌。MCP 服务器会自动刷新令牌并保持代理的登录状态。

**替代方案：使用静态 JWT 令牌**：`ONECLAW_AGENT_TOKEN` + `ONECLAW_VAULT_ID`（令牌会过期，需要手动刷新）。

**托管模式（HTTP 流式访问）**：请参考相关文档。

### TypeScript SDK

请参阅相关文档以获取 SDK 的使用说明。

## 可用功能

### list_secrets

列出 vault 中的所有秘密。返回秘密的路径、类型和版本信息，但不包含秘密的值。

### get_secret

根据路径获取秘密的解密值。请在调用相关 API 之前立即使用该值。切勿将解密值存储或包含在响应中。

### put_secret

存储新的秘密或更新现有秘密。每次调用都会生成一个新的版本。

### delete_secret

软删除秘密。管理员可以随时恢复该秘密。

### describe_secret

获取秘密的元数据（类型、版本和有效期），无需获取秘密的实际值。此功能用于检查秘密是否存在或是否有效。

### rotate_and_store

为现有秘密更新值，生成新的版本。请在重新生成密钥后使用此功能。

### get_env_bundle

获取 `env_bundle` 类型的秘密，并将其内容（KEY=VALUE 格式）解析为 JSON 数据。

### create_vault

创建一个新的 vault 用于管理秘密。

### list_vaults

列出您有权访问的所有 vault。

### grant_access

授予用户或代理对 vault 的访问权限。您只能为自己创建的 vault 授予访问权限。

### share_secret

可以将秘密共享给创建您的用户、特定用户或代理（通过 ID 标识）。您也可以选择 `recipient_type: "creator"` 以将秘密共享给创建您的用户（无需提供接收者的 ID）。

**注意：** `max_access_count: 0` 表示无限访问权限（即允许无限次读取）。接收共享内容的用户或代理必须明确接受共享请求后才能访问秘密。代理无法创建基于电子邮件的共享链接。

## 安全机制

- **凭证配置由人工完成**：`ONECLAW_AGENT_TOKEN` 和 `ONECLAW_VAULT_ID` 环境变量由拥有该代理的用户在 MCP 服务器配置或 SDK 初始化时设置。
- **代理无法查看自己的凭证**：MCP 服务器会从环境变量中读取凭证，并代表代理处理 API 请求的认证。
- **默认情况下访问是被拒绝的**：即使提供了有效的凭证，代理也只能访问其策略允许的秘密。
- **秘密值仅按需获取**：切勿存储、复制或包含在通信内容中。
- **代理无法创建基于电子邮件的共享链接**：这有助于防止钓鱼攻击。
- **加密代理功能是可选的**：只有当人工启用 `crypto_proxy_enabled` 时，代理才能使用该功能。启用后，直接访问 `private_key` 和 `ssh_key` 类型的秘密会被阻止；默认情况下该功能是关闭的。
- **支持双因素认证**：用户可以在控制台（Settings → Security）中启用基于 TOTP 的双因素认证。启用后，登录时除了输入凭证外还需要提供 6 位验证码。双因素认证不会影响代理的认证过程。

## 最佳实践

- **按需获取秘密**：仅在需要使用秘密时才调用 `get_secret`，而不要在对话开始时就获取。
- **切勿泄露秘密值**：不要在响应中直接显示秘密值，应说明“我已获取 API 密钥并已使用”。
- **先使用 `describe_secret`**：在尝试访问秘密之前，先检查其是否存在或是否有效。
- **使用 `list_secrets` 查看可用凭证**：在尝试访问特定秘密之前，先列出所有可用的凭证。
- **重新生成密钥后及时更新**：在从提供商处重新生成 API 密钥后，立即使用 `rotate_and_store` 功能更新秘密。
- **使用 `grant_access` 进行共享**：这是推荐的安全共享方式，可以精确控制访问权限（包括路径模式和权限设置）。
- **使用 `share_secret` 进行一次性共享**：仅用于与特定用户或代理共享单个秘密。

## 错误处理

| 错误代码 | 错误含义 | 处理方法                                                                                              |
| ------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 404   | 未找到秘密              | 使用 `list_secrets` 检查路径是否正确                                                                                          |
| 410   | 密钥已过期或访问次数达到上限    | 要求用户重新生成新的秘密版本                                                                                         |
| 402   | 信用额度不足             | 通知用户补充信用额度或访问 [1claw.xyz/settings/billing] 进行升级。响应中会包含错误代码：`insufficient_credits`、`no_credits` 或 `x402`。平台管理员及其代理不受此限制 |
| 401   | 未通过认证             | 令牌已过期，请重新认证                                                                                         |
| 403   | 没有访问权限             | 要求用户通过策略授予访问权限                                                                                         |
| 429   | 请求频率受限             | 请稍后再试；每次组织最多只能共享 10 次                                                                                         |

## 相关链接

- 控制台：[1claw.xyz](https://1claw.xyz)
- 文档：[docs.1claw.xyz](https://docs.1claw.xyz)
- SDK：[github.com/1clawAI/1claw-sdk](https://github.com/1clawAI/1claw-sdk)
- MCP 服务器：[npm 上的 @1claw/mcp](https://www.npmjs.com/package/@1claw/mcp)
- API：[https://api.1claw.xyz]