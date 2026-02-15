---
name: technical-analyst
description: 此技能适用于分析股票、股票指数、加密货币或外汇对的周价格图表。当用户提供图表图像并请求基于图表数据的技术分析（如趋势识别、支撑/阻力位分析、情景规划或概率评估）时，可以使用此技能。分析过程中不应考虑新闻或基本面因素。
---

# 技术分析师

## 概述

该技能能够对每周价格图表进行全面的技术分析。通过分析图表数据，识别趋势、支撑位和阻力位、移动平均线的关系、成交量模式，并预测未来价格走势的概率情景。所有分析均基于图表数据客观进行，不受新闻、基本面或市场情绪的影响。

## 核心原则

1. **纯粹的图表分析**：所有结论仅基于图表中可见的技术数据。
2. **系统化的方法**：对每个图表分析都采用结构化的方法。
3. **客观评估**：避免主观偏见，专注于可观察到的模式和数据。
4. **概率性情景**：将未来可能性表达为概率加权的情景。
5. **顺序处理**：逐个分析图表，并立即记录分析结果。

## 分析工作流程

### 第一步：接收图表图像

当用户提供一张或多张每周图表图像进行分析时：

1. 确认收到所有图表图像。
2. 确定需要分析的图表数量。
3. 记录用户要求的任何特定关注点。
4. 依次分析图表。

### 第二步：加载技术分析框架

在开始分析之前，请阅读以下技术分析方法指南：

```
Read: references/technical_analysis_framework.md
```

该指南包含以下内容的详细指导：
- 趋势分析及分类
- 支撑位和阻力位的识别
- 移动平均线的解读
- 成量分析
- 图表形态和蜡烛图分析
- 情景开发及概率分配
- 分析的纪律性和客观性

### 第三步：系统地分析每个图表

对于每个图表图像，按照以下顺序进行系统分析：

#### 3.1 趋势分析
- 确定趋势方向（上升趋势、下降趋势或盘整趋势）
- 评估趋势强度（强、中等、弱）
- 注意趋势的持续时间和潜在的衰竭信号
- 观察新高/低或新低的情况

#### 3.2 支撑位和阻力位分析
- 标记重要的水平支撑位
- 标记重要的水平阻力位
- 识别趋势线的支撑/阻力作用
- 注意支撑位和阻力位的反转情况
- 评估多个支撑/阻力位汇聚的区域

#### 3.3 移动平均线分析
- 确定价格相对于20周、50周和200周移动平均线的位置
- 评估移动平均线的排列情况（牛市、熊市或中性）
- 注意移动平均线的走势（上升、下降或持平）
- 识别近期或即将发生的移动平均线交叉
- 观察移动平均线作为动态支撑或阻力线的表现

#### 3.4 成量分析
- 评估整体成交量趋势（增加、减少或稳定）
- 识别成交量峰值及其发生的背景（在支撑位/阻力位、突破时）
- 检查成交量是否与价格走势一致
- 注意成交量的峰值或衰竭模式

#### 3.5 图表形态和价格行为
- 识别反转形态（锤子形态、流星形态、吞没形态等）
- 识别持续形态（旗形、三角形等）
- 注意重要的蜡烛图形态
- 观察近期的突破或跌破情况

#### 3.6 综合观察结果
- 将所有技术要素整合到当前的评估中
- 确定影响图表的最重要因素
- 注意任何矛盾的信号或不确定性
- 确定将决定未来方向的关键水平

### 第四步：开发概率性情景

对于每个分析过的图表，创建2-4个不同的未来价格走势情景：

#### 情景结构

每个情景必须包括：
1. **情景名称**：清晰、描述性的标题（例如：“牛市情景：突破阻力位以上”）
2. **概率估计**：基于技术因素的概率百分比（所有情景的概率之和应为100%）
3. **描述**：该情景的内容及其发展过程
4. **支持因素**：支持该情景的技术依据（至少2-3个因素）
5. **目标价格水平**：如果情景发生时的预期价格水平
6. **无效化水平**：使该情景失效的具体价格水平

#### 典型情景框架

- **基准情景（40-60%）**：基于当前结构最可能的结果
- **牛市情景（20-40%）**：需要向上突破的乐观情景
- **熊市情景（20-40%**：需要向下突破的悲观情景
- **替代情景（5-15%）**：概率较低但技术上可行的结果

