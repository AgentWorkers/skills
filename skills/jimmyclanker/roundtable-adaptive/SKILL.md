---
name: roundtable
description: "**自适应多模型AI圆桌会议**：该会议最多可支持4个AI模型参与（配置灵活），通过两轮辩论进行交流与评估，并采用交叉批评和正式的共识评分机制。会议需要配置相应的Anthropic服务提供商（推荐使用Claude Opus）；也可通过Blockrun代理额外接入GPT-5.3 Codex（OpenAI）、Grok 4和Gemini 3.1 Pro等模型。如果可选服务提供商不可用，系统会自动切换为仅使用Claude模型。所有辩论结果会保存到本地文件系统中。其中，辩论环节的参与者使用持久化的线程会话进行交流，而元讨论环节及结果综合环节的参与者则为一次性使用的临时会话。"
metadata:
  clawdis:
    emoji: "🎯"
    requires:
      env:
        - ANTHROPIC_API_KEY
      config:
        - providers.anthropic
    config:
      requiredEnv:
        - "ANTHROPIC_API_KEY (required — Claude panelist; use API key or OAuth in openclaw.json)"
        - "OPENAI_API_KEY (optional — GPT-5.3 Codex panelist; falls back to Claude if absent)"
        - "BLOCKRUN_PROXY_URL=http://localhost:8402 (optional — adds Grok 4 + Gemini 3.1 Pro; install via openclaw plugins install @blockrun/clawrouter)"
      stateDirs:
        - "{workspace}/memory/roundtables"
    tags:
      - multi-model
      - debate
      - orchestration
      - reasoning
      - claude
      - gpt
      - grok
      - gemini
      - blockrun
---
# 圆桌会议 v2 — 自适应多模型协调器

