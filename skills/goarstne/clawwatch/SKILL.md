---
name: clawwatch
description: >
  Crypto and stock price watchlist tracker. Use when the user asks about their watchlist,
  wants to add/remove assets to track, check prices, set price alerts, or get a market overview.
  Supports BTC, ETH, and all major crypto via CoinPaprika + stocks via Yahoo Finance.
  Also provides the Crypto Fear & Greed Index.
tools: Bash, Read
---

# ClawWatch — 监控列表功能

## 快速参考

| 用户输入... | 您执行... |
|---|---|
| “将比特币添加到监控列表中” | `clawwatch add BTC` |
| “添加NVIDIA和Tesla” | `clawwatch add NVDA TSLA --tag portfolio` |
| “我的监控列表情况如何？” | `clawwatch check --json` → 解析并汇总结果 |
| “只显示加密货币” | `clawwatch list --type crypto --json` |
| “当比特币价格超过10万美元时发出警报” | `clawwatch alert add BTC above 100000` |
| “当以太坊价格在一天内下跌5%时发出警报” | `clawwatch alert add ETH change 5` |
| “市场情绪如何？” | `clawwatch feargreed` |
| “删除TSLA” | `clawwatch remove TSLA` |
| “查看我的警报” | `clawwatch alert check --json` |
| “导出为CSV格式” | `clawwatch export --format csv` |

## 使用方法

1. 通过Bash工具运行命令：`bash clawwatch <命令>`
2. 使用`--json`标志获取机器可读的输出（便于解析）
3. 用自然语言向用户汇总结果
4. 如需深入分析，将JSON数据传递给市场分析师工具

## 重要规则

- **在需要程序化解析输出时，务必使用`--json`标志**
- **不要频繁运行`clawwatch check`——请遵守API速率限制（最多每60秒一次）**
- **自动识别**：只需输入符号（如`BTC`、`ETH`、`NVDA`、`SAP.DE`），工具会自动区分加密货币和股票
- **警报退出代码**：`clawwatch alert check`返回退出代码0（无警报）或1（警报触发）

## 与市场分析师工具结合使用

当用户要求进行分析（而不仅仅是获取价格信息时）：
1. 首先运行`clawwatch check --json`以获取当前价格
2. 将相关数据传递给市场分析师工具进行解读
3. 提供综合分析结果

## 读取缓存数据

您可以直接读取缓存的数据，而无需运行CLI命令：
- `~/.clawwatch/latest.json` — 最新获取的价格信息
- `~/.clawwatch/watchlist.json` — 完整的监控列表状态

## 安装

```bash
pip install clawwatch
# No API keys needed for crypto! Works out of the box.
# Optional: set CoinCap key for higher rate limits
clawwatch config --coincap-key YOUR_KEY  # optional
```