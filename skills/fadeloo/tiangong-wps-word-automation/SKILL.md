---
name: wps-word-automation
description: 通过 COM（Component Object Model）在 Windows 上自动化常见的 Word/WPS 文档操作（读取文本、替换文本、插入内容、添加标题/页脚、分页、合并文档、拆分文档、导出为 PDF/TXT 格式、添加/替换图片）。仅适用于单文档操作（不支持批量处理）。
---

# WPS/Word 自动化（Windows）

使用随附的 Python 脚本通过 COM 接口控制 Word 或 WPS。

## 前提条件

- 安装了 **Microsoft Word** 或 **WPS Writer** 的 Windows 系统。
- 安装了 Python 及 **pywin32** 库（通过 `python -m pip install pywin32` 安装）。

## 快速入门

```bash
python {baseDir}/scripts/wps_word_automation.py read --input "C:\path\file.docx"
python {baseDir}/scripts/wps_word_automation.py replace --input "C:\path\file.docx" --find "旧" --replace "新" --save "C:\path\out.docx"
python {baseDir}/scripts/wps_word_automation.py export --input "C:\path\file.docx" --format pdf --output "C:\path\out.pdf"
```

## 命令

### read
提取纯文本。

```bash
python {baseDir}/scripts/wps_word_automation.py read --input "C:\path\file.docx" --output "C:\path\out.txt"
```

### replace
查找并替换文本。

```bash
python {baseDir}/scripts/wps_word_automation.py replace --input "C:\path\file.docx" --find "old" --replace "new" --save "C:\path\out.docx"
```

### insert
在文档的开头或结尾插入文本。

```bash
python {baseDir}/scripts/wps_word_automation.py insert --input "C:\path\file.docx" --text "Hello" --where start --save "C:\path\out.docx"
```

### headings
为匹配的行应用标题 1/2/3 格式。

```bash
python {baseDir}/scripts/wps_word_automation.py headings --input "C:\path\file.docx" --level 1 --prefix "# " --save "C:\path\out.docx"
```

### header-footer
设置页眉和页脚文本。

```bash
python {baseDir}/scripts/wps_word_automation.py header-footer --input "C:\path\file.docx" --header "标题" --footer "页脚" --save "C:\path\out.docx"
```

### page-break
在文档的末尾插入分页符。

```bash
python {baseDir}/scripts/wps_word_automation.py page-break --input "C:\path\file.docx" --save "C:\path\out.docx"
```

### merge
将多个文档合并为一个。

```bash
python {baseDir}/scripts/wps_word_automation.py merge --inputs "a.docx" "b.docx" --output "merged.docx"
```

### split
根据页码范围分割文档（例如：“1-3,4-6”）。

```bash
python {baseDir}/scripts/wps_word_automation.py split --input "C:\path\file.docx" --pages "1-3,4-6" --outdir "C:\out"
```

### export
将文档导出为 PDF 或 TXT 格式。

```bash
python {baseDir}/scripts/wps_word_automation.py export --input "C:\path\file.docx" --format pdf --output "C:\path\out.pdf"
python {baseDir}/scripts/wps_word_automation.py export --input "C:\path\file.docx" --format txt --output "C:\path\out.txt"
```

### image
在文档的末尾添加或替换图片。

```bash
python {baseDir}/scripts/wps_word_automation.py image --input "C:\path\file.docx" --image "C:\path\img.png" --save "C:\path\out.docx"
```

## 注意事项

- 如果安装了 WPS，请使用 `--app wps` 选项；否则系统会默认使用 Word。
- 如果需要查看用户界面，请使用 `--visible true` 选项。
- 本功能仅适用于单文档操作，不建议批量使用。