# AgResource新闻通讯抓取工具

使用此工具抓取、汇总并分析AgResource发布的谷物市场新闻通讯。

## 实现方式

- **抓取工具：** `scraper.js`（基于Playwright/Node.js开发）
- **情感分析工具：** `agresource_sentiment.py`（Python编写）
- **登录方式：** 使用环境变量`AGRESOURCE_EMAIL`和`AGRESOURCE_PASSWORD`自动登录

## 功能特性

- 登录AgResource管理面板（https://agresource.com/dashboard/#/reports/daily）
- 使用Playwright抓取每日新闻通讯内容
- 保存截图以供参考或调试
- 提取关于玉米/大豆的销售建议和推荐信息
- 生成包含关键新闻和天气信息的简洁摘要
- 分析新闻通讯中的整体情感倾向（看涨/看跌）
- 与之前的新闻通讯进行对比以发现趋势变化
- 将摘要保存在以下路径：
  - `~/clawd/memory/agresource/YYYY-MM-DD.md`（上午版）
  - `~/clawd/memory/agresource/YYYY-MM-DD-noon.md`（下午版）
  - `~/clawd/memory/agresource/YYYY-MM-DD-evening.md`（晚间版）
  - `~/clawd/memory/agresource/YYYY-MM-DD-saturday.md`（周六版）
  - `~/clawd/memory/agresource/YYYY-MM-DD-sunday.md`（周日版）
- 将情感分析结果保存在`~/clawd/memory/agresource/sentiment_history.json`文件中
- 在有新的销售建议时发送Telegram提醒

## 命令操作

### 手动触发
```
"Check AgResource newsletter"
"Summarize today's grain report"
"Show full newsletter" (detailed view)
```

**手动运行抓取工具的方法：**
```bash
cd /home/brianppetty/clawd/skills/agresource

# Morning newsletter (default)
node scraper.js
node scraper.js --type=morning

# Noon/midday newsletter
node scraper.js --type=noon

# Evening newsletter
node scraper.js --type=evening

# Saturday newsletter
node scraper.js --type=saturday

# Sunday newsletter
node scraper.js --type=sunday
```

### Cron作业触发

当Cron任务触发时，根据时间与类型参数进行匹配：

| Cron任务内容 | 使用的类型参数 | 触发时间 |
|--------------|-------------|------|
| "检查AgResource新闻通讯（上午版）" | `--type=morning` | 美国东部时间周一至周五上午8:30 |
| "检查AgResource新闻通讯（下午版）" | `--type=noon` | 美国东部时间周一至周五下午1:30 |
| "检查AgResource新闻通讯（晚间版）" | `--type=evening` | 美国东部时间周一至周六晚上7:00 |
| "检查AgResource新闻通讯（周末版）" | `--type=saturday` 或 `--type=sunday` | 美国东部时间周六/周日下午3:00左右 |

**对于周末任务**，需要根据具体日期选择相应的类型参数：
- 周六：`--type=saturday`
- 周日：`--type=sunday`

### 情感分析查询
```
"What's the current market sentiment?"
"Show sentiment trends"
"What's the sentiment history?"
```

## 情感分析的关注维度（侧重于价格影响）

**情感分析的重点是价格影响，而非简单的“好/坏”信息。**

**需要记住的关键反向关系：**
- ☀️ 南美洲/北美洲的利好天气 → 供应增加 → 对价格产生负面影响（看跌）
- 🌽 收成创纪录 → 供应增加 → 对价格产生负面影响（看跌）
- 🏜️ 干旱/作物生长受阻 → 供应减少 → 对价格产生积极影响（看涨）
- 🏭 出口需求强劲 → 需求增加 → 对价格产生积极影响（看涨）
- 📦 南美洲的竞争加剧 → 美国出口减少 → 对价格产生负面影响（看跌）

在新闻通讯中跟踪以下维度：
- **市场情绪**：看涨 | 看跌 | 中立
  - 看涨：预计价格会上涨
  - 看跌：预计价格会下跌
- **天气影响**：对作物有利 | 对作物不利 | 中立
  - 该指标反映天气对生产的影响（与价格影响方向相反）
  - 对作物有利的天气 → 价格可能下跌（供应增加）
- **生产前景**：乐观 | 谨慎 | 不确定
  - 乐观：供应增加 → 价格可能下跌
  - 谨慎：存在供应问题 → 价格可能上涨
- **趋势方向**：好转 | 下降 | 稳定
- **信心水平**：高 | 中等 | 低

## 销售建议的检测

**用于检测销售建议的关键词：**
- “发现新的销售建议”（包含“购买”、“出售”、“持有”等关键词）
- “建议补仓”（表示需要增加持仓）
- “目前不建议买卖”（表示无需采取行动）
- “持仓状态不变”（表示与上次相同）

## Telegram提醒格式

每条新闻通讯都会发送简短的摘要：
```
🌾 AgResource - 2026-01-08 8:30 AM

Summary: No sales recommended
Sentiment: Bullish (↗️ improving)

Full details in ~/clawd/memory/agresource/
```

## 输出格式

### 每日摘要文件（`YYYY-MM-DD.md`）

```markdown
# AgResource Newsletter - 2026-01-08 8:30 AM

## Quick Summary
[2-3 sentence overview]

## Key Newsworthy Items
- [Grain production relevant news]
- [Weather tidbits]

## Sales Advice Status
- Corn: [New sales advice / No change / No sales recommended]
- Soybeans: [New sales advice / No change / No sales recommended]

## Current Positions (from end of newsletter)
- [Summary of current positioning]

## Sentiment & Trends
- **Market Mood:** Bullish / Bearish / Neutral
- **Previous Mood:** [from last newsletter]
- **Trend:** Improving / Declining / Stable
- **Weather Impact:** Positive / Negative / Mixed
- **Production Outlook:** Optimistic / Cautious / Uncertain

## Full Content
[Optional: full newsletter content for reference]
```

### 情感分析历史文件（`sentiment_history.json`）

```json
{
  "last_updated": "2026-01-08T08:30:00",
  "sentiment_history": [
    {
      "date": "2026-01-08",
      "time": "08:30 AM",
      "market_mood": "bullish",
      "weather_impact": "positive",
      "production_outlook": "optimistic",
      "trend_direction": "improving",
      "confidence": "high",
      "key_phrases": ["prices advancing", "favorable weather"],
      "sales_advice": "No sales recommended"
    }
  ]
}
```

## 配置信息

**登录凭据：** 从环境变量中读取
- `AGRESOURCE_EMAIL`
- `AGRESOURCE_PASSWORD`

**依赖库：**
- Node.js（Clawdbot内置）
- Playwright（需在本地安装：`/home/brianppetty/clawd/skills/agresource/node_modules/playwright`

**调度安排：** 每天执行4次（通过Cron作业）
- 上午：美国东部时间8:30
- 下午：美国东部时间1:30
- 晚上：美国东部时间7:00
- 周末：美国东部时间下午3:00左右

**数据保留策略：** 保留过去15-20条新闻通讯的数据用于情感分析

## 注意事项

- 仅当销售建议发生变化时才发送Telegram提醒
- 必须保存所有摘要和情感分析数据
- 随时间优化情感分析的检测规则
- 晚间版新闻通讯包含当前的持仓情况
- 登录凭据需妥善保管