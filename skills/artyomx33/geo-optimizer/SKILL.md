---
name: geo-optimizer
version: 1.0.0
description: 优化内容以适应AI引用（GEO）的需求。当用户提到“GEO”、“生成引擎优化”、“AI引用”、“被AI引用”、“适合AI的内容”或为ChatGPT/Claude/Perplexity等平台创建内容时，请使用此方法。
---

# GEO内容优化器

## 使用场景
- 为AI引用创建内容
- 重构文章以适应AI的需求
- 提高内容在AI回答中的可引用性
- 在以AI为主导的搜索中提升竞争力
- 添加AI系统能够识别的权威性信号

## 核心概念
**SEO**：在搜索结果中的排名
**GEO**：在AI生成的答案中被引用

## 8个GEO维度

| 维度 | 低（1-2分） | 高（4-5分） |
|---------|---------|-----------|
| 定义的清晰度 | 含糊不清 | 有明确指标的可引用定义 |
| 可引用的陈述 | 普遍性陈述 | 有来源的具体事实 |
| 事实密度 | 意见成分较多 | 数据丰富 |
| 来源引用 | 无 | 可追溯到权威来源 |
| 问答格式 | 仅使用散文形式 | 包含明确的问答部分 |
| 权威性信号 | 无权威证明 | 专家署名、资质证明 |
| 内容时效性 | 过时 | 引用内容为旧信息，数据为最新 |
| 结构清晰度 | 结构混乱 | 有清晰的标题、列表和表格 |

## GEO评分标准
每个维度评分1-5分，总分40分：
- 32-40分：适合AI使用
- 24-31分：需要优化
- 16-23分：需要大量改进

## 快速优化方法（30分钟内可完成）
1. 添加具体数据（含日期和来源）
2. 创建独立的定义段落
3. 包含带有资质证明的专家引语
4. 添加对比表格
5. 创建包含5-7个问题的FAQ部分
6. 将模糊的陈述替换为经过验证的事实
7. 插入权威来源的引用

## 输出格式

```markdown
## GEO Audit
Current Score: [X]/40

### Dimension Scores
| Dimension | Score | Quick Fix |
|-----------|-------|-----------|
| [dimension] | [1-5] | [action] |

## Optimized Content Sections

### Definition (Citable)
[Term] is [category] that [function], [key metric].

### Key Statistics
- [Stat with source and date]
- [Stat with source and date]

### FAQ Section
**Q: [Common question]?**
A: [Direct, quotable answer with citation]
```

## 集成方式
该工具可与以下工具结合使用：
- **app-planning-skill**：用于规划内容策略
- **writing-plans**：用于构建内容项目

---
有关评分细节，请参阅 references/dimensions.md
有关优化方法，请参阅 references/patterns.md
有关优化前后的对比示例，请参阅 references/examples.md