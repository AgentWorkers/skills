---
name: pollinations
version: 1.0.2
description: "**Pollinations.ai API：用于AI生成与分析**  
该API支持文本、图像、视频、音频以及视觉相关任务的生成与分析，同时具备语音转文字（TTS）功能。适用于用户需要AI驱动的内容服务（如文本补全、图像生成/编辑、视频制作、音频处理、图像/视频分析等），或在使用Pollinations相关功能时。API兼容OpenAI的25种以上模型，提供了丰富的功能端点供开发者调用。"
metadata: {"openclaw":{"emoji":"🧬","homepage":"https://pollinations.ai","os":["darwin","linux","win32"],"requires":{"bins":["curl","jq","base64"],"env":["POLLINATIONS_API_KEY"]},"primaryEnv":"POLLINATIONS_API_KEY","install":[{"id":"jq-brew","kind":"brew","formula":"jq","bins":["jq"],"label":"Install jq via Homebrew","os":["darwin"]},{"id":"jq-apt","kind":"shell","command":"sudo apt-get install -y jq","bins":["jq"],"label":"Install jq via apt","os":["linux"]}]}}
---
# Pollinations v1.0.2

这是一个统一的人工智能平台，支持生成和分析文本、图像、视频以及音频，内置了25种以上的模型。

## API密钥

您可以在以下链接获取免费或付费的API密钥：  
https://enter.pollinations.ai  
- **密钥类型（`sk_`）**：用于服务器端，无使用频率限制（推荐使用）  
- **适用操作**：许多操作都需要API密钥；免费 tier 也支持部分功能。

### 运行时要求

| 类型 | 名称 | 必需条件 |
|------|------|----------|
| 环境变量 | `POLLINATIONS_API_KEY` | 可选（免费 tier 可无需此变量） |
| 命令行工具 | `curl` | 是 |
| 命令行工具 | `jq` | 是 |
| 命令行工具 | `base64` | 是 |

## 操作与脚本

### 1. 文本/聊天生成（`scripts/chat.sh`）

使用25种以上的LLM模型（兼容OpenAI的API）生成文本。

**使用方法：**
```bash
scripts/chat.sh "your message"
scripts/chat.sh "your message" --model claude --temp 0.7
scripts/chat.sh "explain quantum physics" --model openai --max-tokens 500
scripts/chat.sh "list 3 colors" --json --model openai
scripts/chat.sh "solve this step by step" --model o3 --reasoning-effort high
scripts/chat.sh "translate to French" --system "You are a translator" --model gemini
```

**可选参数：**
- `--model MODEL` — 模型名称（默认：openai）  
- `--temp N` — 温度参数（0-2，默认：1）  
- `--max-tokens N` — 最大响应长度  
- `--top-p N` — 核心采样次数（0-1）  
- `--seed N` — 生成结果的可重复性（-1表示随机生成）  
- `--system "PROMPT"` — 系统提示语  
- `--json` — 强制输出结构化JSON格式的响应  
- `--reasoning-effort LVL` — 对于o1/o3/R1模型，用于控制推理深度（高/中/低/最小/无）  
- `--thinking-budget N` — 推理模型的token预算  

**可用模型：** openai, claude, gemini, gemini-large, gemini-search, mistral, deepseek, grok, qwen, perplexity, o1, o3, gpt-4等。使用`scripts/models.sh text`可查看所有模型列表。

**简单示例（无需脚本）：**
```bash
curl "https://gen.pollinations.ai/text/Hello%20world"
```

### 2. 图像生成（`scripts/image.sh`）

根据文本提示生成图像，支持多种模型和选项。

**使用方法：**
```bash
scripts/image.sh "a sunset over mountains"
scripts/image.sh "a portrait" --model flux --width 1024 --height 1024
scripts/image.sh "logo design" --model gptimage --quality hd --transparent
scripts/image.sh "photo" --enhance --nologo --private
scripts/image.sh "art" --negative "blurry, low quality" --seed 42
```

