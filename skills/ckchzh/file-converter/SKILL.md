---
name: file-converter
description: "文件格式转换器：能够识别多种文件格式（JSON、YAML、XML、CSV、Markdown），并在这些格式之间进行相互转换；同时具备代码压缩和美化功能。支持的命令包括：`detect`（检测文件格式）、`json2yaml`（将JSON转换为YAML）、`yaml2json`（将YAML转换为JSON）、`csv2md`（将CSV转换为Markdown）、`md2csv`（将Markdown转换为CSV）、`xml2json`（将XML转换为JSON）、`minify`（压缩代码）、`prettify`（美化代码）。适用于数据格式转换、代码压缩及代码格式优化场景。"
---
# 🔄 文件转换器

> 一个命令，支持多种格式。可以在这几种格式之间进行转换：JSON、YAML、XML、CSV 和 Markdown。同时支持代码文件的压缩（minify）和美化（prettify）。

## 快速入门

```bash
bash scripts/convert.sh <command> [file]
```

## 命令列表

| 命令          | 描述                                      | 示例                                      |
|---------------|----------------------------------------|----------------------------------------|
| `detect <文件>`     | 自动检测文件格式                         | `detect data.txt`                             |
| `json2yaml <文件>`    | 将 JSON 转换为 YAML                         | `json2yaml config.json`                         |
| `yaml2json <文件>`    | 将 YAML 转换为 JSON                         | `yaml2json config.yaml`                         |
| `csv2md <文件>`    | 将 CSV 转换为 Markdown 表格                   | `csv2md report.csv`                         |
| `md2csv <文件>`    | 将 Markdown 表格转换为 CSV                         | `md2csv table.md`                         |
| `xml2json <文件>`    | 将 XML 转换为 JSON                         | `xml2json data.xml`                         |
| `json2xml <文件>`    | 将 JSON 转换为 XML                         | `json2xml data.json`                         |
| `minify <文件>`     | 压缩 JSON/CSS/JS 文件                         | `minify app.js`                         |
| `prettify <文件>`     | 美化代码格式                             | `prettify min.json`                         |

## 工作流程

1. 运行 `detect` 命令以确认文件的原始格式。
2. 选择合适的转换命令。
3. 使用 `prettify` 命令检查转换后的文件是否易于阅读。
4. 使用 `minify` 命令压缩最终生成的文件。

## 注意事项

- 转换结果会输出到标准输出（stdout）；若需保存结果，请使用 `>` 重定向到指定文件。
- 支持通过管道输入文件：`cat data.json | bash scripts/convert.sh json2yaml -`
- 对于未知格式的文件，请先运行 `detect` 命令以避免输出混乱。