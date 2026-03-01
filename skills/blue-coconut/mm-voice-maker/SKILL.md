---
name: mm-voice-maker
description: 使用 MiniMax Voice API 和 FFmpeg 实现语音合成、语音克隆、语音设计以及音频后期处理功能。适用于将文本转换为语音、创建自定义语音，或处理/合并音频文件的场景。
---
# MiniMax 语音生成器

这是一个专业的文本转语音（TTS）工具，具备情感检测、语音克隆和音频处理功能，由 MiniMax 语音 API 和 FFmpeg 提供支持。

## 功能

| 功能领域 | 特点                |
|--------|-------------------|
| **文本转语音 (TTS)** | 同步（HTTP/WebSocket）、异步（长文本）、流式传输 |
| **基于段落的处理** | 从 `segments.json` 文件中合成多种声音和情感，支持自动合并 |
| **语音克隆** | 可克隆 10 秒至 5 分钟长度的音频文件；支持根据文本提示进行语音设计 |
| **音频处理** | 支持音频格式转换、合并、标准化、裁剪以及去除静音（使用 FFmpeg） |

## 文件结构：
```
mmVoiceMaker/
├── SKILL.md                       # This overview
├── mmvoice.py                     # CLI tool (recommended for Agents)
├── check_environment.py           # Environment verification
├── requirements.txt
├── scripts/                       # Entry: scripts/__init__.py
│   ├── utils.py                   # Config, data classes
│   ├── sync_tts.py                # HTTP/WebSocket TTS
│   ├── async_tts.py               # Long text TTS
│   ├── segment_tts.py             # Segment-based TTS (multi-voice, multi-emotion)
│   ├── voice_clone.py             # Voice cloning
│   ├── voice_design.py            # Voice design
│   ├── voice_management.py        # List/delete voices
│   └── audio_processing.py        # FFmpeg audio tools
└── reference/                     # Load as needed
    ├── cli-guide.md               # CLI usage guide
    ├── getting-started.md         # Setup and quick test
    ├── tts-guide.md               # Sync/async TTS workflows
    ├── voice-guide.md             # Clone/design/manage
    ├── audio-guide.md             # Audio processing
    ├── script-examples.md         # Runnable code snippets
    ├── troubleshooting.md         # Common issues
    ├── api_documentation.md       # Complete API reference
    └── voice_catalog.md           # Voice selection guide
```

## 主要工作流程（文本转语音）

**六步工作流程：**
[step1]. 验证环境

[step2-preparation]⚠️注意：在处理文本之前，请先阅读 [voice-catalog.md](reference/voice-catalog.md) 以选择合适的语音。

[step2]. 将文本处理成脚本文件，保存到 `<cwd>/audio/segments.json`。**[step2.4] 非常重要**，在将脚本发送给用户之前请务必检查两次。

[step2.5]. ⚠️ 生成预览文件供用户确认（对于多声音内容强烈推荐）

[step3]. 向用户展示计划以获取确认

[step4]. 验证 `segments.json` 文件的内容

[step5]. 生成并合并音频文件，中间文件保存在 `<cwd>/audio/tmp/`，最终输出文件保存在 `<cwd>/audio/output.mp3` 中

[step6]. ⚠️ **关键步骤**：用户需先确认音频质量，确认无误后才能删除临时文件

> `<cwd>` 是 Claude 的当前工作目录（非技能目录）。音频文件会相对于 Claude 运行命令的位置进行保存。

### 第 1 步：验证环境

```bash
python check_environment.py
```

检查以下内容：
- Python 3.8 或更高版本
- 必需的包（`requests`、`websockets`）
- 是否已安装 FFmpeg
- 是否设置了 `MINIMAX_VOICE_API_KEY` 环境变量

如果 API 密钥未设置，请向用户索取并设置它：
```bash
export MINIMAX_VOICE_API_KEY="your-api-key-here"
```

### 第 2 步：决策与预处理

**⚠️ 最重要的原则：先匹配性别**

在选择语音之前，必须先确保性别匹配正确。这一点不可商量。

**黄金法则：**
- 如果角色是男性 → 使用男性语音
- 如果角色是女性 → 使用女性语音
- 如果角色是中性或其他性别 → 选择合适的中性语音

**原因：**
- 如果性别匹配错误（例如，将男性角色设置为女性语音）会破坏沉浸感
- 即使角色性格特征匹配，性别也是首要考虑因素
- 这对于经典文学作品、历史内容和专业旁白尤为重要

