---
name: mm-voice-maker
description: 通过 MiniMax Voice API 和 FFmpeg，支持语音合成、语音克隆、语音设计以及音频后期处理功能。适用于将文本转换为语音、创建自定义语音，或对音频进行加工/合并等场景。
---
# MiniMax 语音生成器

这是一个专业的文本转语音（TTS）工具，具备情感检测、语音克隆和音频处理功能，由 MiniMax 语音 API 和 FFmpeg 提供支持。

## 功能

| 功能领域 | 特点                |
|--------|-------------------|
| **文本转语音 (TTS)** | 支持同步（HTTP/WebSocket）、异步（长文本）和流式传输 |
| **基于片段的 TTS** | 可从 `segments.json` 文件中合成多种声音和情感，并自动合并片段 |
| **语音克隆** | 可克隆时长为 10 秒至 5 分钟的音频文件；支持根据文本提示进行语音设计 |
| **音频处理** | 支持音频格式转换、合并、归一化、裁剪以及去除静音（使用 FFmpeg） |

## 文件结构：
```
mmVoice_Maker/
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

[step2]. 将文本处理成脚本文件 → 存放在 `<cwd>/audio/segments.json` 中。注意：[step2.4] 非常重要，请在将脚本发送给用户之前仔细检查两次。

[step2.5]. ⚠️ 生成预览文件供用户确认（对于多声音内容强烈推荐）

[step3]. 向用户展示计划以获取确认

[step4]. 验证 `segments.json` 文件的内容

[step5]. 生成并合并音频文件 → 中间文件保存在 `<cwd>/audio/tmp/`，最终输出文件保存在 `<cwd>/audio/output.mp3` 中

[step6]. ⚠️ **关键步骤**：用户需先确认音频质量 → 确认无误后才能删除临时文件

> `<cwd>` 是 Claude 的当前工作目录（不是技能目录）。音频文件会根据 Claude 运行命令的位置进行保存。

### 第一步：验证环境

```bash
python check_environment.py
```

检查以下内容：
- Python 3.8 或更高版本
- 必需的包（`requests`, `websockets`）
- 是否已安装 FFmpeg
- 是否设置了 `MINIMAX_VOICE_API_KEY` 环境变量

如果 API 密钥未设置，请向用户索取并设置它：
```bash
export MINIMAX_VOICE_API_KEY="your-api-key-here"
```


### 第二步：决策与预处理

**⚠️ 最重要的原则：首先匹配性别**

在选择语音之前，必须先匹配角色的性别。这是不可商量的。

**黄金法则：**
- 如果角色是男性 → 使用男性声音
- 如果角色是女性 → 使用女性声音
- 如果角色是中性或其他性别 → 选择合适的中性声音

**为什么这很重要：**
- 如果性别匹配错误（例如，将男性角色设置为女性声音）会破坏沉浸感
- 即使角色特征匹配，性别也是首要考虑的因素
- 这对于经典文学作品、历史内容和专业旁白尤为重要

**示例：**
| 角色 | 错误的语音 | 正确的语音 |
|---------|-------------|---------------|
| 唐三藏（男性僧侣） | `female-yujie` ❌ | `Chinese (Mandarin)_Gentleman` ✅ |
| 林黛玉（女性） | `male-qn-badao` ❌ | `female-shaonv` ✅ |
| 曹操（男性武将） | `female-chengshu` ❌ | `Chinese (Mandarin)_Unrestrained_Young_Man` ✅ |

**决策指南：**
根据以下情况做出选择：
- 用户是否指定了特定模型？ → 使用该模型，否则使用默认模型 `speech-2.8`
- 是否需要多声音？ → 每个角色/说话者使用不同的语音 ID
- 对于 `speech-2.8` 模型：情感会自动匹配（可以不填写 `emotion` 字段）
- 对于较旧的模型：需要手动指定情感标签

**使用场景示例：**

| 场景 | 描述 | 需要处理的文本片段 | 语音选择 |
|------|-------------|-----------------|-----------------|
| **单声音** | 用户需要整个内容使用统一的声音。片段长度不超过 1,000,000 个字符 | 仅按长度分割片段 | 所有片段使用相同的语音 ID |
| **多声音** | 多个角色或说话者，每个角色使用不同的语音。根据说话者或角色进行分割 | 按逻辑单元（如说话者、对话等）分割片段 | 每个角色使用不同的语音 ID |
| **播客/访谈** | 主持人和嘉宾使用不同的语音 | 按说话者分割片段 | 主持人和嘉宾分别使用不同的语音 |
| **有声书/小说** | 旁白和角色的声音 | 按旁白和对话内容分割片段 | 旁白和角色分别使用不同的语音 |
| **纪录片** | 主要为旁白，偶尔包含引语 | 将所有片段合并为一个 | 使用统一的旁白声音 |
| **报告/公告** | 正式内容，语调需保持一致 | 将所有片段合并为一个 | 使用专业的语音 |

**处理工作流程（4 个子步骤）：**

**步骤 2.1：文本分割与角色分析**
首先，将文本分割成逻辑单元，并为每个片段确定对应的角色/说话者。

**重要原则：** 按逻辑单元分割，而不仅仅是按句子分割

**何时分割（重要！）：**
- 当不同说话者的内容明显分开时
- 在小说/有声书/访谈等场景中，当旁白和对话混合在同一句子中时

**何时不要分割（重要！）：**
- 第三人称叙述（如 “John said...” 或 “The reporter noted...”）
- 引语部分应保持旁白的声音
- 除非有特殊需求，否则保持旁白的声音

**决策依据：**

| 使用场景 | 例子 | 分割策略 |
|----------|---------|----------------|
| **单声音** | 长篇文章、新闻稿、公告 | 按长度分割（每个片段不超过 1,000,000 个字符），所有片段使用相同的语音 |
| **播客/访谈** | “Host: Welcome to the show. Guest: Thank you for having me.” | 按说话者分割片段 |
| **纪录片旁白** | “The scientist explained, ‘The results are promising.’” | 将所有片段合并为一个（使用旁白的声音） |
| **有声书/小说** | “‘Who’s there?’ she whispered.” | “‘Who’s there?’” 应使用角色的声音，“she whispered.” 应使用旁白的声音 |
| **报告** | “According to the report, the economy is growing.” | 将所有片段合并为一个 |

**示例1：单声音（使用 speech-2.8 模型）**
对于单声音内容（如新闻、公告、文章），仅按长度分割片段：
```json
[
  {"text": "First part of the article (under 1,000,000 chars)...", "role": "narrator", "voice_id": "female-shaonv", "emotion": ""},
  {"text": "Second part of the article (under 1,000,000 chars)...", "role": "narrator", "voice_id": "female-shaonv", "emotion": ""},
  {"text": "Third part of the article (under 1,000,000 chars)...", "role": "narrator", "voice_id": "female-shaonv", "emotion": ""}
]
```

**示例2：有声书中的多声音场景（使用 speech-2.8 模型）**
在有声书中，当旁白和对话混合在同一句子中时，需要分别处理：
```json
[
  {"text": "The detective entered the room.", "role": "narrator", "voice_id": "", "emotion": ""},
  {"text": "\"Who's there?\"", "role": "female_character", "voice_id": "", "emotion": ""},
  {"text": "she whispered.", "role": "narrator", "voice_id": "", "emotion": ""},
  {"text": "\"It's me,\"", "role": "male_character", "voice_id": "", "emotion": ""},
  {"text": "he replied calmly.", "role": "narrator", "voice_id": "", "emotion": ""}
]
```

**示例3：纪录片/播客旁白（使用 speech-2.8 模型）**
引语部分应保持旁白的声音（不需要分割）：
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
4. **Fourth: Match Personality & Role** — Choose the best fit based on personality traits, tone, and character role

**Voice Selection Decision Tree:**
```
这是一个专业领域（故事/新闻/纪录片）吗？
├── 是 → 从 voice_catalog 的第 2.1 节中选择合适的语音
└── 否 → 从 voice_catalog 的第 2.2 节中选择：
    第 1 步：匹配性别
    ├── 男性角色 → 仅选择男性声音
    └── 女性角色 → 仅选择女性声音
    第 2 步：匹配年龄组
    └── 儿童 / 青少年 / 成年人 / 老年人 / 专业人士
    第 3 步：匹配语言
    └── 选择与内容语言匹配的语音
    第 4 步：匹配性格和角色
    └── 根据语调、性格和角色选择最合适的语音
