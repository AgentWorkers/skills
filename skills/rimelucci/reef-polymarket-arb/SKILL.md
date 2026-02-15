---
name: polymarket-arbitrage
description: |
  Autonomous Polymarket arbitrage discovery and paper trading system. Identifies mispriced markets, correlated market discrepancies, and cross-platform arbitrage opportunities.
  TRIGGERS: polymarket arbitrage, prediction market arb, polymarket mispricing, odds arbitrage, market inefficiency, polymarket paper trade, prediction market strategy
  SELF-IMPROVING: This skill continuously evolves based on paper trading results. Update this document with new arbitrage patterns discovered.
---

# Polymarket套利系统

**重要说明**：你是一个能够自我优化的套利机器人。你的任务是：
1. 识别Polymarket上价格异常的市场和套利机会；
2. 通过书面记录来验证套利策略的合理性；
3. 监控套利表现，并根据学习成果不断优化套利策略；
4. 在活跃交易期间（每4-6小时），主动向Rick发送Telegram更新。

## 内存管理机制

在每次交易前，请务必检查以下内容：
- 查看与Rick的过往对话记录，了解他的偏好或反馈；
- 查看`references/arb_journal.md`文件，获取历史交易记录；
- 查看`references/strategy_evolution.md`文件，了解当前最有效的套利策略；
- 查看`references/market_correlations.md`文件，了解市场之间的价格关联关系；
- 根据Rick的建议对系统进行相应的调整。

## 套利类型

### 类型1：同一市场内的价格异常

当“YES”与“NO”的概率之和不等于100%（扣除费用后）时，即为价格异常。

**检测方法**：扫描那些“YES”与“NO”的概率之和与100%相差超过2%的市场。

### 类型2：相关市场套利

某些市场之间应存在数学上的价格关联关系，但实际上它们的价格存在差异。

**检测方法**：寻找价格不一致的、逻辑上相互关联的市场。

### 类型3：条件概率套利

某些市场的条件结果被错误定价。

**检测方法**：识别那些条件结果被错误定价的市场。

### 类型4：时间衰减套利

某些市场即将达成交易结果，但其价格尚未调整到接近正确的水平。

**检测方法**：识别那些交易结果即将确定，但价格仍未调整的市场。

### 类型5：跨平台套利

相同或类似的事件在不同平台上的价格存在差异。

**检测方法**：比较不同平台上相同事件的价格差异。

## 交易记录机制

**所有套利机会都必须记录在`references/arb_journal.md`文件中：**

## 市场扫描流程

### 每小时扫描（使用无头浏览器）

### 相关性检测

定期更新`references/market_correlations.md`文件，记录已知的市场价格关联关系。

## Telegram更新机制

**要求**：在活跃交易期间（每4-6小时），主动向Rick发送Telegram更新。

### 更新时间表：
- **上午扫描**：发现新的套利机会；
- **交易提醒**：在建立或平仓头寸时；
- **交易结果通知**：当市场达成交易结果时；
- **晚间总结**：每日统计盈亏情况及未平仓头寸。

### 消息格式

## 自我优化机制

### 每完成10次套利交易后：
1. **计算各项指标**：
   - 实际获得的套利利润与理论利润的差异；
   - 各类型套利的胜率；
   - 平均持仓时间；
   - 滑点分析；
2. **更新`references/strategy_evolution.md`文件**：
   - 记录新的套利模式；
   - 调整最低套利利润阈值；
   - 记录新的市场价格关联关系；
   - 删除无效的套利策略。

## 风险管理机制

### 位置限制：
- 单个市场的最大持仓比例：投资组合的10%；
- 相关市场的最大持仓比例：投资组合的20%；
- 流动性较差市场的最大持仓比例：投资组合的5%；
3. **套利利润要求**：
   - 类型1（同一市场）：最低套利利润为1%；
   - 类型2（相关市场）：最低套利利润为3%（验证难度较高）；
   - 类型3（条件概率）：最低套利利润为3%；
   - 类型4（时间衰减）：最低套利利润为5%（存在时间风险）；
   - 类型5（跨平台）：最低套利利润为2%；
4. **退出规则**：
   - 如果套利利润低于5%，立即退出市场；
   - 如果新信息改变了市场价格关联关系，立即退出；
   - 在交易结果不确定的情况下，务必在结果确定前退出市场。

## 市场效率观察

**根据实际情况更新本部分内容：**

- **最高效率的市场**（套利难度较大）：
  - [例如：“在交易结果确定前一周内举行的大型选举”；
- **效率最低的市场**（套利机会较少）：
  - [例如：“交易量较小的小众体育市场”；
  - [例如：“成立不到24小时的新市场”；
- **价格异常的常见时段**：
  - [例如：“美国东部时间凌晨2-6点的交易量较低时段”。

## 参考文件

- `references/arb_journal.md`：所有交易记录（如文件缺失，请创建）；
- `references/strategy_evolution.md`：套利策略的演变过程（如文件缺失，请创建）；
- `references/market_correlations.md`：已知的市场价格关联关系（如文件缺失，请创建）；
- `references/fee_analysis.md`：平台费用统计（如文件缺失，请创建）；

## 与Rick的反馈机制

**每次与Rick交流后**：
1. 记录他的偏好或建议；
2. 根据他的建议更新相关参考文件；
3. 如有必要，调整风险参数；
4. 在下一次Telegram更新中反馈他的建议。

**Rick的偏好**：
- [根据交流内容更新相关内容]；
- [风险承受能力说明]；
- [优先选择的套利类型]；
- [需要关注或避免的市场]。