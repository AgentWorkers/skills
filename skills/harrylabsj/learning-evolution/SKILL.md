---
name: learning-evolution
description: 跟踪、分析并优化学习模式，这些模式源于技能的使用和用户互动。该功能可用于识别学习机会、追踪技能随时间的提升情况、分析使用模式，或根据反馈来改进现有技能。
---
# 学习与进化

## 概述

`learning-evolution` 技能负责跟踪、分析并优化技能的使用模式及用户互动情况。通过识别使用模式、收集数据并基于实际使用情况提出改进建议，帮助技能不断提升。

## 使用场景

- 分析技能的使用情况
- 从使用模式中发现学习机会
- 跟踪技能随时间的发展情况
- 根据用户反馈优化技能
- 了解哪些方法有效，哪些无效
- 规划技能的更新与改进
- 测量技能的有效性

## 核心概念

### 学习维度

| 维度 | 描述 | 指标          |
|---------|-------------|--------------|
| `使用频率` | 技能被使用的频率和方式 | 使用次数、使用时长、完成率 |
| `有效性` | 技能实现目标的程度 | 成功率、错误率       |
| `满意度` | 用户对使用效果的满意度 | 评分、反馈、收益      |
| `适应性` | 技能随时间的变化情况 | 功能更新、改进方向     |

### 进化模式

| 模式       | 描述                | 示例                |
|------------|------------------|----------------------|
| **渐进式改进** | 逐步的小幅优化        | 添加错误处理机制           |
| **突破性改进** | 新功能的引入         | 新功能类别的添加           |
| **方向调整** | 根据用户反馈调整技能方向    | 重点功能的转移           |
| **淘汰**     | 因功能价值低而被逐步淘汰     | 功能的弃用             |

### 学习数据来源

1. **使用数据分析**：技能的使用频率、使用模式及使用趋势
2. **错误分析**：错误发生情况、异常情况、漏洞
3. **用户反馈**：用户的评分和具体意见
4. **结果监控**：技能的成功率与失败率
5. **对比分析**：与其他技能或旧版本的对比

## 输入数据

- 技能使用数据
- 用户反馈和评分
- 错误日志及失败情况
- 成功/失败指标
- 分析的时间范围

## 输出结果

- 学习报告
- 进化建议
- 模式分析报告
- 改进方案
- 发展趋势预测

## 工作流程

### 使用模式分析

1. 收集指定时间范围内的使用数据
2. 分析使用频率和时间模式
3. 检查使用完成情况
4. 发现使用中的瓶颈
5. 与预期使用情况对比
6. 提取有价值的洞察

### 有效性跟踪

1. 明确成功标准
2. 记录成功/失败情况
3. 分析错误类型
4. 识别常见的失败原因
5. 测量技能的改进程度
6. 提出修复建议

### 进化规划

1. 审查学习分析结果
2. 确定改进的重点领域
3. 设计改进方案
4. 评估改进方案的影响
5. 制定进化路线图
6. 规划评估方法

### 反馈整合

1. 收集用户反馈
2. 对反馈内容进行分类
3. 将反馈与使用数据关联
4. 确定需要优先解决的问题
5. 提出改进方案
6. 根据反馈更新技能

## 命令示例

### 分析使用模式
```bash
./scripts/analyze-usage.sh --skill <name> --period 30d
```

### 跟踪技能有效性
```bash
./scripts/track-effectiveness.sh --skill <name> --since 2024-01-01
```

### 生成学习报告
```bash
./scripts/generate-report.sh --skill <name> --type comprehensive
```

### 提出改进建议
```bash
./scripts/suggest-evolutions.sh --skill <name> [--min-confidence 0.7]
```

### 对比不同版本
```bash
./scripts/compare-versions.sh --skill <name> --v1 1.0.0 --v2 1.1.0
```

### 监控学习指标
```bash
./scripts/track-metrics.sh [--skill <name>] [--dashboard]
```

## 输出格式

