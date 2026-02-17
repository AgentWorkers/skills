---
name: printer
description: 可以将图像和 PDF 文件打印到任何支持 CUPS 协议的打印机上。该工具具备 PPD（PostScript Printer Description）识别功能：能够在运行时自动检测纸张大小、页边距、分辨率以及是否支持双面打印等打印参数。适用于用户需要打印文件（如 PNG/JPG 格式的图像或 PDF 文件）或查询打印机功能的场景。
  Print images and PDFs to any CUPS printer. PPD-aware: reads paper sizes,
  margins, resolution, and duplex at runtime. Use when the user wants to
  print files (images like PNG/JPG or PDFs) or query printer capabilities.
summary: "Print images and PDFs to any CUPS printer with PPD-aware settings."
version: 1.1.1
homepage: https://github.com/odrobnik/printer-skill
metadata:
  openclaw:
    emoji: "🖨️"
    requires:
      bins:
        - python3
        - lp
        - lpstat
        - lpoptions
      python:
        - Pillow
---
# 打印机

可以将图像和 PDF 文件打印到任何支持 CUPS 协议的打印机上。所有打印设置（纸张大小、页边距、分辨率、双面打印等）都会在运行时从打印机的 PPD（PostScript 打印描述文件）中读取。

**入口点：** `{baseDir}/scripts/print.py`

## 设置

有关先决条件和平台说明，请参阅 [SETUP.md](SETUP.md)。

## 命令

### 列出可用打印机

```bash
uv run {baseDir}/scripts/print.py list
uv run {baseDir}/scripts/print.py list --json
```

显示所有可用打印机的状态以及系统默认打印机。

### 打印文件

```bash
uv run {baseDir}/scripts/print.py print /path/to/file.pdf
uv run {baseDir}/scripts/print.py print /path/to/image.png
uv run {baseDir}/scripts/print.py print /path/to/file.pdf --printer "Custom_Printer"
uv run {baseDir}/scripts/print.py print /path/to/file.pdf -o InputSlot=tray-2
uv run {baseDir}/scripts/print.py print /path/to/file.pdf -o cupsPrintQuality=High -o sides=one-sided
uv run {baseDir}/scripts/print.py print /path/to/file.pdf --json
```

- **PDF 文件**：直接以正确的介质和双面打印设置发送到打印机。
- **图像文件**（PNG、JPG、GIF、BMP、TIFF、WebP）：会在打印机支持的 DPI 下转换为 PDF 格式，并居中显示在可打印区域内，然后进行打印。
- **`-o KEY=VALUE`**：传递任何 CUPS 参数（可重复使用）。使用 `options` 参数可以查看可用的设置（如纸张托盘、打印质量、介质类型、双面打印模式、颜色模式等）。
- 如果输入的是符号链接，系统会解析该链接的路径，但解析后的路径必须位于工作目录内或 `/tmp` 目录中。

### 打印机信息

```bash
uv run {baseDir}/scripts/print.py info
uv run {baseDir}/scripts/print.py info --printer "Custom_Printer"
uv run {baseDir}/scripts/print.py info --json
```

显示打印机的制造商、型号、分辨率、颜色支持情况、默认纸张类型、双面打印模式、输入托盘以及所有纸张尺寸及对应的页边距信息。

### 打印机参数设置

```bash
uv run {baseDir}/scripts/print.py options
uv run {baseDir}/scripts/print.py options --printer "Custom_Printer"
uv run {baseDir}/scripts/print.py options --json
```

显示所有 CUPS 参数及其当前值和可用的选项。

## 注意事项

- 除非指定了 `--printer` 参数，否则会使用 **系统默认打印机**。
- 所有命令都支持 `--json` 选项，以生成机器可读的输出格式。
- 图像转换时会尊重打印机 PPD 文件中规定的可打印区域（包括页边距）。
- 仅支持以下可打印文件格式：PDF、PNG、JPG、GIF、BMP、TIFF、WebP。