---
name: cairn
description: 使用 Markdown 文件进行 AI 代理的项目管理。安装并使用 cairn CLI 来创建项目、管理任务、跟踪项目进度，并通过共享的 Markdown 文件工作空间协调人机协作。
---

# Cairn — 一款专为 AI 设计的项目管理工具

Cairn 为您和您的 AI 代理提供了一个基于 Markdown 文件的共享工作空间，用于管理和协调整个项目和任务。项目状态是通过统一的标记语言（Markdown 格式）来表达的，任何能够读取 Markdown 文件的 AI 都可以轻松使用该工具。

## 安装

```bash
npm install -g cairn-work
cairn onboard
```

运行 `cairn onboard` 命令后，系统会在 `~/cairn/` 目录下自动生成 `AGENTS.md` 和 `.cairn/planning.md` 两个文件，这些文件会被 AI 代理自动读取并用于理解工作空间的结构和规则。

## 社区资源

- 关注 [@letcairnwork](https://x.com/letcairnwork) 在 X 社交平台上的动态
- 访问 [letcairn.work](https://letcairn.work/) 官网
- [提交问题](https://github.com/letcairnwork/cairn-cli/issues)
- [参与讨论](https://github.com/letcairnwork/cairn-cli/discussions)

## 核心命令

### 工作空间操作

- `cairn status` — 查看项目概览及任务数量
- `cairn my` — 查看分配给您的任务
- `cairn active` — 查看所有正在进行中的任务
- `cairn doctor` — 检查工作空间的运行状态

### 项目与任务管理

- `cairn create project "项目名称" --description "..." --objective "..."` — 创建一个新的项目
- `cairn create task "任务名称" --project <项目slug> --description "..." --objective "..."` — 创建一个新的任务
- `cairn list tasks [--status pending,in_progress] [--project <项目slug>]` — 根据状态或项目名称筛选任务列表
- `cairn search "关键词"` — 根据内容搜索任务

### 任务流程

- `cairn start <任务名称>` — 开始执行任务（任务状态变为 `in_progress`）
- `cairn note <任务名称> "进度更新"` — 为任务添加状态备注
- `cairn artifact <任务名称> "交付物名称"` — 为任务创建关联的交付物文件
- `cairn done <任务名称>` — 完成任务（任务状态变为 `review` 或 `completed`）
- `cairn block <任务名称> "原因"` — 将任务标记为“已阻塞”

### 维护操作

- `cairn update-skill` — 在 CLI 更新后刷新工作空间的上下文信息
- `cairn upgrade` — 将 CLI 升级到最新版本

## 工作空间结构

```
~/cairn/
  AGENTS.md                  # Agent context (auto-generated)
  .cairn/planning.md         # Planning guide (auto-generated)
  projects/
    project-slug/
      charter.md             # Why, success criteria, context
      artifacts/             # Deliverables (design docs, proposals, etc.)
      tasks/                 # Individual task markdown files
  inbox/                     # Ideas to triage
  memory/                    # Workspace memory
```

## 任务状态

`pending` → `next_up` → `in_progress` → `review` → `completed`（任务状态可随时变为 `blocked`）

## 自主化级别

您可以为每个任务设置不同的自动化级别，以控制 AI 代理的执行权限：
- **propose**：代理仅负责任务规划，最终由您审核后完成
- **draft**：代理负责执行任务，您需要批准后才能发布结果
- **execute**：代理拥有完全的自主权，任务会直接标记为 `completed`

## 使用提示

- 首先运行 `cairn onboard` 命令，以配置代理所需的所有环境。
- 使用 `cairn my` 命令快速查看您当前的任务分配情况。
- 使用 `cairn artifact` 命令为任务创建关联的交付物文件。
- 所有数据都采用纯 Markdown 格式，并包含 YAML 标头，便于版本控制。