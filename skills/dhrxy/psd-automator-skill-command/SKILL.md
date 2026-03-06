---
name: psd-automator-skill-command
description: "通过输入技能命令来调度 PSD 自动化任务，同时重用相同的 /psd orchestrator。需要 psd-automator 核心组件。"
metadata:
  openclaw:
    userInvocable: true
    commandDispatch: tool
    commandTool: psd_automator_skill_command
    commandArgMode: raw
---
# psd-automator-skill-command

此技能命令提供了与 `/psd` 相同的功能，但不会改变 `/psd` 的现有行为。

## 使用方法

```text
/psd-automator-skill-command <agentId> <taskJsonPath|中文需求> [--dry-run] [--index <indexPath>]
```

示例：

```text
/psd-automator-skill-command design-mac-01 帮我找到20260302工位名牌.psd，把姓名改成小一，并保存成png放到桌面
```

## 注意事项

- 该命令重用了与 `/psd` 相同的 PSD 编排流程。
- 它确保 DINGTALK 图像标记的行为与现有的 PSD 工作流程保持一致。
- 它会使用 `entrypoint=skill_command` 将相关数据记录到相同的技能使用统计存储系统中。