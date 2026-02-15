---
name: elevenlabs-tts
description: ElevenLabs TTS：这是专为 OpenClaw 设计的最佳 ElevenLabs 集成方案。它支持 ElevenLabs 的文本转语音功能（包含情感音频标签），以及用于 WhatsApp 的语音合成服务，并提供多语言支持。用户可以通过 ElevenLabs 的 API 生成逼真的人工智能语音。
tags: [elevenlabs, tts, voice, text-to-speech, audio, speech, whatsapp, multilingual, ai-voice]
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"env":["ELEVENLABS_API_KEY"],"system":["ffmpeg"]},"primaryEnv":"ELEVENLABS_API_KEY"}}
allowed-tools: [exec, tts, message]
---

# ElevenLabs TTS（文本转语音）

使用 ElevenLabs v3 生成具有表现力的语音消息，并支持音频标签。

## 先决条件

- **ElevenLabs API 密钥**（`ELEVENLABS_API_KEY`）：必需。在 [elevenlabs.io](https://elevenlabs.io) 的“个人资料”→“API 密钥”处获取。在 `openclaw.json` 的 `messages.tts.elevenlabs.apiKey` 中配置该密钥。
- **ffmpeg**：用于音频格式转换（将 MP3 转换为 Opus 格式，以兼容 WhatsApp）。必须已安装并确保其在系统的 PATH 环境变量中可用。

## 快速入门示例

**故事讲述（情感表达）：**
```
[soft] It started like any other day... [pause] But something felt different. [nervous] My hands were shaking as I opened the envelope. [gasps] I got in! [excited] I actually got in! [laughs] [happy] This changes everything!
```

**恐怖/悬疑（营造紧张氛围）：**
```
[whispers] The house has been empty for years... [pause] At least, that's what they told me. [nervous] But I keep hearing footsteps. [scared] They're getting closer. [gasps] [panicking] The door— it's opening by itself!
```

**带反应的对话：**
```
[curious] So what happened at the meeting? [pause] [surprised] Wait, they fired him?! [gasps] [sad] That's terrible... [sighs] He had a family. [thoughtful] I wonder what he'll do now.
```

**希伯来语（浪漫场景）：**
```
[soft] היא עמדה שם, מול השקיעה... [pause] הלב שלי פעם כל כך חזק. [nervous] לא ידעתי מה להגיד. [hesitates] אני... [breathes] [tender] את יודעת שאני אוהב אותך, נכון?
```

**西班牙语（从庆祝到反思）：**
```
[excited] ¡Lo logramos! [laughs] [happy] No puedo creerlo... [pause] [thoughtful] Fueron tantos años de trabajo. [emotional] [soft] Gracias a todos los que creyeron en mí. [sighs] [content] Valió la pena cada momento.
```

## 配置（OpenClaw）

在 `openclaw.json` 的 `messages.tts` 部分进行 TTS 配置：

```json
{
  "messages": {
    "tts": {
      "provider": "elevenlabs",
      "elevenlabs": {
        "apiKey": "sk_your_api_key_here",
        "voiceId": "pNInz6obpgDQGcFmaJgB",
        "modelId": "eleven_v3",
        "languageCode": "en",
        "voiceSettings": {
          "stability": 0.5,
          "similarityBoost": 0.75,
          "style": 0,
          "useSpeakerBoost": true,
          "speed": 1
        }
      }
    }
  }
}
```

**获取 API 密钥：**
1. 访问 https://elevenlabs.io
2. 注册/登录
3. 点击“个人资料”→“API 密钥”
4. 复制你的 API 密钥

## 推荐的 v3 语音

这些预制作的语音针对 v3 进行了优化，与音频标签配合使用效果最佳：

| 语音 | ID | 性别 | 口音 | 适用场景 |
|-------|-----|--------|--------|----------|
| **Adam** | `pNInz6obpgDQGcFmaJgB` | 男性 | 美国口音 | 深沉的旁白，通用场景 |
| **Rachel** | `21m00Tcm4TlvDq8ikWAM` | 女性 | 美国口音 | 平静的旁白，适合对话 |
| **Brian** | `nPczCjzI2devNBz1zQrb` | 男性 | 美国口音 | 深沉的旁白，适合播客 |
| **Charlotte** | `XB0fDUnXU5powFXDhCwa` | 女性 | 英英混合口音 | 表现力强，适合视频游戏 |
| **George** | `JBFqnCBsd6RMkjVDRZzb` | 男性 | 英国口音 | 低沉的嗓音，适合故事讲述 |

**查找更多语音：**
- 浏览：https://elevenlabs.io/voice-library
- 专为 v3 优化的语音集合：https://elevenlabs.io/app/voice-library/collections/aF6JALq9R6tXwCczjhKH
- API：`GET https://api.elevenlabs.io/v1/voices`

**语音选择建议：**
- 使用 IVC（即时语音克隆）或预制作的语音；PVC 语音尚未针对 v3 优化。
- 选择与你的使用场景相匹配的语音（例如，低语的语音不适合大声朗读）。
- 对于需要表现力的 IVC 语音，训练样本中应包含多种情感音调。

## 模型设置

- **模型**：`eleven_v3`（alpha 版本）——唯一支持音频标签的模型。
- **语言**：支持 70 多种语言，并可完全控制音频标签。

### 稳定性模式

| 模式 | 稳定性 | 描述 |
|------|-----------|-------------|
| **Creative** | 0.3-0.5 | 更具表现力，但可能产生不自然的效果 |
| **Natural** | 0.5-0.7 | 平衡性较好，接近真实语音 |
| **Robust** | 0.7-1.0 | 非常稳定，但对音频标签的响应较弱 |

对于音频标签，建议使用 **Creative**（0.5）或 **Natural** 模式。稳定性越高，对标签的响应越弱。

### 速度控制

范围：0.7（慢）到 1.2（快），默认值为 1.0。
极端值会影响语音质量。根据需要使用如 `[rushed]` 或 `[drawn out]` 等标签来调整语速。

## 重要规则

### 文本长度限制
- **最佳长度**：每个段落不超过 800 个字符（可获得最佳质量）。
- **最大长度**：10,000 个字符（API 的硬性限制）。
- 文本过长会导致语音质量下降，表现力减弱。

### 音频标签——实现自然音效的最佳实践

- 每个句子或短语使用 1-2 个标签（不要过多）。
- 标签的有效期持续到下一个标签出现为止，无需重复使用。
- 过度使用标签会让人感觉不自然或机器化。

- 标签的放置位置：
  - 在情感转折点
  - 在关键戏剧性时刻之前
  - 在语气或节奏发生变化时

**上下文的重要性**：
  - 编写的文本应与标签所表达的情感相匹配。
  - 带有上下文的较长文本有助于提高语音的解读效果。
  - 例如：`[nervous] 我……我不确定这样做是否合适。如果失败了怎么办？` 比 `[nervous] 你好。` 更有效。

**组合标签以增强效果**：
- `[nervously][whispers]` = 紧张的低语
- `[excited][laughs]` = 兴奋的笑声
- 每组标签组合不超过 2 个。

**为了获得最佳效果，请重新生成语音：**
- v3 的生成结果具有不确定性，相同文本可能会产生不同的输出。
- 生成多个版本后选择最佳结果。
- 对文本进行微调可以改善效果。

**标签与语音的匹配**：
- 低语的语音不适合使用 `[shouts]` 标签。
- 大声或充满活力的语音不适合使用 `[whispers]` 标签。
- 使用所选语音测试标签的效果。

### 注意：v3 不支持 SSML 格式

v3 不支持 SSML 格式的标签，请使用音频标签和标点符号。

### 标点符号的用法

标点符号可以增强音频标签的效果：
- **省略号（...）** → 创造戏剧性的停顿：`[nervous] 我……我不知道……`
- **大写字母** → 强调：`[excited] 太棒了！`
- **破折号（—）** → 表示中断：`[explaining] 所以你的做法是— [interrupting] 等等！`
- **问号** → 表示不确定性：`[nervous] 你确定吗？`
- **感叹号！** → 增强语气：`[happy] 我们做到了！`

**结合标签和标点符号以获得最佳效果：**
```
[tired] It was a long day... [sighs] Nobody listens anymore.
```

## WhatsApp 语音消息

### 完整的工作流程

1. 使用 `tts` 工具生成音频文件（输出格式为 MP3）。
2. 将 MP3 文件转换为 Opus 格式（Android 设备必须使用此格式）。
3. 使用 `message` 工具发送音频文件。

### 具体步骤

**1. 生成 TTS 文件（在文件末尾添加 `[pause]` 标签以防止音频被截断）：**
```
tts text="[excited] This is amazing! [pause]" channel=whatsapp
```
输出文件：`MEDIA:/tmp/tts-xxx/voice-123.mp3`

**2. 将 MP3 文件转换为 Opus 格式：**
```bash
ffmpeg -i /tmp/tts-xxx/voice-123.mp3 -c:a libopus -b:a 64k -vbr on -application voip /tmp/tts-xxx/voice-123.ogg
```

**3. 发送 Opus 文件：**

> **注意：** 在发送消息时，`message` 字段中需要包含一个 Unicode 左到右的标记（`U+200E`）。
> 这是 WhatsApp 的要求——消息体不能为空才能发送语音消息。
> 这个标记是隐藏的，但能满足发送语音消息的条件。

```
message action=send channel=whatsapp target="+972..." filePath="/tmp/tts-xxx/voice-123.ogg" asVoice=true message="‎"
```

### 为什么选择 Opus 格式？

| 格式 | iOS | Android | 是否支持转录 |
|--------|-----|---------|------------|
| MP3 | ✅ 可用 | ❌ 可能无法正常播放 | ❌ 不支持 |
| Opus (.ogg) | ✅ 可用 | ✅ 可用 | ✅ 支持转录 |

**始终将音频转换为 Opus 格式**——这是唯一在所有设备（iOS 和 Android）上都能正常播放的格式，并且支持 WhatsApp 的转录功能。

### 音频截断问题

ElevenLabs 有时会截断音频文件的最后一个单词。**务必在文件末尾添加 `[pause]` 或 `...` 标签：**
```
[excited] This is amazing! [pause]
```

## 长音频文件（如播客）

对于超过 800 个字符的音频文件：
1. 将文件分割成多个长度不超过 800 个字符的段落。
2. 使用 `tts` 工具为每个段落生成音频文件。
3. 使用 `ffmpeg` 将这些文件合并成一个文件。
4. 将合并后的文件转换为 Opus 格式，然后发送。

**注意**：不要在音频文件中提及“第 2 部分”或“第 X 章”等分段信息，以保持音频的连贯性。

## 多角色对话

v3 支持同时为多个角色生成语音：

```
Jessica: [whispers] Did you hear that?
Chris: [interrupting] —I heard it too!
Jessica: [panicking] We need to hide!
```

**对话标签**：`[interrupting]`（打断）、`[overlapping]`（同时说话）、`[cuts in]`（插入对话）。

## 音频标签快速参考

| 类别 | 标签 | 使用场景 |
|----------|------|-------------|
| **情感** | [excited]（兴奋）、[happy]（快乐）、[sad]（悲伤）、[angry]（愤怒）、[nervous]（紧张）、[curious]（好奇） | 表达主要情感 |
| **语调/速度** | [whispers]（低语）、[shouts]（大喊）、[soft]（轻柔）、[rushed]（急促）、[drawn out]（拖长） | 控制音量和语速 |
| **反应** | [laughs]（笑声）、[sighs]（叹息）、[gasps]（倒吸一口气）、[clears throat]（清嗓子）、[gulps]（吞咽） | 表现自然的人际反应 |
| **节奏** | [pause]（暂停）、[hesitates]（犹豫）、[stammers]（结巴）、[breathes]（呼吸） | 调整对话的节奏 |
| **角色特征** | [French accent]（法语口音）、[British accent]（英式口音）、[robotic tone]（机器人音调] | 体现角色的语音特征 |
| **对话** | [interrupting]（打断）、[overlapping]（同时说话）、[cuts in]（插入对话） | 多角色之间的对话 |

