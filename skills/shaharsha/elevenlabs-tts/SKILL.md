---
name: elevenlabs-tts
description: ElevenLabs TTS（文本转语音）支持情感音频标签，以实现更具表现力的语音合成效果。该工具能够生成与WhatsApp兼容的语音消息，并支持Opus音频格式的转换。ElevenLabs TTS支持70多种语言（包括带有选择性尼库德（Nikud）标记的希伯来语），支持多语音角色的对话功能，同时也具备唱歌功能。此外，它还附带了一个音频转换工具。
tags: [elevenlabs, tts, voice, text-to-speech, audio, speech, whatsapp, multilingual, ai-voice, hebrew, nikud, singing]
allowed-tools: [tts, message, exec]
---

# ElevenLabs TTS（文本转语音）

使用 ElevenLabs v3 生成富有表现力的语音消息，并支持音频标签。

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

**希伯来语（浪漫场景 - 仅在必要时添加尼库德）：**
```
[soft] היא עמדה שם, מול השקיעה... [pause] הלב שלי פעם כל כך חזק. [nervous] לא ידעתי מה להגיד. [hesitates] אני... [breathes] [tender] אַתְּ יודעת שאני אוהב אותָךְ, נכון?
```

**西班牙语（从庆祝到反思）：**
```
[excited] ¡Lo logramos! [laughs] [happy] No puedo creerlo... [pause] [thoughtful] Fueron tantos años de trabajo. [emotional] [soft] Gracias a todos los que creyeron en mí. [sighs] [content] Valió la pena cada momento.
```

## 配置（OpenClaw）

在 `openclaw.json` 中，配置 `messages.tts` 部分以使用 TTS 功能：

```json
{
  "messages": {
    "tts": {
      "provider": "elevenlabs",
      "elevenlabs": {
        "apiKey": "sk_your_api_key_here",
        "voiceId": "YOUR_VOICE_ID",
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
3. 点击个人资料 → API 密钥
4. 复制您的密钥

## 推荐的 v3 语音库

这些预制作的语音专为 v3 优化，与音频标签配合使用效果最佳：

| 语音 | ID | 性别 | 口音 | 适用场景 |
|-------|-----|--------|--------|----------|
| **Adam** | `pNInz6obpgDQGcFmaJgB` | 男性 | 美国口音 | 深沉的叙述音，通用场景 |
| **Rachel** | `21m00Tcm4TlvDq8ikWAM` | 女性 | 美国口音 | 平静的叙述音，适合对话 |
| **Brian** | `nPczCjzI2devNBz1zQrb` | 男性 | 美国口音 | 深沉的叙述音，适合播客 |
| **Charlotte** | `XB0fDUnXU5powFXDhCwa` | 女性 | 英式-瑞典口音 | 表现力强的音色，适合电子游戏 |
| **George** | `JBFqnCBsd6RMkjVDRZzb` | 男性 | 英国口音 | 低沉的叙述音，适合故事讲述 |

**查找更多语音：**
- 浏览：https://elevenlabs.io/voice-library
- v3 优化的语音库：https://elevenlabs.io/app/voice-library/collections/aF6JALq9R6tXwCczjhKH
- API：`GET https://api.elevenlabs.io/v1/voices`

**语音选择建议：**
- 使用 IVC（即时语音克隆）或预制作的语音（PVC 尚未针对 v3 优化）
- 选择与场景相匹配的语音（低语的语音不适合大声朗读）
- 对于表现力强的 IVC 语音，训练样本中应包含多种情感音调

## 模型设置

- **模型**：`eleven_v3`（alpha 版本） - 仅支持音频标签
- **语言**：支持 70 多种语言，并可完全控制音频标签

### 稳定性模式

v3 仅支持以下三种模式：0.0、0.5、1.0

| 模式 | 值 | 描述 |
|------|-------|-------------|
| **Creative** | 0.0 | 最具表现力，适合歌唱，可能会产生幻觉效果 |
| **Natural** | 0.5 | 平衡性最佳，最接近原始语音 |
| **Robust** | 1.0 | 稳定性最高，但对标签的响应较弱 |

对于音频标签，建议使用 **Creative**（0.0）或 **Natural**（0.5）。**Robust** 模式的标签响应较弱。

### 速度控制

范围：0.7（慢）到 1.2（快），默认值为 1.0

极端值会影响语音质量。为了调整语速，可以使用如 `[rushed]` 或 `[drawn out]` 等标签。

## 希伯来语尼库德（元音符号）

**仅在选择性情况下添加尼库德** - 仅在发音有疑问的单词上使用。在每个单词上都添加尼库德会降低语音质量。

