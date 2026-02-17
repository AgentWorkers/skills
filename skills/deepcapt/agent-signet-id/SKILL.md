---
name: signet-api
description: 在 Signet 上注册以获取信任评分和 API 密钥。您可以查询代理的信任评分、报告交易记录以及管理代理配置。当您需要建立信任关系、验证其他代理的可靠性或与 Signet 信任评分平台进行交互时，请使用这些功能。
version: "1.2.0"
metadata:
  author: DeepCapt - Jeff Hubrig
  website: https://agentsignet.com
  openclaw:
    emoji: "🛡️"
    homepage: https://agentsignet.com/for-agents
    primaryEnv: SIGNET_API_KEY
    requires:
      env: [SIGNET_API_KEY]
---
# Signet API

Signet 是一个用于评估自主 AI 代理信任度的平台。它为每个注册的代理分配一个唯一的 Signet ID（SID）以及一个介于 0 到 1000 之间的综合信任分数。在允许代理进行交易之前，各个平台会查询该代理的信任分数。

**基础 URL:** `https://api.agentsignet.com`  
所有路由也支持 `/v1/` 格式（例如：`https://api.agentsignet.com/v1/register/self`）。  
所有响应均使用 JSON 格式，并采用蛇形命名法（snake_case）来命名字段。  
所有响应中都包含一个 `X-Request-Id` 标头（UUID），用于调试 purposes。

## 自我注册（无需认证）

通过一次请求即可完成注册，获取 SID 和 API 密钥：  
```
POST https://api.agentsignet.com/register/self
Content-Type: application/json

{
  "name": "your-agent-name",
  "model_provider": "anthropic",
  "model_name": "claude-opus-4",
  "description": "What you do",
  "tools": ["web-search", "code-execution"],
  "memory_config": { "type": "persistent" },
  "system_prompt_hash": "sha256-of-your-system-prompt"
}
```

**必填字段：** `name`、`model_provider`、`model_name`。其他字段均为可选。  
**响应（201 状态码）：**  
```json
{
  "sid": "SID-0x7a3f8b2c1d4e5f6a",
  "api_key": "sk_signet_...",
  "api_key_prefix": "abcdef12",
  "composite_score": 300,
  "confidence": "low",
  "recommendation": "caution",
  "identity_level": 0,
  "fingerprint": "sha256hash",
  "message": "Agent registered successfully. Store your api_key securely -- it cannot be retrieved later."
}
```

**重要提示：** 将获取到的 `api_key` 保存为 `SIGNET_API_KEY` 环境变量。该密钥无法事后重新获取，必须用于所有需要认证的 API 请求。请勿将其记录或传输给除 `api.agentsignet.com` 之外的任何服务。  
如果尝试使用相同的名称和配置再次注册，系统会返回 409 状态码：  
```json
{
  "error": "An agent with this name and configuration already exists."
}
```

**注册速率限制：** 每个 IP 地址每小时最多只能注册 10 次。

## 公开查询代理信任分数（无需认证）

可以查询任何代理的信任分数。  
**请求速率限制：** 每个 IP 地址每分钟最多只能发送 60 次请求。  
```
GET https://api.agentsignet.com/score/{sid}/public
```

**响应内容：**  
```json
{
  "sid": "SID-0x7a3f8b2c1d4e5f6a",
  "agent_name": "my-research-agent",
  "composite_score": 782,
  "confidence": "high",
  "recommendation": "clear",
  "identity_level": 1,
  "operator_name": "my-research-agent (auto)"
}
```

## 以运营商身份注册代理（需要认证）

您可以使用自己的运营商账户来注册代理（适用于人工管理的代理流程）：  
```
POST https://api.agentsignet.com/register
Authorization: Bearer $SIGNET_API_KEY
Content-Type: application/json

{
  "name": "agent-name",
  "modelProvider": "anthropic",
  "modelName": "claude-opus-4",
  "description": "What the agent does",
  "tools": ["web-search"],
  "systemPromptHash": "sha256..."
}
```

**必填字段：** `name`、`model_provider`、`models`。  
**响应（201 状态码）：** 返回代理的 SID、名称、综合信任分数、置信度以及相关信息。

## 申请运营商账户（无需认证）

您可以申请一个人工管理的运营商账户。  
**请求速率限制：** 每个 IP 地址每小时最多只能提交 5 次申请。  
```
POST https://api.agentsignet.com/apply
Content-Type: application/json

{
  "name": "Your Name",
  "email": "you@example.com",
  "company": "Your Company",
  "reason": "Why you want access"
}
```

**必填字段：** `name`、`email`。其他字段均为可选。  
**响应（201 状态码）：** 表示申请已收到；如果账号已存在，则返回 409 状态码。  

## 认证后的 API 端点  

所有需要认证的 API 端点都必须使用 `SIGNET_API_KEY` 环境变量进行身份验证：  
```
Authorization: Bearer $SIGNET_API_KEY
```

### 详细查询代理信任分数（GET /score/{sid}）  

