---
name: polymarket-signal-sniper
displayName: Polymarket Signal Sniper
description: 从您自己的信号源中捕捉 Polymarket 的投资机会。使用具备 Trading Agent 级别安全防护功能的 RSS 订阅源进行实时监控。
metadata: {"clawdbot":{"emoji":"🎯","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false,"automaton":{"managed":true,"entrypoint":"signal_sniper.py"}}}
authors:
  - Simmer (@simmer_markets)
version: "1.3.7"
published: true
---
# Polymarket Signal Sniper

这是一个用于捕捉市场信号的自动化工具，它整合了Simmer的交易智能。

> **这是一个模板。** 默认的信号来源是RSS订阅源——您可以根据需要将其替换为其他数据源（如API、Webhooks或自定义数据抓取工具）。该工具负责处理所有的市场匹配、风险控制以及交易执行等底层逻辑，而用户提供的信息则是决策的关键。

## 适用场景

当用户希望：
- 监控RSS订阅源以寻找交易机会
- 在市场反应之前基于突发新闻进行交易
- 自定义信号来源和关键词
- 为交易获得高级别的风险保护时，可以使用此工具。

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

## 快速上手（临时使用）

**用户提供RSS订阅源和市场信息：**
```
User: "Watch this RSS feed for greenland news: https://news.google.com/rss/search?q=greenland"
User: "Snipe any news about trump from this feed"
```

→ 使用`--feed`和`--market`参数运行脚本：
```bash
python signal_sniper.py --feed "https://news.google.com/rss/search?q=greenland" --market "greenland-acquisition" --dry-run
```

## 持久化设置（可选）

为了实现自动化的定期扫描，可以通过环境变量进行配置：

| 设置 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| RSS订阅源 | `SIMMER_SNIPER_FEEDS` | （无） | 用逗号分隔的RSS地址列表 |
| 目标市场 | `SIMMER_SNIPERMARKETS` | （自动检测） | 用逗号分隔的市场ID列表；如果未设置关键词，系统会自动识别相关市场 |
| 关键词 | `SIMMER_SNIPER_KEYWORDS` | （无） | 用于匹配的新闻关键词 |
| 交易置信度 | `SIMMER_SNIPER_CONFIDENCE` | 0.7 | 最低交易置信度（0.0-1.0） |
| 每笔交易的最大金额（USD） | `SIMMER_SNIPER_MAX_USD` | 25 | 每笔交易的最大金额 |
| 每次扫描的最大交易数量 | `SIMMER_SNIPER_MAX_TRADES` | 5 | 每次扫描的最大交易次数 |

**Polymarket的限制：**
- 每笔订单至少需要5份股份
- 低于此数量的订单将被拒绝，并显示错误信息。

## 工作原理

脚本的工作流程如下：
1. 定期轮询配置的RSS订阅源
2. 根据关键词过滤文章（如果设置了关键词）
3. 将匹配到的文章与目标市场进行匹配（如果未设置市场，系统会自动根据关键词识别目标市场）
4. 对于每个匹配结果，调用SDK的上下文端点进行风险检查：
   - 检查当前持仓情况
   - 判断市场是否发生方向性变化
   - 评估市场流动性
   - 判断市场是否即将达成某种结果
   - 根据具体条件判断是否适合进行交易
5. 如果风险检查通过，根据文章的情感倾向决定交易方向
6. 通过SDK执行交易（遵守每次扫描的最大交易数量限制）
7. 记录已处理过的文章以避免重复计算

## 运行脚本

**进行一次扫描（默认为模拟运行，不执行交易）：**
```bash
python signal_sniper.py
```

**执行实际交易：**
```bash
python signal_sniper.py --live
```

**仅查看信号而不执行交易：**
```bash
python signal_sniper.py --scan-only
```

**查看当前配置：**
```bash
python signal_sniper.py --config
```

**针对单次运行进行临时配置：**
```bash
python signal_sniper.py --feed "https://..." --keywords "trump,greenland" --market "abc123"
```

**查看已处理的文章：**
```bash
python signal_sniper.py --history
```

## 解读警告信息

在交易前，请务必查看系统显示的警告信息。警告内容包括：
- **市场已达成结果**：此时不应进行交易
- **高紧急性：将在X小时内达成结果**：判断信号是否足够及时
- **方向性变化警告**：如果市场方向频繁变动，请谨慎操作或等待更明确的信号
- **价差过大**：考虑减少持仓规模或跳过此次交易
- **Simmer AI信号提示**：参考Simmer的预测意见

## 分析信号

找到匹配的文章后，请仔细分析：
1. **阅读标题和摘要**：了解新闻的实质内容
2. **检查具体结果**：确认该新闻是否与交易条件相关
   - 例如，标题中的“Greenland”并不一定意味着“收购完成”
   - 实际结果可能是“美国将于2027年正式收购格陵兰”
   - 该信号是否符合交易条件？
3. **评估置信度**（0.0-1.0）：
   - 信号与交易条件的关联程度
   - 来源的可靠性
   - 该新闻是否已被市场价格反映
4. **仅在以下情况下进行交易**：
   - 置信度超过阈值（默认0.7）
   - 无严重警告
   - 信号与交易条件一致

## 示例对话

**用户：“为Greenland市场设置新闻监控”**
- 提供需要监控的RSS订阅源
- 配置目标市场和关键词
- 设置定时任务以自动执行扫描

**用户：“检查这个订阅源中的交易信号”**
- 运行命令：`python signal_sniper.py --feed "URL" --scan-only`
- 查看找到的文章和潜在的交易机会

**用户：“从CoinDesk获取比特币相关的交易信号”**
- 使用CoinDesk的RSS源和比特币相关市场
- 查看匹配结果并决定是否进行交易

**用户：“我们处理了哪些信号？”**
- 运行命令：`python signal_sniper.py --history`
- 查看最近的处理记录和交易操作

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

**“未配置订阅源”**
- 在提示中提供RSS地址：`watch this RSS: https://...`
- 或者设置环境变量`SIMMER_SNIPER_FEEDS`

**“未找到匹配文章”**
- 确认关键词是否正确
- 可能是RSS源最近没有更新文章
- 尝试使用`--scan-only`选项查看订阅源内容

**“因市场方向性变化被跳过”**
- 市场方向频繁变动，请等待市场稳定后再进行交易或获取新信息

**“滑点过高”**
- 市场流动性差，建议减少交易规模或跳过此次交易

**“文章已处理过”**
- 该文章已被系统记录过，避免重复处理

**“外部钱包需要预签名订单”**
- 确保环境变量`WALLET_PRIVATE_KEY`已设置
- 当该变量存在时，SDK会自动签名订单，无需手动操作
- 解决方法：`export WALLET_PRIVATE_KEY=0x<your-polymarket-wallet-private-key>`
- 请勿尝试手动签名订单或修改脚本代码

**“账户余额显示为0美元，但我有USDC在Polygon上”**
- Polymarket使用的是**USDC.e**（桥接后的USDC，合约地址`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`），而非原生USDC
- 如果您最近将USDC桥接到了Polygon，可能需要将USDC.e兑换为原生USDC后再进行交易

**如何选择合适的RSS订阅源**

以下是一些建议：
- **Google News RSS**：`https://news.google.com/rss/search?q=YOUR_TOPIC`
- **专业领域来源**：通常比主流新闻更具有参考价值（价格变动较小）
- **官方来源**：政府或公司的公告
- **Twitter列表的RSS版本**：可以使用Nitter或RSS.app等工具获取

该工具在以下情况下表现最佳：
- 订阅源与目标市场相关
- 您有明确的关键词来过滤无关信息
- 来源能在主流媒体之前发布新闻