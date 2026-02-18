---
name: printer
description: 将图像和PDF文件打印到任何支持CUPS协议的打印机上。该工具具备PPD（Postscript Printer Description）识别功能：能够在运行时读取纸张尺寸、页边距、分辨率以及是否支持双面打印等参数。适用于用户需要打印文件（如PNG/JPG格式的图像或PDF文档）或查询打印机功能的场景。
  Print images and PDFs to any CUPS printer. PPD-aware: reads paper sizes,
  margins, resolution, and duplex at runtime. Use when the user wants to
  print files (images like PNG/JPG or PDFs) or query printer capabilities.
summary: "Print images and PDFs to any CUPS printer with PPD-aware settings."
version: 1.2.2
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

可以将图像和PDF文件打印到任何支持CUPS协议的打印机上。所有设置（纸张大小、页边距、分辨率、双面打印等）都会在运行时从打印机的PPD（Postscript Printer Description）文件中读取。

**入口点：** `{baseDir}/scripts/print.py`

## 设置

有关先决条件和平台说明，请参阅 [SETUP.md](SETUP.md)。

## 命令

### 列出可用打印机

```bash
python3 {baseDir}/scripts/print.py list
python3 {baseDir}/scripts/print.py list --json
```

显示所有可用打印机的状态以及系统默认打印机。

### 打印文件

```bash
python3 {baseDir}/scripts/print.py print /path/to/file.pdf
python3 {baseDir}/scripts/print.py print /path/to/image.png
python3 {baseDir}/scripts/print.py print /path/to/file.pdf --printer "Custom_Printer"
python3 {baseDir}/scripts/print.py print /path/to/file.pdf -o InputSlot=tray-2
python3 {baseDir}/scripts/print.py print /path/to/file.pdf -o cupsPrintQuality=High -o sides=one-sided
python3 {baseDir}/scripts/print.py print /path/to/file.pdf --json
```

- **PDF文件**：直接以正确的纸张类型和双面设置发送到打印机。
- **图像文件**（PNG、JPG、GIF、BMP、TIFF、WebP）：会先转换为PDF格式（使用打印机的原生DPI分辨率），然后居中显示在可打印区域内再进行打印。
- **`-o KEY=VALUE`**：传递任何CUPS选项（可重复使用）。可以使用 `options` 参数来查看可用的设置（如纸张托盘、打印质量、纸张类型、双面打印模式、颜色模式等）。
- 如果路径是符号链接，解析后的路径必须位于工作目录内或 `/tmp` 目录中。

### 打印机信息

```bash
python3 {baseDir}/scripts/print.py info
python3 {baseDir}/scripts/print.py info --printer "Custom_Printer"
python3 {baseDir}/scripts/print.py info --json
```

显示打印机的制造商、型号、分辨率、颜色支持情况、默认纸张类型、双面打印模式、输入托盘以及所有支持的纸张尺寸及其对应的页边距。

### 打印机选项

```bash
python3 {baseDir}/scripts/print.py options
python3 {baseDir}/scripts/print.py options --printer "Custom_Printer"
python3 {baseDir}/scripts/print.py options --json
```

显示所有CUPS选项的当前值及可选设置。

## 注意事项

- 除非指定了 `--printer` 参数，否则会使用**系统默认打印机**。
- 所有命令都支持 `--json` 选项，以生成机器可读的格式化输出。
- 图像转换时会根据打印机的PPD文件中的可打印区域（页边距）进行裁剪。
- 仅支持以下可打印文件格式：PDF、PNG、JPG、GIF、BMP、TIFF、WebP。

## 提示

### 选择纸张托盘/纸张类型

某些打印机的PPD文件中可能没有 `InputSlot` 相关的设置，因此仅使用 `-o InputSlot=tray-2` 可能无法正常工作。此时应结合使用 `media` 关键字：

```bash
# Print to a specific tray with media type
python3 {baseDir}/scripts/print.py print envelope.pdf -o media=A6,tray-2,envelope

# Format: -o media=SIZE,TRAY,TYPE
# SIZE: A4, A5, A6, EnvDL, EnvC5, Letter, etc.
# TRAY: tray-1, tray-2, auto
# TYPE: stationery, envelope, cardstock, labels, etc.
```

这种方式会通过IPP协议直接指定纸张托盘，从而绕过PPD文件的设置。