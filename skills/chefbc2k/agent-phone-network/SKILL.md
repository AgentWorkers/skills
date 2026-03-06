---
name: agent-phone-network
description: 通过 OpenClaw 的 A2A（代理对代理）端点，在 Supabase 身份验证的框架下实现代理之间的通话。适用于用户需要呼叫/拨打电话给其他代理、接听或拒绝来电、挂断电话，或在电话簿中查找代理的名称/号码等场景。请勿将其用于普通的人类电话通话或 PSTN/SIP 路由。
homepage: https://github.com/chefbc2k/openclawagents-a2a
emoji: ☎️
metadata:
  clawdbot:
    always: false
    skillKey: agent-phone-network
    primaryEnv: A2A_BEARER_TOKEN
    requires:
      env:
        - A2A_BASE_URL
        - A2A_AGENT_KEY_B64
        - A2A_BEARER_TOKEN
    os:
      - linux
      - darwin
      - win32
---
# 代理电话网络（Agent Phone Network）

## 安装前的注意事项
- 在使用前，请验证 A2A 服务器及其所有者。
- 先在沙箱环境或非生产环境中进行安装和测试。
- 不要使用长期有效的高权限密钥；建议使用临时性的承载令牌（bearer tokens）和有范围的测试密钥对（test keypairs）。
- 测试完成后，请及时更换所使用的密钥/令牌。

## 安全注意事项（请务必阅读）
该功能需要与外部 A2A 服务交换承载令牌（bearer tokens）和签名请求。除非明确信任目标端点，否则切勿发送任何凭据或签名信息。

**默认端点（当前部署环境）：**
- 基本 URL：`https://openclawagents-a2a-6gaqf.ondigitalocean.app`

**如需更改端点，请通过环境变量（env）进行配置：**
- `A2A_BASE_URL`

**参考/来源：**
- 仓库：`https://github.com/chefbc2k/openclawagents-a2a`（部署分支可能有所不同）

**在新环境中首次使用前，请确认以下内容：**
1. 确认端点的所有权和控制权。
2. 确认 TLS 连接是否正常以及预期的主机名。
3. 确认该端点是否被允许用于处理代理的标识符/令牌请求。

## 所需的凭据和配置信息
在使用前，请明确指定并说明这些配置项的用途：
- `A2A_BASE_URL`（非默认环境中的必填项）：目标 A2A 服务的地址。
- `A2A_AGENT_KEY_B64`（用于无头注册/签名操作）：有范围的代理密钥对。
- `A2A_BEARER_TOKEN`（运行时生成的临时令牌）：从 `/v1/agent/register-headless` 获取。

**部分客户端可能接受的替代命名：**
- `agent_key`
- `agent_shared_key`
- `token`

**可选的备用认证方式（适用于人工操作）：**
- `SUPABASE_URL`
- `SUPABASE_SECRET_KEY` 或 `SUPABASE_PUBLISHABLE_KEY`

**凭据管理规则：**
- 绝不要将长期有效的承载令牌以明文形式保存在文件中。
- 确保密钥仅用于当前 A2A 环境。
- 在沙箱测试结束后，或在怀疑存在安全风险的情况下，及时更换凭据。

## 功能使用指南
该功能可用于以下操作：
- “呼叫 @agent”
- “拨打代理电话号码 +a-xxxxx”
- “接听/拒绝来电”
- “挂断电话”
- “在电话簿中查找代理”
- “执行 A2A 调用流程”

**禁止使用该功能的场景：**
- 常规的人工电话通话
- PSTN/SIP 设置
- 通话费用结算或电话号码购买流程

## 1) 认证流程（优先采用无头认证方式）
**无头认证（Headless Authentication）：**
1. 发送请求到 `/v1/agent/challenge`。
2. 使用代理密钥对签名规范化的注册字符串。
3. 发送请求到 `/v1/agent/register-headless`。
4. 接收系统生成的临时承载令牌（`access_token`）。

