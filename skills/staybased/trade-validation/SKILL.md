---
name: trade-validation
description: |
  10-dimension weighted scoring framework for prediction market trade evaluation.
  Enforces disciplined position sizing, circuit breakers, and mandatory counter-arguments.

  Use when: evaluating prediction market trades, scoring opportunities, deciding position sizes,
  comparing Polymarket/Kalshi opportunities, running pre-trade checklists.

  Don't use when: general crypto analysis, DeFi yield farming, non-prediction-market investments,
  stock/equity analysis, sports betting (different framework needed).

  Negative examples:
  - "Should I buy ETH?" → No. This is for prediction markets with binary/discrete outcomes.
  - "What's the best DeFi yield?" → No. Wrong domain entirely.
  - "Score this sports bet" → No. Sports betting has different dimensions (injuries, matchups).

  Edge cases:
  - Crypto prediction markets (e.g., "Will BTC hit $X?") → YES, use this if on Polymarket/Kalshi.
  - Multi-outcome markets → Score each outcome separately.
  - Markets with <$25 liquidity → Auto-fail on Liquidity dimension.
version: "1.0"
---

# 交易验证 —— 十维评分框架

> **规则：** 任何交易的执行都必须满足80%以上的加权置信度得分。
> **如果任何一维的得分低于4/10，则自动否决该交易。**

---

## 评分维度

| 序号 | 维度        | 权重      | 衡量内容                |
|------|------------|---------|----------------------|
| 1    | 信息优势     | 18%      | 我们是否掌握了市场尚未掌握的信息？        |
| 2    | 来源质量     | 12%      | 我们的信息来源是否可靠？           |
| 3    | 市场效率     | 10%      | 该市场是否存在价格失真的情况？         |
| 4    | 时间跨度     | 8%      | 资金被锁定的时间长度是多少？         |
| 5    | 下跌保护     | 15%      | 最坏情况下可能发生的损失是多少？        |
| 6    | 交叉验证     | 12%      | 多个独立信号是否一致？           |
| 7    | 历史准确性   | 5%      | 在类似交易中的表现如何？           |
| 8    | 流动性/执行风险 | 7%      | 我们能否顺利买入和卖出？           |
| 9    | 共识分歧     | 8%      | 我们的观点与市场共识相差多远？         |
| 10   | 事件触发因素   | 5%      | 是否存在已知的事件触发因素？         |

**总分：100%**

### 计算方法

```
Weighted Score = Σ(dimension_score / 10 × weight) × 100
```

---

## 阈值规则

| 加权得分 | 行动        | 下注金额                |
|---------|------------------|----------------------|
| < 80%   | ❌ 禁止交易    | 0美元                |
| 80–84%   | ✅ 最小金额    | 3–5美元                |
| 85–89%   | ✅ 标准金额    | 5–7美元                |
| 90%及以上 | ✅ 确信度较高 | 最高7.50美元（不超过总资金的10%）     |

### 否决规则

- **如果任何一维的得分低于4/10，则无论总分如何，都自动否决该交易**  
- **理由：** 在任何一方面存在严重缺陷（例如，流动性指标为2意味着交易存在巨大风险）。

---

## 风险管理

- **单笔交易的最大持仓比例：** 投资组合的10%  
- **最低市场流动性要求：** 25美元；低于此要求则禁止交易  
- **最大未平仓头寸风险：** 所有头寸的总风险不得超过总资金的30%  
- **每日止损机制：** 单日亏损达到8美元时，所有交易暂停24小时  
- **冷却期：** 在发生亏损后1小时内禁止交易  
- **禁止报复性交易：** 最后一次亏损必须发生在24小时以上，或者新交易与之前的交易无关  
- **禁止在凌晨12点至早上7点交易**（除非交易时间非常紧急）  

---

## 必须记录的反对意见

每笔交易都必须记录以下内容：  
1. **我们可能犯错的原因是什么？**（不是简单的反驳意见，而是基于事实的、有力的反对理由）  
2. **什么情况会改变我们的决定？**（具体的反驳依据）  
3. **退出策略：** 何时应该提前止损？  

---

## 评分卡模板

```
TRADE SCORE CARD
═══════════════════════════════════════════════════════════
Market: [name]
Date: [date]
Position: [YES/NO @ price]

 #  Dimension              Weight   Score   Weighted
─── ────────────────────── ──────── ─────── ──────────
 1  Information Edge        18%     __/10   __._%
 2  Source Quality           12%     __/10   __._%
 3  Market Efficiency        10%     __/10   __._%
 4  Time Horizon              8%     __/10   __._%
 5  Downside Protection      15%     __/10   __._%
 6  Cross-Validation         12%     __/10   __._%
 7  Historical Accuracy       5%     __/10   __._%
 8  Liquidity/Execution       7%     __/10   __._%
 9  Consensus Divergence      8%     __/10   __._%
10  Event Catalyst             5%     __/10   __._%
─── ────────────────────── ──────── ─────── ──────────
                    TOTAL   100%            __._%

Minimum Score: __/10 (dimension: _____________)
VETO Check: [ ] All dimensions ≥ 4 — PASS / FAIL

Counter-argument: ________________________________
What would change our mind: _____________________
Exit strategy: __________________________________

RESULT: TRADE / NO TRADE
Tier: [ ] Min ($3-5)  [ ] Standard ($5-7)  [ ] Conviction ($7.50)
═══════════════════════════════════════════════════════════
```

---

## 交易前检查清单

```
RESEARCH
  [ ] Minimum 3 independent sources consulted
  [ ] Sources documented with links
  [ ] Strong counter-argument documented
  [ ] Counter-argument is genuine (not strawman)

SCORING
  [ ] All 10 dimensions scored
  [ ] Weighted score ≥ 80%
  [ ] No dimension below 4/10
  [ ] Score logged to trade journal

RISK
  [ ] Current bankroll: $______
  [ ] Bet ≤ 10% of bankroll
  [ ] Total open exposure ≤ 30%
  [ ] Daily loss < $8 (circuit breaker not triggered)

DISCIPLINE
  [ ] Cool-down respected (1h since last loss)
  [ ] Not revenge trading
  [ ] Not trading 12am–7am
```

---

## 详细评分标准

完整的评分标准（1–10分）请参见 `references/scoring-rubric.md`。

## 交易日志

将所有经过评分的交易（无论结果如何）记录到 `projects/polymarket/trade-journal/` 目录中：  

```
## [DATE] — [MARKET NAME]
- **Score:** XX.X%
- **Result:** TRADE / NO TRADE / VETO
- **Position:** YES/NO @ XXc | **Stake:** $X.XX
- **Outcome:** WIN / LOSS / PENDING
- **P&L:** +/- $X.XX
- **Lesson:** (post-resolution)
```