**触发方式：** 从您的代理监控的任何频道中执行 `roundtable [--mode] [prompt]` 命令。
**输出结果：** 会发布到您配置的输出频道（在 OpenClaw 配置中设置 `ROUNDTABLE_OUTPUT_CHANNEL`；否则结果将返回到触发命令的频道）。
**参与会议的代理：** 持久性会话（`mode="session", `thread=true`）——会在 Discord 线程中保持活跃状态，以便后续提问。元面板分析师和综合代理为一次性使用（`mode="run"`）。

**请注意：协调器仅负责任务的组织和调度。** 除非在 `panels.json` 中另有指定，否则将使用默认模型。协调器不会参与讨论或表达任何观点。

**核心机制：** 元面板（包含 4 个高级模型）会设计出最适合当前任务的工作流程（可以是并行辩论、顺序处理或混合模式），然后由相应的代理执行该流程。

## 配置

在使用之前，请在 `panels.json` 中设置输出频道（或者使用触发命令的频道）：
```json
{
  "output": {
    "channel": "discord",
    "target": "YOUR_CHANNEL_ID_HERE"
  }
}
```

**（如果使用 Discord 线程：** 为每个圆桌会议创建一个单独的线程，以保持讨论的条理性）：
```json
{
  "output": {
    "channel": "discord",
    "target": "YOUR_CHANNEL_ID_HERE",
    "useThreads": true
  }
}
```
**如果没有进行此配置，结果将直接发布到命令执行的频道。**

## 成本透明化

| 组件 | 每次完整运行的成本 |
|-----------|-----------------|
| Claude Opus (OAuth) | 免费 |
| GPT-5.3 Codex (OAuth) | 免费 |
| Gemini 3.1 Pro (Blockrun) | 约 0.05 美元 |
| Grok 4 (Blockrun) | 约 0.08 美元 |
| **（完整团队模式）** | **约 0.13–0.50 美元** |
| **简化模式（仅使用 Claude）** | **免费** |
**使用 `--quick` 标志可减半成本（仅运行 1 轮）。**

---

## 设置

**（简化模式——免费）：**
1. 在 `openclaw.json` 中配置 `anthropic` 提供者（使用 OAuth 或 API 密钥）。
2. （可选）为 GPT-5.3 Codex 配置 `openai-codex`。
3. 完成配置后，Grok/Gemini 会默认使用 Claude Sonnet 模型。

**（完整团队模式：** 需要使用 Blockrun：）
1. 安装 Blockrun 插件：`openclaw plugins install @blockrun/clawrouter`，然后重启 `openclaw gateway`。
2. 用 USDC 向 Blockrun 的钱包充值（费用约为 5–10 美元）。充值地址会在安装过程中显示。
3. 完整团队模式的每次运行成本约为 0.13–0.50 美元；Claude 和 GPT 模型仍可通过 OAuth 免费使用。

**结果会保存在 `{workspace}/memory/roundtables/YYYY-MM-DD-slug.json` 文件中（文件会自动生成）。**

## 触发模式

### 可选：自动将结果发布到指定频道
您可以在 `AGENTS.md` 中配置一个专门用于圆桌会议的 Discord 频道：
```
Any message in channel [YOUR_CHANNEL_ID] → treat as a roundtable topic automatically.
No prefix needed. Message → auto-detect mode → create thread → spawn orchestrator.
```
**这完全是可选的；** 显式的 `roundtable` 命令可以从任何频道触发讨论。

### 显式触发方式（适用于任何频道）：

- `roundtable [prompt]` — 自动选择默认工作流程。
- `roundtable --debate [prompt]` — 强制使用并行辩论模式。
- `roundtable --build [prompt]` — 强制使用构建/编码模式。
- `roundtable --redteam [prompt]` — 强制使用对抗性讨论模式。
- `roundtable --vote [prompt]` — 强制使用决策模式。
- `roundtable --quick [prompt]` — 跳过元面板，使用默认工作流程，仅运行 1 轮。
- `roundtable --panel model1,model2,model3 [prompt]` — 手动指定团队成员，跳过元面板。
- `roundtable --validate [prompt]` — 添加第三轮代理对综合结果的验证。
- `roundtable --no-search [prompt]` — 跳过网络搜索（仅适用于纯理论性/抽象性主题）。

---

## 第一步：创建讨论线程（必须首先执行）

在开始之前，请在配置好的频道中创建一个讨论线程，并保存该线程的 ID。

### -1a) 避免重复
**（必需）** 如果同一主题被多次触发，要防止创建重复的线程。

1. 对主题字符串进行规范化处理：
   - 转换为小写
   - 去除多余的空白字符
   - 合并多个空格
   - 删除结尾的标点符号
2. 列出目标频道中最近的所有讨论线程：
```
message(action='thread-list', channel='discord', channelId='[CHANNEL_ID]', limit=25)
```
3. 如果存在一个在过去 24 小时内创建的、且主题与规范化后的主题匹配的活跃线程（并且带有类似的标签，例如 `[[DEBATE]]`）：
   - **重用该线程**（`THREAD_ID = existing_thread_id`）
   - 发布提示：`♻️ 发现重复主题——将使用现有线程。`
   - **不要重新启动协调器或团队流程。**
4. 如果没有匹配的线程：创建一个新的线程。

### -1b) 创建新线程
```
message(
  action = 'thread-create',
  channel = '[your configured channel]',
  channelId = '[CHANNEL_ID from user config]',
  threadName = '🎯 [topic — max 8 words] [[MODE]]',
  message = '**Panel:** [model list]\n**Mode:** [mode] | **Rounds:** [N]\n⏳ Analysis in progress...'
)
```

将返回的线程 ID 保存为 `THREAD_ID`。
**后续的所有 `message()` 调用都应使用 `target = THREAD_ID`，而不是频道 ID。**

如果创建线程失败或频道未配置，则直接在当前频道发布结果。

---

## 第 0 步：进行网络搜索（始终优先执行）

在任何操作之前，先对主题进行网络搜索——这样元面板和所有代理都能获得最新的背景信息。
```
web_search(query = prompt, count = 5)
```

**超时策略：** 如果网络搜索在 10 秒内没有返回结果或出现错误，请不要停止搜索，而是立即继续执行，并在输出中显示 `CURRENT_CONTEXT = "没有实时数据可用（搜索失败或超时。"`。此时讨论将仅基于模型提供的信息进行。

**缓存机制：** 如果在同一会话中再次搜索相同主题，直接使用之前的 `CURRENT_CONTEXT` 内容，避免重复搜索。

将搜索结果总结为 `CURRENT_CONTEXT` 块（最多 250 个单词）：
- 关键事实、最新进展、相关数据点
- 搜索日期
- 如果没有找到有用信息：注明“未找到相关的实时数据”，然后继续讨论。

**`CURRENT_CONTEXT` 块的内容会被插入到：**
1. 元面板的提示中（以便他们根据最新信息设计工作流程）
2. 每个参与讨论的代理的提示中（确保所有参与者都基于相同的背景信息进行讨论）

---

## 第 0b 步：元面板——工作流程设计

**在以下情况下可以跳过此步骤：** 使用了 `--panel` 或 `--quick` 标志。

### 并行启动 4 个高级元分析师
读取 `panels.json` 文件中的 `meta.models` 配置。
```
sessions_spawn(
  task = filled prompts/meta-panel.md,
  model = model_id,
  mode = "run",
  label = "rt-meta-[A/B/C/D]",
  runTimeoutSeconds = 90
)
```

### 0b. 根据 4 个建议生成最终工作流程

收集所有元分析结果后，协调器会生成最终的工作流程：
1. **工作流程类型**：根据 4 个建议中的多数意见来决定（如果意见相同，则选择更灵活的 **混合模式**）。
2. **各阶段的模型选择**：统计每个阶段推荐的模型数量；
   - 对于每个阶段，选择推荐次数最多的模型；
   - 如果某个模型不在 `agents.defaults.models` 的允许列表中，则跳过该模型；
   - 如果某个模型是协调器专用的模型，则也跳过它（协调器不能作为团队成员参与）。
3. **轮次安排**：根据推荐结果的中位数来决定轮次（如果结果相同，则向上取整，最多允许 3 轮）。
4. **综合使用的模型**：选择在主要团队中未被推荐的、但被推荐次数最多的高级模型。
5. **记录决策结果**（包含在输出标题中）：
   > “元面板设计的工作流程：[类型]。阶段：[数量]。团队成员：[模型列表]。综合使用的模型：[具体模型]。”

### 0c. 各工作流程类型的说明

- **parallel_debate**（并行辩论）：所有代理在第一阶段独立工作，使用相同的提示。
  - 第二阶段进行相互批评。
  - 适用于辩论、意见交流、风险分析、决策制定等场景。
- **sequential**（顺序处理）：各阶段之间有明确的输出顺序。
  - 第一阶段的代理生成初步结果（草稿、代码、研究内容）；
  - 第二阶段的代理接收第一阶段的成果并进行审查/改进。
  - 适用于编码（编写 → 审查）、研究（收集 → 综合）、创意创作（草稿 → 完善）等场景。
- **hybrid**（混合模式）：第一阶段内各代理并行工作；第二阶段由 1–2 个高级代理整合所有第一阶段的成果。
  - 适用于复杂分析（需要多方面并行研究后再进行综合处理的场景）。

### 0d. 团队成员替换规则

如果某个代理失败，将使用同一模型家族中的其他代理进行替换：
`⚠️ 团队功能降级 — [角色] 由 [替换模型] 替代（属于同一模型家族）`

**请务必在最终输出的 META 部分明确说明替换情况，并提供相应的操作指南：**
- 如果是因为 Blockrun 服务不可用导致的降级：**操作建议：在本地主机 8402 端启动 Blockrun 服务以使用完整团队模式；或者使用 `--panel budget` 选项来使用稳定的双模型团队模式。**
- 如果是因为模型不在允许列表中导致的降级：**操作建议：将 [模型名称] 添加到 `agentsdefaults.models` 文件中。**
- 如果是因为 API 错误导致的降级：**操作建议：检查提供者的 API 密钥或配额，然后重试。**

---

## 第 1 步：确定讨论模式（如果没有指定模式）

| 模式 | 关键词 |
|------|----------|
| **debate** | 优缺点、权衡、是否可行、伦理问题、比较、观点、最佳方案 |
| **build** | 实施、编码、架构设计、开发、创建 |
| **redteam** | 攻击、漏洞、风险、故障、威胁、利用方法 |
| **vote** | 选择方案、做出决策、确定最佳选项 |
| **default** | 其他所有情况 |

---

## 第 2 步：执行工作流程

### parallel_debate（标准模式）

**第 1 轮：** 并行启动所有团队成员的会话（会话为持久性类型）。
```
sessions_spawn(
  task = filled prompts/round1.md,
  model = model_id,
  mode = "session",        ← persistent — stays alive in the thread
  label = "rt-[role]",
  thread = true            ← bound to the thread from Step -1
)
```

- 保存每个会话的 ID：`{"attacker": sessionKey, "defender": sessionKey, ... }`
- 每个代理都会撰写完整的回答以及自己的总结（最后一部分）。
- 收集所有代理的总结内容。
- ⚠️ 代理会保持在线状态，用户可以直接向他们提问以获取更多信息。

**第 2 轮（如果有多轮讨论）：** 通过 `sessions_send` 将交叉批评的提示发送给所有已有的会话。
- 不需要重新创建会话——直接使用第一轮的会话 ID。
- `[SELF_DIGEST]` 表示该代理在第一轮中的总结内容；
- `[PEER_digestS]` 表示其他代理的总结内容（会标明他们的角色）。
- 从每个回答中提取代理之间的共识分数。

**第 3 轮（如果使用了 `--validate` 标志）：** 请参考第 4 步的说明。**

### sequential（顺序处理模式）

**第 1 阶段：** 并行启动所有团队成员的会话（`mode="session", `thread=true`）。
- 使用标准的 `prompts/round1.md` 作为提示。
- 通过 `sessions_send` 将交叉批评的提示发送给所有已有的会话（不重新创建会话）。
- 收集第一阶段的全部输出结果，用于第二轮讨论。

