---
name: remix-api-key-auth
description: 配置并验证用于 Remix 代理发布工作流的 bearer API 密钥认证。
metadata:
  tags: remix, auth, api-key
---

# Remix API 密钥设置

当用户需要为 Remix 服务器的 API 验证外部服务/代理时，请使用此技能。

## 步骤

1. 登录您的 Remix 账户。
2. 访问 `https://remix.gg/api-keys`。
3. 创建一个新的 API 密钥。
4. 将该密钥作为机密信息存储在您的服务运行环境中。
5. 在请求头中添加以下内容：
   - `Authorization: Bearer <api_key>`
6. 使用基础 URL `https://api.remix.gg`。

## 验证

首先运行一个简单的认证请求（例如，在测试项目中发送 `POST /v1/agents/games`），以验证密钥是否有效。

## 解决无效 API 密钥的问题

- 确保 `Authorization` 的格式为 `Bearer <api_key>`。
- 从 `https://remix.gg/api-keys` 复制密钥，并在需要时更新它。
- 确认您的服务正在从运行环境中读取正确的机密信息（secret/env 变量）。
- 确保请求是在服务器端发起的，而不是通过浏览器代码执行的。
- 如果实际行为与本地文档不符，请以 `https://api.remix.gg/docs` 作为权威信息来源。