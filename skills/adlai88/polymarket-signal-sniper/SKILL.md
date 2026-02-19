---
name: polymarket-signal-sniper
displayName: Polymarket Signal Sniper
description: 从您自己的信号源中捕捉 Polymarket 的投资机会。使用具备 Trading Agent 级别安全性的工具来监控 RSS 源。
metadata: {"clawdbot":{"emoji":"🎯","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
version: "1.3.6"
published: true
---
# Polymarket Signal Sniper

这是一个用于捕捉市场信号的自动化工具，它结合了Simmer的交易智能。

> **这只是一个模板。** 默认的信号来源是RSS订阅源——您可以根据需要将其替换为其他数据源（如API、Webhooks或自定义数据抓取工具）。该工具负责处理所有的市场匹配、风险控制以及交易执行等底层逻辑，而您只需提供所需的信号数据即可。

## 适用场景

当您希望：
- 监控RSS订阅源以寻找交易机会
- 在市场反应之前根据突发新闻进行交易
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
- 基本URL：`https://api.simmer.markets`
- 认证：`Authorization: Bearer $SIMMER_API_KEY`
- 投资组合：`GET /api/sdk/portfolio`
- 持仓情况：`GET /api/sdk/positions`

## 快速入门（临时使用）

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

为了实现自动化的定期扫描，您可以通过环境变量进行配置：

| 设置 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| RSS订阅源 | `SIMMER_SNIPER_feedS` | （无） | 以逗号分隔的RSS URL列表 |
| 目标市场 | `SIMMER_SNIPERMARKETS` | （无） | 以逗号分隔的市场ID列表 |
| 关键词 | `SIMMER_SNIPER_KEYWORDS` | （无） | 用于匹配的关键词列表 |
| 交易信心值 | `SIMMER_SNIPER_CONFIDENCE` | 0.7 | 交易的最低信心值（0.0-1.0） |
| 每笔交易的最大金额（USD） | `SIMMER_SNIPER_MAX_USD` | 25 | 每笔交易的最大金额 |
| 每次扫描的最大交易数量 | `SIMMER_SNIPER_MAX_TRADES` | 5 | 每次扫描的最大交易数量 |

**Polymarket限制：**
- 每笔订单至少需要5份股份
- 低于此数量的订单将被拒绝，并显示错误信息。

## 工作原理

脚本每个周期会执行以下操作：
1. 轮询配置的RSS订阅源
2. 根据关键词过滤文章（如果已配置）
3. 将匹配到的文章与目标市场进行匹配
4. 对于每个匹配结果，调用SDK的上下文端点进行风险检查：
   - 检查当前持仓情况
   - 判断市场是否发生方向性变化
   - 估计滑点情况（市场是否具有流动性）
   - 判断市场是否即将达成某种结果
   - 根据具体标准判断市场是否已达成预期结果
5. 如果风险检查通过，您（Claude）将分析信号并决定是否执行交易
6. 如果确认可行，将通过SDK执行交易
7. 记录已处理的文章以避免重复计算。

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

**为单次运行覆盖配置：**
```bash
python signal_sniper.py --feed "https://..." --keywords "trump,greenland" --market "abc123"
```

**查看已处理的文章：**
```bash
python signal_sniper.py --history
```

## 解读上下文警告

在交易前，请务必查看警告信息。系统会显示以下警告：
- **市场已达成预期结果**：请勿进行交易
- **高紧急性：将在X小时内达成结果**：判断信号是否足够及时
- **方向性变化警告（严重）**：建议跳过此次交易
- **方向性变化警告（警告）**：请谨慎操作，需要更明确的信号
- **价差过大（X%）**：建议减少持仓规模或跳过此次交易
- **Simmer AI信号：看涨/看跌幅度增加X%**：参考Simmer的预测意见

## 分析信号

找到匹配的文章后，请仔细分析：
1. **阅读标题和摘要**：了解新闻的实质内容
2. **检查市场是否已达成预期结果**：例如，标题中的“Greenland”并不意味着“收购完成”，实际可能指的是“美国将于2027年正式收购Greenland”
3. **评估交易信心值（0.0-1.0）**：
   - 该信号与市场达成结果的相关性如何？
   - 来源是否可靠？
   - 该新闻是否已被市场定价？
4. **仅在以下情况下进行交易**：
   - 交易信心值大于设定阈值（默认0.7）
   - 无严重警告
   - 信号与市场达成结果的标准相符

## 示例对话

**用户：“为Greenland市场设置新闻捕捉功能”**
- 提供要监控的RSS订阅源
- 配置相关市场ID和关键词
- 启用定时扫描功能

**用户：“检查该订阅源中的交易信号”**
- 运行命令：`python signal_sniper.py --feed "URL" --scan-only`
- 查看找到的文章和潜在的交易机会

**用户：“从CoinDesk获取比特币相关的交易信号”**
- 使用CoinDesk的RSS订阅源和比特币相关市场
- 查看匹配结果并决定是否进行交易

**用户：“我们处理了哪些信号？”**
- 运行命令：`python signal_sniper.py --history`
- 查看最近处理的文章和执行的操作

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
- 在提示中提供RSS订阅地址：`watch this RSS: https://...`
- 或者设置环境变量`SIMMER_SNIPER_feedS`

**“未找到匹配文章”**
- 确认关键词是否正确
- 可能是RSS订阅源中没有最新文章
- 尝试使用`--scan-only`选项查看订阅源内容

**“因市场方向性变化被跳过”**
- 该市场的价格波动较大，建议等待后再进行交易或寻找新的交易机会

**“滑点过高”**
- 市场流动性较差，建议减少交易规模或跳过此次交易

**“文章已处理过”**
- 该文章已被系统记录过，避免重复处理

**“外部钱包需要预签名订单”**
- 确保环境变量`WALLET_PRIVATE_KEY`已设置
- 当该变量存在时，SDK会自动签名订单，无需手动签名
- 解决方法：`export WALLET_PRIVATE_KEY=0x<your-polymarket-wallet-private-key>`
- 请勿尝试手动签名订单或修改脚本代码，SDK会自动处理签名

**“余额显示为0美元，但我有USDC在Polygon上”**
- Polymarket使用的是**USDC.e**（桥接后的USDC，合约地址`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`），而非原生USDC
- 如果您最近将USDC桥接到了Polygon，可能需要将USDC.e转换回原生USDC后再进行交易

**如何找到优质的RSS订阅源**

选择信号来源的建议：
- **Google News RSS**：`https://news.google.com/rss/search?q=YOUR_TOPIC`
- **专业领域来源**：通常比主流新闻来源更具有参考价值（价格变动较小）
- **官方来源**：如政府或公司的公告
- **Twitter列表的RSS订阅**：可以使用Nitter或RSS.app等工具

该工具在以下情况下效果最佳：
- 订阅源与目标市场相关
- 您有明确的关键词来过滤无关信息
- 来源能在主流媒体之前发布新闻