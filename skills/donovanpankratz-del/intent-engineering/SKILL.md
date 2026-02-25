---
name: intent-engineering
description: Adds a machine-readable intent layer to OpenClaw agents. Creates INTENT.md (optimization priorities, tradeoffs, delegation rules), wires it into subagent spawns via agent-context-loader, and ensures every subagent knows what you're optimizing for — not just what to do. Solves the "Klarna failure mode": AI optimizes measurable metrics instead of actual goals. Use when setting up a new OpenClaw workspace, when subagents keep making the wrong tradeoffs, or when you want explicit control over cost/quality/speed priorities.
---

# 意图工程（Intent Engineering）

## 问题

在没有意图层（intent layer）的情况下，代理会优化那些可衡量的指标（如快速响应、无错误），而不是真正重要的目标（即用户的实际优先级）。Klarna的失败案例就说明了这一点：虽然人工智能节省了6000万美元，但却破坏了客户的忠诚度，因为它优化的是问题解决的时间，而非与客户的关系。

## 该技能的作用

1. **`INTENT.md`**：位于工作区根目录下的YAML格式优先级配置文件。
2. **`lib/agent-context-loader.js`**：在每个子代理（subagent）启动时，会在任务描述前添加意图的摘要信息。
3. **路由集成**：在所有路由决策中都会考虑意图的传播规则。

## 安装步骤

### 第1步 — 创建 `INTENT.md`

将 `references/intent-template.md` 复制到工作区根目录，并将其命名为 `INTENT.md`，然后进行编辑：

```bash
cp $(dirname $0)/references/intent-template.md $OPENCLAW_WORKSPACE/INTENT.md
```

或者你可以手动创建它——具体格式请参考 `references/intent-template.md`。

### 第2步 — 安装 `agent-context-loader`

将相关实现代码复制到 `lib/` 目录中：

```bash
cp $(dirname $0)/references/agent-context-loader-template.js $OPENCLAW_WORKSPACE/lib/agent-context-loader.js
```

验证代码是否能够正常运行：

```bash
node $OPENCLAW_WORKSPACE/lib/agent-context-loader.js $OPENCLAW_WORKSPACE
```

### 第3步 — 将意图信息整合到任务描述中

在每个子代理启动时，将意图的上下文信息添加到任务描述中：

```javascript
const { prepareAgentContext } = require('./lib/agent-context-loader');

const { context } = prepareAgentContext(taskType, workspaceRoot);
const fullTask = context ? context + '\n\n---\n\n' + originalTask : originalTask;

// Use fullTask as your subagent task description
```

`taskType` 是一个字符串，用于描述任务类型（例如 `"code_review"`、`"research"`、`"writing"`）。`agent-context-loader` 会自动从 `INTENT.md` 和最近的内存中提取相关的上下文信息。

### 第4步 — 验证效果

启动一个测试子代理，执行一个通常会导致权衡（如成本与质量、速度与深度）的任务。确认子代理的输出能够反映 `INTENT.md` 中设定的优先级。

## `INTENT.md` 的结构

| 字段          | 作用                         |
|---------------|-----------------------------|
| `optimization_priority` | 任务的优先级顺序（从高到低）            |
| `tradeoffs`     | 当目标冲突时的处理规则                |
| `model_tier_intent` | 不同任务类型应使用哪种模型层级           |
| `delegation_intent` | 是否需要将任务委托给其他代理处理           |
| `quality_intent`    | 每个领域的质量标准                    |

完整的注释模板请参见 `references/intent-template.md`。

## 工作原理

`prepareAgentContext()` 函数会在每次调用时重新读取 `INTENT.md` 的内容，提取一个简洁的摘要（长度不超过200个字符），并将其添加到任务的描述中。如果 `INTENT.md` 不存在，系统会使用一个默认的默认值。该加载器在遇到问题时不会抛出异常，而是会默默地降级处理。

## 参考资料

- `references/intent-template.md`：包含所有字段的完整 `INTENT.md` 模板及注释。
- `references/agent-context-loader-template.js`：`agent-context-loader` 的完整实现代码。