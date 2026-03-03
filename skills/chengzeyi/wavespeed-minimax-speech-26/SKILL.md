---
name: wavespeed-minimax-speech-26
description: 使用 WaveSpeed AI 的 MiniMax Speech 2.6 Turbo 将文本转换为语音。该工具具备超逼真的人声克隆功能、低于 250 毫秒的延迟、支持 40 多种语言、情感控制以及 200 多种语音预设。适用于用户需要将文本转换为语音音频的场景。
metadata:
  author: wavespeedai
  version: "1.0"
---
# WaveSpeedAI MiniMax Speech 2.6 Turbo

通过 WaveSpeed AI 平台，使用 MiniMax Speech 2.6 Turbo 将文本转换为语音。该服务支持超逼真的语音克隆、低于 250 毫秒的延迟、40 多种语言支持以及情感控制功能。

## 认证

```bash
export WAVESPEED_API_KEY="your-api-key"
```

请在 [wavespeed.ai/accesskey](https://wavespeed.ai/accesskey) 获取您的 API 密钥。

## 快速入门

```javascript
import wavespeed from 'wavespeed';

const output_url = (await wavespeed.run(
  "minimax/speech-2.6-turbo",
  {
    text: "Hello, welcome to WaveSpeed AI!",
    voice_id: "English_CalmWoman"
  }
))["outputs"][0];
```

## API 端点

**模型 ID：** `minimax/speech-2.6-turbo`

您可以使用可配置的语音、情感、语速、音调和音频格式将文本转换为语音。

### 参数

| 参数 | 类型 | 是否必填 | 默认值 | 描述 |
|-----------|------|----------|---------|-------------|
| `text` | 字符串 | 是 | -- | 需要转换为语音的文本。最多 10,000 个字符。使用 `<#x#>` 在单词之间插入暂停（0.01-99.99 秒）。 |
| `voice_id` | 字符串 | 是 | -- | 语音预设 ID。请参阅下面的 [语音 ID](#voice-ids)。 |
| `speed` | 数字 | 否 | `1` | 语速。范围：0.50-2.00 |
| `volume` | 数字 | 否 | `1` | 语音音量。范围：0.10-10.00 |
| `pitch` | 数字 | 否 | `0` | 语音音高。范围：-12 到 12 |
| `emotion` | 字符串 | 否 | `happy` | 情感基调。可选值：`happy`（快乐）、`sad`（悲伤）、`angry`（愤怒）、`fearful`（恐惧）、`disgusted`（厌恶）、`surprised`（惊讶）、`neutral`（中立） |
| `english_normalization` | 布尔值 | 否 | `false` | 用于优化英语数字的朗读效果 |
| `sample_rate` | 整数 | 否 | -- | 采样率（Hz）。可选值：`8000`、`16000`、`22050`、`24000`、`32000`、`44100` |
| `bitrate` | 整数 | 否 | -- | 比特率（bps）。可选值：`32000`、`64000`、`128000`、`256000` |
| `channel` | 字符串 | 否 | -- | 音频声道。`1`（单声道）或 `2`（立体声） |
| `format` | 字符串 | 否 | -- | 输出格式。可选值：`mp3`、`wav`、`pcm`、`flac` |
| `language_boost` | 字符串 | 否 | -- | 用于增强特定语言的识别效果。请参阅 [支持的语言](#supported-languages)。 |

### 示例

```javascript
import wavespeed from 'wavespeed';

const output_url = (await wavespeed.run(
  "minimax/speech-2.6-turbo",
  {
    text: "The quick brown fox jumps over the lazy dog.",
    voice_id: "English_expressive_narrator",
    speed: 1.0,
    pitch: 0,
    emotion: "neutral",
    format: "mp3",
    sample_rate: 24000,
    bitrate: 128000
  }
))["outputs"][0];
```

### 暂停控制

使用 `<#x#>` 语法在语音中插入暂停，其中 `x` 表示暂停时间（0.01-99.99 秒）：

```javascript
const output_url = (await wavespeed.run(
  "minimax/speech-2.6-turbo",
  {
    text: "And the winner is <#2.0#> WaveSpeed AI!",
    voice_id: "English_CaptivatingStoryteller"
  }
))["outputs"][0];
```

## 高级用法

### 同步模式

```javascript
const output_url = (await wavespeed.run(
  "minimax/speech-2.6-turbo",
  {
    text: "Hello world!",
    voice_id: "English_CalmWoman"
  },
  { enableSyncMode: true }
))["outputs"][0];
```

### 带有重试配置的自定义客户端

```javascript
import { Client } from 'wavespeed';

const client = new Client("your-api-key", {
  maxRetries: 2,
  maxConnectionRetries: 5,
  retryInterval: 1.0,
});

const output_url = (await client.run(
  "minimax/speech-2.6-turbo",
  {
    text: "Welcome to our platform.",
    voice_id: "English_Trustworth_Man"
  }
))["outputs"][0];
```

### 使用 `runNoThrow` 进行错误处理

```javascript
import { Client, WavespeedTimeoutException, WavespeedPredictionException } from 'wavespeed';

const client = new Client();
const result = await client.runNoThrow(
  "minimax/speech-2.6-turbo",
  {
    text: "Testing speech generation.",
    voice_id: "English_CalmWoman"
  }
);

if (result.outputs) {
  console.log("Audio URL:", result.outputs[0]);
  console.log("Task ID:", result.detail.taskId);
} else {
  console.log("Failed:", result.detail.error.message);
  if (result.detail.error instanceof WavespeedTimeoutException) {
    console.log("Request timed out - try increasing timeout");
  } else if (result.detail.error instanceof WavespeedPredictionException) {
    console.log("Prediction failed");
  }
}
```

## 语音 ID

### 英语语音（热门选项）

| 语音 ID | 描述 |
|----------|-------------|
| `English_CalmWoman` | 平静的女性语音 |
| `English_Trustworth_Man` | 可信赖的男性语音 |
| `English_expressive_narrator` | 表情丰富的旁白声音 |
| `English_radiant_girl` | 充满活力的女孩语音 |
| `English_magnetic_voiced_man` | 有魅力的男性语音 |
| `English_CaptivatingStoryteller` | 有感染力的故事讲述者语音 |
| `English_Upbeat_Woman` | 积极向上的女性语音 |
| `English_GentleTeacher` | 温和的教师语音 |
| `English_PlayfulGirl` | 活泼的女孩语音 |
| `English_ManWithDeepVoice` | 深沉的男性语音 |
| `English_ConfidentWoman` | 自信的女性语音 |
| `English_Comedian` | 喜剧风格的语音 |
| `English_SereneWoman` | 平静的女性语音 |
| `English_WiseScholar` | 学者般的语音 |
| `English_Cute_Girl` | 可爱的女孩语音 |
| `English_Sharp_Commentator` | 尖锐的评论员语音 |
| `English_Lucky_Robot` | 机器人语音 |

### 通用语音

`Wise_Woman`、`Friendly_Person`、`Inspirational_girl`、`Deep_Voice_Man`、`Calm_Woman`、`Casual_Guy`、`Lively_Girl`、`Patient_Man`、`Young_Knight`、`Determined_Man`、`Lovely_Girl`、`Decent_Boy`、`Imposing_Manner`、`Elegant_Man`、`Abbess`、`Sweet_Girl_2`、`Exuberant_Girl`

### 特殊语音

`whisper_man`、`whisper_woman_1`、`angry_pirate_1`、`massive_kind_troll`、`movie_trailer_deep`、`peace_and_ease`

### 其他语言

支持的语言包括：中文（普通话）、粤语、阿拉伯语、俄语、西班牙语、法语、葡萄牙语、德语、土耳其语、荷兰语、乌克兰语、越南语、印尼语、日语、意大利语、韩语、泰语、波兰语、罗马尼亚语、希腊语、捷克语、芬兰语、印地语、保加利亚语、丹麦语、希伯来语、马来语、波斯语、斯洛伐克语、瑞典语、克罗地亚语、菲律宾语、匈牙利语、挪威语、斯洛文尼亚语、加泰罗尼亚语、尼诺斯克语、泰米尔语、阿非利卡语。

语音 ID 的格式为 `{语言}_{语音名称}`（例如：`Japanese_KindLady`、`Korean_SweetGirl`、`French_CasualMan`）。

## 支持的语言

对于 `language_boost` 参数，支持的语言包括：`Chinese`（中文）、`Chinese_Yue`（粤语）、`English`（英语）、`Arabic`（阿拉伯语）、`Russian`（俄语）、`Spanish`（西班牙语）、`French`（法语）、`Portuguese`（葡萄牙语）、`German`（德语）、`Turkish`（土耳其语）、`Dutch`（荷兰语）、`Ukrainian`（乌克兰语）、`Vietnamese`（越南语）、`Indonesian`（印尼语）、`Japanese`（日语）、`Italian`（意大利语）、`Korean`（韩语）、`Thai`（泰语）、`Polish`（波兰语）、`Romanian`（罗马尼亚语）、`Greek`（希腊语）、`Czech`（捷克语）、`Finnish`（芬兰语）、`Hindi`（印地语）、`Bulgarian`（保加利亚语）、`Danish`（丹麦语）、`Hebrew`（希伯来语）、`Malay`（马来语）、`Persian`（波斯语）、`Slovak`（斯洛伐克语）、`Swedish`（瑞典语）、`Croatian`（克罗地亚语）、`Filipino`（菲律宾语）、`Hungarian`（匈牙利语）、`Norwegian`（挪威语）、`Slovenian`（斯洛文尼亚语）、`Catalan`（加泰罗尼亚语）、`Nynorsk`（尼诺斯克语）、`Tamil`（泰米尔语）、`Afrikaans`（阿非利卡语）。

## 价格

每 1,000 个字符收费 0.06 美元。

## 安全要求

- **API 密钥安全**：请妥善保管您的 `WAVESPEED_API_KEY`，不要将其硬编码在源文件中或提交到版本控制系统中。建议使用环境变量或秘密管理系统进行管理。
- **输入验证**：仅传递上述文档中规定的参数。在发送请求之前，请验证文本内容。