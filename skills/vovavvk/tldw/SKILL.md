# tldw - YouTube 视频摘要工具

**太长；没看**  
快速高效地提取并总结 YouTube 视频的字幕内容。

## 概述  
tldw 工具接收一个 YouTube URL，提取视频的字幕，并提供内容的详细摘要，帮助用户无需观看完整视频即可快速了解视频内容。

### 目的  
该工具解决了视频内容信息过载的问题。用户无需花费 10 到 60 分钟观看视频，只需几秒钟就能获取关键点、主要论点和结论。

### 使用场景  
- 当用户提供 YouTube 视频 URL 并请求摘要时  
- 当你需要快速了解视频内容而不想观看时  
- 当你需要分析或引用特定视频内容时  
- 当你需要从教育、新闻或纪录片视频中提取信息时  

### 工作原理  
1. **提取**：使用 `yt-dlp` 下载视频字幕（字幕/标题）  
2. **清洗**：通过去重处理去除自动生成的字幕中的冗余内容  
3. **处理**：在主代理会话中直接分析清洗后的字幕  
4. **摘要**：返回包含主要观点、关键论点和结论的结构化摘要  

### 主要特性  
- **缓存**：下载的字幕会存储在本地，避免重复下载  
- **去重**：去除自动生成字幕中的重复行  
- **多格式支持**：支持 VTT、SRT 和 JSON 格式的字幕  
- **Cookie 支持**：可使用 Cookie 文件访问受限内容  
- **全面摘要**：包含论点、关键示例、对比和结论  
- **快速处理**：通常能在几秒钟内完成视频摘要  

