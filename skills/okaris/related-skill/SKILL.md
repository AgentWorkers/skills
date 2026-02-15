---
name: related-skill
description: |
  Discover and install related skills from inference.sh skill registry.
  Helps find complementary skills for your AI workflow.
  Use for: skill discovery, workflow expansion, capability exploration.
  Triggers: related skills, find skills, skill discovery, complementary skills,
  expand workflow, more capabilities, similar skills, skill suggestions
allowed-tools: Bash(npx skills *)
---

# 相关技能发现

寻找并安装互补技能，以扩展您的人工智能代理的功能。

## 快速入门

```bash
# Search for skills
npx skills search "inference-sh image generation"

# List available skills
npx skills list inference-sh/agent-skills

# Install a skill
npx skills add inference-sh/agent-skills@ai-image-generation
```

## 可用的技能类别

| 类别 | 技能 | 描述 |
|----------|-------|-------------|
| **AI模型** | `llm-models` | 访问150多种大型语言模型（LLM） |
| **图像** | `ai-image-generation` | 使用AI生成图像 |
| **图像** | `flux-image` | FLUX图像处理模型 |
| **图像** | `image-upscaling` | 图像缩放与增强 |
| **图像** | `background-removal` | 从图像中去除背景 |
| **视频** | `ai-video-generation` | 使用AI生成视频 |
| **视频** | `ai-avatar-video` | 创建头像视频 |
| **视频** | `google-veo` | 使用Google Veo生成视频 |
| **音频** | `text-to-speech` | 将文本转换为语音 |
| **音频** | `speech-to-text` | 将语音转换为文本 |
| **音频** | `ai-music-generation` | 使用AI生成音乐 |
| **搜索** | `web-search` | 使用AI进行网络搜索 |
| **社交** | `twitter-automation` | 自动化Twitter/X平台的操作 |
| **综合** | `inference-sh` | 集合了所有150多种技能的应用 |

## 按类别安装

### 媒体生成
```bash
npx skills add inference-sh/agent-skills@ai-image-generation
npx skills add inference-sh/agent-skills@ai-video-generation
npx skills add inference-sh/agent-skills@ai-music-generation
```

### 图像处理
```bash
npx skills add inference-sh/agent-skills@image-upscaling
npx skills add inference-sh/agent-skills@background-removal
npx skills add inference-sh/agent-skills@flux-image
```

### 音频处理
```bash
npx skills add inference-sh/agent-skills@text-to-speech
npx skills add inference-sh/agent-skills@speech-to-text
```

### 研究与自动化
```bash
npx skills add inference-sh/agent-skills@web-search
npx skills add inference-sh/agent-skills@twitter-automation
```

### 一次性安装所有技能
```bash
# Install the full platform skill with all 150+ apps
npx skills add inference-sh/agent-skills@inference-sh
```

## 技能组合

### 研究代理
```bash
npx skills add inference-sh/agent-skills@web-search
npx skills add inference-sh/agent-skills@llm-models
```

### 内容创作者
```bash
npx skills add inference-sh/agent-skills@ai-image-generation
npx skills add inference-sh/agent-skills@ai-video-generation
npx skills add inference-sh/agent-skills@text-to-speech
```

### 媒体处理工具
```bash
npx skills add inference-sh/agent-skills@image-upscaling
npx skills add inference-sh/agent-skills@background-removal
npx skills add inference-sh/agent-skills@speech-to-text
```

## 管理技能

```bash
# List installed skills
npx skills list

# Update all skills
npx skills update

# Remove a skill
npx skills remove inference-sh/agent-skills@ai-image-generation
```

## 文档资料

- [代理技能概览](https://inference.sh/blog/skills/agent-skills-overview) - 人工智能功能的开放标准
- [入门指南](https://inference.sh/docs/getting-started/introduction) - inference.sh平台简介
- [应用概览](https://inference.sh/docs/apps/overview) - 了解应用生态系统
- [命令行界面设置](https://inference.sh/docs/extend/cli-setup) - 安装命令行界面
- [什么是inference.sh？](https://inference.sh/docs/getting-started/what-is-inference) - 平台概述

探索更多：[inference.sh/explore](https://inference.sh/explore)