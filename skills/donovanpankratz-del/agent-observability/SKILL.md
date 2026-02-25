---
name: agent-observability
description: Full observability stack for OpenClaw agents. Installs four tools: (1) weekly throughput dashboard (tasks/cost/quality), (2) decision audit log (why decisions were made), (3) failure trace capture (what went wrong when subagents fail), (4) drift-guard auto-scoring (weekly INTENT.md compliance check). Use when you want visibility into agent behavior, when debugging subagent failures, or when setting up production monitoring. Works standalone or alongside intent-engineering skill.
---

# 代理可观测性（Agent Observability）

## 安装的组件

| 文件名 | 功能 | 存放位置 |
|---|---|---|
| `throughput-dashboard.js` | 显示每周的工作效率指标 | `scripts/` |
| `decision-audit.js` | 以只读方式记录决策过程及理由 | `lib/` |
| `failure-tracer.js` | 当质量得分低于7时记录故障追踪信息 | `lib/` |
| `drift-guard-auto.js` | 每周检查INTENT.md文件的合规性 | `scripts/` |

## 安装步骤

### 第1步：复制文件

```bash
WORKSPACE="${OPENCLAW_WORKSPACE:-$(pwd)}"

cp references/throughput-dashboard.js  "$WORKSPACE/scripts/"
cp references/decision-audit.js        "$WORKSPACE/lib/"
cp references/failure-tracer.js        "$WORKSPACE/lib/"
cp references/drift-guard-auto.js      "$WORKSPACE/scripts/"
```

或者手动将这些文件从`references/`目录复制到目标位置。

### 第2步：将文件添加到心跳脚本或每周定时任务中

在您的心跳脚本或每周定时任务中添加以下代码：

```bash
node "$WORKSPACE/scripts/throughput-dashboard.js" "$WORKSPACE"
node "$WORKSPACE/scripts/drift-guard-auto.js" "$WORKSPACE"
```

### 第3步：将`decision-audit.js`与高风险决策关联起来

```javascript
const { logDecision } = require('./lib/decision-audit');

logDecision({
  task_type: 'code_generation',
  decision: 'spawn CoderAgent',
  reasoning_summary: 'Multi-file edit blocks chat >5s',
  session_channel: 'discord'  // optional
}, workspaceRoot);
```

### 第4步：将`failure-tracer.js`与质量验证流程集成（可选）

当对子代理的输出进行评分后，`failure-tracer.js`会自动触发：

```javascript
const { captureFailureTrace } = require('./lib/failure-tracer');

// Call after scoring any subagent output
if (qualityScore < 7) {
  captureFailureTrace('AgentLabel-task', qualityScore, agentOutput, workspaceRoot);
}
```

## 数据读取方式

| 文件路径 | 数据内容 |
|---|---|
| `memory/dashboards/YYYY-MM-DD.md` | 每周的吞吐量统计信息 |
| `memory/drift-reports/YYYY-MM-DD.md` | 合规性报告 |
| `memory/decisions-audit.jsonl` | 完整的决策记录（JSONL格式） |
| `memory/traces/[标签]-[时间戳].json` | 故障追踪记录 |

### 数据查询示例

```bash
# Recent decisions
tail -20 memory/decisions-audit.jsonl | jq .

# All failure traces
ls memory/traces/

# Latest drift report
cat memory/drift-reports/$(ls memory/drift-reports/ | tail -1)
```

## 工具说明

### `throughput-dashboard.js`
汇总每周的指标数据：路由的任务数量、生成的子代理数量、预估成本、质量比率以及任务路由分布。数据来源于`session-metrics.js`（如果已安装）和`drift-guard-auto.js`。如果数据源缺失，程序仍能正常运行（因为每个模块都是独立的）。

### `decision-audit.js`
以只读方式将决策过程记录到`memory/decisions-audit.jsonl`文件中。每条记录包含以下信息：`id`、`时间戳`、`任务类型`、`决策内容`、`决策理由摘要`以及`结果`。使用`updateOutcome(id, 'success', workspaceRoot)`来标记决策结果已解决。

### `failure-tracer.js`
当质量得分低于7时触发该脚本。会将故障追踪信息以结构化JSON格式写入`memory/traces/`文件。每条故障记录包含工具调用顺序、输出片段以及故障原因的推断结果。该工具用于分析子代理为何表现不佳。

### `drift-guard-auto.js`
根据预设的行为规则（如谄媚行为、不必要的解释等）对代理的输出进行评估。如果安装了`INTENT.md`文件，还会参考其中自定义的评估标准。每周会将评估结果写入`memory/drift-reports/`文件。

## 参考资料

- `references/throughput-dashboard.js`：`throughput-dashboard.js`的完整实现代码
- `references/decision-audit.js`：`decision-audit.js`的完整实现代码
- `references/failure-tracer.js`：`failure-tracer.js`的完整实现代码
- `references/drift-guard-auto.js`：`drift-guard-auto.js`的完整实现代码