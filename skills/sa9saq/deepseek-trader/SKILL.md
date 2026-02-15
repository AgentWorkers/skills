---
description: 混合式加密分析方法：将技术指标与 DeepSeek AI 的推理能力相结合。
---

# DeepSeek Trader

这是一个结合了多种技术指标（RSI、MACD、SMA、Bollinger Bands）与DeepSeek AI技术的加密货币分析工具，用于生成买入/卖出/持有信号。

## 快速入门

```bash
cd {skill_dir}
npm install && npm run build

# Set API key securely (don't pass on command line — visible in `ps`)
export DEEPSEEK_API_KEY=your_key

# Analyze a coin
node dist/cli.js analyze --coin bitcoin

# Analyze multiple coins
node dist/cli.js analyze --coins bitcoin,ethereum,solana

# Trading signals only
node dist/cli.js signals --coin bitcoin
```

## 输出格式

```
🔍 BTC Analysis — ¥15,234,567

Technical Indicators:
| Indicator | Value | Signal |
|-----------|-------|--------|
| RSI       | 45.2  | Neutral |
| MACD      | +25   | Bullish |
| SMA 20/50 | Above | Bullish |
| Bollinger | Mid   | Neutral |

AI Signal: HOLD (72% confidence)
Risk: Medium
Action: Wait for RSI < 35 for entry
```

## 架构

```
CoinGecko → Price Data → Technical Indicators → DeepSeek API → Signal
```

## 安全性

- **切勿在命令行中传递API密钥**——请使用`export`命令或`.env`文件来存储密钥；
- 将`.env`文件添加到`.gitignore`列表中；
- API密钥仅会被发送到DeepSeek的API端点。

## 特殊情况处理

- **DeepSeek API不可用**：此时将切换为仅使用技术指标进行分析，不依赖AI结果；
- **CoinGecko的请求限制**：如果可用，将使用缓存的数据；同时会向用户发出警告；
- **指标信号冲突**：AI会综合多个指标的信号，并提供决策依据。

## ⚠️ 免责声明

本工具仅供信息参考或学习用途，不构成任何财务建议。请自行进行充分研究后再做出投资决策（DYOR：Do Your Own Research）。

## 配置参数

| 参数名 | 是否必填 | 说明 |
|----------|----------|-------------|
| `DEEPSEEK_API_KEY` | 是 | DeepSeek API密钥 |
| `COINGECKO_API` | 否 | CoinGecko的API基础URL（默认为免费层级） |

## 系统要求

- Node.js 18及以上版本；
- 拥有DeepSeek API密钥；
- 必须能够访问互联网。