**规则：仅在模型可能判断错误的单词上添加尼库德。**

尼库德有用的常见场景：
1. **性别后缀**：שלומֵךְ（女性） vs שלומְךָ（男性），לָךְ（女性） vs לְךָ（男性），אותָךְ（女性） vs אותְךָ（男性）
2. **达格什（硬/软辅音）**：带有达格什的字母发音会发生变化：
   - פּ = P, פ = F：פִּיצה（披萨），פִּייר（皮埃尔）
   - בּ = B, ב = V：בְּרָכָה（祝福），בְּדִיוּק（贝迪尤克）
   - כּ = K, כ = Kh：כּוֹס（科斯），כַּמָּה（卡玛）
3. **同形异义词**：拼写相同但含义/发音不同的单词：
   - בּוֹקֶר（早晨） vs בּוֹקֵר（牛仔）
   - עוֹלָם（世界） vs עוֹלֵם（隐藏）
   - סֵפֶר（书） vs סָפַר（计数）
4. **外来词和借词**：模型可能判断错误
5. **重音位置**：重音位置会影响发音的准确性

**何时不添加尼库德：**
- 搭配唯一发音的常见单词（如 מה, יש, הרבה, שלום, אני, הוא 等）
- 语境能明确发音的单词
- 句子的大部分内容 - 保持原样

**示例：**
```
❌ Full nikud: מַה שְׁלוֹמְךָ? יֵשׁ לְךָ הַרְבֵּה כֶּסֶף.
✅ Selective: מה שלומְךָ? יש לְךָ הרבה כסף.
✅ Dagesh: ז'אן-פִּייר אפה פִּיצה מושלמת.
```

**原则：** 如果单词的发音只有一种可能性，就省略尼库德；如果有疑问，再添加尼库德。

## 重要规则

### 字符长度限制
- **最佳长度**：每个段落不超过 800 个字符（音质最佳）
- **最大长度**：10,000 个字符（API 的限制）
- 文本过长会导致音质下降，语音表现不一致

### 音频标签 - 为了自然的声音

**标签使用建议：**
- 每个句子或短语使用 1-2 个标签（不要更多！）
- 标签的有效期持续到下一个标签出现为止，无需重复
- 过度使用标签会让人感觉不自然或机械

**标签的放置位置：**
- 在情感转折点
- 在关键戏剧性时刻之前
- 在语气或节奏发生变化时

**语境很重要：**  
- 编写的文本应与标签所表达的情感相匹配
- 有上下文的较长文本有助于提高语音的准确性
- 例如：`[nervous] 我... 我不确定这样做是否可行。如果失败了怎么办？` 比 `[nervous] 你好。` 更有效

**组合标签以增强效果：**
- `[nervously][whispers]` = 紧张的低语
- `[excited][laughs]` = 兴奋的笑声
- 每组标签最多使用 2 个

**为了获得最佳效果，请重新生成：**  
- v3 的输出结果具有不确定性，相同文本可能产生不同结果  
- 生成多个版本，选择最佳结果  
- 对文本进行微调可以改善效果

**标签与语音的匹配：**
- 低语的语音不适合使用 `[shouts]` 标签  
- 大声/充满活力的语音不适合使用 `[whispers]` 标签  
- 使用所选语音测试标签的效果

### SSML 不受支持

v3 不支持 SSML 标签。请使用音频标签和标点符号。

### 标点符号的作用（与标签结合使用！）

标点符号可以增强音频标签的效果：
- **省略号（...）** → 创造戏剧性的停顿：`[nervous] 我... 我不知道...`
- **大写** → 强调：`[excited] 太棒了！`
- **破折号（—）** → 表示中断：`[explaining] 所以你的做法是— [interrupting] 等等！`
- **问号** → 表示疑问：`[nervous] 你确定吗？`
- **感叹号！** → 表示兴奋：`[happy] 我们做到了！`

结合标签和标点符号可以获得最佳效果：
```
[tired] It was a long day... [sighs] Nobody listens anymore.
```

## WhatsApp 语音消息

### 完整的工作流程

1. 使用 `tts` 工具生成音频文件（输出格式为 MP3）
2. 使用内置转换器将 MP3 文件转换为 Opus 格式（Android 设备必需）
3. 使用 `message` 工具发送音频文件

### 分步操作

**1. 生成 TTS 文件（在文件末尾添加 [pause] 标签以防止音频被截断）：**
```
tts text="[excited] This is amazing! [pause]" channel=whatsapp
```
输出文件：`MEDIA:/tmp/tts-xxx/voice-123.mp3`