**第 2 阶段：** 启动新的持久性会话（`mode="session", `thread=true`）。
- 编写提示时，以 `prompts/round1.md` 为基础，并添加第一阶段的输出作为背景信息。
- 标题格式为：“[角色] 的第一阶段输出：[全部内容]”。
- 第二阶段的代理会审查/改进第一阶段的成果，并撰写自己的总结。

### hybrid（混合模式）

**第 1 阶段：** 各代理并行工作（`mode="session", `thread=true`），每个代理负责不同的任务。
- 第 2 阶段：1–2 个高级代理接收所有第一阶段的输出，并整合成最终结果。
- 适用于需要多方面并行研究后再进行综合处理的复杂分析场景。

---

## 第 3 步：计算共识分数

在完成第 2 轮讨论（parallel_debate）或第二阶段（sequential/hybrid）后：
从每个代理的第二轮回答中提取共识分数。
生成分数矩阵：`{ agent_role: { peer_role: score_1_to_5 } }`
计算共识百分比：`(所有分数之和 / (总分数数 × 5)) × 100`
如果第二轮没有分数（快速模式或顺序处理模式），则忽略共识百分比，标记为 “N/A”。

> **关于第三轮的说明：** 第三轮的评估目的是检查综合结果的准确性，而不是代理之间的共识程度。这两者是不同的评估指标。第三轮的评估结果会单独显示在 META 部分，标记为 “Validated: yes/no/partial”。

