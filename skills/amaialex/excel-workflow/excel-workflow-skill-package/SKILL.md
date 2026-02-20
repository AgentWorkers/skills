---
name: excel-workflow
description: >
  完整的 Excel 工作流程：包括本地文件处理、与 Google Drive 的同步以及公式的保留。  
  该流程支持处理 Excel 文件（.xlsx 格式），在 SQLite 数据库中记录文件修改历史，并在文件更新时保持公式原有的计算结果。  
  当用户需要上传 Excel 文件、查询数据、更新单元格内容同时保留公式，或与 Google Drive 同步数据时，可使用此功能。
compatibility: Requires Python 3.8+, openpyxl, rclone, and Google Drive OAuth setup
metadata:
  author: alexey
  version: "1.0.0"
  openclaw:
    emoji: 🔄
    requires:
      bins:
        - rclone
        - python3
      env:
        - OPENCLAW_EXCEL_PATH
---
# Excel 工作流程

这是一个完整的 Excel 文件管理工作流程，支持本地处理、Google Drive 备份、公式保留以及 SQLite 数据跟踪功能。

## 主要特性

- ✅ **公式保留** — 在更新单元格时不会丢失公式（由 openpyxl 提供支持）
- ✅ **Google Drive 同步** — 使用 rclone 自动将文件备份到 Google Drive
- ✅ **SQLite 数据跟踪** — 在本地数据库中记录所有文件、公式和元数据
- ✅ **多文件支持** — 可同时处理多个 Excel 文件
- ✅ **数据分析** — 可查询数据、读取公式并分析文件结构
- ✅ **批量操作** — 可一次性为整列创建公式

## 快速入门

### 1. 上传 Excel 文件

只需将 `.xlsx` 文件放入聊天窗口中，工作流程会自动执行以下操作：
1. 分析文件结构（工作表和公式）
2. 将文件上传到 Google Drive（路径：`gdrive:Excel/`)
3. 将元数据保存到 SQLite 数据库中

```bash
# Manual processing
~/.openclaw/tools/openclaw-excel/excel-workflow process /path/to/file.xlsx
```

### 2. 查询数据

```bash
# Ask questions about your data
~/.openclaw/tools/openclaw-excel/excel-workflow query "what is total revenue?" --file sales.xlsx
```

### 3. 更新单元格（公式保留！）

```bash
# Update values - formulas stay intact
~/.openclaw/tools/openclaw-excel/excel-workflow update '{"C2": 100}' --file sales.xlsx

# Update formulas
~/.openclaw/tools/openclaw-excel/excel-workflow update '{"D2": "=B2*C2*1.5"}' --file sales.xlsx
```

## 安装

### 先决条件

- **Python 3.8+** 及 openpyxl 库
- **rclone**（用于与 Google Drive 集成）
- **Google Drive** 账户

### 第一步：安装依赖项

```bash
# Install rclone (macOS)
brew install rclone

# Python packages (installed in venv automatically)
pip install openpyxl
```

### 第二步：配置 Google Drive

```bash
# Configure rclone with Google Drive
rclone config
```

按照提示操作：
- 名称：`gdrive`
- 存储位置：`drive`（Google Drive）
- 访问权限：`1`（全权限）
- 是否自动配置 OAuth：`y`（会自动打开浏览器进行授权）

验证配置是否成功：
```bash
rclone lsd gdrive:
```

### 第三步：创建 Excel 文件文件夹

```bash
rclone mkdir gdrive:Excel/
```

### 第四步：安装相关工具文件

该工具包含三个主要组件：

1. **Excel 命令行工具**（`~/.openclaw/tools/openclaw-excel/excel`）
   - 命令：`info`、`read`、`update`、`show-formulas`、`get-cell`

2. **数据跟踪工具**（`~/.openclaw/tools/openclaw-excel/excel-tracker`）
   - 使用 SQLite 数据库（文件路径：`~/.openclaw/excel_tracker.db`）
   - 命令：`add`、`get-latest`、`search`、`list`、`stats`

