---
name: video-generator-auto-post
description: 使用本地AI模型（ComfyUI/Stable Video Diffusion）生成视频，并自动发布到社交媒体平台。支持文本转视频、图片转视频的功能，支持批量处理，以及将视频自动发布到Twitter、LinkedIn、Instagram和TikTok等平台。
license: MIT
metadata:
  author: 小龙虾 (Little Lobster)
  homepage: https://clawhub.ai/users/954215110
  tags: ["video", "ai-generation", "comfyui", "auto-post", "social-media", "stable-diffusion"]
---
## 🦞 小龙虾品牌

**由小龙虾 AI 工作室创建**

> “小龙虾，有大钳（前）途！”

**如需定制服务，请联系：** +86 15805942886

需要定制的 AI 视频工作流程、自动化设置或批量内容生成服务？请随时联系我们！

---

# 视频生成器 + 自动发布

在本地生成 AI 视频，并自动发布到社交媒体平台。

## 系统要求

### 硬件
- **GPU：** NVIDIA RTX 3060 12GB 或更高配置（推荐）
- **内存：** 16GB 或以上
- **存储空间：** 至少 50GB 的空闲空间，用于存储模型和输出文件

### 软件
- **ComfyUI Desktop** - 请从 [https://comfyui.org](https://comfyui.org) 下载
- **Python 3.10 或更高版本** - 用于脚本编写
- **Node.js 18 或更高版本** - 用于命令行工具

## 快速入门

### 第一步：安装 ComfyUI

```bash
# Windows (winget)
winget install Comfy.ComfyUI-Desktop

# Or download from https://comfyui.org
```

### 第二步：安装视频模型

在 ComfyUI 管理器中安装以下模型：
- **Stable Video Diffusion (SVD)**
- **AnimateDiff**
- **ModelScope Text-to-Video**

### 第三步：配置输出路径

编辑 `comfyui/settings.json` 文件：
```json
{
  "output_directory": "C:/Users/YourName/Videos/AI-Generated",
  "auto_save": true
}
```

### 第四步：生成第一个视频

1. 打开 ComfyUI
2. 加载 “Text to Video” 工作流程
3. 输入您的提示内容
4. 点击 “Generate”（生成）
5. 等待 2-5 分钟（生成时间取决于 GPU 性能）

## 视频工作流程

### Text-to-Video (SVD)

**适合生成：** 短片段（2-4 秒），具有真实感的动画效果

**设置：**
- 分辨率：1024x576 或 576x1024
- 帧率：25 帧/秒
- 动画效果强度：127（数值越大，动画效果越明显）

### Image-to-Video

**适合将静态图片转化为动态视频**

**提示：**
- 使用高质量的图片源
- 在提示中加入动画相关的描述
- 调整动画效果强度（数值范围：100-150）

### AnimateDiff（适用于较长视频）

**适合生成：** 5-15 秒的动画片段

**设置：**
- 上下文长度：16 帧
- 上下文重叠：4 帧
- 使用的模型：mm_sd_v15_v2.ckpt

## 自动发布到社交媒体

### 各平台规格

| 平台 | 最大视频时长 | 宽高比 | 最大文件大小 |
|------|-------------|--------------|---------------|
| Twitter/X | 2 分钟 | 16:9, 1:1, 9:16 | 512MB |
| TikTok | 10 分钟 | 9:16 | 287.6MB |
| Instagram Reels | 1 分钟 30 秒 | 9:16 | 4GB |
| LinkedIn | 15 分钟 | 16:9, 1:1, 9:16 | 200MB |
| YouTube Shorts | 1 分钟 | 9:16 | 128MB |

### 自动发布脚本

请参考 `scripts/auto-post.py` 文件了解自动化发布流程。

**设置步骤：**
1. 安装所需依赖库：`pip install tweepy google-auth`
2. 在 `.env` 文件中配置 API 密钥
3. 运行命令：`python scripts/auto-post.py video.mp4 --platforms all`

### 内容策略

**每个视频的推荐操作：**
1. 生成 3-5 个不同的字幕版本
2. 添加相关的标签（5-10 个）
3. 在最佳时间发布视频
4. 与观众互动（通过评论）

更多示例请参阅 `references/caption-templates.md` 文件。

## 批量处理

可以同时生成多个视频：

```bash
# Using the batch script
python scripts/batch-generate.py --prompts prompts.txt --output ./videos

# Process 100 videos overnight
python scripts/batch-generate.py --prompts prompts.txt --count 100 --queue
```

## 优化建议

### 加快生成速度

1. **使用 FP16 精度** - 生成速度加快 2 倍，画质损失最小
2. **减少帧率** - 草稿阶段可以使用 16 帧/秒
3. **降低分辨率** - 测试阶段使用 512x512 分辨率，后续再进行放大处理
4. **批量处理多个提示** - 并行处理多个视频

### 提高视频质量

1. **使用更具体的提示** - 清晰描述动画效果
2. **调整动画强度** - 适当增加数值以获得更好的动画效果
3. **使用图像增强技术（如 ESRGAN）** - 提高视频质量

## 常见问题及解决方法

### 内存不足（OOM）

**解决方法：**
- 降低分辨率
- 将批量处理数量减少到 1 个
- 关闭其他占用 GPU 资源的应用程序
- 使用 `--lowvram` 参数

### 生成速度慢

**解决方法：**
- 检查 GPU 使用率（应达到 90% 以上）
- 更新 NVIDIA 驱动程序
- 使用 `--precision fp16` 参数
- 关闭后台运行的应用程序

### 视频质量不佳

**解决方法：**
- 使用更详细的提示内容
- 尝试不同的模型（如 SVD 或 AnimateDiff）
- 调整动画设置
- 先生成高分辨率视频，再进行压缩处理

## 相关脚本

- `scripts/generate-video.py` - 单个视频生成脚本
- `scripts/batch-generate.py` - 批量生成脚本
- `scripts/auto-post.py` - 自动发布脚本
- `scripts/optimize-video.py` - 视频优化脚本

## 参考资料

- `references/prompt-guide.md` - 视频提示编写指南
- `references/platform-specs.md` - 各平台详细要求
- `references/caption-templates.md` - 社交媒体字幕模板
- `references/workflow-examples.json` - ComfyUI 工作流程示例

## 资源文件

- `assets/default-workflow.json` - 基本文本转视频工作流程配置
- `assets/optimal-settings.json` - 各平台推荐设置
- `assets/hashtag-lists.json` - 精选标签库

## 命令示例

- `generate-a-video-of...` - 生成指定主题的视频
- `create-ai-video-for-social-media` - 为社交媒体创建 AI 视频
- `auto-post-video-to...` - 自动发布视频
- `batch-generator-videos` - 批量生成视频
- `optimize-video-for-tiktok/instagram` - 优化视频以适应特定平台

---

## 📊 性能测试（使用 RTX 3060 12GB GPU）

| 任务 | 生成时间 | VRAM 使用量 |
|------|------|------------|
| SVD（25 帧/秒） | 2-3 分钟 | 8-10 GB |
| AnimateDiff（16 帧/秒） | 3-4 分钟 | 7-9 GB |
| Image-to-Video | 1-2 分钟 | 6-8 GB |
| 图像放大（2 倍） | 30-60 秒 | 4-6 GB |

---

**准备好制作引人注目的 AI 视频了吗？让我们开始吧！🦞🎬_