---
name: roundtable
description: "自适应多模型AI圆桌讨论：最多可支持4个AI模型参与讨论（可配置），分为两轮辩论，每轮辩论结束后会进行相互评价和正式的共识评分。需要配置相应的Anthropic提供商（推荐使用Claude Opus）；也可通过Blockrun代理额外添加GPT-5.3 Codex（OpenAI）、Grok 4和Gemini 3.1 Pro等模型。若未配置其他提供商，则仅支持使用Claude模型。讨论结果会保存到本地文件系统中。所有参与模型均为一次性使用的代理（one-shot agents），每轮辩论结束后会自动终止运行。"
metadata:
  clawdis:
    emoji: "🎯"
    requires:
      env:
        - ANTHROPIC_API_KEY
      config:
        - providers.anthropic
        - providers.openai-codex
        - providers.blockrun
    config:
      requiredEnv:
        - name: ANTHROPIC_API_KEY
          description: "Required. Anthropic API key OR configure OAuth in openclaw.json (providers.anthropic). Provides Claude Opus/Sonnet as panel model. Skill cannot run without this."
          required: true
        - name: OPENAI_API_KEY
          description: "Optional. OpenAI API key OR configure OAuth in openclaw.json (providers.openai-codex). Adds GPT-5.3 Codex as a panelist. If absent, slot falls back to Claude Sonnet."
          required: false
        - name: BLOCKRUN_PROXY_URL
          description: "Optional. Set to http://localhost:8402 if Blockrun is installed. Adds Grok 4 and Gemini 3.1 Pro via x402 micropayments on Base (~$0.13/run). Install via: openclaw plugins install @blockrun/clawrouter. If absent, those slots fall back to Claude."
          required: false
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
# 圆桌讨论 v2 — 自适应多模型协调器

**触发方式：** 通过代理监控的任何频道执行 `roundtable [--mode] [prompt]` 命令。
**输出结果：** 会发布到您配置的输出频道（在 OpenClaw 配置中设置 `ROUNDTABLE_OUTPUT_CHANNEL`，否则结果将返回到触发该命令的频道）。
**代理：** 所生成的代理均为一次性使用（`mode="run"`）—— 完成讨论后自动终止，不会持续运行在后台。

**协调器仅担任协调者角色。** 除非在 `panels.json` 中另有指定，否则使用默认模型。协调器不会参与讨论或表达观点。

**核心原理：** Meta-Panel（4 个高级模型）会为任务设计最佳的工作流程（并行辩论、顺序处理或混合模式），然后由相应的代理执行该流程。

## 配置

在使用前，请在 `panels.json` 中设置输出频道（或使用触发命令的频道）：
```json
{
  "output": {
    "channel": "discord",
    "target": "YOUR_CHANNEL_ID_HERE"
  }
}
```

**（如果使用 Discord 线程：** 可选，为每个圆桌讨论创建一个线程以保持讨论的条理）：
```json
{
  "output": {
    "channel": "discord",
    "target": "YOUR_CHANNEL_ID_HERE",
    "useThreads": true
  }
}
```
**如果不进行此配置，结果将直接发布在命令执行的频道中。**

## 成本透明化

| 组件 | 每次完整运行的成本 |
|-----------|-----------------|
| Claude Opus (OAuth) | 免费 |
| GPT-5.3 Codex (OAuth) | 免费 |
| Gemini 3.1 Pro (Blockrun) | 约 0.05 美元 |
| Grok 4 (Blockrun) | 约 0.08 美元 |
| **完整流程（使用所有模型）** | 约 0.13–0.50 美元 |
| **简化模式（仅使用 Claude）** | 免费 |

**使用 `--quick` 标志可降低成本（仅执行 1 轮讨论）。**

---

## 设置

**最低配置（简化模式，免费）：**
1. 在 `openclaw.json` 中配置 `anthropic` 提供者（使用 OAuth 或 API 密钥）。
2. （可选）为 GPT-5.3 Codex 添加 `openai-codex`。
3. 完成配置后，Grok/Gemini 会自动使用 Claude Sonnet 模型。