```

**Step 2.3: Emotions Segmentation** *(For non-2.8 series models only)*
For models other than speech-2.8 series, analyze emotions in your segments:
- For **long segments**, split further based on **emotional transitions**
- Add appropriate **emotion tags** to each segment
- Refer to Section 3 in [text-processing.md](reference/text-processing.md) for emotion tags and examples
- Skip this step for speech-2.8 models (emotion is auto-matched)

**Emotion Tags:**
- For speech-2.6 series (speech-2.6-hd and speech-2.6-turbo): happy, sad, angry, fearful, disgusted, surprised, calm, fluent, whisper
- For older models: happy, sad, angry, fearful, disgusted, surprised, calm (7 emotions)


**Step 2.4: Check and Post-processing**
Finally, review and optimize your script:
- Verify segment length limits (async TTS ≤1,000,000 characters)
- Clean up conversational text (remove speaker names if needed)
- Ensure consistency in voice and emotion tags
- **Critical check for multi-voice content**: For audiobooks, multi-voice fiction, or content where dialogue is presented from a first-person perspective, verify that narration and dialogue mixed in the same sentence are properly split.

  **When splitting IS needed (first-person dialogue in fiction/audiobooks):**
  
  Example: `"John asked, 'Where are you going?'"` should be split into:
  - Segment 1: `"John asked, "` - uses narrator voice (describes who is speaking)
  - Segment 2: `"Where are you going?"` - uses the character's voice (actual dialogue in first-person)

  This ensures proper voice differentiation: descriptive narration uses the narrator's voice, while the character's spoken words use the character's designated voice.

  **When splitting is NOT needed (third-person quotes in podcast/documentary/news):**
  
  In podcasts, documentaries, or news reports, quoted speech is typically presented in third-person narrative style - the speaker's words are being reported, not performed. Keep these as one segment with the narrator's voice and remove the speaker's name at the beginning:
  
  - `"Welcome to our show." → narrator voice, remove the speaker's name (like "The host said:") at the beginning
  - `"According to experts, 'This technology represents a significant breakthrough.'" → keep as one segment (narrator voice)
  - `"Scientists noted, 'The experimental results exceeded our expectations.'" → keep as one segment (narrator voice)
