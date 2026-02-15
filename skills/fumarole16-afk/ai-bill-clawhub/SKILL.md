---
name: ai-bill-intelligence
description: OpenClaw 提供实时 AI API 使用情况跟踪和成本监控功能。通过实时仪表板，您可以监控在 OpenAI、Claude、Geminii、Kimi、DeepSeek 和 Grok 等平台上的支出情况。该功能非常适合需要监控 AI API 成本、追踪令牌使用情况或管理多个 AI 提供商预算的用户。
version: 2.0.0
---

# AI 账单智能

这是一个用于 OpenClaw 的实时 AI API 使用情况跟踪和成本监控的仪表板。

## 快速入门

1. 安装该功能。
2. 在 `vault.json` 文件中配置您的 API 余额。
3. 启动相关服务：`systemctl start ai-bill ai-bill-collector`
4. 通过 `http://localhost:8003` 访问仪表板。

## 配置

编辑 `vault.json` 文件以设置初始余额：
```json
{
  "openai": 10.0,
  "claude": 20.0,
  "kimi": 15.0,
  "deepseek": 8.0,
  "grok": 10.0,
  "gemini": 0
}
```

## 服务

- **ai-bill.service**：Web 仪表板（端口 8003）
- **ai-bill-collector.service**：使用数据收集器（每 30 秒更新一次数据）

## 使用方法

收集器会自动读取 OpenClaw 的会话数据并实时计算费用。您可以通过仪表板查看以下信息：

- 按提供者划分的实时支出
- 剩余余额
- 令牌使用统计信息
- 费用趋势

## 定价

默认定价信息存储在 `prices.json` 文件中。请根据当前的 API 费率更新该文件。

## 故障排除

检查服务状态：
```bash
systemctl status ai-bill ai-bill-collector
```

查看收集器日志：
```bash
journalctl -u ai-bill-collector -f
```