**示例（性别 + 性格匹配）：**
| 角色 | 错误的语音 | 正确的语音 | 原因 |
|---------|-------------|---------------|-----------|
| 唐三藏（男性，温和的僧人） | `female-yujie` ❌ | `Chinese (Mandarin)_Gentleman` ✅ | 男性角色应使用温和的语音 |
| 林黛玉（女性，娇弱的少女） | `male-qn-badao` ❌ | `female-shaonv` ✅ | 女性角色应使用年轻、娇弱的语音 |
| 曹操（男性，专横的军阀） | `female-chengshu` ❌ | `male-qn-badao` ✅ | 男性角色应使用傲慢、强势的语音 |
| 王熙凤（女性，尖锐且强势） | `female-shaonv` ❌ | `Arrogant_Miss` ✅ | 女性角色应使用傲慢的语音 |

**决策指南：**
- 用户是否指定了特定模型？ → 使用该模型，否则使用默认模型 `speech-2.8`
- 是否需要多声音效果？ → 每个说话者/角色使用不同的语音 ID
- 对于 `speech-2.8` 模型：情感会自动匹配（可省略 `emotion` 参数）
- 对于较旧的模型：需要手动指定情感标签

**使用场景示例：**

| 场景 | 描述 | 需要处理的文本片段 | 语音选择方式 |
|--------|----------------|----------------|-------------------|
| **单声音** | 用户需要整个内容使用统一的声音。片段长度不超过 1,000,000 个字符 | 仅按长度分割片段 | 所有片段使用相同的语音 ID |
| **多声音** | 多个角色或说话者，每个角色使用不同的语音 | 按说话者或角色进行分割 | 每个角色使用不同的语音 ID |
| **播客/访谈** | 主播和嘉宾使用不同的语音 | 按说话者分割片段 | 主播和嘉宾使用各自的语音 |
| **有声书/小说** | 旁白和角色的声音 | 按旁白和对话内容分割片段 | 旁白和角色分别使用不同的语音 |
| **纪录片** | 主要为旁白，偶尔有引语 | 将所有内容视为一个整体片段 | 使用统一的旁白声音 |

**处理工作流程（4 个子步骤）：**

**Step 2.1：文本分割与角色分析**
首先，将文本分割成逻辑单元，并为每个片段确定对应的角色/说话者。

**关键原则（非常重要！）：按逻辑单元分割，而不仅仅是按句子分割**

**何时分割（非常重要！）：**
- 当不同说话者的内容明显分开时
- 在小说/有声书/访谈等场景中，当旁白和对话混合出现时

**何时不要分割（非常重要！）：**
- 第三人称叙述（如 “John said...” 或 “The reporter noted...”）
- 旁白中的引语应保持旁白的语音
- 除非有特殊要求，否则引语应保持旁白的语音

**决策依据：**

| 使用场景 | 示例 | 分割策略 |
|--------|---------|----------------|
| **单声音** | 长篇文章、新闻稿、公告 | 按长度分割（每个片段不超过 1,000,000 个字符），所有片段使用相同的语音 |
| **播客/访谈** | “Host: Welcome to the show. Guest: Thank you for having me.” | 按说话者分割 |
| **纪录片旁白** | “The scientist explained, ‘The results are promising.’” | 保持为一个整体片段（使用旁白的语音） |
| **有声书/小说** | “‘Who’s there?’ she whispered.” | 分割：“‘Who’s there?’” 使用角色的声音，“she whispered.” 仍使用旁白的声音 |
| **报告** | “According to the report, the economy is growing.” | 保持为一个整体片段 |

**示例 1：单声音（使用 speech-2.8 模型）**
对于单声音内容（如新闻、公告、文章），仅按长度分割片段，同时保持统一的语音：
```json
[
  {"text": "First part of the article (under 1,000,000 chars)...", "role": "narrator", "voice_id": "female-shaonv", "emotion": ""},
  {"text": "Second part of the article (under 1,000,000 chars)...", "role": "narrator", "voice_id": "female-shaonv", "emotion": ""},
  {"text": "Third part of the article (under 1,000,000 chars)...", "role": "narrator", "voice_id": "female-shaonv", "emotion": ""}
]
```

**示例 2：有声书（多声音）**
在有声书中（多声音小说中），当旁白和对话混合出现时，需要分别分割片段：
```json
[
  {"text": "The detective entered the room.", "role": "narrator", "voice_id": "", "emotion": ""},
  {"text": "\"Who's there?\"", "role": "female_character", "voice_id": "", "emotion": ""},
  {"text": "she whispered.", "role": "narrator", "voice_id": "", "emotion": ""},
  {"text": "\"It's me,\"", "role": "male_character", "voice_id": "", "emotion": ""},
  {"text": "he replied calmly.", "role": "narrator", "voice_id": "", "emotion": ""}
]
```

