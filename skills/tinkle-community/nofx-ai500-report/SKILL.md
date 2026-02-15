---
name: nofx-ai500-report
description: 从 NOFX AI500 系统生成定期的加密货币市场情报报告。该系统会监控选定的加密货币、分析未平仓合约（OI，Open Interest）、机构资金流动、K线技术指标、Delta 值、多头/空头比率以及资金费率。这些报告可用于生成自动化的加密货币市场报告、AI500 信号监控、新加密货币提醒，或通过 Telegram/消息服务发送定期的交易信号摘要。
---

# NOFX AI500 报告功能

该功能能够利用 NOFX AI500 评分系统生成全面的加密货币市场情报报告，并实现自动监控和报告发送。

## 先决条件

- 需要访问 NOFX API：包括基础 URL 和 API 密钥（由用户提供）
- 需要一个用于接收报告的 Telegram 聊天频道或消息传递工具
- 使用 Python 3 编程语言，并安装 `ssl`、`json`、`urllib` 等标准库

## 设置流程

向用户索取以下信息：
1. **NOFX API 基础 URL**（例如：`https://nofxos.ai`）
2. **API 密钥**（例如：`cm_xxxx`）
3. **报告发送目标**：Telegram 聊天 ID 或频道

随后，使用 OpenClaw 的 cron 工具创建两个定时任务：

### 任务 1：新币种监控（每 15 分钟执行一次）

运行 `scripts/monitor.sh` 脚本，并将 API 基础 URL 和密钥作为环境变量传递：
- 如果输出 `NEW:`，则表示有新币种被添加，系统会发送警报并附上详细分析；
- 如果输出 `REMOVED:`，则表示该币种已被移除；
- 如果输出 `NO_CHANGE`，则表示没有变化，系统将不执行任何操作。

完整的 cron 任务模板请参见 `references/monitor-job.md`。

### 任务 2：定期报告（每 30 分钟执行一次）

从多个 NOFX API 端点以及 Binance 的公共 API 中获取数据，并将这些数据整理成格式化的报告。

完整的 cron 任务模板请参见 `references/report-job.md`。

## API 端点说明

所有 NOFX API 端点都需要添加 `?auth=KEY` 参数。

| 端点            | 功能                        | 参数                                      |
|------------------|----------------------------------|----------------------------------------|
| `/api/ai500/list`     | 获取当前的 AI500 评分结果                |                                        |
| `/api/oi/top-ranking`    | 获取 OI（Open Interest）排名变化            | `duration`                                  |
| `/api/oi/low-ranking`    | 获取 OI 排名下降的币种                | `duration`                                  |
| `/api/netflow/top-ranking`   | 获取资金流入排名                  | `type=institution&trade=future&duration`                |
| `/api/netflow/low-ranking`   | 获取资金流出排名                  | same                                      |
| `/api/delta/list`     | 获取价格波动数据                    | `symbol`                                    |
| `/api/long-short-ratio/list` | 获取多头/空头比率                  | `symbol`                                    |
| `/api/funding-rate/top-ranking` | 获取资金费率排名                  |                                          |
| `/api/funding-rate/low-ranking` | 获取资金费率排名（较低水平）                |                                          |

`duration` 的取值范围：`5m`、`15m`、`30m`、`1h`、`4h`、`8h`、`24h`

Binance 的 K 线数据（公开可用，无需认证）：
```
https://fapi.binance.com/fapi/v1/klines?symbol=XXXUSDT&interval=15m&limit=10
```

**SSL 注意事项**：在某些系统中，Python 可能需要额外的 SSL 配置：
```python
import ssl
ctx = ssl._create_unverified_context()
```

## 报告格式

为了确保报告在 Telegram 上正常显示，代码块中使用了 Unicode 格式的图表绘制。每个币种的报告内容包括：

1. **AI500 评分** 以及自被纳入评分以来的累计回报
2. 在 7 个时间周期（5 分钟至 24 小时）内的 OI 变化情况
3. 不同时间周期内的机构资金流入情况（包括排名信息，分为前 20 名）
4. K 线分析结果（15 分钟/1 小时/4 小时）：趋势方向、多头/空头蜡烛数量比例、MA3 与 MA7 的对比、成交量变化、支撑位/阻力位
5. 资金费率（若超过 0.03%，会显示警告）

每个币种的报告还包括以下内容：
- OI 排名表（过去 1 小时/4 小时/24 小时内排名上升/下降的币种）
- 机构资金流入/流出排名表（排名前 8 的币种）
- 每个币种的交易建议

## K 线分析方法

对于每个时间周期（15 分钟/1 小时/4 小时），系统会获取 10 根 K 线数据，并计算以下指标：
- **趋势**：连续 3 根 K 线的方向（上涨/下跌/盘整）
- **多头/空头比率**：绿色蜡烛与红色蜡烛的数量比例
- **MA 对齐情况**：MA3 与 MA7 的排列情况（多头排列/空头排列）
- **成交量变化**：最近 3 根 K 线的成交量与之前 3 根 K 线的成交量对比（百分比）
- **支撑位**：10 根 K 线中的最低点
- **阻力位**：10 根 K 线中的最高点

## 视频报告（可选）

有关如何从报告数据生成视频的详细信息，请参阅 `references/video-pipeline.md`。