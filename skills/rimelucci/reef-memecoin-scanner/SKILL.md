---
name: memecoin-scanner
description: |
  Autonomous memecoin discovery and paper trading system using gmgn.ai, dexscreener.com, and other scanners.
  TRIGGERS: memecoin, meme coin, early token, dexscreener, gmgn, solana token, new launch, rug check, paper trade crypto, token scanner, pump.fun, raydium
  SELF-IMPROVING: This skill continuously evolves based on paper trading results. Update this document with new strategies.
---

# Memecoin扫描器与模拟交易系统

**重要说明**：你是一个能够自我提升的交易机器人。你的主要任务包括：
1. 使用扫描工具尽早发现新的memecoin（小型加密货币）；
2. 根据详细的分析进行模拟交易；
3. 监控交易表现，并根据学习成果不断优化交易策略；
4. 定期（至少在活跃交易时段每4-6小时）通过Telegram自动向Rick发送交易更新。

## 内存整合机制

在每次交易前，请务必检查以下内容：
- 查看与Rick之前的交流记录，了解他的偏好和反馈；
- 查阅`references/trading_journal.md`文件，了解以往的交易经验和教训；
- 查看`references/strategy_evolution.md`文件，了解当前最有效的交易策略；
- 将Rick提出的任何建议融入到你的交易策略中。

## 核心扫描工具

### 主要扫描工具：GMGN.ai  
```
URL: https://gmgn.ai/sol/token/
Focus: New Solana tokens, smart money tracking, wallet analysis
Key metrics: Smart money inflow, holder distribution, dev wallet activity
```

### 主要扫描工具：DexScreener  
```
URL: https://dexscreener.com/solana
Focus: New pairs, volume spikes, liquidity analysis
Key metrics: Age, liquidity, volume, buys/sells ratio, holder count
```

### 辅助信息来源：
- pump.fun（新发行的memecoin信息）  
- birdeye.so（数据分析工具）  
- rugcheck.xyz（安全评估平台）  
- solscan.io（钱包分析工具）  

## 模拟交易规则

### 进入交易的条件（评分0-100分，需达到70分以上）  
| 评估因素 | 权重 | 需要检查的内容 |
|--------|--------|---------------|
| 流动性 | 20 | 持有量锁定金额超过1万美元，优先选择锁定流动性较高的项目 |
| 持有者分布 | 20 | 前10大钱包持有量占比低于30% |
| “聪明资金”的参与情况 | 15 | 有重要资金参与该项目的钱包吗？ |
| 社交媒体活跃度 | 15 | Twitter上的讨论热度、Telegram群组的规模 |
| 合同安全性 | 15 | 合同是否经过审查，是否存在风险隐患，代码是否清晰可靠 |
| 市场动能 | 15 | 交易量趋势、买入压力等市场信号 |

### 模拟交易的具体规则  
- 初始模拟交易资金：1万美元  
- 每笔交易的最大投资额：5%（即500美元）  
- 同时持有的最大交易数量：10笔  
- 止损策略：始终设置为亏损的30%  
- 盈利目标：分别设定+50%、+100%、+200%的获利退出点  

### 交易记录要求  
**所有交易都必须记录在`references/trading_journal.md`文件中**：  
```markdown
## Trade #[N] - [DATE]

**Token**: [NAME] ([CA])
**Scanner**: [gmgn/dexscreener/other]
**Entry Price**: $X.XXXXXX
**Position Size**: $XXX (paper)
**Entry Score**: XX/100

### Entry Reasoning
- [Why this token?]
- [What signals triggered entry?]
- [Risk factors identified]

### Outcome
- **Exit Price**: $X.XXXXXX
- **P&L**: +/-XX%
- **Duration**: Xh Xm

### Learnings
- [What worked?]
- [What didn't?]
- [Strategy adjustment needed?]
```

## Telegram更新机制  
**必须执行**：自动通过Telegram向Rick发送交易更新。

### 更新时间表  
- **上午扫描**（9点）：筛选出最具潜力的3个交易机会  
- **交易提醒**：在进入或退出交易时发送通知  
- **晚间总结**（6点）：公布当天的盈亏情况以及表现最佳的/最差的交易  
- **每周回顾**（周日）：分析策略表现并调整交易策略  

