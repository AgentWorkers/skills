---
name: 1claw
version: 1.1.0
description: 基于HSM（硬件安全模块）的AI代理秘密管理功能：通过1Claw保管库存储、检索、轮换和共享秘密，同时确保这些秘密不会在上下文中被泄露。
homepage: https://1claw.xyz
repository: https://github.com/1clawAI/1claw
metadata:
    {
        "openclaw":
            {
                "requires":
                    {
                        "env":
                            [
                                "ONECLAW_AGENT_ID",
                                "ONECLAW_AGENT_API_KEY",
                                "ONECLAW_VAULT_ID",
                            ],
                        "bins": [],
                    },
                "primaryEnv": "ONECLAW_AGENT_ID",
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
                "credentials": ["ONECLAW_AGENT_API_KEY"],
                "optional_credentials":
                    ["ONECLAW_AGENT_ID", "ONECLAW_VAULT_ID"],
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
                        "tx:sign",
                        "tx:simulate",
                    ],
            },
    }
---
# 1Claw — 为AI代理提供HSM支持的秘密管理工具

1Claw是一个基于云HSM（Hardware Security Module）的秘密管理平台。代理在运行时可以访问API密钥、密码和凭证，而无需将这些信息暴露在通信过程中。所有秘密都使用HSM中的密钥进行加密。

**API基础URL:** `https://api.1claw.xyz`  
**Shroud（TEE代理）:** `https://shroud.1claw.xyz`  
**MCP端点:** `https://mcp.1claw.xyz/mcp`  
**仪表板:** `https://1claw.xyz`  
**文档:** `https://docs.1claw.xyz`  

## 适用场景  
- 当您需要API密钥、密码或凭证来完成某项任务时  
- 当您希望安全存储新生成的凭证时  
- 当您需要与用户或其他代理共享秘密时  
- 当您在重新生成凭证后需要更新其有效期时  
- 当您在使用秘密之前想要检查其是否存在时  
- 当您希望在不暴露私钥的情况下执行EVM（以太坊虚拟机）交易时  
- 当您需要TEE（Trusted Execution Environment）级别的密钥隔离时（请使用`shroud.1claw.xyz`代理）  

---

## 设置方法  

### 选项0：自助注册（新代理）  
如果您还没有凭证，可以自助注册——系统会通过电子邮件将代理ID和API密钥发送给您：  
```bash
# curl
curl -s -X POST https://api.1claw.xyz/v1/agents/enroll \
  -H "Content-Type: application/json" \
  -d '{"name":"my-agent","human_email":"human@example.com"}'

# TypeScript SDK (static method, no auth needed)
import { AgentsResource } from "@1claw/sdk";
await AgentsResource.enroll("https://api.1claw.xyz", {
  name: "my-agent",
  human_email: "human@example.com",
});

# CLI (no auth needed)
npx @1claw/cli agent enroll my-agent --email human@example.com
```  

收到这些信息后，您需要为代理配置访问权限。  

### 选项1：使用MCP服务器（推荐用于AI代理）  
您可以在MCP客户端配置中设置代理的访问信息。只需提供API密钥即可，代理ID和凭证库会自动识别。  
```json
{
    "mcpServers": {
        "1claw": {
            "command": "npx",
            "args": ["-y", "@1claw/mcp"],
            "env": {
                "ONECLAW_AGENT_API_KEY": "<agent-api-key>"
            }
        }
    }
}
```  

可选参数：`ONECLAW_AGENT_ID`（指定代理ID），`ONECLAW_VAULT_ID`（指定凭证库ID）。  

### 其他配置选项：  
- **托管HTTP流模式**：[具体配置代码]  
```
URL: https://mcp.1claw.xyz/mcp
Headers:
  Authorization: Bearer <agent-jwt>
  X-Vault-ID: <vault-uuid>
```  

### TypeScript SDK  
[相关SDK配置代码]  
```bash
npm install @1claw/sdk
```  

### 直接使用REST API  
在每次请求时都需要进行身份验证，并传递Bearer令牌。  
```bash
# Exchange agent API key for a JWT (key-only — agent_id is auto-resolved)
RESP=$(curl -s -X POST https://api.1claw.xyz/v1/auth/agent-token \
  -H "Content-Type: application/json" \
  -d '{"api_key":"<key>"}')
TOKEN=$(echo "$RESP" | jq -r .access_token)
AGENT_ID=$(echo "$RESP" | jq -r .agent_id)

# Use the JWT
curl -H "Authorization: Bearer $TOKEN" https://api.1claw.xyz/v1/vaults
```  

