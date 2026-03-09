---
name: cursor-agent
description: 运行 Cursor Agent CLI 来执行编码任务（如编写、编辑、重构、审查或规划代码），无需消耗 OpenClaw API 信用点数。适用于以下情况：用户要求编写/修复/重构/审查代码；编码任务原本需要通过 Sonnet/Haiku 来完成，但用户明确要求使用 Cursor Agent；或者在已知仓库中执行大量文件编辑操作。**不适用于**关于代码的简单问答（可立即回答）或无需使用子进程的简短命令。
metadata:
  requiredBinaries: ["agent"]
---
# Cursor Agent

Cursor Agent CLI 在用户的 Cursor 订阅服务上运行，无需支付任何 API 费用。对于任何非简单的编码任务，始终建议使用它而不是内联代码生成方式。

## 先决条件

**必需的二进制文件：`agent`**（Cursor Agent CLI）

请从官方网站安装：https://cursor.com/docs/cli/overview，然后使用 `agent --version` 进行验证。如果 `agent` 未出现在 PATH 环境变量中，辅助脚本（`scripts/run.sh`）会输出错误信息并终止执行。

## 需要用户同意 — 强制性要求

此功能严禁自动执行。每次执行前必须：

1. **先明确用户意图** — 告知用户相关信息：仓库地址、任务内容、使用的模型以及是否会对文件进行修改。
2. **等待用户的明确许可** — 未经用户明确同意，不得继续执行操作。
3. **默认设置为只读模式** — 使用 `run.sh <repo> <task> <model> ask` 命令；除非用户明确要求进行修改。
4. **在写入文件之前** — 先以“询问”（`ask`）模式运行脚本，向用户展示修改计划，然后询问用户是否同意应用这些修改。
5. **在执行 `--cloud` 命令之前** — 明确警告用户：“此操作会将仓库内容发送到 cursor.com。是否继续？”
6. **在提交更改之前** — 显示文件差异并获取用户的确认。

辅助脚本（`scripts/run.sh`）默认使用“询问”（只读）模式。只有在用户确认同意应用更改后，才能将模式参数设置为“写入”（`write`）。

## 模型选择

| 任务类型 | 使用的模型 | 模式标志 |
|---|---|---|
| 简单/探索性任务 | 无需指定模型 | 无需设置模式标志 |
| 修复漏洞/添加功能/重构代码 | `--model sonnet-4.6` |
| 代码审查/仅读取数据 | `--model sonnet-4.6` | `--mode=ask` |
| 架构设计规划 | `--model opus-4.6-thinking` | `--mode=plan` |
| 长期后台任务 | `--model sonnet-4.6` | 应使用 `--cloud` 而不是 `-p` |

## 无界面操作命令

**始终以“询问”模式开始** — 在应用更改之前，先进行审查：
```bash
cd <repo> && agent -p "<task>" --model sonnet-4.6 --mode=ask --output-format text --trust
```

**应用更改** — 仅在用户确认修改计划后执行：
```bash
cd <repo> && agent -p "<task>" --model sonnet-4.6 --force --output-format text --trust
```

**云存储/后台任务** — 在执行前警告用户：仓库数据将被上传至 cursor.com：
```bash
cd <repo> && agent -c "<task>" --model sonnet-4.6 --trust
# Monitor at: cursor.com/agents
```

## Git 使用规则

Cursor 沙箱环境会阻止 `git commit` 操作。在完成 Cursor 的编辑后，必须手动执行 `git commit`：
```bash
cd <repo> && git add -A && git commit -m "<conventional commit message>" && git push
```

如果更改内容较多或涉及敏感区域，在提交之前务必向用户展示文件差异并获取确认。

## 仓库与工作目录

- 运行脚本前，请确保切换到正确的仓库目录。
- 检查仓库根目录下是否存在 `.cursor/rules` 和 `AGENTS.md` 文件 — Cursor 会自动加载这些文件以获取项目上下文信息。

## 上下文与会话管理

- 在命令提示符中添加 `@<file>` 以指定需要包含在上下文中的特定文件。
- 使用 `--continue` 或 `--resume` 命令继续之前的会话。
- 使用 `agent ls` 命令查看之前的会话记录。

## 输出处理

- `--output-format text` → 以简洁的文本形式输出结果，向用户总结主要更改内容。
- `--output-format json` → 以结构化格式输出结果，适用于脚本解析。
- 必须向用户报告所有更改内容、已提交的变更以及可能存在的问题。

## 参考资料

- 模型列表及详细信息：`references/models.md`
- 交互式命令指南：`references/slash-commands.md`