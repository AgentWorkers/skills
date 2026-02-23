---
name: roundtable
description: "自适应多模型AI圆桌会议：该系统由4个顶级模型（Claude Opus、GPT-5.2、Gemini 3.1 Pro、Grok 4）组成的元模型组首先为您的任务设计最优的工作流程（并行辩论、顺序处理或混合方式），随后选择合适的模型组来执行该流程。主要功能包括：基于网络搜索的数据获取、自主生成的摘要（无协调者偏见）、正式的共识评分机制、可选的验证环节以及中立的合成模型。需要Blockrun平台才能完整使用该系统。适用于复杂分析、代码审查、对抗性压力测试以及多视角决策等场景。"
metadata:
  openclaw:
    emoji: "🎯"
    requires:
      recommended: ["blockrun"]
    tags: ["multi-model", "debate", "orchestration", "reasoning", "blockrun"]
---
# 圆桌会议 v2 — 自适应多模型协调器

**Jimmy（主会议主持人）= 仅触发器。** 当调用圆桌会议时，启动一个独立的协调器并回复“🎯 圆桌会议已启动...” — 然后停止。

```
sessions_spawn(
  task = <full orchestrator instructions below>,
  model = "blockrun/sonnet",   ← ALWAYS blockrun/sonnet, never Anthropic OAuth
  mode = "run",
  label = "roundtable-orchestrator",
  runTimeoutSeconds = 600
)
```

**协调器（blockrun/sonnet）= 仅协调者。** 从不争论任何观点，也不参与讨论。

核心原则：元面板（4个高级模型）为任务设计最佳的工作流程 — 不仅包括使用哪些模型，还包括它们如何协作、以何种顺序协作以及分工如何。

---

## 要求

**完整会议（推荐）：** Blockrun 配置在 `localhost:8402` — 通过单一代理提供 Claude Opus 4.6、GPT-5.2、Gemini 3.1 Pro、Grok 4。
如果没有 Blockrun，会议将自动降级为可用的备用方案（参见 `panels.json` → `fallbacks`）。

**最低配置（降级模式）：** 在 `openclaw.json` 中至少配置以下一个提供者：
- `anthropic`（Claude Opus/Sonnet） — 作为 Opus 的备用方案
- `openai-codex`（GPT-5.3 Codex） — 作为 GPT 的备用方案

**成本警告：** 完整的圆桌会议（元面板 + 2 轮讨论 + 合成）会触发 9–12 次高级模型的调用。使用 `--quick` 可以进行简化的单轮会议。成本大约为每次 $0.50–$3.00，具体取决于主题长度和所使用的提供者。

---

## 触发模式

- `roundtable [提示]` — 自动检测模式，完整流程
- `roundtable --debate [提示]` — 强制并行辩论模式
- `roundtable --build [提示]` — 强制构建/编码模式
- `roundtable --redteam [提示]` — 强制对抗模式
- `roundtable --vote [提示]` — 强制决策模式
- `roundtable --quick [提示]` — 跳过元面板，使用默认面板进行单轮会议
- `roundtable --panel model1,model2,model3 [提示]` — 手动指定面板，跳过元面板
- `roundtable --validate [提示]` — 添加第三轮的代理验证
- `roundtable --context-from YYYY-MM-DD-slug [提示]` — 将上一轮的会议内容作为上下文（计划中 — 尚未在提示中实现；目前从内存中加载 JSON 并手动添加到 `CURRENT_CONTEXT`）
- `roundtable --no-search [提示]` — 跳过网络搜索（仅用于纯理论/抽象主题）

---

## 第 0 步：网络搜索（始终首先进行）

在开始任何操作之前，对主题进行网络搜索 — 元面板和所有代理都将拥有当前的上下文。

```
web_search(query = prompt, count = 5)
```