根据支持性技术因素的强度调整概率。确保概率合理且总和为100%。

### 第五步：生成分析报告

对于每个分析过的图表，使用以下模板结构生成一份详细的markdown报告：

```
Read and use as template: assets/analysis_template.md
```

报告必须包括以下所有部分：
1. 图表概览
2. 趋势分析
3. 支撑位和阻力位
4. 移动平均线分析
5. 成量分析
6. 图表形态和价格行为
7. 当前市场评估
8. 情景分析（2-4个情景及其概率）
9. 总结
10. 免责声明

**文件命名规则**：将每个分析结果保存为`[符号]_技术分析_[YYYY-MM-DD].md`格式。

示例：`SPY_technical_analysis_2025-11-02.md`

### 第六步：对多个图表进行分析

如果提供了多个图表：

1. 完成第一个图表的完整分析流程（步骤3-5）。
2. 保存分析报告。
3. 继续分析下一个图表。
4. 重复此过程，直到所有图表都得到分析和记录。

**注意事项**：不要批量分析。完成并保存每个报告后，再进行下一个图表的分析。

## 质量标准

### 客观性要求

- 所有分析严格基于图表中的可观察数据。
- 避免引入外部信息（新闻、基本面或市场情绪）。
- 不使用“我认为”或“我感觉”等主观语言。
- 当信号不明确时，清晰地表达不确定性。
- 同时呈现牛市和熊市的可能性，以避免确认偏误。

### 完整性要求

- 涵盖分析模板中的所有部分。
- 提供具体的支撑位、阻力位和目标价格水平。
- 用技术因素证明概率估计的合理性。
- 为每个情景提供无效化水平。
- 注意分析的任何限制或注意事项。

### 清晰度要求

- 正确使用专业的技术术语。
- 用清晰、专业的语言撰写。
- 逻辑清晰地组织信息。
- 提供具体的价格水平（避免模糊的描述）。
- 使情景明确且互斥。

## 示例使用场景

**示例1：单张图表分析**
```
User: "Please analyze this weekly chart of the S&P 500"
[Provides chart image]

Analyst:
1. Confirms receipt of chart image
2. Reads technical_analysis_framework.md for methodology
3. Conducts systematic analysis (trend, S/R, MA, volume, patterns)
4. Develops 3 scenarios with probabilities (e.g., 55% bullish continuation, 30% consolidation, 15% reversal)
5. Generates comprehensive analysis report using template
6. Saves as SPY_technical_analysis_2025-11-02.md
```

**示例2：多张图表分析**
```
User: "Analyze these three charts: Bitcoin, Ethereum, and Nasdaq"
[Provides 3 chart images]

Analyst:
1. Confirms receipt of 3 charts
2. Reads technical_analysis_framework.md
3. Analyzes Bitcoin chart completely → Generates report → Saves as BTC_technical_analysis_2025-11-02.md
4. Analyzes Ethereum chart completely → Generates report → Saves as ETH_technical_analysis_2025-11-02.md
5. Analyzes Nasdaq chart completely → Generates report → Saves as NDX_technical_analysis_2025-11-02.md
6. Notifies user that all three analyses are complete
```

**示例3：针对性分析请求**
```
User: "I'm particularly interested in whether this stock will break above resistance. Analyze the chart."
[Provides chart image]

Analyst:
1. Conducts full systematic analysis
2. Pays special attention to resistance levels and breakout probability
3. Develops scenarios with emphasis on breakout vs. rejection possibilities
4. Assigns probabilities based on volume, trend strength, and proximity to resistance
5. Generates complete report with focused scenario analysis
```

## 资源

该技能包含以下捆绑资源：

### references/technical_analysis_framework.md

包含技术分析的全面方法指南，包括：
- 趋势分析的标准和分类
- 支撑位和阻力位的识别技术
- 移动平均线的解读指南
- 成量分析原则
- 图表形态的识别
- 情景开发及概率分配框架
- 客观性和纪律性的提醒

**使用方法**：在进行分析之前，请阅读此文件，以确保采用系统化、客观的方法。

### assets/analysis_template.md

包含技术分析报告的结构化模板，包含所有必需的部分。

**使用方法**：使用此模板结构为每个分析报告编写报告。复制格式，并根据每个图表的具体情况填写内容。