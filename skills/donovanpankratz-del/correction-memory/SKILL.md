---
name: correction-memory
version: 1.1.0
description: 该技能能够使代理的修正行为具有持久性，并可被重复使用。当您覆盖、拒绝或修正代理的输出时，该技能会记录下这些修正内容，并自动将其应用到同一类型代理的后续实例中。这解决了“代理在不同会话中持续犯相同错误”的问题。该技能会在代理上下文加载器（agent-context-loader）中安装修正跟踪库（correction-tracker lib）及相应的注入钩子（injection hook）。它可以独立运行，也可以与意图工程（intent-engineering）技能配合使用。
---
# 修正记忆功能

## 问题所在

当你修正某个代理的行为后，这些修正内容在会话结束后就会消失。下次再次生成相同类型的代理时，它仍然会犯同样的错误。系统没有保留你之前教给它的任何修正信息。

## 该功能的作用

- **`lib/correction-tracker.js`**：将每种代理类型的修正记录保存到 `memory/corrections/[AgentType].jsonl` 文件中。
- **集成到 `agent-context-loader.js` 中**：在生成代理时自动添加修正信息（前提是已安装了 `intent-engineering` 模块）。

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

如果已经安装了 `lib/agent-context-loader.js`（该模块属于 `intent-engineering` 模块），则修正信息的注入是自动完成的，无需额外配置。`agent-context-loader` 在启动时会检查是否存在 `correction-tracker.js` 文件，并在找到后将其加载。

如果你没有使用 `intent-engineering`，则需要手动将以下代码添加到代理生成逻辑中：

```javascript
const { buildCorrectionPreamble } = require('./lib/correction-tracker');

const agentType   = 'CoderAgent'; // or whatever agent you're spawning
const corrections = buildCorrectionPreamble(agentType, workspaceRoot);
const fullTask    = corrections ? corrections + '\n\n---\n\n' + originalTask : originalTask;
```

## 记录修正信息

### 通过编程方式

你可以直接告诉主代理：

> “注意：[AgentType] 的错误行为是 [正确的行为]”

主代理会自动记录这些修正信息。

## 修正信息的重放机制

每当生成新的子代理时，`agent-context-loader` 会根据任务描述自动识别代理类型，并在代理的行为中添加相应的修正信息。

**只有过去 30 天内的修正信息才会被保存**；过期的修正信息会自动被删除，以避免规则积累过多。

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

## 代理类型识别

`agent-context-loader` 会自动从任务描述中识别代理类型。默认的代理类型对应关系如下：

| 任务关键词 | 代理类型 |
|---|---|
| `code`, `coder`, `impl`, `debug` | `CoderAgent` |
| `writ`, `author`, `novel`, `chapter` | `AuthorAgent` |
| `world`, `build` | `WorldbuilderAgent` |
| 其他所有关键词 | `general` |

如需添加自定义代理类型，请编辑 `agent-context-loader.js` 中的 `detectAgentType()` 函数。

## 参考资料

- `references/correction-tracker-template.js`：`correction-tracker.js` 的完整实现代码。