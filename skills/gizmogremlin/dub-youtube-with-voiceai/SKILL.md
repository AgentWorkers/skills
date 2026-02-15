---
name: dub-youtube-with-voiceai
description: "使用 Voice.ai 的 TTS（文本到语音）功能为 YouTube 视频添加语音解说。将剧本转换为适合发布的配音内容，包括章节划分、字幕以及音频替换功能，适用于 YouTube 的长视频和短视频格式。"
version: 0.1.2
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

# 使用 Voice.ai 为 YouTube 视频添加旁白

> 本技能遵循 [Agent Skills 规范](https://agentskills.io/specification)。

您可以将任何脚本转换为适合在 YouTube 上使用的旁白内容，包括分段编号、合并后的音频文件、章节时间戳、SRT 字幕以及一个用于查看各段落的页面。只需一个命令，即可将旁白应用到现有的视频中。

专为那些希望获得专业级旁白效果但无需专业录音室的 YouTube 创作者设计。该工具由 [Voice.ai](https://voice.ai) 提供支持。

---

## 适用场景

| 场景 | 适用原因 |
|---|---|
| **YouTube 长视频** | 包含章节标记和字幕的完整旁白 |
| **YouTube 短视频** | 简短且富有感染力的旁白 |
| **课程内容** | 教育类视频的专业旁白 |
| **屏幕录制** | 为屏幕录制内容添加清晰的 AI 旁白 |
| **快速迭代** | 智能缓存机制——仅重新渲染修改的部分 |
| **批量制作** | 所有视频使用相同的旁白，保持一致的质量 |

---

## 一步完成的工作流程

拥有脚本和视频吗？只需一个命令即可完成配音：

```bash
node voiceai-vo.cjs build \
  --input my-script.md \
  --voice oliver \
  --title "My YouTube Video" \
  --video ./my-recording.mp4 \
  --mux \
  --template youtube
```

该命令会生成旁白、合并音频文件，并将其应用到您的视频中：

- `out/my-youtube-video/muxed.mp4`：带有 AI 旁白的视频文件 |
- `out/my-youtube-video/master.wav`：独立的音频文件 |
- `out/my-youtube-video/review.html`：用于查看各段落的页面 |
- `out/my-youtube-video/chapters.txt`：可直接粘贴到 YouTube 描述中 |
- `out/my-youtube-video/captions.srt`：用于上传到 YouTube 的字幕文件 |
- `out/my-youtube-video/description.txt`：包含章节信息的预设 YouTube 描述 |

如果音频长度短于视频长度，可以使用 `--sync pad` 选项；如果需要调整音频长度以匹配视频时长，可以使用 `--sync trim` 选项。

---

## 必备要求

- **Node.js 20+**：运行环境（无需安装 npm，因为命令行工具是一个独立的打包文件） |
- **VOICE.AI_API_KEY**：需设置为环境变量或放在技能根目录下的 `.env` 文件中。可在 [voice.ai/dashboard](https://voice.ai/dashboard) 获取 API 密钥。 |
- **ffmpeg**（可选）：用于合并音频文件、MP3 编码、音量调整以及视频配音。即使没有 ffmpeg，该工具仍能生成各段落的音频文件、查看页面、章节信息及字幕。

---

## 配置

在运行前，请将 `VOICE.AI_API_KEY` 设置为环境变量：

```bash
export VOICE_AI_API_KEY=your-key-here
```

该技能不会读取 `.env` 文件或访问其他文件来获取凭证信息，仅依赖环境变量。

在命令前加上 `--mock` 选项，即可在不使用 API 密钥的情况下运行整个流程（此时生成的音频为占位符）。

---

## 命令说明

### `build` — 从脚本生成适合 YouTube 的旁白

```bash
node voiceai-vo.cjs build \
  --input <script.md or script.txt> \
  --voice <voice-alias-or-uuid> \
  --title "My YouTube Video" \
  [--template youtube] \
  [--video input.mp4 --mux --sync shortest] \
  [--force] [--mock]
```

**功能：**
1. 读取脚本，并根据 `.md` 文件中的 `##` 标题或 `.txt` 文件中的句子边界将其分割成多个段落。
2. （可选）在开头或结尾添加 YouTube 的开场/结尾音频片段。
3. 通过 Voice.ai 的 TTS 服务为每个段落生成音频。
4. （如果安装了 ffmpeg）合并音频文件。
5. 生成 YouTube 需要的章节信息、SRT 字幕、查看页面以及预设的描述文件。
6. （可选）将生成的旁白应用到视频中。

**完整参数：**
| 参数 | 说明 |
|---|---|
| `-i, --input <path>` | 脚本文件（.txt 或 .md 格式） | **必需** |
| `-v, --voice <id>` | 旁白角色的别名或 UUID | **必需** |
| `-t, --title <title>` | 视频标题（默认使用文件名） |
| `--template youtube` | 自动添加 YouTube 开场/结尾音频 |
| `--mode <mode>` | `headings` 或 `auto`（默认：针对 `.md` 文件使用标题分段） |
| `--max-chars <n>` | 每个自动分段的最大字符数（默认：1500） |
| `--language <code>` | 语言代码（默认：en） |
| `--video <path>` | 需要配音的视频文件 |
| `--mux` | 启用视频配音功能（需配合 `--video` 使用） |
| `--sync <policy>` | `shortest`、`pad` 或 `trim`（默认：shortest） |
| `--force` | 强制重新渲染所有段落（忽略缓存） |
| `--mock` | 模拟模式——不进行 API 调用，使用占位符音频 |
| `-o, --out <dir>` | 自定义输出目录 |

### `replace-audio` — 为现有视频添加旁白

```bash
node voiceai-vo.cjs replace-audio \
  --video ./my-video.mp4 \
  --audio ./out/my-video/master.wav \
  [--out ./out/my-video/dubbed.mp4] \
  [--sync shortest|pad|trim]
```

该命令需要 ffmpeg。如果未安装 ffmpeg，系统会自动生成相应的 Shell/PowerShell 脚本。

| 同步策略 | 行为 |
|---|---|
| `shortest`（默认） | 当较短音频片段结束时，输出也会停止 |
| `pad` | 用静音填充音频以匹配视频时长 |
| `trim` | 将音频裁剪至与视频时长相同 |

视频流会原封不动地复制（使用 `-c:v copy`），音频会转换为 AAC 格式以适配 YouTube。

**隐私说明：** 视频处理完全在本地完成。只有脚本文本会被发送到 Voice.ai 进行 TTS 处理，您的视频文件不会离开您的设备。

---

## 可用的旁白角色

可以使用以下别名或完整的 UUID 来选择旁白角色：

| 别名 | 旁白角色 | 性别 | 适合的内容类型 |
|----------|----------------------|--------|-----------------------------------|
| `ellie`  | Ellie                | 女性 | Vlog、生活方式类内容 |
| `oliver` | Oliver               | 男性 | 教程、解说类内容 |
| `lilith` | Lilith               | 女性 | ASMR、引导类内容 |
| `smooth` | Smooth Calm Voice    | 男性 | 纪录片、长篇文章类内容 |
| `corpse` | Corpse Husband       | 男性 | 游戏、娱乐类内容 |
| `skadi`  | Skadi                | 女性 | 动漫、角色相关内容 |
| `zhongli`| Zhongli              | 男性 | 游戏、戏剧性开场动画 |
| `flora`  | Flora                | 女性 | 儿童内容、轻松愉快的视频 |
| `chief`  | Master Chief         | 男性 | 游戏、动作片预告 |

`voices` 命令还可以显示 API 中提供的其他可用旁白角色。旁白角色列表会缓存 10 分钟。

---

## 构建后的输出文件

构建完成后，输出目录中会包含所有用于发布到 YouTube 的文件：

```
out/<title-slug>/
  segments/           # Numbered WAV files (001-intro.wav, 002-section.wav, …)
  master.wav          # Stitched voiceover (requires ffmpeg)
  master.mp3          # MP3 for upload (requires ffmpeg)
  muxed.mp4           # Dubbed video (if --video --mux used)
  chapters.txt        # Paste into YouTube description
  captions.srt        # Upload as YouTube subtitles
  description.txt     # Ready-made YouTube description with chapters
  review.html         # Interactive review page with audio players
  manifest.json       # Build metadata: voice, template, segment list
  timeline.json       # Segment durations and start times
```

### YouTube 使用流程

1. 运行 `build` 命令。
2. 上传 `muxed.mp4` 文件（或原始视频文件加上 `master.mp3` 音频文件）。
3. 将 `chapters.txt` 文件的内容粘贴到 YouTube 描述中。
4. 将 `captions.srt` 文件作为字幕上传到 YouTube Studio。
5. 几分钟内即可完成专业旁白、章节信息及字幕的添加。

---

## YouTube 模板

使用 `--template youtube` 可自动生成带有品牌标识的开场和结尾音频：

| 部分 | 源文件 |
|---|---|
| 开场（前置） | `templates/youtube_intro.txt` |
| 结尾（后置） | `templates/youtube_outro.txt` |

您可以在 `templates/` 目录中编辑这些文件以自定义频道风格。

---

## 缓存机制

各段落的缓存依据以下信息生成：`文本内容 + 旁白角色 ID + 语言代码`。

- 未修改的段落会在重建时被跳过，从而实现快速迭代。
- 修改过的段落会自动重新生成。
- 可使用 `--force` 选项强制重新生成所有段落。
- 缓存信息存储在 `segments/.cache.json` 文件中。

---

## 多语言配音

Voice.ai 支持 11 种语言，可为您的 YouTube 视频提供多语言配音：

`en`、`es`、`fr`、`de`、`it`、`pt`、`pl`、`ru`、`nl`、`sv`、`ca`

```bash
node voiceai-vo.cjs build \
  --input script-spanish.md \
  --voice ellie \
  --title "Mi Video" \
  --language es \
  --video ./my-video.mp4 \
  --mux
```

对于非英语语言，系统会自动选择相应的多语言 TTS 模型。

---

## 常见问题及解决方法

| 问题 | 解决方案 |
|---|---|
| **缺少 ffmpeg** | 即使缺少 ffmpeg，系统仍能生成各段落、查看页面、章节信息及字幕。请安装 ffmpeg 以完成音频合并和配音。 |
| **速率限制（429）** | 各段落的生成是顺序进行的，通常不会超过速率限制。请稍后再试。 |
| **信用额度不足（402）** | 请在 [voice.ai/dashboard](https://voice.ai/dashboard) 充值。缓存中的段落在重试时不会重复使用信用额度。 |
| **脚本过长** | 缓存机制可加快重建速度。如果段落超过 490 个字符，系统会自动分批发送请求。 |
| **Windows 路径问题** | 使用引号括起路径：`--input "C:\My Scripts\script.md"` |

更多详细信息请参阅 [`references/TROUBLESHOOTING.md`](references/TROUBLESHOOTING.md)。

---

## 参考资料

- [Agent Skills 规范](https://agentskills.io/specification)
- [Voice.ai](https://voice.ai)
- [`references/VOICEAI_API.md`](references/VOICEAI_API.md)：API 端点、音频格式、可用角色 |
- [`references/TROUBLESHOOTING.md`](references/TROUBLESHOOTING.md)：常见问题及解决方法