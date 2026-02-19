---
name: linear-todos
description: 这是一个命令行工具（CLI），用于执行 Python 源代码，通过 Linear 的 API 来管理待办事项。该工具支持使用自然语言输入日期、优先级和调度信息来创建任务。这属于“源代码执行”（source-execution）功能：当用户调用相关命令时，位于 `src/linear_todos/` 目录下的 Python 代码会被自动执行。
author: K
tags: [todos, linear, tasks, reminders, productivity]
metadata:
  openclaw:
    primaryEnv: LINEAR_API_KEY
    requires:
      env: [LINEAR_API_KEY]
      config: [~/.config/linear-todos/config.json]
    install:
      - kind: uv
        id: linear-todos
        label: Linear Todos CLI
---
# 线性待办事项管理技能（Linear Todos Skill）

> **⚠️ 这是一个需要源代码执行的技能。** 当您通过命令行界面（CLI）调用相关命令时，该技能会从 `src/linear_todos/` 目录中运行 Python 代码。**请注意**，这不仅仅是一个用于显示信息的工具，还需要您进行一些配置操作。在使用前，请务必阅读 `src/linear_todos/api.py` 文件。

> **🔐 安全提示：** 该技能会将您的 Linear API 密钥以明文形式存储在 `~/.config/linear-todos/config.json` 文件中，**但仅限于您执行了 `setup` 命令的情况下**。请使用专用的 API 密钥，并确保其权限范围尽可能小。该密钥仅用于调用 Linear API，绝不会被传输到其他地方。建议使用环境变量 `LINEAR_API_KEY` 以避免数据持久化存储。

> **审计信息：** 该技能**仅**向 `api.linear.app`（Linear 的官方 GraphQL API）发送 HTTPS 请求，不会发送任何数据到其他地方。具体实现细节请参见 `src/linear_todos/api.py` 文件。

## 所需凭证