### 学习报告
```markdown
# Learning Report: Skill Name

**Period**: 2024-01-01 to 2024-03-01  
**Total Uses**: 1,247  
**Success Rate**: 87%

## Usage Patterns

### Frequency
- Daily average: 42 uses
- Peak day: 156 uses (2024-02-15)
- Growth: +23% vs previous period

### Timing
- Most active: 9am-11am, 2pm-4pm
- Weekend usage: 15% of total
- Session duration: avg 3.2 minutes

### Completion
- Full completion: 78%
- Partial completion: 12%
- Abandoned: 10%

## Effectiveness Analysis

### Success Metrics
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Task completion | 87% | 85% | ✅ Exceeds |
| User satisfaction | 4.2/5 | 4.0 | ✅ Exceeds |
| Error rate | 3.2% | 5% | ✅ Good |
| Return rate | 68% | 60% | ✅ Exceeds |

### Error Patterns
1. **Input validation** (45% of errors)
   - Issue: Users provide unexpected formats
   - Suggestion: Add format examples

2. **Timeout errors** (32% of errors)
   - Issue: Long-running operations fail
   - Suggestion: Add progress indicators

## Learning Insights

### What's Working
1. Core workflow is intuitive (high completion)
2. Output quality meets expectations
3. Users return frequently (sticky)

### What Needs Improvement
1. Input guidance could be clearer
2. Error messages are too technical
3. No progress feedback for long ops

### Unexpected Patterns
1. Heavy weekend usage (investigate use case)
2. Users often run skill multiple times in session
3. Mobile usage higher than expected

## Evolution Recommendations

### Immediate (This Sprint)
1. Add input format examples
2. Improve error message clarity
3. Add progress indicators

### Near-term (Next Month)
1. Mobile experience optimization
2. Batch processing capability
3. Session persistence

### Long-term (Next Quarter)
1. AI-powered input suggestions
2. Custom workflow templates
3. Integration with related skills

## Success Forecast

Based on current trajectory:
- Completion rate: 87% → 92% (with recommended fixes)
- User satisfaction: 4.2 → 4.5
- Daily usage: 42 → 55 (+31%)

## Next Steps

- [ ] Implement immediate improvements
- [ ] A/B test new error messages
- [ ] Survey weekend users
- [ ] Plan mobile optimization
```

### 进化建议
```json
{
  "suggestion_id": "EVO-2024-001",
  "skill": "skill-name",
  "type": "incremental",
  "confidence": 0.85,
  "based_on": {
    "usage_pattern": "high_error_rate_on_input",
    "feedback_theme": "unclear_requirements",
    "success_impact": "medium"
  },
  "suggestion": "Add inline input validation with examples",
  "expected_impact": {
    "error_reduction": "40%",
    "completion_increase": "8%",
    "satisfaction_increase": "0.3 points"
  },
  "effort": "low",
  "priority": "high",
  "rationale": "45% of errors are input validation. Adding examples and real-time validation would significantly improve UX."
}
```

## 学习指标

### 使用指标

- 总使用次数
- 不同用户的使用情况
- 使用频率分布
- 完成所需时间
- 使用中的瓶颈

### 质量指标

- 成功率
- 错误类型及发生率
- 用户评分
- 用户收益（如转化率等）
- 净推荐值（Net Promoter Score）

### 进化指标

- 版本采纳率
- 功能使用情况
- 改进速度
- 学习周期时间
- 知识传递效果

## 质量要求

- 建议应基于数据而非假设
- 结合多个数据来源进行分析
- 在可能的情况下与用户确认分析结果
- 监测预测的准确性
- 记录学习过程以供后续参考
- 在不同技能间共享分析结果

## 常见使用场景

- “这个技能的表现如何？”
- “我们能从使用模式中学习到什么？”
- “根据用户反馈提出改进建议”
- “分析技能的有效性”
- “从错误中能发现哪些规律？”
- “这个技能应该如何发展？”
- “将当前版本与旧版本进行比较”

## 限制因素

- 需要足够的使用数据才能进行有意义的分析
- 找到的模式可能不适用于所有用户
- 相关性并不等同于因果关系