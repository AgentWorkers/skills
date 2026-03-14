---
name: openclaw-cron-guardrails
description: 创建、审核、修复或路由 OpenClaw 的 cron 作业以及其他定时执行的代理任务，同时设置安全的默认参数和明确的任务交付/会话路由规则。当用户以自然语言请求提醒、警报、定期提醒、周期性扫描、每日/夜间任务、在当前会话/线程中重复执行某些操作，或任何与 `openclaw cron add/edit/run` 相关的工作流程时，可以使用此功能。特别是在多通道环境中（例如 Discord 与 Feishu 的结合使用），或者在任务交付路由（如 `channel=last`、`sessionTarget`、`timeoutSeconds`、线程目标设置）或自然语言时间表解析可能出现问题的情况下，该功能尤为实用。
---
# OpenClaw Cron Guardrails

当用户需要执行定时或重复性操作时（即使他们没有明确使用“cron”这个词），请使用此技能。

## 该技能的作用

该技能为定时执行的代理任务提供了一套安全防护机制。

可以将 OpenClaw Cron 视为：
- 任务调度器
- 代理任务运行引擎
- 任务交付系统

实际上，设置定时器通常不是最困难的部分；真正困难的是选择合适的任务类型、会话目标以及任务交付目标。

## 使用流程

1. 对请求进行分类。
2. 选择最安全的任务执行模式。
3. 向用户解释任务的具体执行内容。
4. 创建、检查或修改相关任务。
5. 在创建或修改任务后进行验证。

## 首先对请求进行分类

请根据任务类型选择相应的分类：

1. **普通提醒**  
  - 例如：**“20分钟后提醒我回复”**  
  - 默认设置：`main + systemEvent`  
  - 适用于简单的提醒或提示功能。

2. **周期性提醒**  
  - 例如：**“每天早上提醒我查看日历”**  
  - 通常仍使用 `main + systemEvent`  
  - 如果需要考虑实际时间，请明确指定时区。

3. **内部任务**  
  - 例如：**“每晚运行扫描并保存结果到本地”**  
  - 默认设置：`isolated + delivery.mode:none`  
  - 适用于后台任务、扫描操作或需要独立执行的内部任务。

4. **定时可见性发布**  
  - 例如：**“上午9点将每日总结发布到 Discord”**  
  - 默认设置：`isolated + explicit delivery.channel + explicit delivery.to`  
  - 在多渠道环境中，请确保指定明确的接收目标。

5. **会话/线程推送或提示注入**  
  - 例如：**“每10分钟推送当前线程的状态”**  
  - 必须明确保留当前会话/线程的信息；不要将其误判为普通的可见性发布任务。

6. **诊断/修复现有的 Cron 任务**  
  - 例如：**“为什么这个任务没有完成？”**  
  - 首先进行详细检查，切勿盲目重新创建任务。

## 安全默认设置

除非用户有特殊要求，否则请使用以下默认设置：

- 提醒任务：`main + systemEvent`
- 后台任务：`isolated + no-deliver`
- 可见性发布任务：`isolated + explicit channel + explicit to`
- 周期性任务：`explicit tz`（指定时区）
- 复杂任务：`timeoutSeconds >= 180`（设置合理的超时时间）

## 何时需要询问而非猜测

当以下情况不明确时，请向用户寻求具体说明：
- 提醒任务、后台任务还是可见性发布任务
- 是使用当前会话/线程还是外部目标
- 明确指定了发送渠道但未指定接收目标
- 在普通的提醒请求中混入了复杂的任务需求
- 需要考虑实际时间但时区信息不明确

切勿通过默认设置来掩盖潜在的歧义，因为错误的设置可能导致任务发送到错误的位置。

## 响应格式

在处理 Cron 相关请求时，建议按照以下顺序提供信息：
1. 检测到的任务类型
2. 选择的任务执行模式
3. 具体的命令或 JSON/工具参数
4. 选择该模式的安全性依据
5. 验证步骤

## 创建/修改后的验证

在创建或修改任务后，务必进行以下验证：
1. 查看 `openclaw cron list` 的输出。
2. 使用命令 `openclaw cron runs --id <jobId> --limit 5` 检查任务状态。
3. 如果设置安全，再使用 `openclaw cron run <jobId>` 执行任务。
4. 确认以下内容：
  - 会话目标是否正确
  - 任务参数类型是否正确
  - 时区设置是否正确
  - 交付目标是否明确，或者是否选择了 `none`
  - 超时设置是否合理

## 任务修复流程

在修复现有任务时，请按照以下步骤操作：
1. 读取任务的相关信息。
2. 检查任务最近的执行记录。
3. 分析任务失败的原因，而不仅仅是表面现象。

常见的故障类型包括：
- 交付目标不明确
- 权限/认证问题
- 超时时间过短
- 时间安排或时区设置错误
- 提示内容问题

有关更详细的故障排查流程，请参阅 `references/diagnostics.md`。

## 需要阅读的文档

仅阅读与当前任务相关的文档：

### 必读的参考资料（测试版）
- `references/intent-routing.md` — 任务意图分类及规范化规则
- `references/patterns.md` — 安全的默认任务模式
- `references/pitfalls.md` — 常见的故障模式及避免方法
- `references/public-examples.md` — 用户请求的实际使用示例

### 更深入的参考资料
- `references/integration-modes.md` — 不同集成方式的对比（自然语言 vs 规范化意图 vs 规范文档）
- `references/diagnostics.md` — 任务诊断与修复流程
- `references/nl-parser-examples.md` — 自然语言解析器的使用示例
- `references/intent-to-spec-examples.md` — 自然语言意图到 Cron 规范的转换示例
- `references/spec-examples.md` — Cron 规范的 JSON 示例
- `references/target-helpers.md` — 明确的目标字符串使用指南

## 技能范围

请注意，此技能并非旨在实现全面的自然语言理解功能。它的主要作用是：
- 提供易于使用的任务执行模式
- 强制使用安全的任务路由、会话管理和交付设置
- 支持可预测的任务执行流程

上游产品或基础模型可能具备更强大的自然语言理解能力；在这种情况下，优先使用这些更稳定的接口。

## 脚本

当用户需要一个可重复使用的 Cron 定义时，请使用相应的脚本：

- **解析/规范化**：`scripts/parse_nl_intent.py`、`scripts/intent_to_cron_spec.py`
- **验证/渲染/创建**：`scripts/validate_cron_spec.py`、`scripts/render_cron_command.py`、`scripts/create_cron.py`
- **检查/修复**：`scripts/lint_existing_crons.py`、`scripts/cron_fix.py`、`scripts/cron_doctor.py`

## 注意事项

- 该技能不能完全替代 OpenClaw 的官方 Cron 文档。
- 它不能保证在所有运行环境中都能避免故障。
- 当任务意图不明确时，不能随意猜测外部交付目标。
- 建议使用明确、易于复现的 Cron 定义，而非复杂的简写方式。