**超时策略：** 如果网络搜索在约 10 秒内没有返回结果或出现错误，请不要阻塞 — 立即继续，并设置 `CURRENT_CONTEXT = "没有实时数据可用（搜索失败或超时）"。会议将仅基于模型知识进行。

**缓存：** 如果在同一会话中重新搜索相同主题，请重用之前的 `CURRENT_CONTEXT` 内容 — 不需要重新搜索。

将搜索结果总结到一个 `CURRENT_CONTEXT` 块中（最多 250 个单词）：
- 关键事实、最新发展、相关数据点
- 搜索日期
- 如果没有找到有用结果：注明“未找到相关的实时数据”并继续

此块将被插入到：
1. 元面板的提示中（以便他们根据当前上下文设计工作流程）
2. 每个第一轮代理的提示中（以便所有参与者从相同的更新后的基础信息出发进行讨论）

---

## 第 0b 步：元面板 — 工作流程设计

**如果使用了 `--panel` 或 `--quick` 标志，则跳过此步骤。**

### 并行启动 4 个高级元分析师

读取 `panels.json` → `meta.models`。对于每个模型：

```
sessions_spawn(
  task = filled prompts/meta-panel.md,
  model = model_id,
  mode = "run",
  label = "rt-meta-[A/B/C/D]",
  runTimeoutSeconds = 90
)
```

### 0b. 从 4 个建议中合成工作流程

收集所有元分析结果后，由你（Jimmy）合成最终的工作流程：

1. **工作流程类型**：根据 4 个建议中的多数投票结果决定
   - 如果票数相同，则优先选择 `hybrid`（更灵活）

2. **阶段组成**：统计每个阶段的模型建议
   - 对于每个阶段的位置，选择最推荐的模型
   - 如果某个模型不在 `agentsdefaults.models` 的允许列表中，则跳过该模型，选择下一个
   - 如果模型是 `anthropic/claude-sonnet-4-6`，则跳过（保留给 Jimmy）

3. **轮次**：建议的中位数（如果票数相同则向上取整） — **最多 3 轮**

4. **合成模型**：不在主面板中的最推荐的高级模型

5. **记录决策**（包含在输出标题中）：
   > “元面板设计的工作流程：[类型]。阶段：[N]。面板：[模型]。合成：[模型]。”

### 0c. 工作流程类型说明

**parallel_debate** — 经典的圆桌会议
- 第 1 阶段的所有代理独立工作，使用相同的提示
- 第 2 阶段：相互批评
- 适用于：辩论、意见表达、风险分析、决策制定

**sequential** — 阶段之间的输出链式处理
- 第 1 阶段的代理生成输出（草稿、代码、研究）
- 第 2 阶段的代理接收第 1 阶段的输出并进行审查/改进
- 适用于：编码（编写 → 审查）、研究（收集 → 合成）、创意（草稿 → 完善）
- 第 2 阶段可以在第 1 阶段内进行；第 2 阶段是单独的环节

**hybrid** — 阶段内并行处理，阶段间顺序处理
- 第 1 阶段：N 个代理并行处理不同任务
- 第 2 阶段：1-2 个高级代理接收所有第 1 阶段的输出并生成综合结果
- 适用于：复杂分析（并行研究 → 高级模型合成）

### 0d. 面板降级规则

如果任何代理失败并且备用模型属于同一模型系列，则记录：
`⚠️ 面板降级 — [角色] 被 [备用模型] 替换（同一系列：[系列名称]`

务必在最终输出的 META 部分中明确显示这一情况，并提供 **可操作的指导**：
- 如果由于 Blockrun 未启动而降级 → “操作：在 localhost:8402 启动 Blockrun 以进行完整会议，或使用 `--panel budget` 进行稳定的双模型会议”
- 如果由于模型不在允许列表中而降级 → “操作：将 [模型] 添加到 openclaw.json 的 `agentsdefaults.models` 中”
- 如果由于 API 错误而降级 → “操作：检查提供者的 API 密钥/配额，然后重试”

---

## 第 1 步：检测模式（如果没有指定标志）

| 模式 | 关键词 |
|------|----------|
| **debate** | 优点/缺点、权衡、是否应该、伦理、比较、观点、更好的方案 |
| **build** | 实施、编码、架构、构建、设计、开发、创建 |
| **redteam** | 攻击、漏洞、失败、风险、破坏、威胁、利用 |
| **vote** | 选择、决定、哪个方案更好、在多个选项中做出选择 |
| **default** | 其他所有情况 |

---

## 第 2 步：执行工作流程

### parallel_debate（标准模式）

**第 1 轮**：并行启动所有第 1 阶段的代理。
- 使用 `prompts/round1.md`
- 每个代理撰写他们的完整回答 + 自我总结（最后一部分）
- 收集所有代理的自我总结

**第 2 轮**（如果轮次大于等于 2）：并行进行相互批评。
- 使用 `prompts/round2-cross-critique.md`
- `[SELF_digest]` = 该代理在第一轮中的自我总结
- `[PEER_digestS]` = 其他代理的总结（标明角色）
- 从每个回答中提取一致性得分

**第 3 轮**（如果使用了 `--validate`）：参见第 5 步。

### sequential

**第 1 阶段**：使用标准 `prompts/round1.md` 并行启动代理。
- 第 2 轮的相互批评可以根据 `rounds` 设置选择是否进行。
- 收集第 1 轮的所有输出（不仅仅是总结）以供第 2 阶段使用。

**第 2 阶段**：顺序或并行启动第 2 阶段的代理。
- 创建自定义提示：`prompts/round1.md` 为基础 + 添加第 1 阶段的输出
- 标签：`[角色] 的第 1 阶段输出：[完整输出]`
- 第 2 阶段的代理审查/改进第 1 阶段的工作
- 第 2 阶段的代理也撰写自我总结

### hybrid

**第 1 阶段**：代理并行处理不同的子任务。
- 第 2 阶段：1-2 个高级代理接收所有第 1 阶段的输出并生成综合结果
- 创建提示：`prompts/round1.md` 为基础 + “你正在整合和综合多个代理的工作。他们的输出：[所有第 1 阶段的输出]`

