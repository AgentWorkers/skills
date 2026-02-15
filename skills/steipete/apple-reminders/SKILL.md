---
name: apple-reminders
description: 在 macOS 上，可以通过 `remindctl` CLI 命令行工具来管理 Apple 提醒事项（包括列出、添加、编辑、完成和删除提醒事项）。该工具支持列表显示、日期过滤功能，并支持 JSON 或纯文本格式的输出结果。
homepage: https://github.com/steipete/remindctl
metadata: {"clawdbot":{"emoji":"⏰","os":["darwin"],"requires":{"bins":["remindctl"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/remindctl","bins":["remindctl"],"label":"Install remindctl via Homebrew"}]}}
---

# Apple Reminders CLI (remindctl)

使用 `remindctl` 可以直接从终端管理 Apple Reminders。它支持列表过滤、基于日期的视图以及脚本输出功能。

## 安装
- 通过 Homebrew 安装：`brew install steipete/tap/remindctl`
- 从源代码安装：`pnpm install && pnpm build`（生成的二进制文件位于 `./bin/remindctl`）
- 仅适用于 macOS；系统提示时需要授予 Reminders 应用程序相应的权限。

## 权限管理
- 检查状态：`remindctl status`
- 请求访问权限：`remindctl authorize`

## 查看提醒
- 默认视图（今日）：`remindctl`
- 今日的提醒：`remindctl today`
- 明天的提醒：`remindctl tomorrow`
- 本周的提醒：`remindctl week`
- 过期的提醒：`remindctl overdue`
- 即将到期的提醒：`remindctl upcoming`
- 已完成的提醒：`remindctl completed`
- 所有提醒：`remindctl all`
- 指定日期的提醒：`remindctl 2026-01-04`

## 管理提醒列表
- 列出所有列表：`remindctl list`
- 显示特定列表：`remindctl list Work`（例如：列出名为 “Work” 的列表）
- 创建新列表：`remindctl list Projects --create`
- 重命名列表：`remindctl list Work --rename Office`
- 删除列表：`remindctl list Work --delete`

## 创建提醒
- 快速创建提醒：`remindctl add "Buy milk"`
- 为特定列表创建提醒并设置到期时间：`remindctl add --title "Call mom" --list Personal --due tomorrow`

## 编辑提醒
- 修改提醒的标题或到期时间：`remindctl edit 1 --title "New title" --due 2026-01-04`

## 完成提醒
- 根据 ID 完成提醒：`remindctl complete 1 2 3`

## 删除提醒
- 根据 ID 删除提醒：`remindctl delete 4A83 --force`

## 输出格式
- JSON 格式（适用于脚本）：`remindctl today --json`
- 简单的 TSV 格式：`remindctl today --plain`
- 仅显示数量：`remindctl today --quiet`

## 日期格式
`--due` 和日期过滤选项支持的格式包括：
- `today`, `tomorrow`, `yesterday`
- `YYYY-MM-DD`
- `YYYY-MM-DD HH:mm`
- ISO 8601 格式（例如：`2026-01-04T12:34:56Z`

## 注意事项
- 仅适用于 macOS。
- 如果访问权限被拒绝，请在系统设置 → 隐私与安全 → Reminders 中启用 Terminal 和 remindctl 的访问权限。
- 如果通过 SSH 远程执行命令，请确保目标 Mac 上已授予相应的访问权限。