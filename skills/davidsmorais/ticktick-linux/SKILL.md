---
slug: ticktick-linux
name: ticktick-linux
description: 通过本地的 `tickrs` CLI 命令行工具来管理 TickTick 任务（包括添加、查看列表以及标记任务为已完成）。
metadata:
  openclaw:
    requires:
      bins: ["/home/david/.cargo/bin/tickrs"]
      env: ["TICKTICK_CLIENT_ID", "TICKTICK_CLIENT_SECRET"]
    emoji: "✅"
---

# TickTick

用于管理TickTick中的任务。

**先决条件**：
您需要先运行以下命令来认证CLI：
`~/.cargo/bin/tickrs init`

## 工具

### `ticktick_list`

列出默认项目（收件箱）或特定项目中的任务。

- **参数**：
  - `project`（字符串，可选）：用于过滤的项目名称。
  - `status`（字符串，可选）：根据状态进行过滤（`incomplete` [默认值]，`complete`）。

- **命令**：
  ```bash
  /home/david/.cargo/bin/tickrs task list --json \
    {{#if project}}--project-name "{{project}}"{{/if}} \
    {{#if status}}--status {{status}}{{/if}}
  ```

### `ticktick_create`

创建一个新的任务。

- **参数**：
  - `title`（字符串，必填）：任务标题。
  - `content`（字符串，可选）：任务描述或备注。
  - `date`（字符串，可选）：自然语言格式的日期（例如：“今天”，“明天下午5点”，“下周五”）。
  - `project`（字符串，可选）：要添加任务的项目名称。
  - `priority`（字符串，可选）：`none`，`low`，`medium`，`high`。

- **命令**：
  ```bash
  /home/david/.cargo/bin/tickrs task create --json \
    --title "{{title}}" \
    {{#if content}}--content "{{content}}"{{/if}} \
    {{#if date}}--date "{{date}}"{{/if}} \
    {{#if project}}--project-name "{{project}}"{{/if}} \
    {{#if priority}}--priority {{priority}}{{/if}}
  ```

### `ticktick_complete`

通过ID将任务标记为已完成（ID可以从`ticktick_list`中获取）。

- **参数**：
  - `id`（字符串，必填）：任务ID。

- **命令**：
  ```bash
  /home/david/.cargo/bin/tickrs task complete "{{id}}" --json
  ```

### `ticktick_projects`

列出所有项目。

- **命令**：
  ```bash
  /home/david/.cargo/bin/tickrs project list --json
  ```