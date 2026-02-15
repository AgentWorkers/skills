# 信号生成器技能

该技能能够自动生成交易信号，并将警报发送到 Discord 或 Telegram。

## 📋 概述

该技能基于技术指标生成交易信号，并自动将警报发送到您配置的渠道（如 Discord、Telegram 等）。

## 🚀 主要功能

- **多种策略：**
  - **BB Breakout**（布林带突破）：布林带收窄后出现价格突破，并伴有成交量激增
  - **RSI 反转**：超买/超卖信号

- **支持多种时间框架**：可在 15 分钟、1 小时、4 小时等时间框架上运行

- **灵活的发送目标**：可以将警报发送到 Discord、Telegram 或任何 OpenClaw 渠道

- **简单配置**：仅需使用 JSON 格式进行配置，无需编写代码

## 📦 安装

1. 将技能目录复制到您的 OpenClaw 工作区：
```bash
cp -r signal-generator ~/.openclaw/workspace/skills/
```

2. 配置相关设置（详见下方“配置”部分）

3. 运行该技能：
```bash
cd ~/.openclaw/workspace/skills/signal-generator
python3 signal_generator.py
```

## ⚙️ 配置

将 `config.json.example` 复制到 `config.json` 文件中并编辑：

```json
{
  "symbol": "BTC/USDT",
  "strategy": "bb_breakout",
  "intervals": ["15m", "1h"],
  "targets": [
    "discord:your_channel_id",
    "telegram:your_chat_id"
  ],
  "filters": {
    "volume_spike": true,
    "trend_filter": false
  }
}
```

### 配置选项

| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `symbol` | 交易对（例如：BTC/USDT） | BTC/USDT |
| `strategy` | 策略：`bb_breakout` 或 `rsi_reversal` | `bb_breakout` |
| `intervals` | 需要检查的时间框架（例如：`["15m", "1h"]`） | `["15m", "1h"]` |
| `targets` | 警报发送的目标渠道 ID | [] |
| `filters.volume_spike` | 是否需要成交量激增作为信号生成条件 | `true` |
| `filters.trend_filter` | 是否应用趋势过滤（即将推出） | `false` |

## 🎯 策略

### BB Breakout（默认策略）

- **逻辑：**
  1. 检测到布林带收窄（布林带位于 Keltner 通道内）
  2. 价格突破布林带
  3. 成交量超过 20 个周期的平均值

- **买入信号：** 价格收盘价高于布林带上轨且成交量激增
- **卖出信号：** 价格收盘价低于布林带下轨且成交量激增

### RSI 反转

- **逻辑：**
  1. RSI 值低于 30（超卖）→ 买入信号
  2. RSI 值高于 70（超买）→ 卖出信号

- **买入信号：** RSI 值跌破 30 后再次上升
- **卖出信号：** RSI 值突破 70 后再次下降

## 📊 使用示例

### 手动运行

```bash
cd ~/.openclaw/workspace/skills/signal-generator
python3 signal_generator.py
```

### 定时运行

每 5 分钟运行一次：
```bash
*/5 * * * * cd ~/.openclaw/workspace/skills/signal-generator && python3 signal_generator.py
```

## 🔧 故障排除

**未生成信号？**
- 检查 `config.json` 文件是否存在且格式正确（为有效的 JSON）
- 确认交易对名称正确（例如：BTC/USDT，而非 BTCUSDT）
- 检查与 Binance 的 API 连接是否正常

**导入错误？**
- 确保 `quant-trading-bot` 可以正常访问：
```bash
ls /root/quant-trading-bot/src/exchange_api.py
```

## 📝 许可证

本技能按“原样”提供，使用风险自负。交易信号不构成任何财务建议。

## 🤝 贡献

如果您有新的策略想法，欢迎随时贡献！

---

**版本：** 1.0.0
**最后更新时间：** 2026-02-02