**示例 3：纪录片/播客旁白（使用 speech-2.8 模型）**
旁白中的引语应保持旁白的语音（无需分割）：
```json
[
  {
    "text": "The scientist explained, \"The results show significant improvement in all test groups.\"",
    "role": "narrator",
    "voice_id": "",
    "emotion": ""
  },
  {
    "text": "According to the latest report, the economy has grown by 3% this quarter.",
    "role": "narrator",
    "voice_id": "",
    "emotion": ""
  }
]

**Note:** In the preliminary `segments.json`:
- Fill in the `text` field with segment content
- Fill in the `role` field to identify the character (narrator, male_character, female_character, host, guest, etc.)
- Leave `voice_id` empty (to be filled in Step 2.2)
- Leave `emotion` empty for speech-2.8 models


**Step 2.2: Voice Selection**

After segmenting and labeling roles, analyze all detected characters in your text. Consult [voice_catalog.md](reference/voice_catalog.md) **Section 1 "How to Choose a Voice"** to match voices to characters.

**⚠️ CRITICAL: Follow the two-step selection process below**

**Path A — Professional domains (Story/Narration, News/Announcements, Documentary):**
If the content belongs to one of these three professional domains, prioritize selecting from the recommended voices in **voice_catalog.md Section 2.1** (filter by scenario + gender). These voices are specifically optimized for their professional use cases.

**Path B — All other scenarios:**
Select from **voice_catalog.md Section 2.2**, following this strict priority hierarchy:

1. **First: Match Gender** (non-negotiable) — Male characters MUST use male voices, female characters MUST use female voices
2. **Second: Match Language** — The voice MUST match the content language (Chinese content → Chinese voice, Korean content → Korean voice, English content → English voice, etc.). Never assign a voice from the wrong language.
3. **Third: Match Age** — Determine the age group (Children / Youth / Adult / Elderly / Professional) and select from the corresponding subsection in Section 2.2
4. **Fourth: Match Personality & Character Traits** — This step is critical for making each character sound distinct and alive. Analyze the character's personality, temperament, and role in the story, then select the voice whose description best matches those traits.

**⚠️ AVOID GENERIC DEFAULTS: Do NOT always fall back to the same safe/common voices (e.g., `female-shaonv`, `male-qn-qingse`, `Chinese (Mandarin)_Gentleman`) for every character.** The voice catalog offers many distinctive voices with unique personalities — use them! Each character in a story has a unique personality; the voice should reflect that personality.

**Personality-to-Voice Matching Guide:**

| Character Trait | Recommended Voice Style | Example voice_id (Chinese) |
|---|---|---|
| Domineering, arrogant | Arrogant, commanding voices | `male-qn-badao`, `badao_shaoye`, `Arrogant_Miss` |
| Gentle, warm | Soft, warm voices | `Chinese (Mandarin)_Gentleman`, `Chinese (Mandarin)_Warm_Girl` |
| Cold, aloof | Cool, distant voices | `lengdan_xiongzhang`, `Chinese (Mandarin)_Mature_Woman` |
| Playful, mischievous | Playful, cute voices | `qiaopi_mengmei`, `tianxin_xiaoling` |
| Wise, authoritative | Mature, steady voices | `Chinese (Mandarin)_Reliable_Executive`, `male-qn-jingying` |
| Flirty, romantic | Charming, seductive voices | `wumei_yujie`, `junlang_nanyou`, `diadia_xuemei` |
| Innocent, naive | Pure, youthful voices | `chunzhen_xuedi`, `Chinese (Mandarin)_Pure-hearted_Boy` |
| Rebellious, unrestrained | Bold, free-spirited voices | `Chinese (Mandarin)_Unrestrained_Young_Man`, `male-qn-badao` |

**Multi-character differentiation principle:** When a story has multiple characters of the same gender and similar age, you MUST differentiate them by personality. For example, in a story with three young men:
- A sly trickster → `Chinese (Mandarin)_Unrestrained_Young_Man` (不羁青年)
- A cute girl → `lovely_girl` (萌萌女童)


**Voice Selection Decision Tree:**
```

