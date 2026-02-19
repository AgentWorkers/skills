---
name: nvidia-kimi-vision
description: 使用 NVIDIA Kimi K2.5 视觉模型通过 NVIDIA NIM API 分析图像。非常适合为那些没有内置图像处理功能的模型（如 MiniMax M2.5、GLM-5 等）添加图像处理能力。支持处理 png、jpg、jpeg 和 webp 格式的图像文件。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"] },
        "install":
          [
            {
              "id": "python",
              "kind": "system",
              "label": "Install Python dependencies (requests)",
            },
          ],
      },
  }
---
# NVIDIA Kimi Vision

使用 NVIDIA NIM 提供的 Kimi K2.5 多模态模型进行快速图像分析。

## 为什么选择这个技能？

- **速度快**：NVIDIA NIM 的推理速度非常快。
- **质量高**：Kimi K2.5 是一个性能出色的视觉模型。
- **使用简单**：只需传递一张图片和一个提示即可。
- **免费 tier**：可通过 NVIDIA 的 build.nvidia.com 获取免费 API 密钥。

## API 设置（非常重要）

在使用此技能时，如果未找到 API 密钥，系统会自动引导用户完成设置：

### 第一步：获取免费 API 密钥
1. 访问 **https://build.nvidia.com**
2. 使用 GitHub 或 Google 注册/登录
3. 搜索 “Kimi K2.5”
4. 点击该模型以获取免费的 API 密钥

### 第二步：保存密钥
```bash
# Option A: Save to file (recommended)
mkdir -p ~/.config
echo 'your-api-key-here' > ~/.config/nvidia-kimi-api-key

# Option B: Pass directly when running
python3 scripts/analyze_image.py photo.jpg "What's this?" sk-your-key-here
```

### 首次使用时的设置（针对代理）
当用户在没有 API 密钥的情况下尝试使用此技能时，脚本会提供详细的设置说明：
1. 访问 https://build.nvidia.com
2. 获取免费的 API 密钥
3. 将密钥保存到 ~/.config/nvidia-kimi-api-key 文件中

## 使用方法

```bash
python3 scripts/analyze_image.py <image_path> "<prompt>" [api_key]
```

### 示例

```bash
# What's in this image?
python3 scripts/analyze_image.py "/path/to/image.jpg" "Describe what's in this image"

# Extract text from screenshot
python3 scripts/analyze_image.py "/path/screenshot.png" "Extract all text"

# Analyze a meme
python3 scripts/analyze_image.py "/path/meme.jpg" "Explain this meme"

# With API key inline
python3 scripts/analyze_image.py photo.jpg "What's this?" sk-xxxxx
```

## 图像格式支持

支持的图像格式：png、jpg、jpeg、webp

## 使用限制

NVIDIA NIM 的免费 tier 有一些使用限制，但这些限制在官网上的说明并不清晰。请访问 https://build.nvidia.com 以获取关于您的 API 密钥的具体使用限制信息。