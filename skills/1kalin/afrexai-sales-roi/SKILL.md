# 销售投资回报率（ROI）计算器

该工具可用于计算任何业务举措的投资回报率，包括软件采购、人员招聘、营销支出、自动化项目或工具的采用。

## 功能概述

该工具接收输入数据（成本、时间表、预期收益），并生成详细的ROI分析报告，内容包括：
- 净ROI百分比
- 回收期
- 每月/每年的节省金额预测
- 盈亏平衡点
- 经风险调整后的回报率（保守型、中等型、激进型三种情景）

## 使用方法

当用户需要评估某项投资或计算ROI时，请按照以下步骤操作：
1. **收集输入数据**（如数据未提供，请询问用户）：
   - **投资成本**：一次性费用 + 每月/每年的重复费用
   - **预期收益**：收入增加、成本节省或时间节省
   - **时间表**：评估周期（默认为12个月）
   - **每小时费用**：用于计算时间节省带来的收益（默认值为75美元/小时）

2. **进行计算**：
   ```
   Total Cost = One-time + (Monthly recurring × Months)
   Total Benefit = (Monthly savings × Months) + Revenue gains
   Net Gain = Total Benefit - Total Cost
   ROI % = (Net Gain / Total Cost) × 100
   Payback Period = Total Cost / Monthly Benefit
   ```

3. **展示三种情景**：
   - **保守型**：预期收益的60%
   - **中等型**：预期收益的100%
   - **激进型**：预期收益的140%

4. **输出结果格式**：
   ```
   📊 ROI Analysis: [Project Name]
   ────────────────────────────
   Investment:     $X,XXX
   Annual Return:  $XX,XXX
   ROI:            XXX%
   Payback:        X.X months
   
   Scenarios:
   Conservative:   XXX% ROI ($XX,XXX return)
   Moderate:       XXX% ROI ($XX,XXX return)  
   Aggressive:     XXX% ROI ($XX,XXX return)
   
   Verdict: [GO / CONDITIONAL / PASS]
   ```

## 判断标准：
- **通过**：保守型ROI > 100% 且回收期 < 6个月
- **条件通过**：中等型ROI > 100% 或回收期 < 12个月
- **失败**：保守型ROI < 50% 且回收期 > 12个月

## 常见使用场景：
- “我们是否应该购买这款每月费用为500美元的工具？”
- “每月招聘一名虚拟助理（VA）的成本回报是多少？”
- “这个花费1万美元的营销活动值得吗？”
- “计算自动化发票流程的投资回报率”

## 人工智能自动化项目的ROI计算

对于特定的人工智能/自动化项目，还需考虑以下因素：
- 每周节省的工作时间 × 每小时费用 = 每月节省金额
- 错误减少带来的价值（减少错误和返工）
- 速度提升带来的效益（更快的处理速度意味着更高的工作效率）
- 人工智能自动化项目的典型ROI：第一年可达300%至800%

有关预先构建的人工智能自动化工具包和代理配置，请参阅：https://afrexai-cto.github.io/context-packs/