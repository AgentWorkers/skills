---
name: grab
description: 从 URL 下载内容并将其归档（包括推文、X 文章、Reddit 帖子以及 YouTube 视频）。将媒体文件、文本、文字记录以及 AI 生成的摘要保存到结构清晰的文件夹中。
homepage: https://github.com/jamesalmeida/grab
when: "User shares a URL and wants to download/save/grab it, or asks to download a tweet video, YouTube video, Reddit post, or any media from a URL"
examples:
  - "grab this https://x.com/..."
  - "download this tweet"
  - "save this video"
  - "grab https://youtube.com/..."
  - "grab this reddit post"
tags:
  - download
  - media
  - twitter
  - youtube
  - reddit
  - transcript
  - archive
metadata: { "openclaw": { "emoji": "🫳", "requires": { "bins": ["yt-dlp", "ffmpeg", "whisper"] }, "install": [{ "id": "yt-dlp", "kind": "brew", "formula": "yt-dlp", "bins": ["yt-dlp"], "label": "Install yt-dlp (brew)" }, { "id": "ffmpeg", "kind": "brew", "formula": "ffmpeg", "bins": ["ffmpeg"], "label": "Install ffmpeg (brew)" }, { "id": "openai-whisper", "kind": "brew", "formula": "openai-whisper", "bins": ["whisper"], "label": "Install Whisper (brew)" }] } }
---

# grab 🫳  
从指定的 URL 下载内容，并将其整理到相应的文件夹中。  

## 设置  
### 依赖项  
```bash
brew install yt-dlp ffmpeg openai-whisper
```  

### 保存位置  
首次运行时，`grab` 会询问文件保存的位置（默认为：`~/Dropbox/ClawdBox/`）。  
配置信息存储在 `~/.config/grab/config` 文件中，可以通过 `grab --config` 命令进行重新配置。  

### 本地转录（使用 Whisper）  
内容会通过本地的 Whisper 服务进行转录（使用 `turbo` 模型），无需 API 密钥或网络请求。  

### AI 摘要与智能文件夹命名（可选）  
设置 `OPENAI_API_KEY` 可启用以下功能：  
- 由 AI 生成的内容摘要  
- 基于转录内容或图片分析生成的智能文件夹名称  

即使未设置 `OPENAI_API_KEY`，程序仍能正常运行，只是无法生成摘要或自动重命名文件夹。  

## 功能说明  

### 推文（x.com / twitter.com）  
- `tweet.txt`：推文文本、作者、发布日期及互动数据  
- `video.mp4`：附带的视频（如有）  
- `image_01.jpg` 等：附带的图片（如有）  
- `transcript.txt`：从视频中自动生成的文字记录（如有视频）  
- `summary.txt`：视频的 AI 摘要（如有视频）  
- 文件夹名称根据内容描述生成  

### X 杂志文章  
- `article.txt`：包含标题、作者和发布日期的完整文章文本  
- `summary.txt`：文章的 AI 摘要  
- 通过 OpenClaw 浏览器抓取文章内容  
- 当检测到文章时，脚本会以代码 2 和 `ARTICLE_DETECTED:<id>:<url>` 退出  

### Reddit  
- `post.txt`：帖子的标题、作者、子版块、评分及正文  
- `comments.txt`：包含作者和评分的顶级评论  
- `image_01.jpg` 等：附带的图片或图集（如有）  
- `video.mp4`：附带的视频（如有）  
- `transcript.txt`：从视频中自动生成的文字记录（如有视频）  
- `summary.txt`：帖子的 AI 摘要及讨论内容  
- 如果 Reddit 的 JSON API 被屏蔽（退出代码为 3），程序会使用 OpenClaw 浏览器获取内容  

### YouTube  
- `video.mp4`：视频文件  
- `description.txt`：视频描述  
- `thumbnail.jpg`：视频缩略图  
- `transcript.txt`：转录后的音频文本  
- `summary.txt`：视频的 AI 摘要  

## 输出结果  
下载的内容会按照类型进行分类整理：  
```
<save_dir>/
  XPosts/
    2026-02-03_embrace-change-you-can-shape-your-life/
      tweet.txt, video.mp4, transcript.txt, summary.txt
  XArticles/
    2026-01-20_the-arctic-smokescreen/
      article.txt, summary.txt
  Youtube/
    2026-02-03_how-to-build-an-ai-agent/
      video.mp4, description.txt, thumbnail.jpg, transcript.txt, summary.txt
  Reddit/
    2026-02-03_maybe-maybe-maybe/
      post.txt, comments.txt, video.mp4, summary.txt
```  

## 使用方法  
```bash
grab <url>              # Download and archive a URL
grab --config           # Reconfigure save directory
grab --help             # Show help
```  

## 系统要求  
```bash
brew install yt-dlp ffmpeg openai-whisper
```  

**注意：**  
- 转录功能使用本地的 Whisper 服务，无需 API 密钥。  
- `OPENAI_API_KEY` 环境变量为可选参数，用于启用 AI 摘要和智能文件夹命名功能。  
- 即使未设置 `OPENAI_API_KEY`，程序仍能完成媒体文件的下载和转录操作。