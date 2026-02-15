---
name: ticktick-cli
description: 通过 `ticktick` 命令行界面来操作 TickTick，包括身份验证、数据读取/查询流程以及对任务、项目、文件夹、标签、习惯、用户信息、专注度分析数据的安全修改等操作。当用户需要执行 TickTick 终端命令、解析 TickTick CLI 的 JSON 输出、解析 ID，或解决 TickTick CLI 的配置/认证问题时，可以使用该工具。
version: 1.0.3
metadata:
  openclaw:
    requires:
      env:
        - TICKTICK_CLIENT_ID
        - TICKTICK_CLIENT_SECRET
        - TICKTICK_ACCESS_TOKEN
        - TICKTICK_USERNAME
        - TICKTICK_PASSWORD
---

# TickTick CLI

使用此工具，您可以直接通过终端命令执行 TickTick 工作流程，并获得确定性的输出结果。

## 执行策略

1. 首先执行用户请求的 `ticktick ...` 命令。无需进行版本检查或工具存在性检查。
2. 如果由于缺少 CLI 而导致执行失败，请加载 `references/setup-and-auth.md` 并按照安装恢复流程进行操作。
3. 如果由于认证/配置问题导致执行失败，请加载 `references/setup-and-auth.md` 并按照引导进行认证操作，然后再尝试执行原始命令。
4. 认证恢复过程仅通过 CLI 完成，严禁自行编写自定义的 SDK/Python 令牌交换脚本。
5. 仅在命令因未知参数或缺少必需参数而失败时，使用 `--help` 选项进行故障排查。

## 默认设置

- 对于所有数据相关的命令，优先使用 `--json` 选项并解析结构化输出。
- 在进行数据操作之前，将名称解析为对应的 ID；切勿随意猜测标识符。
- 每次写入操作都需遵循“读取 -> 修改 -> 验证”的流程。
- 当需要确保操作结果具有确定性时，建议在修改任务时明确指定 `--project PROJECT_ID` 参数。
- 对于仅包含日期的字段，使用明确的日期格式（`YYYY-MM-DD`）；对于需要时间信息的字段，使用 ISO 日期时间格式。

## 安全性要求

- 在进行安装或环境更改之前，必须获得用户的明确确认。
- 除非用户明确要求，否则严禁使用可能带来风险的系统安装参数。
- 绝不在用户可见的输出中显示任何敏感信息（如密码或令牌）。
- 在执行以下具有破坏性的操作之前，必须获得用户的明确确认：
  - `tasks delete`（删除任务）
  - `projects delete`（删除项目）
  - `folders delete`（删除文件夹）
  - `columns delete`（删除列）
  - `tags delete`（删除标签）
  - `tags merge`（合并标签）
  - `habits delete`（删除习惯记录）

## 参考文档

仅加载当前操作所需的相关文档：

- [设置与认证](references/setup-and-auth.md)
- [任务](references/tasks.md)
- [项目](references/projects.md)
- [文件夹](references/folders.md)
- [列](references/columns.md)
- [标签](references/tags.md)
- [习惯记录](references/habits.md)
- [用户、关注项及同步设置](references/user-focus-sync.md)
- [故障排除](references/troubleshooting.md)