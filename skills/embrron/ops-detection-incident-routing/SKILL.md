---
name: ops-detection-incident-routing
description: 检测代理运行时的异常情况，并通过经过审批流程的安全机制来处理相关事件。适用于需要针对定时任务失败、系统压力、未完成的会话、令牌使用量激增等情况进行确定性检查的场景；同时支持可控的事件处理流程（检测 -> 路由 -> 调查 -> 修复）。
homepage: https://github.com/your-org/openclaw-public-skills
metadata: {"clawdbot":{"emoji":"🛟","requires":{"bins":["bash","jq","python3"]}}}
---
# ops-detection-incident-routing

该技能提供了一套用于检测运行时异常并路由异常事件的工具集，同时具备相应的安全防护机制（guardrails）。

该工具集主要包括以下功能：
1. 从本地状态文件/日志文件中检测运行时异常；
2. 在事件发生过程中实施实时监控及冷却机制（cooldown guards）；
3. 为调查人员或处理人员生成结构化的事故处理指令。

## 使用说明

当您需要为代理系统构建一个生产环境安全级的运维循环（ops loop），并且不希望仅依赖临时性的提示性监控（prompt-only monitoring）时，请使用该技能。

## 相关文件

- `scripts/ops-threshold-detector.sh`：读取会话状态、定时任务状态或快照信息，并将检测结果以 JSONL 格式写入日志文件。
- `scripts/incident-guard-check.sh`：检查特定检测任务的实时监控状态及冷却机制的运行状态。
- `scripts/incident-state-update.sh`：在检测任务开始、完成或失败时更新相应的防护状态。
- `scripts/ops-incident-router.sh`：将检测到的异常信息转换为结构化的事故处理指令。
- `scripts/ops-detector-cycle.sh`：负责执行检测任务及路由异常事件的整个流程。
- `scripts/setup.sh`：用于检查依赖关系并生成示例代码框架。
- `scripts/clean-generated.sh`：在重新发布文件之前，删除生成的 `.jsonl` 文件及锁定相关资源。

## 配置说明

```bash
bash scripts/setup.sh
```

## 快速入门

1. 运行一次完整的测试周期（dry-run cycle）：
```bash
bash scripts/ops-detector-cycle.sh \
  --workspace "$(pwd)/examples/workspace" \
  --state-file "$(pwd)/examples/incident-state.json" \
  --detector-out "$(pwd)/examples/ops-detector.jsonl" \
  --router-out "$(pwd)/examples/router-actions.jsonl"
```

2. 启用实时模式（此时路由器也会获取事件发生的实时数据）：
```bash
bash scripts/ops-detector-cycle.sh \
  --workspace "$(pwd)/examples/workspace" \
  --state-file "$(pwd)/examples/incident-state.json" \
  --detector-out "$(pwd)/examples/ops-detector.jsonl" \
  --router-out "$(pwd)/examples/router-actions.jsonl" \
  --live
```

## 输出规范

- 检测器每次运行后会写入一条 JSON 数据记录。
- 路由器在做出处理决策后，会输出一条 JSON 数据记录。

## 运维模式建议

1. 每 5-15 分钟调度一次 `ops-threshold-detector.sh`；
2. 将最新的检测结果传递给 `ops-incident-router.sh`；
3. 仅根据路由器的输出结果来启动调查或处理流程；
4. 所有修复操作必须经过明确授权后才能执行。

详情请参阅 `references/architecture.md`。