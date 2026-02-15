---
name: crypto-price
description: 通过 CoinGecko API 或 Hyperliquid API 获取加密货币代币的价格，并生成蜡烛图。当用户请求代币价格、加密货币价格、价格图表或加密货币市场数据时，可以使用此功能。
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":["python3"]}}}
---

# 加密货币价格与图表

该脚本用于获取加密货币的价格并生成蜡烛图。

## 使用方法

执行脚本时，需要提供加密货币的符号以及可选的时间范围：

```bash
python3 {baseDir}/scripts/get_price_chart.py <SYMBOL> [duration]
```

**示例：**
- `python3 {baseDir}/scripts/get_price_chart.py HYPE`
- `python3 {baseDir}/scripts/get_price_chart.py HYPE 12h`
- `python3 {baseDir}/scripts/get_price_chart.py BTC 3h`
- `python3 {baseDir}/scripts/get_price_chart.py ETH 30m`
- `python3 {baseDir}/scripts/get_price_chart.py SOL 2d`

**时间范围格式：** `30m`（30分钟）、`3h`（3小时）、`12h`（12小时）、`24h`（默认值）、`2d`（2天）

## 输出结果

脚本返回以下内容的JSON格式数据：
- `price`：当前价格（单位：USD/USDT）
- `change_period_percent`：该时间段内的价格变化百分比
- `chart_path`：生成的PNG图表文件路径（如果有的话）
- `text/plain`：格式化的文本描述

**图表格式：**  
当 `chart_path` 存在时，图表将以图片形式输出。在回复中，需要以如下格式输出 `text/plain` 和 `chart_path`：
```
MEDIA: /tmp/crypto_chart_HYPE_1769204734.png
```
Clawdbot 会将此文件作为图片附件发送。**请勿** 使用 `[chart: path]` 或其他文本占位符，只需使用 `MEDIA: <chart_path>` 即可。

## 图表详情：
- **图表格式：** 蜡烛图（8x8像素的方形图表）
- **主题颜色：** 深色（背景颜色：#0f141c）
- **输出路径：** `/tmp/crypto_chart_{SYMBOL}_{timestamp}.png`

## 数据来源：**
1. **Hyperliquid API**：主要用于 HYPE 及其他 Hyperliquid 平台支持的加密货币
2. **CoinGecko API**：用于其他加密货币的备用数据源

价格数据会缓存 300 秒（5 分钟），缓存文件保存在 `/tmp/crypto_price_*.json` 目录中。