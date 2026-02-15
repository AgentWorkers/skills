---
name: openclaw-health-brief
description: 从 Oura、Whoop 和 Withings 生成每日健康报告。实现统一的重新认证脚本、本地令牌的持久化存储，以及每日早晨的健康状况总结（分为绿色、黄色和红色三个等级）。
---

# OpenClaw 健康概要

来自 **Oura**、**WHOOP** 和 **Withings** 的每日健康数据 → 标准化的 JSON 格式 + Markdown 说明。

## 设置（3 个步骤）

### 第一步：配置密钥

**选项 A：1Password（推荐）**
```bash
export OP_SERVICE_ACCOUNT_TOKEN="your-token"
export OPENCLAW_1P_VAULT="Assistant"  # or your vault name
```

在您的密码管理工具中创建以下条目：
- `OpenClaw Whoop` → `client_id`, `client_secret`, `token`, `refresh_token`
- `OpenClaw Oura` → `client_id`, `client_secret`, `token`, `refresh_token`
- `OpenClaw Withings` → `client_id`, `client_secret`, `access_token`, `refresh_token`, `user_id`

请参阅 `./docs/1PASSWORD_CONVENTIONS.md` 以获取完整的字段详情。

**选项 B：环境变量**
```bash
# WHOOP
export WHOOP_ACCESS_TOKEN="..." WHOOP_REFRESH_TOKEN="..." WHOOP_CLIENT_ID="..." WHOOP_CLIENT_SECRET="..."
# Oura
export OURA_PERSONAL_ACCESS_TOKEN="..."  # or OAuth: OURA_REFRESH_TOKEN + OURA_CLIENT_ID + OURA_CLIENT_SECRET
# Withings
export WITHINGS_CLIENT_ID="..." WITHINGS_CLIENT_SECRET="..." WITHINGS_REFRESH_TOKEN="..." WITHINGS_USER_ID="..."
```

### 第二步：授权服务提供商

```bash
python3 ./bin/health-reauth all
```

这将打开您的浏览器并引导您完成每个服务提供商的授权流程。点击“授权”按钮后，生成的令牌会自动保存到 1Password 以及 `~/.openclaw/secrets/health_tokens.json` 文件中。

您也可以单独重新授权：`python3 ./bin/health-reauth whoop`

### 第三步：运行首次健康概要报告

```bash
./bin/health-brief --date "$(date +%F)" --sources whoop,oura,withings --out "./out/daily_health_$(date +%F).json"
```

这样就完成了设置。令牌的更新会自动处理——新的令牌会保存在本地文件中，因此您无需再次进行授权。

## 将任务添加到 OpenClaw 定时任务中

将此任务设置为每天早晨运行的定时任务：

```bash
openclaw cron add \
  --name "morning-health-brief" \
  --schedule "0 8 * * *" \
  --tz "America/New_York" \
  --session-target isolated \
  --message 'Run the health brief:
source ~/.openclaw/secrets/gateway.env
export OPENCLAW_1P_VAULT=YourVault
./bin/health-brief --date "$(date +%F)" --sources whoop,oura,withings --out "/tmp/daily_health_$(date +%F).json"
Read the JSON output. Report only non-null metrics with a Green/Yellow/Red rating.'
```

定时任务会以独立会话的形式运行，执行健康概要报告的生成，读取结果，并将格式化后的摘要发送到您指定的渠道。

## 测试（无需输入凭据）

```bash
./bin/smoke
```

该测试以示例模式运行，用于验证 JSON 数据结构的正确性。这有助于确认技能安装是否成功。

## 故障排除

### 检查各个服务提供商的连接状态
```bash
./bin/whoop --date "$(date +%F)"
./bin/oura --date "$(date +%F)"
./bin/withings --date "$(date +%F)"
```

### 常见错误
- `has_token: false` → 未找到凭据。请检查 1Password 中的条目名称或环境变量设置。
- `refresh_failed` → 令牌已过期。请运行 `python3 ./bin/health-reauth <provider>` 重新授权。
- `missing_credentials` → `client_id` 或 `client_secret` 未设置。

### 验证输出 JSON 数据
```bash
./bin/validate-json --in ./out/daily_health_YYYY-MM-DD.json
```

## 参考资料
- `./docs/1PASSWORD_CONVENTIONS.md` — 1Password 中字段的命名规则
- `./docs/OURA.md`, `./docs/WHOOP.md`, `./docs/WITHINGS.md` — 各服务提供商的 API 使用说明
- `./docs/MORNING_BRIEF.md` — 早晨健康概要报告的用途和格式规范