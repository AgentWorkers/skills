---
name: skill-market-analyzer
description: 分析技能市场，以识别趋势、发现差距、寻找机会并明确自身的竞争定位。该方法适用于研究技能市场的动态变化、规划新的培训项目、了解用户需求，或优化现有培训内容以更好地适应市场需求。
---
# 技能市场分析器

## 概述

`skill-market-analyzer` 提供了针对技能生态系统的全面市场分析服务。它有助于识别市场趋势、市场缺口、发展机会以及竞争定位，从而为技能开发和投资策略提供决策依据。

## 使用场景

- 规划新技能时需要市场调研
- 分析现有技能的竞争格局
- 识别技能市场中的空白领域
- 了解用户需求模式
- 优化技能的定位和宣传内容
- 确定技能开发优先级
- 评估市场机会

## 核心概念

### 市场维度

| 维度 | 描述 |
|-----------|-------------|
| **需求** | 用户的兴趣和需求频率 |
| **供应** | 某类别中可用的技能数量 |
| **质量** | 现有解决方案的平均质量 |
| **饱和度** | 市场细分领域的竞争程度 |
| **增长** | 市场发展的趋势和速度 |

### 分析类型

| 类型 | 目的 | 输出结果 |
|------|---------|--------|
| **市场概况** | 整体市场概览 | 市场地图 |
| **市场缺口** | 发现未满足的需求 | 机会列表 |
| **竞争分析** | 与竞争对手对比 | 定位分析 |
| **趋势分析** | 识别新兴趋势 | 趋势报告 |
| **机会评估** | 评估潜在机会 | 机会排名列表 |

### 机会评分

评分依据：
- 需求水平（1-10分）
- 竞争程度（1-10分，反向排序）
- 质量差距（1-10分）
- 战略契合度（1-10分）
- 实施难度（1-10分，反向排序）

**计算公式**：`(需求 + (11-竞争程度) + 质量差距 + 战略契合度 + (11-实施难度)) / 5`

## 输入参数

- 市场类别或领域
- 分析类型
- 趋势分析的时间范围
- 用于对比的竞争对手列表
- 目标用户群体

## 输出结果

- 市场分析报告
- 机会排名
- 竞争定位图
- 趋势可视化图表
- 战略建议

## 工作流程

### 市场概况分析

1. 确定市场范围（类别/领域）
2. 收集现有技能数据
3. 分析供需平衡
4. 识别市场领导者
5. 绘制竞争格局图
6. 生成市场概况报告

### 市场缺口分析

1. 识别目标用户群体
2. 列出用户需求和痛点
3. 分析现有技能的覆盖情况
4. 找出未满足的需求领域
5. 根据影响程度优先处理这些缺口
6. 提出开发建议

### 竞争分析

1. 识别直接竞争对手
2. 分析功能覆盖情况
3. 比较各项质量指标
4. 评估竞争定位
5. 寻找差异化优势
6. 提出定位策略建议

### 趋势分析

1. 确定分析时间范围
2. 收集历史数据
3. 识别新兴趋势
4. 预测未来发展趋势
5. 提出战略调整建议

## 命令示例

### 分析市场概况
```bash
./scripts/analyze-market.sh --category productivity --output landscape.md
```

### 识别市场缺口
```bash
./scripts/find-gaps.sh --domain automation --min-opportunity-score 7
```

### 进行竞争分析
```bash
./scripts/analyze-competition.sh --skill my-skill --competitors skill-a,skill-b
```

### 分析市场趋势
```bash
./scripts/analyze-trends.sh --category all --since 2024-01-01
```

### 评估机会潜力
```bash
./scripts/score-opportunity.sh --name "new-skill-idea" --demand 8 --competition 3 --effort 5
```

### 生成完整报告
```bash
./scripts/generate-report.sh --category productivity --type comprehensive
```

## 输出格式

### 市场概况报告
```markdown
# Market Landscape: Productivity Skills

## Executive Summary
- Total Skills: 45
- High-Demand Areas: 8
- Underserved Segments: 5
- Average Quality Score: 6.2/10

## Supply Analysis
| Category | Skills | Saturation |
|----------|--------|------------|
| Task Management | 12 | High |
| Note Taking | 8 | Medium |
| Time Tracking | 5 | Low |

## Demand Analysis
| Need | Frequency | Satisfaction |
|------|-----------|--------------|
| Calendar integration | High | Low |
| Cross-platform sync | Medium | Medium |
| AI assistance | High | Very Low |

## Opportunities
1. **AI-powered task prioritization** (Score: 8.5)
   - High demand, low competition
   - Quality gap: 7/10
   
2. **Cross-tool workflow automation** (Score: 7.8)
   - Medium demand, very low competition
   - Quality gap: 6/10

## Recommendations
- Focus on AI-assisted productivity features
- Consider integration-first approach
- Target underserved time-tracking market
```

### 机会评分卡
```json
{
  "opportunity": "AI Task Prioritizer",
  "score": 8.5,
  "breakdown": {
    "demand": 9,
    "competition": 2,
    "quality_gap": 7,
    "strategic_fit": 8,
    "effort": 6
  },
  "market_size": "Large",
  "time_to_market": "2-3 months",
  "confidence": "High",
  "recommendation": "Strong opportunity - proceed with development"
}
```

## 分析框架

### 供需矩阵
```
High Demand + Low Supply  →  OPPORTUNITY (develop here)
High Demand + High Supply →  COMPETE (differentiate)
Low Demand  + Low Supply  →  NICHE (evaluate carefully)
Low Demand  + High Supply →  AVOID (overcrowded)
```

### 质量-竞争矩阵
```
High Quality + Low Competition  →  LEADER (maintain position)
High Quality + High Competition →  DIFFERENTIATE (find unique angle)
Low Quality  + Low Competition  →  EASY WIN (enter with quality)
Low Quality  + High Competition →  AVOID (red ocean)
```

## 质量评估规则

- 使用多种数据源进行分析
- 通过用户反馈验证分析结果
- 每季度更新分析内容
- 监测预测的准确性
- 记录分析方法
- 明确报告中的置信度水平

## 常见使用场景

- “分析生产力技能的市场情况”
- “当前技能市场中存在哪些缺口？”
- “我的技能与竞争对手相比如何？”
- “自动化技能领域的新兴趋势是什么？”
- “评估这个技能项目的市场潜力”
- “我是否应该开发某个技能？”

## 限制因素

- 分析结果基于现有数据
- 市场趋势可能快速变化
- 用户需求会随时间演变
- 竞争数据可能不完整
- 预测结果仅供参考，不能保证绝对准确性
- 市场时机难以准确预测

## 相关技能

- `decision-distiller` - 用于评估市场机会
- `insight-tracker` - 用于收集市场洞察
- `feedback-loop` - 用于验证市场假设

## 资源

### 脚本：
- `analyze-market.sh` - 市场概况分析
- `find-gaps.sh` - 识别市场缺口
- `analyze-competition.sh` - 竞争分析
- `analyze-trends.sh` - 趋势分析
- `score-opportunity.sh` - 机会评分
- `generate-report.sh` - 生成完整报告

### 参考资料：
- 市场研究模板
- 竞争分析框架
- 趋势分析方法论