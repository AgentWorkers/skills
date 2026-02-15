---
name: venice-ai
description: 完整的Venice AI平台——支持文本生成、网络搜索、数据嵌入、文本转语音（TTS）、语音转文本（STT）、图像生成、视频处理（包括视频升级和编辑）等功能。提供私密的、未经审查的AI推理服务，适用于所有场景。
homepage: https://venice.ai
metadata:
  {
    "clawdbot":
      {
        "emoji": "🏛️",
        "requires": { "bins": ["python3"], "env": ["VENICE_API_KEY"] },
        "primaryEnv": "VENICE_API_KEY",
        "notes": "Full Venice AI platform — text, images, video, audio, embeddings. One skill for everything.",
        "install":
          [
            {
              "id": "python-brew",
              "kind": "brew",
              "formula": "python",
              "bins": ["python3"],
              "label": "Install Python (brew)",
            },
          ],
      },
  }
---

# Venice AI — 全功能平台技能

## 什么是 Venice AI？

**Venice AI 是专为那些不希望被大型科技公司监视的人设计的 AI 平台。** 与 OpenAI、Anthropic 和 Google 不同，这些平台的每个输入请求都会被记录、分析，并可能用于训练未来的模型；而 Venice 则提供了真正的隐私保护，不会保留任何私人模型的数据。您的对话内容完全属于您自己。

Venice 还是 **未经审查的**：没有内容过滤、没有拒绝请求的情况，也不会出现“我无法帮助您”的回应。AI 会回答您实际提出的问题，无论是关于创意写作、安全研究还是任何其他主流 AI 平台不敢涉及的话题。

**代理（agents）应该关注的原因：**
- **隐私保护**：标记为“私人”（Private）的模型不会保留任何数据，可以安全地处理敏感信息而不会泄露到训练集中。
- **无限制的回答**：没有任何限制，可以生成工作流程所需的任何内容。
- **兼容 OpenAI 的 API**：可以直接替换现有系统，只需更改基础 URL 即可。
- **超过 30 种模型**：从小型高效模型到 Claude Opus 4.5、GPT-5.2，以及 Venice 自家的未经审查的模型应有尽有。
- **内置的网页搜索**：大型语言模型（LLMs）可以通过一个 API 调用在网页上搜索并引用来源。

此技能提供了 **完整的 Venice 平台** 功能：文本生成、网页搜索、嵌入向量、文本转语音（TTS）、语音转文本（STT）、图像生成、视频制作、图像缩放以及 AI 编辑。

