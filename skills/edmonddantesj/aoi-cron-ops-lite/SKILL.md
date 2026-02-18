---
name: aoi-cron-ops-lite
description: Cron hygiene and cost-control for OpenClaw. Use to audit/optimize scheduled jobs (cron): detect duplicates, noisy notifications, heavy cadence, repeated failures, and propose safe changes. Default is report-only (no automatic cron updates/removals) and requires explicit user approval before applying schedule changes.
---

# AOI Cron Ops (Lite)

## 功能介绍
- 从 OpenClaw 的 cron 作业列表中生成一份 **易于人类阅读的审计报告**。
- 识别常见的操作问题：
  - 作业重复（多个作业执行相同的功能）
  - 通知信息过多（通知作业过多）
  - 执行频率过高（导致成本增加或系统负载过大）
  - 外部依赖项频繁出错或不稳定
  - 环境配置缺失或无效（例如，缺少必要的配置文件）

## 不可更改的规则
- **默认模式下，仅提供审计报告功能。**
- 除非用户明确要求进行更改，否则 **不得** 禁用、更新或删除任何 cron 作业。
- 在提出更改建议时，应尽量采用 **最小化且可逆的修改方式**：
  - 将作业的更新频率设置为 `none`
  - 降低作业的执行频率
  - 添加一个用于汇总作业信息的辅助作业

## 快速入门（操作步骤）
1) 获取当前的 cron 作业列表（JSON 格式）：
   - 如果使用 OpenClaw 工具：执行 `cron(list)` 并保存输出结果。
   - 如果在终端环境中：执行 `openclaw cron list --json > cron_jobs.json`（如果该命令可用）。

2) 运行分析工具：
```bash
python3 skills/aoi-cron-ops-lite/scripts/analyze_cron_jobs.py --in cron_jobs.json
```

## 预期输出格式
- 输出内容包含 10–25 行信息：
  - 启用/禁用的 cron 作业总数
  - 最主要的潜在风险（前 5 项）
  - 建议采取的应对措施（分类列出）
  - “应用计划”（需要手动执行的修复方案）

## 高级版本功能（后续扩展）
- 高级版本支持自动应用安全补丁（需遵循相关策略并获得批准），生成类似 Pull Request 的差异报告，并维护操作历史记录。
- Lite 版本严禁自动执行任何操作。