- **If the split is missing**: Go back to Step 2.1 and ensure dialogue portions are separated from narration with appropriate role labels.

**Create segments.json:**
After completing all 4 sub-steps, save the final `segments.json` to `<cwd>/audio/segments.json`.


### Step 2.5: Generate Preview for User Confirmation (Highly Recommended)

**For multi-voice content (audiobooks, dramas, etc.), always generate a preview first.**

This saves time and prevents waste when voice selections need adjustment.

**How to generate a preview:**
1. Create a smaller segments file with 10-20 representative segments (include all characters)
2. Generate the preview audio
3. Ask user to listen and confirm voice choices

**Preview segments.json example:**
```json
[
  {"text": "Narration opening...", "role": "narrator", "voice_id": "...", "emotion": ""},
  {"text": "Male character speaks...", "role": "male_character", "voice_id": "...", "emotion": ""},
  {"text": "Female character speaks...", "role": "female_character", "voice_id": "...", "emotion": ""},
  {"text": "More dialogue...", "role": "...", "voice_id": "...", "emotion":...)
]
```

**Preview command:**
```bash
python mmvoice.py generate segments_preview.json -o preview.mp3
```

**When user confirms preview:**
- Use the same voice selections for the full segments.json
- No need to re-select voices

---

### Step 3: Present plan to user for confirmation

Before proceeding to validation and generation, present the segmentation plan to the user and wait for confirmation:

