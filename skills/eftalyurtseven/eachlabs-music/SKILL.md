---
name: eachlabs-music
description: 使用 EachLabs 的 Mureka AI 模型可以生成歌曲、器乐曲、歌词以及播客内容。该工具还支持歌曲的扩展处理、音频元素的提取（如旋律、和声等）以及歌曲的识别功能。非常适合用户需要创作音乐、歌词或音频内容时使用。
metadata:
  author: eachlabs
  version: "1.0"
---

# EachLabs Music

通过 EachLabs 的 Predictions API，利用 Mureka AI 模型生成歌曲、器乐曲、歌词、播客等内容。

## 认证

```
Header: X-API-Key: <your-api-key>
```

请设置 `EACHLABS_API_KEY` 环境变量。您可以在 [eachlabs.ai](https://eachlabs.ai) 获取该密钥。

## 可用功能

### Mureka 模型

| 功能 | Slug | 描述 |
|-----------|------|-------------|
| 生成歌曲 | `mureka-generate-song` | 根据提示生成包含人声的完整歌曲 |
| 生成器乐曲 | `mureka-generate-instrumental` | 生成器乐曲 |
| 生成歌词 | `mureka-generate-lyrics` | 根据提示生成歌词 |
| 扩展歌词 | `mureka-extend-lyrics` | 继续/扩展现有歌词 |
| 扩展歌曲 | `mureka-extend-song` | 继续现有歌曲的内容 |
| 生成语音 | `mureka-create-speech` | 生成语音音频 |
| 创建播客 | `mureka-create-podcast` | 创建多声道播客 |
| 识别歌曲 | `mureka-recognize-song` | 从音频中识别歌曲 |
| 描述歌曲 | `mureka-describe-song` | 分析并描述歌曲 |
| 分离音频元素 | `mureka-stem-song` | 将音频分解为独立的声音元素 |
| 上传文件 | `mureka-upload-file` | 上传音频文件以进行其他操作 |

### Minimax Music

| 功能 | Slug | 描述 |
|-----------|------|-------------|
| Music v2 | `minimax-music-v2` | 最新的 Minimax 音乐生成服务 |
| Music v1.5 | `minimax-music-v1-5` | 稳定的 Minimax 音乐生成服务 |

## 预测流程

1. **检查模型**：`GET https://api.eachlabs.ai/v1/model?slug=<slug>` — 确认模型存在，并返回包含完整输入参数的 `request_schema`。在创建预测请求之前，请务必执行此操作以确保输入正确。
2. **发送请求**：`POST https://api.eachlabs.ai/v1/prediction`，提供模型 slug、版本 `"0.0.1"` 以及符合 schema 的输入数据。
3. **查询结果**：`GET https://api.eachlabs.ai/v1/prediction/{id}`，直到状态变为 `"success"` 或 `"failed"`。
4. **提取结果**：从响应中提取最终结果。

## 示例

### 生成歌曲

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "mureka-generate-song",
    "version": "0.0.1",
    "input": {
      "prompt": "An upbeat indie pop song about summer road trips with catchy chorus",
      "duration": 120
    }
  }'
```

### 生成器乐曲

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "mureka-generate-instrumental",
    "version": "0.0.1",
    "input": {
      "prompt": "Lo-fi hip hop beat with jazzy piano chords and vinyl crackle, relaxing study music"
    }
  }'
```

### 生成歌词

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "mureka-generate-lyrics",
    "version": "0.0.1",
    "input": {
      "prompt": "Write lyrics for a heartfelt country ballad about coming home"
    }
  }'
```

### 创建播客

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "mureka-create-podcast",
    "version": "0.0.1",
    "input": {
      "prompt": "A 5-minute podcast discussion about the future of AI in music production",
      "speakers": ["Luna", "Jake"]
    }
  }'
```

### 扩展现有歌曲

首先上传歌曲文件，然后对其进行扩展：

```bash
# Step 1: Upload the audio file
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "mureka-upload-file",
    "version": "0.0.1",
    "input": {
      "file": "https://example.com/my-song.mp3",
      "purpose": "audio"
    }
  }'

# Step 2: Use the upload ID to extend the song
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "mureka-extend-song",
    "version": "0.0.1",
    "input": {
      "upload_audio_id": "<upload-id-from-step-1>",
      "prompt": "Continue with an energetic guitar solo bridge"
    }
  }'
```

### 分离音频元素

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "mureka-stem-song",
    "version": "0.0.1",
    "input": {
      "url": "https://example.com/song.mp3"
    }
  }'
```

## 提示建议

- 指定音乐类型：例如 “indie pop”、“lo-fi hip hop”、“classical orchestral”、“EDM”
- 描述音乐情绪：如 “upbeat”（欢快）、“melancholic”（忧郁）、“energetic”（充满活力）或 “relaxing”（放松）
- 提及使用的乐器：如 “acoustic guitar”（原声吉他）、“piano”（钢琴）、“synthesizer”（合成器）、“drums”（鼓）
- 描述音乐节奏：如 “slow ballad”（慢节奏民谣）、“fast-paced”（快节奏）、“medium tempo groove”（中等节奏）
- 对于歌词，可说明主题和结构，例如：“verse-chorus-verse”（主歌-副歌-主歌）

## 参数参考

有关每个模型的完整参数详情，请参阅 [references/MODELS.md](references/MODELS.md)。