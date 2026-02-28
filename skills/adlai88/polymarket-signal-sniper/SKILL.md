---
name: polymarket-signal-sniper
displayName: Polymarket Signal Sniper
description: 从您自己的信号源中捕捉 Polymarket 的投资机会。使用具备 Trading Agent 级别安全性的工具来监控 RSS 源。
metadata: {"clawdbot":{"emoji":"🎯","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false,"automaton":{"managed":true,"entrypoint":"signal_sniper.py"},"tunables":[{"env":"SIMMER_SNIPER_CONFIDENCE_THRESHOLD","type":"number","default":0.70,"range":[0.5,0.99],"step":0.01,"label":"Confidence threshold"},{"env":"SIMMER_SNIPER_MAX_USD","type":"number","default":50,"range":[1,200],"step":5,"label":"Max bet per trade"},{"env":"SIMMER_SNIPER_MAX_TRADES_PER_RUN","type":"number","default":5,"range":[1,20],"step":1,"label":"Max trades per run"}]}}
authors:
  - Simmer (@simmer_markets)
version: "1.3.7"
difficulty: intermediate
published: true
---
# Polymarket Signal Sniper

这是您的交易辅助工具——Simmer提供的智能交易信号服务。

> **这是一个模板。** 默认的信号来源是RSS订阅源，您也可以将其与任何数据源（API、Webhook、社交媒体或自定义数据抓取工具）结合使用。该工具负责处理所有的市场匹配、风险控制以及交易执行等底层逻辑，而您的代理程序则负责生成具体的交易策略。

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

## 快速启动（临时使用）

**用户提供RSS订阅源和目标市场信息：**
```
User: "Watch this RSS feed for greenland news: https://news.google.com/rss/search?q=greenland"
User: "Snipe any news about trump from this feed"
```

→ 使用`--feed`和`--market`参数运行脚本：
```bash
python signal_sniper.py --feed "https://news.google.com/rss/search?q=greenland" --market "greenland-acquisition" --dry-run
```

## 持久化配置（可选）

如需自动化定期扫描，请通过环境变量进行配置：

| 配置项 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| RSS订阅源 | `SIMMER_SNIPER_FEEDS` | （无） | 用逗号分隔的RSS地址列表 |
| 目标市场 | `SIMMER_SNIPERMARKETS` | （自动识别） | 用逗号分隔的市场ID列表（若未设置关键词，则自动从关键词中推断） |
| 关键词 | `SIMMER_SNIPER_KEYWORDS` | （无） | 用于匹配的新闻关键词 |
| 交易置信度 | `SIMMER_SNIPER_CONFIDENCE` | 0.7 | 最低交易置信度（0.0-1.0） |
| 每笔交易的最大金额 | `SIMMER_SNIPER_MAX_USD` | 25 | 每笔交易的最大金额 |
| 每次扫描的最大交易数量 | `SIMMER_SNIPER_MAX_TRADES` | 5 | 每次扫描的最大交易次数 |

**Polymarket限制：**
- 每笔订单至少需购买5股股票
- 低于此数量的订单将被拒绝，并显示错误信息。

## 工作原理

脚本每个周期会执行以下操作：
1. 轮询配置的RSS订阅源
2. 根据关键词过滤文章（如已配置）
3. 将匹配到的文章与目标市场进行匹配（若未配置目标市场，则自动从关键词中推断）
4. 对于每个匹配结果，调用SDK的上下文接口进行风险检查：
   - 检查当前持仓情况
   - 判断市场是否发生方向性变化
   - 估计交易滑点
   - 评估市场是否即将达成某个结果
   - 确定影响市场走向的关键因素
5. 如果风险检查通过，根据文章的情感倾向判断交易方向
6. 通过SDK执行交易（遵守每次扫描的最大交易数量限制）
7. 记录已处理的文章以避免重复计算

## 运行脚本

**执行扫描（默认为模拟运行，不进行实际交易）：**
```bash
python signal_sniper.py
```

**执行真实交易：**
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

**临时修改配置：**
```bash
python signal_sniper.py --feed "https://..." --keywords "trump,greenland" --market "abc123"
```

**查看已处理的文章：**
```bash
python signal_sniper.py --history
```

## 解读警告信息

在交易前，请务必查看警告信息。系统会显示以下警告：
- **MARKET RESOLVED**：此时不宜交易
- **HIGH URGENCY: Resolves in Xh**：判断信号是否足够及时
- **flip_flop_warning: SEVERE**：市场方向频繁变动，建议跳过
- **flip_flop_warning: CAUTION**：需谨慎操作，需要更明确的信号
- **Wide spread (X%)**：市场波动较大，建议减小持仓规模或跳过交易
- **Simmer AI signal: X% more bullish/bearish**：参考Simmer的预测意见

## 分析信号

发现匹配文章时，请仔细分析：
1. **阅读标题和摘要**：了解新闻的具体内容
2. **检查关键因素**：该新闻是否真正影响了市场走向？
   - 例如，标题中的“Greenland”并不意味着“收购完成”，实际可能是“美国将于2027年正式收购格陵兰”
3. **评估置信度**（0.0-1.0）：
   - 该信号与市场走向的关联程度如何？
   - 来源是否可靠？
   - 该新闻是否已被市场反映在价格中？
4. **仅当满足以下条件时才进行交易**：
   - 置信度高于阈值（默认0.7）
   - 无严重警告
   - 信号与市场走向相符

## 示例对话

**用户：“为格陵兰市场设置新闻信号监控”**
→ 提供需要监控的RSS订阅源
→ 配置目标市场ID和关键词
→ 启用定时扫描功能

**用户：“检查这个订阅源中的交易信号”**
→ 运行：`python signal_sniper.py --feed "URL" --scan-only`
→ 查看匹配到的文章和潜在交易机会

**用户：“抓取CoinDesk上的比特币相关新闻”**
→ 使用CoinDesk的RSS订阅源和比特币相关市场
→ 查看匹配结果并决定是否进行交易

**用户：“我们处理了哪些信号？”**
→ 运行：`python signal_sniper.py --history`
→ 查看最近处理的文章和交易记录

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
- 可能是RSS订阅源中没有最新文章
- 尝试使用`--scan-only`查看订阅源内容

**“因市场方向频繁变动而跳过交易”**
- 市场波动较大，建议等待或获取新信息后再交易

**“滑点过高”**
- 市场流动性差，建议减小交易规模或跳过交易

**“文章已处理过”**
- 该文章已被记录在系统中（避免重复计算）

**“外部钱包需要预签名订单”**
- 确保环境变量`WALLET_PRIVATE_KEY`已设置
- 当此变量存在时，SDK会自动签名订单，无需手动操作
- 解决方法：`export WALLET_PRIVATE_KEY=0x<your-polymarket-wallet-private-key>`
- 请勿尝试手动签名订单或修改脚本代码，SDK会自动处理

**“账户余额显示为0美元，但我有USDC在Polygon上”**
- Polymarket使用的是**USDC.e**（桥接后的USDC，合约地址`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`），而非原生USDC
- 如果您最近将USDC桥接到了Polygon，可能需要先将原生USDC转换为USDC.e后再进行交易

**如何寻找优质的RSS订阅源**

选择信号来源的建议：
- **Google News RSS**：`https://news.google.com/rss/search?q=YOUR_TOPIC`
- **专业领域来源**：通常比主流新闻更具有参考价值（价格变动较小）
- **官方来源**：政府或公司的公告
- **Twitter列表的RSS订阅**：可以使用Nitter或RSS.app等工具

该工具在以下情况下效果最佳：
- 订阅源与目标市场相关
- 您有明确的关键词来过滤无关信息
- 来源能在主流媒体之前发布新闻