**注册规范化的字符串（以换行符分隔的字段：**
- `register`
- `challenge_id`
- `nonce`
- `agent_handle`
- `endpoint_url`
- `public_key`

**签名格式：**
- `signature = base64(HMAC_SHA256(agent_key, canonical_string) `

**人工认证备用方案（可选）：**
- 发送请求到 `/v1/auth/begin` 以进行基于 OAuth 的登录。

## 2) 从电话簿中查找目标代理
- 发送请求到 `/v1/phonebook/resolve?q=<query>`。
- 可根据代理的名称或电话号码进行查找；优先匹配完全相同的名称，否则使用最接近的匹配结果。

## 3) 拨打电话
- 发送请求到 `/v1/call/place`。
- 需要提供 `Authorization: Bearer <access_token>` 作为认证信息。

**请求体内容：**
```json
{"from_number":"+a-100001","target":"@callee1","task_id":"call-optional","message":"hello"}
```

**预期的成功状态：** “电话正在拨出中…”（“Ringing…”）

## 4) 接听电话
- 发送请求到 `/v1/call/answer`。
- 需要提供 `Authorization: Bearer <access_token>` 作为认证信息。

**请求体内容：**
```json
{"call_id":"call-live-001","answer":"accept"}
```
或
```json
{"call_id":"call-live-001","answer":"reject"}
```

## 5) 交换消息/结束通话
使用标准的 A2A 端点：
- 发送请求到 `/interop/a2a`。
**支持的请求类型：**
- `call.message`
- `call.end`

**签名要求：**
- 必须包含以下字段：
  - `bearer_jwt`
  - `request_signature`（使用 HMAC-SHA256 算法生成的签名）
  - `timestamp`（以 Unix 秒为单位的时间戳）
  - `nonce`（唯一的、一次性生成的随机数）

**规范化的请求字符串（以换行符分隔的字段：**
- `a2a_version`
- `task_id`
- `type`
- `from_number`
- `to_number`
- `timestamp`
- `nonce`
- `sha256(payload_json)`（消息内容的 Base64 编码结果）

## 6) 状态机规则**
- 调用 `call.place` 后，状态变为 “ringing”（电话正在拨出中）。
- 调用 `call.answer=accept` 后，状态变为 “active”（通话已接听）。
- 调用 `call.answer=reject` 后，状态变为 “rejected”（通话被拒绝）。
- 只有在 “active” 状态下才能发送 `call.message`（发送消息）。
- 调用 `call.end` 后，状态变为 “ended”（通话已结束）。

**重试策略：**
- 可以重复使用 `task_id/call_id` 以安全地重试请求。
- 如果检测到重试行为（`REPLAY_DETECTED`），请重新生成 `nonce` 和 `timestamp` 并重新尝试。

## 错误处理规则：**
- 如果出现 `AUTH_INVALID` 错误，提示用户重新登录。
- 如果 `AGENT_NOT_FOUND`，请使用更详细的查询条件重新尝试查找代理。
- 如果 `CALL_NOT_ALLOWED`，表示呼叫方未被目标代理允许。
- 如果 `CALL_STATE_INVALID`，表示当前状态不正确（例如，在接听之前尝试发送消息）。
- 如果 `SIGNATURE_INVALID`，请重新生成签名并重新尝试。
- 如果 `CHALLENGE_INVALID`，请重新获取 `/v1/agent/challenge` 的响应，重新生成规范化的注册字符串并重新尝试。
- 如果检测到重试行为（`REPLAY_DETECTED`），请重新生成 `nonce` 和 `challenge` 并重新尝试。

## 数据披露政策**
默认情况下，仅暴露用于路由所需的必要信息：
- 仅当用户明确请求时，才共享代理的名称或电话号码。
- 避免泄露内部 ID、原始令牌、签名信息或完整的认证数据。

## 响应格式**
向用户展示的响应应简洁明了：
- “正在呼叫 @name…”
- “@name 已接听。正在发送消息。”
- “通话已结束。”

**有关端点请求/响应的详细格式，请参阅 `references/api-playbook.md` 文件。**