---
name: memecoin-scanner
description: |
  Solana memecoin discovery and trading sub-strategy. Part of paper-trader skill.
  Uses gmgn.ai, dexscreener.com, pump.fun for early token identification.
  SUB-STRATEGY: Managed by parent paper-trader orchestrator.
---

# Memecoin扫描策略

**父策略**：本策略是`paper-trader`的子策略。`../../SKILL.md`中定义的 portfolio-level（投资组合级别）规则具有优先级。

**职责**：通过系统自动扫描工具发现早期出现的Solana加密货币，并基于详细的分析进行交易决策。

## 与上级协调器的集成

**向上级协调器报告：**
- 将所有交易记录到`references/trading_journal.md`文件中。
- 上级协调器会查看这些记录以获取统一的投资组合视图，并执行跨策略的风险限制管理。

**交易前需确认的内容：**
- 核实`../../references/master_portfolio.md`中规定的投资组合风险限额。
- 检查不同策略之间的加密货币投资相关性。
- 遵守上级协调器设定的风险等级（🟢/🟡/🟠/🔴）。

**你在系统中的工作内容：**
1. 使用扫描工具发现潜在的memecoin项目。
2. 对这些项目进行模拟交易（paper trading），并详细记录交易理由。
3. 监控交易表现，并根据经验不断优化策略。
4. 定期（至少在活跃交易时段每4-6小时）通过Telegram主动向Rick发送交易更新。

## 内部信息共享机制

**每次交易前务必检查：**
- 查看与Rick之前的交流记录，了解他的偏好和反馈。
- 查阅`references/trading_journal.md`中的交易记录和经验总结。
- 研究`references/strategy_evolution.md`中当前推荐的策略。
- 将Rick的建议融入自己的交易策略中。

## 核心扫描工具

### 主要工具：GMGN.ai
```
URL: https://gmgn.ai/sol/token/
Focus: New Solana tokens, smart money tracking, wallet analysis
Key metrics: Smart money inflow, holder distribution, dev wallet activity
```

### 主要工具：DexScreener
```
URL: https://dexscreener.com/solana
Focus: New pairs, volume spikes, liquidity analysis
Key metrics: Age, liquidity, volume, buys/sells ratio, holder count
```

### 辅助工具：
- pump.fun（新币种发布信息）
- birdeye.so（数据分析工具）
- rugcheck.xyz（安全性评估工具）
- solscan.io（钱包分析工具）

## 模拟交易规则

### 入场标准（评分0-100分，需达到70分以上才能入场）
| 评估因素 | 权重 | 需要检查的内容 |
|--------|--------|---------------|
| 流动性 | 20 | 锁定资金超过1万美元，优先选择锁定期限较长的LP（Liquidity Lock-up） |
| 持币者分布 | 20 | 前10大钱包持有量占比低于30% |
| 智能资金参与度 | 15 | 是否有重要钱包参与交易？ |
| 社交媒体活跃度 | 15 | Twitter上的讨论热度及Telegram群组规模 |
| 合同安全性 | 15 | 合同是否经过审查，是否存在风险隐患（如“蜜罐”设计） |
| 市场动能 | 15 | 交易量趋势及买入压力 |

### 模拟交易参数设置
- 初始模拟交易资金：1万美元
- 每笔交易的最大金额：500美元
- 同时持有的最大头寸数量：10个
- 止损点：-30%（始终设置）
- 盈利目标：分别设定+50%、+100%、+200%的止盈点

### 交易记录要求
**所有交易必须记录在`references/trading_journal.md`文件中：**
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
**必须执行**：主动通过Telegram向Rick发送交易更新。

### 更新频率：
- **上午扫描**：发现的前3个最佳交易机会
- **交易提醒**：入场/出场时发送通知
- **晚间总结**：每日盈亏情况以及表现最佳的/最差的交易
- **每周回顾**：策略表现及调整方案

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

**每完成10笔交易后：**
1. **计算交易指标**：
   - 胜率（目标：>40%）
   - 平均盈利与平均亏损的对比
   - 夏普比率（Sharpe Ratio）
   - 最有效的入场信号

2. **更新`references/strategy_evolution.md`：**
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

3. **更新本策略文档**：
   - 添加新的入场标准
   - 删除无效的入场标准
   根据市场波动性调整交易头寸规模
   记录新的扫描技术

### 模式库（可随时添加新内容）
**发现新的交易模式后，请在此处添加：**
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
### 每小时自动扫描流程
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
**严格遵守以下规则：**
1. 每笔交易的亏损不得超过5%。
2. 始终设置-30%的止损点。
3. 如果某只资产连续亏损3次，立即停止交易。
4. 如果投资组合价值在一天内下跌20%，立即平仓。
5. 在BTC市场波动剧烈时避免交易。
6. 如果连续亏损5笔，暂停交易并重新评估策略。

## 参考资料
- `references/trading_journal.md`：所有交易记录（如文件缺失，请创建）
- `references/strategy_evolution.md`：策略迭代记录（如文件缺失，请创建）
- `references/wallet_watchlist.md`：需要关注的智能资金钱包列表（如文件缺失，请创建）
- `references/token_blacklist.md`：需要避免的交易代币/交易模式列表（如文件缺失，请创建）

## 与上级协调器的交互方式
- Rick的偏好设置保存在`../../references/rick_preferences.md`中。
**每次交易后**：
1. 将交易记录更新到`references/trading_journal.md`。
2. 上级协调器会将所有交易数据汇总到`../../references/master_portfolio.md`中。
3. 上级协调器负责统一发布通过Telegram发送的更新信息。

**策略级别的更新内容将发布到这里，投资组合级别的更新信息将发送给上级协调器。**