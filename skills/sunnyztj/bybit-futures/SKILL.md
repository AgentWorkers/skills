---
name: bybit-futures
description: 完整的Bybit USDT永续期货交易系统，具备风险管理、模拟交易和实时执行功能。适用于构建加密货币期货交易机器人、连接Bybit API、实现止损/止盈策略、管理杠杆和持仓规模、制定模拟交易策略、进行回测，或部署基于WebSocket的实时交易系统。该系统支持EMA交叉信号、RSI指标以及自定义策略模板。
---
# Bybit期货交易系统

为Bybit的USDT永续期货合约提供完整的交易基础设施。

## 快速入门

1. 安装依赖项：`pip install ccxt websockets numpy requests`
2. 将 `scripts/config_template.py` 复制到 `config.py`，并填写API密钥
3. 运行模拟交易：`python scripts/paper_trading_ws.py`
4. 验证通过后，切换到实盘交易：`python scripts/live_trading.py`

## 架构

```
config.py          ← API keys + risk parameters
risk_manager.py    ← Position sizing, daily loss limits, max positions
paper_trading_ws.py ← WebSocket real-time paper trading
live_trading.py    ← Live execution (same logic, real orders)
backtest.py        ← Historical backtesting engine
```

## 风险管理

所有交易都由 `risk_manager.py` 管理：
- **最大持仓量**：可配置的每笔交易占资本的比例（默认为20%）
- **最大杠杆**：可配置（默认为5倍）
- **止损**：每笔交易自动设置（默认为3%）
- **止盈**：每笔交易自动设置（默认为6%，盈亏比为2:1）
- **每日亏损限制**：当日亏损达到X%时停止交易（默认为10%）
- **最大同时持仓数量**：可配置（默认为3）

## 包含的交易策略

### EMA交叉（ETH）
- 当EMA(12)向上穿越EMA(26)时买入
- 当EMA(12)向下穿越EMA(26)时卖出
- 最适合的货币对：ETH/USDT，1小时时间框架

### RSI均值回归（SOL, HYPE, PEPE）
- 当RSI(14)从30以下向上穿越时买入
- 当RSI(14)从70以上向下穿越时卖出
- 最适合的货币对：SOL, HYPE（胜率为73%），1000PEPE（胜率为53%），1小时时间框架
- 回测结果：在90天的1小时数据上，HYPE策略盈利339美元，PEPE策略盈利210美元

### 自定义策略模板
请参阅 `references/custom_strategy.md` 以添加自己的交易策略。

## WebSocket实时引擎

模拟/实盘交易引擎使用Bybit的WebSocket v5 API：
- **行情订阅**：以毫秒级频率更新价格信息（用于止损/止盈）
- **K线订阅**：仅在蜡烛图收盘时计算交易信号
- **自动重连**：断开连接后5秒内自动重连
- **状态保存**：每5分钟将交易状态保存为JSON文件

## 部署建议

建议在VPS上使用systemd服务进行部署。

```bash
# Create service file
sudo tee /etc/systemd/system/paper-trading.service << 'EOF'
[Unit]
Description=Paper Trading Bot (WebSocket)
After=network.target

[Service]
Type=simple
WorkingDirectory=/root/trading
ExecStart=/usr/bin/python3 paper_trading_ws.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable --now paper-trading
```

## Telegram通知

系统支持通过Telegram发送实时通知，涵盖以下事件：
- 交易开仓/平仓
- 止损/止盈触发
- 每6小时生成交易总结报告
- 错误警报

请在配置文件中设置 `TG_BOT_TOKEN` 和 `TGCHAT_ID`。

## 文件目录

- `scripts/config_template.py` — 配置模板
- `scripts/risk_manager.py` — 风险管理模块
- `scripts/paper_trading_ws.py` — 模拟交易脚本
- `scripts/live_trading.py` — 实盘交易脚本
- `scripts/backtest.py` — 回测脚本
- `references/custom_strategy.md` — 自定义策略添加指南
- `references/bybit_api_notes.md` — Bybit API使用注意事项及技巧