**最有效的标签**（通常能产生稳定效果）：
- **情感**：`[excited]`、`[nervous]`、`[sad]`、`happy` |
- **反应**：`[laughs]`、`[sighs]`、`whispers` |
- **节奏**：`[pause]`（暂停）

**效果可能不稳定的标签**：
- **音效**：`[explosion]`（爆炸）、`gunshot`（枪声） |
- **口音**：不同语音的效果可能有所不同。

**完整标签列表**：请参阅 [references/audio-tags.md](references/audio-tags.md)

## 常见问题及解决方法

- **标签是否被正确读取？**
  - 使用 `eleven_v3` 模型进行测试。
  - 使用 IVC 或预制作的语音，避免使用 PVC 语音。
  - 简化标签（避免使用如 “tone” 这样的后缀）。
  - 增加文本长度（至少 250 个字符）。

- **语音表现不一致？**
  - 段落过长——将其分割成不超过 800 个字符的段落。
  - 重新生成音频文件（v3 的生成结果具有不确定性）。
  - 尝试使用较低的稳定性设置。

- **WhatsApp 无法播放音频？**
  - 将音频文件转换为 Opus 格式。

- **即使使用了标签，语音仍没有情感表现？**
  - 可能是因为语音与标签所表达的情感不匹配。
  - 尝试使用 `Creative`（0.5）稳定性模式。
  - 在标签前后添加更多上下文信息。