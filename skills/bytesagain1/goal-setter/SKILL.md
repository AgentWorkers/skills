---
name: goal-setter
description: "**Goal Setter** — 一个帮助你逐步实现目标的个人日常工具。它用于跟踪和管理你的生活。在你需要目标设定功能时，可以使用它。"
runtime: python3
license: MIT
---
# 目标设定器（Goal Setter）

目标设定器——帮助你一步步实现自己的目标

## 为什么需要这项技能？

- 专为个人日常使用设计
- 无需依赖任何外部服务或账户
- 数据存储在本地，保护你的隐私
- 命令简单，但功能强大

## 命令说明：

- `set` — <目标> [截止日期]     设置一个新的目标
- `milestone` — <目标> <步骤>   为目标添加里程碑
- `progress` — <目标> <完成百分比>  更新目标进度（0-100%）
- `check` — <目标> <里程碑>  标记里程碑已完成
- `list` —                列出所有目标
- `active` —             显示当前活跃的目标
- `review` —             每周目标回顾
- `motivate` —            提供激励性的名言
- `archive` — <目标>            将已完成的目标归档
- `stats` —             查看目标统计信息
- `info` —                查看版本信息

## 快速入门

```bash
goal_setter.sh help
```

> **注意**：这是 BytesAgain 公司自主研发的工具，与任何第三方项目无关，也未基于任何第三方项目进行开发。

---
由 BytesAgain 提供支持 | bytesagain.com | hello@bytesagain.com