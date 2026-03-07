---
name: incident-triage-playbook
description: 针对服务中断和高错误警报的情况，采用“运行手册优先”的事件分类（incident triage）工作流程。
version: 1.1.0
---
# 事件分诊助手

当警报触发时，可以使用该工具来确保前15分钟的分诊流程的一致性。

## 需要收集的信息

- 主要目标（服务、团队或数据集）
- 当前的影响程度和紧急性
- 被分配的负责人及截止时间

## 核心命令

- `triage intake --service <名称> --severity <严重程度>`
- `triage timeline --append "<事件>"`
- `triage owner --set "<值班人员>"`
- `workflow checklist --from templates/checklist.md`

## 操作说明

- 在采取行动之前，建议明确指定负责人。
- 保持时间线记录的简洁性，并标注时间戳。
- 保存输出结果以供审计和交接使用。
- 本版本新增了一个操作检查表模板，便于交接工作。

版本标记：incident-triage-playbook 1.1.0