---
name: sentry
description: 为 OpenClaw 设置 Sentry 可观测性（安装插件、配置数据源连接（DSN）、使用 Sentry CLI 调查问题）。适用于为 OpenClaw 实例配置错误跟踪、跟踪信息或结构化日志，或在排查 Sentry 相关问题/错误时使用。
---
# OpenClaw 的 Sentry 可观测性（Sentry Observability for OpenClaw）

## 概述

本文档介绍了两个方面的内容：
1. 如何设置 `openclaw-plugin-sentry` 插件以实现错误/跟踪/日志的收集
2. 如何使用 Sentry 命令行界面（CLI）来排查问题

## 插件设置

### 安装

```bash
openclaw plugins install openclaw-plugin-sentry
```

### 配置

需要在 `openclaw.json` 文件中进行以下两项配置更改：
1. **启用诊断功能**（对于跟踪日志记录是必需的）：
```json
{ "diagnostics": { "enabled": true } }
```

2. **配置插件**：
```json
{
  "plugins": {
    "allow": ["sentry"],
    "entries": {
      "sentry": {
        "enabled": true,
        "config": {
          "dsn": "<your-sentry-dsn>",
          "environment": "production",
          "tracesSampleRate": 1.0,
          "enableLogs": true
        }
      }
    }
  }
}
```

插件配置文件位于 `plugins.entries.sentry.config` 中，而不是 `sentry` 的顶层配置文件中。

### 获取 DSN（数据源名称）

1. 进入 Sentry 的“项目设置”（Project Settings），然后选择“客户端密钥”（Client Keys）以获取 DSN。
2. 复制 DSN 的 URL（格式通常为 `https://key@o000000.ingest.us.sentry.io/0000000`）。

### 收集的数据类型

| 数据类型 | 来源 | Sentry 功能 |
|--------|--------|----------------|
| 错误（Errors） | 自动捕获的异常（如数据获取失败、AbortError 等） | 问题（Issues） |
| 跟踪（Traces） | `model_usage` 中的 `ai.chat` 跨度（spans）、`message.processed` 中的 `openclaw.message` 跨度 | 跟踪（Tracing） |
| 消息（Messages） | `webhook.error`、`session.stuck` | 问题（Issues） |
| 日志（Logs） | 通过 Gateway 日志传输到 `Sentry.logger` | 结构化日志（Structured Logs） |

### 验证插件是否正常工作

重启系统后，向您的机器人发送一条消息，然后检查日志是否被正确记录：
```bash
sentry issue list <org>/<project>        # Should see any errors
sentry event list <org>/<project>        # Should see events
```

或者通过 API 进行验证：
```bash
curl -s "https://sentry.io/api/0/organizations/<org>/events/?project=<project-id>&dataset=discover&field=id&field=title&field=event.type&field=timestamp&sort=-timestamp" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN"
```

## 使用 Sentry CLI 进行问题排查

### 身份验证设置

```bash
npm install -g sentry
sentry login
# Follow browser auth flow — stores config in ~/.sentry/cli.db
```

### 常用命令

```bash
# List issues for a project
sentry issue list <org>/<project>

# View issue details
sentry issue view <short-id>

# AI-powered root cause analysis
sentry issue explain <short-id>

# List recent events
sentry event list <org>/<project>

# Direct API calls
sentry api /organizations/<org>/projects/
```

### 通过 API 查看跟踪记录

跟踪记录无法直接在 CLI 中查看，需要使用 API 来获取：
```bash
SENTRY_TOKEN="..."
curl -s "https://sentry.io/api/0/organizations/<org>/events/?project=<id>&dataset=discover&per_page=10&sort=-timestamp&field=id&field=title&field=timestamp&field=transaction.duration&field=transaction.op&query=event.type:transaction" \
  -H "Authorization: Bearer $SENTRY_TOKEN"
```

## 故障排除

### 跟踪记录未显示

- 确认配置文件中的 `diagnostics.enabled` 是否设置为 `true`（该设置控制事件是否被记录）。
- 检查插件是否已成功加载：在 Gateway 日志中查找 `sentry: initialized` 的记录。
- 确保插件与 Gateway 使用相同的事件监听器：插件的 `onDiagnosticEvent` 方法必须使用与 Gateway 相同的监听器集合（OpenClaw 通过 `globalThis.__oc_diag` 来实现这一点）。

### 跟踪记录的持续时间显示为 0ms

- Sentry SDK v10 要求时间戳以毫秒（milliseconds）为单位。
- 该插件从诊断事件中获取 `evt.ts` 和 `evt.durationMs` 来记录持续时间。

### 插件无法加载

- 确保 `sentry` 在 `plugins.allow` 数组中。
- 确保 `openclaw.plugin.json` 文件中的 `configSchema` 配置包含 `additionalProperties: true`。
- 检查 Gateway 日志中是否有配置验证错误。

### 日志未显示

- 确保插件配置中的 `enableLogs` 设置为 `true`。
- 可能需要在 Sentry 项目设置中启用结构化日志功能。
- 使用 `Sentry.logger` API 时，确保使用的 Node.js 版本为 v10 或更高。