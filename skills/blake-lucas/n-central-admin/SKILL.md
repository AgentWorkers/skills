---
name: n-central-admin
description: 通过其Web UI安全、高效地操作N-able N-central。该工具适用于设备管理、过滤器设置、规则配置、定时任务管理、自动化策略制定、监控关联设置以及针对N-central中的租户/客户/站点级别的更改操作。
---
# N-central 管理

使用此技能来执行可靠的、基于浏览器的 N-central 操作。

## 操作模型

对于几乎所有的更改，请遵循以下步骤：
1. 确认更改的范围（系统操作、客户操作或站点操作）。
2. 确认目标范围（过滤预览或特定设备）。
3. 应用更改（规则/任务/模板/操作）。
4. 在少量设备上验证更改效果。
5. 仅在验证通过后扩大更改范围。

## 仅按需阅读参考资料

- 阅读 `references/ui-navigation-and-operating-model.md`，了解层次结构、模块导航和变更控制流程。
- 阅读 `references/filters-and-rules.md`，了解过滤表达式逻辑、规则行为、触发事件和故障排除方法。
- 阅读 `references/automation-policies-and-tasks.md`，了解自动化管理器的行为、计划任务的执行方式以及离线/时间相关的注意事项。
- 阅读 `references/device-details-tabs-and-tools.md`，了解每个设备的标签页、快速操作以及工具的可用性。
- 阅读 `references/browser-operator-playbooks.md`，了解浏览器执行脚本和稳定性相关的内容。

## 安全准则

- 尽量选择能够解决具体问题的最小范围进行操作。
- 建议克隆并定制共享对象，而不是直接进行有风险的修改。
- 为过滤器/规则/任务指定明确的名称和用途。
- 在保存前和保存后都确认目标设备的数量。
- 对于影响范围较大的更改，应先进行小范围测试。
- 使用监控、关联信息和审计追踪来验证更改结果。

## 快速解决问题

- 如果需要了解左侧导航栏的点击路径，请参考 `references/ui-navigation-and-operating-model.md#left-navigation-path-map-common-admin-tasks`。
- 如果规则行为异常，请参考 `references/filters-and-rules.md#rule-not-firing-checklist`。
- 如果计划执行行为出现问题，请参考 `references/automation-policies-and-tasks.md#offline-and-timing-behavior`。
- 如果目标选择器按钮难以理解，请参考 `references/automation-policies-and-tasks.md#dual-list-selector-buttons-targeting-and-similar-fields`。
- 如果某个设备上缺少预期的工具，请参考 `references/device-details-tabs-and-tools.md#why-actions-may-be-unavailable`。
- 如果浏览器自动化出现故障，请参考 `references/browser-operator-playbooks.md#ui-stability-patterns`。