---
name: wps-ppt-automation
description: 通过 COM（Component Object Model）在 Windows 上自动化常见的 PowerPoint/WPS 演示文稿操作：读取文本/备注/大纲、导出 PDF/图片、替换文本、插入/删除幻灯片、统一字体/大小/主题以及提取图片/媒体文件。适用于单个演示文稿的操作（不支持批量处理）。
---

# WPS/PowerPoint 自动化（Windows）

使用随附的 Python 脚本通过 COM 接口控制 PowerPoint 或 WPS 演示文稿。

## 前提条件

- 安装了 **Microsoft PowerPoint** 或 **WPS Presentation** 的 Windows 系统。
- 安装了 Python 及 `pywin32` 库（通过 `python -m pip install pywin32` 安装）。

## 快速入门

```bash
python {baseDir}/scripts/wps_ppt_automation.py read --input "C:\path\file.pptx"
python {baseDir}/scripts/wps_ppt_automation.py export --input "C:\path\file.pptx" --format pdf --output "C:\path\out.pdf"
```

## 命令

### read
提取所有幻灯片的文本内容。

```bash
python {baseDir}/scripts/wps_ppt_automation.py read --input "C:\path\file.pptx" --output "C:\path\out.txt"
```

### notes
提取演讲者的备注内容。

___CODEBLOCK_2___

### outline
将幻灯片标题导出为大纲格式。

```bash
python {baseDir}/scripts/wps_ppt_automation.py outline --input "C:\path\file.pptx" --output "C:\path\outline.txt"
```

### export
将演示文稿导出为 PDF 或图片（PNG 格式）。

```bash
python {baseDir}/scripts/wps_ppt_automation.py export --input "C:\path\file.pptx" --format pdf --output "C:\path\out.pdf"
python {baseDir}/scripts/wps_ppt_automation.py export --input "C:\path\file.pptx" --format images --outdir "C:\out\slides"
```

### replace
在所有幻灯片中查找并替换指定的文本。

```bash
python {baseDir}/scripts/wps_ppt_automation.py replace --input "C:\path\file.pptx" --find "old" --replace "new" --save "C:\path\out.pptx"
```

### slides
插入或删除幻灯片。

```bash
python {baseDir}/scripts/wps_ppt_automation.py insert-slide --input "C:\path\file.pptx" --index 2 --save "C:\path\out.pptx"
python {baseDir}/scripts/wps_ppt_automation.py delete-slide --input "C:\path\file.pptx" --index 3 --save "C:\path\out.pptx"
```

### font
统一所有幻灯片的字体名称和大小。

```bash
python {baseDir}/scripts/wps_ppt_automation.py font --input "C:\path\file.pptx" --name "Microsoft YaHei" --size 20 --save "C:\path\out.pptx"
```

### theme
应用指定的主题（.thmx 文件）。

```bash
python {baseDir}/scripts/wps_ppt_automation.py theme --input "C:\path\file.pptx" --theme "C:\path\theme.thmx" --save "C:\path\out.pptx"
```

### extract-images
导出嵌入的图片。

```bash
python {baseDir}/scripts/wps_ppt_automation.py extract-images --input "C:\path\file.pptx" --outdir "C:\out\images"
```

## 注意事项

- 如果安装了 WPS，可以使用 `--app wps` 选项；否则脚本将默认使用 PowerPoint。
- 如果需要查看用户界面，请使用 `--visible true` 选项。
- 请避免批量操作；此功能仅适用于单个演示文稿的处理。