**替代方案：**  
`1ck_` API密钥（个人或代理专用）可以直接用作Bearer令牌，无需进行JWT交换。  

---

## 身份验证  

### 代理身份验证流程  
1. 人类管理员在仪表板或通过`POST /v1/agents`接口注册代理，可以选择`auth_method`（默认为`api_key`、`mtls`或`oidc_client_credentials`）。对于使用`api_key`注册的代理，系统会返回`agent_id`和`api_key`（前缀为`ocv_`）；对于使用mtls/OIDC注册的代理，仅返回`agent_id`。  
2. 所有代理会自动获得一对Ed25519 SSH密钥（公钥存储在代理记录中，私钥存储在`__agent-keys`凭证库中）。  
3. 使用`api_key`注册的代理可以通过`POST /v1/auth/agent-token`接口交换凭证：  
   ```json
   { "api_key": "<key>" }
   ```  
   系统会返回：  
   ```json
   { "access_token": "<jwt>", "expires_in": 3600, "agent_id": "<uuid>", "vault_ids": ["..."] }
   ```  
   代理ID是可选的，系统会从密钥前缀中自动推断出来。  
4. 代理在后续请求中需要使用`Authorization: Bearer <jwt>`进行身份验证。  
5. JWT的权限范围由代理的访问策略决定；如果没有策略，则权限范围为空（无法访问任何秘密）。代理的`vault_ids`也会包含在JWT中，用于限制访问未被列出的凭证库。  

## MCP工具参考  

### `list_secrets`  
列出凭证库中的所有秘密。返回秘密的路径、类型和版本信息，但不包含秘密值。  
| 参数 | 类型 | 是否必填 | 描述 |  
| ---- | ---- | ------ | -------- | ---------------------- |  
| `prefix` | string | 否 | 用于过滤的路径前缀（例如`api-keys/`） |  

### `get_secret`  
获取秘密的解密值。请在需要使用该秘密的API调用之前立即获取该值。切勿将秘密值存储或包含在响应中。  
| 参数 | 类型 | 是否必填 | 描述 |  
| ---- | ---- | ------ | ---------------------- |  
| `path` | string | 是 | 秘密的路径（例如`api-keys/stripe`） |  

### `put_secret`  
存储新的秘密或更新现有秘密。每次调用都会创建一个新的版本。  
| 参数 | 类型 | 是否必填 | 默认值 | 描述 |  
| ---- | ---- | -------- | ---------------------- |  
| `path` | string | 是 | 秘密的路径 |  
| `value` | string | 是 | 秘密的值 |  
| `type` | string | 否 | 类型：`api_key`、`password`、`private_key`、`certificate`、`file`、`note`、`ssh_key`、`env_bundle` |  
| `metadata` | object | 否 | 可选的JSON元数据 |  
| `expires_at` | string | 否 | 秘密的过期时间（ISO 8601格式） |  
| `max_access_count` | number | 否 | 最大访问次数（超过次数后将自动过期） |  

### `delete_secret`  
软删除秘密。管理员可以随时恢复该秘密。  
| 参数 | 类型 | 是否必填 | 描述 |  
| ---- | ---- | ---------------------- |  
| `path` | string | 是 | 要删除的秘密的路径 |  

### `describe_secret`  
获取秘密的元数据（类型、版本和过期时间），但不获取秘密值。用于检查秘密是否存在。  
| 参数 | 类型 | 是否必填 | 描述 |  
| ---- | ---- | ------ | ---------------------- |  
| `path` | string | 是 | 秘密的路径 |  

### `rotate_and_store`  
为现有秘密存储新值，同时创建一个新的版本。请在重新生成密钥后使用此方法。  
| 参数 | 类型 | 是否必填 | 描述 |  
| ---- | ---- | ---------------------- |  
| `path` | string | 秘密的路径 |  
| `value` | string | 新的秘密值 |  

### `get_env_bundle`  
获取`env_bundle`类型的秘密，并将其`KEY=VALUE`格式的键值对解析为JSON格式。  
| 参数 | 类型 | 是否必填 | 描述 |  
| ---- | ---- | ---------------------- |  
| `path` | string | 是 | `env_bundle`秘密的路径 |  

