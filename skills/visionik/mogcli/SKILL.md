---
name: mog
description: Microsoft Ops Gadget — 用于 Microsoft 365（邮件、日历、驱动器、联系人、任务、Word、PowerPoint、Excel、OneNote）的命令行界面（CLI）。
---

# mog — Microsoft Ops Gadget

这是一个用于管理 Microsoft 365 服务的命令行工具（CLI），支持 Mail、Calendar、OneDrive、Contacts、Tasks、Word、PowerPoint、Excel 和 OneNote 等服务。

它是 `gog`（Google Ops Gadget）的 Microsoft 对应版本，使用相同的操作模式，但针对不同的云服务。

## 快速参考

如需详细使用说明，请运行：
```bash
mog --ai-help
```

该命令会输出符合 dashdash 格式的完整文档，内容包括：
- 安装/前置要求
- 所有命令及选项
- 日期/时间格式
- 使用示例
- 故障排除方法
- 关于 Slug 系统的说明
- 与 `gog` 的兼容性说明

## 模块

| 模块 | 命令        |
|--------|------------|
| **mail**  | search、get、send、folders、drafts、attachment |
| **calendar** | list、create、get、update、delete、calendars、respond、freebusy、acl |
| **drive** | ls、search、download、upload、mkdir、move、rename、copy、rm |
| **contacts** | list、search、get、create、update、delete、directory |
| **tasks** | list、add、done、undo、delete、clear |
| **word**  | list、export、copy |
| **ppt**  | list、export、copy |
| **excel** | list、get、update、append、create、metadata、tables、add-sheet、clear、copy、export |
| **onenote** | notebooks、sections、pages、get、create-notebook、create-section、create-page、delete、search |

## 快速入门

```bash
# Mail
mog mail search "from:someone" --max 10
mog mail send --to a@b.com --subject "Hi" --body "Hello"
mog mail send --to a@b.com --subject "Report" --body-file report.md
mog mail send --to a@b.com --subject "Newsletter" --body-html "<h1>Hello</h1>"
cat draft.txt | mog mail send --to a@b.com --subject "Hi" --body-file -

# Calendar
mog calendar list
mog calendar create --summary "Meeting" --from 2025-01-15T10:00:00 --to 2025-01-15T11:00:00
mog calendar freebusy alice@example.com bob@example.com

# Drive
mog drive ls
mog drive upload ./file.pdf
mog drive download <slug> --out ./file.pdf

# Tasks
mog tasks list
mog tasks add "Buy milk" --due tomorrow
mog tasks clear

# Contacts
mog contacts list
mog contacts directory "john"

# Excel
mog excel list
mog excel get <id> Sheet1 A1:D10
mog excel update <id> Sheet1 A1:B2 val1 val2 val3 val4
mog excel append <id> TableName col1 col2 col3

# OneNote
mog onenote notebooks
mog onenote search "meeting notes"
```

## Slug 生成

mog 会为 Microsoft 的长 GUID 生成 8 个字符的 Slug：
- 例如：`a3f2c891`（而非 `AQMkADAwATMzAGZmAS04MDViLTRiNzgt...`）
- 所有命令都支持使用 Slug 或完整的 GUID 格式
- 使用 `--verbose` 选项可查看完整的 GUID

## 别名

- `mog cal` → `mog calendar`（用于调用 calendar 模块）
- `mog todo` → `mog tasks`（用于调用 tasks 模块）

## 凭据存储

OAuth 令牌存储在配置目录中（权限设置为 0600）：

| 平台 | 存储位置       |
|--------|--------------|
| **macOS** | `~/.config/mog/`     |
| **Linux** | `~/.config/mog/`     |
| **Windows** | `%USERPROFILE%\.config\mog\` |

配置文件包括：
- `tokens.json`：OAuth 令牌（由操作系统加密存储）
- `settings.json`：客户端 ID
- `slugs.json`：Slug 缓存文件

## 相关文档

- `mog --ai-help`：查看完整文档
- `mog <command> --help`：查看特定命令的帮助信息