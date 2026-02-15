---
name: "Synthesize"
description: "通过源代码跟踪、冲突解决以及覆盖范围验证，将多个来源的数据整合为统一的分析结果。"
---

## 核心原则

当来源之间存在隐性的矛盾或覆盖范围存在空白时，综合分析就会失败。必须记录所有信息，并明确解决这些冲突。

## 协议

```
Gather → Map → Extract → Reconcile → Synthesize → Verify
```

### 1. 收集数据

整理所有来源及其元数据：
```
| # | Source | Type | Date | Credibility | Scope |
```

标记：过时的来源、权威级别不一致的来源、覆盖范围有空白的来源。

### 2. 分析数据

识别不同来源之间的共同主题，并构建重叠矩阵：
- 哪些来源涵盖了哪些主题？
- 各来源在哪些观点上存在分歧？
- 有哪些内容仅被某个来源提及？

### 3. 提取关键信息

从每个来源中提取关键主张、证据和独特的见解。
为每条提取的内容标注来源编号，确保所有信息都有明确的出处。

### 4. 协调分歧

对于存在分歧的内容：
- 明确记录这些分歧；
- 根据信息的最新性、权威性和证据的质量来权衡这些分歧；
- 选择一种观点进行展示，或者同时呈现两种观点并说明原因。

切勿默默地选择其中一种观点。分歧本身就是一个有价值的信号。

### 5. 综合分析

将提取的信息整合成统一的叙述：
- 以各方达成共识的内容作为开头；
- 显示出观点上的差异（例如：A认为X，B认为Y，原因在于……）；
- 突出那些仅被某个来源提及的独特见解。

### 6. 验证结果

在发布最终结果之前进行验证：
- 确保所有来源都被考虑在内；
- 没有任何主题被遗漏；
- 所有分歧都得到了解决；
- 所有覆盖范围的空白都得到了承认。

## 输出格式

```
📚 SOURCES: [count] ([types breakdown])
🎯 SYNTHESIS: [unified narrative]
⚡ KEY INSIGHTS: [bulleted, with source attribution]
⚠️ TENSIONS: [conflicts and resolution reasoning]
🕳️ GAPS: [what wasn't covered, needs more research]
```

## 在以下情况下应拒绝执行

- 来源过于多样化，导致难以协调；
- 项目范围不明确；
- 时间不足，无法进行有效的协调。

参考文档：`source-types.md`、`conflict-resolution.md`、`coverage-matrix.md`