### `create_vault`  
创建一个新的凭证库来管理秘密。  
| 参数 | 类型 | 是否必填 | 描述 |  
| ---- | ---- | ---------------------- |  
| `name` | string | 策略库的名称（1–255个字符） |  
| `description` | string | 策略库的简短描述 |  

### `list_vaults`  
列出您有权访问的所有凭证库。无需参数。  

### `grant_access`  
授予用户或代理对特定凭证库的访问权限。  
| 参数 | 类型 | 是否必填 | 默认值 | 描述 |  
| ---- | ---- | ---------------------- |  
| `vault_id` | string (UUID) | 是 | 策略库ID |  
| `principal_type` | `user` \| `agent` | 是 | 授予访问权限的对象类型 |  
| `principal_id` | string (UUID) | 是 | 用户或代理的UUID |  
| `permissions` | string[] | 是否允许的权限（例如`["read"]`、`["write"]`） |  
| `secret_path_pattern` | string | 是否允许的秘密路径模式 |  

### `share_secret`  
通过链接分享秘密，可以分享给创建代理的人或特定的用户/代理。  
| 参数 | 类型 | 是否必填 | 描述 |  
| ---- | ---- | ---------------------- |  
| `secret_id` | string (UUID) | 是 | 秘密的UUID |  
| `recipient_type` | `user` \| `agent` \| `anyone_with_link` \| `creator` | 分享方式 |  
| `recipient_id` | string (UUID) | 是 | （对于`user`和`agent`类型）接收者ID |  
| `expires_at` | string | 是否设置过期时间 |  
| `max_access_count` | number | 是否设置最大访问次数 |  

### `simulate_transaction`  
模拟EVM交易，但不进行签名。返回交易金额变化、Gas费用估算以及交易是否成功/失败的信息。  
| 参数 | 类型 | 是否必填 | 默认值 | 描述 |  
| ---- | ---- | ---------------------- |  
| `to` | string | 目标地址（以`0x`开头） |  
| `value` | string | 交易金额（以ETH为单位） |  
| `chain` | string | 链路名称或ID |  
| `data` | string | 数据（以hex编码格式） |  
| `signing_key_path` | string | 签名键的路径（位于`keys/{chain}`目录下） |  
| `gas_limit` | number | Gas费用限制 |  

### REST API快速参考  
基础URL：`https://api.1claw.xyz`。所有需要身份验证的接口都需要使用`Authorization: Bearer <token>`进行请求。  

### 公开访问（无需令牌）  
| 方法 | 路径 | 描述 |  
| ---- | ---------------------- | ---------------------- |  
| `POST` | `/v1/auth/token` | 登录（使用电子邮件和密码） → 返回`access_token` |  
| `POST` | `/v1/auth/agent-token` | 代理登录（使用代理ID和API密钥） → 返回`access_token` |  
| `POST` | `/v1/auth/google` | 使用Google OAuth登录 |  
| `POST` | `/v1/auth/signup` | 注册新账户 → 发送验证邮件 |  
| `POST` | `/v1/auth/verify-email` | 验证电子邮件令牌 → 创建用户账户 |  
| `POST` | `/v1/auth/mfa/verify` | 登录时验证MFA代码 |  

### 已认证用户可使用的接口  
| 方法 | 路径 | 描述 |  
| ---- | ---------------------- | ---------------------- |  
| `GET` | `/v1/auth/me` | 获取当前用户信息 |  
| `PATCH` | `/v1/auth/me` | 更新用户信息（`display_name`、`marketing_emails`） |  
| `DELETE` | `/v1/auth/me` | 删除账户（请求体中包含`{"confirmation": "DELETE MY ACCOUNT"}`） |  
| `DELETE` | `/v1/auth/token` | 注销当前令牌 |  
| `POST` | `/v1/auth/change-password` | 更改密码 |  

### 策略库相关接口  
| 方法 | 路径 | 描述 |  
| ---- | ---------------------- | ---------------------- |  
| `POST` | `/v1/vaults` | 创建新的策略库（`{ name, description?}`） → 返回`201` |  
| `GET` | `/v1/vaults` | 列出所有策略库 |  
| `GET` | `/v1/vaults/{id}` | 获取特定策略库的详细信息 |  
| `DELETE` | `/v1/vaults/{id}` | 删除策略库 |  
| `POST` | `/v1/vaults/{id}/cmek` | 启用CMEK（`{ fingerprint }`） |  
| `DELETE` | `/v1/vaults/{id}/cmek` | 关闭CMEK |  
| `POST` | `/v1/vaults/{id}/cmek-rotate` | 启动CMEK密钥轮换（请求头中包含`X-CMEK-Old-Key`、`X-CMEK-New-Key`） |  
| `GET` | `/v1/vaults/{id}/cmek-rotate/{job_id}` | 获取轮换作业的状态 |  

