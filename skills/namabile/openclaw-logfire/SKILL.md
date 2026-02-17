---
name: openclaw-logfire
description: Pydantic 与 Logfire 的可观测性集成：OTEL GenAI 跟踪功能、工具调用时间跨度、令牌指标以及分布式追踪系统
version: 0.1.2
homepage: https://github.com/Ultrathink-Solutions/openclaw-logfire
metadata:
  openclaw:
    primaryEnv: LOGFIRE_TOKEN
    requires:
      env:
        - LOGFIRE_TOKEN
---
# OpenClaw Logfire 插件

这是一个为 OpenClaw 开发的 Pydantic [Logfire](https://pydantic.dev/logfire) 可观测性插件。该插件使用 [OTEL GenAI 语义规范](https://opentelemetry.io/docs/specs/semconv/gen-ai/) 来追踪代理的完整生命周期，包括工具调用、令牌使用情况、错误信息以及跨服务的分布式追踪数据。

## 安装

```bash
openclaw plugins install @ultrathink-solutions/openclaw-logfire
```

设置您的 Logfire 写入令牌：

```bash
export LOGFIRE_TOKEN="your-token"
```

将插件配置添加到 `openclaw.json` 文件中：

```json
{
  "plugins": {
    "entries": {
      "openclaw-logfire": {
        "enabled": true,
        "config": {}
      }
    }
  }
}
```

重启 OpenClaw，之后追踪数据将显示在 Logfire 仪表板上。

## 支持的追踪内容

每次代理调用都会生成一个追踪树（span tree）：

```
invoke_agent chief-of-staff          (root span)
  |-- execute_tool Read              (file read)
  |-- execute_tool exec              (shell command)
  |-- execute_tool Write             (file write)
```

这些追踪数据遵循 OTEL GenAI 语义规范，包括以下字段：`gen_ai.agent.name`、`gen_ai.tool.name`、`gen_ai_usage.input_tokens`、`gen_ai_usage.output_tokens` 等。

## 监控指标

- `gen_ai.client.token_usage`：令牌使用情况（输入/输出）
- `gen_ai.client.operation.duration`：代理调用耗时

## 主要配置参数

| 参数 | 默认值 | 说明 |
|---------|---------|-------------|
| `environment` | `development` | 部署环境标签 |
| `serviceName` | `openclaw-agent` | OTEL 服务名称 |
| `providerName` | — | GenAI 提供商（例如 `anthropic`） |
| `captureToolInput` | `true` | 记录工具参数 |
| `redactSecrets` | `true` | 移除 API 密钥和 JWT 信息 |
| `distributedTracing.enabled` | `false` | 是否启用 W3C traceparent 传播功能 |

## 安全性与隐私设置

- **秘密信息保护**（默认启用）：在导出数据前会移除 API 密钥、平台令牌、JWT 以及凭证信息。
- **工具输出** 默认不被记录（`captureToolOutput: false`）。
- **消息内容** 默认不被记录（`captureMessageContent: false`）。
- **数据传输方式**：追踪数据通过 OTLP HTTP 协议传输到 Pydantic Logfire（美国或欧盟地区），不会访问其他外部端点。
- **无本地数据存储**：所有数据均实时传输至 Logfire，不会保存到本地磁盘。

## 外部端点

| 端点地址 | 发送的数据 |
|-----|-----------|
| `https://logfire-api.pydantic.dev`（美国） | OTLP 追踪数据及指标 |
| `https://logfire-api-eu.pydantic.dev`（欧盟） | OTLP 追踪数据及指标 |

仅当您信任这些数据传输目的地时，才建议安装此插件。

## 链接

- [GitHub 仓库](https://github.com/Ultrathink-Solutions/openclaw-logfire) |
- [npm 包页](https://www.npmjs.com/package/@ultrathink-solutions/openclaw-logfire) |
- [Logfire 官方文档](https://pydantic.dev/logfire) |
- [博客文章：将 OpenClaw 应用于生产环境](https://ultrathinksolutions.com/the-signal/openclaw-to-production/)