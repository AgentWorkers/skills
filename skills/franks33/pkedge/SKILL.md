---
name: pkedge
description: "监控 Polymarket 的预测市场，发现群体预测与现实世界证据之间的价格差异；追踪排名前 50 的钱包持有者的交易行为（即“鲸鱼”投资者的动向），并检测新的内部交易信号。该工具支持四种模式：  
1. **SCAN**：每日汇总被标记为异常的市场情况；  
2. **DEEP DIVE**：对单个市场进行深入分析，并结合网络搜索结果进行验证；  
3. **WHALE WATCH**：分析顶级交易者的持仓情况，以识别市场共识；  
4. **INSIDER WATCH**：检测新出现的、涉及大额资金交易的内部交易信号。"
homepage: https://polymarket.com
metadata: { "openclaw": { "emoji": "📈", "requires": { "bins": ["curl", "node"], "env": ["PKEDGE_TELEGRAM_TOKEN_FREE", "PKEDGE_TELEGRAM_CHAT_FREE", "PKEDGE_TELEGRAM_TOKEN_TRADER", "PKEDGE_TELEGRAM_CHAT_TRADER"] } } }
version: 1.1.0
author: pkedge
license: MIT
---
# PKEdge — Polymarket 智能分析技能

## 概述  
PKEdge 是一个基于 OpenClaw 的分析技能，用于监控 Polymarket 的预测市场，识别市场参与者预期与现实数据之间的价格异常，追踪排名前 50 的交易者的交易行为，并检测新出现的交易者活动。该技能提供四种运行模式：SCAN、DEEP DIVE、WHALE WATCH 和 INSIDER WATCH。  

**仅提供信息参考，不提供交易建议。请自行判断风险并做出决策。**  

**调度时间：**  
- 上午 8:00（东部时间）——每日市场扫描摘要（适用于所有用户）  
- 上午 8:05（东部时间）——上午交易者观察（回顾过去 48 小时的市场数据）  
- 上午 8:10（东部时间）——上午交易者内部观察（回顾过去 48 小时的市场数据）  
- 下午 4:00（东部时间）——下午交易者观察（回顾过去 24 小时的市场数据）  
- 下午 4:05（东部时间）——下午交易者内部观察（回顾过去 24 小时的市场数据）  
- 每 30 分钟——当有 3 个或更多交易者同时进入同一市场时，发送实时警报  
- 每 30 分钟——当有新交易者在该市场进行超过 5 万美元的交易时，发送实时警报  

---

## 安装方法  
1. 进入技能文件夹，运行 `npm install`  
2. 创建一个 `.env` 文件，填写您的 Telegram 凭据：  
  - `PKEDGE_TELEGRAM_TOKEN_FREE`：免费通道的机器人令牌  
  - `PKEDGE_TELEGRAM_chat_FREE`：免费通道的聊天 ID  
  - `PKEDGE_TELEGRAM_TOKEN_TRADER`：交易者通道的机器人令牌  
  - `PKEDGE_TELEGRAMCHAT_TRADER`：交易者通道的聊天 ID  
3. 运行 `node cron.js` 以启动定时任务，或配置 `launchd` 以便在系统启动时自动运行该技能  

---

## 触发语句  
当用户说出以下语句时，Claude 会激活该技能：  

### SCAN 模式  
- `pkedge scan`  
- `run the pkedge scan`  
- `prediction market scan`  
- `polymarket scan`  
- `what markets are flagged today`  
- `pkedge morning digest`  

### DEEP DIVE 模式  
- `pkedge deep dive [问题或主题]`  
- `analyze this market: [问题]`  
- `pkedge analyze: [问题]`  
- `what does pkedge think about [主题]`  
- `is [市场问题] mispriced`  
- `/deepdive [问题]`  

### WHALE WATCH 模式  
- `pkedge whale watch`  
- `whale watch`  
- `what are the whales doing`  
- `polymarket whale positions`  
- `pkedge whales`  

### INSIDER WATCH 模式  
- `pkedge insider watch`  
- `insider watch`  
- `fresh wallet alert`  
- `any insider activity`  
- `pkedge insiders`  
- `suspicious wallets`  
- `new money polymarket`  

---

## 文件位置  
（文件路径未在文档中提供，保留原样）  

---

## SCAN 模式  
**功能：**  
按交易量筛选 Polymarket 上活跃的前 200 个市场，标记异常情况，并生成摘要。  

