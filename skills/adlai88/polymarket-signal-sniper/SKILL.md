---
name: polymarket-signal-sniper
displayName: Polymarket Signal Sniper
description: 从您自己的信号源中捕捉 Polymarket 的投资机会。使用具备 Trading Agent 级别安全性的工具来监控 RSS 源。
metadata: {"clawdbot":{"emoji":"🎯","requires":{"env":["SIMMER_API_KEY"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
version: "1.3.3"
published: true
---

# Polymarket Signal Sniper  
——为您的交易提供精准的信号与智能分析  

## 适用场景  
当您希望：  
- 监控 RSS 源以寻找交易机会；  
- 在市场反应之前根据突发新闻进行交易；  
- 自定义信号来源和关键词；  
- 为交易获得高级别的安全保障时，可使用此工具。  

## 快速命令  
（具体命令内容请参见下方代码块）  

**API 参考：**  
- 基本 URL：`https://api.simmer.markets`  
- 认证方式：`Authorization: Bearer $SIMMER_API_KEY`  
- 财产组合信息：`GET /api/sdk/portfolio`  
- 持仓情况：`GET /api/sdk/positions`  

## 快速入门（临时使用）  
用户需提供 RSS 源和目标市场信息：  
（具体操作步骤请参见下方代码块）  
→ 使用 `--feed` 和 `--market` 参数运行脚本：  
（具体命令内容请参见下方代码块）  

## 持久化设置（可选）  
如需自动定期扫描，可通过环境变量进行配置：  
| 设置 | 环境变量 | 默认值 | 说明 |  
|---------|---------------------|---------|-------------|  
| RSS 源 | `SIMMER_SNIPER_FEEDS` | （空） | 以逗号分隔的 RSS URL 列表 |  
| 目标市场 | `SIMMER_SNIPERMARKETS` | （空） | 以逗号分隔的市场 ID 列表 |  
| 关键词 | `SIMMER_SNIPER_KEYWORDS` | （空） | 用于匹配的关键词 |  
| 交易置信度 | `SIMMER_SNIPER_CONFIDENCE` | 0.7 | 最低交易置信度（0.0–1.0） |  
| 单次交易最大金额 | `SIMMER_SNIPER_MAX_USD` | 25 | 每笔交易的最大金额 |  
| 每次扫描的最大交易数量 | `SIMMER_SNIPER_MAX_TRADES` | 5 | 每次扫描的最大交易次数 |  

**Polymarket 限制规则：**  
- 每笔订单至少需购买 5 股；  
- 低于此数量的订单将被拒绝，并显示错误信息。  

## 工作原理  
脚本每个周期会执行以下操作：  
1. 访问配置的 RSS 源；  
2. 根据关键词过滤文章；  
3. 将匹配到的文章与目标市场进行匹配；  
4. 对于每个匹配结果，调用 SDK 的相关接口进行安全检查（例如：当前是否已持有该资产、市场是否具有流动性等）；  
5. 如果安全检查通过，您（Claude）将分析信号并决定是否执行交易；  
6. 执行交易后，系统会跟踪已处理的文章以避免重复记录。  

## 运行脚本  
**执行扫描（默认为模拟运行，不进行交易）：**  
（具体命令内容请参见下方代码块）  
**执行实际交易：**  
（具体命令内容请参见下方代码块）  
**仅查看信号而不执行交易：**  
（具体命令内容请参见下方代码块）  
**查看当前配置：**  
（具体命令内容请参见下方代码块）  
**针对单次运行进行自定义设置：**  
（具体命令内容请参见下方代码块）  
**查看已处理的文章：**  
（具体命令内容请参见下方代码块）  

## 解读系统警告  
**交易前务必查看警告信息！**  
系统会显示以下警告：  
| 警告类型 | 应对措施 |  
|---------|--------|  
| `MARKET RESOLVED` | 不要交易 |  
| `HIGH URGENCY: Resolves in Xh` | 评估信号是否及时 |  
| `flip_flop_warning: SEVERE` | 警告：市场波动剧烈，需谨慎 |  
| `flip_flop_warning: CAUTION` | 警告：需等待更明确的信号 |  
| `Wide spread (X%)` | 减少持仓规模或跳过交易 |  
| `Simmer AI signal: X% more bullish/bearish` | 参考 Simmer 的预测意见 |  

## 分析信号  
找到匹配文章后，请仔细分析：  
1. **阅读标题和摘要**：了解新闻内容；  
2. **检查相关标准**：确认该新闻是否符合交易条件；  
3. **评估置信度**（0.0–1.0）：判断信号与交易条件的关联程度及来源可靠性；  
4. **仅在满足以下条件时交易**：  
  - 信任度高于阈值（默认 0.7）；  
  - 无严重警告；  
  - 信号符合交易条件。  

## 示例对话：  
**用户：“为 Greenland 市场设置新闻监控”**  
→ 提供要监控的 RSS 源；  
→ 配置市场 ID 和关键词；  
→ 启用定时扫描功能。  
**用户：“查看该 RSS 源中的交易信号”**  
→ 运行：`python signal_sniper.py --feed "URL" --scan-only`；  
→ 查看匹配到的文章及潜在交易机会。  
**用户：“获取 CoinDesk 上的比特币相关新闻”**  
→ 使用 CoinDesk 的 RSS 源和比特币相关市场进行扫描；  
→ 查看匹配结果并决定是否交易。  
**用户：“我们处理了哪些信号？”**  
→ 运行：`python signal_sniper.py --history`；  
→ 查看最近的文章及交易记录。  

## 示例交易流程  
（具体交易流程请参见下方代码块）  

## 故障排除：  
- **“未配置 RSS 源”**：  
  提供 RSS 源地址（例如：`watch this RSS: https://...`）；  
  或设置环境变量 `SIMMER_SNIPER_FEEDS`。  
- **“未找到匹配文章”**：  
  确认关键词是否正确；  
  或检查 RSS 源是否包含最新文章；  
  尝试使用 `--scan-only` 选项查看内容。  
- **“因市场波动剧烈而跳过交易”**：  
  市场流动性差，建议等待或获取新信息后再交易。  
- **“滑点过高”**：  
  减少交易规模或跳过交易。  
- **“文章已处理过”**：  
  系统会避免重复处理同一篇文章。  

## 选择 RSS 源的建议：  
- **Google News RSS**：`https://news.google.com/rss/search?q=YOUR_TOPIC`  
- **专业领域来源**：通常比主流媒体更可靠；  
- **官方来源**：政府或公司发布的公告；  
- **Twitter 列表（RSS 格式）**：可使用 Nitter 或 RSS.app 等工具获取。  

**使用提示：**  
- 确保 RSS 源与目标市场相关；  
- 使用特定关键词过滤无关信息；  
- 选择在主流媒体之前发布信息的来源，以获取更及时的信号。