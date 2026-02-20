---
name: agentkeys
description: 用于AI代理的安全凭证代理。通过AgentKeys进行API调用——真正的机密信息永远不会离开安全存储库。
metadata:
  openclaw:
    requires:
      env:
        - AGENTKEYS_PROXY_URL
    credentials:
      - name: AGENTKEYS_API_KEY
        description: "Workspace API key (starts with ak_ws_). Use with X-Credential-Name header to proxy by credential name."
        required: false
      - name: AGENTKEYS_PROXY_TOKEN
        description: "Direct proxy token for a single credential (starts with pxr_). Simpler but limited to one credential."
        required: false
---
# AgentKeys 技能

这是一个用于保护 AI 代理的安全凭证代理服务。所有 API 调用都会通过 AgentKeys 进行路由，因此代理程序永远不会接触到真实的凭证信息。

## 配置

您有两种配置方式：可以在环境中设置这些参数，或者将它们保存在 `.env` 文件中：

### 选项 A — API 密钥（推荐，支持多种凭证）

```
AGENTKEYS_API_KEY=ak_ws_...
AGENTKEYS_PROXY_URL=https://proxy.agentkeys.io
```

使用您的工作区 API 密钥来代理针对任意凭证的请求。您可以从 [设置](https://app.agentkeys.io/dashboard/settings) 获取 API 密钥。

### 选项 B — 直接代理令牌（仅支持单一凭证）

```
AGENTKEYS_PROXY_TOKEN=pxr_...
AGENTKEYS_PROXY_URL=https://proxy.agentkeys.io
```

使用代理令牌来访问特定的凭证。您可以在 [控制台](https://app.agentkeys.io) 为代理程序分配相应的凭证以获取代理令牌。

## 使用方法

### 使用 API 密钥（选项 A）——按凭证名称进行请求

```bash
curl -X POST $AGENTKEYS_PROXY_URL/v1/proxy \
  -H "Authorization: Bearer $AGENTKEYS_API_KEY" \
  -H "X-Credential-Name: resend" \
  -H "X-Target-Url: https://api.resend.com/emails" \
  -H "Content-Type: application/json" \
  -d '{"from": "noreply@example.com", "to": "user@example.com", "subject": "Hello", "text": "Sent via AgentKeys"}'
```

### 使用代理令牌（选项 B）——直接访问凭证

```bash
curl -X POST $AGENTKEYS_PROXY_URL/v1/proxy \
  -H "Authorization: Bearer $AGENTKEYS_PROXY_TOKEN" \
  -H "X-Target-Url: https://api.resend.com/emails" \
  -H "Content-Type: application/json" \
  -d '{"from": "noreply@example.com", "to": "user@example.com", "subject": "Hello", "text": "Sent via AgentKeys"}'
```

## 请求头

| 请求头 | 是否必需 | 说明 |
|--------|----------|-------------|
| `Authorization` | ✅ | `Bearer $AGENTKEYS_API_KEY` 或 `Bearer $AGENTKEYS_PROXY_TOKEN` |
| `X-Target-Url` | ✅ | 需要转发的目标 API 地址 |
| `X-Credential-Name` | ✅（仅适用于 API 密钥模式） | 要使用的凭证名称（不区分大小写） |
| `Content-Type` | ❌ | 该请求头不会被传递给目标 API |

## 工作原理

1. 代理程序使用 API 密钥和凭证名称（或代理令牌）向 AgentKeys 发送请求。
2. AgentKeys 在服务器端查找并解密真实的凭证信息。
3. 真实的凭证信息会被添加到请求头中。
4. 请求会被转发到目标 API。
5. 响应结果会返回给代理程序。
6. 所有请求都会被记录在审计日志中。

代理程序永远不会看到真实的 API 密钥、OAuth 令牌或密码。

## 支持的凭证类型

- API 密钥：以 `Authorization: Bearer <密钥>` 的形式添加到请求头中。
- 基本认证（Basic Auth）：以 `Authorization: Basic base64(用户名:密码)` 的形式添加到请求头中。
- 自定义请求头：以键值对的形式添加到请求头中。
- 查询参数：作为 URL 的查询参数添加。
- Cookies：以 `Cookie` 请求头的形式添加。
- OAuth 令牌：系统会自动更新令牌。

## 安全性

- 凭证信息在存储时采用 AES-256-GCM 加密算法进行加密。
- 代理令牌仅适用于特定的凭证和代理程序。
- 使用 API 密钥时，系统会尊重工作区的权限设置。
- 令牌可以在控制台随时被撤销。
- 所有代理请求都会被详细记录在审计日志中。
- 代理程序无法访问原始的凭证信息。

## 相关链接

- 控制台：[app.agentkeys.io](https://app.agentkeys.io)
- 文档：[agentkeys.io/docs](https://agentkeys.io/docs)
- 技术支持：support@agentkeys.io