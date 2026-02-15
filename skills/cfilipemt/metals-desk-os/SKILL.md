---
name: metals-desk-os
description: 专为XAU/USD和XAG/USD交易设计的机构级全自动化交易操作系统。该系统采用事件驱动、以风险控制为核心的设计理念，基于多引擎架构运行，作为OpenClaw交易代理中的持续分析与执行流程的一部分。
---

# Metals Desk OS

这是一个面向机构级用户的金属交易操作系统，专门用于黄金（XAU/USD）和白银（XAG/USD）的交易。该系统能够将OpenClaw交易代理升级为具备实时分析、自动执行、风险管理及交易绩效跟踪功能的全面交易辅助工具。

## 适用场景

- 分析黄金或白银的市场结构（采用ICT/SMC方法）
- 生成包含入场价、止损价（SL）和目标价（TP）的交易信号
- 通过MT5平台执行自动化或半自动化的交易
- 监控实时的风险状况、资金回撤情况以及持仓管理
- 追踪交易绩效（胜率、预期收益、夏普比率等指标）
- 获取与交易时段和宏观经济环境相关的交易决策支持

## 系统架构概述

该系统采用事件驱动的架构运行：

```
PRICE FEED → SESSION ENGINE → STRUCTURE ENGINE → LIQUIDITY ENGINE →
MACRO ENGINE → BIAS ENGINE → VOLATILITY ENGINE → RISK ENGINE →
EXECUTION ENGINE → BROKER → PERFORMANCE ENGINE → DASHBOARD → ALERTS
```

所有系统组件通过一个中央的**事件总线**（EventEmitter模式）进行通信，所有事件都会被记录下来，并可通过WebSocket实时监控。

## 核心组件

| 组件 | 功能 | 主要输出 |
|--------|---------|-------------|
| **结构分析引擎** | 检测市场中的重要价格点（HH/HL/LH/LL）、趋势反转点（BOS/CHoCH）、价格波动模式（FVG）及订单区块 | 市场结构、趋势方向及结构变化 |
| **流动性引擎** | 寻找价格等高点/低点、识别流动性聚集区及交易时段特征 | 流动性池信息及交易确认结果 |
| **趋势判断引擎** | 多时间框架下的趋势方向判断，并给出置信度评分 | 长期趋势（HTF）及日内趋势，置信度评分（0-100分） |
| **宏观经济引擎** | 监控美元指数（DXY）、10年期美国国债收益率及市场风险情绪 | 宏观趋势（牛市/熊市/中性），宏观风险等级 |
| **波动性引擎** | 计算平均真实范围（ATR），检测价格波动异常 | 波动性水平（低/正常/高/极端） |
| **风险控制引擎** | 确定交易头寸大小，监控资金回撤情况，并触发交易暂停机制 | 每笔交易的风险百分比及是否允许执行 |
| **执行引擎** | 结合所有组件的分析结果生成交易信号 | 完整的交易计划（包括入场价、止损价、目标价及头寸大小） |
| **绩效评估引擎** | 计算胜率、预期收益、夏普比率等绩效指标 | 综合交易绩效数据 |

## 系统运行模式

| 模式 | 名称 | 功能 |
|------|------|----------|
| 1 | **咨询模式** | 运行完整分析流程，生成交易信号，但不执行交易 |
| 2 | **半自动化模式** | 生成交易信号，并自动管理止损价和目标价 |
| 3 | **全自动模式** | 自动执行交易，包括开仓、止损、调整止损价及平仓 |
| 4 | **风险禁用模式** | 仅进行监控，不生成交易信号 |

模式设置可通过`data/state.json`文件或WebSocket命令进行调整。建议先从模式1开始进行系统验证。

## 不可更改的风险规则

以下风险规则由风险控制引擎严格执行，不可更改：
- **单笔交易的最大风险为2%** — 头寸大小 = （账户余额 × 风险百分比）/ 止损距离 |
- **每日累计风险敞口不得超过5%** |
- **连续亏损3次后，暂停当天的交易** |
- **市场波动剧烈时，自动减少交易头寸50%**（极端情况下减少75%） |
- **价差扩大时，禁止入场**（具体阈值因交易品种而异） |
- **高影响力新闻发布后20分钟内，禁止所有交易** |
- **账户资金回撤超过8%时，暂停交易直至手动恢复** |
- **如果API请求失败，取消交易，不得重试** |
- **与经纪商连接中断时，立即平仓所有头寸**

## 交易管理规则

- **目标价1.5R时，平仓40%的头寸** |
- **目标价2.5R时，平仓30%的头寸** |
- **目标价4.0R时，平仓剩余30%的头寸** |
- 所有交易记录均需保存在绩效数据中

## 入场条件

执行引擎生成交易信号的前提是必须满足以下所有条件：
- **趋势判断置信度≥65/100** |
- **系统组件间的匹配度评分≥0.6** |
- 确认流动性状况与市场趋势一致 |
- 当前交易时段为伦敦或纽约时段（优先选择） |
- 宏观风险处于较低或中等水平 |
- 价差在允许范围内 |
- 无影响交易的新闻事件 |
- 连续亏损次数不超过3次

## 文件结构

