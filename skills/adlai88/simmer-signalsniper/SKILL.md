---
name: simmer-signalsniper
displayName: Polymarket Signal Sniper
description: 从您自己的信号源中捕捉 Polymarket 的投资机会。使用具备 Trading Agent 级别安全性的工具来监控 RSS 源。
metadata: {"clawdbot":{"emoji":"🎯","requires":{"env":["SIMMER_API_KEY"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
version: "1.3.2"
---

# Polymarket Signal Sniper  
这是一个用于捕捉市场信号的自动化工具，它结合了Simmer的交易智能系统。  

## 适用场景  
当用户希望：  
- 监控RSS源以寻找交易机会；  
- 在市场反应之前基于突发新闻进行交易；  
- 自定义信号来源和关键词；  
- 为交易设置高级的安全保障机制时，可以使用此工具。  

## 快速命令  
（具体命令内容请参见**```bash
# Check account balance and positions
python scripts/status.py

# Detailed position list
python scripts/status.py --positions
```**）  

**API参考**：  
- 基础URL：`https://api.simmer.markets`  
- 认证方式：`Authorization: Bearer $SIMMER_API_KEY`  
- 财产信息：`GET /api/sdk/portfolio`  
- 持仓情况：`GET /api/sdk/positions`  

## 快速上手（临时使用）  
用户需提供RSS源和市场信息：  
（具体操作内容请参见**```
User: "Watch this RSS feed for greenland news: https://news.google.com/rss/search?q=greenland"
User: "Snipe any news about trump from this feed"
```**）  
通过`--feed`和`--market`参数运行脚本：  
（具体运行命令请参见**```bash
python signal_sniper.py --feed "https://news.google.com/rss/search?q=greenland" --market "greenland-acquisition" --dry-run
```**）  

## 持久化设置（可选）  
若需自动定期扫描市场，可通过环境变量进行配置：  
| 设置          | 环境变量            | 默认值            | 说明                          |  
|----------------|------------------|------------------|----------------------------------|  
| RSS源          | `SIMMER_SNIPER_feedS`       | （无）             | 用逗号分隔的RSS地址列表                |  
| 市场ID          | `SIMMER_SNIPERMARKETS`      | （无）             | 用逗号分隔的市场ID列表                |  
| 关键词          | `SIMMER_SNIPER_KEYWORDS`       | （无）             | 用于匹配的关键词列表                |  
| 交易置信度        | `SIMMER_SNIPER_CONFIDENCE`     | 0.7              | 最低交易置信度（0.0–1.0）                |  
| 单次交易最大金额     | `SIMMER_SNIPER_MAX_USD`      | 25               | 每次交易的最大金额                |  
| 每次扫描最大交易数量   | `SIMMER_SNIPER_MAX_TRADES`     | 5               | 每次扫描的最大交易数量                |  

**Polymarket限制**：  
- 每笔订单至少需购买5股股票；  
- 低于此数量的订单将被拒绝，并显示错误信息。  

## 工作原理  
脚本每个周期会执行以下操作：  
1. 访问配置的RSS源；  
2. 根据关键词过滤文章；  
3. 将匹配到的文章与目标市场进行匹配；  
4. 对每个匹配结果，调用SDK接口进行安全检查（例如：是否已持有该资产、市场是否处于波动期、市场流动性如何等）；  
5. 如果安全检查通过，用户（Claude）会分析信号；  
6. 若确认信号可靠，通过SDK执行交易；  
7. 记录已处理的文章以避免重复交易。  

## 运行脚本  
**执行扫描（默认为模拟运行，不进行交易）**：  
（具体命令请参见**```bash
python signal_sniper.py
```**）  
**执行实际交易**：  
（具体命令请参见**```bash
python signal_sniper.py --live
```**）  
**查看信号信息（不执行交易）**：  
（具体命令请参见**```bash
python signal_sniper.py --scan-only
```**）  
**查看当前配置**：  
（具体命令请参见**```bash
python signal_sniper.py --config
```**）  
**单次运行时覆盖配置**：  
（具体命令请参见**```bash
python signal_sniper.py --feed "https://..." --keywords "trump,greenland" --market "abc123"
```**）  
**查看已处理的文章**：  
（具体命令请参见**```bash
python signal_sniper.py --history
```**）  

## 解读警告信息  
在交易前，请务必查看警告信息。常见警告及其对应操作如下：  
| 警告          | 建议操作                |  
|----------------|------------------|  
| `MARKET RESOLVED`   | 不要交易                |  
| `HIGH URGENCY: Resolves in Xh` | 评估信号是否及时            |  
| `flip_flop_warning: SEVERE` | 警告：市场波动剧烈，谨慎操作       |  
| `flip_flop_warning: CAUTION` | 警告：需更明确的信号            |  
| `Wide spread (X%)`    | 减少持仓规模或跳过交易           |  
| `Simmer AI signal: X% more bullish/bearish` | 参考Simmer的预测方向            |  

## 分析信号  
找到匹配文章后，请仔细分析：  
1. **阅读标题和摘要**：了解新闻内容；  
2. **检查是否符合交易条件**：确认新闻是否符合预设的判断标准；  
3. **评估置信度**（0.0–1.0）：分析信号与交易条件的关联程度及来源可靠性；  
4. **仅在满足以下条件时交易**：  
   - 交易置信度高于阈值（默认0.7）；  
   - 无严重警告；  
   - 信号与判断标准一致。  

## 示例对话  
**用户：“为Greenland市场设置新闻监控”**  
→ 提供要监控的RSS源；  
→ 配置市场ID和关键词；  
→ 启用定时扫描功能。  

**用户：“检查该RSS源中的交易信号”**  
→ 运行：`python signal_sniper.py --feed "URL" --scan-only`  
→ 查看匹配到的文章及潜在交易机会。  

**用户：“抓取CoinDesk上的比特币相关新闻”**  
→ 指定CoinDesk的RSS源和相关市场；  
→ 查看匹配结果并决定是否进行交易。  

**用户：“我们处理了哪些信号？”**  
→ 运行：`python signal_sniper.py --history`  
→ 查看最近处理的文章及交易记录。  

## 示例交易流程  
（具体交易流程请参见**```
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
```**）  

## 故障排除**  
- **“未配置RSS源”**：  
  提示：提供RSS地址（例如：`watch this RSS: https://...`）；  
  或设置环境变量`SIMMER_SNIPER_feedS`。  
- **“未找到匹配文章”**：  
  确认关键词是否正确；  
  可尝试使用`--scan-only`查看RSS源内容。  
- **“因市场波动被跳过”**：  
  市场波动剧烈，建议等待或获取新信息后再交易。  
- **“滑点过高”**：  
  市场流动性差，可减少交易规模或跳过交易。  
- **“文章已处理过”**：  
  确认文章未被重复处理。  

## 选择RSS源的建议：  
- **Google News RSS**：`https://news.google.com/rss/search?q=YOUR_TOPIC`  
- **专业领域来源**：通常比主流新闻更可靠；  
- **官方来源**：政府或公司发布的公告；  
- **Twitter列表的RSS版本**：可使用Nitter或RSS.app等工具获取。  

**使用提示**：  
- 确保RSS源与目标市场相关；  
- 使用特定关键词过滤无关信息；  
- 优先选择在主流媒体之前发布信息的来源。