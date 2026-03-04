---
name: imgbb-api
description: Upload images to ImgBB and get shareable URLs. Use when: (1) User wants to upload images to imgbb, (2) Need to get direct image URLs for sharing, (3) Converting local images to shareable links, (4) Bulk uploading images, (5) Uploading from URL, (6) Base64 encoding.
version: 1.1.0
changelog: "v1.1.0: Added reasoning framework, decision tree, troubleshooting"
metadata:
  openclaw:
    requires:
      bins:
        - python3
      pip:
        - requests
      env:
        - IMGBB_API_KEY
    emoji: "📸"
    category: "utility"
    homepage: https://github.com/KeXu9/imgbb-api
---

# ImgBB API

用于将图片上传到ImgBB并获取可分享的URL。

## 该技能的触发条件

当用户希望将图片上传到网上以供分享时，此技能会被触发。

## 动作流程

| 步骤 | 操作 | 原因 |
|------|--------|-----|
| 1 | **检查** | 确认API密钥是否可用 |
| 2 | **准备** | 获取图片的路径或URL |
| 3 | **上传** | 将图片发送到ImgBB API |
| 4 | **返回** | 返回可分享的URL |

---

## 设置

```bash
export IMGBB_API_KEY="your_api_key_here"
# or
echo "your_api_key" > ~/.imgbb_api_key
```

## 获取API密钥

1. 访问 https://api.imgbb.com/
2. 点击“获取API密钥”
3. 复制您的API密钥

---

## 使用方法

```bash
# Upload file
python imgbb.py image.jpg

# With custom API key
python imgbb.py image.jpg --key YOUR_KEY

# From URL
python imgbb.py --url "https://..."

# Batch upload
python imgbb.py --batch ./folder/

# JSON output
python imgbb.py image.jpg --json
```

## 参数选项

| 参数 | 说明 |
|------|-------------|
| `image` | 图片的路径 |
| `--key` | API密钥 |
| `--url` | 从URL上传图片 |
| `--name` | 自定义图片名称 |
| `--expiration` | 图片的有效期（秒） |
| `--json` | 以JSON格式输出结果 |
| `--batch` | 批量处理文件夹中的图片 |
| `--set-key` | 保存API密钥 |

---

## 常见问题及解决方法

### 问题：未找到API密钥
- 解决方案：设置`IMGBB_API_KEY`环境变量或使用`--key`参数。

### 问题：文件未找到
- 解决方案：检查文件路径是否正确。

### 问题：图片格式无效
- 解决方案：仅支持JPG、PNG、GIF或WEBP格式的图片。

### 问题：图片过大
- 解决方案：将图片压缩至32MB以下。

---

## 快速参考

| 功能 | 命令示例 |
|------|---------|
| 上传图片 | `python imgbb.py image.jpg` |
| 从URL上传图片 | `python imgbb.py --url "URL"` |
| 批量处理图片 | `python imgbb.py --batch ./folder/` |
| 以JSON格式输出结果 | `python imgbb.py image.jpg --json` |