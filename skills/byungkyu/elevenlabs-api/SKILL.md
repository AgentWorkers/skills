---
name: elevenlabs
description: |
  ElevenLabs API integration with managed authentication. AI-powered text-to-speech, voice cloning, sound effects, and audio processing.
  Use this skill when users want to generate speech from text, clone voices, create sound effects, or process audio.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# ElevenLabs

您可以使用受管理的身份验证方式访问 ElevenLabs API。该 API 支持将文本转换为逼真的语音、克隆声音、创建音效以及处理音频文件。

## 快速入门

```bash
# List available voices
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/elevenlabs/v1/voices')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/elevenlabs/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 ElevenLabs API 端点路径。该网关会将请求代理到 `api.elevenlabs.io`，并自动插入您的 API 密钥。

## 身份验证

所有请求都必须在 `Authorization` 头部包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的 ElevenLabs 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=elevenlabs&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'elevenlabs'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接信息

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "connection": {
    "connection_id": "ff2079b1-f40a-43b7-a807-1d5deea29c5b",
    "status": "ACTIVE",
    "creation_time": "2026-02-12T00:50:40.292363Z",
    "last_updated_time": "2026-02-12T00:51:14.547893Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "elevenlabs",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成身份验证。

### 删除连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 指定连接

如果您有多个 ElevenLabs 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/elevenlabs/v1/voices')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'ff2079b1-f40a-43b7-a807-1d5deea29c5b')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头部，网关将使用默认的（最旧的）活动连接。

## API 参考

### 文本转语音

#### 将文本转换为语音

```bash
POST /elevenlabs/v1/text-to-speech/{voice_id}
Content-Type: application/json

{
  "text": "Hello, this is a test of the ElevenLabs API.",
  "model_id": "eleven_multilingual_v2",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.75
  }
}
```

返回音频数据（默认为 mp3 格式）。

查询参数：
- `output_format` - 音频格式（例如：`mp3_44100_128`、`pcm_16000`、`pcm_22050`）

#### 流式文本转语音

```bash
POST /elevenlabs/v1/text-to-speech/{voice_id}/stream
Content-Type: application/json

{
  "text": "Hello, this is streamed audio.",
  "model_id": "eleven_multilingual_v2"
}
```

返回流式音频数据。

#### 带时间戳的文本转语音

```bash
POST /elevenlabs/v1/text-to-speech/{voice_id}/with-timestamps
Content-Type: application/json

{
  "text": "Hello world",
  "model_id": "eleven_multilingual_v2"
}
```

返回带有单词级时间戳的音频数据。

### 声音

#### 列出可用声音

```bash
GET /elevenlabs/v1/voices
```

列出所有可用的声音，包括预制作的声音和克隆的声音。

#### 获取特定声音的信息

```bash
GET /elevenlabs/v1/voices/{voice_id}
```

返回关于特定声音的元数据。

#### 获取默认声音设置

```bash
GET /elevenlabs/v1/voices/settings/default
```

#### 获取声音设置

```bash
GET /elevenlabs/v1/voices/{voice_id}/settings
```

#### 创建声音克隆

```bash
POST /elevenlabs/v1/voices/add
Content-Type: multipart/form-data

name: My Cloned Voice
files: [audio_sample.mp3]
description: A custom voice clone
remove_background_noise: false
```

#### 编辑声音

```bash
PATCH /elevenlabs/v1/voices/{voice_id}/edit
Content-Type: multipart/form-data

name: Updated Voice Name
description: Updated description
```

#### 删除声音

```bash
DELETE /elevenlabs/v1/voices/{voice_id}
```

### 模型

#### 列出模型

```bash
GET /elevenlabs/v1/models
```

列出可用的模型：
- `eleven_multilingual_v2` - 最新的多语言模型
- `eleven_turbo_v2_5` - 低延迟模型
- `eleven_monolingual_v1` - 旧版英语模型（已弃用）

### 用户

#### 获取用户信息

```bash
GET /elevenlabs/v1/user
```

#### 获取订阅信息

```bash
GET /elevenlabs/v1/user/subscription
```

返回订阅详情，包括字符限制和使用情况。

### 历史记录

#### 列出历史记录项

```bash
GET /elevenlabs/v1/history?page_size=100
```

查询参数：
- `page_size` - 每页显示的项数（默认：100，最大：1000）
- `start_after_history_item_id` - 分页的起始项 ID
- `voice_id` - 按声音过滤

#### 获取历史记录项

```bash
GET /elevenlabs/v1/history/{history_item_id}
```

#### 从历史记录中获取音频文件

```bash
GET /elevenlabs/v1/history/{history_item_id}/audio
```

返回历史记录项对应的音频文件。

#### 删除历史记录项

```bash
DELETE /elevenlabs/v1/history/{history_item_id}
```

#### 下载历史记录项

```bash
POST /elevenlabs/v1/history/download
Content-Type: application/json

