---
name: "Workflows via Ask Gina"
description: "用于编写、运行、评估和优化Gina沙箱工作流程的脚本集，具备安全默认设置和可重复的操作机制。"
---
# 通过“Ask Gina Skill”实现的工作流程

## 功能概述

“Ask Gina Skill”为Gina沙箱自动化提供了一种实用的工作流程编写和操作标准：

- 创建并验证工作流程定义。
- 运行工作流程并检查生成的结果/日志。
- 采用可重复的“评估 -> 优化 -> 对比”循环流程。
- 在步骤逻辑中使用安全的TypeScript/SQL/KV模式。

## 使用场景

- 当您需要创建或维护多步骤的工作流程编排时。
- 当您需要从运行结果中复现调试过程时。
- 当您希望通过对比基线数据来衡量工作流程的改进效果时。

## 不适用场景

- 当任务仅涉及单一操作且无需流程编排时。
- 当您只需要高层次的策略描述而无需具体可执行的步骤时。
- 当您无法明确指定权限或处理潜在的副作用时。

## 输入参数

- 工作流程的意图及成功标准。
- 触发条件及其输入数据格式。
- 所需的工具/数据来源及权限范围。
- 可选的基线运行ID（用于后续优化）。

## 输出结果

- 经过验证的工作流程定义（格式为`.ts`）。
- 可执行的工作流程结果（包含可追踪的详细信息）。
- 包含基线对比的评估记录。
- 为防止回归问题提供的明确回滚路径。

## 核心命令

```bash
workflow create <id>
workflow validate <id>
workflow run <id> [--input JSON]
workflow status <run-id>
workflow logs <run-id> [--step <step-id>]
workflow eval <run-id>
workflow optimize <id> --baseline <run-id>
workflow rollback <id> <opt-run-id>
```

## 设置步骤

1. 确保具备所需的工作流程工具（执行`workflow list`命令应无错误）。
2. 在`/workspace/.harness/workflows/`目录下创建或打开目标工作流程文件。
3. 如果存在不同版本的工作流程，请使用`@latest.ts`命名格式来区分它们。
4. 在每次运行前进行验证：`workflow validate <id>`。
5. 对于涉及风险的操作，请先捕获基线数据并在编辑前进行评估。

## 能力契约检查清单

对于每个工作流程条目，需明确指定以下内容：

- 触发条件。
- 输入参数。
- 输出结果。
- 可能产生的副作用。
- 可能出现的故障模式。
- 权限范围。

## 可能出现的故障模式

- 由于步骤定义错误导致的验证失败。
- TypeScript/SQL/Bash步骤中的运行时错误。
- 缺少必要的工具权限或工具本身不可用。
- 数据格式变化导致解析/类型转换失败。
- 外部调用中的超时或重试次数耗尽。

## 安全性与权限管理

- 通过`allow`和`block`指令为每个步骤设置最小权限。
- 在提交文档中明确声明所需的权限（避免使用通配符权限）。
- 绝不要在技能描述、日志或示例中包含任何敏感信息（如密码）。
- 将文件写入、数据存储、外部数据交互等操作视为明确的副作用。

## 需求文档要求

- 设置过程应简单明了，审核人员能在10分钟内完成。
- 提供一个可复现的运行结果示例或运行日志。
- 明确说明预期的输出结果及可接受的故障行为。

## 可选目录

```text
workflows/
  SKILL.md
  references/   # implementation and API details
  scripts/      # optional helpers for repeatable checks
  assets/       # optional diagrams/screenshots
```

## 参考资料

相关的技术参考资料已单独整理如下：

- `references/cli-and-definition.md`
- `references/eval-optimize-and-artifacts.md`
- `references/polymarket-patterns.md`

请将这些参考资料作为附录使用，本文件主要聚焦于工作流程的操作层面。