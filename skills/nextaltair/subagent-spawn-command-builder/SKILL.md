---
name: subagent-spawn-command-builder
description: 从 JSON 配置文件中生成 `build Sessions Spawn` 命令的负载数据。当您需要可重用的子代理配置（包括模型、思考时间、超时设置、代理 ID、标签等）以及无需执行 `spawn` 操作即可使用的命令相关 JSON 数据时，可以使用此方法。
---

# subagent-spawn-command-builder

该工具用于根据配置文件生成用于 `sessions_spawn` 的 JSON 数据。该工具本身不会执行 `sessions_spawn` 操作，仅负责生成所需的 JSON 数据。

## 相关文件

- 配置文件模板：`state/spawn-profiles.template.json`
- 当前使用的配置文件：`state/spawn-profiles.json`
- 生成 JSON 数据的脚本：`scripts/build_spawn_payload.py`
- 脚本运行日志：`state/build-log.jsonl`

## `sessions_spawn` 支持的参数

- `task`（必填）
- `label`（可选）
- `agentId`（可选）
- `model`（可选）
- `thinking`（可选）
- `runTimeoutSeconds`（可选）
- `cleanup`（可选，取值：`keep` 或 `delete`）

## 设置步骤

```bash
cp skills/subagent-spawn-command-builder/state/spawn-profiles.template.json \
   skills/subagent-spawn-command-builder/state/spawn-profiles.json
```

接下来，请编辑 `spawn-profiles.json` 文件。

## 生成 JSON 数据

```bash
python3 skills/subagent-spawn-command-builder/scripts/build_spawn_payload.py \
  --profile heartbeat \
  --task "Analyze recent context and return a compact summary" \
  --label heartbeat-test
```

该脚本会生成可直接用于 `sessions_spawn` 的 JSON 数据。

## 数据合并规则与优先级

数据值的优先级顺序如下：

1. 命令行参数（如 `--model`、`--thinking` 等）
2. 配置文件中的值（格式：`profiles.<name>.*`）
3. 默认值（格式：`defaults.*`）

`task` 参数始终来自命令行参数 `--task`。

## 命令行参数说明

注意：如果生成的任务包含 Python 执行步骤，请使用 `python3` 而不是 `python` 来执行相关命令。

- `--profile`（必填）
- `--task`（必填）
- `--label`
- `--agent-id`
- `--model`
- `--thinking`
- `--run-timeout-seconds`
- `--cleanup keep|delete`