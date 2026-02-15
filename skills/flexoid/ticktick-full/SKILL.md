---
name: ticktick-cli
description: 通过 `ticktick` 命令行界面来操作 TickTick，包括身份验证、数据读取/查询、以及对任务、项目、文件夹、标签、习惯、用户信息、专注度分析数据以及同步数据的操作。当用户需要运行 TickTick 终端命令、解析 TickTick CLI 的 JSON 输出、解析 ID，或解决 TickTick CLI 的配置/认证问题时，可以使用该工具。
---

# TickTick CLI

使用此工具，您可以通过终端命令直接执行 TickTick 工作流程，并获得可预测的运行结果。

## 执行策略

1. 首先执行用户请求的 `ticktick ...` 命令。无需进行版本检查或工具是否存在性的预验证。
2. 如果由于 CLI 未安装而导致执行失败，请加载 `references/setup-and-auth.md` 并按照安装恢复流程进行操作。
3. 如果执行失败是由于认证或配置问题引起的，请加载 `references/setup-and-auth.md` 并按照引导式认证流程进行操作，然后再重试原始命令。
4. 认证恢复过程仅通过 CLI 完成，严禁自行编写自定义的 SDK/Python 令牌交换脚本。
5. 仅在命令因未知参数或缺少必需参数而失败时，使用 `--help` 选项进行故障排查。

## 默认设置

- 在所有数据相关命令中，优先使用 `--json` 选项以解析结构化输出。
- 在进行数据修改之前，将名称转换为对应的 ID；切勿猜测标识符。
- 对于所有写入操作，必须遵循“读取 → 修改 → 验证”的流程。
- 当需要确保操作结果的确定性时，建议在任务修改时明确指定 `--project PROJECT_ID` 参数。
- 日期字段应使用明确的格式（仅包含日期时使用 `YYYY-MM-DD`，包含时间时使用 ISO 日期格式）。

## 安全性

- 在进行安装或环境更改之前，必须获得用户的明确确认。
- 除非用户明确要求，否则严禁使用可能带来风险的系统安装相关参数。
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