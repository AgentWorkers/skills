# 视频分析技能

只需提供一个视频链接，即可对该视频进行分析。支持TikTok、YouTube、Instagram、Twitter/X以及1000多个其他平台。该技能会自动转录视频中的音频，并能回答用户关于视频内容的任何问题。

---

## 何时使用此技能

当用户执行以下操作时，可激活此技能：
- 分享视频链接（如tiktok.com、youtube.com、instagram.com、twitter.com等）
- 提问“这个视频是关于什么的？”、“请总结一下视频内容”、“视频主要讲了什么”等
- 对之前保存的视频提出疑问

---

## ⚠️ 重要规则 — 在使用前请务必阅读

**规则1 — 每次操作前都必须发送这条消息，无一例外：**

在使用任何执行命令之前，必须通过`message`工具发送以下消息：
> 📡 视频已接收，正在分析中...

这条消息必须通过`message`工具发送，而不能作为最终的回复内容。如果直接将这条消息写入回复中，用户将无法及时收到反馈，从而失去该技能的实用价值。

**规则2 — 处理过程中必须持续与用户保持沟通**
在处理视频的过程中，每30-60秒必须向用户发送一条反馈信息。如果长时间没有反馈，即表示系统出现故障。
- 下载完成后：发送“📥 下载完成！正在转录中...”
- 如果某个步骤耗时超过30秒：发送“⏳ 正在处理中...”

**规则3 — 绝对禁止添加个人评论**
严禁添加以下任何内容：
- “这个视频我们之前已经分析过”
- “我认识这个链接” / “您之前发过这个链接”
- “注意——这是同一个链接”
- 任何关于链接或之前使用情况的备注或解释

只需执行技能并给出答案，然后提示用户是否需要保存结果。仅此而已。

如果转录结果已被缓存，只需回复“📚 已保存在您的资料库中！”即可。

**规则4 — 首次使用时的提示**
如果用户的转录结果文件夹为空（首次使用），请提前告知用户：
> ⚠️ 首次使用——正在下载AI模型（约150MB），首次下载需要2-4分钟，之后就不会再需要下载了。

---

## 预先检查依赖项

在首次使用之前，请检查所有必要的依赖项是否已安装：

```bash
which ffmpeg && python3 -c "import faster_whisper; print('ok')" && python3 -c "import yt_dlp; print('ok')"
```

**如果缺少任何依赖项，请指导用户安装：**

Mac/Linux本地环境：
```bash
brew install ffmpeg
pip3 install faster-whisper yt-dlp --break-system-packages
```

Linux/VPS环境：
```bash
apt install -y ffmpeg
pip install faster-whisper yt-dlp --break-system-packages
```

---

## 使用流程

### 第一步 — 立即确认收到视频
发送消息：`📡 视频已接收，正在分析中...`

### 第一步（首次使用时的提示）
如果这是用户的首次使用（没有缓存过的转录结果），请提前告知用户：
> ⚠️ 首次使用——需要下载AI转录模型（约150MB），首次下载需要2-4分钟，之后就不会再需要下载了。请稍等片刻☕

### 第二步 — 下载视频文件
执行以下操作：
```bash
python3 ~/.openclaw/skills/tiktok-analyzer/transcribe.py --download-only "URL_HERE"
```

系统会返回一个JSON响应，其中包含`status: "downloaded"`和`video_id`。如果`from_cache: true`且`skip_transcribe: true`，则直接进入第三步，跳过第二步b。

### 第二步b — 发送进度信息（通过`message`工具），然后开始转录
使用`message`工具发送消息：`📥 下载完成！正在转录中...`

随后立即执行以下操作：
```bash
python3 ~/.openclaw/skills/tiktok-analyzer/transcribe.py --transcribe-only "VIDEO_ID"
```

请将`VIDEO_ID`替换为上一步中获取的`video_id`。

系统会返回一个JSON响应：
```json
{
  "transcript": "full text here...",
  "language": "en",
  "video_id": "abc123",
  "from_cache": false
}
```

如果`from_cache: true`（表示视频已从缓存中读取），则回复“📚 已在您的资料库中找到——答案已准备好！”并跳过后续的等待提示。

如果返回的JSON中包含`error`键，请如实告知用户错误信息（切勿向用户展示Python的错误堆栈追踪）。

### 第三步 — 回答用户的问题
根据转录结果回答用户的问题。如果没有具体问题，可以提供以下信息：
- **视频的主题**（1-2句话）
- **视频的主要内容/核心信息**（以项目符号列出）
- **视频的风格/目的**（教育性、娱乐性、故事性等）

### 第四步 — 提供保存选项（如果`from_cache: false`，则必须执行）
在给出答案后，务必询问用户是否需要保存转录结果：
> 💾 是否希望保存转录结果，以便日后可以再次查看？（是/否）

只有当`from_cache: true`（视频已保存在缓存中）时，才跳过此步骤。

如果用户选择保存，执行以下操作：
```bash
python3 ~/.openclaw/skills/tiktok-analyzer/save_transcript.py "VIDEO_ID" 'JSON_DATA'
```

确认保存结果：`✅ 已保存在您的视频资料库中！`

---

## 查找已保存的转录结果

当用户询问之前分析过的视频时：
1. 查看`~/.openclaw/skills/tiktok-analyzer/transcripts/`目录下的文件
2. 读取相应的`.json`文件
3. 根据保存的转录结果回答用户的问题

---

## 错误处理

| 错误类型 | 对应的回复 |
|-------|----------|
| 视频为私密或已被删除 | “该视频是私密的或已被删除，请尝试其他链接。” |
| 未安装ffmpeg | “您需要安装ffmpeg。在Mac上运行：`brew install ffmpeg`，在Linux上运行：`apt install ffmpeg`” |
| 未安装faster-whisper工具 | “请先安装faster-whisper工具（命令：`pip install faster-whisper yt-dlp`），然后再尝试。” |
| 下载超时/视频文件过大 | “该视频文件较大，可能需要更多时间下载——请尝试较短的视频片段或检查网络连接。” |

---

## 使用提示

- **演示时**：使用之前分析过的视频（由于缓存存在，可以立即得到结果，效果更佳）
- **首次使用时**：务必提前告知用户需要下载150MB的模型文件
- **支持所有平台**：faster-whisper工具兼容TikTok、YouTube、Instagram、Twitter、Reddit、Vimeo等1000多个平台