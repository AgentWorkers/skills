---
name: google-sheet-api
description: **OpenClaw 技能：安装 Google Sheets 命令行工具（CLI）**  
该技能提供了安装 Google Sheets 命令行工具（CLI）的详细步骤及相关命令，支持读写数据、批量操作、格式化表格以及管理 Sheets 文件的功能。  

**安装步骤：**  
1. 访问 [OpenClaw 官方网站](https://openclaw.org/) 并下载适用于您的操作系统的安装包。  
2. 按照安装程序的指示完成安装。  
3. 安装完成后，您可以在命令行中通过 `openclaw-cli` 命令访问 Google Sheets CLI。  

**常用命令：**  
- `openclaw-cli list-sheets`：列出所有可操作的 Sheets 文件。  
- `openclaw-cli read-sheet <sheet-id>`：读取指定 Sheets 文件的内容。  
- `openclaw-cli write-sheet <sheet-id> <data>`：将数据写入指定 Sheets 文件。  
- `openclaw-cli batch-read-sheets <sheet-ids>`：批量读取多个 Sheets 文件的内容。  
- `openclaw-cli batch-write-sheets <sheet-ids> <data>`：批量将数据写入多个 Sheets 文件。  
- `openclaw-cli format-sheet <sheet-id>`：格式化指定 Sheets 文件。  
- `openclaw-cli delete-sheet <sheet-id>`：删除指定 Sheets 文件。  

**示例：**  
1. **读取单个 Sheets 文件内容：**  
   ```
   openclaw-cli read-sheet SPreadsheet1
   ```
2. **写入数据到 Sheets 文件：**  
   ```
   openclaw-cli write-sheet SPreadsheet1 "Hello, World!"
   ```
3. **批量读取多个 Sheets 文件的内容：**  
   ```
   openclaw-cli batch-read-sheets SPreadsheet1 SPreadsheet2 SPreadsheet3
   ```
4. **批量将数据写入多个 Sheets 文件：**  
   ```
   openclaw-cli batch-write-sheets SPreadsheet1 "New Data" SPreadsheet2 "New Data"
   ```
5. **格式化 Sheets 文件：**  
   ```
   openclaw-cli format-sheet SPreadsheet1
   ```
6. **删除 Sheets 文件：**  
   ```
   openclaw-cli delete-sheet SPreadsheet1
   ```
---

# Google Sheets API 技能（高级版）

## 目的  
为 OpenClaw 提供一个可用于生产环境的 Google Sheets 命令行工具（CLI）。该工具支持数据读写、批量操作、格式化以及使用服务账户进行工作表管理。

## 适用场景  
- 需要一个可重复使用的 CLI 来执行自动化任务。  
- 希望数据交换采用 JSON 格式（输入/输出）。  
- 需要执行比基本读写操作更高级的功能（如格式化、工作表操作、批量更新）。

## 不适用场景  
- 不能使用终端用户的 OAuth 认证流程（本技能仅支持服务账户认证）。  
- 仅需要简单的、一次性编辑操作。

## 一次性设置步骤  
1. 创建或选择一个 Google Cloud 项目。  
2. 启用 Google Sheets API。  
3. 创建一个服务账户并下载其 JSON 密钥。  
4. 将目标工作表共享给该服务账户的邮箱地址。

## 安装  
```bash
cd google-sheet-api
npm install
```

## 运行  
```bash
node scripts/sheets-cli.js help
node scripts/sheets-cli.js read <spreadsheetId> "Sheet1!A1:C10"
node scripts/sheets-cli.js append <spreadsheetId> "Sheet1!A:B" '@data.json'
```

您也可以使用 npm 来安装该工具：  
```bash
npm run sheets -- read <spreadsheetId> "Sheet1!A1:C10"
```

## 凭据配置  
支持的凭证来源（优先选择第一个匹配项）：  
- `GOOGLE_SHEETS_CREDENTIALS_JSON`（内联 JSON 字符串）  
- `GOOGLE_SERVICE_ACCOUNT_KEY`（文件路径）  
- `GOOGLE_SHEETS_KEY_FILE`（文件路径）  
- `GOOGLE_APPLICATION_CREDENTIALS`（文件路径）  
- `./service-account.json`、`./credentials.json`、`./google-service-account.json`  
- `~/.config/google-sheets/credentials.json`  

## 输入格式  
- JSON 数据可以内联提供，也可以通过 `@path` 从文件中加载。  
- 写入或追加数据时，输入应为二维数组格式。  
示例 `data.json` 文件内容：  
```json
[["Name","Score"],["Alice",95]]
```

## 命令列表（高级功能）  
- 数据操作：`read`、`write`、`append`、`clear`、`batchGet`、`batchWrite`  
- 格式化操作：`format`、`getFormat`、`borders`、`merge`、`unmerge`、`copyFormat`  
- 布局调整：`resize`、`autoResize`、`freeze`  
- 工作表操作：`create`、`info`、`addSheet`、`deleteSheet`、`renameSheet`  
- 高级功能：`batch`（通过 `spreadsheets.batchUpdate` 请求进行批量操作）  

## 运行指南  
- 在可能的情况下，建议使用只读权限来执行数据读取操作。  
- 对于 429 错误和暂时性的 5xx 错误，应采用指数级退避策略进行重试。  
- 为避免请求限制，请确保请求数据量较小。  

## 预期输出  
- 成功操作时，输出结果以 JSON 格式显示到标准输出（stdout）；遇到错误时，程序会返回非零退出码。  

## 安全注意事项  
- 严禁记录或提交服务账户的密钥信息。  
- 仅将目标工作表共享给该技能所需的服务账户邮箱地址。