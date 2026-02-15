---
name: chain-of-density
description: "使用“密度链”（Chain-of-Density）技术迭代地优化文本摘要。该技术适用于压缩冗长的文档内容、精简需求描述，或在保留信息密度的同时生成简洁的执行摘要。"
license: Apache-2.0
compatibility: "Python 3.10+ (for text_metrics.py script via uv run)"
metadata:
  author: agentic-insights
  version: "1.2"
  paper: "From Sparse to Dense: GPT-4 Summarization with Chain of Density Prompting"
  arxiv: "https://arxiv.org/abs/2309.04269"
---

# 密度链摘要技术（Chain-of-Density Summarization）

该技术通过迭代的方式，根据 CoD 论文中的方法论对文本进行压缩。每次迭代都会识别出源文本中的缺失实体，并将这些实体添加到摘要中，同时保持摘要的字符长度不变。

## 技术原理

“密度链摘要”技术通过多次迭代来实现压缩目标：

1. **第 1 次迭代**：生成一个简洁但信息量较大的基础摘要（包含 `target_words` 个单词）。
2. **后续迭代**：每次迭代都会：
   - 从源文本中识别出 1-3 个缺失的实体。
   - 重新编写摘要以包含这些实体。
   - 确保压缩后的摘要单词数量与原始摘要相同。

**核心原则**：仅添加缺失的实体，绝不删除任何实体。

## 实体筛选标准

每个被添加的实体必须满足以下 5 个标准：

| 标准 | 描述 |
|---------|---------|
| **相关性** | 与主题紧密相关 |
| **具体性** | 描述性强且简洁（不超过 5 个单词） |
| **新颖性** | 在之前的摘要中未出现过 |
| **真实性** | 确实存在于源文本中 |
| **来源多样性** | 可以来自源文本的任何部分 |

## 快速入门步骤

1. 用户提供需要压缩的文本。
2. 通过 `cod-iteration` 代理执行 5 次迭代。
3. 每次迭代都会通过 `Missing_Entities:` 行报告新增的实体信息。
4. 最后返回压缩后的摘要以及实体添加的历史记录。

## 运行流程

```
Iteration 1: Sparse base (target_words, verbose filler)
     ↓ Missing_Entities: (none - establishing base)
Iteration 2: +3 entities, compress filler
     ↓ Missing_Entities: "entity1"; "entity2"; "entity3"
Iteration 3: +3 entities, compress more
     ↓ Missing_Entities: "entity4"; "entity5"; "entity6"
Iteration 4: +2 entities, tighten
     ↓ Missing_Entities: "entity7"; "entity8"
Iteration 5: +1-2 entities, final density
     ↓ Missing_Entities: "entity9"
Final dense summary (same word count, 9+ entities)
```

## 运行方式

**第 1 次迭代**：仅传递源文本：

```
Task(subagent_type="cod-iteration", prompt="""
iteration: 1
target_words: 80
text: [SOURCE TEXT HERE]
""")
```

**第 2-5 次迭代**：同时传递之前的摘要和源文本：

```
Task(subagent_type="cod-iteration", prompt="""
iteration: 2
target_words: 80
text: [PREVIOUS SUMMARY HERE]
source: [ORIGINAL SOURCE TEXT HERE]
""")
```

**重要提示**：
- 这些迭代需要依次执行，不能并行进行。
- 每次迭代都需要传递源文本以识别缺失的实体。
- 通过 `Missing_Entities:` 行来跟踪添加的实体信息。

## 代理输出格式

`cod-iteration` 代理会返回以下格式的结果：

```
Missing_Entities: "entity1"; "entity2"; "entity3"

Denser_Summary:
[The densified summary - identical word count to previous]
```

需要解析这两个部分：一部分用于记录实体添加的历史信息，另一部分用于传递给下一次迭代。

## 密度计算方法

使用 `scripts/text_metrics.py` 脚本来进行精确的单词计数：

```bash
echo "your summary text" | uv run scripts/text_metrics.py words
# Returns: word count

uv run scripts/text_metrics.py metrics "your summary text"
# Returns: {"words": N, "chars": N, "bytes": N}
```

