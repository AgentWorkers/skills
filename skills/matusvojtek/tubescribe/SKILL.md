---
name: TubeScribe
description: "**YouTube视频摘要工具：支持语音检测、格式化文档生成及音频输出**  
该工具可立即在macOS系统自带的TTS（文本转语音）功能上使用。推荐使用额外的工具（如pandoc、ffmpeg、mlx-audio）来提升输出质量。使用该工具需要互联网连接以访问YouTube视频。无需支付任何API费用或订阅服务。  

**使用场景：**  
当用户提供YouTube视频链接或请求对视频进行摘要/转录时，即可使用该工具。  

**主要功能：**  
1. **视频摘要生成**：自动提取视频的核心内容并生成结构化的文本文档。  
2. **语音检测**：识别视频中的说话者身份。  
3. **音频输出**：将处理后的音频文件以指定格式（如MP3）保存。  

**注意事项：**  
- 该工具基于macOS系统自带的TTS技术，兼容性强。  
- 部分高级功能（如pandoc、ffmpeg、mlx-audio）为可选插件，可提升输出效果。  

**适用人群：**  
视频编辑者、内容创作者、学习者等需要快速获取视频核心信息的用户。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "bins": ["summarize"] }
      }
  }
---

# TubeScribe 🎬

**将任何YouTube视频转换为精美的文档和音频摘要。**

只需提供YouTube链接，即可获得包含演讲者标签、关键引语、可链接回视频的时间戳，以及可以随时收听的音频摘要的漂亮转录文本。

### 💸 免费且无需API密钥

- **无需订阅或API密钥** — 无需额外配置即可使用
- **本地处理** — 转录、演讲者检测和文本转语音（TTS）都在您的机器上完成
- **网络访问** — 从YouTube获取字幕、元数据和评论需要网络连接
- **不上传任何数据** — 所有处理都在您的机器上完成，不会发送到外部服务
- **安全的子代理** — 生成的子代理有严格指令：不安装任何软件，不会进行超出YouTube范围的网络请求

### ✨ 主要功能

- **📄 带有摘要和关键引语的转录文本** — 可导出为DOCX、HTML或Markdown格式
- **🎯 智能演讲者检测** — 自动识别视频中的演讲者
- **🔊 音频摘要** — 可以收听视频中的关键内容（MP3/WAV格式）
- **📝 可点击的时间戳** — 每条引语都直接链接到视频中的相应位置
- **💬 YouTube评论** — 分析观众情绪并显示最佳评论
- **📋 队列支持** — 可同时处理多个链接
- **🚀 非阻塞式工作流程** — 视频处理时可以继续进行其他操作

### 🎬 支持任何类型的视频

- 采访和播客（多演讲者）
- 讲座和教程（单演讲者）
- 音乐视频（提取歌词）
- 新闻和纪录片
- 任何带有字幕的YouTube内容

## 快速入门

当用户发送YouTube链接时：
1. 立即启动子代理来处理整个流程
2. 回复：“🎬 TubeScribe正在处理中 — 处理完成后会通知您！”
3. 继续进行其他操作（无需等待！）
4. 子代理会发送完成通知，包括标题和详细信息

**请不要阻塞** — 立即启动子代理并继续其他操作。

## 首次设置

运行设置脚本以检查依赖项并配置默认值：

```bash
python skills/tubescribe/scripts/setup.py
```

此脚本会检查以下工具：`summarize` CLI、`pandoc`、`ffmpeg`、`Kokoro TTS`

## 完整工作流程（使用单个子代理）

启动一个子代理来处理整个流程：

```python
sessions_spawn(
    task=f"""
## TubeScribe: Process {youtube_url}

⚠️ CRITICAL: Do NOT install any software.
No pip, brew, curl, venv, or binary downloads.
If a tool is missing, STOP and report what's needed.

Run the COMPLETE pipeline — do not stop until all steps are done.

### Step 1: Extract
```bash
python3 skills/tubescribe/scripts/tubescribe.py "{youtube_url}"
```
Note the **Source** and **Output** paths printed by the script. Use those exact paths in subsequent steps.

### Step 2: Read source JSON
Read the Source path from Step 1 output and note:
- metadata.title (for filename)
- metadata.video_id
- metadata.channel, upload_date, duration_string

### Step 3: Create formatted markdown
Write to the Output path from Step 1:

1. `# **<title>**`
---
2. Video info block — Channel, Date, Duration, URL (clickable). Empty line between each field.
---
3. `## **Participants**` — table with bold headers:
   ```
   | **名称** | **角色** | **描述** |
   |----------|----------|-----------------|
   ```
---
4. `## **Summary**` — 3-5 paragraphs of prose
---
5. `## **Key Quotes**` — 5 best with clickable YouTube timestamps. Format each as:
   ```
   “这里写引语内容。” - [12:34](https://www.youtube.com/watch?v=ID&t=754s)
   “另一条引语。” - [25:10](https://www.youtube.com/watch?v=ID&t=1510s)
   ```
   Use regular dash `-`, NOT em dash `—`. Do NOT use blockquotes `>`. Plain paragraphs only.
