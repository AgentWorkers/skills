---
name: gws-sheets-read
version: 1.0.0
description: "Google Sheets：从电子表格中读取数据。"
metadata:
  openclaw:
    category: "productivity"
    requires:
      bins: ["gws"]
    cliHelp: "gws sheets +read --help"
---
# sheets +read

> **前提条件：** 需要阅读 `../gws-shared/SKILL.md` 以了解认证信息、全局参数和安全规则。如果文件缺失，请运行 `gws generate-skills` 命令来生成该文件。

**从电子表格中读取数据**

## 使用方法

```bash
gws sheets +read --spreadsheet <ID> --range <RANGE>
```

## 参数说明

| 参数 | 是否必填 | 默认值 | 说明 |
|------|---------|---------|-------------|
| `--spreadsheet` | ✓ | — | 电子表格的 ID |
| `--range` | ✓ | — | 需要读取的数据范围（例如：'Sheet1!A1:B2'） |

## 示例

```bash
gws sheets +read --spreadsheet ID --range "Sheet1!A1:D10"
gws sheets +read --spreadsheet ID --range Sheet1
```

## 提示：

- 该功能仅支持读取操作，不会修改电子表格中的数据。
- 如需更高级的功能，可以使用 `raw_values.get` API。

## 相关文档：

- [gws-shared](../gws-shared/SKILL.md) — 全局参数和认证机制
- [gws-sheets](../gws-sheets/SKILL.md) — 所有与电子表格读写相关的命令