**这是专业领域吗？（故事/新闻/纪录片）**
├── 是 → 从 `voice-catalog` 的第 2.1 节中选择语音
└── 否 → 从 `voice-catalog` 的第 2.2 节中选择：
    Step 1：匹配性别
    ├── 男性角色 → 仅选择男性语音
    └── 女性角色 → 仅选择女性语音
    Step 2：匹配语言
    └── 选择与内容语言匹配的语音
    Step 3：匹配年龄组
    └── 儿童 / 青少年 / 成年人 / 老年人 / 专业人士
    Step 4：匹配性格和角色特征
    └── 分析角色性格，选择最符合的角色语音
        （不要使用通用语音——要根据角色性格选择合适的语音！）**

**示例代码：**
```json
[
  {"text": "Narration opening...", "role": "narrator", "voice_id": "...", "emotion": ""},
  {"text": "Male character speaks...", "role": "male_character", "voice_id": "...", "emotion": ""},
  {"text": "Female character speaks...", "role": "female_character", "voice_id": "...", "emotion": ""},
  {"text": "More dialogue...", "role": "...", "voice_id": "...", "emotion": ""},
]
```

**执行命令：**
```bash
python mmvoice.py generate segments_preview.json -o preview.mp3
```

**我已分析文本并制定了分割计划：**

**角色和对应语音：**
- 旁白：`audiobook_male_1`（发音清晰，节奏适中）
- 主角：`female-shaonv`（明亮、充满活力、年轻）
- 反派：`Chinese (Mandarin)_Unrestrained_Young_Man`（冷静、具有威胁感）

**模型：** `speech-2.8-hd`（推荐使用，支持自动情感匹配）
**语言：** 中文
**片段总数：** 8 个

请查看并确认：
1. ⚠️ **性别验证**：语音的性别是否与角色性别匹配？
   - [旁白：男性 ✓] [主角：女性 ✓] [反派：男性 ✓]
2. ⚠️ **语言验证**：语音的语言是否与内容语言匹配？
   - [所有语音：中文 ✓]
3. 语音分配是否适合每个角色（年龄、性格）？
4. 是否有需要合并或重新分割的片段？
5. 是否有其他修改建议？

**生成完成后：**
- 我会先生成一个预览文件供您审核
- 在您确认音频质量无误后，我会删除临时文件
- 如果不满意，我会重新生成，直到您满意为止

回复 “confirm” 以继续，或告诉我需要调整的地方。
```

**Wait for user response:**
- If user confirms → Proceed to Step 4 (validate)
- If user suggests changes → Update `segments.json` and present the plan again for confirmation


### Step 4: Validate segments.json (model, emotion, voice_id validation)

Before generating audio, validate the segments file:

```

**默认设置：** `speech-2.8-hd`（支持自动情感匹配）
```bash
python mmvoice.py validate <cwd>/audio/segments.json
```

**根据具体需求指定模型进行验证：**
```bash
python mmvoice.py validate <cwd>/audio/segments.json --model speech-2.6-hd
```

**验证可用语音：**
```bash
python mmvoice.py validate <cwd>/audio/segments.json --validate-voices
```

**组合使用选项（推荐）：**
```bash
python mmvoice.py validate <cwd>/audio/segments.json --model speech-2.6-hd --validate-voices
```

**使用 `--verbose` 选项查看详细信息：**
```bash
python mmvoice.py validate <cwd>/audio/segments.json --model speech-2.6-hd --validate-voices --verbose
```

**文件路径示例：**
```bash
<cwd>/                      # Claude 的当前工作目录
└── audio/                  # 生成的中间文件
    ├── tmp/                # 中间片段文件
    │   ├── segment_0000.mp3
    │   ├── segment_0001.mp3
    │   └── ...
    └── <custom_audio_name>.mp3             # 最终合并后的音频文件，文件名可自定义
```

**执行命令：**
```bash
# 默认设置：使用 speech-2.8-hd，输出文件保存在 <cwd>/audio/output.mp3`
python mmvoice.py generate <cwd>/audio/segments.json
```

**指定输出路径：**
```bash
python mmvoice.py generate <cwd>/audio/segments.json -o <cwd>/audio/<custom_audio_name>.mp3
```

**如果需要指定模型：**
```bash
python mmvoice.py generate <cwd>/audio/segments.json --model speech-2.6-hd
```

**仅生成未生成的片段：**
```bash
python mmvoice.py generate <cwd>/audio/segments.json --skip-existing
```

**删除临时文件：**
```bash
rm -rf <cwd>/audio/tmp/
```

**执行语音克隆和设计命令：**
```bash
python mmvoice.py clone AUDIO_FILE --voice-id VOICE_ID   # 克隆 10 秒至 5 分钟长度的音频
python mmvoice.py design "DESCRIPTION" --voice-id ID      # 根据文本设计语音
python mmvoice.py list-voices                             # 列出所有可用的语音
```

**其他相关命令：**
- **脚本：** `scripts/audio_processing.py`（用于音频合并、转换、标准化、裁剪）
- **文档：** `reference/audio-guide.md`（包含格式转换、合并（包括交叉淡入/淡出效果）、标准化、裁剪等操作）
```

