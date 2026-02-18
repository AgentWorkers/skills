---
name: congress-trades
description: 使用 Quiver Quant API 实时追踪美国国会议员和政治家的股票交易记录。将交易数据同步到本地的 SQLite 数据库中，检测到金额超过 15,000 美元的重要交易时，会通过 OpenClaw 消息系统发送警报。该工具仅需要 Python 语言、requests 库以及一个名为 QUIVER_API_KEY 的环境变量即可使用。适用于设置国会交易监控系统、接收政治家股票交易警报、监控内幕交易行为，或追踪参议员和众议员的买卖行为。
---
# 国会交易追踪器

通过 Quiver Quant API 监控美国国会的股票交易记录，将数据存储到本地的 SQLite 数据库中，并在新发生的重要交易时发出警报。需要 Python 的 `requests` 库以及 Quiver Quant API 密钥。

## 要求

- Python 3.10 及以上版本，并已安装 `requests` 库（使用 `pip install requests` 安装）
- **QUIVER_API_KEY** 环境变量（请在 https://www.quiverquant.com/ 获取 API 密钥）

## 环境变量

| 变量 | 是否必需 | 默认值 | 说明 |
|---|---|---|---|
| QUIVER_API_KEY | 是 | — | Quiver Quant API 的访问令牌 |
| CONGRESS_DB_PATH | 否 | data/congress_trades.db | SQLite 数据库路径 |
| MIN_TRADE_AMOUNT | 否 | 15001 | 触发警报的最低交易金额 |

请将这些环境变量设置到您的 shell 配置文件（`.env`）或 cron 任务中。切勿在脚本中直接硬编码 API 密钥。

## 设置

### 1. 安装 Python 依赖项

```bash
pip install requests
```

### 2. 设置 API 密钥

```bash
export QUIVER_API_KEY="your-api-key-here"
```

### 3. 使用用户 cron 任务进行定时执行（无需 sudo）

将环境变量添加到 `~/.profile` 或 shell 会加载的 `.env` 文件中，然后添加 cron 任务：

```bash
crontab -e
# Add this line (uses env vars from your profile):
* * * * * . "$HOME/.profile" && /usr/bin/python3 /path/to/scripts/scraper.py >> /path/to/logs/scraper.log 2>&1
```

请勿在 crontab 任务中直接写入 API 密钥。

### 4. 配置 OpenClaw 警报接收

在 `HEARTBEAT.md` 文件中添加相关配置：

```markdown
## Check for congress trade alerts
- Read `congress_trades/data/pending_congress_alert.txt` — if it has content, send the alert to the user, then delete the file.
```

或者创建一个 OpenClaw cron 任务（每 5 分钟执行一次），以接收并转发警报。

## 工作原理

1. 该脚本每分钟运行一次，从 `api.quiverquant.com` 获取最新的 200 笔交易记录。
2. 将数据插入本地 SQLite 数据库，并通过 `trade_key` 进行去重处理。
3. 首次运行时初始化数据库并报告最新的交易记录。
4. 之后的运行会检测新的交易记录，筛选出金额超过设定阈值的买入/卖出交易。
5. 将格式化的警报信息写入 `data/pending_congress_alert.txt` 文件，以便 OpenClaw 接收。
6. 最后 50 条警报记录会保存在 `data/new_trades.json` 文件中。

## 网络与数据

- **仅进行出站连接**：`api.quiverquant.com`（Quiver Quant API）
- **数据存储**：本地 SQLite 文件及 `data/` 目录下的 JSON 格式警报文件
- **除 Quiver API 外，不使用任何外部接口**
- 限制 `data/` 目录的文件访问权限（使用 `chmod 700 data/`）

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
- **数据获取数量**：修改 `fetch_trades()` 函数中的 `limit=200` 以获取更多交易记录
- **cron 执行频率**：如需减少轮询频率，可将时间间隔设置为每 5 分钟或 15 分钟