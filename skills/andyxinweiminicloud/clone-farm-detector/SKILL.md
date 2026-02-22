---
name: clone-farm-detector
description: 该工具有助于检测人工智能代理市场中存在的“克隆刷量”（即通过复制其他代理来提升自身排名）和“虚假声誉”（即通过虚假行为来伪造良好的评价）行为。它能识别出几乎完全相同的技能（这些技能可能用于掩盖代理的真实身份）、批量发布的模式，以及通过协同上传操作来人为制造的高声誉现象。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins: [curl, python3]
      env: []
    emoji: "🧬"
---
# 市场上40%的技能实际上是克隆品——在信任体系受到破坏之前发现这种行为

> 该工具有助于识别那些通过大量近乎相同的技能充斥代理市场（agent markets）的恶意行为，这些行为旨在操纵游戏声誉系统。

## 问题背景

代理市场根据技能的受欢迎程度、下载量以及发布者的声誉来对技能进行排名。这种机制反而激发了某些用户的不正当行为：他们以不同的名称发布数十个几乎完全相同的技能，并相互引用，以此人为地提升各项指标。其结果就是，真正的创新技能被这些克隆品所掩盖，搜索结果变得毫无意义，用户也无法区分哪些技能是真正的创新成果，哪些只是通过虚假手段提升声誉的产物。这种现象在人工智能领域类似于搜索引擎优化（SEO）中的垃圾信息（spam），而大多数市场对此毫无应对措施。

## 检测内容

该检测工具会从市场中选取一系列技能，通过以下指标来识别克隆行为：

1. **内容相似性**：比较这些技能的源代码（Capsule格式）和技能描述（Gene格式）。如果内容几乎完全相同，只是变量名称、注释或格式略有改动，就很可能是克隆品。
2. **批量发布模式**：在短时间内由同一发布者发布多个技能，尤其是那些使用序列化或模板化命名的技能。
3. **ID篡改**：虽然技能的SHA-256哈希值不同，但代码功能完全相同；这种行为通常是通过插入空白字符、注释或无操作语句来绕过重复检测机制实现的。
4. **相互引用关系**：某些技能在依赖关系链中相互引用，但实际上并无功能上的必要性，这种结构只是为了制造虚假的信任关系。
5. **元数据模板化**：所有技能的描述结构完全相同，使用的表情符号也一致，摘要内容只是简单地替换了名词而已。

## 使用方法

**输入**：
- 提供一组需要比较的Capsule/Gene格式的JSON对象。
- 提供一个发布者节点的ID，以便扫描该节点发布的所有技能。
- 提供一个市场搜索词，以检查搜索结果中是否存在克隆行为。

**输出**：
- 一份结构化的报告，包含：
  - 相似或相同技能的集群分组。
  - 被标记为相似的技能对之间的相似度评分。
  - 技能的发布时间线分析。
  - 风险等级：正常（CLEAN）、可疑（SUSPECT）或涉嫌克隆（FARMING）。
  - 每个技能集群的相关证据摘要。

## 示例

**输入**：扫描市场中搜索“code formatter”得到的前10个搜索结果。

```
🧬 FARMING DETECTED — 2 clone clusters found

Cluster A (4 skills, 92% avg similarity):
  - "python-formatter-pro"     published 2024-12-01 08:01
  - "py-code-beautifier"       published 2024-12-01 08:03
  - "format-python-fast"       published 2024-12-01 08:07
  - "python-style-fixer"       published 2024-12-01 08:12
  Publisher: same node (node_a8f3...)
  Technique: variable rename + comment injection
  ID washing: 4 unique hashes, 1 functional implementation

Cluster B (2 skills, 87% similarity):
  - "js-lint-helper"           published 2024-12-02
  - "javascript-lint-tool"     published 2024-12-02
  Publisher: same node (node_a8f3...)
  Cross-cites Cluster A skills as "dependencies"

Total: 6/10 top results are clones from one publisher.
Recommendation: Flag publisher for review. Genuine skills in results: 4/10.
```

## 限制

虽然相似性检测有助于发现可能的克隆品，但无法直接证明发布者的意图。合法的技能分支、模板化版本或教育性修改都可能导致误判。因此，建议通过人工审核来最终确认是否存在克隆行为。高相似度仅是一个提示，不能作为最终结论。