---

## 第 4 步：第三轮——验证（仅在使用 `--validate` 标志时执行）

**在以下情况下建议使用 `--validate`：**
- 共识百分比低于 40%（表示意见分歧较大，综合结果可能存在偏差）；
- 使用对抗性讨论模式（需要高度可靠的综合结果）；
- 使用三个或更多第二阶段模型的复杂整合场景；
- 用户明确要求进行最终决策或需要发布结果。

**在这种情况下，先生成初步的综合结果（步骤 5），但不要立即发布。**

然后启动验证代理：
```
sessions_spawn(
  task = filled prompts/round3-validation.md,
  model = original agent model,
  label = "rt-r3-validate-[role]",
  runTimeoutSeconds = 60
)
```

根据评估结果采取相应措施：
- 如果有 2 个或更多个模型的评估结果不准确，**重新编写综合报告**；
- 如果只有 1 个模型的评估结果不准确，在 META 中标注：`⚠️ [角色] 的回答存在问题：[问题描述及修正措施]`；
- 如果所有模型的评估结果都准确或部分准确，在 META 中标记为 “Validated: yes” 或 “Validated: partial”。

---

## 第 5 步：生成最终综合报告（由第三方模型完成）

**请勿自行编写综合报告。**

**填写 `prompts/final-synthesis.md` 文件中的占位符：**
- `[ROUND1_SUMMARIES]`：所有代理的总结内容：`[角色] 的总结：[模型名称]`
- `[ROUND2_SUMMARIES]`：各代理对其他代理观点的批评内容及原因
- `[CONSENSUS_SCORES]`：完整的分数矩阵及计算出的百分比
- `[DISCORD_THREAD_ID]`：第一步中保存的线程 ID（综合报告将由该线程发布）

**使用第一步中保存的 `THREAD_ID` 将结果发布到 Discord 上**。所有轮次的讨论结果和最终的综合报告都会发布到同一个线程中。

---

## 第 6 步：保存结果**