**2. 使用转换器将 MP3 文件转换为 Opus 格式：**
```
python3 lib/audio_convert.py convert /tmp/tts-xxx/voice-123.mp3 /tmp/tts-xxx/voice-123.ogg
```

**3. 发送转换后的 Opus 文件：**
```
message action=send channel=whatsapp target="+972..." filePath="/tmp/tts-xxx/voice-123.ogg" asVoice=true message="‎"
```

### 为什么选择 Opus 格式？

| 格式 | iOS | Android | 是否支持转录功能 |
|--------|-----|---------|------------|
| MP3 | ✅ 支持 | ❌ 可能无法播放 | ❌ 不支持 |
| Opus (.ogg) | ✅ 支持 | ✅ 支持 | ✅ 支持 |

**务必将音频转换为 Opus 格式** - 因为它是唯一在所有设备（iOS 和 Android）上都能正常播放的格式，并且支持 WhatsApp 的转录功能。

### 音频截断问题

ElevenLabs 有时会截断音频文件的最后一个单词。**务必在文件末尾添加 `[pause]` 或 `...` 标签：**
```
[excited] This is amazing! [pause]
```

## 长篇音频（如播客）

对于超过 800 个字符的音频内容：
1. 将音频分割成多个长度不超过 800 个字符的片段
2. 使用 `tts` 工具为每个片段生成音频文件
3. 使用内置转换器将所有片段合并成一个文件
4. 将合并后的文件转换为 Opus 格式，然后发送

**注意：** 不要提及“第 2 部分”或“第 X 章”等分界信息，以保持音频的连贯性。

## 多角色对话

v3 支持同时生成多个角色的语音：

```
Jessica: [whispers] Did you hear that?
Chris: [interrupting] —I heard it too!
Jessica: [panicking] We need to hide!
```

**对话标签**：`[interrupting]`（打断），`[overlapping]`（重叠），`[cuts in]`（插入），`[interjecting]`（插话）

## 音频标签快速参考

| 类别 | 标签 | 使用场景 |
|----------|------|-------------|
| **情感** | [excited]（兴奋的），[happy]（快乐的），[sad]（悲伤的），[angry]（愤怒的），[nervous]（紧张的），[curious]（好奇的] | 表达主要情感状态，每个段落使用一个标签 |
| **语气** | [whispers]（低语的），[shouts]（大声的），[soft]（轻柔的），[rushed]（急促的），[drawn out]（拖长的） | 用于表示音量或语速的变化 |
| **反应** | [laughs]（笑声），[sighs]（叹息），[gasps]（喘息），[clears throat]（清嗓子），[gulps]（吞咽） | 表现自然的人际反应，适量使用 |
| **节奏** | [pause]（暂停），[hesitates]（犹豫），[stammers]（结巴），[breathes]（呼吸） | 用于控制节奏 |
| **角色特征** | [French accent]（法语口音），[British accent]（英式口音），[robotic tone]（机器人音调] | 用于模拟不同角色的语音特征 |
| **对话** | [interrupting]（打断），[overlapping]（重叠），[cuts in]（插入） | 用于表示多角色之间的对话 |

**效果较好的标签**：
- **情感标签**：`[excited]`（兴奋的），`[nervous]`（紧张的），`[sad]`（悲伤的），`happy`（快乐的）
- **反应标签**：`[laughs]`（笑声），`[sighs]（叹息）`, [whispers]（低语） |
- **节奏标签**：`[pause]`（暂停） |

**效果较弱的标签（需测试和重新生成）：**
- **音效标签**：`[explosion]`（爆炸），`[gunshot]`（枪声） |
- **口音标签**：不同语音的效果可能有所不同

**完整标签列表**：请参阅 [references/audio-tags.md](references/audio-tags.md)

## 常见问题及解决方法

**标签被大声读出来？**
- 使用 `eleven_v3` 模型进行测试
- 使用 IVC 或预制作的语音，避免使用 PVC 标签
- 简化标签（避免使用如 “tone” 这样的附加后缀）
- 增加文本长度（至少 250 个字符）

**语音表现不一致？**
- 文本片段过长，建议分段（每段不超过 800 个字符）
- 重新生成音频文件（v3 的输出结果可能不稳定）
- 尝试使用较低的稳定性设置

**WhatsApp 无法播放音频？**
- 确保音频文件格式为 Opus

**添加了标签但情感表达不明显？**
- 可能是因为语音与标签风格不匹配
- 尝试使用 **Creative**（0.0）稳定性模式
- 在标签周围添加更多上下文信息