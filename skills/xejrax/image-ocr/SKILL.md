---
name: image-ocr
description: "使用 Tesseract OCR 从图像中提取文本"
metadata:
  {
    "openclaw":
      {
        "emoji": "👁️",
        "requires": { "bins": ["tesseract"] },
        "install":
          [
            {
              "id": "dnf",
              "kind": "dnf",
              "package": "tesseract",
              "bins": ["tesseract"],
              "label": "Install via dnf",
            },
          ],
      },
  }
---

# 图像OCR

使用Tesseract OCR从图像中提取文本。支持多种语言和图像格式，包括PNG、JPEG、TIFF和BMP。

## 命令

```bash
# Extract text from an image (default: English)
image-ocr "screenshot.png"

# Extract text with a specific language
image-ocr "document.jpg" --lang eng
```

## 安装

```bash
sudo dnf install tesseract
```