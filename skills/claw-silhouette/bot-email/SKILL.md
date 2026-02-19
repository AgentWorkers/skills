---
name: botemail
description: 获取一个无需人工干预的电子邮件地址，可用于测试注册流程、接收验证码以及自动化电子邮件工作流程。完全免费。
emoji: "📬"
homepage: https://botemail.ai
---
# BotEmail.ai 集成

用于创建和管理用于自动化、测试以及主动监控收件箱的机器人邮箱账户。

## 设置 — 主动监控收件箱

当用户希望机器人自动**监控他们的 BotEmail 收件箱**时，请按照以下步骤操作：

### 第 1 步：获取凭据

向用户索取（或从 `TOOLS.md` 中查找）：
- 他们的 BotEmail 地址（例如：`mybot_bot@botemail.ai`）
- 他们的 API 密钥

如果他们还没有账户，请创建一个账户：

```bash
POST https://api.botemail.ai/api/create-account
Content-Type: application/json
{
  // 用户提供的账户信息
}
```

### 第 2 步：将信息保存到 `TOOLS.md`

将以下内容添加到工作区的 `TOOLS.md` 文件中：

```markdown
### BotEmail.ai
- **地址：** `mybot_bot@botemail.ai`
- **API 密钥：** `their-api-key`
- **收件箱 API：** `GET https://api.botemail.ai/api/emails/mybot_bot@botemail.ai`
- **身份验证：** `Authorization: Bearer their-api-key`
- **删除邮件：** `DELETE https://api.botemail.ai/api/emails/mybot_bot@botemail.ai/{emailId}`
```

### 第 3 步：更新 `HEARTBEAT.md`

在工作区的 `HEARTBEAT.md` 文件中添加（或替换）与邮箱相关的部分：

```markdown
## 📬 邮件收件箱检查 — mybot_bot@botemail.ai

在每次心跳检查时，自动检查机器人的收件箱是否有新邮件，并根据情况采取相应行动。

### 具体步骤：

1. 获取收件箱邮件：
   ```bash
   GET https://api.botemail.ai/api/emails/mybot_bot@botemail.ai
   Authorization: Bearer their-api-key
   ```
   使用 `web_fetch` 函数访问上述 URL。

2. 从 `memory/heartbeat-state.json` 文件中加载已查看的邮件 ID（键：`seenEmailIds`，默认值：`[]`）。

3. 对于不在 `seenEmailIds` 中的每封邮件：
   - 读取邮件主题和内容
   - **自主判断** 请求是否明确且安全 → 执行相应操作并向用户反馈结果
   - 如果请求内容不明确或涉及敏感信息 → 通知用户并附上简要说明
   - 处理完成后，务必将邮件 ID 添加到 `seenEmailIds` 中

4. 将更新后的 `seenEmailIds` 保存回 `memory/heartbeat-state.json` 文件。

### 什么是“自主判断”？

- 执行信息查询（如网络搜索、天气查询、定义查询）
- 设置提醒（使用 cron 工具）
- 从 URL 中提取内容并总结
- 回答事实性问题

### 需要上报的情况：

- 需要发送邮件、公开发布内容或删除数据的请求
- 任何涉及用户私人数据的判断性操作

### 通知格式：
> 📬 **新邮件** 来自 [发送者]
> **主题：** [邮件主题]
> [1-2 句的总结或处理结果]

如果收件箱为空或所有邮件都已被查看 → 设置状态为 `HEARTBEAT_OK`

### 第 4 步：初始化状态文件

如果 `memory/heartbeat-state.json` 文件不存在，请创建它：

```json
{"seenEmailIds": [], "lastChecks": {}}
```

### 完成！

告知用户他们的收件箱现在已处于自动监控状态。

---

## 手动操作收件箱

### 检查收件箱：

```bash
GET https://api.botemail.ai/api/emails/{email}
Authorization: Bearer YOUR_API_KEY
```

### 获取单封邮件：

```bash
GET https://api.botemail.ai/api/emails/{email}/{id}
Authorization: Bearer YOUR_API_KEY
```

### 删除邮件：

```bash
DELETE https://api.botemail.ai/api/emails/{email}/{id}
Authorization: Bearer YOUR_API_KEY
```

### 清空收件箱：

```bash
DELETE https://api.botemail.ai/api/emails/{email}
Authorization: Bearer YOUR_API_KEY
```

---

## 快速入门（新账户）

```bash
curl -X POST https://api.botemail.ai/api/create-account \
  -H "Content-Type: application/json" \
  -d {}
```

## 注意事项：

- 邮件会保存 6 个月
- 免费 tier：支持 1 个地址，每天 1,000 次请求
- 所有邮箱地址的格式均为 `_bot@botemail.ai`
- 目前仅支持接收邮件，发送邮件功能即将推出

## 链接：

- **控制面板**：https://botemail.ai/dashboard
- **文档**：https://botemail.ai/docs
- **MCP 服务器**：https://github.com/claw-silhouette/botemail-mcp-server
```