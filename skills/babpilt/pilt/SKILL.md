---
name: pilt
description: 访问Pilt的筹款数据——包括投资者匹配信息、活动统计数据、外联活动详情以及演示文稿分析结果。
metadata: {"openclaw":{"requires":{"env":["PILT_API_KEY"],"bins":["curl"]},"primaryEnv":"PILT_API_KEY","emoji":"🦞","homepage":"https://pilt.ai"}}
---
# Pilt API 技能

您可以使用 curl 从 Pilt 中检索筹款数据。所有请求都发送到一个统一的端点，并需要您的个人 API 密钥。

## 端点

```
POST https://pilt.ai/api/v1/gateway
```

## 必需的请求头

每个请求都必须包含以下两个请求头：

- `Content-Type: application/json`
- `x-pilt-api-key: $PILT_API_KEY`

## 安全性

所有的授权都通过您的个人 `x-pilt-api-key` 来完成。网关会在服务器端验证您的密钥，并为每个响应设置相应的权限范围。无需其他凭证。

## 请求体

请求体是一个 JSON 对象，其中必须包含 `action` 字段。支持的操作有：`get_matches`、`get_campaign_stats`、`get_campaign_events`、`get_analysis`。

## 操作说明

### get_matches

返回用户最新资料分析中匹配到的投资者及其匹配分数。

```bash
curl -s -X POST \
  https://pilt.ai/api/v1/gateway \
  -H "Content-Type: application/json" \
  -H "x-pilt-api-key: $PILT_API_KEY" \
  -d '{"action": "get_matches"}'
```

### get_campaign_stats

返回汇总的电子邮件推广统计数据：待发送、已发送、已打开和已回复的数量。

```bash
curl -s -X POST \
  https://pilt.ai/api/v1/gateway \
  -H "Content-Type: application/json" \
  -H "x-pilt-api-key: $PILT_API_KEY" \
  -d '{"action": "get_campaign_stats"}'
```

### get_campaign_events

返回每个投资者的事件日志（包含时间戳，例如发送、打开、回复等操作）。

```bash
curl -s -X POST \
  https://pilt.ai/api/v1/gateway \
  -H "Content-Type: application/json" \
  -H "x-pilt-api-key: $PILT_API_KEY" \
  -d '{"action": "get_campaign_events"}'
```

### get_analysis

返回资料分析的摘要：分数、行业、阶段以及简要说明。

```bash
curl -s -X POST \
  https://pilt.ai/api/v1/gateway \
  -H "Content-Type: application/json" \
  -H "x-pilt-api-key: $PILT_API_KEY" \
  -d '{"action": "get_analysis"}'
```

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 401 | 缺少或无效的 `x-pilt-api-key` 请求头（必须以 `pilt_sk_` 开头） |
| 403 | API 密钥未找到或已被吊销 |
| 400 | 缺少或不支持的 `action` 字段 |
| 413 | 请求体超过 10KB 的限制 |
| 503 | 服务器端尚未配置 API 网关 |

## 用户设置

将您的 Pilt API 密钥保存为 `PILT_API_KEY` 环境变量。在 OpenClaw 中，将其添加到 `~/.openclaw/openclaw.json` 文件中：

```json
{
  "skills": {
    "entries": {
      "pilt": {
        "enabled": true,
        "apiKey": "pilt_sk_..."
      }
    }
  }
}
```

您可以在 Pilt 的仪表板中，通过“设置” → “API 密钥”来生成 API 密钥。