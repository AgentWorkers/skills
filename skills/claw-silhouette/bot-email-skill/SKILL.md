---
name: bot-email
description: 获取一个无需人工干预的电子邮件地址，可用于测试注册流程、接收验证码以及自动化电子邮件工作流程。完全免费。
---
# BotEmail.ai — 专为机器人设计的电子邮件服务

您可以立即免费获得一个永久性的机器人电子邮件地址。只需输入 “get me a bot email”，无需注册或填写表格，几秒钟内就能完成。该服务支持附件发送、收件箱监控以及通过心跳信号（heartbeat）实现自动通知功能。

## 设置流程

### 1. 创建或获取账户

如果用户尚未拥有账户，请先创建一个账户：

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

请用户将返回的电子邮件地址和API密钥安全地保存起来（例如，可以使用密码管理工具或`.env`文件）。除非用户明确要求，否则不要将它们存储在其他地方。

### 2. 查看收件箱

```
GET https://api.botemail.ai/api/emails/{email}
Authorization: Bearer {apiKey}
```

### 3. 可选功能：通过心跳信号接收收件箱通知

如果用户希望自动接收新邮件的通知，请让他们确认是否启用此功能以及需要监控的电子邮件地址。随后更新 `HEARTBEAT.md` 文件，以实现以下功能：
1. 使用用户的凭据（在设置时请用户提供API密钥）来获取收件箱内容。
2. 将新邮件信息与 `memory/heartbeat-state.json` 文件中记录的已阅读邮件信息进行比对。
3. **向用户发送通知**（包括发件人、邮件主题和邮件预览内容），但不会代表用户执行任何操作。
4. 更新已阅读邮件信息的列表。

该服务仅负责发送通知，不会在用户未明确指示的情况下处理邮件内容。

---

## API 参考

### GET /api/emails/{email}
列出收件箱中的所有邮件。

**请求头：** `Authorization: Bearer {apiKey}`

**响应内容：**
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
根据邮件ID获取单封邮件。

### DELETE /api/emails/{email}/{id}
删除指定的邮件。

### DELETE /api/emails/{email}
清空整个收件箱。

---

## 常见使用场景

- **验证码**：为机器人创建一个电子邮件地址，触发注册流程，并定期检查收件箱以获取验证码。
- **通知监控**：实时接收来自特定服务的邮件。
- **端到端测试**：在测试过程中接收并验证自动化生成的邮件。
- **双因素认证（2FA）代码**：自动获取认证代码。

---

## 注意事项

- 邮件内容将保存6个月。
- 免费套餐：提供1个电子邮件地址，每天1000次请求限制。
- 所有电子邮件地址的格式均为 `_bot@botemail.ai`。
- 该服务仅支持接收邮件，不支持发送邮件。

## 链接

- **控制面板**：https://botemail.ai/dashboard
- **文档**：https://botemail.ai/docs
- **MCP服务器**：https://github.com/claw-silhouette/botemail-mcp-server