## 参数设置

| 参数 | 默认值 | 说明 |
|---------|---------|-------------|
| iterations | 5 | 迭代次数（论文中推荐使用 5 次） |
| target_words | 80 | 所有迭代过程中保持不变的单词数量 |
| return_history | false | 是否包含中间摘要和实体信息 |

**注意**：`target_words` 可根据源文本的长度和所需的压缩效果进行调整。

## 输出格式

- **简化格式（默认）**：```
[Final dense summary text]
```
- **包含历史记录的格式（return_history=true）**：```yaml
final_summary: |
  [Dense summary at target_words with accumulated entities]
iterations:
  - turn: 1
    missing_entities: "(none - establishing base)"
    words: 80
    summary: |
      [Sparse iteration 1]
  - turn: 2
    missing_entities: "entity1; entity2; entity3"
    words: 80
    summary: |
      [Denser iteration 2]
  # ... etc
total_entities: 9
```

## 适用场景

- 长度超过 500 字的冗长文档
- 需要精简的内容（如需求文档）
- 从详细报告中提取核心信息的执行摘要
- 需要压缩的技能描述（超过推荐长度的文档）

## 不适用场景

- 法律/合规性文本（需要高度精确性）
- 教程内容（初学者需要详细的解释）
- 已经非常简洁的文本（少于 300 字）
- 技术规范（不应被压缩）

## 示例

**源文本**（180 字，内容较为冗长）：
```
The name field is a required field that must be present in every skill.
The name field identifies the skill and must follow a specific format.
For the name field, you should use lowercase letters and hyphens only.
The name field can be 1 to 64 characters long. The description field
is also required and tells agents when to use your skill...
```

**第 1 次迭代**（生成的摘要，包含 80 个单词）：
```
Missing_Entities: (none - establishing base)

Denser_Summary:
This document discusses the requirements for skill configuration fields in agent systems. It covers various aspects of how fields should be formatted and what values they can contain. The document also mentions validation rules that apply to these fields and provides guidance on best practices for developers. Additionally, it includes information about both optional and required elements that need to be considered when creating new skills for the system.
```

**第 3 次迭代**（经过两次迭代后，摘要仍为 80 个单词）：
```
Missing_Entities: "1-64 characters"; "lowercase alphanumeric-hyphens"; "Use when phrase"

Denser_Summary:
Skills require `name` (1-64 chars, lowercase alphanumeric-hyphens) and `description` fields with validation rules. The name identifies skills; descriptions tell agents when to invoke using "Use when..." phrases. Both fields have format constraints and best practices. Optional metadata fields provide author, version, and compatibility information for cross-platform agent discovery.
```

**第 5 次迭代**（最终生成的摘要，保持 80 个单词，达到最大压缩效果）：
```
Missing_Entities: "Claude Code"; "Cursor"; "GitHub Copilot"

Denser_Summary:
Required: `name` (1-64 chars, ^[a-z0-9]+(-[a-z0-9]+)*$) and `description` (1-1024 chars) with validation. Description includes "Use when..." + discovery keywords for auto-invocation. Optional: license (SPDX), compatibility, metadata (author, version, tags). Cross-platform: Claude Code, Cursor, GitHub Copilot. Name matches directory. Progressive disclosure via references/, assets/, scripts/ subdirectories.
```

## 架构说明

该技术实现了 [CoD 论文](https://arxiv.org/abs/2309.04269) 中提出的方法论：
- **Skill**：负责整个流程的协调工作（即本文件）。
- **Agent**：无状态的工作进程（`cod-iteration`）。
- **Script**：用于执行具体操作的脚本（`text_metrics.py`）。
- 下级代理不能直接调用其他代理；所有操作都必须通过 `Task` 工具来协调。

## 参考文献

- 论文：[From Sparse to Dense: GPT-4 Summarization with Chain of Density Prompting](https://arxiv.org/abs/2309.04269)
- 数据集：[HuggingFace griffin/chain_of_density](https://huggingface.co/datasets/griffin/chain_of_density)