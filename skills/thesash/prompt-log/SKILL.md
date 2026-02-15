---
name: prompt-log
description: **从 AI 编码会话日志中提取对话记录**  
（适用于 Clawdbot、Claude Code、Codex 等工具）  
当需要从 `.jsonl` 格式的会话文件中导出提示历史记录、会话日志或对话记录时，可使用此功能。
---

# 提示日志（Prompt Log）

## 快速入门

在会话文件上运行捆绑的脚本：

```bash
scripts/extract.sh <session-file>
```

## 输入参数

- **会话文件（Session file）**：来自 Clawdbot、Claude Code 或 Codex 的 `.jsonl` 格式会话日志文件。
- **可选过滤条件**：`--after` 和 `--before`：用于指定时间戳范围的参数。
- **可选输出路径（Optional output path）**：用于存放 Markdown 转录本的路径。

## 输出结果

- 生成一个 Markdown 格式的日志文件。默认输出路径为当前项目目录下的 `.prompt-log/YYYY-MM-DD-HHMMSS.md`。

## 示例

```bash
scripts/extract.sh ~/.codex/sessions/2026/01/12/abcdef.jsonl
scripts/extract.sh ~/.claude/projects/my-proj/xyz.jsonl --after "2026-01-12T10:00:00" --before "2026-01-12T12:00:00"
scripts/extract.sh ~/.clawdbot/agents/main/sessions/123.jsonl --output my-transcript.md
```

## 所需依赖项

- 确保 `jq` 已添加到系统的 `PATH` 环境变量中。
- 如果 macOS 上安装了 `gdate`，则会使用 `gdate`；否则将使用 `date` 命令。