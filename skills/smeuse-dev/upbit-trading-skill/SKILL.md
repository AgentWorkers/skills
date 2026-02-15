---
name: upbit-trading
version: 1.0.0
description: Upbit 实时交易机器人 - 利用 GLM 人工智能进行分析，结合技术指标实现自动交易
author: smeuseBot
price: 29.99
tags: [trading, crypto, upbit, automation, korean]
---

# Upbit 交易机器人 🚀

基于 AI 的实时加密货币交易机器人

## 主要功能

- 📊 **技术指标**: RSI、MACD、Bollinger Bands、MA/EMA
- 🤖 **AI 分析**: 使用 GLM-4.7 进行实时市场分析
- ⚡ **10 秒监控**: 快速检查价格变化
- 🎯 **自动设置目标价/止损**: 可自定义止盈/止损价格
- 📱 **Telegram 通知**: 实时事件提醒

## 设置步骤

1. 申请 Upbit API 密钥（https://upbit.com/mypage/open_api_management）
2. 设置环境变量：

```bash
cp .env.example .env
# UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY 입력
```

3. 运行机器人：
```bash
node realtime-bot.js
```

## 系统要求

- Node.js 18 及以上版本
- Upbit 账户及 API 密钥
- （可选）用于 AI 分析的 GLM API 密钥

## 文件结构

- `realtime-bot.js`：主交易机器人脚本
- `indicators.js`：技术指标计算模块
- `analyze.js`：市场分析模块
- `balance.js`：账户余额查询模块

## 许可证

MIT 许可证 - 可自由使用和修改