**使用所有模型（包括 Grok 4 和 Gemini 3.1 Pro）：**
1. 安装 Blockrun 插件：`openclaw plugins install @blockrun/clawrouter`，然后重启 `openclaw gateway`。
2. 用 USDC 为 Blockrun 钱包充值（约 5–10 美元）。充值地址会在安装过程中显示。
3. 完整流程的成本约为每次运行 0.13–0.50 美元；Claude 和 GPT 模型仍可通过 OAuth 免费使用。

讨论结果会保存在 `{workspace}/memory/roundtables/YYYY-MM-DD-slug.json` 文件中（文件会自动生成）。

---

## 触发模式

### 可选：自动将讨论结果发布到指定频道
您可以在 `AGENTS.md` 中配置一个专门用于圆桌讨论的 Discord 频道：
```
Any message in channel [YOUR_CHANNEL_ID] → treat as a roundtable topic automatically.
No prefix needed. Message → auto-detect mode → create thread → spawn orchestrator.
```
**这完全是可选的；** 显式使用 `roundtable` 命令时，无论从哪个频道发起命令都能触发讨论。

### 显式触发方式（适用于任何频道）：

- `roundtable [prompt]` — 启用默认流程
- `roundtable --debate [prompt]` — 强制使用并行辩论模式
- `roundtable --build [prompt]` — 强制使用构建/编码模式
- `roundtable --redteam [prompt]` — 强制使用对抗性讨论模式
- `roundtable --vote [prompt]` — 强制使用决策模式
- `roundtable --quick [prompt]` — 跳过 Meta-Panel，使用默认流程，仅执行 1 轮讨论
- `roundtable --panel model1,model2,model3 [prompt]` — 手动指定使用特定模型，跳过 Meta-Panel
- `roundtable --validate [prompt]` — 在第三轮中添加对讨论结果的验证
- `roundtable --no-search [prompt]` — 跳过网络搜索（仅适用于纯理论或抽象主题）

---

## 第一步：创建讨论线程（首要操作）

在开始之前，请在配置好的频道中创建一个讨论线程，并保存该线程的 ID。
```
message(
  action = 'thread-create',
  channel = '[your configured channel]',
  channelId = '[CHANNEL_ID from user config]',
  threadName = '🎯 [topic — max 8 words] [[MODE]]',
  message = '**Panel:** [model list]\n**Mode:** [mode] | **Rounds:** [N]\n⏳ Analysis in progress...'
)
```

将保存的线程 ID 存储为 `THREAD_ID`。
**后续的所有 `message()` 调用都应使用 `target = THREAD_ID`，而不是频道 ID。**

如果创建线程失败或频道未配置，则直接在当前频道发布讨论内容。

---

## 第零步：进行网络搜索（必选步骤）

在开始讨论之前，先对该主题进行网络搜索，以便所有代理都能获取最新的背景信息。
```
web_search(query = prompt, count = 5)
```

**超时处理：** 如果网络搜索在 10 秒内没有返回结果或出现错误，请不要停止讨论，直接继续执行，并在输出中显示 “当前没有实时数据（搜索失败或超时）”。此时讨论将仅基于模型提供的信息进行。

**缓存机制：** 如果在同一会话中再次搜索相同主题，直接使用上一次的 `CURRENT_CONTEXT` 内容，无需重新搜索。

将搜索结果总结为 `CURRENT_CONTEXT` 块（最多 250 个单词）：
- 关键事实、最新进展、相关数据点
- 搜索日期
- 如果没有找到有用信息：显示 “未找到相关实时数据”，并继续讨论

`CURRENT_CONTEXT` 块的内容会用于：
1. Meta-Panel 的提示信息（以便他们根据最新信息设计讨论流程）
2. 所有参与讨论的代理的初始提示信息（确保所有参与者基于相同的信息进行讨论）

---

## 第零步（可选）：Meta-Panel — 设计讨论流程

**在以下情况下可跳过此步骤：** 使用了 `--panel` 或 `--quick` 标志。

### 并行生成 4 个高级分析模型

读取 `panels.json` 文件中的 `meta.models` 部分，然后为每个模型执行以下操作：
```
sessions_spawn(
  task = filled prompts/meta-panel.md,
  model = model_id,
  mode = "run",
  label = "rt-meta-[A/B/C/D]",
  runTimeoutSeconds = 90
)
```

### 0b. 根据 4 个模型的建议设计讨论流程

收集所有模型的建议后，协调器会生成最终的工作流程：
1. **流程类型**：根据 4 个模型的建议进行多数投票
   - 如果投票结果相同，选择 **混合模式**（更具灵活性）