```
metals-desk-os/
├── SKILL.md                    # This file
├── index.js                    # Main orchestrator & entry point
├── package.json                # npm dependencies
├── skill.json                  # OpenClaw registration manifest
├── manifest.json               # Runtime configuration
├── core/                       # 8 trading engines
│   ├── structure-engine.js     # HH/HL/LH/LL, BOS, CHoCH, FVG, OB
│   ├── liquidity-engine.js     # Pools, sweeps, equal levels
│   ├── bias-engine.js          # MTF bias, conviction scoring
│   ├── macro-engine.js         # DXY, yields, sentiment, news
│   ├── volatility-engine.js    # ATR, regime, spikes
│   ├── risk-engine.js          # Position sizing, halts
│   ├── execution-engine.js     # Signal generation
│   └── performance-engine.js   # Metrics tracking
├── automation/                 # System automation layer
│   ├── event-bus.js            # Central event system
│   ├── price-feed.js           # MT5/MetaAPI price data
│   ├── session-engine.js       # London/NY/Asian sessions
│   ├── scheduler.js            # Cron tasks
│   └── news-monitor.js         # Economic calendar
├── broker/                     # MT5 broker integration
│   ├── mt5-connector.js        # Order execution via MetaAPI
│   ├── risk-guard.js           # Position monitoring & trailing
│   └── order-manager.js        # Order lifecycle management
├── dashboard/                  # Real-time monitoring
│   ├── websocket-feed.js       # WebSocket broadcaster (port 3078)
│   ├── desk-dashboard.json     # Widget layout config
│   └── metrics.json            # Metrics template
├── alerts/                     # Notification channels
│   ├── whatsapp-alert.js       # WhatsApp Business API
│   ├── telegram-alert.js       # Telegram Bot
│   └── risk-alert.js           # Centralized dispatcher
├── data/                       # Persistent state files
│   ├── state.json              # System mode & connections
│   ├── trade-log.json          # Trade history
│   ├── performance.json        # Performance metrics
│   └── bias-memory.json        # Bias state persistence
└── prompts/                    # AI agent prompts
    ├── system.txt              # Main system prompt
    ├── intraday.txt            # Intraday trading protocol
    ├── swing.txt               # Swing trading protocol
    └── execution.txt           # Execution protocol
```

## 安装说明

### 第一步：部署到OpenClaw

```bash
cp -r metals-desk-os/ ~/.openclaw/agents/trader/agent/metals-desk-os/
cd ~/.openclaw/agents/trader/agent/metals-desk-os/
```

### 第二步：安装依赖库

```bash
npm install
```

### 第三步：配置环境

在技能根目录下创建一个`.env`文件，设置以下环境变量：

```
# MetaAPI / MT5 Connection
METAAPI_TOKEN=your_metaapi_token_here
MT5_ACCOUNT_ID=your_mt5_account_id_here

# WhatsApp Business API (optional)
WHATSAPP_API_URL=https://graph.facebook.com/v18.0/YOUR_PHONE_NUMBER_ID/messages
WHATSAPP_TOKEN=your_whatsapp_token_here
WHATSAPP_PHONE=your_phone_number_with_country_code

# Telegram Bot (optional)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here

# News API (optional)
NEWS_API_KEY=

# AI Keys (optional, for enhanced analysis)
OPENROUTER_API_KEY=
ANTHROPIC_API_KEY=
```

- **MetaAPI**：在https://metaapi.cloud注册账户，并关联您的Fusion Markets MT5账户。
- **Telegram**：通过@BotFather创建机器人账户，获取聊天ID（来自@userinfobot）。
- **WhatsApp**：通过Meta Business API进行配置。

### 第四步：设置初始运行模式

编辑`data/state.json`文件，将`"mode"设置为1（咨询模式）以进行安全测试。

### 第五步：启动系统

```bash
# Direct
node index.js

# Or with PM2 for production
pm2 start index.js --name metals-desk-os
pm2 save
pm2 startup
```

## 仪表盘

通过WebSocket客户端连接到`ws://localhost:3078`，即可接收实时数据，包括：
- 实时价格和价差统计信息 |
- 长期及日内趋势判断结果及置信度评分 |
- 活跃头寸的实时盈亏情况 |
- 流动性分布图（价格等高点/低点信息） |
- 宏观经济指标（美元指数、收益率、新闻事件） |
- 综合绩效指标（胜率、预期收益、夏普比率） |
- 风险状态（交易暂停状态、每日盈亏情况） |
- 系统事件日志

## 警报格式

- **交易开启**：```
TRADE OPENED
Pair: XAUUSD
Direction: Long
Entry: 5024.50
SL: 5010.00
TP1: 5046.25
Risk: 1.5%
Session: London
Conviction: 82/100
```

- **交易暂停**：```
RISK HALT ACTIVATED
Reason: 3 consecutive losses
Trading paused for session
```

## 重要系统事件

事件总线会发布以下事件，外部系统可订阅这些事件：
- `price.update`：新的价格更新及蜡烛图数据 |
- `structure.shift`：检测到市场结构变化 |
- `liquidity.sweep`：流动性池更新 |
- `bias.update`：趋势判断结果更新 |
- `bias.flip`：长期趋势方向变化 |
- `execution.signal`：生成有效的交易信号 |
- `risk.halt` / `risk.resume`：交易暂停或恢复 |
- `order.filled` / `order.closed`：订单执行状态变化 |
- `performance.update`：新的交易记录到绩效数据 |
- `macro.news.block`：影响交易执行的新闻事件

## 验证步骤

在切换到更高级的模式（半自动化或全自动模式）之前，请确保以下功能正常运行：
1. 价格数据源能够提供实时或模拟的价格数据。
2. 结构分析引擎能够准确检测到价格波动点和趋势反转点。
3. 流动性引擎能够识别流动性聚集区。
4. 趋势判断引擎能够生成大于0的置信度评分。
5. 系统能够正确识别当前的交易时段。
6. 风险控制引擎能够验证各种交易场景。
7. 执行引擎能够生成包含完整交易计划的信号。
8. 警报能够通过配置的渠道发送。
9. WebSocket能够实时更新系统状态。

验证通过后，可依次尝试半自动化模式（模式2）和全自动模式（模式3），分别测试头寸管理和自动交易功能。