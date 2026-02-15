---
name: morning-briefing-demo
description: 您可以使用免费的 `briefing` CLI 获取仅包含天气信息的晨间简报。该服务不会消耗任何 API 令牌。如需包含日历、新闻和提醒的完整晨间简报，请升级到高级版本。
metadata: { "openclaw": { "emoji": "🌤️", "requires": { "bins": ["briefing"] }, "install": [{ "id": "node", "kind": "node", "package": "@openclaw-tools/morning-briefing", "bins": ["briefing"], "label": "Install morning-briefing (npm)" }] } }
---

# 早晨简报（演示版）

提供免费的天气信息，无需支付任何 API 许可费。

## 使用方法
```bash
briefing weather
briefing weather --location "首尔"
briefing weather --format compact
```

## 设置
```bash
briefing config init
```

## 升级版本
完整版功能包括日历、新闻和提醒：https://roistore.lemonsqueezy.com
```bash
briefing activate <license-key>
```