**可选参数：**
- `--model MODEL` — 使用的模型（默认：flux）  
- `--width N` — 图像宽度（16-2048像素，默认：1024）  
- `--height N` — 图像高度（16-2048像素，默认：1024）  
- `--seed N` — 生成结果的可重复性  
- `--output FILE` — 输出文件名  
- `--enhance` — 用于优化图像生成的AI提示语  
- `--negative "TEXT"` — 需要避免的负面内容  
- `--nologo` — 移除水印  
- `--private` — 以私密模式生成  
- `--safe` — 启用成人内容过滤  
- `--quality LEVEL` — 图像质量（低/中/高/高清，仅限gptimage）  
- `--transparent` — 透明背景PNG图像（仅限gptimage）  
- `--image-url URL` — 用于图像到图像转换的源图像  

**可用模型：** flux（默认），turbo, gptimage, kontext, seedream, nanobanana, nanobanana-pro。使用`scripts/models.sh image`可查看所有模型列表。

### 3. 图像编辑 / 图像到图像转换（`scripts/image-edit.sh`）

使用AI对现有图像进行编辑或转换。

**使用方法：**
```bash
scripts/image-edit.sh "make it blue" --source "https://example.com/photo.jpg"
scripts/image-edit.sh "add sunglasses" --source photo.jpg --model kontext
scripts/image-edit.sh "convert to watercolor" --source input.png --output watercolor.jpg
```

**可选参数：**
- `--source URL/FILE` — 源图像（URL或本地文件）  
- `--model MODEL` — 使用的模型（默认：kontext）  
- `--seed N` — 生成结果的可重复性  
- `--negative "TEXT"` — 需要避免的负面内容  
- `--output FILE` — 输出文件名  

### 4. 视频生成（`scripts/image.sh`，支持视频模型）

根据文本提示或图像生成视频。

**使用方法：**
```bash
scripts/image.sh "a cat playing piano" --model veo --duration 6
scripts/image.sh "ocean waves" --model seedance --duration 8 --aspect-ratio 16:9
scripts/image.sh "timelapse" --model veo --duration 4 --audio
scripts/image.sh "animate this" --model seedance --image-url "https://example.com/photo.jpg"
```

**额外参数（与图像生成相同）：**
- `--model VEO|SEEDANCE` — 使用的视频模型（必选）  
- `--duration N` — 视频时长（秒，veo模型：4/6/8秒；seedance模型：2-10秒）  
- `--aspect-ratio RATIO` — 宽高比（16:9或9:16）  
- `--audio` — 是否启用音频生成（仅限veo模型）  
- `--image-url URL` — 用于图像到视频转换的源图像  

**帧插值（仅veo模型）：** 可通过API直接传递两张图像以进行第一帧/最后一帧的插值处理：  
```
https://gen.pollinations.ai/image/prompt?model=veo&image[0]=first_frame_url&image[1]=last_frame_url
```

**可用模型：** veo（支持4-8秒视频，支持音频，支持帧插值）；seedance（支持2-10秒视频，支持图像到视频转换）。

### 5. 文本转语音 / 音频转换（`scripts/tts.sh`）

将文本转换为多种语言的语音文件。

**使用方法：**
```bash
scripts/tts.sh "Hello world"
scripts/tts.sh "Bonjour le monde" --voice nova --format mp3
scripts/tts.sh "Welcome" --voice coral --format wav --output welcome.wav
```

**可选参数：**
- `--voice VOICE` — 选择的语音（默认：nova）  
- `--format FORMAT` — 输出格式（默认：mp3）  
- `--model MODEL` — 使用的模型（默认：openai-audio）  
- `--output FILE` — 输出文件名  

**可用语音：** alloy, amuch, ash, ballad, coral, dan, echo, fable, nova, onyx, sage, shimmer, verse  

**可用格式：** mp3, wav, flac, opus, pcm16

### 6. 图像分析 / 视觉识别（`scripts/analyze-image.sh`）

使用视觉识别模型分析图像。

**使用方法：**
```bash
scripts/analyze-image.sh "https://example.com/photo.jpg"
scripts/analyze-image.sh photo.jpg --prompt "What objects are in this image?"
scripts/analyze-image.sh image.png --model claude --prompt "Extract all text from this image"
```