**步骤：**  
1. 从 `fetch.js` 中调用 `fetchActiveMarkets()`，获取包含 `yesPrice`、`noPrice`、`volume`、`volume24hr`、`endDate` 的市场对象。  
2. 过滤出交易量超过 1 万美元的市场。  
3. 从 `analyze.js` 中调用 `runScanFlags(markets)`，应用 5 个评估指标：`VOLUME_SURGE`、`SPREAD_ANOMALY`、`VOLUME_SPIKE`、`EXTREME_LOW/HIGH`、`RESOLVING_SOON`；每个指标对应一定的分数，`scanScore` 为这些分数的总和。  
4. 对标记出的市场按分数降序排序。  
5. 对前 5 个标记出的市场，通过网页搜索获取最新新闻（例如：`"[市场问题]" news today`），并将结果添加到市场分析中。  
6. 从 `formatter.js` 中调用 `formatScanDigest(flaggedMarkets, 5)` 生成交易者通道的摘要内容；  
7. 从 `formatter.js` 中调用 `formatScanPreview(flaggedMarkets[0])` 生成免费通道的摘要内容。  
8. 通过 `deliver.js` 的 `sendToTrader()` 和 `sendToFree()` 方法发送结果。  

---

## DEEP DIVE 模式  
**功能：**  
对单个市场进行深入分析，对比市场参与者的预期与实际价格，评估市场公允价值，并生成结构化的报告。  

**步骤：**  
1. 解析用户输入的市场问题。  
2. 从 `fetch.js` 中调用 `searchMarkets(query)`，找到对应的 Polymarket 市场（若有多个结果，选择交易量最大的市场）。  
3. 获取市场数据：  
  - `fetchPriceHistory(market.id, '1d')`：获取每日价格走势  
  - `fetchBookDepth(market.clobTokenIds[0])`：获取订单簿深度信息  
  - 计算价格波动率（最近价格与 24 小时前价格的百分比差异）。  
4. 从 `analyze.js` 中调用 `analyzeMarket(market, bookDepth)`，获取分析结果（包括市场状况、价格波动等信息）。  
5. 通过网页搜索收集更多证据：  
  - 搜索相关新闻（例如：`"[市场问题]" news [当前年份]`）  
  - 汇总关键信息（如市场趋势、重要事件等）。  
6. 根据收集到的信息估算市场公允价值，并以概率范围表示（例如：“52–60% 可能上涨”）。  
7. 从 `analyze.js` 中调用 `computeConviction(crowdPct, fairPct)` 计算分析结果。  
8. 从 `formatter.js` 中调用 `formatDeepDive(analysis, conviction, evidenceLines)` 生成报告。  
9. 仅通过 `sendToTrader()` 方法发送报告（仅限交易者查看）。  

---

## WHALE WATCH 模式  
**功能：**  
监控按历史利润排名前 50 的 Polymarket 交易者，检测多个交易者同时进入同一市场的行为，并发送实时警报。  

**运行时间：**  
- 上午 8:05（东部时间）：回顾过去 48 小时的市场数据  
- 下午 4:00（东部时间）：回顾过去 24 小时的市场数据  

**步骤：**  
1. 从 `fetch.js` 中调用 `fetchLeaderboard(50)`，获取历史利润排名前 50 的交易者信息。  
2. 遍历这些交易者的交易记录，提取地址信息。  
3. 从 `analyze.js` 中调用 `buildWhaleReport(leaderboard, walletPositions, windowHours)`，生成报告：  
  - 上午：回顾过去 48 小时的市场数据  
  - 下午：回顾过去 24 小时的市场数据  
  - 过滤出在指定时间内开仓的交易记录，统计进入同一市场的交易者数量。  
4. 通过 `sendToTrader()` 方法发送报告。  
5. 对于当天尚未发送警报的市场，通过 `formatWhaleAlert(consensusMarket, latestPosition)` 发送实时警报。  

---

## INSIDER WATCH 模式  
**功能：**  
检测新出现的交易者及其大额交易行为（通常是知情交易的信号）。新交易者的账户创建时间通常较短（<30 天），且交易次数较少（<20 次）。  

**警报等级：**  
- 单笔交易额 > 5 万美元 = 👀 观察（记录在每日摘要中）  
- 单笔交易额 > 2.5 万美元 = ⚠️ 警报（记录在每日摘要中）  
- 单笔交易额 > 50 万美元 = 🚨 即时警报（立即发送，不等待每日摘要）  
- 6 小时内有多个新交易者进入同一市场 = 🚨 协调交易（立即发送警报）  

