---
name: "Skill Manager"
description: "管理已安装技能的生命周期：根据使用场景提供推荐，跟踪安装情况，检查更新，并清理未使用的技能。"
version: "1.0.3"
changelog: "Fix contradictions: clarify declined tracking, add npx security note"
---
## 技能生命周期管理

管理已安装技能的完整生命周期：发现、安装、更新和清理。

**参考文档：**
- `suggestions.md` — 根据当前任务推荐技能的时机
- `lifecycle.md` — 安装、更新和清理流程

**配套工具：**
- `skill-finder` — 用户主动搜索工具（例如：“为我查找适用于 X 的技能”）
- `skill-manager` — 主动进行技能生命周期管理

---

## 功能范围

此技能仅执行以下操作：
- 根据当前任务上下文推荐技能
- 在 `~/skill-manager/inventory.md` 文件中记录已安装的技能
- 记录用户明确拒绝使用的技能及其拒绝原因
- 检查技能是否有更新

**注意事项：**
- 该技能不会统计任务重复次数或用户行为模式
- 未经用户明确同意，不会自动安装任何技能
- 该技能不会读取 `~/skill-manager/` 目录以外的文件

---

## 安全提示

此技能使用 `npx clawhub` 命令，这些命令会从 ClawHub 注册表中下载并执行相关代码。这是技能管理的标准方式。在安装任何技能之前，请务必仔细检查相关内容。

---

## 基于上下文的技能推荐

在执行任务时，请注意当前的 **任务上下文**：
- 如果用户提到了特定的工具（如 Stripe、AWS、GitHub），请检查是否存在相应的技能
- 如果任务涉及不熟悉的领域，建议用户进行搜索

这种推荐行为是基于当前任务上下文进行的，而非对用户行为模式的跟踪。

## 生命周期管理操作

| 操作        | 命令                |
|-------------|---------------------|
| 安装         | `npx clawhub install <技能名称>`      |
| 更新         | `npx clawhub update <技能名称>`      |
| 查看信息     | `npx clawhub info <技能名称>`      |
| 卸载         | `npx clawhub uninstall <技能名称>`      |

---

## 数据存储

所有技能信息存储在 `~/skill-manager/inventory.md` 文件中。

**首次使用方法：** `mkdir -p ~/skill-manager`

**数据格式：**
```markdown
## Installed
- slug@version — purpose — YYYY-MM-DD

## Declined
- slug — "user's stated reason"
```

**记录的内容：**
- 用户安装的技能（包括安装目的和日期）
- 用户明确拒绝使用的技能及其拒绝原因

**记录拒绝使用的原因：** 为了避免再次推荐用户已经拒绝过的技能。仅记录用户明确表示拒绝的技能信息。