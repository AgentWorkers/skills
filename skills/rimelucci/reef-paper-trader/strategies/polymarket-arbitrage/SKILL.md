---
name: polymarket-arbitrage
description: |
  Polymarket arbitrage sub-strategy. Part of paper-trader skill.
  Identifies mispriced markets, correlated market discrepancies, cross-platform opportunities.
  SUB-STRATEGY: Managed by parent paper-trader orchestrator.
---

# Polymarket套利策略

**父策略**：本策略是`paper-trader`的子策略。`../../SKILL.md`中定义的 portfolio-level（投资组合级别）规则具有优先级。

**职责**：在Polymarket平台上识别并利用市场中性套利机会进行交易。

## 与上级策略的集成

**向上级策略报告：**
- 将所有套利交易记录到`references/arb_journal.md`文件中。
- 上级策略会读取该文件以获取统一的投资组合视图。
- 上级策略负责执行跨策略的风险限制。

**交易前需确认的内容：**
- 核实`../../references/master_portfolio.md`中定义的投资组合级别风险限额。
- 检查与Polymarket Research持仓的相关性（针对相同的市场）。
- 遵守上级策略设定的风险等级（🟢/🟡/🟠/🔴）。

**你在系统中的工作内容：**
1. 识别价格异常的市场及套利机会。
2. 通过书面记录进行模拟交易（paper trading）。
3. 跟踪交易表现，并根据经验更新策略。
4. 策略相关的更新信息会通过上级策略传递给你。

## 参考文件**

- `references/arb_journal.md` - 所有套利交易记录
- `references/strategy_evolution.md` - 策略的迭代过程
- `references/market_correlations.md` - 已知的市场相关性数据
- `../../references/rick_preferences.md` - Rick的个人偏好设置（上级策略的配置）

## 套利类型

### 类型1：同一市场内的价格异常

当“YES”与“NO”的概率之和不等于100%（扣除费用后）时，存在套利机会。

```
Example:
- "Will X happen?" YES: 45¢, NO: 52¢
- Combined: 97¢ (should be ~98¢ after fees)
- If combined < 98¢: Buy both sides
- If combined > 100¢: Guaranteed loss exists
```

**检测方法**：扫描“YES”与“NO”的概率之和与100%相差超过2%的市场。

### 类型2：相关市场套利

某些市场之间应存在数学上的关联，但实际上它们的价格存在异常。

```
Example:
- "Will Biden win election?" YES: 30¢
- "Will a Democrat win election?" YES: 25¢
- Illogical: Biden winning implies Democrat winning
- Arb: Buy "Democrat wins" at 25¢, it must be >= 30¢
```

**检测方法**：寻找价格存在不一致性的相关市场。

### 类型3：条件概率套利

某些市场的条件结果被错误定价。

```
Example:
- "Will X happen in January?" YES: 20¢
- "Will X happen in Q1?" YES: 15¢
- Illogical: Q1 includes January, must be >= January price
```

### 类型4：时间衰减套利

某些市场即将达成交易结果，但其价格尚未调整至接近正确的水平。

```
Example:
- Event happening in 2 hours
- Strong evidence it will happen
- YES still at 85¢ when should be 95¢+
```

### 类型5：跨平台套利

相同或类似的事件在不同平台上的价格存在差异。

```
Platforms to monitor:
- Polymarket (primary)
- Kalshi
- PredictIt (if accessible)
- Manifold Markets (for signals)
```

## 模拟交易协议

### 初始参数
- 模拟交易起始资金：10,000美元（USDC）
- 每次套利的最大收益：10%（即1,000美元）
- 预期最低套利利润：2%（扣除费用后）
- Polymarket平台的手续费：约2%（往返费用）

### 交易记录要求

**所有套利机会都必须记录到`references/arb_journal.md`文件中：**

```markdown
## Arb #[N] - [DATE]

**Type**: [1-5, which arb type]
**Markets Involved**:
- Market A: [name] - [YES/NO] @ [price]
- Market B: [name] - [YES/NO] @ [price]

**Theoretical Edge**: X.X%
**Position Size**: $XXX per leg
**Net Exposure**: $XXX or $0 (hedged)

### Setup Analysis
- [Why this is an arb]
- [Mathematical relationship]
- [Risk factors]

### Outcome
- **Resolution Date**: [date]
- **Result**: [which side won]
- **P&L**: +/-$XX
- **Actual Edge**: X.X%

### Learnings
- [What worked]
- [What was missed]
- [Adjustment needed]
```

## 市场扫描流程

### 每小时扫描（使用无头浏览器）

