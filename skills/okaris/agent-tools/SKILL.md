---
name: agent-tools
description: "通过 `inference.sh` CLI 运行 150 多个 AI 应用程序，包括图像生成、视频制作、大型语言模型（LLMs）、搜索、3D 处理以及 Twitter 自动化等功能。支持的模型有：FLUX、Veo、Gemini、Grok、Claude、Seedance、OmniHuman、Tavily、Exa、OpenRouter 等。适用于运行 AI 应用程序、生成图像/视频、调用大型语言模型、进行网络搜索或自动化 Twitter 操作。触发命令包括：`inference.sh`、`infsh`、`ai model`、`run ai`、`serverless ai`、`ai api`、`flux`、`veo`、`claude api`、`image generation`、`video generation`、`openrouter`、`tavily`、`exa search`、`twitter api`、`grok`。"
allowed-tools: Bash(infsh *)
---
# [inference.sh](https://inference.sh)

通过一个简单的命令行界面（CLI），您可以在云端运行150多种AI应用程序，无需使用GPU。

![[inference.sh](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kgjw8atdxgkrsr8a2t5peq7b.jpeg)

## 安装CLI

```bash
curl -fsSL https://cli.inference.sh | sh
infsh login
```

> **安装脚本的作用是什么？** [安装脚本](https://cli.inference.sh) 会检测您的操作系统和架构，从 `dist.inference.sh` 下载相应的二进制文件，验证其SHA-256校验和，然后将其添加到您的系统路径（PATH）中。整个过程无需提升权限，也不会启动任何后台进程或收集任何数据。如果您安装了 [cosign](https://docs.sigstore.dev/cosign/system_config/installation/)，安装脚本还会自动验证文件的Sigstore签名。
>
> **手动安装**（如果您不想通过管道将命令传递给 `sh` 命令行）：
> ```bash
> # Download the binary and checksums
> curl -LO https://dist.inference.sh/cli/checksums.txt
> curl -LO $(curl -fsSL https://dist.inference.sh/cli/manifest.json | grep -o '"url":"[^"]*"' | grep $(uname -s | tr A-Z a-z)-$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/') | head -1 | cut -d'"' -f4)
> # Verify checksum
> sha256sum -c checksums.txt --ignore-missing
> # Extract and install
> tar -xzf inferencesh-cli-*.tar.gz
> mv inferencesh-cli-* ~/.local/bin/inferencesh
> ```

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
| 获取应用程序详情 | `infsh app get google/veo-3-1-fast`   |
| 生成示例输入数据 | `infsh app sample google/veo-3-1-fast --save input.json` |
| 运行应用程序 | `infsh app run google/veo-3-1-fast --input input.json` |
| 不等待结果运行 | `infsh app run <app> --input input.json --no-wait` |
| 检查任务状态 | `infsh task get <task-id>`     |

## 可用的应用程序类别

| 类别 | 示例                |
|------|-------------------|
| **图像处理** | FLUX, Gemini 3 Pro, Grok Imagine, Seedream 4.5, Reve, Topaz Upscaler |
| **视频处理** | Veo 3.1, Seedance 1.5, Wan 2.5, OmniHuman, Fabric, HunyuanVideo Foley |
| **大型语言模型（LLMs）** | Claude Opus/Sonnet/Haiku, Gemini 3 Pro, Kimi K2, GLM-4, 任何OpenRouter模型 |
| **搜索功能** | Tavily Search, Tavily Extract, Exa Search, Exa Answer, Exa Extract |
| **3D生成** | Rodin 3D Generator |
| **Twitter/X平台相关** | 发布推文、创建新推文、发送私信、关注用户、点赞推文、转发推文 |
| **实用工具** | 媒体合并、添加字幕、图像拼接、音频提取 |

## 相关技能

```bash
# Image generation (FLUX, Gemini, Grok, Seedream)
npx skills add inference-sh/skills@ai-image-generation

# Video generation (Veo, Seedance, Wan, OmniHuman)
npx skills add inference-sh/skills@ai-video-generation

# LLMs (Claude, Gemini, Kimi, GLM via OpenRouter)
npx skills add inference-sh/skills@llm-models

# Web search (Tavily, Exa)
npx skills add inference-sh/skills@web-search

# AI avatars & lipsync (OmniHuman, Fabric, PixVerse)
npx skills add inference-sh/skills@ai-avatar-video

# Twitter/X automation
npx skills add inference-sh/skills@twitter-automation

# Model-specific
npx skills add inference-sh/skills@flux-image
npx skills add inference-sh/skills@google-veo

# Utilities
npx skills add inference-sh/skills@image-upscaling
npx skills add inference-sh/skills@background-removal
```

## 参考文件

- [身份验证与设置](references/authentication.md)
- [应用程序发现](references/app-discovery.md)
- [应用程序运行](references/running-apps.md)
- [命令行界面参考](references/cli-reference.md)

## 文档资料

- [代理技能概述](https://inference.sh/blog/skills/skills-overview) - AI功能的开放标准
- [入门指南](https://inference.sh/docs/getting-started/introduction) - inference.sh平台简介
- [inference.sh是什么？](https://inference.sh/docs/getting-started/what-is-inference) - 平台概述
- [应用程序概览](https://inference.sh/docs/apps/overview) - 应用程序生态系统介绍
- [命令行界面安装指南](https://inference.sh/docs/extend/cli-setup) - CLI的安装方法
- [工作流程与代理的使用场景](https://inference.sh/blog/concepts/workflows-vs-agents) - 何时使用工作流程或代理
- [为什么运行时性能很重要](https://inference.sh/blog/agent-runtime/why-runtimes-matter) - 运行时性能的优势