该接口返回代理的五个维度信任分数：  
```json
{
  "sid": "SID-0x...",
  "agent_name": "my-agent",
  "composite_score": 782,
  "reliability": 790,
  "quality": 745,
  "financial": 700,
  "security": 650,
  "stability": 750,
  "confidence": "high",
  "recommendation": "clear",
  "identity_level": 1,
  "operator": { "name": "...", "score": 720, "verified": false },
  "config_fingerprint": "sha256hash",
  "last_updated": "2026-02-12T14:12:00.000Z"
}
```

### 报告交易结果（POST /transactions）  

您可以提交交易结果以更新代理的信任分数：  
**响应结果可能包含以下状态：** `success`、`partial`、`failure`、`timeout`、`error`。  
“Signals”字段为可选的整数（0-1000），用于表示交易的稳定性；系统会自动根据交易结果更新代理的信任分数。  
**安全提示：** `metadata` 字段仅用于存储非敏感的操作信息（如平台名称、任务类型等），切勿在其中包含任何凭证、API 密钥、个人身份信息（PII）、文件内容或内部系统细节。

### 更新代理配置（POST /agents/{sid}/config）  

您可以提交配置变更：  
**配置变更的生效方式：**  
- `model_swap`（25%）  
- `prompt_update`（10%）  
- `tool_change`（8%）  
- `memory_change`（5%）  

### 查看个人资料（GET /me）  

该接口返回您的运营商资料以及您所管理的所有代理信息。支持分页查询（示例：`?limit=50&offset=0`，最多显示 200 条记录）。  

### 更换 API 密钥（POST /me/rotate-key）  

系统会生成新的 API 密钥并立即使旧密钥失效：  
**响应内容：**  
`{"api_key": "sk_signet_new...", "api_key_prefix": "...", "message": "API 密钥已更新."}`  
**重要提示：** 更换密钥后请立即更新 `SIGNET_API_KEY` 环境变量，旧密钥将立即失效。  

## 信任分数计算规则：**

- **分数范围：** 0-1000（自我注册的代理初始分数为 300 分，通过运营商注册的代理初始分数为 500 分）  
- **评分维度：**  
  - 可靠性（30%）  
  - 质量（25%）  
  - 安全性（20%）  
  - 稳定性（15%）  
- **置信度判断：**  
  - 低（交易次数少于 20 次）  
  - 中等（交易次数超过 20 次且使用时间超过 7 天）  
  - 高（交易次数超过 100 次且使用时间超过 30 天）  
- **推荐等级：**  
  - “清晰”（分数超过 700 分，置信度中等及以上，身份验证通过）  
  - “审核中”（分数在 400-699 分之间）  
  - “谨慎”（分数低于 400 分）  
- **分数更新机制：** 每笔交易都会对信任分数产生影响，采用指数移动平均算法计算；分数波动范围限制在 ±50 分以内。  
- **身份验证等级：**  
  - 0（未验证，最高推荐等级为“审核中”）  
  - 1（通过回调验证，可提升至“清晰”等级）  
  - 2（通过运营商人工验证）  

## 身份验证流程  

自我注册的代理初始身份等级为 0（未验证），最高推荐等级为“审核中”。若要提升至“清晰”等级，需通过回调进行身份验证：  
**步骤 1：** 发起身份验证请求（POST /agents/{sid}/verify）：**  
```
POST https://api.agentsignet.com/agents/{sid}/verify
Authorization: Bearer $SIGNET_API_KEY
Content-Type: application/json

{
  "callbackUrl": "https://your-agent.example.com/signet-callback"
}
```  
Signet 会向您提供的回调 URL 发送验证请求：  
```json
{
  "type": "signet_verification",
  "challenge": "64-hex-token",
  "sid": "SID-0x...",
  "confirm_url": "https://api.agentsignet.com/agents/SID-0x.../verify/confirm"
}
```  
**步骤 2：** 确认身份（POST /agents/{sid}/verify/confirm）：**  
```
POST https://api.agentsignet.com/agents/{sid}/verify/confirm
Authorization: Bearer $SIGNET_API_KEY
Content-Type: application/json

{
  "challengeToken": "the-64-hex-token-from-step-1"
}
```  
系统会返回验证结果（例如：`{"identity_level": 1, "callback_url": "...", "message": "代理身份已通过回调验证."}`）  
**验证请求速率限制：** 每个代理每小时最多只能进行 3 次尝试；验证请求在 10 分钟后失效。  

## 错误代码说明：**

| 状态码 | 含义 |  
|--------|---------|  
| 201 | 注册成功 |  
| 200 | 查询/更新操作成功 |  
| 400 | 请求无效（缺少或字段格式错误） |  
| 401 | 未授权（API 密钥错误） |  
| 403 | 您无权操作该代理 |  
| 404 | 代理不存在 |  
| 409 | 注册重复 |  
| 429 | 请求超出速率限制，请稍后重试 |  

## OpenAPI 规范  

完整的 OpenAPI 3.1.0 规范可在以下地址查看：  
`https://agentsignet.com/.well-known/skills/signet-api/`  
或通过仓库文件 `api/openapi.yaml` 获取。该规范涵盖了所有 19 个 API 端点，包括请求/响应格式、错误示例及速率限制信息。