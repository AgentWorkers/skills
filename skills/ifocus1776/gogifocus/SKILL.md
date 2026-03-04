---
name: gogifocus
description: Google Workspace 命令行工具（CLI）：用于管理 Gmail、日历、云端硬盘（Drive）、联系人、表格（Sheets）和文档（Docs）。
homepage: https://gogcli.sh
metadata: {"clawdbot":{"emoji":"🎮","requires":{"bins":["gog"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/gogcli","bins":["gog"],"label":"Install gog (brew)"}]}}
---
# gog

使用 `gog` 可以管理 Gmail、日历、云端硬盘（Drive）、联系人、表格（Sheets）和文档（Docs）。需要先进行 OAuth 设置。

**设置（只需一次）：**
- `gog auth credentials /path/to/client_secret.json` （输入 OAuth 密钥文件路径）
- `gog auth add you@gmail.com --services gmail,calendar,drive,contacts,sheets,docs` （添加用户账号及服务）
- `gog auth list` （查看已授权的服务）

**常用命令：**
- **Gmail：**
  - `gog gmail search 'newer_than:7d' --max 10` （搜索最近 7 天内的邮件）
  - `gog gmail send --to a@b.com --subject "Hi" --body "Hello"` （发送邮件至 a@b.com）
- **日历：**
  - `gog calendar events <calendarId> --from <iso> --to <iso>` （查询日历事件）
- **云端硬盘：**
  - `gog drive search "query" --max 10` （搜索云端硬盘中的文件）
- **联系人：**
  - `gog contacts list --max 20` （列出联系人信息）
- **表格：**
  - `gog sheets get <sheetId> "Tab!A1:D10" --json` （获取表格数据）
  - `gog sheets update <sheetId> "Tab!A1:B2" --values-json '[["A","B"],["1","2"]]' --input USER_ENTERED` （更新表格内容）
  - `gog sheets append <sheetId> "Tab!A:C" --values-json '[["x","y","z"]]' --insert INSERT_ROWS` （向表格中添加数据）
  - `gog sheets clear <sheetId> "Tab!A2:Z"` （清除表格内容）
  - `gog sheets metadata <sheetId> --json` （查询表格元数据）
  - `gog docs export <docId> --format txt --out /tmp/doc.txt` （导出文档为文本文件）
  - `gog docs cat <docId>` （查看文档内容）

**注意事项：**
- 将 `GOG_ACCOUNT=you@gmail.com` 设置为默认账号，以避免每次使用时重复输入 `--account` 参数。
- 在脚本中使用 `--json` 和 `--no-input` 可简化参数传递。
- 表格数据可通过 `--values-json` 传递（推荐方式），也可以行格式直接输入。
- 文档支持导出、查看和复制操作；直接编辑文档需要使用专门的 Docs API 客户端（gog 不支持）。
- 在发送邮件或创建日历事件前，请务必确认操作内容。