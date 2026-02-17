---
name: congress-trades
description: 使用 Quiver Quant API 实时跟踪美国国会议员的股票交易记录。该工具会自动将交易数据同步到 SQLite 数据库（无需任何外部依赖），检测出金额超过 15,000 美元的重要交易，并通过 OpenClaw 发送警报。使用该工具前需设置 QUIVER_API_KEY 环境变量。适用于设置国会议员交易监控系统、为政治人物提供股票交易警报，或进行内幕交易监控。
---
# 国会交易追踪器

通过 Quiver Quant API 监控美国国会的股票交易，将交易数据存储在 SQLite 数据库中（无需外部数据库），并在发生新的重大交易时发出警报。

## 要求

- Python 3.10 及以上版本，并安装 `requests` 库（使用 `pip install requests` 安装）
- **QUIVER_API_KEY** 环境变量（在 https://www.quiverquant.com/ 获取 API 密钥）

## 环境变量

| 变量 | 是否必需 | 默认值 | 说明 |
|---|---|---|---|
| QUIVER_API_KEY | 是 | — | Quiver Quant API 的访问令牌 |
| CONGRESS_DB_PATH | 否 | data/congress_trades.db | SQLite 数据库路径 |
| MIN_TRADE_AMOUNT | 否 | 15001 | 触发警报的最低交易金额 |

请将这些环境变量设置到您的 shell 配置文件（`.env`）或 cron 任务中。切勿在脚本中直接硬编码 API 密钥。

## 设置流程

### 1. 安装 Python 依赖项

```bash
pip install requests
```

### 2. 设置 API 密钥

```bash
export QUIVER_API_KEY="your-api-key-here"
```

### 3. 使用用户 cron 任务调度（无需 sudo 权限）

```bash
crontab -e
# Add this line:
* * * * * QUIVER_API_KEY="your-key" /usr/bin/python3 /path/to/scripts/scraper.py >> /path/to/logs/scraper.log 2>&1
```

### 4. 配置 OpenClaw 警报接收

在 `HEARTBEAT.md` 文件中添加以下内容：

```markdown
## Check for congress trade alerts
- Read `congress_trades/data/pending_congress_alert.txt` — if it has content, send the alert to the user, then delete the file.
```

或者创建一个 OpenClaw cron 任务（每 5 分钟执行一次），以便接收并处理警报。

## 工作原理

1. 该脚本每分钟运行一次，从 `api.quiverquant.com` 获取最新的 200 笔交易数据。
2. 将交易数据插入本地的 SQLite 数据库，并通过唯一的交易 ID 进行去重处理。
3. 首次运行时初始化数据库并报告最新的交易记录。
4. 之后的运行会检测新的交易，筛选出金额超过设定阈值的买入/卖出交易。
5. 将格式化的警报信息写入 `data/pending_congress_alert.txt` 文件，以便 OpenClaw 接收。
6. 最后 50 条警报会被保存在 `data/new_trades.json` 文件中。

## 网络与数据

- **仅进行出站连接**：`api.quiverquant.com`（Quiver Quant API）
- **数据存储**：本地 SQLite 文件以及 `data/` 目录下的 JSON 格式警报文件
- **除 Quiver API 外，不使用任何外部服务**
- 限制数据目录的文件访问权限（使用 `chmod 700 data/` 设置）

## 警报格式

```
🏛️ 3 new congress trade(s) detected:

🟢 PURCHASE: Nancy Pelosi (D) [Rep]
   $NVDA — $1,000,001 - $5,000,000
   Trade: 2026-02-10 | Reported: 2026-02-14

🔴 SALE: Dan Crenshaw (R) [Rep]
   $MSFT — $15,001 - $50,000
   Trade: 2026-02-09 | Reported: 2026-02-14
```

## 自定义设置

- **MIN_TRADE_AMOUNT**：通过环境变量调整警报触发金额的阈值
- **数据获取数量**：修改 `fetch_trades()` 函数中的 `limit=200` 参数，以获取更多交易数据
- **cron 执行频率**：如需减少请求频率，可将时间间隔设置为每 5 分钟或 15 分钟