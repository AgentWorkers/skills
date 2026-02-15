---
name: Upbit Trading Bot (A-Plan)
description: 这是一个由Cron定时触发、单次运行的自动化交易引擎，专为Upbit平台设计，并针对OpenClaw进行了优化。
version: 3.2.0
author: sgyeo
metadata:
  openclaw:
    runtime: nodejs
    entry: skill.js
    scheduler:
      cron: "*/5 * * * *"
      command: "node skill.js monitor_once"
---

# Upbit交易机器人（A-Plan）

这是一个专为OpenClaw环境设计的高可靠性自动化交易工具。它采用**单次运行执行模型（A-Plan）**进行操作，每次执行都会完成完整的市场扫描和交易流程后才会退出。

---

# 1. 概述

该工具具备以下功能：
- **单次运行调度**：每5分钟通过cron触发一次。
- **波动性突破策略**：根据每日价格范围的突破来识别入场时机。
- **状态感知执行**：使用独立的存储/键值对（KV）来管理持仓，以避免重复操作。
- **安全锁机制**：通过分布式锁机制防止多个cron任务同时执行。
- **严格的JSON输出格式**：输出单行JSON数据，便于日志记录和监控。

该工具还提供了仅用于执行的**查询命令**，以便OpenClaw能够回答用户的问题：
- 获取价格：`node skill.js price KRW-BTC`
- 查看持仓：`node skill.js holdings`
- 获取资产价值（韩元）：`node skill.js assets`

---

# 2. 执行流程（monitor_once）

当执行`node skill.js monitor_once`时：

1. **并发检查**：检查存储中是否存在`lock:monitor_once`键。如果存在有效的锁（且未过期），则直接退出。
2. **卖出评估**：
    - 从存储中加载所有处于“OPEN”状态的持仓。
    - 通过OpenClaw的`getTickers`函数获取当前价格。
    - 计算盈亏（PnL）。如果`PnL >= TARGET_PROFIT`或`PnL <= STOP_LOSS`，则执行卖出操作。
3. **买入扫描**：
    - 遍历`WATCHLIST`中的市场。
    - 通过OpenClaw的`getCandles`函数获取每日和每小时的价格数据。
    - 验证是否满足**波动性突破**（价格突破目标值）和**看涨条件**（当前价格高于开盘价）。
4. **买入执行**：
    - 进行风险检查（当前余额与预算的对比）。
    - 通过OpenClaw的`placeOrder`函数下达市场买入订单。
    - 将持仓状态更新为“OPEN”。
5. **终止**：以单行JSON格式输出执行总结（包括诊断日志），然后退出。

---

# 3. 存储/键值对（KV）结构

| 键        | 格式        | 用途                |
|------------|------------|-------------------|
| `lock:monitor_once` | JSON        | 用于并发控制的锁信息（包含`runId`和`ts`） |
| `positions:<market>` | JSON        | 持仓状态（`OPEN`、`FLAT`）以及买入价格和数量 |
| `cooldown:<market>` | JSON        | 防止快速再次买入的冷却时间（以秒为单位） |
| `active_markets` | Array       | 所有曾经进行交易的市场列表 |

---

# 4. 策略逻辑

### 入场条件（两个条件都必须满足）：
1. **价格突破**：`price > (today_open + (yesterday_high - yesterday_low) * K_VALUE)`
2. **看涨信号**：`current_price > hour_opening_price`

### 退出条件（满足任意一个条件即可）：
1. **获利平仓**：`PnL >= TARGET_PROFIT`（默认值：0.05 / 5%）
2. **止损**：`PnL <= STOP_LOSS`（默认值：-0.05 / -5%）

---

# 5. 环境变量

使用以下环境变量配置机器人：

| 变量        | 默认值       | 描述                |
|------------|------------|-------------------|
| `WATCHLIST`    | `KRW-BTC,KRW-ETH,KRW-SOL` | 以逗号分隔的市场代码 |
| `TARGET_PROFIT` | `0.05`      | 盈利目标比例           |
| `STOP_LOSS`    | `-0.05`      | 止损比例             |
| `K_VALUE`     | `0.5`      | 用于判断波动性的因子         |
| `BUDGET_KRW`    | `10000`      | 每笔买入订单的金额（韩元）       |
| `BUY_COOLDOWN_SEC` | `1800`      | 重新买入同一市场的冷却时间（秒）     |
| `LOCK_TTL_SEC`    | `120`      | 单次运行的最大锁持续时间（秒）     |

---

# 6. JSON输出格式

执行完成后，机器人会输出一行JSON数据：

```json
{
  "ok": true,
  "runId": "run_1707920000000",
  "actions": [
    { "type": "BUY", "market": "KRW-BTC", "result": "SUCCESS" }
  ],
  "errors": [],
  "logs": [
    { "level": "INFO", "message": "Signal: BUY KRW-BTC breakout detected" }
  ],
  "timestamp": "2026-02-14T23:30:00Z"
}
```

---

# 7. 目录结构

```
skill.js                # CLI Entrypoint & Runner
handlers/
  monitorOnce.js        # Main A-Plan Orchestrator
repo/
  positionsRepo.js      # Storage/KV Abstraction
domain/
  strategies.js         # Strategy Math (Pure)
  riskManager.js        # Balance & Order Validation
adapters/
  execution.js          # OpenClaw Tool Interface
services/
  orderService.js       # Trade Execution logic
utils/
  log.js                # In-memory log buffer (NO stdout)
  time.js               # Time & Config Utilities
```