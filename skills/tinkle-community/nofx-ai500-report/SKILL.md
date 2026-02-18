---
name: nofx-ai500-report
description: 从 NOFX AI500 系统生成定期的加密货币市场情报报告。该系统会监控所选加密货币的行情数据，分析未平仓合约（OI，Open Interest）、机构资金流动情况、K 线技术指标、Delta 值、多空持仓比例以及资金费率等关键参数。这些报告可用于生成自动化的加密货币市场报告、AI500 信号监控系统、新加密货币的预警通知，或通过 Telegram/消息平台发送定期的交易信号摘要。
license: MIT
---
# NOFX AI500 报告功能

该功能能够利用 NOFX AI500 评分系统自动生成全面的加密货币市场情报报告，并实现自动监控和报告发送。

## 前提条件

- 具备 NOFX API 访问权限：基础 URL + 认证密钥（由用户提供）
- 需要一个用于接收报告的 Telegram 聊天频道或消息传递渠道
- 使用支持 `ssl`, `json`, `urllib` 的 Python 3 环境

## 设置流程

请用户提供以下信息：
1. **NOFX API 基础 URL**（例如：`https://nofxos.ai`）
2. **API 认证密钥**（例如：`cm_xxxx`）
3. **报告发送目标**——Telegram 聊天 ID 或频道

接下来，使用 OpenClaw cron 工具创建两个定时任务：

### 任务 1：新币种监控（每 15 分钟执行一次）

通过 `exec` 命令运行 `scripts/monitor.sh` 脚本，并将 API 基础 URL 和认证密钥作为环境变量传递：
- 如果输出 `NEW:`，则表示有新币种被添加到监控列表中，系统会发送警报并生成详细分析报告；
- 如果输出 `REMOVED:`，则表示该币种已被移出监控列表；
- 如果输出 `NO_CHANGE`，则表示该币种的状态没有变化，系统将不发送任何通知。

完整的 cron 任务配置模板请参见 `references/monitor-job.md`。

### 任务 2：定期报告（每 30 分钟执行一次）

从多个 NOFX API 端点以及 Binance 公共 API 获取数据，并将其整理成格式化的报告。

完整的 cron 任务配置模板请参见 `references/report-job.md`。

## API 端点说明

所有 NOFX API 端点都需要添加 `?auth=KEY` 参数。

| 端点            | 功能                          | 参数                                      |
|------------------|----------------------------------|-----------------------------------------|
| `/api/ai500/list`     | 获取当前 AI500 评分列表                 |                                        |
| `/api/oi/top-ranking`    | 获取 OI（Open Interest）排名变化            | `duration`                               |
| `/api/oi/low-ranking`    | 获取 OI 排名下降的币种                | `duration`                               |
| `/api/netflow/top-ranking`   | 获取资金流入排名                   | `type=institution&trade=future&duration`                |
| `/api/netflow/low-ranking`   | 获取资金流出排名                   | same                                      |
| `/api/delta/list`      | 获取币种价格变动数据                   | `symbol`                                   |
| `/api/long-short-ratio/list` | 获取多空持仓比率                   | `symbol`                                   |
| `/api/funding-rate/top-ranking` | 获取资金费率排名                   |                                        |
| `/api/funding-rate/low-ranking` | 获取资金费率排名                   |                                        |

`duration` 可选值：`5m`, `15m`, `30m`, `1h`, `4h`, `8h`, `24h`

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

为了确保报告能在 Telegram 上正常显示，代码块中会使用 Unicode 格式进行图表绘制。每个币种的报告内容包括：

1. **AI500 评分** 以及自被纳入监控列表以来的累计回报
2. 在 7 个时间周期（5 分钟至 24 小时）内的 OI 变化情况，包括百分比和美元数值（来自 `oi_delta_value`）
3. 不同时间周期内的机构资金流入情况，以及 해당币种在排名前 20 名中的位置
4. K 线分析结果（15 分钟/1 小时/4 小时周期）：趋势方向、多头/空头蜡烛数量占比、MA3 与 MA7 的对比、成交量变化、支撑位/阻力位
5. 资金费率（如果超过 0.03%，会发出警告）

每个币种的报告还包括以下内容：
- OI 排名表（排名前 8 的上涨/下跌币种，时间周期为 1 小时/4 小时/24 小时）
- 机构资金流入/流出排名表（排名前 8 的币种）
- 每个币种的总结及可行的交易建议

## K 线分析方法

对于每个时间周期（15 分钟/1 小时/4 小时），系统会获取 10 根 K 线数据并计算以下指标：
- **趋势**：连续 3 根 K 线的方向（📈上涨/📉下跌/↔️横盘）
- **多头/空头比率**：10 根 K 线中绿色蜡烛与红色蜡烛的数量比例
- **MA 对齐情况**：MA3 与 MA7 的对比（上涨/下跌趋势）
- **成交量变化**：最近 3 根 K 线的成交量与之前 3 根 K 线的成交量对比（百分比）
- **支撑位**：10 根 K 线中的最低价
- **阻力位**：10 根 K 线中的最高价

## 视频报告（可选）

有关如何从报告数据生成视频的详细信息，请参阅 `references/video-pipeline.md`。