{
  "history_item_ids": ["id1", "id2", "id3"]
}
```

返回包含请求音频文件的 zip 文件。

### 音效

#### 创建音效

```bash
POST /elevenlabs/v1/sound-generation
Content-Type: application/json

{
  "text": "A thunderstorm with heavy rain and distant thunder",
  "duration_seconds": 10.0
}
```

查询参数：
- `output_format` - 音频格式（例如：`mp3_44100_128`）

### 音频处理

#### 去除背景噪音

```bash
POST /elevenlabs/v1/audio-isolation
Content-Type: multipart/form-data

audio: [audio_file.mp3]
```

返回去除背景噪音的音频文件。

#### 流式音频处理

```bash
POST /elevenlabs/v1/audio-isolation/stream
Content-Type: multipart/form-data

audio: [audio_file.mp3]
```

### 语音转文本

#### 将音频转录为文本

```bash
POST /elevenlabs/v1/speech-to-text
Content-Type: multipart/form-data

audio: [audio_file.mp3]
model_id: scribe_v1
```

返回转录结果，可选包含单词级时间戳。

### 语音转语音（声音转换）

#### 转换声音

```bash
POST /elevenlabs/v1/speech-to-speech/{voice_id}
Content-Type: multipart/form-data

audio: [source_audio.mp3]
model_id: eleven_multilingual_sts_v2
```

在保持语调的情况下，将音频转换为另一种声音。

### 项目

#### 列出项目

```bash
GET /elevenlabs/v1/projects
```

#### 获取项目信息

```bash
GET /elevenlabs/v1/projects/{project_id}
```

#### 创建项目

```bash
POST /elevenlabs/v1/projects
Content-Type: application/json

{
  "name": "My Audiobook Project",
  "default_title_voice_id": "voice_id",
  "default_paragraph_voice_id": "voice_id"
}
```

### 发音词典

#### 列出发音词典

```bash
GET /elevenlabs/v1/pronunciation-dictionaries
```

#### 创建发音词典

```bash
POST /elevenlabs/v1/pronunciation-dictionaries/add-from-file
Content-Type: multipart/form-data

name: My Dictionary
file: [lexicon.pls]
```

## 响应头

ElevenLabs API 的响应包含以下有用头信息：
- `x-character-count` - 请求中使用的字符数
- `request-id` - 唯一的请求标识符

## 分页

历史记录和其他列表端点使用基于游标的分页方式：

```bash
GET /elevenlabs/v1/history?page_size=100&start_after_history_item_id=last_item_id
```

## 代码示例

### JavaScript - 文本转语音

```javascript
const response = await fetch(
  'https://gateway.maton.ai/elevenlabs/v1/text-to-speech/JBFqnCBsd6RMkjVDRZzb',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      text: 'Hello world!',
      model_id: 'eleven_multilingual_v2'
    })
  }
);
const audioBuffer = await response.arrayBuffer();
```

### Python - 文本转语音

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/elevenlabs/v1/text-to-speech/JBFqnCBsd6RMkjVDRZzb',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={
        'text': 'Hello world!',
        'model_id': 'eleven_multilingual_v2'
    }
)
audio_data = response.content
with open('output.mp3', 'wb') as f:
    f.write(audio_data)
```

### Python - 列出声音

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/elevenlabs/v1/voices',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
voices = response.json()
for voice in voices['voices']:
    print(f"{voice['name']}: {voice['voice_id']}")
```

## 注意事项

- 文本转语音按字符计费
- 音效按生成次数计费
- 语音转文本按音频分钟计费
- 音频输出格式可以通过 `codec_sample_rate_bitrate` 指定（例如：`mp3_44100_128`）
- 可用的模型：`eleven_multilingual_v2`（推荐）、`eleven_turbo_v2_5`（低延迟）
- 可以通过 `List Voices` 端点获取声音 ID
- 不同模型的最大文本长度不同
- 重要提示：当 URL 包含括号时，使用 `curl -g` 可以避免全局解析问题
- 重要提示：将 curl 输出传递给 `jq` 时，环境变量可能无法正确解析。建议使用 Python 示例。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 未建立 ElevenLabs 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 403 | 权限不足或超出配额 |
| 422 | 参数无效 |
| 429 | 超过使用限制 |
| 4xx/5xx | 来自 ElevenLabs API 的传递错误 |

### 故障排除：API 密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证 API 密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用名称无效

1. 确保您的 URL 路径以 `elevenlabs` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/elevenlabs/v1/voices`
- 错误的路径：`https://gateway.maton.ai/v1/voices`

## 资源

- [ElevenLabs API 文档](https://elevenlabs.io/docs/api-reference)
- [ElevenLabs 开发者门户](https://elevenlabs.io/developers)
- [ElevenLabs 模型概述](https://elevenlabs.io/docs/overview/models)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)