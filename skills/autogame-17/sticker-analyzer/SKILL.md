---
name: sticker-analyzer
description: 使用 Vision API 分析媒体/贴纸中的图像，以识别和过滤出与表情包/贴纸相关的内容，从而将其与截图或文档区分开来。
tags: [vision, image-analysis, stickers, memes]
---

# Sticker Analyzer 技能

该技能使用 Google Gemini Vision API 分析 `media/stickers` 目录中的图片，以过滤掉非贴纸文件（如截图和文档）。

## 工具

### analyze_stickers
用于运行分析脚本。
- 无需参数。脚本会扫描 `~/.openclaw/media/stickers` 目录中的所有文件。

## 设置要求
1. 需要安装 `npm install @google/generative-ai`。
2. 需要在 `.env` 文件中配置有效的 Google AI Studio API 密钥（GEMINI_API_KEY）。

## 状态
该技能处于激活状态。已配置为使用 Gemini 2.5 Flash 版本，以实现高速贴纸过滤功能。