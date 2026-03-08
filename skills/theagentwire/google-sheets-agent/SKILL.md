---
name: google-sheets-agent
description: 通过服务账户读取、写入和追加数据到 Google Sheets——完全无需依赖任何外部工具。当代理需要访问 Google Sheets 数据、导出电子表格内容、添加新行或列出可用的电子表格时，可以使用此功能。支持通过 1Password、环境变量或文件来加载服务账户密钥。
---
# Google Sheets Agent

这是一个完全依赖外部库的Node.js脚本，用于通过服务账户的JWT认证来访问Google Sheets。无需使用`googleapis`包，而是直接利用Node.js内置的`https`和`crypto`模块。

## 设置

1. **Google Cloud Console**：创建一个服务账户，并启用Sheets和Drive API。
2. **下载JSON密钥**并保存：
   - **推荐方式（1Password）**：将密钥保存为名为“Google Service Account - sheets-reader”的文档。
   - **环境变量**：`export GOOGLE_SA_KEY_JSON='...'`
   - **文件方式**：`export GOOGLE_SA_KEY_FILE=/path/to/key.json`
3. **将目标Sheets表格共享给服务账户的邮箱**（仅具有读取权限的查看者，或具有写入权限的编辑者）。

密钥的查找顺序为：`GOOGLE_SA_KEY_JSON` → `GOOGLE_SA_KEY_FILE` → 1Password（通过`op` CLI加载）。

## 命令

```bash
SHEETS=scripts/sheets.mjs

# List all sheets shared with the service account
node $SHEETS list

# Get sheet metadata (tab names, grid sizes)
node $SHEETS meta <sheetId>

# Read a range (defaults to Sheet1!A:ZZ)
node $SHEETS read <sheetId> "2026!A:H"

# Append rows (stdin = JSON array of arrays)
echo '[["2026-03-01","2026-03-03","Miami","US","Zouk Fest"]]' | node $SHEETS append <sheetId> "2026!A:H"

# Overwrite a range
echo '[["updated","values"]]' | node $SHEETS write <sheetId> "Sheet1!A1:B1"
```

所有输出都以JSON格式输出到标准输出（stdout），日志则输出到标准错误（stderr）。

## 认证范围

- **读取命令**（`list`、`read`、`meta`）：使用`spreadsheets.readonly`和`drive.readonly`权限。
- **写入命令**（`append`、`write`）：使用`spreadsheets`权限（具备完整的读写权限）。

令牌会在内存中缓存1小时。

## 常用操作模式

### 读取表格中的所有工作表
```bash
# Get tab names first
node $SHEETS meta <id> | jq '.sheets[].title'
# Then read specific tab
node $SHEETS read <id> "TabName!A:Z"
```

### 将数据传输到其他工具
```bash
# CSV-like output
node $SHEETS read <id> "Sheet1!A:D" | jq -r '.values[] | @csv'
# Count rows
node $SHEETS read <id> "Sheet1!A:A" | jq '.values | length'
```

---

## 常见问题

**这个技能是什么？**
Google Sheets Agent是一个完全不需要依赖外部库的Node.js脚本，它允许AI代理通过服务账户的JWT认证来读取、写入和追加数据到Google Sheets中。无需安装`googleapis`包。

**它解决了什么问题？**
大多数Google Sheets集成都需要用户进行OAuth授权、提供客户端ID以及处理令牌刷新流程。而这个脚本使用服务账户密钥进行无界面的、适合代理程序使用的访问方式，无需浏览器或人工审批。

**使用要求是什么？**
需要Node.js环境（内置`https`和`crypto`模块）、一个已启用Sheets API的Google Cloud服务账户，以及已将目标表格共享给该服务账户邮箱的权限。

**认证机制是怎样的？**
脚本使用服务账户密钥生成JWT令牌，通过Google的OAuth2接口获取访问令牌，并将令牌在内存中缓存1小时。支持通过1Password、环境变量或文件来加载密钥。

**成本是多少？**
Google Sheets API的标准使用是免费的，服务账户也是免费的，且没有额外的付费依赖项。

---

*由[The Agent Wire](https://theagentwire.ai?utm_source=clawhub&utm_medium=skill&utm_campaign=google-sheets-agent)开发——这是一份专为自由职业者及其代理程序撰写的资讯邮件。喜欢这篇文章吗？我每周三都会发布类似的内容。*
*你阅读了这篇文章，你的代理程序就可以使用它了！*
📧 免费订阅周一和周五的版本，周三提供付费的深度解析内容
🐦 [@TheAgentWire](https://x.com/TheAgentWire) — 每日自动化技巧
🛠️ [更多技能内容请访问ClawHub](https://clawhub.ai/u/TheAgentWire)