**运行时间：**  
- 上午 8:10（东部时间）：回顾过去 48 小时的市场数据  
- 下午 4:05（东部时间）：回顾过去 24 小时的市场数据  
- 每 30 分钟：检测新出现的交易额超过 5 万美元的交易（较低金额的交易记录在每日摘要中）。  

---

## API 参考（全部免费，无需授权）  
| API 地点 | 功能 |  
|---|---|  
| `GET https://gamma-api.polymarket.com/markets?active=true&limit=200` | 查看所有市场  
| `GET https://gamma-api.polymarket.com/markets?slug={slug}` | 根据 slug 查看特定市场  
| `GET https://gamma-api.polymarket.com/prices-history?market={id}&interval=1d` | 获取市场价格历史数据  
| `GET https://clob.polymarket.com/book?token_id={tokenId}` | 获取订单簿信息  
| `GET https://clob.polymarket.com/midpoint?token_id={tokenId}` | 获取市场价格中间价  
| `GET https://clob.polymarket.com/bbo?token_id={tokenId}` | 获取最佳买卖价  
| `GET https://clob.polymarket.com/trades?token_id={tokenId}&limit=500` | 获取近期市场交易记录（用于内部观察）  
| `GET https://data-api.polymarket.com/v1/leaderboard?timePeriod=ALL&orderBy=PNL&limit=50` | 查看顶级交易者信息  
| `GET https://data-api.polymarket.com/positions?user={address}` | 查看交易者的交易记录和账户信息  
| `GET https://data-api.polymarket.com/trades?user={address}&limit=500` | 查看交易者的完整交易历史和账户信息  

---

## 环境变量  
（相关环境变量未在文档中提供，保留原样）  

---

## 订阅套餐  
| 订阅等级 | 价格 | 服务内容 |  
|---|---|---|  
| FREE EDGE | $0 | 每日扫描摘要（1 个市场）  
| WATCHER | $9/月 | 全部 5 个市场的扫描摘要，基础功能（每天 3 次查询）  
| TRADER | $29/月 | 无限次深度分析、交易者观察、内部观察功能，以及所有实时警报  
| QUANT | $99/月 | 原始数据分析 API、Discord 量化交易社区、历史数据分析日志  

---

## 评分标准  
**SCAN 模式评分标准：**  
| 指标 | 分数 | 触发条件 |  
|---|---|---|  
| VOLUME_SPIKE | 3 | 24 小时交易量超过日均交易量的 3 倍 |  
| VOLUME_SURGE | 2 | 24 小时交易量超过历史交易量的 25% |  
| RESOLVING_SOON | 2 | 价格将在 7 天内确定 |  
| SPREAD_ANOMALY | 1 | 买卖价差超过 6 分 |  
| EXTREME_LOW / HIGH | 1 | 价格波动幅度超过 10% 或低于 90% |  

**警报等级阈值：**  
- 2 分 = 观察级别 | 4 分 = 高风险级别 | 6 分以上 = 高风险级别  

**内部交易信号评分标准：**  
| 交易额 > 5 万美元 | 1 分 |  
| 交易额 > 25 万美元 | 3 分 |  
| 交易额 > 50 万美元 | 3 分 |  
| 账户创建时间 < 7 天 | 3 分 |  
| 账户创建时间 7–14 天 | 2 分 |  
| 账户创建时间 15–30 天 | 1 分 |  
| 交易次数 < 5 次 | 2 分 |  
| 6 小时内有多个新账户进入同一市场 | +5 分（额外加分）  

---

**使用注意事项：**  
- 不得预测市场走势的方向  
- 不得直接建议“买入”或“卖出”，而应说明“根据现有信息，买入可能性较高”  
- 始终注明“本技能仅提供信息参考，不提供交易建议。预测市场存在风险”  
- 如果网页搜索未找到有用信息，应如实告知用户  
- 如果市场订单簿深度不足（<1 万美元），必须明确标注  
- 对于交易量低于 5 万美元的市场，不进行深入分析（流动性不足）  
- 在内部观察模式下，不得指责交易者的行为，应描述为“异常交易模式”  
- 新交易者的行为可能是偶然的，需注意大额交易可能有其他合理原因