---
6. `## **Viewer Sentiment**` (if comments exist)
---
7. `## **Best Comments**` (if comments exist) — Top 5, NO lines between them:
   ```
   在这里写评论内容。
   *- ▲ 123 @AuthorName*
   下一条评论内容。
   *- ▲ 45 @AnotherAuthor*
   ```
   Attribution line: dash + italic. Just blank line between comments, NO `---` separators.

---
8. `## **Full Transcript**` — merge segments, speaker labels, clickable timestamps

### Step 4: Create DOCX
Clean the title for filename (remove special chars), then:
```bash
pandoc <output_path> -o ~/Documents/TubeScribe/<safe_title>.docx
```

### Step 5: Generate audio
Write the summary text to a temp file, then use TubeScribe's built-in audio generation:
```bash
# 将摘要写入临时文件（使用python3以避免shell转义问题）
python3 -c "
text = '''YOUR SUMMARY TEXT HERE'''
with open('<temp_dir>/tubescribe_<video_id>_summary.txt', 'w') as f:
    f.write(text)
"

# 生成音频（根据配置自动选择引擎和格式）
python3 skills/tubescribe/scripts/tubescribe.py \
  --generate-audio <temp_dir>/tubescribe_<video_id>_summary.txt \
  --audio-output ~/Documents/TubeScribe/<safe_title>_summary
```
This reads `~/.tubescribe/config.json` and uses the configured TTS engine (mlx/kokoro/builtin), voice blend, and speed automatically. Output format (mp3/wav) comes from config.

### Step 6: Cleanup
```bash
python3 skills/tubescribe/scripts/tubescribe.py --cleanup <video_id>
```

### Step 7: Open folder
```bash
open ~/Documents/TubeScribe/
```

