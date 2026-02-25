---
name: correction-memory
description: 该技能能够使代理的更正行为具有持久性，并可被重复使用。当您覆盖、拒绝或更正代理的输出时，该技能会记录下这些更正内容，并自动将其应用到未来生成的相同类型的代理实例中。这有效解决了“代理在不同会话中持续犯同样错误”的问题。该技能会在代理上下文加载器（agent-context-loader）中安装一个用于跟踪更正操作的库（correction-tracker）以及相应的注入钩子（injection hook）。它可以独立运行，也可以与意图工程（intent-engineering）技能配合使用。
---
# 修正记忆功能

## 问题所在

当你修正某个代理的行为后，这些修正内容会在会话结束后被清除。下次再次生成相同类型的代理时，它还是会犯同样的错误。系统没有保留你之前教给它的知识。

## 该技能的作用

- **`lib/correction-tracker.js`**：将每种代理类型的修正记录保存到 `memory/corrections/[AgentType].jsonl` 文件中。
- **集成到 `agent-context-loader.js` 中**：在生成代理时自动添加修正提示（前提是已安装了 `intent-engineering` 技能）。

## 安装步骤

### 第一步：安装 correction-tracker

```bash
cp references/correction-tracker-template.js $OPENCLAW_WORKSPACE/lib/correction-tracker.js
```

验证其是否正常运行：

```bash
node $OPENCLAW_WORKSPACE/lib/correction-tracker.js
```

### 第二步：集成 agent-context-loader（如果使用了 intent-engineering）

如果已经安装了 `lib/agent-context-loader.js`（来自 `intent-engineering` 技能），修正内容的注入是自动完成的，无需额外配置。该加载器会在启动时检查是否存在 `correction-tracker.js` 并将其加载。

如果你没有使用 `intent-engineering`，则需要手动将以下代码添加到代理生成逻辑中：

```javascript
const { buildCorrectionPreamble } = require('./lib/correction-tracker');

const agentType   = 'CoderAgent'; // or whatever agent you're spawning
const corrections = buildCorrectionPreamble(agentType, workspaceRoot);
const fullTask    = corrections ? corrections + '\n\n---\n\n' + originalTask : originalTask;
```

## 记录修正内容

### 程序化方式

```javascript
const { logCorrection } = require('./lib/correction-tracker');

logCorrection(
  'CoderAgent',                                    // agent type
  'Used ESM import instead of require()',          // what was wrong
  'Always use require() for Node.js stdlib modules', // correct behavior
  workspaceRoot,
  { session_channel: 'discord' }                  // optional metadata
);
```

### 通过主代理（自然语言指令）

只需向主代理发送如下指令：

> “注意：[AgentType] 的错误行为是 [正确的行为]”

主代理会自动记录这些修正内容。

## 修正内容的重放机制

每当生成新的子代理时，`agent-context-loader` 会从任务描述中检测代理类型，并自动添加相应的修正提示：

```
## Corrections from Previous Sessions

The following corrections were logged for CoderAgent. Apply these behaviors:

1. **[2026-03-01] Issue:** Used ESM import instead of require()
   **Correction:** Always use require() for Node.js stdlib modules
```

系统只会保留 **过去 30 天** 内的修正内容。过期的修正记录会自动被清除，以避免规则堆积。

## 查看修正记录

```bash
# All corrections for an agent type
cat $OPENCLAW_WORKSPACE/memory/corrections/CoderAgent.jsonl | jq .

# List all agent types with corrections
ls $OPENCLAW_WORKSPACE/memory/corrections/

# Count corrections per agent
for f in $OPENCLAW_WORKSPACE/memory/corrections/*.jsonl; do
  echo "$(basename $f .jsonl): $(wc -l < $f) corrections"
done
```

## 代理类型检测

加载器会自动从任务描述中识别代理类型。默认的代理类型对应关系如下：

| 任务关键词 | 代理类型 |
|---|---|
| `code`, `coder`, `impl`, `debug` | `CoderAgent` |
| `writ`, `author`, `novel`, `chapter` | `AuthorAgent` |
| `world`, `build` | `WorldbuilderAgent` |
| 其他所有关键词 | `general` |

如需添加自定义代理类型，请编辑 `agent-context-loader.js` 中的 `detectAgentType()` 函数。

## 参考资料

- `references/correction-tracker-template.js`：`correction-tracker.js` 的完整实现代码。