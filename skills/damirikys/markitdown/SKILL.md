---
name: markitdown
description: MarkItDown 是微软提供的一个 Python 工具，用于将多种文件（PDF、Word、Excel、PPTX、图片、音频）转换为 Markdown 格式。该工具非常适用于提取结构化文本，以便用于大型语言模型（LLM）的分析。
homepage: https://github.com/microsoft/markitdown
repository: https://github.com/microsoft/markitdown
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"] },
        "install":
          [
            {
              "id": "venv",
              "kind": "exec",
              "command": "python3 -m venv .venv && .venv/bin/pip install 'markitdown[all]'",
              "label": "Create virtual environment and install markitdown with all dependencies from PyPI",
            },
          ],
      },
  }
---
# MarkItDown 技能

## 描述
MarkItDown 是由微软开发的一款 Python 工具（源代码链接：https://github.com/microsoft/markitdown），用于将各种文件和办公文档转换为 Markdown 格式。它可以帮助我轻松地从复杂的文档格式中提取结构化文本（包括表格、标题和列表），从而更好地理解文档内容。转换过程在本地完成，使用的是已安装的 Python 库。

**安全提示**：安装过程中会从官方的 Python 包索引（PyPI）下载 `markitdown` 及其依赖项。处理某些格式（如 YouTube 链接）时需要外部网络访问来获取内容；处理本地文件时则需要访问目标文件所在的目录。

## 支持的格式
- **办公文档**：PowerPoint（PPTX）、Word（DOCX）、Excel（XLSX、XLS）。
- **PDF**  
- **图片**：文本提取（OCR）和元数据（EXIF）。  
- **音频/视频**：语音转录（wav、mp3、YouTube 链接）以及 EXIF 标签。  
- **网页和文本**：HTML、CSV、JSON、XML。  
- **压缩文件和电子书**：ZIP 压缩包、EPub 格式。

## 依赖项
该工具会在本地虚拟环境中安装。由于通过 PyPI 安装了 `markitdown[all]` 依赖项，因此大多数功能都可以直接使用。对于特定的格式（如音频/视频），可能需要额外的系统库（例如 `ffmpeg`），这些库需要单独在主机上安装。

## 使用场景
- 当你需要阅读、分析或从 PDF、Word、Excel 或 PowerPoint 文件中提取信息时。
- 当文档的结构对结果非常重要时（例如包含表格或格式化的列表）。
- 当你需要从音频或视频文件中提取文本，或者“读取”图片内容时。

## 使用方法
安装该工具后，虚拟环境会自动创建。你需要在工具所在的文件夹内运行该工具。

### 控制台输出转换（STDOUT）
适用于处理较小的文件，可以立即查看转换结果。
```bash
./.venv/bin/markitdown /path/to/file.pdf
```

### 文件输出转换
对于较大的文档，建议将转换结果保存为 `.md` 文件，然后使用 `read` 工具进行阅读。
```bash
./.venv/bin/markitdown /path/to/file.pdf -o /path/to/result.md
```

### 示例：Excel 文件转换
导航到工具所在的文件夹（例如：`cd ~/skills/markitdown`），然后执行以下命令：
```bash
./.venv/bin/markitdown ~/downloads/report.xlsx -o ~/downloads/report.md
```
之后，你可以阅读生成的 `report.md` 文件。