### Report
Tell what was created: DOCX name, MP3 name + duration, video stats.
""",
    label="tubescribe",
    runTimeoutSeconds=900,
    cleanup="delete"
)
```

**启动后，请立即回复：**
> 🎬 TubeScribe正在处理中 - 处理完成后会通知您！
然后继续进行其他操作。子代理会发送完成通知。

## 配置

配置文件：`~/.tubescribe/config.json`

```json
{
  "output": {
    "folder": "~/Documents/TubeScribe",
    "open_folder_after": true,
    "open_document_after": false,
    "open_audio_after": false
  },
  "document": {
    "format": "docx",
    "engine": "pandoc"
  },
  "audio": {
    "enabled": true,
    "format": "mp3",
    "tts_engine": "mlx"
  },
  "mlx_audio": {
    "path": "~/.openclaw/tools/mlx-audio",
    "model": "mlx-community/Kokoro-82M-bf16",
    "voice": "af_heart",
    "lang_code": "a",
    "speed": 1.05
  },
  "kokoro": {
    "path": "~/.openclaw/tools/kokoro",
    "voice_blend": { "af_heart": 0.6, "af_sky": 0.4 },
    "speed": 1.05
  },
  "processing": {
    "subagent_timeout": 600,
    "cleanup_temp_files": true
  }
}
```

### 输出选项
| 选项 | 默认值 | 描述 |
|--------|---------|-------------|
| `output_folder` | `~/Documents/TubeScribe` | 文件保存路径 |
| `output.open_folder_after` | `true` | 处理完成后打开输出文件夹 |
| `output.open_document_after` | `false` | 不自动打开生成的文档 |
| `output.open_audio_after` | `false` | 不自动打开生成的音频摘要 |

### 文档选项
| 选项 | 默认值 | 描述 |
|--------|---------|--------|-------------|
| `document.format` | `docx` | 输出格式（docx, html, md） |
| `document.engine` | `pandoc` | 用于生成DOCX的转换工具（默认为pandoc） |

### 音频选项
| 选项 | 默认值 | 描述 |
|--------|---------|--------|-------------|
| `audio.enabled` | `true` | 是否生成音频摘要 |
| `audio.format` | `mp3` | 音频格式（mp3需要ffmpeg） |
| `audio.tts_engine` | `mlx` | 用于文本转语音的引擎（mlx在Apple Silicon上性能最佳） |

### MLX-Audio选项（推荐在Apple Silicon上使用）
| 选项 | 默认值 | 描述 |
|--------|---------|-------------|
| `mlx_audio.path` | `~/.openclaw/tools/mlx-audio` | mlx-audio的路径 |
| `mlx_audio.model` | `mlx-community/Kokoro-82M-bf16` | 使用的MLX模型 |
| `mlx_audioVOICE` | `af_heart` | 默认语音预设 |
| `mlx_audio.voice_blend` | `{af_heart: 0.6, af_sky: 0.4}` | 自定义语音混合比例 |
| `mlx_audio.lang_code` | `a` | 语言代码（a=美式英语） |
| `mlx_audio.speed` | `1.05` | 播放速度（1.0 = 正常速度，1.05 = 快5%） |

### Kokoro PyTorch选项（备用方案）
| 选项 | 默认值 | 描述 |
|--------|---------|-------------|
| `kokoro.path` | `~/.openclaw/tools/kokoro` | Kokoro的路径 |
| `kokoro.voice_blend` | `{af_heart: 0.6, af_sky: 0.4}` | 自定义语音混合比例 |
| `kokoro.speed` | `1.05` | 播放速度（1.0 = 正常速度，1.05 = 快5%） |

### 处理选项
| 选项 | 默认值 | 描述 |
|--------|---------|-------------|
| `processing.subagent_timeout` | `600` | 子代理的处理超时时间（长视频可适当增加） |
| `processingcleanup_temp_files` | `true` | 处理完成后删除临时文件 |

### 评论选项
| 选项 | 默认值 | 描述 |
|--------|---------|-------------|
| `comments.max_count` | `50` | 获取的评论数量 |
| `comments.timeout` | `90` | 获取评论的超时时间（秒） |

### 队列选项
| 选项 | 默认值 | 描述 |
|--------|---------|-------------|
| `queue.stale_minutes` | `30` | 视为过时的处理任务的最长时间（分钟） |

## 输出结构

处理完成后，会打开包含所有文件的文件夹（而不是单独的文件）。

## 所需依赖项

**必需依赖：**
- `summarize` CLI — 使用`brew install steipete/tap/summarize`安装
- Python 3.8及以上版本

**可选依赖（提高质量）：**
- `pandoc` — 用于生成DOCX文件：`brew install pandoc`
- `ffmpeg` — 用于处理MP3音频：`brew install ffmpeg`
- `yt-dlp` — 用于获取YouTube评论：`brew install yt-dlp`
- `mlx-audio` — 在Apple Silicon上最快的文本转语音引擎：`pip install mlx-audio`（Kokoro使用此引擎）
- Kokoro TTS — 作为PyTorch的备用方案：详见https://github.com/hexgrad/kokoro

### yt-dlp的搜索路径

TubeScribe会按以下顺序查找这些工具：

| 优先级 | 路径 | 来源 |
|----------|------|--------|
| 1 | `which yt-dlp` | 系统PATH |
| 2 | `/opt/homebrew/bin/yt-dlp` | Homebrew（Apple Silicon） |
| 3 | `/usr/local/bin/yt-dlp` | Homebrew（Intel）/Linux |
| 4 | `~/.local/bin/yt-dlp` | 使用`pip install --user`安装 |
| 5 | `~/.local/pipx/venvs/yt-dlp/bin/yt-dlp` | 使用`pipx`安装 |
| 6 | `~/.openclaw/tools/yt-dlp/yt-dlp` | TubeScribe自动安装的版本 |

如果找不到相应的工具，系统会自动从指定路径下载。

## 队列管理

当用户同时发送多个YouTube链接时：

### 启动前的检查
```bash
python skills/tubescribe/scripts/tubescribe.py --queue-status
```

### 如果已有任务正在处理中
```bash
# Add to queue instead of starting parallel processing
python skills/tubescribe/scripts/tubescribe.py --queue-add "NEW_URL"
# → Replies: "📋 Added to queue (position 2)"
```

### 处理完成后
```bash
# Check if more in queue
python skills/tubescribe/scripts/tubescribe.py --queue-next
# → Automatically pops and processes next URL
```

### 队列命令
| 命令 | 描述 |
|---------|-------------|
| `--queue-status` | 显示当前正在处理和待处理的链接 |
| `--queue-add URL` | 将链接添加到队列 |
| `--queue-next` | 处理队列中的下一个链接 |
| `--queue-clear` | 清空整个队列 |

### 批量处理（同时处理多个链接）
```bash
python skills/tubescribe/scripts/tubescribe.py url1 url2 url3
```
依次处理所有链接，并在处理完成后生成摘要。

## 错误处理

脚本会检测并显示以下错误信息：

| 错误 | 说明 |
|-------|---------|
| 无效的URL | ❌ 非有效的YouTube链接 |
| 私人视频 | ❌ 视频是私有的，无法访问 |
| 视频已删除 | ❌ 视频找不到或已被删除 |
| 无字幕 | ❌ 该视频没有字幕 |
| 年龄限制 | ❌ 视频受年龄限制，无法访问 |
| 地区限制 | ❌ 视频在您的地区被屏蔽 |
| 直播流 | ❌ 不支持直播流，请等待直播结束 |
| 网络错误 | ❌ 网络问题，请检查网络连接 |
| 超时 | ❌ 请求超时，请稍后再试 |

遇到错误时，会向用户报告并停止处理该视频。

## 提示

- 对于时长超过30分钟的视频，建议将子代理的超时时间设置为900秒
- 演讲者检测在清晰的采访或播客格式下效果最佳
- 单演讲者的视频（如教程、讲座）会自动省略演讲者标签
- 时间戳会直接链接到视频中的相应位置
- 对于多个视频，可以使用批量处理模式：`tubescribe url1 url2 url3`