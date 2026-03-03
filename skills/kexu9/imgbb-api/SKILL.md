---
name: imgbb-api
description: Upload images to ImgBB and get shareable URLs. Use when: (1) User wants to upload images to imgbb, (2) Need to get direct image URLs for sharing, (3) Converting local images to shareable links, (4) Bulk uploading images, (5) Uploading from URL, (6) Base64 encoding.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - IMGBB_API_KEY
    primaryEnv: IMGBB_API_KEY
    emoji: "📸"
    homepage: https://github.com/KeXu9/imgbb-api
---

# ImgBB API

这是一个免费的图片托管API，支持上传图片并生成可分享的URL。

## 设置

**选项1：环境变量（推荐）**
```bash
export IMGBB_API_KEY="your_api_key_here"
```

**选项2：配置文件**
创建一个名为`~/.imgbb_api_key`的文件，将您的API密钥保存在其中。

**选项3：作为参数传递**
```bash
python scripts/imgbb.py image.jpg --key YOUR_API_KEY
```

## 获取API密钥

1. 访问 https://api.imgbb.com/
2. 点击“获取API密钥”
3. 复制您的API密钥

## 上传方法

### 1. 本地文件
```bash
curl -s -X POST "https://api.imgbb.com/1/upload?key=YOUR_KEY" -F "image=@/path/to/image.jpg"
```

### 2. 从URL上传
```bash
curl -s -X POST "https://api.imgbb.com/1/upload?key=YOUR_KEY" -F "image=https://example.com/image.jpg"
```

### 3. 使用Base64编码上传
```bash
curl -s -X POST "https://api.imgbb.com/1/upload?key=YOUR_KEY" -F "image=base64_data"
```

### 4. 带有有效期（60-15552000秒）
```bash
curl -s -X POST "https://api.imgbb.com/1/upload?key=YOUR_KEY&expiration=3600" -F "image=@image.jpg"
```

## 脚本使用示例
```bash
# Upload file (uses IMGBB_API_KEY env or ~/.imgbb_api_key)
python scripts/imgbb.py /path/to/image.jpg

# With custom API key
python scripts/imgbb.py /path/to/image.jpg --key YOUR_KEY

# With name
python scripts/imgbb.py image.jpg --name custom_name

# With expiration
python scripts/imgbb.py image.jpg --expiration 3600

# From URL
python scripts/imgbb.py --url "https://..."

# JSON output
python scripts/imgbb.py image.jpg --json

# Batch upload
python scripts/imgbb.py --batch /folder/
```

## 响应字段

| 字段 | 描述 |
|-------|-------------|
| `url` | 图片的直接URL |
| `url_viewer` | 图片的查看页面 |
| `thumb.url` | 图片的缩略图URL |
| `delete_url` | 删除图片的链接 |
| `width` | 图片的宽度 |
| `height` | 图片的高度 |
| `size` | 图片的大小（字节） |

## 优先级

API密钥的获取顺序如下：
1. `--key` 参数（优先级最高）
2. `IMGBB_API_KEY` 环境变量
3. `~/.imgbb_api_key` 配置文件

## 所需依赖库

- Python 3
- `requests` 库（使用 `pip install requests` 安装）