### 基于段落的文本转语音（主要工作流程）

- **命令行界面 (CLI)：** 使用 `validate` 和 `generate` 命令，操作方式与上述步骤 4–5 相同。
- **脚本：** `scripts/segment_tts.py`
- **文档：** `reference/cli-guide.md` 和 `reference/api_documentation.md`

---

## 参考文档（按需查阅）

当您需要具体的使用方法、参数或遇到问题时，请查阅这些文档。文档路径相对于技能目录的根目录。

| 文档 | 内容                |
|----------|------------------------|
| **reference/cli-guide.md** | 所有 CLI 命令（`validate`、`generate`、`tts`、`clone`、`design`、`list-voices`、`merge`、`convert`、`check-env`）的用法和示例。 |
| **reference/getting-started.md** | 环境设置（虚拟环境、安装依赖包 FFmpeg）、`MINIMAX_VOICE_API_KEY`，以及基本的语音合成测试。适用于初次设置或环境配置问题 |
| **reference/tts-guide.md** | 同步文本转语音（短文本）、异步文本转语音（长文本）、流式文本转语音的功能和参数设置。 |
| **reference/voice-guide.md** | 语音克隆（快速、高质量的语音克隆功能，包含操作步骤和提示音频文件的使用方法）、语音设计、语音管理。 |
| **reference/audio-guide.md** | 音频格式转换、合并（包括交叉淡入/淡出效果）、标准化、裁剪等操作。 |
| **reference/script-examples.md** | 可直接运行的示例代码，用于同步文本转语音、异步文本转语音、基于段落的文本转语音、音频处理、语音克隆/设计等操作。 |
| **reference/troubleshooting.md** | 解决环境配置（API 密钥、FFmpeg 使用问题）、API 错误、基于段落的文本转语音相关问题。 |
| **reference/api_documentation.md** | 完整的 API 参考文档：配置参数、同步/异步文本转语音功能、情感参数设置、基于段落的文本转语音、语音克隆/设计、音频处理等功能的详细信息。 |
| **reference/voice_catalog.md** | 系统提供的语音列表（男性/女性/测试版）、语音选择指南、语音参数、自定义语音信息。用于选择或查找所需的语音 ID。 |

## 重要说明

### 系统要求**
- **Python**：版本需为 3.8 或更高
- **API 密钥**：必须设置 `MINIMAX_VOICE_API_KEY` 环境变量
- **FFmpeg**：用于音频处理（合并、转换、标准化）
  - 安装方法：`brew install ffmpeg`（macOS）或 `sudo apt install ffmpeg`（Ubuntu）

### 限制与注意事项**
- **文本长度**：同步文本转语音支持的文本长度不超过 10,000 个字符；异步文本转语音支持的文本长度不超过 1,000,000 个字符
- **语音克隆**：克隆的音频文件时长必须在 10 秒至 5 分钟之间，文件大小不超过 20MB，支持的音频格式为 mp3/wav/m4a
- **语音有效期**：自定义克隆或设计的语音文件在 7 天后失效，除非被用于文本转语音功能

### 特殊功能**
- **暂停插入**：在文本中使用 `<#x#>` 标记暂停时间（x 代表暂停时长，单位为秒，范围 0.01–99.99）
  - 例如：`"Hello<#1.5#>world` 表示在单词之间插入 1.5 秒的暂停
- **支持的情感类型**：快乐、悲伤、愤怒、恐惧、厌恶、惊讶、平静、流畅、低语
  - `speech-2.8` 模型支持自动情感匹配；`speech-2.6` 模型支持所有 9 种情感；较旧模型仅支持前 7 种情感

### 故障排除**
- 运行 `python check_environment.py` 以检查系统配置是否正确
- 查阅 [troubleshooting.md](reference/troubleshooting.md) 以获取常见问题的解决方案
- 参考 [getting-started.md](reference/getting-started.md) 以获取详细的设置指南