```
1. Navigate to polymarket.com/markets
2. For each active market:
   a. Record YES price, NO price
   b. Calculate YES + NO spread
   c. Flag if spread < 96% or > 102%

3. Build correlation map:
   a. Group markets by topic (elections, sports, crypto, etc.)
   b. Identify logical relationships
   c. Check for price inconsistencies

4. Cross-reference with:
   a. Kalshi (kalshi.com) for same events
   b. News for time-sensitive opportunities

5. Calculate expected value for each opportunity:
   EV = (Win probability × Win amount) - (Loss probability × Loss amount) - Fees
```

### 相关性检测

维护`references/market_correlations.md`文件，记录已知的市场相关性数据：

```markdown
## Correlation: [Topic]

### Markets
- Market A: [ID/Name]
- Market B: [ID/Name]

### Relationship
[Mathematical relationship: A implies B, A + B = C, etc.]

### Historical Spread
- Average: X%
- Range: X% to Y%
- When spread > Y%: Consider arb
```

## Telegram更新

**要求**：主动通过Telegram向Rick发送交易更新信息。

### 更新频率
- **上午扫描**（9点）：发现活跃的套利机会
- **交易提醒**：在建立或平仓时
- **结果确认提醒**：当市场达成交易结果时
- **晚间总结**（6点）：每日盈亏情况、未平仓头寸

### 消息格式

```
[CLAWDBOT POLYMARKET ARB UPDATE]

Paper Portfolio: $X,XXX (+/-X.X%)

Open Arbitrage Positions:
- [Market A vs B]: Edge X.X%, resolves [date]
- [Market C]: Time decay play, target [date]

Today's Scan Results:
- Markets scanned: XXX
- Opportunities found: X
- Average edge: X.X%

Best Current Opportunity:
[Market name]
- Type: [arb type]
- Edge: X.X%
- Confidence: [High/Medium/Low]
- Risk: [Description]

Strategy Notes:
[Observations about market efficiency]
```

## 自我改进机制

### 每完成10次套利交易后：
1. **计算指标**：
   - 实际获得的套利利润与理论预期利润的对比
   - 各类型套利的胜率
   - 平均持有时间
   - 滑点分析

2. **更新`references/strategy_evolution.md`文件**：
   ```markdown
   ## Iteration #[N] - [DATE]

   ### Performance Last 10 Arbs
   - Win Rate: XX%
   - Avg Edge Captured: X.X%
   - Theoretical Edge: X.X%
   - Slippage: X.X%

   ### By Arb Type
   | Type | Count | Win Rate | Avg Edge |
   |------|-------|----------|----------|
   | 1 | X | XX% | X.X% |
   | 2 | X | XX% | X.X% |
   | ... | | | |

   ### Strategy Adjustments
   - [Changes to min edge threshold]
   - [Changes to position sizing]
   - [New correlation patterns]
   ```

3. **更新本策略文档**：
   - 添加新发现的套利模式
   - 调整最低套利利润阈值
   - 记录新的市场相关性数据
   - 删除无效的套利策略

## 风险管理

### 位置限制
- 单个市场的最大持仓比例：投资组合的10%
- 相关市场的最大持仓比例：投资组合的20%
- 流动性较差市场的最大持仓比例：投资组合的5%

### 套利利润要求
- 类型1（同一市场）：最低套利利润为1%
- 类型2（相关市场）：最低套利利润为3%
- 类型3（条件概率）：最低套利利润为3%
- 类型4（时间衰减）：最低套利利润为5%
- 类型5（跨平台）：最低套利利润为2%

### 平仓规则
- 当套利利润低于5%时立即平仓
- 如果新信息导致相关性发生变化，立即平仓
- 在市场结果不确定的情况下，务必在结果确定前平仓

## 市场效率观察

**根据实际情况更新本部分内容：**

### 最具效率的市场（套利难度较高）：
- [例如：“在结果确定前一周内举行的重要选举”

### 套利机会较少的市场（最佳套利目标）：
- [例如：“交易量较小的小众体育市场”
- [例如：“成立不到24小时的新市场”

### 时间规律
- [例如：“在交易量较低的时段（美国东部时间凌晨2-6点），价格异常情况较为常见”

## 参考资料

- `references/arb_journal.md` - 所有交易记录（如文件缺失，请创建）
- `references/strategy_evolution.md` - 策略迭代过程（如文件缺失，请创建）
- `references/market_correlations.md` - 已知的市场相关性数据（如文件缺失，请创建）
- `references/fee_analysis.md` - 平台手续费统计（如文件缺失，请创建）

## 与Rick的反馈机制

**每次与Rick沟通后**：
1. 记录他的任何偏好或建议。
2. 根据建议更新相关参考文件。
3. 如有必要，调整风险参数。
4. 在下一次Telegram更新中反馈沟通内容。

**Rick的偏好设置：**
- [根据沟通内容进行更新]
- [风险承受能力说明]
- [优先选择的套利类型]
- [应关注或避免的市场]