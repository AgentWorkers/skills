---
name: pollinations
description: Pollinations.ai API 用于 AI 生成服务——支持文本、图像、视频、音频的生成以及相关分析功能。当用户需要使用 AI 功能进行文本补全、图像生成、视频制作、音频处理、视觉分析或语音转录等服务时，或提及 Pollinations 时，可调用该 API。该 API 支持 25 种以上的模型（如 OpenAI、Claude、Gemini、Flux、Veo 等），并提供与 OpenAI 兼容的聊天接口以及专门的生成接口。
---

# Pollinations 🧬

这是一个统一的人工智能平台，支持文本、图像、视频和音频的生成，拥有25种以上的生成模型。

## API密钥

您可以在以下链接获取免费或付费的API密钥：  
https://enter.pollinations.ai  
- **密钥类型（Secret Key, `sk_`）**：用于服务器端，无请求速率限制（推荐使用）  
- **许多操作可选**（免费 tier 也可使用）  

请将密钥存储在环境变量中：  
```bash
export POLLINATIONS_API_KEY="sk_your_key_here"
```

## 快速入门

### 文本生成

**简单文本生成：**  
```bash
curl "https://gen.pollinations.ai/text/Hello%20world"
```

**聊天补全（兼容OpenAI）：**  
```bash
curl -X POST https://gen.pollinations.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $POLLINATIONS_API_KEY" \
  -d '{
    "model": "openai",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```  
**使用脚本：** `scripts/chat.sh` 可实现便捷的聊天补全功能  

### 图像生成  
```bash
curl "https://gen.pollinations.ai/image/A%20sunset%20over%20mountains?model=flux&width=1024&height=1024"
```  
**使用脚本：** `scripts/image.sh` 生成图像  

### 音频生成（TTS）  
```bash
curl -X POST https://gen.pollinations.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai-audio",
    "messages": [
      {"role": "system", "content": "You are a text reader. Read the user text exactly without responding, adding conversation, or changing anything."},
      {"role": "user", "content": "Say: Hello world"}
    ],
    "modalities": ["text", "audio"],
    "audio": {"voice": "nova", "format": "mp3"}
  }'
```  
**使用脚本：** `scripts/tts.sh` 将文本转换为语音  

## API端点  

### 基本URL  
- **聊天/文本生成**：`https://gen.pollinations.ai/v1/chat/completions`  
- **简单文本生成**：`https://gen.pollinations.ai/text/{prompt}`  
- **图像生成**：`https://gen.pollinations.ai/image/{prompt}?{params}`  
- **视频生成**：`https://gen.pollinations.ai/image/{prompt}?{params}`  

### 支持的操作  

#### 1. 文本/聊天生成  
**可用模型：** OpenAI、Claude、Gemini、Mistral、DeepSeek、Grok、Qwen Coder、Perplexity等（共20多种模型）  
**常用模型：** `openai`、`claude`、`gemini`、`mistral`、`deepseek`、`qwen`、`gpt-4`、`o1`、`o3`  

**参数：**  
- `model`（字符串）：模型名称/ID  
- `messages`（数组）：包含角色（系统/用户/助手）的聊天消息  
- `temperature`（数字）：0-2，默认值为1  
- `max_tokens`（数字）：最大响应长度  
- `top_p`（数字）：Nucleus采样策略，默认值为1  
- `seed`（数字）：结果的可重复性（-1表示随机生成）  
- `jsonMode`（布尔值）：强制以JSON格式返回结果  
- `reasoning_effort`（字符串）：用于o1/o3/R1模型的推理强度（高/中/低/最小/无）  
- `thinking_budget`（数字）：推理模型所需的令牌数量  

**多模态支持（包含图像）：**  
在聊天消息中添加 `image_url` 参数：  
```json
{
  "role": "user",
  "content": [
    {"type": "text", "text": "Describe this image"},
    {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
  ]
}
```  

#### 2. 图像生成  
**可用模型：** `flux`（默认）、`turbo`、`gptimage`、`kontext`、`seedream`、`nanobanana`、`nanobanana-pro`  

