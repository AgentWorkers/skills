---
name: crisp
description: 通过 Crisp API 提供客户支持。当用户需要查看、阅读、搜索或回复 Crisp 收件箱中的消息时，请使用此方式。需要 Crisp 网站 ID 和插件令牌（通过环境变量 CRISP_WEBSITE_ID、CRISP_TOKEN_ID 和 CRISP_TOKEN_KEY 进行身份验证）。
---

# Crisp 客户支持平台

Crisp 是一个用于提供客户支持的平台。当用户需要执行以下操作时，可以使用该技能：
- 查看收件箱中的新消息
- 阅读对话记录
- 搜索对话内容
- 向客户发送回复
- 查看对话状态

## 认证信息

使用 Crisp 需要通过 HTTP 请求头进行身份验证，验证方式包括基本认证（Basic Auth），同时需要提供 API URL 所对应的网站 ID。

请将这些信息设置为环境变量（确保安全存储，切勿记录在日志中）：
- `CRISP_WEBSITE_ID` – 你的网站标识符（例如：`0f4c...`）
- `CRISP_TOKEN_ID` – 你的插件令牌标识符（例如：`e47d...`）
- `CRISP_TOKEN_KEY` – 你的插件令牌密钥（例如：`a7d7...`）

## 常见工作流程

### 查看收件箱状态
```bash
scripts/crisp.py inbox list --page 1
```

### 阅读对话记录
```bash
scripts/crisp.py conversation get <session_id>
```

### 获取对话中的消息
```bash
scripts/crisp.py messages get <session_id>
```

### 发送回复
```bash
scripts/crisp.py message send <session_id> "Your reply text here"
```

### 搜索对话记录
```bash
scripts/crisp.py conversations search "query terms" --filter unresolved --max 10
```

### 将消息标记为已读
```bash
scripts/crisp.py conversation read <session_id>
```

### 解决对话问题
```bash
scripts/crisp.py conversation resolve <session_id>
```

## API 参考

常用的 API 端点：
- `GET /v1/website/{website_id}/conversations/{page}` – 列出所有对话记录
- `GET /v1/website/{website_id}/conversation/{session_id}` – 获取特定对话的详细信息
- `GET /v1/website/{website_id}/conversation/{session_id}/messages` – 获取对话中的所有消息
- `POST /v1/website/{website_id}/conversation/{session_id}/message` – 向对话中发送新消息
- `PATCH /v1/website/{website_id}/conversation/{session_id}/read` – 将消息标记为已读
- `PATCH /v1/website/{website_id}/conversation/{session_id}` – 更新或解决对话问题

基础 URL：`https://api.crisp.chat`

## 注意事项

- 在向客户发送回复之前，请务必确认回复的语气和内容。
- 在对话记录中查找 `meta.email` 以获取客户的电子邮件地址。
- 在执行任何操作之前，请确保 `CRISP_WEBSITE_ID`、`CRISP_TOKEN_ID` 和 `CRISP_TOKEN_KEY` 已正确设置。
- 在通过脚本进行操作时，使用 `--json` 标志来获取 JSON 格式的输出。