3. **工作流程协调器**（`~/.openclaw/tools/openclaw-excel/excel-workflow`）
   - 命令：`process`、`query`、`update`、`list`、`stats`

详细安装指南请参阅 [安装指南](https://github.com/your-repo/excel-workflow)。

## 命令说明

### process 命令

分析文件内容，将其上传到 Google Drive，并将相关信息保存到数据库中：

```bash
excel-workflow process /path/to/file.xlsx [--telegram-id ID]
```

**输出结果：**
```json
{
  "status": "success",
  "filename": "sales.xlsx",
  "file_id": 1,
  "drive_url": "gdrive:Excel/sales.xlsx",
  "analysis": {
    "sheets": 2,
    "formulas": 15,
    "sheet_names": ["Sales", "Summary"]
  },
  "message": "✅ File processed successfully!"
}
```

### query 命令

用于读取数据并回答问题：

```bash
excel-workflow query "show me the data" [--file filename.xlsx]
```

**输出结果：**
```json
{
  "filename": "sales.xlsx",
  "file_id": 1,
  "sheets": ["Sales", "Summary"],
  "data": [
    [
      {"address": "A1", "value": "Product", "type": "str"},
      {"address": "B1", "value": "Price", "type": "int"}
    ]
  ],
  "formulas": [
    {"cell": "D2", "formula": "=B2*C2"}
  ],
  "question": "show me the data",
  "context": {
    "sheet_count": 2,
    "formula_count": 15,
    "uploaded_at": "2026-02-20 10:30:00"
  }
}
```

### update 命令

更新单元格内容（包括数值和公式）：

```bash
# Update values
excel-workflow update '{"C2": 100, "C3": 200}' [--file filename.xlsx]

# Update formulas
excel-workflow update '{"D2": "=B2*C2*1.5"}' --file sales.xlsx

# Mass update - create formulas for entire column
excel-workflow update '{"D2": "=B2*0.5", "D3": "=B3*0.5", ...}' --file data.xlsx
```

**输出结果：**
```json
{
  "status": "success",
  "filename": "sales.xlsx",
  "updated": 2,
  "changes": [
    {"cell": "C2", "old_value": 50, "new_value": 100},
    {"cell": "C3", "old_value": 75, "new_value": 200}
  ],
  "message": "✅ Updated and re-uploaded to Google Drive"
}
```

### list 命令

显示所有被跟踪的文件信息：

```bash
excel-workflow list [--limit 10]
```

**输出结果：**
```json
[
  {
    "id": 2,
    "original_filename": "sales_2026.xlsx",
    "sheet_count": 2,
    "formula_count": 15,
    "uploaded_at": "2026-02-20 14:20:00"
  },
  {
    "id": 1,
    "original_filename": "budget.xlsx",
    "sheet_count": 3,
    "formula_count": 42,
    "uploaded_at": "2026-02-19 09:15:30"
  }
]
```

### stats 命令

显示统计信息：

```bash
excel-workflow stats
```

**输出结果：**
```json
{
  "total_files": 5,
  "files_on_drive": 5,
  "total_sheets": 12,
  "total_formulas": 87
}
```

## 适用于 AI 代理的使用场景

### 使用场景 1：用户上传 Excel 文件

**用户操作：** 通过 Telegram 上传 `sales.xlsx` 文件

**代理工作流程：**
1. 通过 Telegram 处理器将文件保存到临时目录
2. 检测文件扩展名为 `.xlsx`
3. 运行命令：`excel-workflow process /path/to/sales.xlsx --telegram-id <id>`
4. 解析 JSON 结果并回复用户

```
Agent: "✅ I've received and processed sales.xlsx!

📊 Analysis:
- 2 sheets: Sales, Summary
- 15 formulas detected
- ☁️ Uploaded to Google Drive

What would you like to know about this file?"
```

### 使用场景 2：用户提问

**用户问题：** “我的销售文件中的总收入是多少？”

**代理工作流程：**
1. 运行命令：`excel-workflow query "what is total revenue?" --file sales.xlsx`
2. 读取包含所有数据和公式的 JSON 结果
3. 分析数据以获取与收入相关的信息并回复用户

```
Agent: "Looking at your sales.xlsx file:

Total Revenue: 650,000 руб

Breakdown:
- iPhone: 150,000 (3 × 50,000)
- MacBook: 200,000 (2 × 100,000)
- iPad: 300,000 (5 × 60,000)

The file has a SUM formula in cell D5 that calculates this automatically."
```

### 使用场景 3：用户请求更新数据

**用户请求：** “将 iPhone 的数量更改为 20”

**代理工作流程：**
1. 运行命令：`excel-workflow query "find iPhone row"`
2. 确定 iPhone 对应的行号（例如第 2 行）和列号（公式位于 C 列）
3. 运行命令：`excel-workflow update '{"C2": 20}' --file sales.xlsx`
4. 确认更新结果

```
Agent: "✅ Updated sales.xlsx:

Changed C2 (iPhone quantity): 3 → 20

New revenue for iPhone: 1,000,000 руб (was 150,000)
Total revenue updated automatically thanks to formulas!

File has been re-uploaded to Google Drive."
```

### 使用场景 4：批量创建公式

**用户请求：** “为所有产品创建一个新列，将价格乘以 0.5”

**代理工作流程：**
1. 读取文件内容以确定行数
2. 生成包含批量公式更新的 JSON 数据
3. 运行命令：`excel-workflow update '{"D2": "=B2*0.5", "D3": "=B3*0.5", ...}' --file prices.xlsx`
4. 确认更新结果

## 技术细节

### 组件说明

1. **Excel 命令行工具**：基于 openpyxl 的工具，用于读写 Excel 文件
   - 使用 `data_only=False` 选项来保留公式
   - 支持的命令：`read`、`update`、`info`、`show-formulas`、`get-cell`

2. **数据跟踪工具**：使用 SQLite 数据库记录文件元数据
   - 数据库文件路径：`~/.openclaw/excel_tracker.db`
   - 记录的字段包括文件名、工作表、公式、文件路径和修改时间戳

3. **工作流程协调器**：负责协调 Excel 命令行工具、rclone 和数据跟踪工具的运行顺序
   - 将文件分析、上传、跟踪和更新等操作整合在一起
   - 进度信息输出到标准错误流（stderr），结果输出到标准输出流（stdout）

### 文件存储位置

- **数据库文件：** `~/.openclaw/excel_tracker.db`
- **Google Drive 文件夹：** `gdrive:Excel/`
- **本地文件：** 用户指定的路径（文件通过 Telegram 保存到 `~/.openclaw/media/`

### 公式保留机制

- openpyxl 在读取文件时使用 `data_only=False` 选项来保留公式
- 公式以文本字符串的形式存储（例如 `"=B2*C2"`）
- 更新单元格时，openpyxl 会保留这些公式字符串
- 当文件再次被打开时，Excel 会重新计算公式

**示例：**
```python
# This preserves formulas
ws['D2'] = '=B2*C2'  # Formula remains
ws['B2'] = 100       # Data changes, formula in D2 recalculates
```

### 公式保留的范围

- **被保留的元素：**
  - 公式（如 `=SUM`、`=IF`、`=B2*C2` 等）
  - 数据（数字、文本、日期）
  - 文件结构（工作表、表格）
  - 格式设置（颜色、字体、边框、加粗）
  - 图表（图表会自动更新）

- **无法保留的元素：**
  - 条件格式（复杂的格式规则）
  - 宏（.xlsm 文件不支持）
  - 数据透视表（可能无法正确显示）
  - 数据切片器和高级筛选功能

## 错误处理

- **常见错误：**
  - **文件未找到**：```json
   {"error": "File not found: /path/to/file.xlsx"}
   ```
  - **Google Drive 配置错误**：```json
   {"error": "rclone remote 'gdrive' not configured"}
   ```（解决方法：运行 `rclone config`）
  - **公式语法错误**：```json
   {"error": "Invalid formula: =B2*"}
   ```（解决方法：检查公式语法）
  - **数据库被锁定**：```json
   {"error": "Database is locked"}
   ```（解决方法：稍后重试）

## 示例

- **示例 1：财务数据分析**：```bash
# Upload stock data
excel-workflow process ~/Desktop/ARKK.xlsx

# Query
excel-workflow query "show last 10 rows" --file ARKK.xlsx

# Add calculated column (50% of price)
# First, find row count, then generate formulas
excel-workflow update '{"C2": "=B2*0.5", "C3": "=B3*0.5", ...}' --file ARKK.xlsx
```
- **示例 2：价格列表更新**：```bash
# Process price list
excel-workflow process prices.xlsx

# Update prices
excel-workflow update '{"B10": 99.99, "B11": 149.99}' --file prices.xlsx

# Add tax column
excel-workflow update '{"D2": "=B2*1.2"}' --file prices.xlsx
```
- **示例 3：处理多个文件**：```bash
# Upload multiple files
excel-workflow process january.xlsx
excel-workflow process february.xlsx

# List all files
excel-workflow list

# Query specific file
excel-workflow query "total sales" --file january.xlsx

# Stats
excel-workflow stats
```

## 故障排除

- **问题 1：rclone 未找到**：```bash
# Install rclone
brew install rclone  # macOS
sudo apt install rclone  # Linux
```
- **问题 2：openpyxl 未安装**：```bash
# Install in virtual environment
cd ~/.openclaw/tools/openclaw-excel
python3 -m venv venv
./venv/bin/pip install openpyxl
```
- **问题 3：Google Drive 访问权限被拒绝**：```bash
# Reconfigure rclone
rclone config
# Delete old gdrive remote and create new one
```
- **问题 4：公式被错误地更新为数值**：**这种情况不应发生！** 如果发生，请检查：
  - 确保 `excel` 命令行工具在读取文件时使用了 `data_only=False`
  - 确保公式字符串以 `=` 开头
  - 验证 openpyxl 的版本（使用 `pip show openpyxl`，版本应大于或等于 3.1.0）

## 最佳实践

- **对于用户：**
  - 为文件起具有描述性的名称（例如：`sales_2026_Q1.xlsx`）
  - 提出具体问题（例如：`January 的总收入是多少？`）
  - 保持文件结构的一致性，以便 AI 更容易理解文件内容

- **对于开发者：**
  - 在处理文件前务必检查文件是否存在
  - 对于同一文件的多次操作，使用事务（session）来确保数据完整性
  - 使用 `try/except` 语句优雅地处理错误
  - 在标准错误流中显示处理进度，在标准输出流中显示结果
  - 在更新单元格前验证公式内容的正确性

## API 参考

详细 API 文档请参阅 [Excel 命令行工具文档](./excel_cli.md) 和 [数据跟踪工具文档](./tracker.md)。

## 相关资源

- [openpyxl 官方文档](https://openpyxl.readthedocs.io/)
- [rclone 官方文档](https://rclone.org/docs/)
- [Microsoft Excel 文件格式规范](https://learn.microsoft.com/en-us/openspecs/office_standards/ms-xlsx/)
- [使用 rclone 连接 Google Drive 的方法](https://rclone.org/drive/)

## 技术支持

- 问题反馈：[GitHub 问题页面：[your-repo/excel-workflow/issues]**
- 文档资料：[your-repo/excel-workflow/docs]
- 社区资源：[OpenClaw 社区]

## 许可证

本工具采用 MIT 许可证，详细许可信息请参阅 `LICENSE.txt` 文件。

## 更新记录

### 版本 1.0.0（2026-02-20）

- 首次发布
- 支持使用 openpyxl 保留公式
- 实现了通过 rclone 与 Google Drive 的同步功能
- 引入了 SQLite 数据跟踪机制
- 支持多文件处理
- 新增了批量公式更新功能
- 更新了与 AI 代理的集成方式