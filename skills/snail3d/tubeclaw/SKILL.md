# TubeClaw - YouTube 视频分析工具

可以分析任何 YouTube 视频，提取关键信息，去除冗余内容，并提供包含相关链接的可操作性摘要。

## 功能介绍

- 📥 下载 YouTube 视频的字幕
- 🧠 分析视频内容以提取关键信息
- ✂️ 删除广告/赞助内容
- 🔗 提取视频中提到的资源/工具/链接
- 📝 提供简洁、实用的内容摘要

## 使用方法

### 命令行方式
```bash
node analyze.js --url "https://youtube.com/watch?v=..."
```

### 程序化方式
```javascript
const { analyzeVideo } = require('./analyze');

const result = await analyzeVideo('https://youtube.com/watch?v=...');
console.log(result.summary);
console.log(result.keyPoints);
console.log(result.resources);
```

## 系统要求

- Node.js 14 及以上版本
- 需要安装 OpenClaw/Clawdbot 并启用 `youtube-transcript` 插件
- 需要访问 AI 模型（如 Claude 或 OpenAI）来进行内容分析

## 工作原理

1. **提取字幕**：使用 `video-transcript-downloader` 插件下载视频的字幕文件。
2. **清理内容**：去除广告、赞助信息以及冗余的文字。
3. **内容分析**：通过 AI 技术提取视频中的关键信息和主题。
4. **查找资源**：识别视频中提到的工具、链接以及 GitHub 仓库。
5. **生成摘要**：生成一份包含关键信息的实用性摘要。

## 示例输出
```json
{
  "title": "Video Title",
  "channel": "Channel Name",
  "summary": "Clean summary without fluff...",
  "keyPoints": [
    "Main insight 1",
    "Main insight 2"
  ],
  "resources": [
    {
      "name": "Tool Name",
      "url": "https://...",
      "context": "Why it's mentioned"
    }
  ],
  "topics": ["AI", "Coding", "Tools"]
}
```

## 许可证

MIT 许可证 - OpenClaw