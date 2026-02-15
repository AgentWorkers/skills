---
name: voiceai-creator-voiceover-pipeline
description: "使用 Voice.ai 的 TTS（文本到语音）功能，将脚本转换为可发布的旁白内容，包括各个段落、章节、字幕以及视频的混合处理（video muxing）。"
version: 0.2.1
env:
  - VOICE_AI_API_KEY
required_env:
  - VOICE_AI_API_KEY
credentials:
  - VOICE_AI_API_KEY
setup: "none — single file, runs directly with Node.js"
runtime: "node>=20"
optional_deps: "ffmpeg"
---

# Voice.ai 创作者语音合成流程

> 本技能遵循 [Agent Skills 规范](https://agentskills.io/specification)。

将任何脚本转换为 **可直接发布的音频解说**——包括编号的片段、合并后的主音频文件、YouTube 分章节信息、SRT 字幕以及一个精美的审核页面。可选地，您还可以替换现有视频中的音频轨道。

专为那些希望获得专业级配音效果但无需使用专业录音室的创作者设计。由 [Voice.ai](https://voice.ai) 提供支持。

---

## 适用场景

| 场景 | 适用原因 |
|---|---|
| **YouTube 长视频** | 包含章节标记和字幕的完整旁白 |
| **YouTube 短视频** | 使用 `shortform` 模板制作简短的开场/结尾片段 |
| **播客** | 保持一致的主持人声音及开场/结尾模板 |
| **课程内容** | 教育视频的专业旁白 |
| **快速迭代** | 智能缓存机制——仅重新渲染修改过的片段 |
| **视频音频替换** | 将 AI 合成的音频添加到屏幕录制内容或背景素材中 |

---

## 一键工作流程

拥有脚本和视频吗？只需一个命令即可将它们转换为带有 AI 合成音频的成品视频：

```bash
node voiceai-vo.cjs build \
  --input my-script.md \
  --voice oliver \
  --title "My Video" \
  --video ./my-recording.mp4 \
  --mux
```

该命令会生成音频解说、合并主音频文件，并将其添加到您的视频中：

- `out/my-video/muxed.mp4` — 带有新音频解说的视频文件 |
- `out/my-video/master.wav` — 独立的音频文件 |
- `out/my-video/review.html` — 可用于听取和查看每个片段的审核页面 |
- `out/my-video/chapters.txt` — 适用于 YouTube 的章节时间戳文件 |
- `out/my-video/captions.srt` — SRT 字幕文件 |

如果音频长度短于视频长度，可以使用 `--sync pad` 选项；如果需要调整音频长度以匹配视频时长，则使用 `--sync trim` 选项。

---

## 必备要求

- **Node.js 20+** — 运行环境（无需安装 npm，因为 CLI 是一个独立的打包文件） |
- **VOICE.AI_API_KEY** — 需要设置为环境变量或技能根目录下的 `.env` 文件。您可以在 [voice.ai/dashboard](https://voice.ai/dashboard) 获取 API 密钥。 |
- **ffmpeg**（可选）—— 用于合并音频文件、MP3 编码、音量调整和视频合并。即使没有 ffmpeg，该流程仍能生成单独的片段、审核页面、章节信息和字幕。 |

---

## 配置

该技能会从以下位置读取 `VOICE.AI_API_KEY`：

1. 环境变量 `VOICE.AI_API_KEY`
2. 环境变量 `VOICEAI_API_KEY`（备用选项）
3. 技能根目录下的 `.env` 文件

```bash
echo 'VOICE_AI_API_KEY=your-key-here' > .env
```

在命令前加上 `--mock` 选项，可以无需 API 密钥即可运行整个流程（此时生成的音频为占位符）。

---

## 命令说明

### `build` — 从脚本生成音频解说

```bash
node voiceai-vo.cjs build \
  --input <script.md or script.txt> \
  --voice <voice-alias-or-uuid> \
  --title "My Project" \
  [--template youtube|podcast|shortform] \
  [--language en] \
  [--video input.mp4 --mux --sync shortest] \
  [--force] [--mock]
```

**功能：**
1. 读取脚本，并根据 `.md` 文件中的 `##` 标题或 `.txt` 文件中的句子边界将其分割成多个片段。
2. （可选）在片段前后添加模板化的开场/结尾片段。
3. 通过 Voice.ai 的 TTS 服务将每个片段转换为编号后的 WAV 文件。
4. （如果安装了 ffmpeg）合并主音频文件。
5. 生成章节信息、字幕、审核页面和元数据文件。
6. （可选）将音频解说合并到现有视频中。

**完整选项：**
| 选项 | 说明 |
|---|---|
| `-i, --input <path>` | 脚本文件（.txt 或 .md 格式）——**必需** |
| `-v, --voice <id>` | 音频角色的别名或 UUID —**必需** |
| `-t, --title <title>` | 项目标题（默认使用文件名） |
| `--template <name>` | `youtube`、`podcast` 或 `shortform` — 选择模板类型 |
| `--mode <mode>` | `headings` 或 `auto`（默认：.md 文件使用标题格式） |
| `--max-chars <n>` | 每个片段的最大字符数（默认：1500） |
| `--language <code>` | 语言代码（默认：en） |
| `--video <path>` | 用于合并的输入视频文件 |
| `--mux` | 启用视频合并功能（需要 `--video` 参数） |
| `--sync <policy>` | `shortest`、`pad` 或 `trim`（默认：`shortest`） |
| `--force` | 强制重新渲染所有片段（忽略缓存） |
| `--mock` | 模拟模式——不调用 API，使用占位符音频 |
| `-o, --out <dir>` | 自定义输出目录 |

### `replace-audio` — 替换视频中的音频轨道

```bash
node voiceai-vo.cjs replace-audio \
  --video ./input.mp4 \
  --audio ./out/my-project/master.wav \
  [--out ./out/my-project/muxed.mp4] \
  [--sync shortest|pad|trim]
```

该命令需要 ffmpeg。如果未安装 ffmpeg，系统会自动生成相应的 Shell/PowerShell 脚本。

| 同步策略 | 行为 |
|---|---|
| `shortest`（默认） | 输出时长与较短音频片段相同 |
| `pad` | 用静音填充音频以匹配视频时长 |
| `trim` | 剪裁音频以匹配视频时长 |

视频流会被原封不动地复制（使用 `-c:v copy` 命令），音频会被编码为 AAC 格式。同时会生成一个合并报告文件。

**隐私说明：** 视频处理完全在本地完成，只有脚本文本会被发送到 Voice.ai 进行语音合成。

### `voices` — 列出可用的语音角色

```bash
node voiceai-vo.cjs voices [--limit 20] [--query "deep"] [--mock]
```

---

## 可用语音角色

您可以使用以下别名或完整的 UUID 来选择语音角色：

| 别名 | 语音角色 | 性别 | 风格 |
|----------|----------------------|--------|--------------------------|
| `ellie`  | Ellie                | 女性 | 年轻、充满活力的博主风格 |
| `oliver` | Oliver               | 男性 | 友善的英式发音 |
| `lilith` | Lilith               | 女性 | 温柔、女性化的声音 |
| `smooth` | Smooth Calm Voice    | 男性 | 深沉、平稳的旁白风格 |
| `corpse` | Corpse Husband       | 男性 | 深沉、独特的声音 |
| `skadi`  | Skadi                | 女性 | 动漫角色风格 |
| `zhongli`| Zhongli              | 男性 | 深沉、权威的声音 |
| `flora`  | Flora                | 女性 | 欢快、高音调的声音 |
| `chief`  | Master Chief         | 男性 | 英雄主义、指挥风格 |

`voices` 命令还可以显示 API 中提供的其他可用语音角色。语音列表会缓存 10 分钟。

---

## 构建后的输出文件

构建完成后，输出目录中将包含以下文件：

### review.html

一个独立的 HTML 页面，包含：
- 合并后的主音频文件（如果使用了该选项）
- 带有标题和时长信息的单个片段播放器 |
- 每个片段的脚本文本（可折叠显示）
- 提供重新生成音频片段的提示

---

## 模板

模板会根据脚本内容自动生成开场/结尾片段：

| 模板类型 | 添加的开场/结尾文件 | 添加的结尾文件 |
|---|---|---|
| `youtube` | `templates/youtube_intro.txt` | `templates/youtube_outro.txt` |
| `podcast` | `templates/podcast_intro.txt` | — |
| `shortform` | `templates/shortform_hook.txt` | — |

您可以在 `templates/` 目录中编辑这些文件以自定义开场/结尾文本。

---

## 缓存机制

片段会根据以下信息进行缓存：`文本内容 + 语音角色 ID + 语言代码`。

- 未修改的片段在重新构建时会被跳过，从而实现快速迭代。
- 修改过的片段会自动重新生成。
- 可使用 `--force` 选项强制重新生成所有片段。
- 缓存信息存储在 `segments/.cache.json` 文件中。

---

## 多语言支持

Voice.ai 支持 11 种语言。使用 `--language <code>` 参数进行切换：

`en`, `es`, `fr`, `de`, `it`, `pt`, `pl`, `ru`, `nl`, `sv`, `ca`

对于非英语语言，系统会自动选择相应的语言 TTS 模型。

---

## 常见问题及解决方法

| 问题 | 解决方案 |
|---|---|
| **缺少 ffmpeg** | 即使没有 ffmpeg，流程仍能正常运行（会生成片段、审核页面、章节信息和字幕）。请安装 ffmpeg 以完成音频合并和视频合并。 |
| **达到速率限制（429）** | 片段会依次生成，通常不会超过速率限制。请稍后重试。 |
| **信用额度不足（402）** | 请在 [voice.ai/dashboard](https://voice.ai/dashboard) 充值。已缓存的片段在重试时不会重复使用信用额度。 |
| **脚本过长** | 缓存机制可加快重建速度。超过 490 个字符的片段会自动分批次发送。 |
| **Windows 路径** | 路径中包含空格时需用引号括起来：`--input "C:\My Scripts\script.md"` |

更多详细信息请参阅 [`references/TROUBLESHOOTING.md`](references/TROUBLESHOOTING.md)。

---

## 参考资料

- [Agent Skills 规范](https://agentskills.io/specification)
- [Voice.ai](https://voice.ai)
- [`references/VOICEAI_API.md`](references/VOICEAI_API.md) — API 端点、音频格式和模型信息 |
- [`references/TROUBLESHOOTING.md`](references/TROUBLESHOOTING.md) — 常见问题及解决方法