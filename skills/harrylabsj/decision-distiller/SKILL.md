---
name: decision-distiller
description: 将决策的背景、选项、权衡因素及结果整理成结构化的决策记录。适用于用户面临选择时、需要记录已做出的决策时，或需要分析过去的决策以寻找规律时。该记录会包含决策的依据、考虑过的替代方案以及从中获得的经验教训。
---
# 决策记录工具（Decision Distiller）

## 概述

决策记录工具（Decision Distiller）帮助用户捕捉、整理并学习在 OpenClaw 会议中做出的决策。它将非正式的决策过程转化为可文档化、可审查的记录，从而逐步构建组织的知识体系。

## 使用场景

在以下情况下使用该工具：
- 用户需要在多个选项中做出选择，并需要明确的决策依据；
- 已经做出决策，需要将其记录下来；
- 需要回顾或分析过去的决策；
- 需要识别不同会议中的决策模式；
- 用户要求“记录这个决策”或“说明我们为什么选择某个选项”。

## 核心概念

### 决策记录
一种结构化的文档，包含以下内容：
- **背景**：需要做出决策的情境；
- **选项**：考虑过的备选方案；
- **评估标准**：评估选项的方法；
- **决策结果**：最终的选择；
- **决策理由**：选择该选项的原因；
- **权衡因素**：所获得或放弃的东西；
- **决策结果**：决策的实际效果（可后续填写）；
- **经验教训**：从决策中总结出的知识。

### 决策状态
- **待定**：决策尚未做出；
- **已决定**：决策已做出，但结果尚未确定；
- **已验证**：决策被证明是正确的；
- **已修改**：根据新信息调整了决策；
- **已归档**：决策不再相关。

## 输入方式
该工具接受多种形式的决策信息：
- 关于选项的讨论记录；
- 列出优缺点的清单；
- 直接表达的选择结果；
- 回顾性分析。

## 输出内容
- 带日期的决策记录（Markdown 格式）；
- 决策摘要；
- 决策模式的分析结果；
- 决策状态报告。

## 工作流程

### 记录新决策
1. **确定背景**：
   - 是什么情境导致了需要做出决策？
   - 关键问题是什么？
   - 有哪些相关人员参与其中？

2. **列出选项**：
   - 考虑了哪些备选方案？
   - 哪些选项被提前排除了？
   - 哪些选项进入了最终评估阶段？

3. **定义评估标准**：
   - 是如何评估这些选项的？
   - 最重要的因素是什么？
   - 是否存在任何限制条件？

4. **记录决策**：
   - 最终选择了哪个选项？
   - 决策是在何时做出的？
   - 谁做出了这个决定？

5. **记录决策理由**：
   - 为什么选择这个选项？
   - 是什么因素影响了最终决策？
   - 做出了哪些假设？

6. **记录权衡因素**：
   - 放弃了什么？
  - 接受了哪些风险？
  - 错过了哪些机会？

### 回顾过去的决策
1. **收集记录**：
   - 收集相关的决策记录；
   - 可按主题、日期或状态进行筛选。

2. **分析决策模式**：
   - 常用的评估标准是什么？
   - 是否存在重复出现的权衡因素？
   - 决策通常遵循什么样的时间线？

3. **总结经验教训**：
   - 哪些做法是有效的？
   - 哪些方面可以改进？
   - 有哪些规律性现象？

## 输出格式

### 决策记录
```markdown
# Decision: [Title] - YYYY-MM-DD

**ID**: DEC-2024-001
**Status**: decided
**Decided By**: [Name/Role]
**Date**: YYYY-MM-DD

## Context
[Description of the situation requiring a decision]

## Options Considered

### Option 1: [Name]
- **Description**: 
- **Pros**: 
- **Cons**: 
- **Estimated Impact**: 

### Option 2: [Name]
- **Description**: 
- **Pros**: 
- **Cons**: 
- **Estimated Impact**: 

## Decision Criteria
1. [Criterion 1] - Weight: High/Medium/Low
2. [Criterion 2] - Weight: High/Medium/Low

## Decision
**Chosen**: [Option X]

## Rationale
[Why this option was selected over others]

## Trade-offs
- **Accepted**: [What we gave up]
- **Mitigated**: [How we reduced risks]

## Expected Outcome
[What we expect to happen]

## Actual Outcome
[Filled in later - what actually happened]

## Lessons Learned
[Filled in later - insights from the outcome]

## Related Decisions
- [Link to related decision]
```

## 命令说明

### 创建决策记录
```
decision create "Decision title" --status pending
```

### 更新决策记录
```
decision update DEC-2024-001 --status validated
```

### 列出所有决策
```
decision list --status decided --since 2024-01-01
```

### 分析决策模式
```
decision analyze --topic architecture
```

## 质量要求
- **具体明确**：模糊的决策无法提供有价值的经验教训；
- **包含备选方案**：没有备选方案的决策不算真正的决策；
- **记录决策理由**：未来的你需要知道决策背后的原因；
- **回顾决策结果**：只有了解了结果，决策才算完整；
- **关联相关决策**：帮助构建决策知识网络。

## 常见的使用提示
- “请记录这个决策：我们选择了 X”；
- “帮我在这两个选项 A 和 B 之间做出选择”；
- “我们在架构方面做出了哪些决策？”；
- “回顾上个月的部署决策”；
- “我决定使用 Y 而不是 Z，请记录下来”。

## 参考资源
- `references/decision-templates.md`：针对不同类型决策的模板；
- `references/analysis-frameworks.md`：用于分析决策的工具。