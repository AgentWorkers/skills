---
name: Spreadsheet
slug: spreadsheet
version: 1.0.0
description: 使用模式内存（schema memory）功能，支持读写和分析表格数据，同时保持数据的格式不变，并兼容多种平台。
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 使用场景

当用户需要对电子表格进行操作时，例如读取数据、修改单元格内容、分析表格数据、生成报告，或者在不同格式的文件（如 Google Sheets、Excel 或 CSV）中追踪结构化信息，就可以使用此技能。

## 架构

程序的内存数据存储在 `~/spreadsheet/` 目录下。具体配置方法请参考 `memory-template.md` 文件。

```
~/spreadsheet/
  memory.md           # Preferences, recent sheets, format rules
  projects/           # Per-project schemas and configs
    {name}.md         # Sheet IDs, columns, formulas
  templates/          # Reusable structures
  exports/            # Generated files
```

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 内存配置 | `memory-template.md` |
| Google Sheets API | `google-sheets.md` |
| Excel 操作 | `excel.md` |
| CSV 文件处理 | `csv.md` |

## 使用范围

此技能仅用于：
- 根据用户请求读取或写入电子表格数据；
- 将数据结构和用户偏好设置存储在 `~/spreadsheet/` 目录下；
- 处理用户提供的文件内容。

**注意：**  
此技能绝不会：
- 在未经用户请求的情况下访问电子表格；
- 存储密码、API 密钥或敏感的财务数据；
- 修改位于 `~/spreadsheet/` 目录之外的文件。

## 数据存储

所有数据均存储在 `~/spreadsheet/` 目录下。首次使用该技能时，系统会自动创建相关数据结构文件。

## 自我更新规则

此技能本身不会被修改。所有用户数据仅存储在 `~/spreadsheet/` 目录下。

## 核心规则

### 1. 数据结构优先

首次访问任何电子表格时，需完成以下操作：
1. 记录表格中的列信息（列名、数据类型及示例值）；
2. 将这些信息保存到 `projects/{name}.md` 文件中；
3. 在后续操作中引用该数据结构。

### 2. 格式保留

- **单元格更新**：保持原有的格式；
- **数字显示**：根据用户的地区设置（例如，1,000.00 或 1.000,00）；
- **日期格式**：使用用户指定的格式；
- **公式编写**：除非用户明确要求，否则不要覆盖原有的公式。

### 3. 大量数据处理策略

- **数据行数较少（<1000行）**：直接加载全部数据；
- **数据行数在 1000 到 10000 行之间**：采用抽样查询的方式；
- **数据行数超过 10000 行**：分页处理，并在加载前向用户发出警告。

### 4. 集成优先级

- **Google Sheets**：优先使用其提供的 API；
- **Excel（.xlsx 格式）**：优先使用 openpyxl 库处理本地文件；
- **CSV 文件**：作为通用处理方式。

### 5. 内存更新规则

- **新电子表格被访问时**：将表格的 ID 和数据结构添加到内存中；
- **用户修改了数据格式**：更新相应的偏好设置；
- **列名被更改**：更新相关的数据结构文件。

## 常见问题及解决方法

- **数据截断问题**：在加载超过 1000 行的数据前，请务必确认；
- **公式丢失问题**：在使用 openpyxl 时，需将 `data_only` 参数设置为 `False`，并单独读取公式内容；
- **数据结构不一致问题**：如果上次访问电子表格已超过 7 天，需重新验证数据结构；
- **请求速率限制**：针对 Google Sheets 的 API 请求，每 100 秒内最多发送 100 个请求；
- **编码问题**：默认使用 UTF-8 编码；对于欧洲地区的文件，需检查文件是否包含 BOM（Byte Order Mark）；
- **空单元格问题**：Google Sheets API 会忽略空单元格；pandas 库会用 `NaN` 值填充空单元格。