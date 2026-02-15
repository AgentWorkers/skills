---
description: 通过 REST API 和 CLI，使用“批准/拒绝”工作流来管理待处理的操作（发布、部署等）。
---

# 审批队列

这是一个轻量级的审批队列系统，用于管理待处理的操作，例如 SNS 发布、部署任务和内容发布。只需轻轻一点即可完成批准或拒绝操作。

## 快速入门

```bash
cd {skill_dir}
npm install && npm run build

# Start API server
node dist/server.js --port 3010

# CLI usage
node dist/cli.js add --type sns_post --payload '{"text":"Hello world","platform":"twitter"}'
node dist/cli.js list --status pending
node dist/cli.js approve <item-id>
node dist/cli.js reject <item-id> --reason "Not appropriate"
```

## API 端点

| 方法 | 路径 | 描述 |
|--------|------|-------------|
| `GET` | `/api/queue` | 列出队列中的项目（过滤条件：`?status=pending&type=sns_post`） |
| `POST` | `/api/queue` | 添加项目到队列 |
| `POST` | `/api/queue/:id/approve` | 批准项目 |
| `POST` | `/api/queue/:id/reject` | 拒绝项目（请求体：`{"reason": "..."}`） |
| `GET` | `/api/queue/:id` | 获取项目详情 |
| `DELETE` | `/api/queue/:id` | 删除项目 |

## 队列项目结构

```json
{
  "id": "uuid",
  "type": "sns_post",
  "status": "pending",
  "payload": { "text": "Post content", "platform": "twitter" },
  "created_at": "2025-01-01T00:00:00Z",
  "reviewed_at": null,
  "reviewer_note": null
}
```

## 与 OpenClaw 的集成

```
Agent creates content → Adds to queue → Sends inline approval button → User taps → Action executes
```

## 安全性

- 在将数据加入队列之前，验证所有输入数据；拒绝格式错误的 JSON 数据。
- 对 `reviewer_note` 进行清理，以防止在用户界面中显示时发生注入攻击。
- 在生产环境中使用身份验证中间件（API 密钥或 JWT）。
- SQLite 数据库文件的权限应设置为 `chmod 600`。

## 配置参数

| 参数 | 默认值 | 描述 |
|----------|---------|-------------|
| `PORT` | 3010 | 服务器端口 |
| `DB_PATH` | `./data/queue.db` | SQLite 数据库文件路径 |
| `WEBHOOK_URL` | — | 批准/拒绝操作的回调 URL |

## 故障排除

- **端口冲突**：使用 `lsof -i :3010` 命令检查端口是否已被占用。
- **数据库锁定**：确保只有一个服务器进程可以访问 SQLite 文件。
- **Webhook 失败**：检查回调 URL 是否可访问；在生产环境中添加重试逻辑。

## 系统要求

- Node.js 18 及以上版本 |
- 不需要外部 API 密钥