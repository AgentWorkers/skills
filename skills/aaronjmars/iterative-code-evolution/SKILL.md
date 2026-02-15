---
name: iterative-code-evolution
description: 通过结构化的分析-修改-评估循环（Analysis-Mutation-Evaluation loop）来系统地改进代码。该方法借鉴了ALMA（Automated meta-Learning of Memory designs for Agentic systems）的理念。适用于在代码质量迭代、实现优化、持续性问题调试，或通过多个改进周期来完善设计时使用。它取代了传统的“试错”方法，采用规范的反思流程、变体跟踪机制，以及基于原则的选择机制来决定下一步该修改哪些内容。
---

# 迭代式代码演进

这是一种结构化的方法论，通过“反思 → 修改 → 验证 → 评分”的循环来改进代码，该方法论借鉴了ALMA研究框架中用于元学习代码设计的理念。

## 适用场景

- 当代码的性能、正确性或设计存在问题，需要迭代改进时
- 在多轮修改后优化代码实现时
- 在调试持续存在或反复出现的问题时（简单的修复方法始终无效）
- 通过结构化的实验来改进系统设计时
- 在已经尝试了两种以上方法，但需要有条理地决定下一步该做什么时
- 在构建或改进提示系统、处理流程、代理程序或任何可以从迭代优化中受益的“程序”时

## 不适用场景

- 简单的一次性代码生成（直接编写即可）
- 有明确解决方案的机械性任务（重构、格式化、迁移等）
- 用户已经明确指出了需要修改的内容

## 核心概念

### 进化循环

每个改进循环都遵循以下步骤：

```
┌─────────────────────────────────────────────────────┐
│  1. ANALYZE  — structured diagnosis of current code │
│  2. PLAN     — prioritized, concrete changes        │
│  3. MUTATE   — implement the changes                │
│  4. VERIFY   — run it, check for errors             │
│  5. SCORE    — measure improvement vs. baseline     │
│  6. ARCHIVE  — log what was tried and what happened │
│                                                     │
│  Loop back to 1 with new knowledge                  │
└─────────────────────────────────────────────────────┘
```

### 进化日志

将所有迭代记录在项目根目录下的`.evolution/log.json`文件中。这份日志记录使得每次迭代都比上一次更高效。

```json
{
  "baseline": {
    "description": "Initial implementation before evolution began",
    "score": 0.0,
    "timestamp": "2025-01-15T10:00:00Z"
  },
  "variants": {
    "v001": {
      "parent": "baseline",
      "description": "Added input validation and error handling",
      "changes_made": [
        {
          "what": "Added type checks on all public methods",
          "why": "Runtime crashes from malformed input in 3/10 test cases",
          "priority": "High"
        }
      ],
      "score": 0.6,
      "delta": "+0.6 vs parent",
      "timestamp": "2025-01-15T10:30:00Z",
      "learned": "Input validation was the primary failure mode — most other logic was sound"
    },
    "v002": {
      "parent": "v001",
      "description": "Refactored parsing logic to handle edge cases",
      "changes_made": [
        {
          "what": "Rewrote parse_input() to use state machine instead of regex",
          "why": "Regex approach failed on nested structures (seen in test cases 7,8)",
          "priority": "High"
        }
      ],
      "score": 0.85,
      "delta": "+0.25 vs parent",
      "timestamp": "2025-01-15T11:00:00Z",
      "learned": "State machine approach generalizes better than regex for this grammar"
    }
  },
  "principles_learned": [
    "Input validation fixes give the biggest early gains",
    "Regex-based parsing breaks on recursive structures — prefer state machines",
    "Small targeted changes score better than large rewrites"
  ]
}
```

## 详细流程

### 第1阶段：分析 — 结构化诊断

在修改任何内容之前，先对当前代码及其输出进行结构化分析。这是最重要的阶段，可以避免不必要的修改。

**步骤1 — 从过去的修改中学习**（首次迭代可跳过）

查看进化日志。对于之前的每次修改：
- 代码的性能是否有所提升或下降？
- 是什么因素导致了修改的成功或失败？
- 提取2-3个可以借鉴的原则和2-3个需要避免的陷阱

**步骤2 — 组件级评估**

对每个有意义的组件（函数、类、模块、处理流程阶段）进行分类：

| 分类 | 含义 |
|-------|---------|
| **正常工作** | 产生正确的输出，没有发现问题 |
| **脆弱** | 在正常情况下可以工作，但在边缘情况或特定输入下会出错 |
| **损坏** | 产生错误的输出或错误 |
| **冗余** | 重复了其他地方的逻辑，增加了不必要的复杂性 |
| **缺失** | 需要的组件尚未实现 |