### 来源  
该工具基于 [tldw 项目](https://github.com/rmusser01/tldw)（作者：stong）。完整的致谢和许可信息请参见 [ATTRIBUTION.md]。  

---

## 必备要求  

### 系统要求  
- **Python**：3.8 或更高版本  
- **磁盘空间**：约 60MB 用于虚拟环境和依赖项，另需额外空间存储字幕缓存  

### 必需依赖项  
该工具使用包含以下依赖项的 Python 虚拟环境：  
- **yt-dlp**：视频字幕下载工具（通过 pip 安装）  
- **Python 标准库**：`json`、`re`、`argparse`（内置库）  
所有依赖项均安装在 `venv/` 目录下的虚拟环境中。  

### 可选依赖项  
- **Cookie 文件**：用于访问受限或会员专享内容  
  - 格式：Netscape Cookie 格式（可从浏览器导出）  
  - 将其放在技能目录中，并使用 `--cookies` 标志指定  

### 目录结构  
```
tldw/
├── SKILL.md              # This documentation
├── ATTRIBUTION.md        # Credit to original project
├── LICENSE               # AGPL-3.0 license
├── scripts/
│   └── extract_transcript.py   # Main extraction script
├── cache/                # Cached transcripts (auto-created)
└── venv/                 # Python virtual environment
    ├── bin/
    │   └── yt-dlp        # Video transcript downloader
    └── lib/              # Python packages
```  

### 设置步骤  
按照以下步骤设置 tldw 工具：  
1. **进入技能目录：**  
   ```bash
   cd tldw/
   ```  
2. **创建 Python 虚拟环境：**  
   ```bash
   python3 -m venv venv
   ```  
3. **安装依赖项：**  
   ```bash
   venv/bin/pip install yt-dlp webvtt-py
   ```  
4. **验证安装：**  
   ```bash
   venv/bin/yt-dlp --version
   ```  
首次使用时，缓存目录将自动创建。  

### 使用说明  
1. 当用户提供 YouTube URL 并请求摘要时，按照以下流程操作：  
   - 使用提取脚本提取字幕  
   - 解析 JSON 输出以获取清洗后的字幕  
   - 直接对字幕进行总结（对于较长的字幕，不建议使用子代理）  
   - 向用户返回结构化摘要  

### 命令语法  
```bash
cd tldw/ && \
venv/bin/python scripts/extract_transcript.py \
  --json --cache-dir cache "YOUTUBE_URL"
```  

### 处理输出  
脚本返回的 JSON 数据结构如下：  
```json
{
  "transcript": "Full cleaned transcript text...",
  "video_id": "video_id_here",
  "title": "Video Title",
  "description": "Video description...",
  "duration": 1234,
  "uploader": "Channel Name",
  "upload_date": "20260101",
  "view_count": 12345,
  "webpage_url": "https://www.youtube.com/watch?v=..."
}
```  
直接提取 `transcript` 字段并对其进行处理，以生成详细的摘要。  

### 命令选项  
- `--json`：以 JSON 格式输出（推荐用于解析）  
- `--cache-dir <path>`：指定缓存目录（默认：`cache/`）  
- `--cookies <file>`：Netscape 格式的 Cookie 文件路径（用于访问受限内容）  

### 示例流程  
```bash
# 1. Extract transcript
cd tldw/ && \
venv/bin/python scripts/extract_transcript.py \
  --json --cache-dir cache "https://www.youtube.com/watch?v=VIDEO_ID"

# 2. Parse the JSON output and extract the transcript field

# 3. Summarize the transcript directly (include main points, key arguments, conclusions)

# 4. Return formatted summary to user
```  

### 访问受限内容  
对于受限或会员专享的视频，请按照以下步骤操作：  
1. 安装浏览器扩展程序（如 “Get cookies.txt LOCALLY”）  
2. 登录后访问 YouTube  
3. 将 Cookie 导出为 Netscape 格式  
4. 保存到 tldw 目录（例如：`youtube_cookies.txt`）  
5. 使用命令 `--cookies youtube_cookies.txt` 运行工具  

### 错误处理  
- **无字幕**：  
  **错误信息：** “未找到字幕/标题”  
  **含义：** 视频没有自动生成或手动添加的字幕。  
  **解决方法：** 告知用户视频无法被转录。  

- **无效 URL**：  
  **错误信息：** “ERROR: 无法下载视频数据”  
  **含义：** URL 格式错误、视频不存在或视频被设置为私密状态。  
  **解决方法：** 确认 URL 是否正确，并检查视频是否可公开访问。  

- **受限内容**：  
  **错误信息：** “请登录以验证年龄” 或类似认证错误  
  **含义：** 视频需要年龄验证或 YouTube 登录。  
  **解决方法：** 使用 `--cookies` 标志并提供浏览器导出的 Cookie。  

- **网络/连接问题**：  
  **错误信息：** “无法下载”、“连接超时” 或提取失败  
  **含义：** 网络问题、YouTube 阻止请求或 `yt-dlp` 版本过旧。  
  **解决方法：**  
    1. 更新 `yt-dlp`：  
      ```bash
   cd tldw/ && \
   venv/bin/pip install --upgrade yt-dlp
   ```  
    2. 重试提取。  
    3. 如果问题依旧存在，请检查网络连接或稍后尝试。  
YouTube 的 API 经常更新，因此保持 `yt-dlp` 的最新版本非常重要。  

- **缓存问题**：  
  **症状：** 权限错误或磁盘空间不足  
  **解决方法：** 使用 `df -h` 检查可用磁盘空间，并确认 `cache/` 目录的写入权限。  

- **处理长字幕**：  
  **注意：** 字幕超过 50,000 个字符时处理时间可能较长。  
  **最佳实践：** 直接在主代理会话中处理长字幕，避免使用子代理（因为子代理在处理大文件时可能不可靠）。  

- **调试**  
  **查看完整错误信息**：  
    ```bash
cd tldw/ && \
venv/bin/python scripts/extract_transcript.py \
  --json --cache-dir cache "YOUTUBE_URL"
```  
  **查看缓存字幕**：  
    ```bash
ls -lh tldw/cache/
```  

### 限制事项  
- **字幕依赖性**：  
  - 该工具 **仅适用于有字幕的视频**  
  - 无法转录只有音频的视频（无内置的语音转文本功能）  
  - 自动生成的字幕可能存在错误、拼写错误或时间同步问题  
  - 去重功能可帮助清理这些问题，但效果并非完美  

- **语言支持**：  
  - 取决于 YouTube 提供的字幕语言  
  - 脚本会提取所有可用的字幕（自动生成或手动添加的）  
  - 非英语字幕也可使用，但摘要质量取决于语言模型的性能  
  - 英语字幕通常效果最佳  

- **视频长度**：  
  - 非常长的视频（超过 2 小时）可能产生大量字幕（超过 100,000 个字符）  
  - 处理时间会随字幕长度增加  
  - 虽无硬性限制，但实际使用时需考虑上下文窗口和处理时间  

- **平台限制**：  
  - **仅支持 YouTube URL**  
  - 不支持其他视频平台（如 Vimeo、Dailymotion、TikTok 等）  
  - 虽然 `yt-dlp` 支持多种平台，但此脚本专为 YouTube 优化  

- **内容访问限制**：  
  - 无法访问真正私密的视频  
  - 会员专享或频道内容需要通过认证后的 Cookie 访问  
  - 直播视频可能需要在直播结束后才提供字幕  
  - 部分地理限制无法通过 Cookie 绕过  

- **去重限制**：  
  - 去重逻辑仅去除连续的重复行  
  - 有时可能会误删合法重复的内容  
  - 主要用于处理自动生成的字幕，不适用于所有重复情况  
  - 手动添加的字幕通常不需要去重  

- **音频提取**：  
  - 该工具仅提取 **文本字幕**，不处理音频文件  
  - 如需提取或处理音频，需使用其他工具（如带有音频参数的 `yt-dlp`）  
  - 该工具专注于基于文本的内容分析