**可选参数：**
- `--prompt "TEXT"` — 分析指令（默认：“详细描述这幅图像”）  
- `--model MODEL` — 使用的视觉模型（默认：gemini）  

**输入格式：** URL或本地文件（jpg, png, gif, webp）

**可用模型：** gemini, gemini-large, claude, openai等支持视觉识别的模型。使用`scripts/models.sh vision`可查看所有模型列表。

### 7. 视频分析（`scripts/analyze-video.sh`）

使用视觉识别模型分析视频内容。

**使用方法：**
```bash
scripts/analyze-video.sh "https://example.com/video.mp4"
scripts/analyze-video.sh recording.mp4 --prompt "Summarize the key moments"
scripts/analyze-video.sh clip.mov --model gemini-large --prompt "Count the people"
```

**可选参数：**
- `--prompt "TEXT"` — 分析指令（默认：“详细描述这个视频”）  
- `--model MODEL` — 使用的视频模型（默认：gemini）  

**输入格式：** URL或本地文件（mp4, mov, avi）

**可用模型：** gemini, gemini-large, claude, openai等支持视频分析的模型。

### 8. 音频转录（`scripts/transcribe.sh`）

将音频文件转换为文本。

**使用方法：**
```bash
scripts/transcribe.sh recording.mp3
scripts/transcribe.sh podcast.wav --model gemini-large
scripts/transcribe.sh "https://example.com/audio.mp3" --prompt "Transcribe in French"
```

**可选参数：**
- `--prompt "TEXT"` — 转录指令（默认：准确转录）  
- `--model MODEL` — 使用的音频模型（默认：gemini）  

**输入格式：** 本地文件或URL（mp3, wav, flac, ogg, m4a）

**可用模型：** gemini, gemini-large, gemini-legacy, openai-audio

### 9. 查看所有可用模型（`scripts/models.sh`）

动态列出API中所有可用的模型。

**使用方法：**
```bash
scripts/models.sh              # List all models
scripts/models.sh text         # Text/chat models only
scripts/models.sh image        # Image generation models
scripts/models.sh video        # Video generation models
scripts/models.sh vision       # Vision/analysis models
scripts/models.sh audio        # Audio/TTS models
```

## API端点参考

| 操作 | 端点 | 方法 |
|-----------|----------|--------|
| 文本生成 | `/text/{prompt}` | GET |
| 聊天生成 | `/v1/chat/completions` | POST |
| 图像生成 | `/image/{prompt}?{params}` | GET |
| 图像到图像转换 | `/image/{prompt}?image={url}&{params}` | GET |
| 视频生成 | `/image/{prompt}?model=veo&{params}` | GET |
| 视频分析 | `/v1/chat/completions`（带图像URL） | POST |
| 视频分析 | `/v1/chat/completions`（带视频URL） | POST |
| 音频/文本转语音 | `/v1/chat/completions`（openai-audio） | POST |
| 音频转录 | `/v1/chat/completions`（带音频文件） | POST |
| 查看文本模型 | `/v1/models` | GET |
| 查看图像模型 | `/image/models` | GET |
| 查看视觉模型 | `/text/models` | GET |

## 提示：

1. **免费 tier**：许多操作无需API密钥即可使用（但会有使用频率限制）。  
2. **兼容OpenAI**：聊天功能可与现有的OpenAI集成。  
3. **结果可重复性**：使用`seed`参数可确保所有操作的结果具有一致性。  
4. **图像优化**：使用`--enhance`参数可优化图像生成的提示内容。  
5. **结构化数据**：在聊天功能中使用`--json`参数可获取结构化数据。  
6. **推理深度控制**：使用`--reasoning-effort`参数可控制o1/o3/R1模型的推理深度。  
7. **视频生成**：使用`--image-url`参数可进行图像到视频的转换；使用`--audio`参数可为视频添加音频。  
8. **本地文件支持**：图像分析/编辑/转录脚本支持URL和本地文件。  
9. **私密模式**：使用`--private`参数可将生成结果隐藏在公共 feed 中。  

## API文档

完整文档：  
https://enter.pollinations.ai/api/docs