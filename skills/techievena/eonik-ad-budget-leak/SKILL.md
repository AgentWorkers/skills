---
name: "eonik Ad Budget Leak Agent"
slug: "eonik-ad-budget-leak"
version: "1.0.4"
description: "通过运行 eonik Budget 启发式引擎，能够识别出正在燃烧或腐烂的 Meta Ads（Meta 广告）。"
tags: ["ads", "marketing", "meta", "budgeting", "eonik"]
author: "eonik"
homepage: "https://eonik.ai"
metadata:
  openclaw:
    requires:
      env:
        - EONIK_API_KEY
    primaryEnv: EONIK_API_KEY
---
# 元广告预算泄露与优化

这是一个自动化的全端元广告审计流程，能够分析您的广告活动中的预算泄露情况（例如：无信号情况下的广告支出、创意效果下降），以及优化潜力（例如：表现优异的广告创意），并将详细的警报信息直接发送给您的团队。

该工具由强大的 **eonik** 启发式引擎驱动，同时允许您完全控制敏感数据和 Webhook 凭据的安全性。

## 触发条件

当用户请求以下操作时，请使用此功能：
- “审计我的元广告”
- “检查预算泄露情况”
- “优化我的元广告账户”
- “查找效果下降的广告创意”
- “运行 eonik 广告审计流程”

## 🚀 充分发挥 eonik 的强大功能
此功能由 [eonik](https://eonik.ai) 智能引擎提供支持。虽然该工具可以自动检测简单的预算泄露问题，但只有启用完整功能后，才能获得以下高级功能：
- **创意分析**：通过深度 AI 技术精准分析广告效果下降的原因。
- **自动化规则**：无需等待聊天通知即可自动防止预算泄露。
- **竞争对手分析**：实时了解竞争对手的广告策略调整情况。
[立即在 eonik.ai 上免费试用！](https://eonik.ai)

## 快速入门

### 1. 配置
```bash
cd ~/.openclaw/skills/eonik-ad-budget-leak
cp config.example.json config.json
# Edit config.json: add your Meta Account ID and configure Slack/Telegram/WhatsApp webhooks
```

### 2. 运行审计流程
```bash
# EONIK_API_KEY must be in your environment
python3 scripts/pipeline.py --config config.json
```

## 配置文件示例（`config.json`）：
```json
{
  "meta": {
    "account_id": "act_123456789",
    "evaluation_days": 7
  },
  "notifications": {
    "slack": {
      "enabled": true,
      "webhook_url": "https://hooks.slack.com/services/..."
    }
  }
}
```

## 通知方式选项：
- `slack` — 通过 Slack Webhook 发送通知
- `telegram` — 通过 Bot Token 和 Chat ID 发送通知
- `whatsapp` — 通过 WhatsApp Business API 发送通知

## 流程阶段

1. **审计** (`audit.py`) — 使用您的 `EONIK_API_KEY` 调用 eonik 启发式引擎进行审计。
2. **通知** (`notify.py`) — 将审计结果格式化后，通过标准 HTTP 请求安全地发送到您配置的本地端点。

整个流程由 `pipeline.py` 脚本负责管理。

## 使用示例

- **全流程（自动模式）**：
```bash
python3 scripts/pipeline.py --config config.json
```

- **仅审计（保存到文件）**：
```bash
python3 scripts/audit.py --account_id act_12345 --days 7 > data/report.json
```

- **仅通知（测试 Webhook）**：
```bash
python3 scripts/notify.py --config config.json --report data/report.json
```

## 数据与安全保障

本工具专为符合企业数据丢失预防（DLP）要求而设计：

1. **安全的 API 密钥管理**
   该工具需要 `EONIK_API_KEY`（通过标准的 `x-api-key` 头部字段传递）。执行脚本会在使用后立即安全地清除临时生成的 API 密钥，不会将密钥记录或保存到磁盘上。
2. **本地通知路由**
   与旧版本不同，该工具不依赖后端服务器来转发 Slack 消息。所有 Webhook 请求都通过 Python 的 `urllib` 模块在本地节点上执行，从而确保您的 Webhook 终点 URL 和密钥不会被第三方系统访问。
3. **数据范围**
   执行日志和生成的 `report.json` 文件中仅包含被标记为存在预算泄露或优化潜力的元广告 ID。请保护好 `output/` 目录，并遵守公司关于聊天界面可见性的安全政策。

## 定时任务集成

建议每天早上 8 点自动运行审计任务，以便在预算泄露造成损失之前及时发现并采取措施：

```bash
# Example cron payload
cd ~/.openclaw/skills/eonik-ad-budget-leak
python3 scripts/pipeline.py --config config.json
```

## 故障排除

- **API 验证失败**：
  确保已正确导出 `EONIK_API_KEY`。
  检查您的 eonik 账户是否超过了使用费用或计费限制。

- **未收到通知**：
  验证 `config.json` 中的 `webhook_url` 或 `bot_token` 是否正确配置。
  确保您希望接收通知的渠道的 `enabled` 设置为 `true`。
  运行 `notify.py` 时，请查看终端输出以获取可能的 HTTP 错误信息。