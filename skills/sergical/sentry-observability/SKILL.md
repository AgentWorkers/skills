---
name: sentry
description: "为您的 OpenClaw 实例添加可观测性功能：将错误信息、日志以及跟踪数据发送到 Sentry。通过 Sentry 插件设置监控机制，然后使用 `sentry` CLI 命令行工具来排查问题。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🐛",
        "requires": { "bins": ["sentry"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": "sentry",
              "global": true,
              "bins": ["sentry"],
              "label": "Install Sentry CLI (npm)",
            },
          ],
      },
  }
---
# Sentry — OpenClaw 可观测性

在 Sentry 中，您可以查看 OpenClaw 实例的运行情况：错误信息、结构化日志以及性能追踪数据。

整个流程分为两个部分：**设置**（配置数据传输）和**查询**（使用 CLI 进行数据查询）。

---

## 设置

### 1. 认证

```bash
sentry auth login
```

遵循浏览器提示完成 OAuth 认证流程。认证凭据存储在 `~/.sentry/cli.db` 文件中。

**替代方案（简短命令）：**
- `sentry auth login --token <TOKEN>` — 直接输入认证令牌
- `SENTRY_AUTH_TOKEN=<token>` — 环境变量，适用于持续集成（CI）场景

### 2. 创建项目

为您的 OpenClaw 实例创建一个专属的 Sentry 项目：

```bash
sentry api /teams/<org>/<team>/projects/ \
  --method POST \
  --field name="my-openclaw" \
  --field platform=node
```

如果您不知道组织的名称或团队名称，可以先列出所有可用的选项：

```bash
sentry api /organizations/                          # list orgs
sentry api /organizations/<org>/teams/              # list teams in org
```

### 3. 获取 DSN（数据源连接字符串）

```bash
sentry project view <org>/my-openclaw --json | jq -r '.dsn'
```

或者通过 API 端点获取 DSN：

```bash
sentry api /projects/<org>/my-openclaw/keys/ | jq '.[0].dsn.public'
```

### 4. 配置 OpenClaw

将 DSN 添加到 `openclaw.json` 文件中：

```json
{
  "plugins": {
    "entries": {
      "sentry": {
        "enabled": true,
        "config": {
          "dsn": "https://examplePublicKey@o0.ingest.sentry.io/0",
          "enableLogs": true
        }
      }
    }
  }
}
```

> **注意：** 配置信息应保存在 `plugins.entries.sentry.config` 文件中，而非直接放在 `sentry` 目录下。

接下来，需要安装 Sentry 插件。有关使用 `@sentry/node` 实现该插件的详细信息，请参阅 `references/plugin-setup.md`。

> **关于日志缓冲区：** Sentry 的结构化日志会在自动刷新前最多存储 100 条记录。对于像 OpenClaw 这样日志量较小的服务，日志可能会在缓冲区中停留较长时间。建议插件定期（例如每 30 秒）调用 `_INTERNAL_flushLogsBuffer(client)` 方法，并在程序关闭前执行 `Sentry.flush()`。具体实现方式请参考 `references/plugin-setup.md`。

### 5. 验证配置

重启 OpenClaw 服务，然后检查 Sentry 中是否有新的事件记录：

```bash
sentry issue list <org>/my-openclaw --limit 5
```

---

## 查询

一旦数据传输配置完成，您可以使用 CLI 查询 OpenClaw 的错误信息、性能追踪数据以及相关事件。

### 列出问题

```bash
sentry issue list <org>/<project>
sentry issue list <org>/<project> --query "is:unresolved" --sort freq --limit 20
sentry issue list <org>/                              # all projects in org
```

### 查看问题详情

```bash
sentry issue view <short-id>                          # e.g. MY-OPENCLAW-42
sentry issue view <short-id> --json                   # structured output
```

### 人工智能（AI）根本原因分析

```bash
sentry issue explain <issue-id>                       # Seer analyzes the root cause
sentry issue explain <issue-id> --force               # force fresh analysis
sentry issue plan <issue-id>                          # generate a fix plan (run explain first)
```

### 结构化日志

```bash
sentry log list <org>/<project>                       # last 100 logs
sentry log list <org>/<project> --limit 50            # last 50
sentry log list <org>/<project> -q 'level:error'      # filter by level
sentry log list <org>/<project> -q 'database'         # filter by message
sentry log list <org>/<project> -f                    # stream in real-time (2s poll)
sentry log list <org>/<project> -f 5                  # stream with 5s poll
sentry log list <org>/<project> --json                # structured output
```

### 查看特定日志条目

```bash
sentry log view <log-id>                              # 32-char hex ID
sentry log view <log-id> --json
sentry log view <log-id> --web                        # open in browser
```

### 检查事件详情

```bash
sentry event view <event-id>                          # full stack trace + context
sentry event view <event-id> --json
```

### 直接调用 Sentry API

```bash
sentry api /projects/<org>/<project>/issues/ --paginate
sentry api /issues/<id>/ --method PUT --field status=resolved
sentry api /issues/<id>/ --method PUT --field assignedTo="user@example.com"
```

### 处理错误的步骤：
1. `sentry issue list <org>/<project> --query "is:unresolved" --sort date --limit 5` — 列出未解决的问题
2. `sentry issue view <short-id>` — 查看问题详情、受影响用户及事件时间线
3. `sentry issue explain <issue-id>` — 查看问题的根本原因（通过 AI 分析）
4. `sentry issue plan <issue-id>` — 查看具体的修复步骤
5. 修复问题后：`sentry api /issues/<id>/ --method PUT --field status=resolved` — 更新问题状态为“已解决”

---

## 参考资料：
- 完整的 CLI 命令列表：`references/cli-commands.md`
- 插件实现文档：`references/plugin-setup.md`
- Sentry CLI 文档：https://cli.sentry.dev
- Sentry API 文档：https://docs.sentry.io/api/
- Node.js SDK 文档：https://docs.sentry.io/platforms/javascript/guides/node/