---
name: "Skill Manager"
description: "通过安装跟踪和智能建议，主动发现并管理用户的技能。"
version: "1.0.1"
changelog: "Migrate user data to external memory storage at ~/skill-manager/"
---
## 自适应技能管理

通过发现与用户需求相关的技能来提升用户体验，并跟踪技能的安装情况，以避免技能的重复安装。

**参考文档：**
- `dimensions.md` — 触发主动搜索的规则
- `criteria.md` — 提出技能的建议时机和方式

---

## 规则

- 当用户请求重复性或复杂性的任务时，先搜索现有的技能。
- 在建议新技能之前，请先使用以下命令在 ClawHub 中进行搜索：`npx clawhub search <查询内容>`
- 提出技能建议前必须获得用户的同意，切勿未经用户同意就进行安装。
- 记录技能的安装、卸载情况以及原因。
- 查阅 `dimensions.md` 以获取搜索触发条件，参考 `criteria.md` 以确定技能推荐的标准。

## 主动搜索触发机制

如果任务具有重复性、属于特定领域，或者可以从专业指导中受益，那么应主动搜索相关的技能。

---

## 用户数据存储

用户数据存储在 `~/skill-manager/memory.md` 文件中。系统会在用户激活应用程序时加载这些数据。

**仅存储以下由用户明确操作产生的数据：**
- 用户已同意安装的技能
- 用户已卸载的技能（附带卸载原因）
- 用户拒绝安装的技能（附带拒绝原因）
- 用户的技能偏好

**数据格式：**
```markdown
# Skill Manager Memory

## Installed
- slug@version — purpose

## History
- slug — removed (reason)

## Rejected
- slug — reason given

## Preferences
- trait from explicit user statement
```

**规则：**
- 仅记录用户明确操作产生的数据（如安装、卸载、拒绝技能等）。
- 未经用户明确说明，切勿推测用户的技能偏好。
- 数据条目长度应控制在 50 行以内；过期的数据会被存档到 `history.md` 文件中。