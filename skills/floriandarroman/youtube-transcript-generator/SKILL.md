---
name: youtube-transcript-generator
description: 从任何 YouTube 视频中下载并生成清晰、易读的文字记录。该工具可以提取字幕（无论是自动生成的还是手动添加的），同时删除时间戳和格式化信息，最终输出格式为纯文本的段落式记录。适用于需要将 YouTube 视频内容转录为文字、获取文字记录或提取视频中的文本的场景。
---
# YouTube 字幕生成器

可以从任何 YouTube 视频 URL 下载干净的字幕文件。

## 使用要求

- 必须安装 `yt-dlp`（在 macOS 上使用 `brew install yt-dlp`，在 Linux 或 Windows 上使用 `pip install yt-dlp`）。

## 使用方法

使用以下命令运行脚本，并传入 YouTube 视频的 URL：

```bash
bash scripts/get_transcript.sh "https://www.youtube.com/watch?v=VIDEO_ID"
```

脚本将执行以下操作：
1. 首先尝试下载英语字幕；
2. 如果英语字幕不可用，会自动切换到自动生成的英语字幕；
3. 如果英语字幕仍然不可用，会尝试下载所有可用的字幕语言；
4. 将原始字幕文件处理成易于阅读的段落；
5. 将处理后的字幕内容输出到标准输出（stdout），并保存到 `transcript_video_ID.txt` 文件中。

## 可选参数

```bash
# Save to a specific file
bash scripts/get_transcript.sh "URL" output.txt

# Get transcript WITH timestamps (default: without)
bash scripts/get_transcript.sh "URL" output.txt en timestamps

# Get transcript in a specific language
bash scripts/get_transcript.sh "URL" output.txt fr
```

## 工作原理

1. `yt-dlp` 用于下载字幕文件（格式为 VTT/SRT）；
2. 脚本会去除 HTML 标签和重复的行；
3. **不包含时间戳（默认设置）**：将字幕内容合并成简洁、易读的段落；
4. **包含时间戳**：在每行字幕前保留 `[HH:MM:SS]` 的时间戳格式，以便于查看。

## 示例输出

输入：`https://www.youtube.com/watch?v=HMTxOecbyPg`

输出：
```
How OpenClaw Runs My Entire Business. I record a podcast episode and that is
literally the only thing I do. Everything else is handled by 13 AI agents
running on a Mac Mini in my office...
```

## 常见问题及解决方法

- **找不到字幕**：并非所有视频都配有字幕。脚本会显示可用的字幕语言。
- **未找到 `yt-dlp`**：请使用 `brew install yt-dlp`（macOS）或 `pip install yt-dlp` 进行安装。
- **受到下载速度限制**：请稍后再试。YouTube 有时会限制字幕下载的速率。

## 相关资源

- 完整的使用指南和模板：[OpenClaw Lab](https://openclawlab.xyz)
- 免费的 OpenClaw 安装程序：[installopenclawnow.com](https://installopenclawnow.com)
- OpenClaw 社区：[OpenClaw Lab on Skool](https://www.skool.com/openclaw-lab)