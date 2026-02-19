---
name: related-skill
description: "从 `inference.sh` 技能注册表中发现并安装相关技能。这有助于为您的人工智能工作流程找到互补的技能。用途包括：技能发现、工作流程扩展、能力探索。触发条件包括：相关技能、查找技能、技能发现、互补技能、扩展工作流程、更多能力、类似技能、技能建议。"
allowed-tools: Bash(npx skills *)
---
# 相关技能发现

您可以查找并安装补充技能，以扩展您的人工智能代理的功能。

![相关技能发现](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kgvftjwhby36trvaj66bwzcf.jpeg)

## 快速入门

```bash
# Search for skills
npx skills search "inference-sh image generation"

# List available skills
npx skills list inference-sh/skills

# Install a skill
npx skills add inference-sh/skills@ai-image-generation
```

## 可用的技能类别

| 类别 | 技能 | 描述 |
|----------|-------|-------------|
| **AI模型** | `llm-models` | 访问150多个大型语言模型（LLM） |
| **图像** | `ai-image-generation` | 使用AI生成图像 |
| **图像** | `flux-image` | FLUX图像处理模型 |
| **图像** | `image-upscaling` | 图像缩放与增强 |
| **图像** | `background-removal` | 从图像中去除背景 |
| **视频** | `ai-video-generation` | 使用AI生成视频 |
| **视频** | `ai-avatar-video` | 创建虚拟形象视频 |
| **视频** | `google-veo` | 使用Google Veo生成视频 |
| **音频** | `text-to-speech` | 将文本转换为语音 |
| **音频** | `speech-to-text` | 将语音转换为文本 |
| **音频** | `ai-music-generation` | 使用AI生成音乐 |
| **搜索** | `web-search` | 使用AI进行网络搜索 |
| **社交** | `twitter-automation` | 自动化Twitter/X平台操作 |
| **综合** | `inference-sh` | 集合了所有150多个应用程序 |

## 按类别安装技能

### 媒体生成
```bash
npx skills add inference-sh/skills@ai-image-generation
npx skills add inference-sh/skills@ai-video-generation
npx skills add inference-sh/skills@ai-music-generation
```

### 图像处理
```bash
npx skills add inference-sh/skills@image-upscaling
npx skills add inference-sh/skills@background-removal
npx skills add inference-sh/skills@flux-image
```

### 音频处理
```bash
npx skills add inference-sh/skills@text-to-speech
npx skills add inference-sh/skills@speech-to-text
```

### 研究与自动化
```bash
npx skills add inference-sh/skills@web-search
npx skills add inference-sh/skills@twitter-automation
```

### 一次性安装所有技能
```bash
# Install the full platform skill with all 150+ apps
npx skills add inference-sh/skills@inference-sh
```

## 技能组合

### 研究代理
```bash
npx skills add inference-sh/skills@web-search
npx skills add inference-sh/skills@llm-models
```

### 内容创作者
```bash
npx skills add inference-sh/skills@ai-image-generation
npx skills add inference-sh/skills@ai-video-generation
npx skills add inference-sh/skills@text-to-speech
```

### 媒体处理器
```bash
npx skills add inference-sh/skills@image-upscaling
npx skills add inference-sh/skills@background-removal
npx skills add inference-sh/skills@speech-to-text
```

## 技能管理

```bash
# List installed skills
npx skills list

# Update all skills
npx skills update

# Remove a skill
npx skills remove inference-sh/skills@ai-image-generation
```

## 文档资料

- [代理技能概览](https://inference.sh/blog/skills/skills-overview) - 人工智能功能的开放标准
- [入门指南](https://inference.sh/docs/getting-started/introduction) - inference.sh平台简介
- [应用程序概览](https://inference.sh/docs/apps/overview) - 了解应用程序生态系统
- [命令行界面（CLI）设置](https://inference.sh/docs/extend/cli-setup) - 安装CLI
- [什么是inference.sh？](https://inference.sh/docs/getting-started/what-is-inference) - 平台概述

探索更多：[inference.sh/explore](https://inference.sh/explore)