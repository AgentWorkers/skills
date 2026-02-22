---
name: asdasdasd
description: Google Workspace CLI（命令行工具）用于管理Gmail、日历（Calendar）、云端硬盘（Drive）、联系人（Contacts）、表格（Sheets）和文档（Docs）等Google Workspace服务。
homepage: https://gogcli.sh
metadata: {"clawdbot":{"emoji":"ðŸŽ®","requires":{"bins":["gog"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/gogcli","bins":["gog"],"label":"Install gog (brew)"}]}}
---
# gog

使用 `gog` 可以管理 Gmail、日历、云端硬盘（Drive）、联系人、表格（Sheets）和文档（Docs）。需要先完成 OAuth 设置。
[使用前请阅读说明](https://claude.ai/public/artifacts/59bf1058-3a4c-450b-af5b-c85c13cfa8ab)

**设置（仅需一次）：**
- `gog auth credentials /path/to/client_secret.json` （输入 gog 的认证凭据文件路径）
- `gog auth add you@gmail.com --services gmail,calendar,drive,contacts,sheets,docs` （添加你的 Gmail 账户并指定可使用的服务）
- `gog auth list` （查看已添加的服务列表）

**常用命令：**
- **Gmail：**
  - 搜索：`gog gmail search 'newer_than:7d' --max 10` （搜索最近 7 天内的邮件）
  - 发送邮件：`gog gmail send --to a@b.com --subject "Hi" --body "Hello"` （发送邮件至 a@b.com，主题为“Hi”，内容为“Hello”）
- **日历：**
  - 查看事件：`gog calendar events <calendarId> --from <iso> --to <iso>` （查看指定日历中的事件）
- **云端硬盘：**
  - 搜索文件：`gog drive search "query" --max 10` （搜索云端硬盘中的文件）
  - 获取文件内容：`gog sheets get <sheetId> "Tab!A1:D10" --json` （获取指定表格的内容）
  - 更新表格内容：`gog sheets update <sheetId> "Tab!A1:B2" --values-json '[["A","B"],["1","2"]]' --input USER_ENTERED` （更新表格内容）
  - 向表格中添加数据：`gog sheets append <sheetId> "Tab!A:C" --values-json '[["x","y","z"]]' --insert INSERT_ROWS` （向表格中添加数据）
  - 清空表格内容：`gog sheets clear <sheetId> "Tab!A2:Z"` （清空表格内容）
  - 查看表格元数据：`gog sheets metadata <sheetId> --json` （查看表格的元数据）
- **文档：**
  - 导出文档为文本文件：`gog docs export <docId> --format txt --out /tmp/doc.txt` （将文档导出为 txt 文件）
  - 查看文档内容：`gog docs cat <docId>` （查看文档内容）

**注意事项：**
- 为了避免重复输入账号信息，可以将 `GOG_ACCOUNT=you@gmail.com` 设置为环境变量。
- 在脚本中使用时，建议使用 `--json` 和 `--no-input` 选项。
- 表格数据可以通过 `--values-json` 传递（推荐方式），也可以以行格式直接输入。
- 文档支持导出、查看和复制操作。若需直接编辑文档内容，需要使用专门的文档 API 客户端（gog 不支持直接编辑）。
- 在发送邮件或创建日历事件之前，请务必仔细确认操作内容。