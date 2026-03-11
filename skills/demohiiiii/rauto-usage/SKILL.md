---
name: rauto-usage
description: "为用户直接执行 rauto 功能：包括运行设备命令、模板执行、事务处理（tx block）、事务工作流（tx workflow）、多设备协同操作（multi-device orchestration）、回放（replay）、备份/恢复（backup/restore）以及连接管理（connection/profile/template/history）等操作。该功能可响应诸如“为我运行命令”（run command for me）、“在设备上执行操作”（execute on device）、“查看历史记录”（check history）、“协调多个设备”（orchestrate multiple devices）、“应用分阶段部署策略”（apply staged rollout）、“使用库存/组管理”（use inventory/groups）、“诊断用户配置文件”（diagnose profile）、“管理模板/配置文件/连接”（manage templates/profiles/connections）、“回放操作记录”（replay records）或“恢复备份数据”（restore backup data）等请求。"
---
# Rauto 使用说明

尽可能直接为用户执行 rauto 操作，避免提供过于繁琐的教程式回答。

## 核心模式

优先采用“先行动、后确认”的处理方式：

1. 解析用户的目标，并判断该操作是只读操作还是需要修改配置的操作。
2. 对于只读操作，立即执行相应的 `rauto` 命令。
3. 对于需要修改配置的操作，优先使用 `tx`、`tx-workflow` 或 `orchestrate` 等工具，并确保操作具有回滚机制。
4. 如果命令是由代理自动生成的，在执行前需要用户确认。
5. 返回关键操作结果（而非原始数据），同时提供所使用的命令信息。

## 执行规则

1. 对于只读/查询请求，立即执行：
   - 例如：`device list`、`connection list`、`history list`、`templates list`、`replay --list`。
2. 对于需要修改配置的请求，优先使用支持回滚的执行方式：
   - 单个操作：`tx`
   - 多步骤/多资源操作：`tx-workflow`
   - 多设备分阶段部署：`orchestrate`
3. 对于由代理生成的修改命令，不要立即执行，而是先展示计划中的操作内容及回滚策略，并请求用户确认。
4. 对于明确的只读命令（例如 `show`），不需要使用 `tx` 或 `workflow`。
5. 连接信息的确定优先级如下：
   - 明确提供的命令参数 > `--connection <name>` > 请求用户补充缺失的信息。
6. 如果代理能够执行某个操作，就不要让用户手动运行该操作。
7. 以结构化的方式汇总输出结果，包括目标设备、操作模式、操作结果、错误信息以及下一步需要执行的操作。

## 风险控制机制

在执行具有破坏性的操作之前，必须获得用户的明确确认：
- 如 `rauto backup restore ... --replace`、`profile/template/connection delete` 等操作。
- 当用户的操作意图不明确时，不要执行会修改配置的 `tx` 或 `workflow` 操作。

对于配置修改操作，还需遵循以下安全要求：
- 优先使用具有回滚机制的 `tx`、`tx-workflow` 或 `orchestrate`。
- 对于基于工作流的修改操作，先执行 `--dry-run` 以验证操作效果。
- 在执行 `orchestrate` 之前，务必检查目标范围、设置 `fail_fast` 选项、控制并发数，并明确回滚边界。
- 未经用户确认，严禁自动执行代理生成的修改命令。
- 在执行任何操作之前，必须在提案中提供详细的回滚方案。

如果用户明确要求执行具有破坏性的操作，方可继续执行。

## 缺失输入的处理策略

仅请求用户提供必要的输入信息：
- 对于 `exec`、`template`、`tx`、`tx-workflow`、`orchestrate` 或 `connection test` 等操作，需要完整的主机凭据或有效的 `--connection` 参数。
- 对于 `replay` 操作，需要提供记录文件的路径或 JSONL 数据源。
- 对于历史记录查询，需要提供连接名称。

## 响应格式

在执行命令后，需报告以下信息：
- `Operation`：执行的操作类型。
- `Command`：具体的 rauto 命令内容。
- `Result`：操作的关键结果摘要。
- `Notes`：操作过程中遇到的风险、错误信息或后续需要执行的操作。

## 参考资料（按需加载）

- 代理执行决策流程及命令模板：`references/agent-execution.md`
- 完整的 CLI 命令参考：`references/cli.md`
- 可执行的多设备编排 JSON 模板（英文版）：`references/orchestration-json-template.md`
- 多设备编排前的风险检查：`references/orchestration-risk-check.md`
- 运行时存储路径：`references/paths.md`
- 故障排除与恢复指南：`references/troubleshooting.md`
- 全端操作场景说明：`references/scenarios.md`
- 英文版常见问题解答：`references/examples.md`
- 可执行的工作流 JSON 模板（英文版）：`references/workflow-json-template.md`
- 网页操作相关内容（仅当用户请求时提供）：`references/web.md`