---
name: agent-tools
description: |
  Run 150+ AI apps via inference.sh CLI - image generation, video creation, LLMs, search, 3D, Twitter automation.
  Models: FLUX, Veo, Gemini, Grok, Claude, Seedance, OmniHuman, Tavily, Exa, OpenRouter, and many more.
  Use when running AI apps, generating images/videos, calling LLMs, web search, or automating Twitter.
  Triggers: inference.sh, infsh, ai model, run ai, serverless ai, ai api, flux, veo, claude api,
  image generation, video generation, openrouter, tavily, exa search, twitter api, grok
allowed-tools: Bash(infsh *)
---

# [inference.sh](https://inference.sh)

![[inference.sh](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kgjw8atdxgkrsr8a2t5peq7b.jpeg)

通过一个简单的命令行界面（CLI），您可以在云端运行150多种AI应用程序，无需使用GPU。

## 安装CLI

```bash
curl -fsSL https://cli.inference.sh | sh
infsh login
```

## 快速示例

```bash
# Generate an image
infsh app run falai/flux-dev-lora --input '{"prompt": "a cat astronaut"}'

# Generate a video
infsh app run google/veo-3-1-fast --input '{"prompt": "drone over mountains"}'

# Call Claude
infsh app run openrouter/claude-sonnet-45 --input '{"prompt": "Explain quantum computing"}'

# Web search
infsh app run tavily/search-assistant --input '{"query": "latest AI news"}'

# Post to Twitter
infsh app run x/post-tweet --input '{"text": "Hello from AI!"}'

# Generate 3D model
infsh app run infsh/rodin-3d-generator --input '{"prompt": "a wooden chair"}'
```

## 命令

| 任务 | 命令                |
|------|-------------------|
| 列出所有应用程序 | `infsh app list`       |
| 搜索应用程序 | `infsh app list --search "flux"`    |
| 按类别筛选 | `infsh app list --category image`   |
| 获取应用程序详情 | `infsh app get google/veo-3-1-fast` |
| 生成样本输入数据 | `infsh app sample google/veo-3-1-fast --save input.json` |
| 运行应用程序 | `infsh app run google/veo-3-1-fast --input input.json` |
| 不等待结果运行 | `infsh app run <app> --input input.json --no-wait` |
| 检查任务状态 | `infsh task get <task-id>`     |

## 可用功能

| 类别 | 示例                |
|----------|-------------------------|
| **图像处理** | FLUX, Gemini 3 Pro, Grok Imagine, Seedream 4.5, Reve, Topaz Upscaler |
| **视频处理** | Veo 3.1, Seedance 1.5, Wan 2.5, OmniHuman, Fabric, HunyuanVideo Foley |
| **大型语言模型（LLMs）** | Claude Opus/Sonnet/Haiku, Gemini 3 Pro, Kimi K2, GLM-4, 任何OpenRouter模型 |
| **搜索** | Tavily Search, Tavily Extract, Exa Search, Exa Answer, Exa Extract |
| **3D处理** | Rodin 3D Generator |
| **Twitter/X平台相关** | 发布推文、创建新推文、发送私信、关注用户、点赞推文、转发推文 |
| **实用工具** | 媒体合并、添加字幕、图像拼接、音频提取 |

## 相关技能

```bash
# Image generation (FLUX, Gemini, Grok, Seedream)
npx skills add inferencesh/skills@ai-image-generation

# Video generation (Veo, Seedance, Wan, OmniHuman)
npx skills add inferencesh/skills@ai-video-generation

# LLMs (Claude, Gemini, Kimi, GLM via OpenRouter)
npx skills add inferencesh/skills@llm-models

# Web search (Tavily, Exa)
npx skills add inferencesh/skills@web-search

# AI avatars & lipsync (OmniHuman, Fabric, PixVerse)
npx skills add inferencesh/skills@ai-avatar-video

# Twitter/X automation
npx skills add inferencesh/skills@twitter-automation

# Model-specific
npx skills add inferencesh/skills@flux-image
npx skills add inferencesh/skills@google-veo

# Utilities
npx skills add inferencesh/skills@image-upscaling
npx skills add inferencesh/skills@background-removal
```

## 参考文件

- [身份验证与设置](references/authentication.md)
- [发现应用程序](references/app-discovery.md)
- [运行应用程序](references/running-apps.md)
- [CLI参考指南](references/cli-reference.md)

## 文档资料

- [代理技能概述](https://inference.sh/blog/skills/skills-overview) - AI功能的开放标准
- [入门指南](https://inference.sh/docs/getting-started/introduction) - inference.sh平台简介
- [什么是inference.sh？](https://inference.sh/docs/getting-started/what-is-inference) - 平台概述
- [应用程序概述](https://inference.sh/docs/apps/overview) - 应用程序生态系统介绍
- [CLI设置](https://inference.sh/docs/extend/cli-setup) - CLI的安装方法
- [工作流程与代理的使用](https://inference.sh/blog/concepts/workflows-vs-agents) - 选择使用方式的建议
- [代理运行时的重要性](https://inference.sh/blog/agent-runtime/why-runtimes-matter) - 运行时的优势