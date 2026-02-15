---
name: moodcast
description: 使用 ElevenLabs v3 的音频标签和 Sound Effects API，将任何文本转换为具有情感表达的音频，并加入环境音效。
metadata: {"moltbot":{"requires":{"env":["ELEVENLABS_API_KEY"]},"primaryEnv":"ELEVENLABS_API_KEY","homepage":"https://github.com/ashutosh887/moodcast"}}
---

# MoodCast

MoodCast可以将任何文本转换为带有环境音效的、富有情感表达的音频。该工具会分析文本内容，使用 ElevenLabs v3 的音频标签来增强文本的表达力，并为音频添加相应的环境音效。

## 适用场景

当用户希望实现以下需求时，可以使用 MoodCast：
- 听到带有自然情感表达的文本朗读
- 为文章、故事或剧本创建音频版本
- 生成具有氛围感的旁白
- 收听引人入胜的晨间简报
- 将枯燥的文本转化为引人入胜的音频内容

**常用指令：**
- `read this dramatically`（以戏剧性的方式朗读文本）
- `make this sound good`（让内容听起来更好）
- `moodcast this`（将文本转换为音频）
- `read with emotion`（带着情感朗读文本）
- `narrate this`（为内容添加旁白）

**命令行语法：**
`/moodcast`

## 核心功能

### 1. 情感分析及文本增强
- 自动分析文本，并插入适当的 v3 音频标签：
  - **情感标签**：`[excited]`（兴奋的）、`[nervous]`（紧张的）、`[angry]`（愤怒的）、`[sorrowful]`（悲伤的）、`[calm]`（平静的）
  - **朗读方式**：`[whispers]`（低语）、`[shouts]`（大声喊叫）、`[rushed]`（急促的）、`[slows down]`（放慢语速）
  - **反应动作**：`[laughs]`（笑声）、`[sighs]`（叹息）、`[gasps]`（倒吸一口气）、`[giggles]`（咯咯笑）、`[crying]`（哭泣）
  - **节奏控制**：`[pause]`（暂停）、`[breathes]`（呼吸声）、`[stammers]`（结巴）、`[hesitates]`（犹豫）

### 2. 环境音效生成
- 使用 Sound Effects API 生成与文本内容相匹配的背景音效：
  - 新闻：柔和的办公室环境音效
  - 故事：符合故事氛围的音效
  - 励志内容：振奋人心的背景音效
  - 恐怖内容：紧张、诡异的氛围音效

### 3. 多人对话
- 对于对话或剧本，可以为不同角色分配不同的声音和情感表达方式

## 使用说明

### 快速操作（单条命令）
```bash
python3 {baseDir}/scripts/moodcast.py --text "Your text here"
```

### 添加环境音效
```bash
python3 {baseDir}/scripts/moodcast.py --text "Your text here" --ambient "coffee shop background noise"
```

### 保存到文件
```bash
python3 {baseDir}/scripts/moodcast.py --text "Your text here" --output story.mp3
```

### 设置不同的情感风格
```bash
python3 {baseDir}/scripts/moodcast.py --text "Your text" --mood dramatic
python3 {baseDir}/scripts/moodcast.py --text "Your text" --mood calm
python3 {baseDir}/scripts/moodcast.py --text "Your text" --mood excited
python3 {baseDir}/scripts/moodcast.py --text "Your text" --mood scary
```

### 查看可用声音列表
```bash
python3 {baseDir}/scripts/moodcast.py --list-voices
```

### 自定义配置
```bash
python3 {baseDir}/scripts/moodcast.py --text "Your text" --voice VOICE_ID --model eleven_v3 --output-format mp3_44100_128
```

## 情感检测规则

该工具会自动检测并优化文本内容的情感表达：
| 文本内容 | 添加的音频标签 |
|-------------|-----------------|
| “amazing”, “incredible”, “wow” | `[excited]`（兴奋的） |
| “scared”, “afraid”, “terrified” | `[nervous]`（紧张的） |
| “angry”, “furious”, “hate” | `[angry]`（愤怒的） |
| “sad”, “sorry”, “unfortunately” | `[sorrowful]`（悲伤的） |
| “secret”, “quiet”, “between us” | `[whispers]`（低语） |
| “!”（感叹词） | `[excited]`（兴奋的） |
| 以 “...” 结尾的句子 | `[pause]`（暂停） |
| “haha”, “lol” | `[laughs]`（笑声） |
- 问句：使用自然的语调上升方式朗读

## 示例转换结果

**输入文本：**
```
Breaking news! Scientists have discovered something incredible. 
This could change everything we know about the universe...
I can't believe it.
```

**处理后的输出：**
```
[excited] Breaking news! Scientists have discovered something incredible.
[pause] This could change everything we know about the universe...
[gasps] [whispers] I can't believe it.
```

**输入文本：**
```
It was a dark night. The old house creaked. 
Something moved in the shadows...
"Who's there?" she whispered.
```

**处理后的输出：**
```
[slows down] It was a dark night. [pause] The old house creaked.
[nervous] Something moved in the shadows...
[whispers] "Who's there?" she whispered.
```

## 环境变量设置

- `ELEVENLABS_API_KEY`（必填）：您的 ElevenLabs API 密钥
- `MOODCAST_DEFAULT_VOICE`（可选）：默认声音 ID（默认为 `CwhRBWXzGAHq8TQ4Fs17`）
- `MOODCAST_MODEL`（可选）：默认模型 ID（默认为 `eleven_v3`）
- `MOODCAST_OUTPUT_FORMAT`（可选）：默认输出格式（默认为 `mp3_44100_128`）
- `MOODCAST_AUTO_AMBIENT`（可选）：设置为 `"true` 时，使用 `--mood` 命令会自动添加环境音效

**配置优先级：** 命令行参数的设置会覆盖环境变量的默认值。

## 技术细节

- 使用 ElevenLabs 的 Eleven v3 模型来处理音频标签
- 通过 Sound Effects API 生成环境音效（最长 30 秒）
- 免费试用：每月 10,000 个信用点（约 10 分钟的音频时长）
- 每段文本最多 2,400 个字符（v3 模型支持 5,000 个字符，为保证稳定性我们进行了限制）
- 音频标签需使用小写形式（例如：`[whispers]`，而非 `[WHISPERS]`）

## 使用建议

- **戏剧性强的内容**（如故事、新闻、剧本）效果最佳
- **较短的文本片段**（少于 500 个字符）听起来更自然
- 结合环境音效可提升沉浸感
- `Roger` 和 `Rachel` 这两个声音在 v3 模型下表现最为生动

## 开发者信息

由 [ashutosh887](https://github.com/ashutosh887) 开发  
基于 ElevenLabs 的 Text-to-Speech v3 和 Sound Effects API 实现  
专为 #ClawdEleven 编程马拉松项目开发