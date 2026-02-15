---
name: save-usage
description: >
  **自动检测 OpenAI oAuth 模型（gpt-5.1-codex-mini 和 gpt-5.3-codex）的任务复杂性**  
  - 仅将安全或影响较小的任务路由到 gpt-5.1-codex-mini；  
  - 对于需要执行、存在不确定性或影响较大的任务，使用 gpt-5.3-codex。  
  **规则：**  
  1. 首先对任务进行分类。  
  2. 默认模型为 gpt-5.3-codex。  
  3. **仅** 在安全性评估、摘要生成、数据提取、格式转换、去重、提示草稿生成以及非执行性问答等场景下使用 gpt-5.1-codex-mini。  
  4. **严禁** 在涉及安全、身份验证、敏感信息处理、架构设计、系统迁移、旧系统重构、集成协议制定、模式映射、顺序控制、幂等性验证、代码修改、工具运行，或需要做出难以撤销的决策时使用 gpt-5.1-codex-mini。  
  **理由：**  
  - 对于 gpt-5.1-codex-mini，初始设置为其“低”复杂度级别；  
  - 对于 gpt-5.3-codex，默认复杂度为“低”或“中等”；  
  - 在满足以下条件时，应立即将其复杂度提升至“高”或“极高”：  
    - 操作难以撤销；  
    - 影响两个以上领域（基础设施、数据、安全、运营或成本）；  
    - 存在潜在的严重故障模式；  
    - 需要处理复杂的依赖关系链。  
  **特殊情况：**  
  - 如果任务结果将被实际执行（如工具或代码的生成），或经过一次处理后仍存在歧义，或任务要求具有多重约束或结构化输出，必须立即切换到 gpt-5.3-codex。
  Auto-detect task complexity for OpenAI oAuth models (gpt-5.1-codex-mini + gpt-5.3-codex). Route only
  safe/negligible tasks to gpt-5.1-codex-mini. Use gpt-5.3-codex for anything executed, uncertain, or
  high-impact. RULES: Classify first. Default model: gpt-5.3-codex. Use gpt-5.1-codex-mini ONLY for safe
  triage/summarize/extract/reformat/dedupe/prompt-drafts/non-executable Q&A. NEVER use mini for security,
  auth, secrets, architecture, migrations, brownfield refactors, integration contracts, schema mapping,
  ordering/idempotency/retries, code changes, tool runs, or decisions that are hard to reverse. Reasoning:
  start LOW for mini. For 5.3-codex use LOW/MEDIUM by default; escalate to HIGH/EXTRA HIGH when 2+ are true:
  hard to reverse, affects 2+ domains (infra/data/security/ops/cost), subtle/expensive failure modes, long
  dependency-chain reasoning. ESCALATE immediately to gpt-5.3-codex if any: output will be executed (tools/code),
  ambiguity remains after 1 pass, contradictions found, or requirements are multi-constraint/structured output.
---
# 使用说明

仅在对任务安全性或影响可忽略的情况下，才使用 **gpt-5.1-codex-mini**。当任务确实需要更高性能的模型时，请使用 **gpt-5.3-codex**。除非绝对必要，否则避免使用外部 API 密钥。

## 关键原则：**先分类，再行动**

在生成任何响应之前，你必须：

1. 检查：当前任务是否符合以下任何升级触发条件？
2. 如果符合 → 立即调用 `sessionsspawn()`。切勿尝试自行回答。
3. 如果不符合 → 直接使用当前模型进行回答。

如有疑问，请立即升级处理。错误的处理方式可能造成的损失较小，但错误的 “mini” 模型回答可能会浪费时间或导致问题。

## 经验法则

> 如果有任何操作需要执行，或者结果至关重要，请立即升级处理。

## 何时需要升级 → 必须调用 `sessionsspawn`

如果任务符合以下任何条件，请立即升级处理，而不要自行回答：

```
sessions_spawn(
	message: "<the full task description>",
	model: "gpt-5.3-codex",
	label: "<short task label>"
)
```


### 升级触发条件（始终适用）

- **执行的操作** — 任何工具的运行、代码更改、补丁应用、Shell 命令、基础设施操作
- **安全/认证/密钥** — 威胁建模、权限管理、令牌处理、访问控制
- **架构与迁移** — 大规模系统重构、现有系统的改造
- **集成/合同相关的工作** — 数据模型映射、任务顺序安排、操作的幂等性处理、重试机制、数据一致性
- **存在不确定性** — 经过一次处理后仍存在模糊不清的情况、矛盾之处、缺失的约束条件
- **高影响力决策** — 难以撤销的决策、代价高昂或影响广泛的故障模式、涉及多个领域
- **复杂的推理过程** — 长链条的依赖关系、多步骤的分析、非显而易见的权衡
- **结构化输出物** — 表格、大纲、报告/提案、长篇写作内容、技术规范

### 在 gpt-5.3-codex 中的升级判断标准

- 默认级别：**低/中**
- 如果同时满足以下两个或更多条件，升级至 **高/极高**：
  - 决策难以撤销
  - 影响两个或更多领域（基础设施/数据/安全/运营/成本）
  - 故障模式复杂或代价高昂
  - 需要复杂的依赖关系分析

## 在 gpt-5.1-codex-mini 上绝对禁止以下操作

- 绝对禁止输出任何将要执行的操作（工具、代码、命令）——必须立即升级
- 绝对禁止处理与安全/认证/密钥相关的问题——必须立即升级
- 绝对禁止处理架构相关的问题或系统重构——必须立即升级
- 绝对禁止处理集成合同或数据模型相关的工作——必须立即升级
- 绝对禁止生成结构化输出物（表格/大纲/报告/技术规范）——必须立即升级
- 绝对禁止做出高影响力决策或进行复杂的推理——必须立即升级

如果你发现自己需要对内容的正确性或安全性负责，请立即停止并调用 `sessionsspawn`。

## 何时继续使用 gpt-5.1-codex-mini

仅在对任务安全性或影响可忽略且无需执行任何操作的情况下使用：

- **任务分类/优先级判断** — 对任务进行分类，选择合适的代理模型或推理方式
- **信息汇总与提取** — 提取关键信息、行动事项、字段内容
- **格式转换** — 将内容转换为 Markdown、YAML 或 JSON 格式（无需执行任何操作）
- **编写提示语句** — 为更强大的模型编写提示语句
- **简单问答** — 提供定义、简短解释、简单翻译、单位转换服务
- **日常聊天** — 进行简单的问候或回复

请保持简短的回复。

## 更进一步的优化：降级处理

如果某个任务最初被升级到了 gpt-5.3-codex，但后续的处理内容明显安全且无需执行任何操作，应立即切换回 gpt-5.1-codex-mini。直接返回结果即可，除非用户特别询问模型切换的情况。

## 为什么 `description` 字段如此冗长

Clawdbot 技能系统仅将 `description` 字段插入到系统提示中，而 SKILL.md 文件的正文内容并不会自动被包含进来。模型可以选择性地读取整个文件，但这并非强制要求。由于这是一种 **行为相关技能**（用于指导模型的消息处理方式），而非工具技能（用于教授特定的 CLI 命令），因此核心的路由逻辑必须记录在 `description` 字段中，以确保模型始终能够看到这些信息。

上述内容提供了详细的触发条件列表、推理级别以及使用建议，模型在读取文件时可以参考这些信息。

**简而言之：** `description` 字段是模型始终会看到的内容；`body` 字段则包含详细的参考文档。