**Present to the user:**
- **Roles identified**: List all characters/speakers in the text
- **Voice assignments**: Show which voice_id is assigned to each role (include voice characteristics from voice_catalog.md)
- **Model being used**: Explain why this model was selected
- **Language**: Confirm the primary language of the content
- **Emotion approach**: Auto-matched (speech-2.8) or manual tags (older models)


**Example confirmation message:**
```
我已经分析了文本并制定了分割计划：

**角色和对应的语音：**
- 旁白：`male-qn-jingying`（深沉、权威，适合讲述故事）
- 主角：`female-shaonv`（明亮、充满活力、年轻）
- 反派：`male-qn-qingse`（冷酷、具有威胁感）

**模型推荐：** `speech-2.8-hd`（自动匹配情感）
**语言：** 中文
**片段总数：** 8 个

请查看并确认：
1. ⚠️ **性别匹配**：角色的性别与所选语音的性别是否一致？
   - [旁白：男性 ✓] [主角：女性 ✓] [反派：男性 ✓]
2. **语言匹配**：所有语音的语言是否与内容语言一致？
   - [所有语音：中文 ✓]
3. 为每个角色分配的语音是否合适（考虑年龄和性格因素）？
4. 是否有需要合并或重新分割的片段？
5. 是否有其他修改建议？

**生成完成后：**
- 我会先生成一个预览文件供您审核
- 在您确认音频质量后，我会删除临时文件
- 如果不满意，我会重新生成，直到您满意为止

回复 “confirm” 以继续执行，或告诉我需要调整的地方。
```

**Wait for user response:**
- If user confirms → Proceed to Step 4 (validate)
- If user suggests changes → Update `segments.json` and present the plan again for confirmation


### Step 4: Validate segments.json (model, emotion, voice_id validation)

Before generating audio, validate the segments file:

```bash
# 默认模型：`speech-2.8-hd`（自动匹配情感）
python mmvoice.py validate <cwd>/audio/segments.json

# 指定模型以进行特定场景的验证
python mmvoice.py validate <cwd>/audio/segments.json --model speech-2.6-hd

# 验证可用语音与指定的语音 ID 是否匹配（此操作较慢，需要调用 API）
python mmvoice.py validate <cwd>/audio/segments.json --validate-voices

# 结合多个选项进行验证（推荐）
python mmvoice.py validate <cwd>/audio/segments.json --model speech-2.6-hd --validate-voices

# 使用 `--verbose` 选项查看详细的分割信息
python mmvoice.py validate <cwd>/audio/segments.json --model speech-2.6-hd --validate-voices --verbose

```

**Emotion Validation checks:**

| Model | Emotion Validation |
|-------|-------------------|
| **speech-2.8-hd/turbo** | Emotion can be empty (auto emotion matching) |
| **speech-2.6-hd/turbo** | All 9 emotions supported |
| **Older models** | happy, sad, angry, fearful, disgusted, surprised, calm (7 emotions) |

**Voice ID validation:**
**With `--validate-voices`:**
- Calls API once to get all available voices
- Validates each voice_id against the list
- Shows errors for invalid voice_ids (blocks validation)


### Step 5: Generate and merge audio

Generate audio for all segments and merge into final output.

