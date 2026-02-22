---
name: solo-you2idea-extract
description: 通过 solograph MCP 从 YouTube 视频中提取创业灵感：对视频字幕进行索引、搜索和分析，以获取商业创意。该系统采用多 MCP 协调模式（数据来源：YouTube → 分析 → 存储）。适用于用户提出以下需求时：从 YouTube 中提取灵感、对 YouTube 视频进行索引、在视频中寻找创业点子、分析视频内容以获取创意，或了解视频中包含的创意。**请勿将其用于普通观看 YouTube 视频（无需任何技能）或内容创作（请使用 /content-gen 功能）**。
license: MIT
metadata:
  author: fortunto2
  version: "2.0.0"
  openclaw:
    emoji: "💡"
allowed-tools: Read, Grep, Bash, Glob, Write, Edit, AskUserQuestion, mcp__solograph__source_search, mcp__solograph__source_list, mcp__solograph__source_tags, mcp__solograph__source_related, mcp__solograph__kb_search, mcp__solograph__web_search
argument-hint: "[video-url or channel-name or 'analyze <query>']"
---
# /you2idea-extract

从YouTube视频中提取创业创意。根据可用的工具，提供两种操作模式。

## 模式检测

检查可用的工具：
- **使用solograph MCP**：使用`source_search`、`source_list`、`source_tags`、`source_related`来处理索引化的数据集
- **不使用MCP（独立模式）**：使用`yt-dlp`和`Read`工具进行字幕分析

## MCP工具（如果可用）

- `source_search(query, source="youtube")` — 对索引化的视频进行语义搜索
- `source_list()` — 查看索引中的视频数量
- `source_tags()` — 自动检测主题并给出置信度评分
- `source_related(video_url)` — 通过共享的标签找到相关视频
- `kb_search(query)` — 与知识库进行交叉查询
- `web_search(query)` — 发现新的视频以进行索引

## 步骤

### 模式1：索引 + 分析（使用solograph MCP）

1. **解析输入**（来自 `$ARGUMENTS`）：
   - 视频URL（例如：`https://youtube.com/watch?v=...`） → 单个视频的索引
   - 频道名称（例如：`GregIsenberg`） → 频道批量索引
   - 查询文本 → 在现有数据集中搜索（跳到步骤4）
   - 如果输入为空，提示：“请输入视频URL、频道名称或搜索查询？”

2. **通过solograph对视频进行索引**：
   ```bash
   # Install if needed
   pip install solograph  # or: uvx solograph

   # Single video
   solograph-cli index-youtube -u "$URL"

   # Channel batch (needs web search for discovery)
   solograph-cli index-youtube -c "$CHANNEL" -n 5
   ```

3. **验证索引** — 使用`source_list()`确认新视频的数量；使用`source_tags()`查看主题分布。

4. **在数据集中搜索** — 使用`source_search(query="startup ideas", source="youtube")`进行搜索。

5. **进行交叉查询** — 使用`kb_search(query)`查找相关的现有机会（如果知识库可用）。

6. **提取见解** — 对于每个相关的视频片段：
   - 确定提到的创业创意
   - 记录时间戳和演讲者的背景信息
   - 评估创意的潜力（具体性、市场证据、可行性）
   - 标记符合趋势或经过验证的模式的相关创意

7. **将结果写入`docs/youtube-ideas.md`文件或打印摘要。

### 模式2：独立模式（不使用MCP）

1. **解析输入** — 与模式1的步骤1相同。

2. **通过`yt-dlp`下载字幕**：
   ```bash
   # Check yt-dlp is available
   command -v yt-dlp >/dev/null 2>&1 && echo "yt-dlp: ok" || echo "Install: pip install yt-dlp"

   # Download subtitles only (no video)
   yt-dlp --write-auto-sub --sub-lang en --skip-download -o "transcript" "$URL"

   # Convert VTT to plain text
   sed '/^$/d; /^[0-9]/d; /-->/d; /WEBVTT/d; /Kind:/d; /Language:/d' transcript.en.vtt | sort -u > transcript.txt
   ```

3. **读取字幕** — 打开`transcript.txt`文件。

4. **分析字幕以提取创业创意**：
   - 寻找商业机会、痛点、产品创意
   - 根据VTT（Video Text Tracks）中的时间戳记录大致的时间点
   - 评估每个创意的具体性和市场潜力
   - 通过WebSearch进行市场验证

5. **进行频道分析** — 下载多个视频的字幕：
   ```bash
   # Get video list from channel
   yt-dlp --flat-playlist --print "%(id)s %(title)s" "https://youtube.com/@$CHANNEL" | head -10

   # Download transcripts for top videos
   for id in $VIDEO_IDS; do
     yt-dlp --write-auto-sub --sub-lang en --skip-download -o "transcripts/%(id)s" "https://youtube.com/watch?v=$id"
   done
   ```

6. **将结果写入`docs/youtube-ideas.md`文件，格式如下**：
   ```markdown
   # YouTube Ideas — [Channel/Video]
   Date: YYYY-MM-DD

   ## Idea 1: [Name]
   - **Source:** [Video title] @ [timestamp]
   - **Problem:** [What pain point]
   - **Solution:** [What they propose]
   - **Market signal:** [Evidence of demand]
   - **Potential:** [High/Medium/Low] — [why]

   ## Idea 2: ...
   ```

## 常见问题

### 无法找到`yt-dlp`
**解决方法：** 使用`pip install yt-dlp`或`brew install yt-dlp`安装该工具。

### 没有字幕
**原因：** 视频没有自动生成的字幕或手动添加的字幕。
**解决方法：** 尝试使用`--sub-lang en,ru`参数来下载多种语言的字幕。有些视频只有自动生成的字幕。

### 无法使用`solograph MCP`
**解决方法：** 可以单独使用`yt-dlp`和`Read`工具。如果需要对多个视频进行索引化搜索，可以安装`solograph`：`pip install solograph`。为了增强Web搜索功能，可以设置[SearXNG](https://github.com/fortunto2/searxng-docker-tavily-adapter)（私有、自托管、免费）。

### 创意太多，难以优先排序
**解决方法：** 对排名前三的创意使用`/validate`命令，通过STREAM框架对它们进行评估和评分。