---
name: sector-analyst
description: 此技能适用于分析行业和领域的绩效图表，以评估市场定位和轮动模式。当用户提供行业或领域的绩效图表（时间范围为1周或1个月），并请求进行市场周期评估、行业轮动分析或基于绩效数据的战略定位建议时，可使用此技能。所有的分析和输出结果将以英文形式提供。
---

# 行业分析师

## 概述

该技能能够全面分析行业和领域的表现图表，以确定市场周期的位置，并预测可能的行业轮动情景。分析过程结合了观察到的表现数据与既定的行业轮动原则，提供客观的市场评估和概率性的情景预测。

## 适用场景

在以下情况下使用该技能：
- 用户提供了行业表现图表（通常为1周和1个月的时间范围）
- 用户提供了显示相对表现数据的行业图表
- 用户请求分析当前的市场周期位置
- 用户要求进行行业轮动的评估或预测
- 用户需要基于概率的市场定位方案

示例用户请求：
- “分析这些行业表现图表，告诉我我们目前处于市场周期的哪个阶段”
- “根据这些表现图表，哪些行业接下来可能会表现优异？”
- “根据这些数据，防御性行业轮动的概率是多少？”
- “请审查这些行业和领域图表，并提供情景分析”

## 分析工作流程

在分析行业/领域表现图表时，请遵循以下结构化的工作流程：

### 第一步：数据收集与观察

首先仔细检查所有提供的图表图像，提取以下信息：
- **行业层面的表现**：识别哪些行业（如科技、金融、消费 discretionary 等）表现优异或不佳
- **领域层面的表现**：注意哪些领域表现出强势或疲弱
- **时间范围的比较**：比较1周与1个月的表现，以确定趋势的一致性或差异
- **表现的幅度**：评估相对表现差异的大小
- **表现的广度**：判断表现是集中还是分散的

在分析图表时，请用英语思考，并记录关键行业和领域的具体数值表现数据。

### 第二步：市场周期评估

加载行业轮动知识库以辅助分析：
- 阅读 `references/sector_rotation.md`，以获取市场周期和行业轮动的框架
- 将观察到的表现模式与每个周期阶段的预期模式进行对比：
  - 周期初期复苏
  - 周期中期扩张
  - 周期后期
  - 经济衰退

通过以下方式确定当前观察结果最符合哪个周期阶段：
- 将表现优异的行业与典型的周期领头羊对应起来
- 将表现不佳的行业与典型的周期落后者对应起来
- 评估多个行业之间的一致性
- 评估防御性行业与周期性行业表现之间的匹配程度

### 第三步：当前情况分析

将观察结果综合成客观的评估：
- 说明当前表现最接近哪个市场周期阶段
- 强调支持这一观点的具体证据（哪些行业/领域证实了这一观点）
- 注意任何矛盾的信号或不寻常的模式
- 根据信号的一致性评估置信度

使用数据驱动的语言，并引用具体的表现数据。

### 第四步：情景开发

基于行业轮动原则和当前的市场位置，为下一个阶段开发2-4个潜在的情景：

对于每个情景：
- 描述市场周期的转变
- 识别哪些行业可能会表现优异
- 识别哪些行业可能会表现不佳
- 指出确认这一情景的催化剂或条件
- 为每个情景分配一个概率（参见 `sector_rotation.md` 中的概率评估框架）

情景应从最有可能的（概率最高）到替代性/反向情景进行排列。

### 第五步：输出生成

创建一个结构化的Markdown文档，包含以下部分：

**必填部分**：
1. **执行摘要**：2-3句话的总结性内容，概述主要发现
2. **当前情况**：对当前表现模式和市场周期位置的详细分析
3. **支持证据**：支持周期评估的具体行业和领域表现数据
4. **情景分析**：2-4个情景及其描述和概率分配
5. **推荐定位**：根据情景概率提出的战略性和战术性定位建议
6. **主要风险**：需要关注的主要风险或矛盾信号

## 输出格式

将分析结果保存为Markdown文件，文件命名格式为：`sector_analysis_YYYY-MM-DD.md`

使用以下结构：

```markdown
# Sector Performance Analysis - [Date]

## Executive Summary

[2-3 sentences summarizing key findings]

## Current Situation

### Market Cycle Assessment
[Which cycle phase and why]

### Performance Patterns Observed

#### 1-Week Performance
[Analysis of recent performance]

#### 1-Month Performance
[Analysis of medium-term trends]

#### Sector-Level Analysis
[Detailed breakdown by sector]

#### Industry-Level Analysis
[Notable industry-specific observations]

## Supporting Evidence

### Confirming Signals
- [List data points supporting cycle assessment]

### Contradictory Signals
- [List any conflicting indicators]

## Scenario Analysis

### Scenario 1: [Name] (Probability: XX%)
**Description**: [What happens]
**Outperformers**: [Sectors/industries]
**Underperformers**: [Sectors/industries]
**Catalysts**: [What would confirm this scenario]

### Scenario 2: [Name] (Probability: XX%)
[Repeat structure]

[Additional scenarios as appropriate]

## Recommended Positioning

### Strategic Positioning (Medium-term)
[Sector allocation recommendations]

### Tactical Positioning (Short-term)
[Specific adjustments or opportunities]

## Key Risks and Monitoring Points

[What to watch that could invalidate the analysis]

---
*Analysis Date: [Date]*
*Data Period: [Timeframe of charts analyzed]*
```

## 关键分析原则

在进行分析时，请遵循以下原则：
1. **客观性优先**：让数据引导结论，而非先入之见
2. **概率性思维**：通过概率范围表达不确定性
3. **多时间范围**：比较1周和1个月的数据以确认趋势
4. **相对表现**：关注相对强度，而非绝对回报
5. **广度的重要性**：广泛的表现比孤立的运动更具意义
6. **没有绝对性**：市场很少完全遵循教科书中的模式
7. **历史背景**：参考典型的轮动模式，但也要承认市场的独特性

## 概率指南

根据证据强度应用以下概率范围：
- **70-85%**：具有跨行业和时间范围的多个确认信号的强有力证据
- **50-70%**：具有部分确认信号但指标混合的中等证据
- **30-50%**：证据薄弱，信号有限或相互矛盾
- **15-30%**：与当前指标相反的投机性情景，但仍有可能发生

所有情景的总概率应约为100%。

## 资源

### 参考资料/
- `sector_rotation.md` - 包含市场周期阶段、典型行业表现模式和概率评估框架的综合性知识库

### 示例文件**
- `sector_performance.jpeg` - 行业表现图示例（1周和1个月的时间范围）
- `industory_performance_1.jpeg` - 表现优异的领域示例图表
- `industory_performance_2.jpeg` - 表现不佳的领域示例图表

这些示例文件展示了该技能所分析的视觉数据类型。用户提供的图表格式可能有所不同，但应包含类似的相对表现信息。

## 重要说明

- 所有分析工作均需用英语完成
- 输出的Markdown文件必须使用英语
- 每次分析都应引用行业轮动知识库
- 保持客观性，避免确认偏误
- 如果有新的数据出现，应及时更新概率评估
- 图表通常显示1周和1个月的时间段内的表现