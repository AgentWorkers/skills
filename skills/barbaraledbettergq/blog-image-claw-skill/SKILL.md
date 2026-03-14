---
name: blog-image-claw-skill
description: 自动为博客文章生成匹配的英雄图片（hero images）和内联图片（inline images）。该代理会读取文章内容，从中提取视觉元素，并生成一套可直接使用的图片资源。
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - NETA_TOKEN
      bins:
        - node
    primaryEnv: NETA_TOKEN
    emoji: "📝"
    homepage: https://github.com/BarbaraLedbettergq/blog-image-claw-skill
---
# 博文图片生成技能（Blog Image Generation Skill）

该代理会读取博客内容（文本、文件或URL），为页面中的主要元素（如标题、正文等）生成相应的视觉提示，随后调用 `blogimg.js` 脚本来生成图片。

## 辅助脚本（Helper Script）

```bash
node blogimg.js gen "<visual_prompt>" --size header|inline
# → {"status":"SUCCESS","url":"https://...","width":1024,"height":576}
```

该辅助脚本负责处理所有的内容分析工作，仅负责调用图片生成相关的 API。

## 配置（Setup）

```
NETA_TOKEN=your_token_here
```
在 `~/.openclaw/workspace/.env` 文件中：