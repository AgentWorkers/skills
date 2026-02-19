---
name: email-webhook
description: 通过 JSON Webhook 接收传入的电子邮件，并触发代理程序的运行。专为 AI Commander 设计。
metadata: {"openclaw": {"requires": {"bins": ["node", "openclaw"], "env": ["WEBHOOK_SECRET"]}, "primaryEnv": "WEBHOOK_SECRET", "install": [{"id": "npm-deps", "kind": "node", "package": "express@4.21.2", "label": "Install Webhook dependencies"}]}}
---
# 电子邮件 Webhook 接收器

该功能提供了一个安全的端点，用于接收以标准化 JSON 格式发送的 Webhook 数据，并能自动唤醒代理程序（agent）。

## ⚡️ 唤醒机制

当收到电子邮件时，服务器会执行 `openclaw system event --mode now` 命令。这确保代理程序能够立即收到通知，并立即处理传入的通信内容，而无需等待下一次心跳周期。

## 🚨 安全性与隐私保护

### 命令注入防护
服务器使用 `child_process.spawn` 来安全地启动子进程，而非直接执行 shell 命令。用户提供的输入（如邮件头部信息）无法被用来执行任意系统命令。

### 路径遍历防护
`INBOX_FILE` 参数通过 `path.basename()` 函数进行清理处理，确保文件仅被写入服务器的工作目录内。

### 认证
服务器启动时必须设置一个强密码 `WEBHOOK_SECRET` 环境变量。所有传入的请求都必须在 `Authorization: Bearer <secret>` 头部中提供该密钥。

### 数据存储
- **本地收件箱**：收到的电子邮件（原始正文和元数据）会被追加到本地的 `inbox.jsonl` 文件中。
- **清理**：用户应定期更新或删除收件箱文件，以节省磁盘空间并保护隐私。

## 环境变量

| 变量 | 是否必填 | 默认值 | 说明 |
|---|---|---|---|
| `WEBHOOK_SECRET` | 是 | — | 用于 Webhook 认证的密钥。 |
| `PORT` | 否 | `19192` | 服务器监听的端口。 |
| `INBOX_FILE` | 否 | `inbox.jsonl` | 活动日志文件的名称。 |

## 设置步骤

1. **安装依赖项**：
   ```bash
   npm install express@4.21.2
   ```
2. **启动服务器**：
   ```bash
   WEBHOOK_SECRET=your-strong-token node scripts/webhook_server.js
   ```

## 运行时要求
需要安装 `express`、`node` 和 `openclaw` 命令行工具（CLI）。