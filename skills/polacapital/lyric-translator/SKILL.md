---
name: lyric-translator
description: |
  Translate Indonesian song lyrics to natural-sounding English. Use when Beralio
  needs to translate their Indonesian lyrics for international release, sync
  licensing, or collaboration with English-speaking artists. Applies humanizer
  techniques to ensure translations feel authentic, poetic, and human-written—
  never robotic or AI-generated. Preserves rhythm, syllable flow, and emotional
  intent of the original.
---

# 歌词翻译器：印尼语 → 英语

将Beralio的印尼语歌词翻译成英语，使其听起来像是由英语母语歌手创作的，而不是由AI翻译的。

## 核心理念

**翻译是一种重写，而不仅仅是转换。** 优秀的歌词翻译应该捕捉到歌词的*情感*和*适合演唱的特质*，而不仅仅是字面意思。有时，你需要完全重新构思某一句歌词，才能使其在英语中通顺自然。

## 翻译流程

### 1. 先理解
- 在翻译之前，先通读整首歌的歌词。
- 确定每个段落的核心情感或主题。
- 注意歌词中的双关语、文化引用或多重含义。
- 了解每句歌词的音节结构和重音。

### 2. 为便于演唱而翻译
- 尽可能保持音节数量的一致性（允许相差1-2个音节）。
- 在强拍上保留重读音节。
- 在自然的情况下保留押韵结构；不要强行使用生硬的押韵。
- 相比字面准确性，更注重翻译后的*听觉效果*。

### 3. 强化人性化翻译
在歌词翻译中特别注意避免以下AI式的表达方式：

#### 应避免：
- ❌ 过于诗意或华丽的语言（如“情感的织锦”、“情感的交响乐”）
- ❌ 除非原歌词有意使用，否则避免使用常见的爱情歌曲陈词滥调
- ❌ 每个段落都使用完全相同的平行结构
- ❌ 为了追求“华丽”的词汇而刻意使用同义词词典
- ❌ 对隐喻进行解释（如果原歌词中隐喻性地使用了“hujan”（雨），就不要再加“like rain falling on my heart”这样的描述）
- ❌ 过度使用破折号
- ❌ 除非是为了故意的重复，否则不要让多行歌词以相同的词开头

#### 应采用：
- ✅ 通俗的表述方式（如“I don't know”而非“I am uncertain”）
- ✅ 缩略语（如“don't”, “can't”, “won't”, “I'm”, “you're”）
- ✅ 当某些表达更富有感染力时，可以使用句子片段
- ✅ 如果听起来更自然，可以使用不完美的语法
- ✅ 优先使用具体的意象而非抽象的概念
- ✅ 如果符合歌曲的风格，可以使用俚语
- ✅ 允许某些句子保持简单直接

### 4. 保留文化特色
- 一些印尼语表达在英语中没有对应的词汇——需要根据上下文进行重新构思：
- “Galau”可以根据不同情境翻译为“迷失”、“心烦意乱”、“混乱”或“思绪万千”
- “Rindu”可以翻译为“miss you”，但也可以考虑使用“ache for”或“long for”
- “Baper”可以翻译为“深陷情感之中”、“难以自拔”或“无法摆脱”

## 输出格式

对于每段翻译内容，提供如下格式：

```
### Original (Indonesian)
[paste original lyrics with section labels]

### Translation (English)
[translated lyrics with same section labels]

### Notes
- Key translation choices explained
- Lines where meaning was adapted for singability
- Cultural references that were reimagined
```

## 示例

### ❌ 不好的翻译（听起来像AI翻译）
**原歌词：** “Aku tak sanggup melihatmu pergi”
**糟糕的翻译：** “I find myself unable to witness your departure from my presence”
**问题：** 语言冗长、正式，不适合演唱，听起来像法律文件。

### ✅ 良好的翻译（人性化表达）
**原歌词：** “Aku tak sanggup melihatmu pergi”
**好的翻译：**
- “I can't watch you leave”（直接且适合演唱）
- “Don't make me watch you go”（更具情感表达，音节数量一致）
- “Watching you walk away breaks me”（如果需要更多音节）

---

### ❌ 不好的翻译（听起来像AI翻译）
**原歌词：** 
```
Kau bagai mentari
Yang menerangi hariku
```
**糟糕的翻译：**
```
You are like the radiant sun
Illuminating the entirety of my day
```
**问题：** 使用了诸如“radiant”、“illuminating”、“entirety”等AI风格的词汇；音节数量严重不匹配。

### ✅ 良好的翻译（人性化表达）
**原歌词：** 
```
Kau bagai mentari (5 syllables)
Yang menerangi hariku (8 syllables)
```
**好的翻译：**
```
You're the sun (3 syllables—close enough)
Lighting up my every day (7 syllables)
```

或者如果歌曲风格较为随意：
```
You're my sunshine
Making every day bright
```

---

## 节奏匹配指南

| 印尼语表达模式 | 英语翻译方法 |
|-------------------|------------------|
| 4-5个音节 | 保持3-5个音节的节奏 |
| 7-8个音节 | 尽量翻译为6-8个音节 |
| 长而连贯的句子 | 可以拆分成两个较短的短语 |
| 重复的音节结尾（押韵） | 优先选择自然的押韵方式，而非强行押韵 |

## 常见的印尼语歌词短语翻译

| 印尼语 | 应避免 | 应采用 |
|-----------|---------|------|
| Aku mencintaimu | I am loving you with all my heart | 我全心全意地爱你 |
| Kau begitu indah | You possess such immense beauty | 你如此美丽 |
| Hatiku hancur | My heart has been shattered into pieces | 我的心碎了 |
| Rindu | I am experiencing a profound longing | 我非常想念你 |
| Kenapa kau pergi | Why have you chosen to depart | 你为什么要离开？ |
| Aku tak bisa | I find myself incapable | 我无法做到 |
| Malam ini | On this particular evening | 在这个特别的夜晚 |
| Untuk selamanya | For the duration of eternity | 永远 |

## 质量检查

在交付翻译结果之前，大声朗读一遍英文版本，仿佛自己在唱歌一样。然后问自己：
1. 这段翻译是否流畅自然？
2. 这像是英语母语者写的吗？
3. 有没有使用到AI风格的词汇（如“delve”、“tapestry”、“journey”等）？
4. 重读音节是否落在强拍上？
5. 语言是否过于冗长？是否有可以删减的部分？
6. 翻译后的表达是否与原歌词的感觉一致？

如果有任何问题，就需要进行修改。

## 针对Beralio的特殊要求：
- Beralio的歌曲风格受流行乐/R&B影响——翻译应保持这种风格。
- 在不确定时，倾向于使用更随意的表达方式。
- 可以为关键歌词提供2-3个翻译选项。
- 标出那些直译会丢失重要意义的句子。
- 如果印尼语中某个段落有重复的内容，应保留这种重复结构。