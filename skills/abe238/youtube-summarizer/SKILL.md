---
name: youtube-summarizer
description: **自动获取 YouTube 视频的字幕，生成结构化的摘要，并将完整的字幕发送到消息平台。**  
该功能能够识别 YouTube 的视频链接，提供视频的元数据、关键信息以及可下载的字幕文件。
version: 1.0.0
author: abe238
tags: [youtube, transcription, summarization, video, telegram]
---

# YouTube 摘要生成技能

该技能可自动从 YouTube 视频中获取字幕，生成结构化的摘要，并将完整字幕发送到消息平台。

## 使用场景

在以下情况下激活此技能：
- 用户分享了 YouTube 链接（如：youtube.com/watch、youtu.be、youtube.com/shorts）
- 用户请求对 YouTube 视频进行摘要生成或字幕转换
- 用户询问有关 YouTube 视频内容的信息

## 依赖项

**必需依赖项：** 必须在 `/root/clawd/mcp-server-youtube-transcript` 路径下安装 MCP YouTube 字幕服务器。如果未安装，请执行以下操作：
```bash
cd /root/clawd
git clone https://github.com/kimtaeyoon83/mcp-server-youtube-transcript.git
cd mcp-server-youtube-transcript
npm install && npm run build
```

## 工作流程

### 1. 检测 YouTube 链接
从以下格式中提取视频 ID：
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/shorts/VIDEO_ID`
- 直接视频 ID：`VIDEO_ID`（11 个字符）

### 2. 获取字幕
运行以下命令以获取字幕：
```bash
cd /root/clawd/mcp-server-youtube-transcript && node --input-type=module -e "
import { getSubtitles } from './dist/youtube-fetcher.js';
const result = await getSubtitles({ videoID: 'VIDEO_ID', lang: 'en' });
console.log(JSON.stringify(result, null, 2));
" > /tmp/yt-transcript.json
```

请将 `VIDEO_ID` 替换为提取到的视频 ID。输出结果将保存在 `/tmp/yt-transcript.json` 文件中。

### 3. 处理数据
解析 JSON 数据，提取以下信息：
- `result.metadata.title`：视频标题
- `result.metadata.author`：频道名称
- `result.metadata.viewCount`：观看次数
- `result.metadata.publishDate`：发布日期
- `result(actualLang`：使用的语言
- `result_lines`：字幕段落数组

完整字幕内容：`result_lines.map(l => l.text).join(' ')`

### 4. 生成摘要
使用以下模板生成结构化的摘要：
```markdown
📹 **Video:** [title]
👤 **Channel:** [author] | 👁️ **Views:** [views] | 📅 **Published:** [date]

**🎯 Main Thesis:**
[1-2 sentence core argument/message]

**💡 Key Insights:**
- [insight 1]
- [insight 2]
- [insight 3]
- [insight 4]
- [insight 5]

**📝 Notable Points:**
- [additional point 1]
- [additional point 2]

**🔑 Takeaway:**
[Practical application or conclusion]
```

摘要要求：
- 主要观点：1-2 句
- 关键要点：3-5 个要点（每个要点 1-2 句）
- 重要细节：2-4 个补充信息
- 总结：具有可操作性的结论

### 5. 保存完整字幕
将完整字幕保存为带时间戳的文件：
```
/root/clawd/transcripts/YYYY-MM-DD_VIDEO_ID.txt
```

文件应包含以下内容：
- 视频元数据信息
- 完整字幕文本
- 视频链接

### 6. 根据平台发送摘要
**如果目标平台是 Telegram：**
```bash
message --action send --channel telegram --target CHAT_ID \
  --filePath /root/clawd/transcripts/YYYY-MM-DD_VIDEO_ID.txt \
  --caption "📄 YouTube Transcript: [title]"
```

**如果目标平台是其他聊天工具或网页聊天：**
仅回复摘要内容（无需附件）。

### 7. 回复用户
将生成的结构化摘要作为回复发送给用户。

## 错误处理

**如果字幕获取失败：**
- 检查视频是否启用了字幕功能
- 如果请求的语言不可用，尝试使用 `lang: 'en'` 作为备用语言
- 通知用户字幕无法获取，并提供替代方案：
  - 使用 YouTube 的手动字幕功能
  - 视频可能没有字幕
  - 请尝试其他视频

**如果 MCP 服务器未安装：**
- 提供安装说明
- 在适当的情况下主动建议用户安装该服务器

**如果无法提取视频 ID：**
- 请用户提供完整的 YouTube 链接或视频 ID

## 示例
示例输出文件位于 `examples/` 目录中。

## 质量标准
- **简洁性：** 摘要应能在 30 秒内阅读完毕
- **准确性：** 不要添加字幕中不存在的信息
- **结构化：** 使用一致的格式以便阅读
- **针对性：** 根据视频长度调整详细程度：
  - 短视频（<5 分钟）：简短摘要
  - 长视频（>30 分钟）：更详细的解析

## 注意事项
- MCP 服务器使用 Android 客户端模拟技术来绕过 YouTube 的云 IP 阻止策略
- 该技能在 VPS 或云环境中稳定运行（yt-dlp 通常在这些环境中会遇到问题）
- 支持多种语言，并可自动切换到英文
- 字幕质量取决于 YouTube 自动生成的字幕或手动添加的字幕