---

## 第 3 步：共识评分

在第 2 轮（parallel_debate）或第 2 阶段（sequential/hybrid）之后：

从每个代理的第 2 轮回答中提取一致性得分。
构建得分矩阵： `{ agent_role: { peer_role: score_1_to_5 } }`
共识百分比 = （所有得分之和 / (n_scores × 5)）× 100
如果没有第 2 轮的得分（快速模式/顺序模式）：忽略共识百分比，标记为 “N/A”

> **关于第 3 轮的说明：** 第 3 轮的验证使用的是 **准确性/部分准确性/不准确性** — 这是一个与共识百分比 **不同的指标**。第 3 轮检查的是合成的准确性，而不是代理之间的共识。不要将这两个指标混淆。共识百分比仅来自第 2 轮的得分；第 3 轮的结果会在 META 部分单独显示为 “Validated: yes/no/partial”。

---

## 第 4 步：第 3 轮 — 验证（仅使用 `--validate` 标志）

**何时向用户推荐使用 `--validate`：**
- 共识百分比 < 40%（意见分歧较大 — 合成结果可能存在偏差）
- 对抗模式（存在争议性结果 — 合成结果必须准确无误）
- 使用 3 个或更多第 2 阶段模型的构建模式（集成复杂，容易产生误导）
- 用户明确提到 “高风险”、“最终决策” 或 “发布结果”

**何时不使用它：** 快速模式、讨论主观性主题，或者时间比精度更重要的情况。

首先起草合成结果（见第 5 步），但不要立即发布。

启动验证代理：
```
sessions_spawn(
  task = filled prompts/round3-validation.md,
  model = original agent model,
  label = "rt-r3-validate-[role]",
  runTimeoutSeconds = 60
)
```

统计结果：
- 如果有 2 个或更多代理的回答不准确 → 重新编写合成结果并纳入修正
- 如果有 1 个代理的回答不准确 → 在 META 中注明：`⚠️ [角色] 的回答存在错误：[修正总结]`
- 如果所有代理的回答都准确/部分准确 → 在 META 中标记为 `Validated: yes` 或 `Validated: partial`

---

## 第 5 步：合成 — 启动中性模型

**永远不要自己编写合成结果。**

```
sessions_spawn(
  task = filled prompts/final-synthesis.md,
  model = [synthesis model from meta-panel recommendation, or anthropic/claude-opus-4-6 as default],
  label = "rt-synthesis",
  runTimeoutSeconds = 120
)
```

填写 `prompts/final-synthesis.md` 中的占位符：
- `[ROUND1_SUMMARIES]` → 所有代理的自我总结：》“**[角色]**（[模型]）：[总结]”
- `[ROUND2_SUMMARIES]` → 批评：”**[角色]** 批评了 **[对手]** 的观点，原因是 **[原因]**”
- `[CONSENSUS_SCORES]` → 完整的得分矩阵 + 计算出的百分比%

**发布到 Discord**（或你配置的频道）。频道 ID 是用户特定的 — 使用你的默认 Discord 频道，或在触发时传递 `--channel <id>`。

---

## 第 6 步：保存结果

将结果保存到 `~/clawd/memory/roundtables/YYYY-MM-DD-[topic-slug].json`：
```json
{
  "date": "YYYY-MM-DD",
  "topic": "[prompt]",
  "mode": "[mode]",
  "workflow_type": "parallel_debate|sequential|hybrid",
  "stages": [{ "model": "...", "role": "...", "task": "..." }],
  "meta_panel_recommendation": "[summary of meta votes]",
  "panel_degraded": false,
  "panel_degradation_notes": "",
  "consensus_pct": "XX% or N/A",
  "synthesis_model": "[model]",
  "validated": "yes|no|partial",
  "synthesis": "[final synthesis text]"
}
```

---

