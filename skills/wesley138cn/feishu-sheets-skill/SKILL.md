---
name: feishu-sheets
description: >
  Feishu在线电子表格（Sheets）的操作包括创建、读取、写入数据以及管理工作表。  
  当用户提到Feishu Sheets、在线电子表格或电子表格时，通常指的是这个工具。  
  该工具支持以下功能：  
  - 创建电子表格  
  - 读取/写入单元格的值  
  - 添加/删除行或列  
  - 管理工作表
---
# Feishu Sheets 工具

`feishu_sheets` 是一个单一的工具，通过提供相应的动作参数来执行所有电子表格操作。

## 令牌提取

从 URL `https://xxx.feishu.cn/sheets/shtABC123` 中提取令牌：`spreadsheet_token` = `shtABC123`

## 动作

### 创建电子表格

```json
{ "action": "create", "title": "New Spreadsheet" }
```

（可选文件夹配置：）
```json
{ "action": "create", "title": "New Spreadsheet", "folder_token": "fldcnXXX" }
```

返回值：`spreadsheet_token`、`url`、`title`

### 写入数据

```json
{
  "action": "write",
  "spreadsheet_token": "shtABC123",
  "sheet_id": "0bxxxx",
  "range": "A1:C3",
  "values": [["Name", "Age", "City"], ["Alice", 25, "Beijing"], ["Bob", 30, "Shanghai"]]
}
```

### 读取数据

```json
{
  "action": "read",
  "spreadsheet_token": "shtABC123",
  "sheet_id": "0bxxxx",
  "range": "A1:C10"
}
```

### 添加数据

```json
{
  "action": "append",
  "spreadsheet_token": "shtABC123",
  "sheet_id": "0bxxxx",
  "values": [["Charlie", 28, "Shenzhen"]]
}
```

### 插入行/列

```json
{
  "action": "insert_dimension",
  "spreadsheet_token": "shtABC123",
  "sheet_id": "0bxxxx",
  "dimension": "ROWS",
  "start_index": 5,
  "end_index": 7
}
```

### 删除行/列

```json
{
  "action": "delete_dimension",
  "spreadsheet_token": "shtABC123",
  "sheet_id": "0bxxxx",
  "dimension": "ROWS",
  "start_index": 5,
  "end_index": 7
}
```

### 获取电子表格信息

```json
{ "action": "get_info", "spreadsheet_token": "shtABC123" }
```

返回值：包含所有工作表 ID 和标题的元数据

### 添加工作表

```json
{
  "action": "add_sheet",
  "spreadsheet_token": "shtABC123",
  "title": "Sheet2"
}
```

### 删除工作表

```json
{
  "action": "delete_sheet",
  "spreadsheet_token": "shtABC123",
  "sheet_id": "0bxxxx"
}
```

## 范围格式

- 单个单元格：`A1`、`B5`
- 范围：`A1:C10`、`B2:D5`
- 整个列：`A:A`、`B:D`
- 整行：`1:1`、`3:5`
- 带有工作表 ID 的范围：`0bxxxx!A1:C10`

## 工作表 ID

- 从 URL 中获取：`https://xxx.feishu.cn/sheets/shtABC123?sheet=0bxxxx`
- 也可以通过 `get_info` 动作获取
- 默认的第一个工作表通常具有简单的 ID，例如 `0bxxxx`

## 数据类型

数据类型包括：
- 字符串：`"Hello"`
- 数字：`123`、`45.67`
- 公式：`{"type": "formula", "text": "=SUM(A1:A10)"}`
- 链接：`{"type": "url", "text": "点击这里", "link": "https://..."}`

## 配置选项

```yaml
channels:
  feishu:
    tools:
      sheets: true  # default: true
```

## 所需权限

- `sheets:spreadsheet`：创建和管理电子表格
- `sheets:spreadsheet:readonly`：读取电子表格数据
- `drive:drive`：访问云存储

## API 参考

基础 URL：`https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/`

详细 API 文档请参阅 `api-reference.md`。