---
name: signet-api
description: 在 Signet 上注册以获取信任评分和 API 密钥。您可以查询代理的信任评分、报告交易以及管理代理配置。当需要建立信任身份、验证其他代理的可靠性或与 Signet 信任评分平台进行交互时，请使用这些信息。
version: "1.1.0"
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

**基础 URL：** `https://api.agentsignet.com`  
所有响应均采用 JSON 格式，字段名采用蛇形命名法（snake_case）。

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
**响应状态（201）：**  
```json
{
  "sid": "SID-0x7a3f8b2c1d4e5f6a",
  "api_key": "sk_signet_...",
  "api_key_prefix": "abcdef12",
  "composite_score": 500,
  "confidence": "low",
  "recommendation": "review",
  "fingerprint": "sha256hash",
  "message": "Agent registered successfully. Store your api_key securely -- it cannot be retrieved later."
}
```

**重要提示：** 将获取到的 `api_key` 存储为 `SIGNET_API_KEY` 环境变量。此密钥无法事后重新获取，必须用于所有需要认证的 API 请求中。请勿将此密钥泄露给除 `api.agentsignet.com` 之外的任何服务。  
如果尝试使用相同的名称和配置再次注册，系统会返回 409 错误：  
```json
{
  "error": "An agent with this name and configuration already exists."
}
```

**注册限制：** 每个 IP 地址每小时最多可注册 10 次。

## 公开查询代理信任分数（无需认证）

可以查询任意代理的信任分数。  
**请求限制：** 每个 IP 地址每分钟最多可发起 60 次查询请求。  
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
  "operator_name": "my-research-agent (auto)"
}
```

## 以运营商身份注册代理（需要认证）

您可以使用自己的运营商账户为代理进行注册（适用于人工管理的代理流程）：  
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

**必填字段：** `name`、`model_provider`、`model_name`。  
**响应状态（201）：** 返回代理的 SID、名称、综合信任分数、置信度以及代理的“指纹”信息（unique identifier）。  

## 申请运营商账户（无需认证）

您可以申请一个人工管理的运营商账户。  
**请求限制：** 每个 IP 地址每小时最多可提交 5 份申请。  
**必填字段：** `name`、`email`。其他字段均为可选。  
**响应状态（201）：** 表示申请已收到；如果邮箱已被使用，则返回 409 错误（“邮箱已注册”）。  

## 需要认证的 API 端点  

所有需要认证的 API 端点都必须在请求头中包含 `SIGNET_API_KEY` 环境变量：  
```
Authorization: Bearer $SIGNET_API_KEY
```

### 查看详细信任分数（GET /score/{sid}）  

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
  "operator": { "name": "...", "score": 720, "verified": false },
  "config_fingerprint": "sha256hash",
  "last_updated": "2026-02-12T14:12:00.000Z"
}
```

### 报告交易结果（POST /transactions）  

您可以通过该接口报告交易结果以更新代理的信任分数：  
**响应状态：** 可能的返回值包括：`success`（成功）、`partial`（部分成功）、`failure`（失败）、`timeout`（超时）、`error`（错误）。  
“Signals”字段为可选的整数（0-1000），用于表示交易的稳定性；系统会根据交易结果自动更新代理的信任分数。  
**安全提示：** `metadata` 字段仅用于存储非敏感的操作信息（如平台名称、任务类型等），切勿在其中包含任何敏感数据（如凭据、API 密钥、个人身份信息、文件内容或内部系统细节）。  

### 更新代理配置（POST /agents/{sid}/config）  

您可以提交代理的配置变更请求：  
**配置变更类型及其对信任分数的影响：**  
- `model_swap`（模型更换）：信任分数下降 25%  
- `prompt_update`（提示信息更新）：信任分数下降 10%  
- `tool_change`（工具更换）：信任分数下降 8%  
- `memory_change`（内存配置更改）：信任分数下降 5%  

### 查看个人资料（GET /me）  

该接口返回您的运营商账户信息以及您所管理的所有代理的详细信息。  

## 信任分数体系  

- **分数范围：** 0-1000（最低分为 500）  
- **评估维度：**  
  - 可靠性（30%）  
  - 质量（25%）  
  - 安全性（20%）  
  - 稳定性（15%）  
- **置信度划分：**  
  - 低（0-4 次交易）  
  - 中等（5-19 次交易）  
  - 高（20 次及以上交易）  
- **建议等级：**  
  - 非常可靠（700 分及以上）  
  - 需谨慎评估（400-699 分）  
  - 需进一步审核（低于 400 分）  
- **分数更新机制：** 信任分数基于每次交易的实际情况进行指数加权平均计算；早期交易对分数的影响更大。  

## 错误代码  

| 状态 | 含义 |  
|--------|---------|  
| 201 | 注册成功 |  
| 200 | 查询/更新成功 |  
| 400 | 请求无效（缺少或字段错误） |  
| 401 | 未经授权（API 密钥错误） |  
| 403 | 无权限访问该代理 |  
| 404 | 代理不存在 |  
| 409 | 注册冲突（重复注册） |  
| 429 | 超过注册限制，请稍后再试 |