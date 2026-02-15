---
name: markitdown-skill
description: OpenClaw代理技能：用于将文档转换为Markdown格式。该工具提供了与Microsoft的MarkItDown库相关的文档和实用程序，支持转换PDF、Word、PowerPoint、Excel文件，以及图像（通过OCR技术进行识别）、音频文件（转换为文本）、HTML文档和YouTube视频。
metadata:
  openclaw:
    emoji: "📄"
    homepage: https://github.com/karmanverma/markitdown-skill
    requires:
      bins: ["python3", "pip", "markitdown"]
    install:
      - id: "markitdown"
        kind: "pip"
        package: "markitdown[all]"
        bins: ["markitdown"]
        label: "Install MarkItDown CLI (pip)"
---

# MarkItDown 技能

本技能提供了使用微软的 [MarkItDown](https://github.com/microsoft/markitdown) 库将文档转换为 Markdown 格式的工具和文档。

> **注意：** 本技能仅提供相关文档和批处理脚本；实际的转换工作由通过 `pip` 安装的 `markitdown` 命令行工具或库完成。

## 使用场景

**MarkItDown 可用于：**
- 📄 获取文档（如 README 文件、API 文档）
- 🌐 将网页转换为 Markdown 格式
- 📝 文档分析（PDF、Word、PowerPoint 文件）
- 🎬 YouTube 视频的字幕提取
- 🖼️ 图片中的文字提取（OCR 技术）
- 🎤 音频内容的转录

## 快速入门

```bash
# Convert file to markdown
markitdown document.pdf -o output.md

# Convert URL
markitdown https://example.com/docs -o docs.md
```

## 支持的格式

| 格式 | 支持的功能 |
|--------|----------|
| PDF | 文本提取、结构保留 |
| Word (.docx) | 标题、列表、表格 |
| PowerPoint | 幻灯片、文本内容 |
| Excel | 表格、单元格内容 |
| 图片 | 图片中的文字提取（OCR 技术）及 EXIF 元数据 |
| 音频 | 音频内容的转录 |
| HTML | 保留文档结构 |
| YouTube | 视频的字幕提取 |

## 安装

本技能需要安装微软提供的 `markitdown` 命令行工具：

```bash
pip install 'markitdown[all]'
```

或者仅安装特定格式的转换工具：

```bash
pip install 'markitdown[pdf,docx,pptx]'
```

## 常用操作模式

### 获取文档
```bash
markitdown https://github.com/user/repo/blob/main/README.md -o readme.md
```

### 转换 PDF 文件
```bash
markitdown document.pdf -o document.md
```

### 批量转换
```bash
# Using included script
python ~/.openclaw/skills/markitdown/scripts/batch_convert.py docs/*.pdf -o markdown/ -v

# Or shell loop
for file in docs/*.pdf; do
  markitdown "$file" -o "${file%.pdf}.md"
done
```

## Python API

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("document.pdf")
print(result.text_content)
```

## 常见问题解答

### “markitdown 未找到”
```bash
pip install 'markitdown[all]'
```

### OCR 功能无法使用
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract
```

## 本技能提供的内容

| 组件 | 来源 |
|-----------|--------|
| `markitdown` 命令行工具 | 微软提供的 Python 包 |
| `markitdown` Python API | 微软提供的 Python 包 |
| `scripts/batch_convert.py` | 本技能对应的批处理脚本 |
| 文档 | 本技能的详细使用说明 |

## 相关资源

- [USAGE-GUIDE.md](USAGE-GUIDE.md) - 详细使用示例
- [reference.md](reference.md) - 完整的 API 参考文档
- [Microsoft MarkItDown](https://github.com/microsoft/markitdown) - 原始库的链接