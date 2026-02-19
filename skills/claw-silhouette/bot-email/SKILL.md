---
name: bot-email
description: 在 BotEmail.ai 上创建和管理机器人电子邮件账户。这些账户可用于测试注册流程、接收验证码、自动化电子邮件工作流程或监控传入的电子邮件。该服务支持账户创建、收件箱检查、电子邮件检索和删除功能。此外，还可以通过心跳（heartbeat）机制设置定期的收件箱通知功能。
---
# BotEmail.ai — 专为机器人设计的电子邮件服务

通过 JSON API，可以程序化地创建永久性的机器人电子邮件地址并管理收件箱。

## 设置

### 1. 创建或获取账户

如果用户还没有账户，请先创建一个：

```
POST https://api.botemail.ai/api/create-account
Content-Type: application/json

{}
```

返回结果：
```json
{ "email": "9423924_bot@botemail.ai", "apiKey": "..." }
```

自定义用户名：
```json
{ "username": "mybot" }
```

请用户将返回的电子邮件地址和 API 密钥安全地保存起来（例如，使用密码管理器或 `.env` 文件）。除非用户明确要求，否则不要将它们存储在其他地方。

### 2. 查看收件箱

```
GET https://api.botemail.ai/api/emails/{email}
Authorization: Bearer {apiKey}
```

### 3. 可选功能：通过心跳机制接收收件箱通知

如果用户希望自动接收新邮件的通知，请让他们确认是否启用此功能以及需要监控的电子邮件地址。然后更新 `HEARTBEAT.md` 文件，以实现以下功能：
1. 使用用户的凭据（在设置时请用户提供 API 密钥）获取收件箱内容。
2. 与 `memory/heartbeat-state.json` 文件中的已查看邮件 ID 进行比较。
3. **通知用户** 新邮件的相关信息（发送者、主题、邮件预览内容），但不会代表用户执行任何操作。
4. 更新已查看邮件 ID 的列表。

该服务仅负责通知用户，不会在用户未明确指示的情况下处理邮件内容。

---

## API 参考

### GET /api/emails/{email}
列出收件箱中的所有邮件。

**请求头：** `Authorization: Bearer {apiKey}`

**响应：**
```json
{
  "emails": [
    {
      "id": "abc123",
      "from": "sender@example.com",
      "subject": "Hello",
      "timestamp": "2026-02-17T12:00:00Z",
      "bodyText": "Hello!"
    }
  ]
}
```

### GET /api/emails/{email}/{id}
根据邮件 ID 获取单封邮件。

### DELETE /api/emails/{email}/{id}
删除指定的邮件。

### DELETE /api/emails/{email}
清空整个收件箱。

---

## 常见使用场景

- **验证码**：创建机器人邮箱地址，触发注册流程，并定期检查收件箱以获取验证码。
- **通知监控**：监控来自特定服务的邮件。
- **端到端测试**：在测试中接收并验证自动发送的邮件。
- **双因素认证代码**：自动获取认证代码。

---

## 注意事项

- 邮件会保存 6 个月。
- 免费套餐：支持 1 个邮箱地址，每天 1,000 次请求。
- 所有邮箱地址的格式均为 `_bot@botemail.ai`。
- 仅支持接收邮件，不支持发送邮件。

## 链接

- **控制面板**：https://botemail.ai/dashboard
- **文档**：https://botemail.ai/docs
- **MCP 服务器**：https://github.com/claw-silhouette/botemail-mcp-server