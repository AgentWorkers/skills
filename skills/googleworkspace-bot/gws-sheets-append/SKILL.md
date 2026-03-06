---
name: gws-sheets-append
version: 1.0.0
description: "**Google Sheets：向电子表格中添加一行。**"
metadata:
  openclaw:
    category: "productivity"
    requires:
      bins: ["gws"]
    cliHelp: "gws sheets +append --help"
---
# sheets +append

> **前提条件：** 请阅读 `../gws-shared/SKILL.md` 以了解身份验证、全局参数和安全规则。如果文件缺失，请运行 `gws generate-skills` 生成该文件。

**功能：** 向电子表格中添加一行数据。

## 使用方法

```bash
gws sheets +append --spreadsheet <ID>
```

## 参数说明

| 参数          | 是否必填 | 默认值    | 说明                          |
|--------------|---------|---------|--------------------------------------------|
| `--spreadsheet`  | ✓       |         | 电子表格的 ID                          |
| `--values`     |         |         | 以逗号分隔的字符串（简单数据）                   |
| `--json-values`  |         |         | JSON 格式的行数据，例如 `[[“a”, “b”], [“c”, “d”]]`           |

## 示例

```bash
gws sheets +append --spreadsheet ID --values 'Alice,100,true'
gws sheets +append --spreadsheet ID --json-values '[["a","b"],["c","d"]]'
```

## 提示：

- 对于简单的单行数据添加，使用 `--values` 参数。
- 对于批量多行数据的插入，使用 `--json-values` 参数。

> **注意：** 此命令具有写入电子表格的功能，请在执行前确认用户已授权。

## 相关文档：

- [gws-shared](../gws-shared/SKILL.md) — 全局参数和身份验证相关说明
- [gws-sheets](../gws-sheets/SKILL.md) — 所有与电子表格读写相关的命令说明