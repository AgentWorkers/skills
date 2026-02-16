---
name: "Skill Finder"
description: "找到适合您需求的技能。通过智能搜索、评估和比较来挑选合适的技能。"
version: "1.0.4"
changelog: "Add Security Note about npx for VirusTotal compliance"
---
## 寻找合适的技能

应根据实际需求进行搜索，而不仅仅是技能名称。在推荐技能之前，务必先评估其质量。

**参考文档：**
- `search.md` — 搜索策略和命令
- `evaluate.md` — 质量评估标准
- `criteria.md` — 何时更新用户偏好设置

**相关技能：**
- `skill-manager` — 管理已安装的技能，并主动向用户推荐新技能
- `skill-builder` — 创建新的技能

---

## 功能范围

此技能仅执行以下操作：
- 通过 `npx clawhub search` 命令在 ClawHub 中搜索技能
- 评估搜索结果中的技能
- 将用户的偏好设置存储在 `~/skill-finder/memory.md` 文件中

此技能绝不会执行以下操作：
- 读取 `~/skill-finder/` 目录之外的文件
- 从用户行为中推断用户的偏好设置
- 自动安装技能

---

## 安全提示

此技能使用 `npx clawhub search` 命令来查询 ClawHub 注册表。该操作仅用于读取数据，不会下载或执行任何技能代码。安装技能需要用户的明确同意。

---

## 使用场景

当用户明确提出以下需求时，可以使用此技能：
- “有没有适用于 X 的技能？”
- “帮我找一下能完成 Y 功能的技能”
- “关于 Z，有哪些可用的技能？”

## 工作流程：
1. **搜索**：`npx clawhub search "查询内容"`
2. **评估**：根据 `evaluate.md` 中定义的标准对搜索结果进行评估
3. **比较**：如果有多个匹配项，根据适用程度对结果进行排序
4. **推荐**：展示排名前 1-3 的技能，并说明推荐理由

---

## 数据存储

用户的偏好设置存储在 `~/skill-finder/memory.md` 文件中。

**首次使用前的准备：** 使用 `mkdir -p ~/skill-finder` 创建相应的文件夹。

**存储的内容（仅限于用户明确表达的信息）：**
- 用户明确表示的偏好（例如：“我更喜欢 X”）
- 用户表示喜欢的技能及其原因
- 用户表示不喜欢的技能及其原因

**绝对不会存储的内容：**
- 从用户行为中推断出的偏好设置
- 未经用户确认的安装历史记录
- 任何超出此技能功能范围的数据

**格式说明：**
```markdown
## Preferences
- "value" — user's exact words

## Liked
- slug — "reason user gave"

## Passed
- slug — "reason user gave"
```

**注意：** 每条记录的长度不得超过 50 行。当记录数量超过限制时，系统会自动删除旧记录。