**File placement (default behavior if user doesn't specify):**

```
<cwd>/                      # Claude 的当前工作目录
└── audio/                  # 生成的临时文件目录
    ├── tmp/                # 中间文件
    │   ├── segment_0000.mp3
    │   ├── segment_0001.mp3
    │   └── ...
    └── <custom_audio_name>.mp3             # 最终合并后的音频文件，文件名可自定义
```

Where `<cwd>` is Claude's current working directory (where commands are executed).

- If `-o` is not specified, output goes to `<cwd>/audio/output.mp3`
- Intermediate files go to `<cwd>/audio/tmp/`
- After user confirms the final audio, ask whether to delete `<cwd>/audio/tmp/`

**Basic usage:**
```bash
# 默认模型：`speech-2.8-hd`，输出文件路径为 <cwd>/audio/output.mp3`
python mmvoice.py generate <cwd>/audio/segments.json

# 指定输出路径
python mmvoice.py generate <cwd>/audio/segments.json -o <cwd>/audio/<custom_audio_name>.mp3

# 如需指定模型，可以这样使用
python mmvoice.py generate <cwd>/audio/segments.json --model speech-2.6-hd
```

**Skip existing segments (for rate limit retries):**
```bash
# 仅生成尚未生成的片段（跳过已存在的文件）
python mmvoice.py generate <cwd>/audio/segments.json --skip-existing
```

**Error handling:**
- If a segment fails, the script reports which segment and why
- Use `--continue-on-error` to generate remaining segments despite failures
- Use `--skip-existing` to skip already successfully generated segments (recommended for retries after rate limit)
- The script automatically uses fallback merging if FFmpeg filter_complex fails

### Step 6: Confirm and cleanup

**⚠️ CRITICAL: Never delete temp files until user confirms!**

After generation completes, you MUST follow this exact sequence:

**Step 6.1: Report generation result to user**
```
✓ 音频文件保存路径：<output_path>
  生成了 X/Y 个片段
  中间文件保存在：<cwd>/audio/tmp/
```

**Step 6.2: Ask user to confirm audio quality**
Ask the user to listen to the audio and confirm:
1. Is the audio quality satisfactory?
2. Are all voices appropriate?
3. Any adjustments needed?

**Step 6.3: Wait for user response**

**Step 6.4: Only after user confirms, offer cleanup**
```
确认音频质量后，可以删除临时文件：
rm -rf <cwd>/audio/tmp/
```

**NEVER execute rm -rf on temp files without explicit user confirmation!**

If user is NOT satisfied:
- Do NOT delete temp files
- Discuss what needs to be adjusted
- Re-generate affected segments if needed
- Ask for confirmation again


## Other Usage

Use the following when the task involves **voice creation**, **single-voice TTS** (sync/async), or **audio processing** instead of the main segment-based workflow. Each subsection gives CLI commands, script paths, and the reference doc to open for details.

### Voice creation (clone / design / list)

- **Purpose:** Create custom voices from audio (clone) or from a text description (design); list system and custom voices.
- **CLI (entry point: `mmvoice.py`):**
  ```bash
  python mmvoice.py clone AUDIO_FILE --voice-id VOICE_ID   # 克隆时长为 10 秒至 5 分钟的音频文件
  python mmvoice.py design "DESCRIPTION" --voice-id ID      # 根据文本设计语音
  python mmvoice.py list-voices                             # 列出所有可用的语音
  ```
- **Scripts:** `scripts/voice_clone.py` (clone), `scripts/voice_design.py` (design), `scripts/voice_management.py` (list/manage).
- **Documentation:** **reference/voice-guide.md** — cloning (quick + high-quality + step-by-step), design workflow, management.

### Text-to-speech (sync / async)

- **Purpose:** Single-voice TTS: sync for short text (≤10k chars), async for long text (up to 1M chars); optional streaming.
- **CLI:**
  ```bash
  python mmvoice.py tts "TEXT" -o OUTPUT.mp3 [-v VOICE_ID] [--model MODEL]
  ```
- **Scripts:** `scripts/sync_tts.py` (HTTP/WebSocket sync), `scripts/async_tts.py` (async task + poll).
- **Documentation:** **reference/tts-guide.md** — sync TTS, async TTS, streaming, segment-based production.

### Audio processing (merge / convert / normalize)

- **Purpose:** Merge files (with optional crossfade), convert format, normalize loudness, trim.
- **CLI:**
  ```bash
  python mmvoice.py merge FILE1 [FILE2 ...] -o OUTPUT [--crossfade MS]
  python mmvoice.py convert INPUT -o OUTPUT [--format FORMAT]
  ```
- **Scripts:** `scripts/sync_tts.py` (HTTP/WebSocket sync), `scripts/async_tts.py` (async task + poll).
- **Documentation:** **reference/tts-guide.md** — sync TTS, async TTS, streaming, segment-based production.

### Audio processing (merge / convert / normalize)

- **Purpose:** Merge files (with optional crossfade), convert format, normalize loudness, trim.
- **CLI:**
  ```