2. **各阶段的模型分配**：统计每个阶段最受欢迎的模型
   - 如果某个模型不在 `agentsdefaults.models` 的允许列表中，则跳过该模型，选择下一个模型
   - 如果某个模型是协调器专用的模型，则不将其纳入流程（协调器专用模型，不能作为讨论参与者使用）
3. **讨论轮次**：根据模型的推荐结果进行排序（出现平局时向上取整）—— 最多允许使用 3 个模型
4. **最终使用的合成模型**：在主流程中未出现的最受欢迎的高级模型
5. **记录决策结果**（包含在输出标题中）：
   > “Meta-Panel 设计的流程：[类型]。阶段：[数量]。使用的模型：[模型列表]。”

### 0c. 各流程类型的说明

- **parallel_debate**（并行辩论）：所有代理在第一阶段独立工作，使用相同的讨论主题
  - 第二阶段进行互相评价
  - 适用于辩论、意见交流、风险分析、决策制定等场景
- **sequential**（顺序处理）：各阶段之间有明确的输出顺序
  - 第一阶段的代理生成输出（草稿、代码、研究结果）
  - 第二阶段的代理接收第一阶段的输出并进行审查、改进
  - 适用于编码、研究、创意创作等需要逐步推进的任务
- **hybrid**（混合模式）：第一阶段各代理并行工作；第二阶段由 1–2 个高级模型整合所有第一阶段的输出
  - 适用于需要综合分析的复杂任务

### 0d. 备用模型规则

如果某个代理出现故障且无法使用其他模型，则记录以下信息：
`⚠️ 讨论流程降级 — [角色] 被 [备用模型] 替代（属于同一模型系列）`

请在最终输出的 META 部分明确显示这一情况，并提供相应的处理建议：
- 如果是因为 Blockrun 服务不可用导致流程降级：**操作建议：在 localhost:8402 启动 Blockrun 服务以使用完整流程；或使用 `--panel budget` 选项使用 2 个模型**
- 如果是因为模型不在允许列表中导致流程降级：**操作建议：将 [模型名称] 添加到 `agentsdefaults.models` 文件中**
- 如果是因为 API 错误导致流程降级：**操作建议：检查提供者的 API 密钥或配额，然后重试**

---

## 第一步：确定讨论模式（如果没有指定模式）

| 模式 | 关键词 |
|------|----------|
| **debate** | 优点/缺点、权衡、是否可行、伦理问题、比较、观点、最佳方案 |
| **build** | 实现、编码、架构设计、开发、创建 |
| **redteam** | 攻击、漏洞、失败风险、威胁、利用方法 |
| **vote** | 选择方案、做出决策、确定最佳选项 |
| **default** | 其他所有情况 |

---

## 第二步：执行讨论流程

### parallel_debate（标准模式）

**第一轮：** 并行生成所有代理，并让它们一次性完成讨论。
```
sessions_spawn(
  task = filled prompts/round1.md,
  model = model_id,
  mode = "run",
  label = "rt-r1-[role]",
  runTimeoutSeconds = 120
)
```

- 每个代理生成完整的回答及自己的总结（`SELF-DIGEST` 部分）
- 收集所有代理的回答并生成总结
- 所有第一轮的代理完成讨论后自动终止

**第二轮（如果有多于 2 轮讨论）：** 生成新的代理，这些代理的提示中会包含第一轮的讨论内容。
- 为每个代理重新生成提示（`prompts/round2-cross-critique.md`），并包含第一轮的讨论内容
- `[SELF_DIGEST]` 表示该代理在第一轮中的总结
- `[PEER_digestS]` 表示其他代理的总结（标注了对应的角色）
- 从每个代理的回答中提取同意度分数
- 所有第二轮的代理完成讨论后自动终止

**第三轮（如果使用了 `--validate` 标志）：** 见第 4 步。

### sequential（顺序处理模式）

**第一阶段：** 并行生成所有代理，并让它们一次性完成讨论。
- 使用标准提示 `prompts/round1.md`。
- 收集所有第一阶段的输出结果
- 所有第一阶段的代理完成讨论后自动终止