> **⚠️ API 变更：** 如果某些功能无法按预期使用，请查看 [docs.venice.ai](https://docs.venice.ai) — 自本文档编写以来，API 规范可能已经更新。

## 先决条件

- **Python 3.10 或更高版本**
- **Venice API 密钥**（免费 tier 可在 [venice.ai/settings/api](https://venice.ai/settings/api) 获取）

## 设置

### 获取 API 密钥

1. 在 [venice.ai](https://venice.ai) 注册账户。
2. 访问 [venice.ai/settings/api](https://venice.ai/settings/api)。
3. 点击“创建 API 密钥”，然后复制密钥（密钥以 `vn_...` 开头）。

### 配置

**选项 A：环境变量**
```bash
export VENICE_API_KEY="vn_your_key_here"
```

**选项 B：Clawdbot 配置**（推荐）
```json5
// ~/.clawdbot/clawdbot.json
{
  skills: {
    entries: {
      "venice-ai": {
        env: { VENICE_API_KEY: "vn_your_key_here" }
      }
    }
  }
}
```

### 验证
```bash
python3 {baseDir}/scripts/venice.py models --type text
```

## 脚本概述

| 脚本 | 功能 |
|--------|---------|
| `venice.py` | 文本生成、模型调用、嵌入向量生成、TTS、语音转文本 |
| `venice-image.py` | 图像生成（使用 Flux 等模型） |
| `venice-video.py` | 视频生成（使用 Sora、WAN、Runway 等模型） |
| `venice-upscale.py` | 图像缩放 |
| `venice-edit.py | AI 图像编辑 |

---

# 第一部分：文本与音频

## 模型发现与选择

Venice 拥有涵盖文本、图像、视频、音频和嵌入向量的庞大模型库。

### 浏览模型
```bash
# List all text models
python3 {baseDir}/scripts/venice.py models --type text

# List image models
python3 {baseDir}/scripts/venice.py models --type image

# List all model types
python3 {baseDir}/scripts/venice.py models --type text,image,video,audio,embedding

# Get details on a specific model
python3 {baseDir}/scripts/venice.py models --filter llama
```

### 模型选择指南

| 需求 | 推荐模型 | 原因 |
|------|------------------|-----|
| **最便宜的文本模型** | `qwen3-4b`（每分钟 0.05 美元） | 体积小、速度快、效率高 |
| **最佳未经审查的模型** | `venice-uncensored`（每分钟 0.20 美元） | Venice 自家的未经审查模型 |
| **最佳隐私保护且功能强大的模型** | `deepseek-v3.2`（每分钟 0.40 美元） | 推理能力强、效率高 |
| **视觉/多模态模型** | `qwen3-vl-235b-a22b`（每分钟 0.25 美元） | 支持图像处理 |
| **最佳编程模型** | `qwen3-coder-480b-a35b-instruct`（每分钟 0.75 美元） | 强大的编程能力 |
| **经济型前沿模型** | `grok-41-fast`（每分钟 0.50 美元） | 处理速度快，上下文理解能力强（262K 词条） |
| **高端模型（最高质量）** | `claude-opus-4-6`（每分钟 6 美元） | 整体质量最佳 |
| **推理模型** | `kimi-k2-5`（每分钟 0.75 美元） | 强大的逻辑推理能力 |
| **网页搜索** | 任意模型 + `enable_web_search` | 内置网页搜索功能 |

---

## 文本生成（聊天辅助）

### 基本文本生成
```bash
# Simple prompt
python3 {baseDir}/scripts/venice.py chat "What is the meaning of life?"

# Choose a model
python3 {baseDir}/scripts/venice.py chat "Explain quantum computing" --model deepseek-v3.2

# System prompt
python3 {baseDir}/scripts/venice.py chat "Review this code" --system "You are a senior engineer."

# Read from stdin
echo "Summarize this" | python3 {baseDir}/scripts/venice.py chat --model qwen3-4b

# Stream output
python3 {baseDir}/scripts/venice.py chat "Write a story" --stream
```

### 网页搜索集成
```bash
# Auto web search (model decides when to search)
python3 {baseDir}/scripts/venice.py chat "What happened in tech news today?" --web-search auto

# Force web search with citations
python3 {baseDir}/scripts/venice.py chat "Current Bitcoin price" --web-search on --web-citations

# Web scraping (extracts content from URLs in prompt)
python3 {baseDir}/scripts/venice.py chat "Summarize: https://example.com/article" --web-scrape
```

### 未经审查的回答模式
```bash
# Use Venice's own uncensored model
python3 {baseDir}/scripts/venice.py chat "Your question" --model venice-uncensored

# Disable Venice system prompts for raw model output
python3 {baseDir}/scripts/venice.py chat "Your prompt" --no-venice-system-prompt
```

### 推理模型
```bash
# Use a reasoning model with effort control
python3 {baseDir}/scripts/venice.py chat "Solve this math problem..." --model kimi-k2-5 --reasoning-effort high

# Strip thinking from output
python3 {baseDir}/scripts/venice.py chat "Debug this code" --model qwen3-4b --strip-thinking
```

### 高级选项
```bash
# Temperature and token control
python3 {baseDir}/scripts/venice.py chat "Be creative" --temperature 1.2 --max-tokens 4000

# JSON output mode
python3 {baseDir}/scripts/venice.py chat "List 5 colors as JSON" --json

# Prompt caching (for repeated context)
python3 {baseDir}/scripts/venice.py chat "Question" --cache-key my-session-123

# Show usage stats
python3 {baseDir}/scripts/venice.py chat "Hello" --show-usage
```

---

## 嵌入向量

生成用于语义搜索、检索式问答（RAG）和推荐系统的嵌入向量：

```bash
# Single text
python3 {baseDir}/scripts/venice.py embed "Venice is a private AI platform"

# Multiple texts (batch)
python3 {baseDir}/scripts/venice.py embed "first text" "second text" "third text"

# From file (one text per line)
python3 {baseDir}/scripts/venice.py embed --file texts.txt

# Output as JSON
python3 {baseDir}/scripts/venice.py embed "some text" --output json
```

模型：`text-embedding-bge-m3`（私有模型，每百万个标记 0.15 美元）

---

## 文本转语音（TTS）

支持 60 多种语言的语音将文本转换为语音：

```bash
# Default voice
python3 {baseDir}/scripts/venice.py tts "Hello, welcome to Venice AI"

# Choose a voice
python3 {baseDir}/scripts/venice.py tts "Exciting news!" --voice af_nova

# List available voices
python3 {baseDir}/scripts/venice.py tts --list-voices

# Custom output path
python3 {baseDir}/scripts/venice.py tts "Some text" --output /tmp/speech.mp3

# Adjust speed
python3 {baseDir}/scripts/venice.py tts "Speaking slowly" --speed 0.8
```

**常用语音：** `af_sky`, `af_nova`, `am_liam`, `bf_emma`, `zf_xiaobei`（中文），`jm_kumo`（日语）

模型：`tts-kokoro`（私有模型，每百万个字符 3.50 美元）

---

## 语音转文本（STT）

将音频文件转录为文本：

```bash
# Transcribe a file
python3 {baseDir}/scripts/venice.py transcribe audio.wav

# With timestamps
python3 {baseDir}/scripts/venice.py transcribe recording.mp3 --timestamps

# From URL
python3 {baseDir}/scripts/venice.py transcribe --url https://example.com/audio.wav
```

支持的格式：WAV、FLAC、MP3、M4A、AAC、MP4

模型：`nvidia/parakeet-tdt-0.6b-v3`（私有模型，每音频秒 0.0001 美元）

---

## 检查 API 使用情况

```bash
python3 {baseDir}/scripts/venice.py balance
```

---

# 第二部分：图像与视频

## 价格概述

| 功能 | 费用 |
|---------|------|
| 图像生成 | 每张图片约 0.01-0.03 美元 |
| 图像缩放 | 每张图片约 0.02-0.04 美元 |
| 图像编辑 | 0.04 美元 |
| 视频（WAN） | 每段视频约 0.10-0.50 美元 |
| 视频（Sora） | 每段视频约 0.50-2.00 美元 |
| 视频（Runway） | 每段视频约 0.20-1.00 美元 |

使用 `--quote` 参数可以在生成前查看具体费用。

---

## 图像生成

```bash
# Basic generation
python3 {baseDir}/scripts/venice-image.py --prompt "a serene canal in Venice at sunset"

# Multiple images
python3 {baseDir}/scripts/venice-image.py --prompt "cyberpunk city" --count 4

# Custom dimensions
python3 {baseDir}/scripts/venice-image.py --prompt "portrait" --width 768 --height 1024

# List available models and styles
python3 {baseDir}/scripts/venice-image.py --list-models
python3 {baseDir}/scripts/venice-image.py --list-styles

# Use specific model and style
python3 {baseDir}/scripts/venice-image.py --prompt "fantasy" --model flux-2-pro --style-preset "Cinematic"

# Reproducible results with seed
python3 {baseDir}/scripts/venice-image.py --prompt "abstract" --seed 12345
```

**关键参数：** `--prompt`（提示内容），`--model`（默认：flux-2-max），`--count`（生成数量），`--width`（宽度），`--height`（高度），`--format`（输出格式：webp/png/jpeg），`--resolution`（分辨率），`--aspect-ratio`（纵横比），`--negative-prompt`（是否使用否定提示），`--style-preset`（风格预设），`--cfg-scale`（缩放比例），`--seed`（随机种子），`--safe-mode`（安全模式），`--hide-watermark`（是否隐藏水印），`--embed-exif`（是否嵌入 EXIF 信息）

---

## 图像缩放

```bash
# 2x upscale
python3 {baseDir}/scripts/venice-upscale.py photo.jpg --scale 2

# 4x with AI enhancement
python3 {baseDir}/scripts/venice-upscale.py photo.jpg --scale 4 --enhance

# Enhanced with custom prompt
python3 {baseDir}/scripts/venice-upscale.py photo.jpg --enhance --enhance-prompt "sharpen details"

# From URL
python3 {baseDir}/scripts/venice-upscale.py --url "https://example.com/image.jpg" --scale 2
```

**关键参数：** `--scale`（缩放比例，1-4，默认：2），`--enhance`（图像增强），`--enhance-prompt`（增强提示），`--enhance-creativity`（创意增强程度，0.0-1.0），`--url`（输入图像 URL），`--output`（输出文件路径）

---

## 图像编辑

使用 AI 进行图像编辑：

```bash
# Add elements
python3 {baseDir}/scripts/venice-edit.py photo.jpg --prompt "add sunglasses"

# Modify scene
python3 {baseDir}/scripts/venice-edit.py photo.jpg --prompt "change the sky to sunset"

# Remove objects
python3 {baseDir}/scripts/venice-edit.py photo.jpg --prompt "remove the person in background"

# From URL
python3 {baseDir}/scripts/venice-edit.py --url "https://example.com/image.jpg" --prompt "colorize"
```

**注意：** 图像编辑功能使用的是 Qwen-Image 模型，该模型对某些内容有限制。

---

## 视频生成

```bash
# Get price quote first
python3 {baseDir}/scripts/venice-video.py --quote --model wan-2.6-image-to-video --duration 10s

# Image-to-video (WAN - default)
python3 {baseDir}/scripts/venice-video.py --image photo.jpg --prompt "camera pans slowly" --duration 10s

# Image-to-video (Sora)
python3 {baseDir}/scripts/venice-video.py --image photo.jpg --prompt "cinematic" \
  --model sora-2-image-to-video --duration 8s --aspect-ratio 16:9 --skip-audio-param

# Video-to-video (Runway Gen4)
python3 {baseDir}/scripts/venice-video.py --video input.mp4 --prompt "anime style" \
  --model runway-gen4-turbo-v2v

# List models with available durations
python3 {baseDir}/scripts/venice-video.py --list-models
```

**关键参数：** `--image` 或 `--video`（选择生成类型），`--prompt`（生成提示），`--model`（默认：wan-2.6-image-to-video），`--duration`（视频时长），`--resolution`（分辨率），`--aspect-ratio`（纵横比），`--audio`/`--no-audio`（是否包含音频），`--quote`（是否生成音频），`--timeout`（生成超时时间）**

**可用模型：**
- **WAN**：图像转视频，支持自定义音频，时长 5 秒至 21 秒。
- **Sora**：需要指定纵横比，可使用 `--skip-audio-param` 参数。
- **Runway**：视频转视频功能。

---

# 提示与技巧

### 🔍 网页搜索 + 大语言模型（LLM） = 研究助手
使用 `--web-search on --web-citations` 可构建高效的研究工作流程。Venice 可在一次 API 调用中完成网页搜索、结果合成及来源引用。

### 🔓 未经审查的创意内容
Venice 的未经审查模型适用于文本和图像生成，没有任何限制，适合创意创作。

### 🎯 提示缓存
如果您运行的代理循环重复发送相同的系统提示，可以使用 `--cache-key` 选项来节省高达 90% 的费用。

### 🎤 音频处理流程
结合使用 `tts` 和 `transcribe` 功能：使用 `tts` 生成语音内容，使用 `transcribe` 处理音频文件。这两个功能都支持隐私保护。

### 🎬 视频制作流程
1. 生成或找到基础图像。
2. 使用 `--quote` 参数估算视频制作成本。
3. 根据需求选择合适的模型和时长进行生成。
4. 视频生成时间根据设置不同，通常需要 1-5 分钟。

---

## 故障排除

| 问题 | 解决方案 |
|---------|----------|
| `VENICE_API_KEY 未设置` | 通过环境变量设置 API 密钥，或在 `~/.clawdbot/clawdbot.json` 文件中配置。 |
| API 密钥无效 | 在 [venice.ai/settings/api](https://venice.ai/settings/api) 验证密钥有效性。 |
| 模型未找到 | 运行 `--list-models` 命令查看可用模型；新模型可使用 `--no-validate` 参数。 |
| 使用频率受限 | 查看 `--show-usage` 的输出信息。 |
| 视频生成失败 | 视频生成可能需要 1-5 分钟；长视频可使用 `--timeout 600` 设置超时时间。 |

## 资源

- **API 文档**：[docs.venice.ai](https://docs.venice.ai)
- **平台状态**：[veniceai-status.com](https://veniceai-status.com)
- **Discord 社区**：[discord.gg/askvenice](https://discord.gg/askvenice)