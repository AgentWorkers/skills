---
name: qrcode-generator
description: "从文本、URL或图片生成二维码。当用户请求“生成二维码”、“创建二维码”或“为……制作二维码”时可以使用该功能。支持文本内容、URL以及本地图片（会自动压缩）。"
version: 2.0.0
author: bowen nan
license: MIT
permissions: file read (specified image paths), file write (temp directory)
---
# QR码生成器

该工具可以从文本、URL或本地图片生成QR码，非常适合用于分享链接、联系信息或小型图片。

## 主要功能
- ✅ 从文本生成QR码  
- ✅ 从URL生成QR码  
- ✅ 从本地图片生成QR码（自动压缩）  
- ✅ 可自定义QR码的大小和颜色  
- ✅ 提供生成的QR码图片的路径，便于分享  

## 安装  
```bash
pip install qrcode[pil] pillow
```  

## 使用示例  

### 基本用法  
```python
from agent import handle_call

# Generate QR for URL
result = handle_call({"content": "https://openclaw.ai"})

# Generate QR for text
result = handle_call({"content": "Hello OpenClaw"})

# Generate QR from image
result = handle_call({"image": "/path/to/image.jpg"})
```  

### 命令行用法  
```bash
# Install dependencies first
pip install qrcode[pil] pillow

# Run the example
python example.py
```  

## 参数  
- `content` (string): 需要编码的文本或URL  
- `image` (string): 本地图片文件的完整路径  

## 返回值  
- `image_path`: 生成的QR码图片的路径  
- `error`: 如果生成失败，返回错误信息  
- `message`: 提供有关操作状态的信息  

## 注意事项  
- 大于10MB的图片将无法被生成为QR码  
- 大型图片在生成QR码时会自动压缩  
- 为了获得最佳效果，请使用URL而不是本地图片文件  

---