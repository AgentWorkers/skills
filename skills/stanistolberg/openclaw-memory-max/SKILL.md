---
name: openclaw-memory-max
description: SOTA Memory Suite — 包括自动回忆功能、跨编码器重排序机制、多跳深度搜索技术、因果知识图谱、情景记忆系统，以及夜间睡眠周期中的记忆巩固机制。
metadata:
  openclaw:
    emoji: "🧠"
    homepage: "https://github.com/stanistolberg/openclaw-memory-max"
---
# OpenClaw 最大内存容量

您使用的是 **最大内存容量**（Memory Max）这一先进的记忆系统，它将您的内存处理能力提升到了远超默认内存插件所能达到的水平。

## 目前激活的功能

### 自动化功能（无需手动操作）
- **自动回忆**：在每个回合开始前，与您当前任务最相关的记忆会被自动插入到您的上下文中，以 `<relevant-memories>` 的 XML 格式呈现。您无需手动搜索——相关内容会自动出现在您的视野中。
- **自动捕获**：对话结束后，系统会自动捕获重要的用户信息（规则、修改内容、偏好设置等），并保存这些信息以备夜间整合。
- **压缩保护**：当上下文窗口被压缩时，系统会先保留重要内容，避免重要信息被删除。
- **情景记录**：每次会话都会被记录为一个包含时间戳、使用工具及关键决策的“情景”。
- **夜间整合**：每天凌晨 03:00，系统会自动将捕获的记忆整合到 `MEMORY.md` 文件中，优化因果关系图，并清除过时的信息。

### 可用的工具

#### `precision_memory_search`
采用交叉编码器进行重新排序搜索，并结合信息的重要性进行筛选。返回最相关的 K 个记忆。
```json
{"query": "deployment configuration", "topK": 5}
```
当您需要从记忆中查找特定信息时，请使用此工具。该工具比默认的记忆搜索功能更精确，因为它会同时考虑查询内容和候选记忆之间的语义关联，而不仅仅是使用余弦相似度进行匹配。

#### `deep_memory_search`
多步检索功能：首先进行一次搜索，从结果中提取关键概念，然后基于这些概念再次进行搜索，最终将所有相关信息合并。
```json
{"query": "why did the migration fail last time"}
```
适用于需要处理复杂问题的情况，因为答案可能分布在多个相关的记忆中。

#### `reward_memory_utility`
对有用的记忆进行奖励，以提高其未来的检索优先级。
```json
{"memoryId": "abc-123", "rewardScalar": 0.2}
```
当某个记忆帮助您给出了正确答案时，请调用此函数。

#### `penalize_memory_utility`
对导致错误或无关紧要的记忆进行惩罚。
```json
{"memoryId": "abc-123", "penaltyScalar": 0.2}
```
当某个记忆让您做出了错误的决策时，请调用此函数。

#### `memory_graph_add`
记录因果关系链，并自动删除重复的记录。
```json
{"cause": "nginx misconfigured", "action": "added proxy_pass", "effect": "site loaded", "outcome": "success", "tags": ["nginx"]}
```
在完成任何有意义的操作后，请调用此函数来构建您的经验数据库。

#### `memory_graph_query`
通过语义匹配来查询过去的经验。
```json
{"query": "website not loading", "outcomeFilter": "success"}
```
在采取重大行动之前，请调用此函数，以了解过去的经验是否有助于您做出正确的决策。

#### `memory_graph_summary`
获取所有学习到的因果关系的总结信息（成功/失败次数、最常见模式、近期结果等）。
```json
{}
```
在会话开始时使用此函数，可以帮助您快速了解自己的经验。

#### `compress_context`
提示系统需要压缩上下文。返回上次压缩过程中保留的内容。
```json
{"compression_reason": "context window approaching limit after long debugging session"}
```

## 规则

1. **自动回忆功能始终开启**：您会在上下文中看到 `<relevant-memories>` 标签下的记忆内容，请务必使用它们。
2. **奖励有用的记忆**：当某个记忆帮助您正确回答问题时，调用 `reward_memory_utility` 以增强记忆系统的检索能力。
3. **惩罚错误的记忆**：当某个记忆导致错误时，调用 `penalize_memory_utility` 以防止类似错误再次发生。
4. **记录因果关系**：在完成重要操作（如使用工具、做出决策、解决问题等）后，请调用 `memory_graph_add`。这有助于您的未来版本更好地利用这些经验。
5. **行动前先回顾经验**：在采取重大行动之前，调用 `memory_graph_query` 来查看是否曾经遇到过类似的情况。
6. **使用深度搜索处理复杂问题**：如果 `precision_memory_search` 无法找到所需信息，可以尝试 `deep_memory_search`，它能够跨多个记忆链进行搜索。

## 通过 YAML 固定规则

用户可以通过在 `MEMORY.md` 文件中添加 YAML 代码块来固定某些关键规则：

```markdown
<!--yaml
rules:
  - weight: 1.0
    constraint: "Never delete production data"
  - weight: 0.5
    preference: "Prefer TypeScript over JavaScript"
-->
```

权重大于或等于 1.0 的规则会在您的系统提示中显示为 **关键约束**（CRITICAL CONSTRAINTs）。请务必遵守这些规则。