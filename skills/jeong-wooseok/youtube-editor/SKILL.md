---
name: youtube-editor
description: 自动化YouTube视频编辑工作流程：  
**下载 -> 语音转文字（Whisper） -> 分析（GPT-4） -> 制作高质量缩略图（支持韩文显示及字符一致性）**
version: 1.0.14
author: Flux
requiredEnvVars:
  - OPENAI_API_KEY
optionalEnvVars:
  - NANO_BANANA_KEY
---

# 🎬 YouTube AI编辑器（v1.0.14）

## ⚠️ 安全提示

由于该技能包含合法的自动化功能，可能会触发安全警告：

**所需权限：**
- **API密钥**：需要 `OPENAI_API_KEY`（用于Whisper/GPT-4）和 `NANO_BANANA_KEY`（用于AI图像生成，可选）
- **子进程执行**：使用 `ffmpeg` 进行视频处理（标准视频编辑工具）
- **跨技能集成**：调用 `nano-banana-pro` 技能进行AI图像生成（可选功能）
  - 仅当用户安装了 `nano-banana-pro` 时才会执行
  - 使用固定的脚本路径，并具有超时保护机制
- **文件读写**：读取用户指定的头像/字体文件，并将输出文件（缩略图、字幕）写入工作目录

**安全措施：**
- YouTube URL验证（阻止本地主机/私有IP的访问）
- HTML转义文本渲染
- 子进程超时限制（最长900秒）
- 固定的脚本路径（防止任意代码执行）

所有代码均为开源，可审计。如果使用图像生成功能，请单独审查 `nano-banana-pro` 的代码。

---

**只需几分钟，即可将原始视频转换为适合在YouTube上发布的格式。**

该技能可自动化视频制作的繁琐环节，现在还支持**完整的韩文支持**和**一致的字符生成**！

---

## ✨ 功能特点

- **📥 通用下载**：支持YouTube URL和本地视频文件。
- **🗣️ 自动字幕**：使用OpenAI Whisper生成准确的`.srt`字幕。
- **🧠 内容分析**：利用GPT-4生成**韩文**的SEO优化标题、描述和标签。
- **🎨 AI缩略图（专业版）**：
  - **保持一致性**：在生成新姿势时，会保留您的头像风格（或默认的海盗龙虾风格）！（图像到图像转换）
  - **自定义字体**：支持使用Paperlogy ExtraBold字体。
  - **背景去除**：自动去除生成字符的背景。
  - **布局**：采用专业的黑金设计。
- **🛡️ 安全强化（v1.0.11）**：
  - YouTube URL白名单验证（阻止本地主机/私有网络的访问）
  - 缩略图模板中的HTML转义文本渲染
  - 更安全的Nano Banana脚本执行机制及子进程超时设置

---

## 🛠️ 依赖项

### 1. 系统工具
需要安装 **FFmpeg**（通过您的包管理器进行安装）。

### 2. Python包（可选）
如需高级缩略图功能，请安装：
- `playwright` + `rembg[cpu]`

### 3. API密钥（环境变量）
运行前请设置以下变量：
- `OPENAI_API_KEY` - 用于Whisper和GPT-4
- `NANO_BANANA_KEY` - 用于AI字符生成

---

## 🚀 使用方法

### 选项1：全自动模式（海盗龙虾风格）
AI会生成一个与您的视频内容相关的**海盗龙虾角色**，同时保持原始角色的设计风格一致。

```bash
# Run from skills/youtube-editor/
uv run scripts/process_video.py --url "https://youtube.com/watch?v=YOUR_VIDEO_ID"
```

### 选项2：自定义品牌（使用您的照片）
使用您自己的照片作为头像。AI会生成**“您”执行不同动作**的场景！

```bash
uv run scripts/process_video.py \
  --input "video.mp4" \
  --author "My Awesome Channel" \
  --avatar "/path/to/my_face.jpg"
```

---

*由Flux（OpenClaw Agent）创建*