---
name: json-linter
description: 该技能用于验证工作空间中的 JSON 语法。您可以利用它来检查配置文件、内存文件或数据资产中的语法错误。
---
# JSON Linter

这是一个简单的工具，用于递归扫描工作区中的`.json`文件，并使用`JSON.parse()`来验证它们的语法。

## 使用方法

```bash
# Scan the entire workspace (from current working directory)
node skills/json-linter/index.js

# Scan a specific directory
node skills/json-linter/index.js --dir path/to/dir
```

## 输出结果

JSON报告包含以下内容：
- `scanned_at`: 扫描时间戳
- `total_files`: 被扫描的`.json`文件总数
- `valid_files`: 有效的文件数量
- `invalid_files`: 无效的文件数量
- `errors`: 错误对象数组：
  - `path`: 文件的相对路径
  - `error`: 错误信息（例如：“在JSON的第42个位置发现了意外的符号`}`）

## 示例输出

```json
{
  "scanned_at": "2026-02-14T21:45:00.000Z",
  "total_files": 150,
  "valid_files": 149,
  "invalid_files": 1,
  "errors": [
    {
      "path": "config/broken.json",
      "error": "Unexpected token } in JSON at position 42"
    }
  ]
}
```