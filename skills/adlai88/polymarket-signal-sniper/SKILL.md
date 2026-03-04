---
name: polymarket-signal-sniper
description: 从您自己的信号源中捕捉 Polymarket 的投资机会。使用与 Trading Agent 同级别的安全机制来监控 RSS 源。
metadata:
  author: Simmer (@simmer_markets)
  version: "1.3.7"
  displayName: Polymarket Signal Sniper
  difficulty: intermediate
---# Polymarket Signal Sniper

这是您的交易辅助工具——Simmer提供的智能交易信号服务。

> **这是一个模板。** 默认的信号来源是RSS订阅源，您可以根据需要将其替换为其他数据源（API、Webhook或自定义数据抓取工具）。该工具会处理所有的市场匹配、风险控制以及交易执行等底层逻辑，而您的代理程序则负责生成具体的交易策略。

## 适用场景

当用户希望：
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

**用户提供RSS订阅源和目标市场：**
```
User: "Watch this RSS feed for greenland news: https://news.google.com/rss/search?q=greenland"
User: "Snipe any news about trump from this feed"
```

→ 使用`--feed`和`--market`参数运行脚本：
```bash
python signal_sniper.py --feed "https://news.google.com/rss/search?q=greenland" --market "greenland-acquisition" --dry-run
```

## 持久化设置（可选）

为了实现自动化的定期扫描，请通过环境变量进行配置：

| 设置 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| RSS订阅源 | `SIMMER_SNIPER_FEEDS` | （无） | 用逗号分隔的RSS链接列表 |
| 目标市场 | `SIMMER_SNIPERMARKETS` | （自动检测） | 用逗号分隔的市场ID列表（若未设置关键词，则自动从用户提供的关键词中识别） |
| 关键词 | `SIMMER_SNIPER_KEYWORDS` | （无） | 用于匹配的新闻关键词 |
| 交易置信度 | `SIMMER_SNIPER_CONFIDENCE` | 0.7 | 最低交易置信度（0.0-1.0） |
| 每笔交易的最大金额 | `SIMMER_SNIPER_MAX_USD` | 25 | 每笔交易的最大金额 |
| 每次扫描的最大交易数量 | `SIMMER_SNIPER_MAX_TRADES` | 5 | 每次扫描的最大交易次数 |

**Polymarket的限制：**
- 每笔订单至少需要5份资产
- 低于此数量的订单将被拒绝，并显示错误信息。

## 工作原理

脚本会定期执行以下操作：
1. 访问配置的RSS订阅源
2. 根据关键词过滤文章（如已配置）
3. 将匹配到的文章与目标市场进行匹配（若未配置市场，则自动从关键词中识别）
4. 对于每个匹配结果，调用SDK的上下文接口进行风险评估：
   - 检查当前持仓情况
   - 判断市场是否发生方向性变化
   - 估算滑点风险
   - 评估市场是否即将达成某种状态
   - 确定影响市场的具体因素
5. 如果风险评估通过，根据文章内容判断交易方向
6. 通过SDK执行交易（遵守每次扫描的最大交易数量限制）
7. 记录已处理的文章以避免重复计算。

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

**针对单次运行进行临时设置：**
```bash
python signal_sniper.py --feed "https://..." --keywords "trump,greenland" --market "abc123"
```

**查看已处理的文章：**
```bash
python signal_sniper.py --history
```

## 解读风险警告

在交易前，请务必查看风险警告。系统会显示以下警告信息：
- **MARKET RESOLVED**：请勿交易
- **HIGH URGENCY: Resolves in Xh**：判断信号是否足够及时
- **flip_flop_warning: SEVERE**：建议跳过此次交易（市场方向变化过于频繁）
- **flip_flop_warning: CAUTION**：请谨慎操作，需要更明确的交易信号
- **Wide spread (X%)**：建议减小持仓规模或跳过此次交易
- **Simmer AI signal: X% more bullish/bearish**：参考Simmer的预测意见

## 分析交易信号

找到匹配的文章后，请仔细分析：
1. **阅读标题和摘要**：了解新闻的实质内容
2. **检查市场达成条件**：确认该新闻是否真正符合交易条件
   - 例如，标题中的“Greenland”并不一定意味着“收购完成”
   - 实际的达成条件可能是“美国将于2027年前正式收购格陵兰”
   - 该新闻是否会影响相关市场的价格走势？
3. **评估置信度**（0.0-1.0）：
   - 该信号与市场达成条件的关联程度如何？
   - 来源是否可靠？
   - 该新闻是否已经被市场定价？
4. **仅当满足以下条件时才进行交易**：
   - 交易置信度高于阈值（默认0.7）
   - 无严重风险警告
   - 信号内容与市场达成条件一致

## 示例对话

**用户：“为格陵兰市场设置新闻监控”**
- 提供需要监控的RSS订阅源
- 配置目标市场ID和关键词
- 启用定时扫描功能

**用户：“检查这个订阅源是否有交易信号”**
- 运行：`python signal_sniper.py --feed "URL" --scan-only`
- 查看找到的文章和潜在的交易机会

**用户：“从CoinDesk获取比特币相关交易信号”**
- 使用CoinDesk的RSS源和比特币相关市场进行扫描
- 查看匹配结果并决定是否进行交易

**用户：“我们处理了哪些交易信号？”**
- 运行：`python signal_sniper.py --history`
- 查看最近的处理记录和交易结果

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

- **“未配置RSS订阅源”**：在命令行中提供RSS地址，例如：`watch this RSS: https://...`
- 或者设置环境变量`SIMMER_SNIPER_feedS`

- **“未找到匹配文章”**：
  - 确认关键词是否正确
  - 可能是RSS源最近没有更新文章
  - 尝试使用`--scan-only`选项查看订阅源内容

- **“因市场方向变化频繁而跳过交易”**：
  - 市场方向变化过于频繁，建议稍后再试或寻找新的交易机会

- **“滑点过高”**：
  - 市场流动性不足，建议减小交易规模或跳过此次交易

- **“文章已处理过”**：
  - 该文章已被系统记录过，避免重复处理

- **“外部钱包需要预签名订单”**：
  - 确保环境变量`WALLET_PRIVATE_KEY`已设置
  - 当该变量存在时，SDK会自动完成订单签名，无需手动操作
  - 解决方法：`export WALLET_PRIVATE_KEY=0x<your-polymarket-wallet-private-key>`
  - 请勿尝试手动签名订单或修改脚本代码

- **“账户余额显示为0美元，但我有USDC在Polygon上”**：
  - Polymarket使用的是**USDC.e**（桥接后的USDC，合约地址`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`），而非原生USDC
  - 如果您最近将USDC桥接到了Polygon，可能需要先将USDC转换为USDC.e后再进行交易

**寻找优质的RSS订阅源**

选择信号来源的建议：
- **Google News RSS**：`https://news.google.com/rss/search?q=YOUR_TOPIC`
- **专业领域来源**：通常比主流新闻来源更具有参考价值（价格变动较小）
- **官方来源**：政府或公司的公告
- **Twitter列表的RSS订阅**：可以使用Nitter或RSS.app等工具

该工具在以下情况下效果最佳：
- 订阅源与目标市场相关
- 您有明确的关键词来过滤无关信息
- 来源能在主流媒体之前发布新闻