### 秘密相关接口  
| 方法 | 路径 | 描述 |  
| ---- | ---------------------- | ---------------------- |  
| `PUT` | `/v1/vaults/{id}/secrets/{path}` | 存储/更新秘密（`{ type, value, metadata?, expires_at?, max_access_count?}`） → 返回`201` |  
| `GET` | `/v1/vaults/{id}/secrets/{path}` | 获取秘密信息（包含路径、类型、值和版本） |  
| `DELETE` | `/v1/vaults/{id}/secrets/{path}` | 删除秘密 |  
| `GET` | `/v1/vaults/{id}/secrets?prefix=...` | 列出所有秘密的元数据（不包含秘密值） |  

### 代理相关接口  
| 方法 | 路径 | 描述 |  
| ---- | ---------------------- | ---------------------- |  
| `POST` | `/v1/agents` | 创建代理（包含`agent: {...}, api_key: "ocv_..."`） |  
| `GET` | `/v1/agents` | 列出所有代理 |  
| `GET` | `/v1/agents/{id}` | 获取特定代理的信息 |  
| `GET` | `/v1/agents/me` | 获取当前代理的信息 |  
| `PATCH` | `/v1/agents/{id}` | 更新代理信息（`is_active`、`scopes`、`intents_api_enabled`等） |  
| `DELETE` | `/v1/agents/{id}` | 删除代理 |  
| `POST` | `/v1/agents/{id}/rotate-key` | 旋转代理的API密钥 |  
| `POST` | `/v1/agents/{id}/rotate-identity-keys` | 旋转代理的SSH密钥和ECDH密钥对（仅限管理员操作） |  

### 访问控制相关接口  
| 方法 | 路径 | 描述 |  
| ---- | ---------------------- | ---------------------- |  
| `POST` | `/v1/vaults/{id}/policies` | 创建访问控制策略（`{ principal_type, principal_id, secret_path_pattern, permissions, conditions?, expires_at?}`） |  
| `GET` | `/v1/vaults/{id}/policies` | 列出策略库的策略 |  
| `PUT` | `/v1/vaults/{id}/policies/{pid}` | 更新策略（仅更新`permissions`和`expires_at`） |  
| `DELETE` | `/v1/vaults/{id}/policies/{pid}` | 删除策略 |  

### 分享相关接口  
| 方法 | 路径 | 描述 |  
| ---- | ---------------------- | ---------------------- |  
| `POST` | `/v1/secrets/{id}/share` | 创建分享链接 |  
| `GET` | `/v1/shares/outbound` | 查看您创建的分享链接 |  
| `GET` | `/v1/shares/inbound` | 查看发送给您的分享链接 |  
| `POST` | `/v1/shares/{id}/accept` | 接受传入的分享链接 |  
| `POST` | `/v1/shares/{id}/decline` | 拒绝传入的分享链接 |  
| `DELETE` | `/v1/share/{id}` | 取消分享链接 |  
| `GET` | `/v1/share/{id}` | 查看分享链接的内容 |  

### Intents API（需`intents_apienabled`启用）  
| 方法 | 路径 | 描述 |  
| ---- | ---------------------- | ---------------------- |  
| `POST` | `/v1/agents/{id}/transactions` | 提交交易请求（可选`Idempotency-Key`头用于防止重复提交） |  
| `GET` | `/v1/agents/{id}/transactions` | 查看代理的交易记录（`signed_tx`字段会被隐藏，除非`?include_signed_tx=true`） |  
| `GET` | `/v1/agents/{id}/transactions/{txid}` | 获取交易详情（`signed_tx`字段会被隐藏，除非`?include_signed_tx=true`） |  
| `POST` | `/v1/agents/{id}/transactions/simulate` | 模拟单次交易 |  
| `POST` | `/v1/agents/{id}/transactions/simulate-bundle` | 模拟多个交易 |  