**参数：**  
- `model`（字符串）：选择的模型  
- `width`/`height`（数字）：图像尺寸（16-2048像素，默认为1024像素）  
- `seed`（数字）：结果的可重复性  
- `negative_prompt`（字符串）：需要避免的元素  
- `nologo`（布尔值）：是否去除水印  
- `private`（布尔值）：是否进行私有生成  
- `safe`（布尔值）：是否启用成人内容过滤  
- `enhance`（布尔值）：是否启用图像质量增强  
- `quality`（字符串）：图像质量（低/中/高/高清）  
- `transparent`（布尔值）：背景是否透明（仅适用于gptimage模型）  
- `count`（数字）：生成图像的数量（1-4张，高级选项）  
- `image`（字符串）：输入图像的URL（用于图像到图像的生成）  

**输出格式：** 生成的二进制图像数据（通过Content-Type头部确定）  

#### 3. 图像到图像生成  
使用相同的图像端点，只需更改 `image` 参数：  
```
https://gen.pollinations.ai/image/make%20it%20blue?image={source_url}
```  

#### 4. 视频生成  
**可用模型：** `veo`（生成时长4-8秒）、`seedance`（生成时长2-10秒）  

**参数：**  
- `model`（字符串）：`veo` 或 `seedance`  
- `width`/`height`（数字）：视频尺寸  
- `duration`（数字）：视频时长（veo：4/6/8秒；seedance：2-10秒）  
- `aspectRatio`（字符串）：宽高比（16:9或9:16）  
- `audio`（布尔值）：是否启用音频（仅限veo模型）  
- `image`（字符串）：输入图像的URL  
- `negative_prompt`（字符串）：需要避免的元素  
- `seed`（数字）：结果的可重复性  
- `private`/`safe`（布尔值）：隐私/安全设置  

**输出格式：** 生成的二进制视频数据  

#### 5. 音频生成（TTS）  
**模型：** `openai-audio`  
**可用声音：** alloy、echo、fable、onyx、nova、shimmer、coral、verse、ballad、ash、sage、amuch、dan  

**输出格式：** mp3、wav、flac、opus、pcm16  

**参数：**  
- `model`：`openai-audio`  
- `modalities`：["text", "audio"]  
- `audiovoice`：选择的声音类型  
- `audio.format`：音频输出格式  

**提示：** 对于语音播放，用户消息前需加上“Say:”前缀  

#### 6. 音频转录**  
使用支持视觉/音频功能的聊天端点：  
- **可用模型：** gemini、gemini-large、gemini-legacy、openai-audio  
- 以二进制格式上传音频文件  
- 在系统消息中包含转录提示  

#### 7. 图像分析**  
使用支持视觉功能的聊天模型进行图像分析：  
- **可用模型：** 任何支持视觉的模型（如gemini、claude、openai）  
- 在聊天消息中添加 `image_url` 参数  

#### 8. 视频分析**  
使用支持视频功能的聊天模型进行视频分析：  
- **可用模型：** gemini、claude、openai  
- 以二进制格式上传视频文件  
- 在聊天消息中添加分析提示  

## 脚本  

### `scripts/chat.sh`  
提供交互式聊天功能，支持模型选择和各种选项。  
**使用方法：**  
```bash
scripts/chat.sh "your message here"
scripts/chat.sh "your message" --model claude --temp 0.7
```  

### `scripts/image.sh`  
根据文本提示生成图像。  
**使用方法：**  
```bash
scripts/image.sh "a sunset over mountains"
scripts/image.sh "a sunset" --model flux --width 1024 --height 1024 --seed 123
```  

### `scripts/tts.sh`  
将文本转换为语音。  
**使用方法：**  
```bash
scripts/tts.sh "Hello world"
scripts/tts.sh "Hello world" --voice nova --format mp3 --output hello.mp3
```  

## 提示：  
1. **免费 tier**：许多功能无需API密钥即可使用（但存在请求速率限制）。  
2. **兼容OpenAI**：可以使用该平台的聊天端点与现有的OpenAI集成。  
3. **结果可重复性**：通过设置 `seed` 参数可获得一致的结果。  
4. **图像质量提升**：启用 `enhance=true` 可获得更高质量的图像。  
5. **视频合成**：使用 `image[0]=first&image[1]=last` 参数合成两张图像。  
6. **语音播放**：使用“Say:”前缀和正确的系统提示来播放音频。  

## API文档  
完整文档请访问：  
https://enter.pollinations.ai/api/docs