---
name: pixverse
description: "使用 Pixverse API 生成高质量的人工智能视频——支持文本转视频、图片转视频以及视频扩展功能。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "bins": ["pixverse"], "env": ["PIXVERSE_API_KEY"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": ".",
              "bins": ["pixverse"],
              "label": "Build pixverse skills (npm)",
            },
          ],
      },
  }
---
# Pixverse Skills

这是一套专为 Claude Code 和 OpenClaw 设计的 AI 视频生成工具集。

## 主要功能

- **文本转视频**：根据文本描述生成视频
- **图片转视频**：将静态图片转换为动态视频
- **视频扩展**：能够无缝地添加新的视频片段到现有视频中

## 安装步骤

1. 从 [Pixverse 平台](https://platform.pixverse.ai) 获取您的 API 密钥。
2. 设置环境变量：
   ```bash
   export PIXVERSE_API_KEY="sk-your-api-key"
   ```
3. 打开技能目录的链接：
   ```bash
   # For Claude Code
   ln -s $(pwd) ~/.claude/skills/pixverse

   # For OpenClaw
   ln -s $(pwd) ~/.openclaw/skills/pixverse
   ```

## 使用方法

### 从文本生成视频

```
Please generate a video of a cat playing piano
```

或者直接使用该技能：
```
/gen_video {"prompt": "a cat playing piano", "duration": 5, "resolution": "720p"}
```

### 将图片转换为视频

```
Animate this image: /path/to/photo.jpg with a slow zoom in effect
```

### 向视频中添加新片段

```
Extend this video: /path/to/clip.mp4 by 5 seconds
```

## 系统要求

- Node.js 20 及以上版本
- Pixverse API 密钥
- 互联网连接

## 技术支持

- 官方文档：https://docs.platform.pixverse.ai
- GitHub 仓库：https://github.com/PixVerseAI/Pixverse-Skills