### 审计相关接口  
| 方法 | 路径 | 描述 |  
| ---- | ---------------------- | ---------------------- |  
| `GET` | `/v1/audit/events?limit=N&action=...&from=...&to=...` | 查询审计事件 |  

### 账务相关接口  
| 方法 | 路径 | 描述 |  
| ---- | ---------------------- | ---------------------- |  
| `GET` | `/v1/billing/subscription` | 查看订阅状态和使用情况 |  
| `GET` | `/v1/billing/credits/balance` | 查看信用余额和过期时间 |  
| `GET` | `/v1/billing/credits/transactions` | 查看交易记录 |  
| `PATCH` | `/v1/billing/overage-method` | 设置超出使用量的处理方式（`credits`或`x402`） |  
| `GET` | `/v1/billing/usage` | 查看当前月的使用情况 |  
| `GET` | `/v1/billing/history` | 查看使用历史记录 |  

### 其他接口  
| 方法 | 路径 | 描述 |  
| ---- | ---------------------- | ---------------------- |  
| `GET` | `/v1/health` | 获取系统健康状态 |  
| `GET` | `/v1/health/hsm` | 获取HSM的健康状态 |  
| `POST/GET/DELETE` | `/v1/auth/api-keys[/{id}` | 管理个人API密钥 |  
| `GET/POST/DELETE` | `/v1/security/ip-rules[/{id}` | 管理IP访问规则 |  
| `GET/PATCH/DELETE` | `/v1/org/members[/{id}` | 管理组织成员 |  

## SDK方法参考  
所有方法返回`Promise<OneclawResponse<T>`类型。可以通过`client.<resource>.<method>(...)`进行调用。  
| 资源 | 方法 | 描述 |  
| ---- | ---------------------- | ---------------------- |  
| `vaults` | `create` | 创建策略库 |  
| `vaults` | `get` | 获取策略库信息 |  
| `vaults` | `list` | 列出所有策略库 |  
| `vaults` | `delete` | 删除策略库 |  
| `secrets` | `set` | 存储/更新秘密 |  
| `secrets` | `get` | 获取秘密（解密后返回） |  
| `secrets` | `list` | 列出秘密元数据 |  
| `secrets` | `delete` | 删除秘密 |  
| `agents` | 创建/更新代理信息 |  
| `agents` | 提交交易请求 |  
| `agents` | 模拟交易 |  
| `agents` | 获取交易详情 |  
| `agents` | 授权代理访问权限 |  
| `agents` | 授权用户访问权限 |  
| `agents` | 更新代理策略 |  
| `agents` | 删除代理 |  
| `agents` | 旋转代理API密钥 |  
| `agents` | 提交交易请求 |  
| `agents` | 模拟交易 |  
| `agents` | 获取交易详情 |  
| `agents` | 列出代理的交易记录 |  
| `access` | 授权代理访问权限 |  
| `access` | 授权用户访问权限 |  
| `access` | 更新策略 |  
| `access` | 取消代理访问权限 |  
| `sharing` | 创建分享链接 |  
| `access` | 查看分享链接 |  
| `sharing` | 接受/拒绝分享链接 |  
| `audit` | 查询审计事件 |  
| `billing` | 查看使用情况和账单信息 |  

## SDK方法参考（详细信息）  
所有SDK方法返回`Promise<OneclawResponse<T>`类型。可以通过`client.<resource>.<method>(...)`进行调用。  
| 资源 | 方法 | 描述 |  
| ---- | ---------------------- | ---------------------- |  
| ... | ... | ... | ... |  

## 支持的区块链  
默认支持的区块链列表（通过`GET /v1/chains`查询）：  
| 名称 | 链路ID | 是否为测试网 |  
| ----- | -------- | -------- | ---------------------- |  
| ethereum | 1 | 否 |  
| base | 8453 | 否 |  
| optimism | 10 | 否 |  
| arbitrum-one | 42161 | 否 |  
| polygon | 137 | 否 |  
| sepolia | 11155111 | 是 |  
| base-sepolia | 84532 | 是 |  

在交易请求中可以使用区块链的名称或ID。  

## 访问控制模型  
代理无法直接访问所有秘密。必须由人类管理员创建访问策略才能允许代理访问特定路径。  
- **路径模式**：使用通配符（如`api-keys/*`、`db/**`、`**`）来指定访问范围。  
- **权限**：`read`、`write`（删除操作需要`write`权限）。  
- **条件**：可以设置IP访问列表和时间限制（JSON格式）。  
- **过期时间**：支持ISO 8601格式的日期。  
如果未匹配任何策略，则会返回`403 Forbidden`错误。策略库的创建者始终具有完全访问权限。  