对于每个分类，写一句话解释其原因，并附上具体的测试输出或观察到的行为作为依据。

**步骤3 — 质量和一致性检查**

检查跨组件的问题：
- **数据流**：组件之间是否传递了结构化的数据，还是依赖于隐含的状态？
- **错误处理**：错误是否被捕获并处理了，还是被默默地忽略了？
- **重复代码**：相同的逻辑是否在多个地方重复出现？
- **硬编码**：是否存在魔法数字、硬编码的路径或特定于环境的假设？
- **泛化能力**：哪些部分可以在新的输入下仍然有效，哪些部分只是针对测试用例进行了过度优化？

**步骤4 — 提出优先级建议**

根据步骤1-3的内容，提出具体的修改建议。每个建议都必须基于实际的观察结果。

```
- PRIORITY: High | Medium | Low
- WHAT: Precise description of the change (code-level, not vague)
- WHY: Link to a specific observation from Steps 1-3
- RISK: What could go wrong if this change is made incorrectly
```

**规则：每个建议都必须有具体的观察依据。** 不要提出“这可能会有帮助”的建议，只提出基于代码或输出中实际发现的问题提出的修改。

**规则：每个循环最多提出3个建议。** 如果同时进行超过3个修改，将无法准确判断哪些修改导致了性能提升或下降。**

### 第2阶段：规划 — 确定修改内容

从分析结果中选择1-3个建议。选择原则如下：
- **优先处理关键问题** — 先修复损坏的部分，再优化正常工作的部分
- **每个循环专注于一个主题** — 不要同时进行不相关的修改（例如，不要在同一轮修改中同时修复解析问题和重构错误处理）
- **优先选择针对性的修改** — 对单个函数进行精细调整，而不是重写整个模块
- **如果遇到瓶颈，尝试其他方法** — 如果连续多个循环在同一组件上都没有取得明显效果，尝试修改另一个组件（这是ALMA框架中的“轮换原则”）

### 第3阶段：修改代码

编写新的代码。关键原则如下：
- **只修改计划中指定的内容**。避免在修改过程中试图“再修复一个问题”。
- **保持接口的一致性**。除非计划中有明确要求，否则不要修改函数签名或返回类型。
- **添加注释说明修改理由**。在每个修改处添加简短的注释，注明该修改所属的进化循环（例如：`# evo-v003：针对边缘情况错误切换到了状态机`）

### 第4阶段：验证 — 运行并检查

使用相同的输入和测试用例来运行修改后的代码。

**如果代码崩溃（最多尝试3次）：**

按照以下步骤进行修复：
1. 读取完整的错误堆栈跟踪信息
2. 找出**根本原因**（而不是表面现象）
3. **仅**修复根本原因，不要进行其他无关的改进
4. 重新运行代码

如果尝试3次后仍然失败，**恢复到原始版本** 并记录失败原因：
```json
{
  "attempted": "Description of what was tried",
  "failure_mode": "The error that couldn't be resolved",
  "learned": "Why this approach doesn't work"
}
```

这些失败记录非常宝贵，可以防止重复使用错误的修改方法。

**如果代码运行正常但输出错误：**

不要立即再次尝试。回到第1阶段（分析），使用新的输出结果重新进行分析。错误的输出可以作为诊断依据。

### 第5阶段：评分 — 测量改进效果

将新版本的代码性能与原始版本进行比较（而不仅仅是与基准版本进行比较）。评分方法因具体场景而异：

| 评估标准 | 评分方法 |
|---------|-------------|
| 测试情况 | 通过率：通过的测试数 / 总测试数 |
| 性能优化 | 性能指标的变化（延迟、吞吐量、内存使用） |
| 代码质量 | 权重评分标准（正确性、边缘情况处理、可读性） |
| 用户反馈 | 用户的评价（更好/更差/相同） |
| LLM/提示系统的输出质量 | 根据标准对输出样本进行评分 |

**始终比较新版本与原始版本的差异。** 这样才能判断哪些修改是有帮助的，哪些是有害的。

### 第6阶段：归档 — 记录并总结经验

更新`.evolution/log.json`文件：
1. 记录新版本的信息，包括原始版本、修改内容、评分结果和差异
2. 添加一个“learned”字段，简要说明这次迭代中学到了什么
3. 如果评分有所提升，将相关的改进原则添加到`principles_learned`列表中
4. 如果评分下降，将失败的原因添加到`principles_learned`列表中，作为需要避免的陷阱

