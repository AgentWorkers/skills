---
name: brainrepo
description: >
  Your personal knowledge repository — capture, organize, and retrieve everything using PARA + Zettelkasten.
  Triggers on: "save this", "remember", "note", "capture", "brain dump", daily/weekly
  reviews, searching stored knowledge, managing projects/areas/people. Works with any AI agent that reads
  markdown. Stores everything as .md files in a Git repo for Obsidian, VS Code, or any editor.
---

# BrainRepo

这是您的个人知识管理仓库。它能快速捕获信息、自动进行组织，并支持即时检索。

## 数据存储位置

**固定路径：** `~/Documents/brainrepo/`

此路径无法配置。所有数据都存储在这里。

## 首次使用时的检查

**在采取任何操作之前**，请检查 brainrepo 是否已初始化：

1. 确认 `~/Documents/brainrepo/` 是否存在，并且具有预期的文件夹结构（`Inbox/`, `Projects/`, `Areas/`）。
2. 如果未找到 → **自动执行初始化流程**。
3. 如果已找到 → 可以根据用户需求继续使用。

## 初始化流程

在首次使用或用户请求时自动触发初始化流程：

1. 在 `~/Documents/brainrepo/` 下创建相应的文件夹结构。
2. 使用 `assets/templates/` 中的模板创建初始文件：
   - `Tasks/index.md` — 任务管理文件夹
   - `Areas/personal-growth/index.md` — 个人成长相关文件
   - `Areas/family/index.md` — 家庭相关文件
3. （可选）初始化 Git 仓库：
   ```bash
cd <path> && git init && git add -A && git commit -m "init: brainrepo"
```

4. 确认初始化完成，并向用户展示快速使用指南。

## 核心工作流程

**数据捕获 → 处理 → 检索**

1. **捕获数据**：将所有信息放入 `Inbox/` 文件夹（暂时不进行分类）。
2. **处理数据**：在晚上对 `Inbox/` 中的内容进行整理，将其移至相应的永久存储位置。
3. **检索信息**：通过系统请求 AI 来查找所需的内容。

## 仓库结构

详细结构请参阅 [references/structure.md](references/structure.md)。

## 数据捕获规则

### 应立即捕获的内容

| 类型 | 存储位置 | 示例 |
|------|-------------|---------|
| 随机想法 | `Inbox/` | “也许我们应该……” |
| 做出决定 | `Inbox/` 或 `Notes/` | “决定使用 Next.js” |
| 个人信息 | `People/` | 新联系人信息或更新 |
| 项目更新 | `Projects/<项目名称>/` | 会议记录、项目进度 |
| 任务/待办事项 | `Tasks/index.md` | “需要完成 X 任务” |
| 链接/文章 | `Resources/` 或 `Inbox/` | 带有上下文的网址 |
| 个人成长 | `Areas/personal-growth/` | 健康、习惯、学习相关内容 |
| 家庭信息 | `Areas/family/` | 重要日期、家庭相关事项 |

### 不应捕获的内容

- 无实际信息价值的随意聊天记录
- 临时性的查询（如“现在几点了”）
- 可以在线轻松搜索到的信息

## 笔记格式

所有笔记都采用简洁的格式编写，具体格式请参考 [CODE_BLOCK_3___]。

创建新笔记时，请使用 `assets/templates/` 中提供的模板。

## 日常工作流程

### 白天
- 将所有信息捕获到 `Inbox/` 文件夹中。
- 不要立即进行分类，只需先保存下来。

### 晚上（5-10 分钟）
- 处理 `Inbox/` 中的笔记：
  - 将需要长期保存的内容移至相应文件夹，或直接删除。
- 在 `Journal/YYYY-MM-DD.md` 文件中记录处理总结。
- 执行 `git commit -am "daily processing"` 命令。

## 周期性回顾（每周日，15 分钟）

- 回顾所有项目：是否有项目仍然在进行中？
- 检查各个分类下的内容：是否有被忽视的部分？
- 将已完成的项目移至 `Archive/` 文件夹。
- 更新 `Tasks/index.md` 文件。

详细的工作流程请参阅 [references/workflows.md](references/workflows.md)。

## 常用命令

| 用户指令 | 执行操作 |
|-----------|--------|
| “设置 BrainRepo” | 自动执行初始化流程并创建文件夹结构 |
| “保存这个内容：[文本]” | 将内容捕获到 `Inbox/` |
| “新建项目：[项目名称]” | 使用模板创建新项目 |
| “添加人员：[姓名]” | 使用模板创建人员信息文件 |
| “关于 X，我知道什么？” | 通过系统查询相关信息 |
| “进行日常回顾” | 处理 `Inbox/` 中的笔记并更新日志文件 |
| “进行每周回顾” | 全面检查整个知识管理系统 |

## 链接管理

使用 `[[wiki-links]]` 标签来关联笔记之间的内容。

## 项目与分类的区别

| 项目 | 分类 |
|------|-------|
| 有截止日期 | 分类没有固定结束日期 |
| 可以“完成” | 分类中的内容会长期保留 |
| 需要达到特定结果 | 分类中的内容需要持续维护 |

## 文件命名规则

- 文件夹名称：使用驼峰式命名法（例如 `Projects/MyNewProject`）
- 文件名称：使用驼峰式命名法（例如 `my-task.md`）
- 日期文件：格式为 `YYYY-MM-DD.md`
- 人员信息文件：格式为 `firstname-lastname.md`

## 参考资料

- [结构指南](references/structure.md) — 仓库文件夹的详细划分规则
- [工作流程](references/workflows.md) — 日常/每周/每月的工作流程
- [模板](assets/templates/) — 笔记模板