将结果保存到 `{workspace}/memory/roundtables/YYYY-MM-DD-[topic-slug].json` 文件中：
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
  "elapsed_time_sec": 0,
  "synthesis": "[final synthesis text]"
}
```

同时，在 `{workspace}/memory/roundtables/scorecard.jsonl` 文件中添加一条 JSONL 格式的记录，内容如下：
`ts, topic, mode, workflow_type, elapsed_time_sec, consensus_pct, validated, panel_degraded`。

---

## 特殊情况处理

| 情况 | 应采取的措施 |
|-----------|--------|
| 网络搜索失败 | 在所有提示中显示 “没有实时数据可用” 的提示信息 |
| 使用了 `--no-search` 标志 | 完全跳过第 0 步的网络搜索 |
| 元面板的所有组件都失败 | 使用默认的团队模式，并在日志中记录警告信息 |
| 使用了 `--quick` 标志 | 跳过元面板和第二轮讨论，始终使用并行辩论模式。如果检测到需要使用多个模型，则使用默认的团队模式（3 个模型），并在第一轮结束后生成综合报告。 |
| 指定了特定的团队模型 | 跳过元面板，使用指定的模型；默认使用并行辩论模式 |
- 如果替代模型属于同一模型家族 | 在日志中记录团队功能降级的情况 |
- 如果所有模型和替代模型都失败 | 跳过相关代理的处理，但在日志中记录错误信息 |
- 未配置 Blockrun 服务 | 警告用户：“Blockrun 服务不可用。将使用默认的团队模式。完整团队模式需要通过 localhost:8402 启动 Blockrun 服务。” |
- 任何一轮中代理超时 | **继续执行**：将超时的代理视为未参与讨论，并在日志中标记为 “Timeout”，然后继续使用剩余的代理进行讨论 |
- 如果某个代理在讨论过程中失败 | 使用该代理在第一轮中的总结结果作为最终答案，但不将其分数计入共识计算 |
- 综合报告生成失败 | 由协调器负责生成综合报告，并在日志中说明：“综合报告由协调器生成（可能存在偏见）” |
- 第二阶段的代理失败 | 在日志中记录失败情况，并仅使用第一阶段的成果进行综合 |
- 如果没有代理响应 | 报告失败情况，并建议重新尝试 |
- 只有一个代理响应 | 跳过第二轮讨论，仅使用第一阶段的成果进行综合，并将共识结果标记为 “N/A” |
- 使用了 `--context-from SLUG` 标志 | 从 `{workspace}/memory/roundtables/[slug].json` 文件中加载相关数据，提取综合报告内容，并将其作为背景信息添加到 `CURRENT_CONTEXT` 中。如果文件不存在，则继续讨论，但不使用之前的背景信息。 |

### 占位符使用规则

在填写提示模板时，请遵循以下规则：
- 如果某个占位符缺失或无法获取数据，**请采取相应的处理措施**：
  | `[CURRENT_CONTEXT]` | 网络搜索失败 | 在提示中显示 “没有实时数据可用”。 |
  | `[SELF_DIGEST]` | 有代理在第一轮中超时 | 在第二轮中忽略该代理的贡献 |
  | `[PEER_digestS]` | 所有代理都失败 | 直接进入综合报告阶段 |
  | `[ROUND1_SUMMARIES]` | 第一轮没有结果 | 报告错误：“没有代理响应” |
  | `[ROUND2_SUMMARIES]` | 使用了快速模式或只进行了一轮讨论 | 在提示中显示 “没有进行交叉批评” |
  | `[CONSENSUS_SCORES]` | 无法提取分数 | 在提示中显示 “无法获取分数” |
  | `[SYNTHESIS_DRAFT]` | 综合报告生成失败 | 跳过第三轮讨论 |

**注意：** 请确保所有占位符都被正确填充。未填充的占位符会导致模型无法正常工作，从而产生错误的输出结果。

### 分数解析（第二轮讨论）
代理会以自由文本的形式提交分数。请使用以下规则提取分数：
1. 查找 `SCORES:` 标签；
2. 匹配格式：“- [角色]: X/5” — 提取整数 X（1–5）；
3. 如果找不到明确的整数，尝试提取与角色名称最接近的数字；
4. 如果仍然无法确定分数，則默认赋值为 3，并在日志中标记为 “[SCORE INFERRED]”。

---

## 快速参考：元面板失败时的默认处理方案（备用方案）

```json
debate:  [opus-4.6, gpt-5.3-codex, gemini-3.1-pro, grok-4] → Advocate / Devil's Advocate / Analyst / Contrarian
build:   [opus-4.6, gemini-3.1-pro, grok-4, gpt-5.3-codex] → Architect / Reviewer / Engineer / Implementer
redteam: [opus-4.6, gemini-3.1-pro, grok-4, gpt-5.3-codex] → Defender / Analyst / Attacker / Red Teamer
vote:    [opus-4.6, gemini-3.1-pro, grok-4, gpt-5.3-codex]  → 4-way vote panel
(all via blockrun/ prefix — see panels.json for exact model IDs and fallbacks)
```