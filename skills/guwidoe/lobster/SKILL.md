---
name: lobster
description: >
  Lobster workflow runtime for deterministic pipelines with approval gates.
  Use when: (1) Running multi-step automations that need human approval before side effects,
  (2) Monitoring PRs/issues for changes, (3) Processing data through typed JSON pipelines,
  (4) Email triage or batch operations, (5) Any workflow that should halt and ask before acting.
  Lobster saves tokens by running deterministic pipelines instead of re-planning each step.
---

# Lobster

> **贡献方式：** 欢迎在 [github.com/guwidoe/lobster-skill](https://github.com/guwidoe/lobster-skill) 提交源代码和 Pull Request。

Lobster 是一个用于 AI 代理的工作流运行时工具，支持基于文本的管道（pipelines）以及审批流程。

## CLI（命令行界面）的位置

```bash
# Set alias (adjust path to your install location)
LOBSTER="node /home/molt/clawd/tools/lobster/bin/lobster.js"

# Or install globally: npm install -g @clawdbot/lobster
# Then use: lobster '<pipeline>'
```

## 快速参考

```bash
# Run pipeline (human mode - pretty output)
$LOBSTER '<pipeline>'

# Run pipeline (tool mode - JSON envelope for integration)
$LOBSTER run --mode tool '<pipeline>'

# Run workflow file
$LOBSTER run path/to/workflow.lobster

# Resume after approval
$LOBSTER resume --token "<token>" --approve yes|no

# List commands/workflows
$LOBSTER commands.list
$LOBSTER workflows.list
```

## 核心命令

| 命令 | 功能 |
|---------|---------|
| `exec --json --shell "cmd"` | 运行 shell 命令，并将标准输出解析为 JSON 格式 |
| `where 'field=value'` | 根据字段值过滤对象 |
| `pick field1,field2` | 选择指定的字段 |
| `head --n 5` | 获取前 N 个元素 |
| `sort --key field --desc` | 按字段值降序排序 |
| `groupBy --key field` | 按字段值分组 |
| `dedupe --key field` | 删除重复项 |
| `map --wrap key` | 转换数据结构 |
| `template --text "{{field}}"` | 使用模板生成输出 |
| `approve --prompt "ok?"` | 请求审批 |
| `diff.last --key "mykey"` | 与上一次运行结果进行比较（支持状态保存） |
| `state.get key` / `state.set key` | 读取/写入持久化状态 |
| `json` / `table` | 以 JSON 或表格形式输出结果 |

## 内置工作流

```bash
# Monitor PR for changes (stateful - remembers last state)
$LOBSTER "workflows.run --name github.pr.monitor --args-json '{\"repo\":\"owner/repo\",\"pr\":123}'"

# Monitor PR and emit message only on change
$LOBSTER "workflows.run --name github.pr.monitor.notify --args-json '{\"repo\":\"owner/repo\",\"pr\":123}'"
```

## 审批流程（工具模式）

当工作流执行到 `approve` 命令时，系统会返回相应的审批结果：

```json
{
  "status": "needs_approval",
  "requiresApproval": {
    "prompt": "Send 3 emails?",
    "items": [...],
    "resumeToken": "eyJ..."
  }
}
```

要继续执行工作流，请执行以下命令：

```bash
$LOBSTER resume --token "eyJ..." --approve yes
```

## 示例工作流

```bash
# List recent PRs, filter merged, show as table
$LOBSTER 'exec --json --shell "gh pr list --repo owner/repo --json number,title,state --limit 20" | where "state=MERGED" | table'

# Get data, require approval, then process
$LOBSTER run --mode tool 'exec --json --shell "echo [{\"id\":1},{\"id\":2}]" | approve --prompt "Process these?" | pick id | json'

# Diff against last run (only emit on change)
$LOBSTER 'exec --json --shell "gh pr view 123 --repo o/r --json state,title" | diff.last --key "pr:o/r#123" | json'
```

## 工作流文件（.lobster）

工作流文件采用 YAML 或 JSON 格式，包含步骤、条件以及审批流程：

```yaml
name: pr-review-reminder
steps:
  - id: fetch
    command: gh pr list --repo ${repo} --json number,title,reviewDecision
  - id: filter
    command: jq '[.[] | select(.reviewDecision == "")]'
    stdin: $fetch.stdout
  - id: notify
    command: echo "PRs needing review:" && cat
    stdin: $filter.stdout
    approval: required
```

运行方式：`$LOBSTER run workflow.lobster --args-json '{"repo":"owner/repo"}'`

## 与 Clawdbot 的集成

Lobster 可以通过 `clawd.invoke` 调用 Clawdbot 的相关工具：

```bash
$LOBSTER 'clawd.invoke --tool message --action send --args-json "{\"target\":\"123\",\"message\":\"hello\"}"'
```

使用前需要设置 `CLAWD_URL` 和 `CLAWD_TOKEN` 环境变量。

## 状态存储目录

Lobster 默认将状态数据存储在 `~/.lobster/state/` 目录中。可以通过 `LOBSTER_STATE_DIR` 配置自定义存储路径。