---
name: pixverse
description: "使用 PixVerse API 生成高质量的人工智能视频——支持文本转视频、图片转视频以及视频扩展功能。"
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
# PixVerse 技能

为 Claude Code 和 OpenClaw 提供的 AI 视频生成功能。

## 特点

- **文本转视频**：根据文本描述生成视频
- **图片转视频**：将静态图片制作成动画
- **视频扩展**：无缝扩展现有视频

## 安装

1. 从 [PixVerse 平台](https://platform.pixverse.ai) 获取您的 API 密钥
2. 设置环境变量：
   ```bash
   export PIXVERSE_API_KEY="sk-your-api-key"
   ```
3. 链接到技能目录：
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

### 图片转视频

```
Animate this image: /path/to/photo.jpg with a slow zoom in effect
```

### 扩展视频

```
Extend this video: /path/to/clip.mp4 by 5 seconds
```

## 系统要求

- Node.js 20 及以上版本
- PixVerse API 密钥
- 互联网连接

## 支持资源

- 文档：https://docs.platform.pixverse.ai
- GitHub 仓库：https://github.com/PixVerseAI/PixVerse-Skills