**第二阶段：** 生成新的代理，提示中包含第一阶段的讨论内容。
- 提示格式：`prompts/round1.md` + 第一阶段的输出结果
- 标签：`[角色] 的第一阶段输出：[所有输出结果]`
- 第二阶段的代理会审查并改进第一阶段的成果
- 第二阶段的代理也会生成自己的总结

### hybrid（混合模式）

**第一阶段：** 并行生成代理（`mode="run"`），每个代理负责不同的子任务。
- 自定义第一阶段的提示，明确每个代理的具体任务：
  > “您在这个阶段的具体任务是：[任务描述]”
- 代理完成任务后生成总结并终止

**第二阶段：** 生成 1–2 个高级代理，他们的提示中包含所有第一阶段的输出结果。
- 提示格式：`prompts/round1.md` + “您正在整合多个代理的成果。他们的输出结果如下：[所有第一阶段的输出结果]`
- 第二阶段生成最终的综合结果并终止

---

## 第三步：计算共识分数

在第二轮（parallel_debate）或第二阶段（sequential/hybrid）结束后：
从每个代理的第二轮回答中提取同意度分数。
生成分数矩阵：`{ agent_role: { peer_role: score_1_to_5 } }`
共识百分比 = （所有分数之和 / （代理数量 × 5）× 100`
如果第二轮没有分数（使用快速模式或顺序处理模式），则忽略共识百分比，标记为 “N/A”

> **关于第三轮的说明：** 第三轮的目的是验证综合结果的准确性，而非代理之间的共识程度。第三轮的评分标准与共识百分比是分开的。第三轮的评分仅用于判断综合结果的准确性，不会与共识百分比混淆。共识百分比仅来自第二轮的分数；第三轮的结果会在 META 部分单独显示为 “Validated: yes/no/partial”。

---

## 第四步：第三轮 — 验证（仅在使用 `--validate` 标志时执行）

**何时建议使用第三轮验证：**
- 共识百分比低于 40%（说明综合结果可能存在偏差）
- 使用对抗性讨论模式（需要确保综合结果的准确性）
- 使用 3 个或更多第二阶段模型的情况（复杂整合过程容易产生误导）
- 用户明确要求 “高精度结果” 或 “做出最终决策”

**何时不使用第三轮验证：** 使用快速模式、讨论主题具有主观性，或者时间比精度更重要的情况。

**首先生成初步的综合结果（见第五步），但不要立即发布。**

然后生成验证用的代理：
```
sessions_spawn(
  task = filled prompts/round3-validation.md,
  model = original agent model,
  label = "rt-r3-validate-[role]",
  runTimeoutSeconds = 60
)
```

根据评分结果进行相应处理：
- 如果有 2 个或更多代理的评分不准确：重新生成综合结果
- 如果有 1 个代理的评分不准确：在 META 部分标注：“⚠️ [角色] 的回答存在错误：[错误原因总结]”
- 如果所有代理的评分都准确：在 META 部分标记为 “Validated: yes” 或 “Validated: partial”

---

## 第五步：生成最终综合结果（由第三方模型完成）

**切勿自行编写综合结果。**

```
sessions_spawn(
  task = filled prompts/final-synthesis.md,
  model = [synthesis model from meta-panel recommendation, or anthropic/claude-opus-4-6 as default],
  label = "rt-synthesis",
  mode = "run",
  runTimeoutSeconds = 180
)
```

填写 `prompts/final-synthesis.md` 文件中的占位符：
- `[ROUND1_SUMMARIES]`：所有代理的总结：“**[角色]** 的总结：**[模型名称]**”
- `[ROUND2_SUMMARIES]`：批评内容：“**[角色]** 对 **[其他角色]** 的观点的批评理由”
- `[CONSENSUS_SCORES]`：完整的分数矩阵
- `[DISCORD_THREAD_ID]`：第一步中保存的线程 ID（综合结果将由该线程发布）

**使用第一步中保存的 `THREAD_ID` 将结果发布到 Discord**。所有讨论结果和最终的综合结果都会发布到同一个线程中。

---

## 第六步：保存结果

将结果保存到 `~/clawd/memory/roundtables/YYYY-MM-DD-[主题名称].json` 文件中：
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

## 异常情况处理