| 变量          | 是否必需 | 说明                          |
|-----------------|---------|---------------------------------------------|
| `LINEAR_API_KEY`    | 是        | 来自 [linear.app/settings/api](https://linear.app/settings/api) 的 Linear API 密钥 |
| `LINEAR_team_ID`    | 否        | 默认的待办事项团队 ID                   |
| `LINEAR_STATE_ID`    | 否        | 新创建待办事项的默认状态                   |
| `LINEAR_DONE_STATE_ID` | 否        | 已完成的待办事项的状态                   |
| `LINEAR_TIMEZONE`    | 否        | 您的本地时区（例如：`America/New_York`、`Europe/London`）     |
|                          |             | 用于计算“当天结束时间”                     |

**配置文件路径：** `~/.config/linear-todos/config.json`（由 `setup` 命令生成，权限设置为 0o600）

## 安全性与审计

### 该技能的功能

- **HTTP 请求：** 仅向 `https://api.linear.appGraphQL`（Linear 的官方 API）发送 HTTPS 请求，不涉及任何遥测数据或第三方服务。
- **数据存储：** 仅在您执行了 `setup` 命令的情况下，才会将您的 API 密钥和配置信息以明文形式存储在 `~/.config/linear-todos/config.json` 文件中（权限设置为 0o600）。团队/待办事项数据每次运行时都会重新获取，不会被缓存到本地。
- **运行时行为：** 该技能通过捆绑的 Python 源代码运行（而非预安装的系统工具）。当您通过 CLI 调用命令时，它会执行 `main.py` 以及 `src/linear_todos/` 目录中的代码。
- **设置流程：** 在交互式设置过程中，向导会临时将 `LINEAR_API_KEY` 设置在进程环境中以进行测试，但设置内容不会被持久化保存。
- **自动启用：** 该技能不会自动请求系统权限（默认设置为 `false`），也不会自动为所有代理启用。
- **代码位置：**
  - `src/linear_todos/api.py`：处理所有向 Linear 的 HTTP 请求
  - `src/linear_todos/config.py`：处理配置文件
  - `src/linear_todos/setup_wizard.py`：实现交互式设置向导
  - `src/linear_todos/cli.py`：实现 CLI 命令

### 推荐的安全实践

1. **使用专用 API 密钥：** 为该技能创建一个权限范围有限的专用 Linear API 密钥。如果卸载或停止使用该技能，请及时吊销该密钥。
2. **优先使用环境变量：** 将 `LINEAR_API_KEY` 设置在 shell 环境变量中，避免生成明文配置文件。
3. **审核代码：** 在首次使用前，请仔细检查 `src/linear_todos/api.py` 文件，确保 HTTP 请求的目标地址正确。
4. **在隔离环境中进行初始设置：** 如果不确定该技能的行为，请在容器或虚拟机中运行设置流程以进行测试。

### Cron 作业（可选）

`cron-jobs.txt` 文件包含用于每日数据汇总的示例 Cron 作业脚本。**请注意，这些脚本不会自动安装**，需要您手动添加。

**推荐替代方案：** 使用 OpenClaw 内置的 Cron 任务管理功能，而非系统的 crontab 功能。

## 快速入门

### 设置流程

### 1. 获取 API 密钥

从 [linear.app/settings/api](https://linear.app/settings/api) 获取您的 API 密钥。**建议** 为该技能创建一个权限范围有限的专用 API 密钥。

### 2. 运行设置流程

交互式设置向导将帮助您完成以下步骤：
- 验证您的 API 密钥
- 列出您的 Linear 团队
- 选择待办事项所属的团队
- 配置待办事项的初始状态和完成状态
- 将设置保存到 `~/.config/linear-todos/config.json` 文件（格式为明文 JSON）

### 手动配置（可选）

您也可以通过设置环境变量来配置该技能：

### 创建新的待办事项

**创建新的待办事项时，可以指定完成时间、优先级和描述。**

### 列出所有待办事项

### 将待办事项标记为已完成

### 重新安排待办事项的完成时间

### 按紧急程度整理待办事项

输出结果包含以下分类：
- 🚨 **逾期**：已超过截止日期的待办事项
- 📅 **今日到期**：今天到期的待办事项
- ⚡ **高优先级**：紧急或重要的待办事项
- 📊 **本周内完成**：需在 7 天内完成的待办事项
- 📅 **本月内完成**：需在 28 天内完成的待办事项
- 📝 **无截止日期**：没有固定完成时间的待办事项

### 设置流程

交互式设置向导将引导您完成以下步骤：
- 验证您的 API 密钥
- 选择您的 Linear 团队
- 配置待办事项的初始状态和完成状态
- 将设置保存到 `~/.config/linear-todos/config.json` 文件

## 代理端的处理逻辑

当用户请求提醒或查看待办事项时，系统会执行以下操作：

### 1. 解析用户输入的日期

将用户输入的日期转换为具体的日期格式。

### 2. 确定待办事项的优先级

如果用户未指定优先级，系统会自动分配以下优先级：
- **紧急**（🔥）：必须立即处理的问题
- **高**（⚡）：重要且需尽快处理
- **普通**（📌）：标准优先级（默认值）
- **低**（💤）：可以稍后处理的待办事项

### 日常任务提醒

当用户询问“今天有什么任务需要处理”时，系统会按照以下格式呈现待办事项列表：

### 完成待办事项

当用户表示某项任务已完成时，系统会将其标记为已完成状态。

## 日期解析参考

| 输入            | 解析结果                         |
|-----------------|--------------------------------------------|
| `today`         | 当前日期                          |
| `tomorrow`        | 明天                            |
| `next Monday`      | 下周的周一                        |
| `this Friday`     | 当前的周五                        |
| `in 3 days`       | 3 天后                          |
| `in 2 weeks`       | 14 天后                          |
| `2025-04-15`      | 指定的具体日期                        |

## 优先级等级

| 优先级等级 | 对应数字 | 图标        | 适用场景                          |
|-------------|---------|-----------------------------|
| 紧急        | 1       | 🔥            | 需立即处理的紧急问题                    |
| 高          | 2       | ⚡            | 重要且时间敏感的任务                    |
| 普通        | 3       | 📌            | 标准优先级的任务                      |
| 低          | 4       | 💤            | 可以稍后处理的待办事项                    |

## 时区支持

默认情况下，截止日期的计算基于 UTC 时间（“当天结束时间”为 UTC 23:59:59）。如果您希望使用本地时区来计算“当天结束时间”，可以按照以下方式配置：

### OpenClaw 集成

如果在 OpenClaw 工作空间中运行该技能，系统会自动从 `USER.md` 文件中读取您的时区设置（例如 `timezone: America/New_York`）。无需手动配置时区。

- `--when day`：将截止日期设置为当天结束时间（转换为 UTC 时间）。
- `--when week`：将截止日期设置为 7 天后的当天结束时间（转换为 UTC 时间）。
- `--date "tomorrow"`：将截止日期设置为明天结束时间（转换为 UTC 时间）。

常见的时区设置包括：`America/New_York`、`America/Los_Angeles`、`Europe/London`、`Europe/Paris`、`Asia/Tokyo`。

## 配置优先级

配置项的加载顺序如下（后续设置会覆盖之前的设置）：
1. 默认值
2. 配置文件 `~/.config/linear-todos/config.json`
3. 环境变量 `LINEAR_*
4. 命令行参数 `--team`、`--state`

## 相关文件

- `main.py`：CLI 的主入口文件
- `src/linear_todos/cli.py`：实现 CLI 功能的 Python 文件
- `src/linear_todos/api.py`：处理 Linear API 请求的代码
- `src/linear_todos/config.py`：管理配置信息的文件
- `src/linear_todos/dates.py`：用于日期解析的辅助函数
- `src/linear_todos/setup_wizard.py`：实现交互式设置向导的脚本