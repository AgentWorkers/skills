# 密钥过期追踪器

该工具仅追踪 API 密钥、客户端密钥、证书的过期日期（元数据），并在这些密钥或证书过期前发出警报。

## 说明

Key Expiry Tracker 通过跟踪凭证（API 密钥、客户端密钥、证书）的过期日期来帮助您避免因凭证过期而导致的系统故障，并提前向您发出提醒。

**该工具从不存储、读取或传输任何凭证的详细信息**——您只需维护一个包含凭证标签和过期时间戳的本地 JSON 文件即可。

**运行成本：** 每次运行大约需要 200 至 500 个令牌（用于 cron 任务和简单的 JSON 解析）。

## 使用方法

### 添加新的凭证

编辑文件 `~/.openclaw/workspace/.credentials.json`：

```json
{
  "credentials": [
    {
      "name": "Azure OpenClaw Calendar",
      "type": "client-secret",
      "expires": "2026-03-15T00:00:00Z",
      "provider": "Microsoft Azure",
      "notes": "For M365 calendar integration"
    }
  ]
}
```

### 手动检查

```bash
~/.openclaw/workspace/skills/key-expiry-tracker/scripts/check-credentials.sh
```

### Cron 计划

每周日 10:00 自动运行检查：

```
cron add --name "key-expiry-tracker" \
  --schedule "0 10 * * 0" \
  --payload '{"kind":"systemEvent","text":"Run key-expiry-tracker weekly check"}' \
  --sessionTarget main
```

## 凭证类型

- `client-secret`：Azure AD、API 密钥
- `api-key`：第三方 API（如 OpenAI 等）的密钥
- `certificate`：SSL/TLS 证书
- `token`：OAuth 令牌、刷新令牌
- `password`：具有过期时间的密码

## 警报阈值

- **14 天**：警告（黄色）
- **7 天**：严重警告（红色）
- **已过期**：凭证已失效！

## JSON 数据结构

```json
{
  "credentials": [
    {
      "name": "string (required)",
      "type": "client-secret|api-key|certificate|token|password",
      "expires": "ISO-8601 timestamp (required)",
      "provider": "string (optional)",
      "renewed": "ISO-8601 timestamp (optional, last renewal)",
      "notes": "string (optional)"
    }
  ]
}
```