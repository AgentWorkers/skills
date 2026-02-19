---
name: Productivity
slug: productivity
version: 1.0.3
homepage: https://clawic.com/skills/productivity
description: 通过能源管理、时间规划以及针对特定工作场景的生产力系统来规划、集中精力并完成工作任务。
changelog: Added explicit scope and learning boundaries
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 使用场景

当用户寻求关于生产力、注意力集中、时间管理或工作模式的帮助时，该技能会提供相应的框架、策略以及针对具体情境的建议。

## 架构

用户的 productivity（生产力）相关设置保存在 `~/productivity/` 目录下。具体设置方法请参阅 `memory-template.md` 文件。

```
~/productivity/
├── memory.md         # User's stated preferences
└── [topic].md        # Optional topic files
```

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 内存管理设置 | `memory-template.md` |
| 生产力框架 | `frameworks.md` |
| 常见误区 | `traps.md` |
| 学生的生产力提升 | `situations/student.md` |
| 高管的时间管理 | `situations/executive.md` |
| 自由职业者的工作方式 | `situations/freelancer.md` |
| 父母的时间平衡 | `situations/parent.md` |
| 创意工作的状态管理 | `situations/creative.md` |
| 疲劳恢复 | `situations/burnout.md` |
| 创业者的工作方式 | `situations/entrepreneur.md` |
| 多动症（ADHD）患者的应对策略 | `situations/adhd.md` |
| 远程工作 | `situations/remote.md` |
| 管理者的任务分配 | `situations/manager.md` |
| 好习惯的培养 | `situations/habits.md` |
| 内疚情绪的处理 | `situations/guilt.md` |

## 范围

该技能仅负责：
- 提供生产力相关的框架和建议
- 存储用户明确在 `~/productivity/` 目录中指定的偏好设置
- 根据用户提供的情境信息加载相应的指导文档

该技能绝不会：
- 访问用户的日历、电子邮件或联系人信息
- 跟踪用户的时间使用情况或行为
- 通过观察用户的言行来推断其偏好设置
- 发起任何网络请求
- 修改自身的技能文档（SKILL.md）

## 核心规则

### 1. 首先查看用户偏好设置

请阅读 `~/productivity/memory.md` 文件，了解用户明确指定的偏好设置。

### 2. 仅依据用户的明确表述进行学习

| 学习来源 | 举例 |
|------------|----------|
| 直接的表述 | “我早上工作效率最高” |
| 明确的修正说明 | “实际上，我更喜欢使用时间管理工具” |
| 用户主动提到的偏好 | “我的高效工作时间是早上6点到10点” |

切勿通过观察用户的言行或沉默来推断其偏好设置。

### 3. 根据情境选择合适的指导内容

- 询问用户的具体工作或生活情境（例如：学生、家长、高管等）
- 从 `situations/` 目录中加载相应的指导文档
- 不要随意假设用户的情境

### 4. 依靠系统而非意志力

- 规律性比意志力更重要
- 良好的工作环境比自我约束更有效
- 减少阻碍良好行为的因素

### 5. 根据用户的最新反馈更新偏好设置

- 当用户提供新信息时（例如：“我在X时间工作效率最高”或“Y因素会分散我的注意力”等），请及时更新 `memory.md` 文件中的相关内容

## 常见误区

- **提供通用建议**：请先了解用户的具体情境
- **从用户的沉默中推断偏好**：请等待用户给出明确的信息
- **错误地假设用户属于某种特定群体**：不同群体的需求可能不同
- **过度复杂化解决方案**：简单的方法往往更有效

## 技能的自我更新

该技能绝不会修改自身的技能文档（SKILL.md）或辅助文件。所有用户数据均保存在 `~/productivity/memory.md` 文件中。

## 安全性与隐私保护

- **仅存储用户明确提供的信息**：所有数据仅保存在用户本地设备上（`~/productivity/` 目录中）。
- **不涉及网络请求**：该技能不会发送任何网络请求。
- **不侵犯用户隐私**：该技能不会访问用户的日历、电子邮件或任何外部服务，也不会跟踪或监控用户的行为。
- **不推断用户偏好**：所有数据均基于用户的明确输入。