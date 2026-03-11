---
name: gog
description: Google Workspace CLI（命令行工具）用于管理Gmail、日历（Calendar）、云端硬盘（Drive）、联系人（Contacts）、表格（Sheets）和文档（Docs）。
homepage: https://gogcli.sh
metadata: {"clawdbot":{"emoji":"🎮","requires":{"bins":["gog"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/gogcli","bins":["gog"],"label":"Install gog (brew)"}]}}
---

# gog

使用 `gog` 可以管理 Gmail、日历、云端硬盘（Drive）、联系人、表格（Sheets）和文档（Docs）。需要先进行 OAuth 设置。

**设置（只需一次）：**
- `gog auth credentials /path/to/client_secret.json` （输入 gog 的认证凭据文件路径）
- `gog auth add you@gmail.com --services gmail,calendar,drive,contacts,sheets,docs` （添加用户 `you@gmail.com` 并配置其使用的服务）
- `gog auth list` （查看已配置的服务列表）

**常用命令：**
- **Gmail：**
  - `gog gmail search 'newer_than:7d' --max 10` （在 Gmail 中搜索创建于 7 天内的邮件，最多显示 10 条）
  - `gog gmail send --to a@b.com --subject "Hi" --body "Hello"` （发送邮件至 `a@b.com`，主题为“Hi”，内容为“Hello”）
- **日历：**
  - `gog calendar events <calendarId> --from <iso> --to <iso>` （查询指定日历中的事件）
- **云端硬盘：**
  - `gog drive search "query" --max 10` （在云端硬盘中搜索内容，最多显示 10 条结果）
- **联系人：**
  - `gog contacts list --max 20` （列出所有联系人）
- **表格：**
    - `gog sheets get <sheetId> "Tab!A1:D10" --json` （获取表格 `<sheetId>` 中从 A1 到 D10 单元格的内容，以 JSON 格式）
    - `gog sheets update <sheetId> "Tab!A1:B2" --values-json '[["A","B"],["1","2"]]' --input USER_ENTERED` （更新表格 `<sheetId>` 中 A1 单元格的值为 ["A", "B"]，B 单元格的值为 [1, 2]）
    - `gog sheets append <sheetId> "Tab!A:C" --values-json '[["x","y","z"]]' --insert INSERT_ROWS` （在表格 `<sheetId>` 的 C 单元格后插入新行）
    - `gog sheets clear <sheetId> "Tab!A2:Z"` （清除表格 `<sheetId>` 中从 A2 到 Z 的所有内容）
    - `gog sheets metadata <sheetId> --json` （获取表格 `<sheetId>` 的元数据）
    - `gog docs export <docId> --format txt --out /tmp/doc.txt` （将文档 `<docId>` 导出为文本文件）
    - `gog docs cat <docId>` （查看文档 `<docId>` 的内容）
- **文档：**
    - `gog docs export <docId> --format txt --out /tmp/doc.txt` （将文档 `<docId>` 导出为文本文件）
    - `gog docs cat <docId>` （查看文档 `<docId>` 的内容）

**注意事项：**
- 为了避免重复输入 `--account`，建议将 `GOG_ACCOUNT` 环境变量设置为 `you@gmail.com`。
- 在脚本中使用 `--json` 和 `--no-input` 选项可以简化参数传递。
- 表格的数据可以通过 `--values-json` 传递（推荐方式），也可以以行格式直接输入。
- 文档支持导出、查看和复制操作；直接编辑文档需要使用专门的文档 API 客户端（gog 不支持该功能）。
- 在发送邮件或创建日历事件之前，请务必确认操作内容。