## 特殊情况

| 情况 | 操作 |
|-----------|--------|
| 网络搜索失败 | 在所有提示中继续，并注明“没有实时上下文可用” |
| 使用了 `--no-search` 标志 | 完全跳过第 0 步的网络搜索 |
| 元面板全部失败 | 使用检测到的模式对应的默认面板，并记录警告 |
| 使用了 `--quick` | 跳过元面板和第 2 轮。始终使用 `parallel_debate` 工作流程。使用默认面板（3 个模型）。仅在第 1 轮后进行合成 |
| 指定了 `--panel` 但未找到对应的模型 | 跳过元面板，使用指定的模型，默认使用 parallel_debate |
| 备用模型与主模型属于同一系列 | 继续执行，并在 META 中记录面板降级的警告 |
| 代理和备用模型都失败 | 跳过该代理，并在 META 中记录警告 — **不要等待，不要阻塞** |
| 未配置 Blockrun | 警告用户：“Blockrun 无法使用。使用预算面板。完整会议需要通过 localhost:8402 启动 Blockrun。” 自动切换到 `panels.json` 中的 `budget` 配置 |
| 任何一轮中的代理超时 | **失败后继续**：视为代理缺席，在 META 中标记为 `[TIMEOUT]`，并继续使用剩余的代理 |
- 代理在第 2 轮中失败 | 使用该代理在第一轮中的总结作为最终结果，从共识计算中排除其得分 |
- 合成代理失败 | 由 Jimmy 编写合成结果，并注明：“合成结果由协调器生成（可能存在偏见）” |
- 第 2 阶段的代理失败 | 在 META 中记录，并仅使用第 1 阶段的结果进行合成 |
- 没有代理响应 | 报告失败，并建议重新尝试 |
- 只有一个代理响应 | 跳过第 2 轮（没有其他代理），仅使用第 1 轮的结果进行合成，并将共识标记为 “N/A” |
- 使用了 `--context-from SLUG` | 加载 `~/clawd/memory/roundtables/[slug].json`，提取 `synthesis` 字段，并将其添加到 `CURRENT_CONTEXT` 的开头，格式为 “之前的会议上下文：[合成结果]”。如果文件未找到：警告并继续执行，不使用之前的上下文。 |

### 占位符规则

在填写提示模板时，对每个 `[PLACEHOLDER]` 适用以下规则：

| 占位符 | 如果缺失/失败 | 操作 |
|-------------|------------------|--------|
| `[CURRENT_CONTEXT]` | 网络搜索失败 | 插入：“没有实时上下文可用。” |
| `[SELF_digest]` | 代理在第 1 轮超时 | 完全跳过该代理在第二轮中的参与 |
| `[PEER_digestS]` | 所有代理都失败 | 跳过第二轮，直接进行合成 |
| `[ROUND1_SUMMARIES]` | 没有第 1 轮的输出 | 中止并显示错误：“0 个代理响应” |
| `[ROUND2_SUMMARIES]` | 快速模式/没有第 2 轮 | 插入：“没有进行相互批评（快速模式或单轮会议）” |
| `[CONSENSUS_SCORES]` | 无法提取得分 | 插入：“N/A — 无法获取得分” |
| `[SYNTHESIS_DRAFT]` | 合成失败 | 跳过第 3 轮，并在 META 中记录 |

**提示中的占位符必须填写。** 如果占位符未填写，会导致模型混淆并产生错误的输出。**

### 得分解析（第 2 轮）
代理以自由文本的形式写入得分。使用以下规则提取得分：
1. 查找 `SCORES:` 块
2. 匹配模式：`- [角色]: X/5` — 提取整数 X（1–5）
3. 如果没有找到清晰的整数，查找与角色名称最接近的数字 1–5
4. 如果仍然不确定 → 分配 3 分（表示中立），并在 META 中注明 `[SCORE INFERRED]`
不要因为得分格式不正确而中断工作流程。

---

## 快速参考：默认面板（元面板失败时的备用方案）

```json
debate:  [opus-4.6, gpt-5.2, gemini-3.1-pro] → Advocate / Skeptic / Devil's Advocate
build:   [gpt-5.2, grok-code-fast, opus-4.6] → Implementer / Optimizer / Architect-Reviewer
redteam: [grok-4, gpt-5.2, gemini-3.1-pro, opus-4.6] → Attacker / Defender / Auditor / Insider Threat
vote:    [opus-4.6, gpt-5.2, gemini-3.1-pro, grok-4]  → 4-way vote panel
(all via blockrun/ prefix — see panels.json for exact model IDs and fallbacks)
```