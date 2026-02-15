---
name: simmer-signalsniper
displayName: Polymarket Signal Sniper
description: 从您自己的信号源中捕捉 Polymarket 的投资机会。使用具有 Trading Agent 级别安全性的工具来监控 RSS 源。
metadata: {"clawdbot":{"emoji":"🎯","requires":{"env":["SIMMER_API_KEY"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
version: "1.3.0"
---

# Polymarket Signal Sniper  
这是一个用于捕捉市场信号的自动化工具，它结合了Simmer的交易智能。  

## 何时使用该工具  
当用户希望：  
- 监控RSS源以寻找交易机会  
- 在市场反应之前根据突发新闻进行交易  
- 自定义信号来源和关键词  
- 为交易提供高级的安全保障时，可以使用该工具。  

## 快速命令  
（命令示例请参见下方代码块）  

**API参考：**  
- 基本URL：`https://api.simmer.markets`  
- 认证：`Authorization: Bearer $SIMMER_API_KEY`  
- 投资组合：`GET /api/sdk/portfolio`  
- 持仓情况：`GET /api/sdk/positions`  

## 快速入门（临时使用）  
**用户提供RSS源和市场信息：**  
（具体操作请参见下方代码块）  
→ 使用`--feed`和`--market`参数运行脚本：  
（示例命令：`python signal_sniper.py --feed "URL" --scan-only`）  

## 持久化设置（可选）  
如需自动定期扫描，可通过环境变量进行配置：  
| 设置 | 环境变量 | 默认值 | 说明 |  
|---------|---------------------|---------|-------------|  
| RSS源 | `SIMMER_SNIPER_feedS` | （无） | 以逗号分隔的RSS地址列表 |  
| 市场 | `SIMMER_SNIPERMARKETS` | （无） | 以逗号分隔的市场ID列表 |  
| 关键词 | `SIMMER_SNIPER_KEYWORDS` | （无） | 需要匹配的关键词列表 |  
| 交易置信度 | `SIMMER_SNIPER_CONFIDENCE` | 0.7 | 最低交易置信度（0.0-1.0） |  
| 每笔交易最大金额 | `SIMMER_SNIPER_MAX_USD` | 25 | 每笔交易的最大金额 |  
| 每次扫描的最大交易数量 | `SIMMER_SNIPER_MAX_TRADES` | 5 | 每次扫描的最大交易数量 |  

**Polymarket限制：**  
- 每笔订单至少需5股股票；低于此数量的订单将被拒绝并显示错误信息。  

## 工作原理  
脚本每个周期会执行以下操作：  
1. 访问配置的RSS源  
2. 根据关键词过滤文章  
3. 将匹配到的文章与目标市场进行匹配  
4. 对每个匹配结果，调用SDK接口进行安全检查（例如：是否已持有该股票、市场是否具有流动性等）  
5. 如果安全检查通过，用户（Claude）会分析信号并决定是否执行交易  
6. 执行交易后，系统会记录已处理的文章以避免重复。  

## 运行该工具  
**进行扫描（默认为模拟运行，不执行交易）：**  
（示例命令：`python signal_sniper.py`）  
**执行真实交易：**  
（示例命令：`python signal_sniper.py --feed "URL" --trade`）  
**仅查看信号而不执行交易：**  
（示例命令：`python signal_sniper.py --scan-only`）  
**查看当前配置：**  
（示例命令：`python signal_sniper.py --config`）  
**针对单次运行进行自定义设置：**  
（示例命令：`python signal_sniper.py --config "RSS=URL, markets=MARKET_ID, keywords=KEYWORDLIST"`）  
**查看已处理的文章：**  
（示例命令：`python signal_sniper.py --history`）  

## 解读警告信息  
在交易前，请务必查看警告信息：  
| 警告 | 处理方式 |  
|---------|--------|  
| `MARKET RESOLVED` | 不要交易 |  
| `HIGH URGENCY: Resolves in Xh` | 评估信号是否及时 |  
| `flip_flop_warning: SEVERE` | 警告：市场波动频繁，需谨慎操作 |  
| `flip_flop_warning: CAUTION` | 警告：需要更明确的信号 |  
| `Wide spread (X%)` | 减少持仓规模或跳过该交易 |  
| `Simmer AI signal: X% more bullish/bearish` | 参考Simmer的预测意见 |  

## 分析信号  
找到匹配的文章后，请仔细分析：  
1. **阅读标题和摘要**：了解新闻内容。  
2. **检查是否符合交易条件**：确认新闻是否符合交易标准（例如，“greenland”并不一定意味着“收购完成”）。  
3. **评估置信度**（0.0-1.0）：判断信号与交易条件的关联程度及来源的可信度。  
4. **仅在执行交易时满足以下条件**：  
  - 置信度高于阈值（默认0.7）  
  - 无严重警告  
  - 信号符合交易条件。  

## 示例对话：  
**用户：“为Greenland市场设置新闻监控”**  
  - 提供要监控的RSS源  
  - 配置市场ID和关键词  
  - 启用定时扫描功能  

**用户：“检查该RSS源中的交易信号”**  
  - 运行：`python signal_sniper.py --feed "URL" --scan-only`  
  - 查看匹配到的文章及潜在交易机会  

**用户：“抓取CoinDesk上的比特币相关新闻”**  
  - 使用CoinDesk的RSS源和比特币相关市场  
  - 查看匹配结果并决定是否进行交易  

**用户：“我们处理了哪些信号？”**  
  - 运行：`python signal_sniper.py --history`  
  - 查看最近的文章及交易记录  

## 示例交易流程  
（交易流程示意图请参见下方代码块）  

## 故障排除：  
- **“未配置RSS源”**：提供RSS地址或设置`SIMMER_SNIPER_feedS`环境变量。  
- **“未找到匹配文章”**：检查关键词是否正确；RSS源可能没有最新文章；尝试使用`--scan-only`模式查看内容。  
- **“因市场波动频繁而跳过交易”**：等待市场稳定后再操作或获取新信息。  
- **“滑点过高”**：市场流动性差，减少交易规模或跳过交易。  
- **“文章已处理过”**：系统会避免重复处理相同文章。  

## 选择RSS源的建议：  
- **Google News RSS**：`https://news.google.com/rss/search?q=YOUR_TOPIC`  
- **专业领域来源**：通常比主流媒体更新及时  
- **官方来源**：政府或公司公告  
- **Twitter列表的RSS订阅**：可使用Nitter或RSS.app等工具  

**使用提示：**  
- 确保RSS源与目标市场相关；  
- 使用特定关键词过滤无关信息；  
- 选择在主流媒体之前发布信息的来源，以便更早获取交易机会。