## 变体管理

### 何时进行分支修改 vs. 何时直接修改

- **直接修改**（在同一文件中添加新版本）：当修改是渐进式的（修复错误、添加检查机制、调整参数等）
- **创建分支**（复制到新文件中）：当尝试根本不同的方法时（不同的算法、不同的架构、不同的策略）

将分支保存在`.evolution/variants/`目录下，并为每个分支添加描述性名称。进化日志会记录当前正在使用的版本。

### 选择下一个迭代对象

如果有多个代码变体，可以使用以下标准来选择下一个改进的目标：

```
score(variant) = normalized_reward - 0.5 * log(1 + visit_count)
```

其中：
- `normalized_reward` 表示变体的评分相对于基准版本的得分（0-1范围）
- `visit_count` 表示该变体被选中进行迭代的次数

这种方法平衡了“利用现有最佳版本”和“探索新方法”的需求，防止陷入局部最优解。

## 快速参考：分析模板

在进行第1阶段分析时，可以按照以下结构来组织思路：

```markdown
## Evolution Cycle [N] — Analysis

### Lessons from Previous Cycles
- Cycle [N-1] changed [X], score went [up/down] by [amount]
- Principle: [what we learned]
- Pitfall: [what to avoid]

### Component Assessment
| Component | Status | Evidence |
|-----------|--------|----------|
| function_a() | Working | All test cases pass |
| function_b() | Fragile | Fails on empty input (test #4) |
| class_C | Broken | Returns None instead of dict |

### Cross-Cutting Issues
- [Issue 1 with specific evidence]
- [Issue 2 with specific evidence]

### Planned Changes (max 3)
1. **[High]** WHAT: ... | WHY: ... | RISK: ...
2. **[Medium]** WHAT: ... | WHY: ... | RISK: ...
```

## 示例：完整的迭代流程

**场景**：用户要求改进一个网页爬虫，该爬虫在40%的目标页面上无法正常工作。

**第1轮迭代 — 分析：**
- 组件评估：`parse_html()` 出现问题（在没有 `<article>` 标签的页面上崩溃），`fetch_page()` 可以正常工作，`extract_links()` 在处理相对URL时存在问题
- 跨组件问题：没有错误处理机制——一个错误页面会导致整个批次失败
- 之前的修改记录：无
- 计划：[高优先级] 在 `parse_html()` 中为没有 `<article>` 标签的页面添加备用选择器

**第1轮迭代 — 修改：** 添加级联选择逻辑：首先尝试匹配 `<article>`，如果找不到则尝试匹配 `<main>`，如果仍然找不到则尝试匹配 `<body>`

**第1轮迭代 — 验证：** 代码运行正常，没有崩溃

**第1轮迭代 — 评分：** 通过率从40%提升到72%。提升幅度：+32%

**第1轮迭代 — 归档：** 学到的经验：“大多数失败是由于选择器未能正确匹配标签，而不是逻辑错误。备用选择器非常有效。”

**第2轮迭代 — 分析：**
- 经验：备用选择器提高了32%的性能。原则：在修复逻辑之前，先处理结构上的差异。
- 组件评估：`parse_html()` 现在可以正常工作，但 `extract_links()` 在处理相对URL时仍然存在问题
- 计划：[高优先级] 在 `extract_links()` 中使用 `urljoin` 方法来解析相对URL

**第2轮迭代 — 修改：** 添加URL解析功能

**第2轮迭代 — 评分：** 通过率从72%提升到88%。提升幅度：+16%

**第2轮迭代 — 归档：** 学到的经验：“URL解析是第二大问题。在提取数据时应该统一处理URL格式。”

## 关键原则

- **每个修改都必须基于具体的观察结果** — 避免随意的猜测性修改
- **每个循环最多进行3次修改** — 以便准确判断改进效果
- **记录所有修改过程** — 失败的尝试与成功的修改同样重要
- **与原始版本进行比较** — 而不仅仅是与基准版本进行比较
- **遇到瓶颈时尝试其他方法** — 如果连续多个循环在同一组件上都没有取得明显效果，尝试修改其他组件
- **在尝试3次失败后恢复到原始版本** — 避免陷入恶性循环；记录失败原因并尝试其他方法
- **不断总结经验**：进化日志中的 `principles_learned` 列表是最有价值的文档，它记录了适用于当前代码库的最佳实践