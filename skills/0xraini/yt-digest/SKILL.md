# yt-digest

从YouTube视频中提取摘要、字幕和关键片段。

## 功能

- **字幕提取**：获取包含时间戳的完整字幕。
- **摘要**：由AI生成的视频内容摘要。
- **关键片段**：提取视频中的重要章节和精彩部分。
- **音频输出**：将摘要转换为音频（通过sag技能实现）。

## 使用方法

```bash
# Get transcript
yt-digest transcript "https://youtube.com/watch?v=..."

# Get summary
yt-digest summary "https://youtube.com/watch?v=..."

# Get key moments/chapters
yt-digest chapters "https://youtube.com/watch?v=..."

# Full analysis
yt-digest analyze "https://youtube.com/watch?v=..."
```

## 输出结果

```
📺 Video: How to Build AI Agents
👤 Channel: TechChannel
⏱️ Duration: 15:32

## Summary
This video covers the basics of building AI agents...

## Key Moments
- 0:00 Introduction
- 2:30 Setting up the environment
- 5:45 Building the first agent
- 10:20 Advanced techniques
- 14:00 Conclusion

## Transcript (first 1000 chars)
...
```

## 系统要求

需要使用YouTube的字幕API（公开视频无需API密钥）。