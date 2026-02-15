---
name: google-sheets
description: 通过 Google Sheets API（Node.js SDK）来读取、写入、追加数据以及管理 Google Sheets 文档。当您需要与电子表格进行交互时（例如读取数据、写入/更新单元格内容、追加新行、清除数据范围、格式化单元格或管理整个工作表），可以使用该 SDK。使用前，请确保您拥有已启用 Sheets API 的 Google Cloud 服务账户。
---

# Google Sheets 技能

使用服务账户与 Google Sheets 进行交互。

## 设置（一次性操作）

1. **Google Cloud 控制台：**
   - 创建或选择一个项目
   - 启用“Google Sheets API”
   - 创建一个服务账户（IAM → 服务账户 → 创建）
   - 下载 JSON 密钥

2. **配置凭据**（选择以下其中一种方式）：
   - 设置环境变量：`GOOGLE_SERVICE ACCOUNT_KEY=/path/to/key.json`
   - 将 `service-account.json` 或 `credentials.json` 文件放入技能目录中
   - 将文件放入 `~/.config/google-sheets/credentials.json`

3. **使用服务账户的电子邮件地址（在 JSON 密钥中标记为 `client_email`）共享工作表**

4. **安装依赖项：**
   ```bash
   cd skills/google-sheets && npm install
   ```

## 使用方法

```bash
node scripts/sheets.js <command> [args]
```

## 命令

### 数据操作

| 命令 | 参数 | 描述 |
|---------|------|-------------|
| `read` | `<id> <range>` | 读取指定范围内的单元格数据 |
| `write` | `<id> <range> <json>` | 向指定范围内的单元格写入数据 |
| `append` | `<id> <range> <json>` | 向指定范围内追加行 |
| `clear` | `<id> <range>` | 清空指定范围内的单元格 |

### 格式设置

| 命令 | 参数 | 描述 |
|---------|------|-------------|
| `format` | `<id> <range> <formatJson>` | 格式化指定范围内的单元格 |
| `getFormat` | `<id> <range>` | 获取指定范围内单元格的格式 |
| `borders` | `<id> <range> [styleJson]` | 为指定范围内的单元格添加边框 |
| `copyFormat` | `<id> <source> <dest>` | 将格式从指定范围复制到另一个范围 |
| `merge` | `<id> <range>` | 合并指定范围内的单元格 |
| `unmerge` | `<id> <range>` | 分开指定范围内的单元格 |

### 布局设置

| 命令 | 参数 | 描述 |
|---------|------|-------------|
| `resize` | `<id> <sheet> <cols\|rows> <start> <end> <px>` | 调整工作表的列/行大小 |
| `autoResize` | `<id> <sheet> <startCol> <endCol>` | 自动调整列的宽度 |
| `freeze` | `<id> <sheet> [rows] [cols]` | 冻结指定范围内的行/列 |

### 工作表管理

| 命令 | 参数 | 描述 |
|---------|------|-------------|
| `create` | `<title>` | 创建新的电子表格 |
| `info` | `<id>` | 获取工作表的元数据 |
| `addSheet` | `<id> <title>` | 添加新的工作表标签 |
| `deleteSheet` | `<id> <sheetName>` | 删除指定的工作表标签 |
| `renameSheet` | `<id> <oldName> <newName>` | 重命名工作表标签 |

## 示例

```bash
# Read data
node scripts/sheets.js read "SPREADSHEET_ID" "Sheet1!A1:C10"

# Write data
node scripts/sheets.js write "SPREADSHEET_ID" "Sheet1!A1:B2" '[["Name","Score"],["Alice",95]]'

# Format cells (yellow bg, bold)
node scripts/sheets.js format "SPREADSHEET_ID" "Sheet1!A1:B2" '{"backgroundColor":{"red":255,"green":255,"blue":0},"textFormat":{"bold":true}}'

# Copy format from one range to another
node scripts/sheets.js copyFormat "SPREADSHEET_ID" "Sheet1!A1:C3" "Sheet1!D1:F3"

# Add borders
node scripts/sheets.js borders "SPREADSHEET_ID" "Sheet1!A1:C3"

# Resize columns to 150px
node scripts/sheets.js resize "SPREADSHEET_ID" "Sheet1" cols A C 150

# Auto-fit column widths
node scripts/sheets.js autoResize "SPREADSHEET_ID" "Sheet1" A Z

# Freeze first row and column
node scripts/sheets.js freeze "SPREADSHEET_ID" "Sheet1" 1 1

# Add new sheet tab
node scripts/sheets.js addSheet "SPREADSHEET_ID" "NewSheet"
```

## 格式选项

```json
{
  "backgroundColor": {"red": 255, "green": 255, "blue": 0},
  "textFormat": {
    "bold": true,
    "italic": false,
    "fontSize": 12,
    "foregroundColor": {"red": 0, "green": 0, "blue": 0}
  },
  "horizontalAlignment": "CENTER",
  "verticalAlignment": "MIDDLE",
  "wrapStrategy": "WRAP"
}
```

## 边框样式

边框样式：点线（DOTTED）、虚线（DASHED）、实线（SOLID）、粗实线（SOLID_THICK）、双线（DOUBLE）

## 查找电子表格 ID

通过以下 URL 获取：`https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`

## 故障排除

- **403 Forbidden**：工作表未与服务账户的电子邮件地址共享
- **404 Not Found**：提供的电子表格 ID 或工作表名称错误