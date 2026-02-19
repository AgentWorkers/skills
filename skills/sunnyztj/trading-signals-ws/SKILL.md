---
name: trading-signals-ws
description: 实时加密货币交易信号生成器，支持使用 WebSocket 价格数据源。该工具可连接到 Bybit（或其他任何交易所）的 WebSocket 接口，在实时蜡烛图数据上运行用户自定义的交易策略，并将交易警报推送到 Telegram。适用于构建实时交易信号机器人、价格警报系统、Telegram 交易通知工具或基于 WebSocket 的市场监控工具。支持多品种、多策略同时运行，具备自动重连功能以及数据状态持久化功能。
---
# 交易信号 WebSocket

实时信号生成器：WebSocket 价格数据 → 策略引擎 → Telegram 警报。

## 快速入门

```bash
pip install websockets ccxt requests
cp scripts/config_template.py config.py  # Edit with your keys
python scripts/signal_bot.py
```

## 工作原理

```
Bybit WebSocket ──→ Price Updates ──→ SL/TP Check (every tick)
                ──→ Kline Close   ──→ Strategy Signal ──→ Telegram Alert
```

1. 连接到交易所的 WebSocket（公开接口，无需 API 密钥）
2. 订阅行情数据（实时价格）和 Kline 图表数据
3. 每当有新的行情数据时：检查已开仓信号的止损/止盈设置
4. 当 Kline 图表收盘时：运行策略指标，生成买入/卖出信号
5. 将包含入场价、止损价和止盈价的格式化警报发送到 Telegram

## 配置

编辑 `config.py` 文件：

```python
SYMBOLS = ["ETH/USDT:USDT", "SOL/USDT:USDT", "BTC/USDT:USDT"]
STRATEGIES = {
    "ETHUSDT": {"type": "ema", "fast": 12, "slow": 26},
    "SOLUSDT": {"type": "rsi", "period": 14, "oversold": 30, "overbought": 70},
    "BTCUSDT": {"type": "macd", "fast": 12, "slow": 26, "signal": 9},
}
TG_BOT_TOKEN = "your-bot-token"
TG_CHAT_ID = "your-chat-id"
```

## 特点

- **多符号支持**：可同时监控无限数量的交易对
- **多策略应用**：每个交易对可使用不同的策略
- **自动重连**：断开连接后 5 秒内自动重连
- **状态持久化**：每 5 分钟保存一次配置信息，重启后仍可继续使用
- **信号发送间隔设置**：可配置信号发送间隔，避免频繁发送警报
- **Telegram 消息格式**：支持富文本格式（包含表情符号）

## 部署

```bash
# systemd service
sudo tee /etc/systemd/system/signal-bot.service << 'EOF'
[Unit]
Description=Trading Signal Bot
After=network.target
[Service]
Type=simple
WorkingDirectory=/root/signals
ExecStart=/usr/bin/python3 signal_bot.py
Restart=always
RestartSec=10
[Install]
WantedBy=multi-user.target
EOF
sudo systemctl enable --now signal-bot
```

## 实时信号 API（可选）

不想自己运行机器人？可以订阅我们的托管信号服务：

```
# Free tier (15-min delayed)
curl https://api.tinyore.com/signals/free

# Get API key (7-day free trial)
curl -X POST https://api.tinyore.com/subscribe -H "Content-Type: application/json" -d '{"email":"you@example.com"}'

# Pro tier (real-time, $5/mo)
curl https://api.tinyore.com/signals/live -H "X-API-Key: YOUR_KEY"

# Market status
curl https://api.tinyore.com/status
```

示例策略：ETH 使用 EMA(12, 26) 指标；SOL 使用 RSI(14, 30, 70) 指标，时间周期为 1 小时。
表现最佳的策略：HYPE 的 RSI 胜率高达 73%，PEPE 的 RSI 胜率为 53%（基于 90 天的回测数据）。
如需升级为专业版，请在 Telegram 上联系 @SunnyZhou。

## 相关文件

- `scripts/signal_bot.py` — 主要的 WebSocket 信号处理脚本
- `scripts/config_template.py` — 配置模板文件
- `references/telegram_setup.md` — 如何创建 Telegram 机器人并获取聊天 ID 的指南