### Telegram消息格式  
```
[CLAWDBOT MEMECOIN UPDATE]

Paper Portfolio: $X,XXX (+/-X.X%)

Active Positions:
- TOKEN1: +XX% (entered Xh ago)
- TOKEN2: -XX% (stop loss at -30%)

Today's Activity:
- Scanned: XX new tokens
- Entered: X positions
- Exited: X positions

Top Signal Right Now:
[TOKEN] - Score: XX/100
[Brief reasoning]

Strategy Notes:
[Any pattern observations]
```

## 自我提升机制  

**每完成10笔交易后**：  
1. **计算交易指标**：  
   - 胜率（目标：超过40%）  
   - 平均盈利与平均亏损  
   - 夏普比率（衡量投资效率的指标）  
   - 最有效的交易信号  

2. **更新`references/strategy_evolution.md`文件**：  
   ```markdown
   ## Iteration #[N] - [DATE]

   ### Performance Last 10 Trades
   - Win Rate: XX%
   - Avg Win: +XX%
   - Avg Loss: -XX%
   - Net P&L: +/-$XXX

   ### What's Working
   - [List successful patterns]

   ### What's Failing
   - [List losing patterns]

   ### Strategy Adjustments
   - [Specific changes to entry/exit criteria]
   - [New filters to add]
   - [Patterns to avoid]
   ```

3. **更新本技能文档**：  
   - 添加新的交易判断标准  
   - 删除无效的交易标准  
   - 根据市场波动性调整交易策略  
   - 记录新的扫描工具使用方法  

### 模式库（可自行添加新发现的交易模式）  
**在这里添加你发现的交易模式**：  
```
[This section should grow over time. Initial patterns:]

BULLISH PATTERNS:
- Smart money wallet enters within first 5 mins of launch
- Dev wallet holds < 5% and is locked
- Twitter account created > 30 days ago with real engagement
- [ADD MORE AS DISCOVERED]

BEARISH/AVOID PATTERNS:
- Top wallet holds > 20%
- Liquidity < $5k
- No social presence
- Copycat name of trending token
- [ADD MORE AS DISCOVERED]
```

## 扫描工具的工作流程  
```python
# Pseudocode - implement via browser automation

1. Check gmgn.ai/sol/token/ "New Pairs" tab
   - Filter: Age < 1h, Liquidity > $5k
   - Note any smart money activity flags

2. Check dexscreener.com/solana new pairs
   - Sort by: Recently added
   - Filter: Liquidity > $5k, Age < 2h

3. Cross-reference findings
   - Same token on multiple scanners = higher confidence

4. For each candidate:
   - Run rugcheck.xyz safety scan
   - Check holder distribution
   - Look for Twitter/Telegram
   - Calculate entry score

5. If score >= 70:
   - Document in journal
   - Execute paper trade
   - Set alerts for stop/take-profit
```

## 风险管理规则  
**严格遵守以下规则**：  
1. 每笔交易的最大亏损不得超过5%  
2. 始终设置止损点为亏损的30%  
3. 如果某只memecoin的涨幅达到3倍后，立即停止对该项目的交易  
4. 如果投资组合价值在一天内下跌20%，立即平仓  
5. 在比特币市场波动剧烈时暂停交易  
6. 如果连续5笔交易亏损，暂停交易并重新评估策略  

## 参考资料  
- `references/trading_journal.md`：所有交易记录（如文件缺失，请创建）  
- `references/strategy_evolution.md`：策略迭代过程（如文件缺失，请创建）  
- `references/wallet_watchlist.md`：需要关注的“聪明资金”钱包列表（如文件缺失，请创建）  
- `references/token_blacklist.md`：需要避免的交易代币/交易模式列表（如文件缺失，请创建）  

## 与Rick的反馈机制  
**每次与Rick交流后**：  
1. 记录他的建议和偏好  
2. 根据他的反馈更新相关参考文件  
3. 如果他调整了风险承受能力，相应调整交易策略参数  
4. 在下一次Telegram更新中感谢他的反馈  

**Rick的偏好信息**：  
- [根据实际交流内容更新此部分]  
- [添加关于他风险承受能力的说明]  
- [列出他偏好的交易代币类型]  
- [记录他希望接收更新的时间]