---
name: polymarket-signal-sniper
displayName: Polymarket Signal Sniper
description: 从您自己的信号源中捕捉 Polymarket 的投资机会。使用具备 Trading Agent 级别安全防护功能的 RSS 源监控工具进行实时监控。
metadata: {"clawdbot":{"emoji":"🎯","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
version: "1.3.4"
published: true
---
# Polymarket Signal Sniper

这是一个用于捕捉市场信号的自动化工具，它整合了Simmer的交易智能。

> **这只是一个模板。** 默认的信号来源是RSS订阅源——您可以根据需要将其替换为任何数据源（API、Webhook或自定义数据抓取工具）。该工具负责处理所有的市场匹配、风险控制以及交易执行等底层逻辑，而您的代理（agent）则负责最终的交易决策。

## 适用场景

当用户希望：
- 监控RSS订阅源以寻找交易机会
- 在市场反应之前根据突发新闻进行交易
- 自定义信号来源和关键词
- 为交易获得高级别的风险保护机制时，可以使用此工具。

## 快速命令

```bash
# Check account balance and positions
python scripts/status.py

# Detailed position list
python scripts/status.py --positions
```

**API参考：**
- 基础URL：`https://api.simmer.markets`
- 认证：`Authorization: Bearer $SIMMER_API_KEY`
- 投资组合：`GET /api/sdk/portfolio`
- 持仓情况：`GET /api/sdk/positions`

## 快速入门（临时使用）

**用户提供RSS订阅源和目标市场：**
```
User: "Watch this RSS feed for greenland news: https://news.google.com/rss/search?q=greenland"
User: "Snipe any news about trump from this feed"
```

→ 使用`--feed`和`--market`参数运行脚本：
```bash
python signal_sniper.py --feed "https://news.google.com/rss/search?q=greenland" --market "greenland-acquisition" --dry-run
```

## 持续设置（可选）

为了实现自动化的定期扫描，可以通过环境变量进行配置：

| 设置 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| RSS订阅源 | `SIMMER_SNIPER_FEEDS` | （无） | 用逗号分隔的RSS地址列表 |
| 目标市场 | `SIMMER_SNIPERMARKETS` | （无） | 用逗号分隔的市场ID列表 |
| 关键词 | `SIMMER_SNIPER_KEYWORDS` | （无） | 用于匹配的关键词列表 |
| 交易信心值 | `SIMMER_SNIPER_CONFIDENCE` | 0.7 | 最低交易信心值（0.0-1.0） |
| 每笔交易的最大金额（美元） | `SIMMER_SNIPER_MAX_USD` | 25 | 每笔交易的最大金额 |
| 每次扫描的最大交易数量 | `SIMMER_SNIPER_MAX_TRADES` | 5 | 每次扫描的最大交易次数 |

**Polymarket的限制：**
- 每笔订单至少需要5股股票
- 低于此数量的订单将被拒绝，并显示错误信息。

## 工作原理

脚本每个周期会执行以下操作：
1. 轮询配置好的RSS订阅源
2. 根据关键词过滤文章（如果已配置）
3. 将匹配到的文章与目标市场进行匹配
4. 对于每个匹配结果，调用SDK的相应接口进行风险检查：
   - 检查当前持仓情况
   - 判断市场是否发生方向性变化
   - 估计滑点情况（市场是否具有流动性）
   - 判断市场是否即将达成某种结果
   - 根据具体标准判断市场是否真正发生了变化
5. 如果风险检查通过，您（Claude）将分析信号
6. 如果认为信号可靠，将通过SDK执行交易
7. 记录已处理的文章内容以避免重复处理

## 运行脚本

**执行扫描（默认为模拟运行，不进行交易）：**
```bash
python signal_sniper.py
```

**执行实际交易：**
```bash
python signal_sniper.py --live
```

**仅查看信号而不进行交易：**
```bash
python signal_sniper.py --scan-only
```

**查看当前配置：**
```bash
python signal_sniper.py --config
```

**针对单次运行进行自定义设置：**
```bash
python signal_sniper.py --feed "https://..." --keywords "trump,greenland" --market "abc123"
```

**查看已处理的文章：**
```bash
python signal_sniper.py --history
```

## 解读警告信息

在交易前，请务必查看警告信息。系统会显示以下警告：
- **MARKET RESOLVED**：不要进行交易
- **HIGH URGENCY: Resolves in Xh**：判断信号是否及时
- **flip_flop_warning: SEVERE**：建议跳过此次交易（市场方向变化过于频繁）
- **flip_flop_warning: CAUTION**：需谨慎操作，需要更明确的信号
- **Wide spread (X%)**：建议减小持仓规模或跳过此次交易
- **Simmer AI signal: X% more bullish/bearish**：参考Simmer的预测意见

## 分析信号

找到匹配的文章后，请仔细分析：
1. **阅读标题和摘要**：了解新闻的实质内容
2. **检查市场判断标准**：判断该新闻是否真正符合市场变化的标准
   - 例如，标题中的“Greenland”并不一定意味着“收购完成”
   - 实际的判断标准可能是“美国将在2027年前正式收购格陵兰”
   - 该信号是否符合这些标准？
3. **评估信心值（0.0-1.0）**：
   - 该信号与市场判断标准的关联程度如何？
   - 来源是否可靠？
   - 该新闻是否已经被市场定价反映了？
4. **仅在执行交易时满足以下条件：**
   - 信心值大于阈值（默认0.7）
   - 没有严重的警告信息
   - 信号与市场判断标准一致

## 示例对话

**用户：“为格陵兰市场设置新闻捕捉功能”**
- 提供想要监控的RSS订阅源
- 配置目标市场和关键词
- 启用定时扫描功能

**用户：“检查这个订阅源中的交易信号”**
- 运行命令：`python signal_sniper.py --feed "URL" --scan-only`
- 查看找到的文章和潜在的交易机会

**用户：“从CoinDesk获取比特币相关的交易信号”**
- 使用CoinDesk的RSS源和比特币相关市场进行扫描
- 查看匹配结果并决定是否进行交易

**用户：“我们处理了哪些信号？”**
- 运行命令：`python signal_sniper.py --history`
- 查看最近的处理记录和执行的操作

## 示例交易流程

```
1. RSS poll finds: "Trump and Denmark reach preliminary Greenland agreement"
2. Keywords match: "greenland", "trump"
3. Call context endpoint for market "greenland-acquisition-2027"
4. Check warnings: none severe ✓
5. Resolution criteria: "Resolves YES if US formally acquires Greenland by 2027"
6. You analyze: "preliminary agreement" ≠ "formally acquires" but bullish signal
7. Confidence: 0.75 (positive indicator, not definitive)
8. Check slippage: 2.5% on $25 ✓
9. Execute: BUY YES $25
10. Report: "🎯 Sniped: Trump/Greenland agreement → BUY YES $25"
```

## 故障排除

- **“未配置订阅源”**：在提示中提供RSS地址：`watch this RSS: https://...`
- 或者设置环境变量`SIMMER_SNIPER_FEEDS`

- **“未找到匹配文章”**：
  - 确认关键词是否正确
  - 可能是RSS源没有最新的文章
  - 尝试使用`--scan-only`选项查看订阅源的内容

- **“因市场方向变化频繁而跳过交易”**：
  - 市场方向变化过于频繁，建议等待后再进行交易或寻找新的交易机会

- **“滑点过高”**：
  - 市场流动性差，建议减小交易规模或跳过此次交易

- **“文章已处理过”**：
  - 该文章已被系统记录过，系统会避免重复处理

## 选择合适的RSS订阅源

以下是一些建议：
- **Google News RSS**：`https://news.google.com/rss/search?q=YOUR_TOPIC`
- **专业领域来源**：通常比主流新闻来源更具有参考价值（价格变动较小）
- **官方来源**：政府或公司的公告
- **Twitter列表的RSS订阅**：可以使用Nitter或RSS.app等工具获取

该工具在以下情况下效果最佳：
- 订阅源与目标市场相关
- 您有特定的关键词来过滤无关信息
- 来源能在主流媒体之前发布新闻