## 策略库绑定和令牌权限控制  
可以通过以下方式进一步限制代理的访问权限：  
- `vault_ids`：指定代理只能访问特定的策略库；如果未设置此参数，尝试访问其他策略库会返回403错误。  
- `token_ttl_seconds`：为每个代理设置自定义的JWT过期时间（例如300秒）。  
- **令牌权限范围**：JWT的权限范围由代理的访问策略决定；如果没有策略或明确设置权限范围，代理将无法访问任何秘密。  

## 客户管理的加密密钥（CMEK）  
企业级功能（仅限高级用户）：人类管理员可以在仪表板中生成256位的AES密钥；该密钥不会存储在服务器上，仅存储其SHA-256哈希值。  
- **启用CMEK**：通过`POST /v1/vaults/{id}/cmek`接口进行配置。  
- **禁用CMEK**：通过`DELETE /v1/vaults/{id}/cmek`接口进行配置。  
- **轮换CMEK密钥**：通过`POST /v1/vaults/{id}/cmek-rotate`接口进行配置（服务器协助，批量处理）。  

## 其他功能  
- **Intents API**（需`intents_api_enabled`启用）：  
  - 代理可以通过Intents API进行交易签名（密钥存储在HSM中）。  
  - 该功能可防止重复提交相同的交易请求。  
- **Replay Protection（Idempotency-Key）**：在`POST /v1/agents/{id}/transactions`请求中包含`Idempotency-Key: <unique-string>`头；服务器会对密钥进行SHA-256哈希处理并缓存结果，避免重复提交。  

## 安全性措施  
- **代理的LLM流量会通过Shroud代理（`shroud.1claw.xyz`）进行传输**，以实现秘密内容的隐藏、个人身份信息（PII）的过滤和威胁检测。  
- **提供了多种配置选项**，以便管理员精细调整代理的代理行为。  

## 链路管理  
支持自定义SDK的API规范（以npm包形式提供）。  
提供了`openapi.yaml`和`openapi.json`文件，可使用任何OpenAPI 3.1代码生成工具进行生成。  

## 支持的区块链  
默认支持的区块链列表（通过`GET /v1/chains`查询）：  
| 名称 | 链路ID | 是否为测试网 |  
| ----- | -------- | -------- | ---------------------- |  
| ethereum | 1 | 否 |  
| base | 8453 | 否 |  
| optimism | 10 | 否 |  
| arbitrum-one | 42161 | 否 |  
| polygon | 137 | 否 |  
| sepolia | 11155111 | 是 |  
| base-sepolia | 84532 | 是 |  

## 访问控制模型  
代理不能直接访问所有秘密。必须由人类管理员创建访问策略才能允许代理访问特定路径。  
- **路径模式**：使用通配符（如`api-keys/*`、`db/**`等）来指定访问范围。  
- **权限**：`read`、`write`（删除操作需要`write`权限）。  
- **条件**：支持IP访问列表和时间限制（JSON格式）。  
- **过期时间**：支持ISO 8601格式的日期。  

## 其他功能  
- 提供了详细的文档和API接口说明。  
- 支持多种账单和审计功能。  
- 支持自定义SDK的开发和配置。  

---

## 更多信息：  
- 官方网站：[1claw.xyz](https://1claw.xyz)  
- 文档：[docs.1claw.xyz](https://docs.1claw.xyz)  
- 访问仪表板：[1claw.xyz/status](https://1claw.xyz/status)  
- API文档：[https://api.1claw.xyz]  
- SDK：[@1claw/sdk](https://www.npmjs.com/package/@1claw/sdk)  
- OpenAPI规范：[@1claw/openapi-spec](https://www.npmjs.com/package/@1claw/openapi-spec)  
- MCP服务器：[@1claw/mcp](https://www.npmjs.com/package/@1claw/mcp)  
- CLI工具：[@1claw/cli](https://www.npmjs.com/package/@1claw/cli)  
- GitHub仓库：[github.com/1clawAI](https://github.com/1clawAI)  
- 售后支持：[ops@1claw.xyz](mailto:ops@1claw.xyz)