| 情况 | 处理方式 |
|-----------|--------|
| 网络搜索失败 | 在所有提示中显示 “当前没有实时数据” |
| 使用了 `--no-search` 标志 | 完全跳过网络搜索步骤 |
| Meta-Panel 所有模型都失败 | 使用默认的讨论流程，并在日志中记录警告 |
| 使用了 `--quick` 标志 | 跳过 Meta-Panel 和第二轮讨论，始终使用 `parallel_debate` 模式。如果检测到需要使用 3 个模型，则使用默认的讨论流程，并在第一轮结束后生成综合结果 |
| 指定了特定的模型但无法使用 | 跳过 Meta-Panel，使用指定的模型；默认使用 `parallel_debate` 模式 |
- 备用模型也失败 | 在日志中记录 “流程降级” 并提供相应的处理建议 |
- 既没有可用模型也没有备用模型 | 警告用户：“Blockrun 服务不可用。使用默认的讨论流程。完整流程需要通过 localhost:8402 启动 Blockrun 服务。” |
- 代理在讨论过程中超时 | 将该代理视为未参与讨论，在日志中标记为 “Timeout”，并继续使用剩余的代理 |
- 代理在第二轮讨论中失败 | 使用该代理在第一轮中的总结作为最终结果，忽略其评分 |
- 综合结果生成失败 | 由协调器生成综合结果，并在日志中说明：“综合结果由协调器生成（可能存在偏见）” |
- 第二阶段的代理失败 | 在日志中记录这一情况，并使用第一阶段的总结作为最终结果 |
- 没有代理响应 | 报告失败情况，并建议重新尝试 |
- 只有一个代理响应 | 跳过第二轮讨论，仅使用第一阶段的总结作为最终结果 |
- 使用了 `--context-from SLUG` 标志 | 从 `~/clawd/memory/roundtables/[slug].json` 文件中加载相关数据，并将结果添加到 `CURRENT_CONTEXT` 中 |
| 占位符未填写**：** 在填写提示内容时，请确保填写所有占位符。未填写的占位符会导致模型无法正确工作，从而产生错误的结果 |

### 占位符使用规则

在填写提示内容时，请遵循以下规则：
| 占位符 | 如果未填写或填写错误 | 处理方式 |
|-------------|------------------|--------|
| `[CURRENT_CONTEXT]` | 网络搜索失败 | 插入提示：“当前没有实时数据” |
| `[SELF_DIGEST]` | 代理在第一轮中超时 | 跳过该代理在第二轮中的参与 |
| `[PEER_digestS]` | 所有代理都失败 | 跳过第二轮讨论，直接进入综合步骤 |
| `[ROUND1_SUMMARIES]` | 第一轮没有输出结果 | 报告错误：“没有代理响应” |
| `[ROUND2_SUMMARIES]` | 使用了快速模式或只进行了一轮讨论 | 插入提示：“未进行交叉评价（快速模式或只进行了一轮讨论）” |
| `[CONSENSUS_SCORES]` | 无法提取分数 | 插入提示：“无法获取分数” |
| `[SYNTHESIS_DRAFT]` | 综合结果生成失败 | 跳过第三轮讨论 |

**注意：** 确保提示中的所有占位符都被正确填写。未填写的占位符会导致模型无法正常工作，从而产生错误的结果。**

### 分数解析（第二轮讨论）

代理会以自由文本的形式提交分数。使用以下规则提取分数：
1. 查找 `SCORES:` 标签
2. 匹配格式：“`[角色]: X/5`”——提取整数 X（1–5）
3. 如果找不到明确的整数，尝试提取与角色名称最接近的数字
4. 如果仍然无法确定分数，则默认赋值为 3（表示“不确定”），并在日志中注明 “[SCORE INFERRED]”

---

## 快速参考：默认讨论流程（在 Meta-Panel 失败时使用）

```json
debate:  [opus-4.6, gpt-5.3-codex, gemini-3.1-pro, grok-4] → Advocate / Devil's Advocate / Analyst / Contrarian
build:   [opus-4.6, gemini-3.1-pro, grok-4, gpt-5.3-codex] → Architect / Reviewer / Engineer / Implementer
redteam: [opus-4.6, gemini-3.1-pro, grok-4, gpt-5.3-codex] → Defender / Analyst / Attacker / Red Teamer
vote:    [opus-4.6, gemini-3.1-pro, grok-4, gpt-5.3-codex]  → 4-way vote panel
(all via blockrun/ prefix — see panels.json for exact model IDs and fallbacks)
```