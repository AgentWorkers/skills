---
name: google-workspace
description: Google Workspace 命令行工具（CLI）：用于管理 Gmail、日历、云端硬盘（Drive）、联系人、表格（Sheets）和文档（Docs）。
homepage: https://gogcli.sh
metadata: {"clawdbot":{"emoji":"🎮","requires":{"bins":["gog"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/gogcli","bins":["gog"],"label":"Install gog (brew)"}]}}
---

# gog

使用 `gog` 可以管理 Gmail、日历、云端硬盘（Drive）、联系人、表格（Sheets）和文档（Docs）等 Google 服务。需要先完成 OAuth 设置。

**设置（只需一次）：**
- `gog auth credentials /path/to/client_secret.json` （输入 OAuth 密钥文件路径）
- `gog auth add you@gmail.com --services gmail,calendar,drive,contacts,sheets,docs` （添加用户账号及所需服务）
- `gog auth list` （查看已授权的服务列表）

**常用命令：**
- **Gmail：**
  - 搜索邮件：`gog gmail search 'newer_than:7d' --max 10` （搜索发送时间在 7 天内的邮件，最多显示 10 条）
  - 发送邮件：`gog gmail send --to a@b.com --subject "Hi" --body "Hello"` （发送邮件至 a@b.com，主题为“Hi”，内容为“Hello”）
- **日历：**
  - 查看事件：`gog calendar events <calendarId> --from <iso> --to <iso>` （查看指定日历中的事件）
- **云端硬盘：**
  - 搜索文件：`gog drive search "query" --max 10` （搜索云端硬盘中的文件）
- **联系人：**
  - 查看联系人列表：`gog contacts list --max 20` （查看联系人列表）
- **表格：**
    - 获取数据：`gog sheets get <sheetId> "Tab!A1:D10" --json` （获取表格 <sheetId> 中 A1 到 D10 单元格的数据）
    - 更新数据：`gog sheets update <sheetId> "Tab!A1:B2" --values-json '[["A","B"],["1","2"]]' --input USER_ENTERED` （更新表格 <sheetId> 中 A1 到 B2 单元格的数据）
    - 添加数据：`gog sheets append <sheetId> "Tab!A:C" --values-json '[["x","y","z"]]' --insert INSERT_ROWS` （在表格 <sheetId> 的指定位置添加数据）
    - 清空表格：`gog sheets clear <sheetId> "Tab!A2:Z"` （清除表格 <sheetId> 的内容）
    - 查看表格元数据：`gog sheets metadata <sheetId> --json` （查看表格元数据）
    - 导出文档：`gog docs export <docId> --format txt --out /tmp/doc.txt` （将文档 <docId> 导出为 txt 格式）
    - 查看文档内容：`gog docs cat <docId>` （查看文档 <docId> 的内容）

**注意事项：**
- 为避免重复输入账号信息，建议将 `GOG_ACCOUNT` 设置为 `you@gmail.com`。
- 在脚本中使用 `--json` 和 `--no-input` 选项可简化参数传递。
- 表格数据可以通过 `--values-json` 传递（推荐方式），也可以以行格式直接输入。
- 文档支持导出、查看和复制功能；直接编辑文档需要使用专门的 Docs API 客户端（gog 不支持）。
- 在发送邮件或创建事件之前，请务必确认操作内容。