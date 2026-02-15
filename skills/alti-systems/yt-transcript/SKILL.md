# YouTube 视频字幕提取

使用多种方法从 YouTube 视频中提取高质量的字幕。

## 命令

```bash
# Extract transcript from YouTube URL or video ID
/root/clawd/yt-transcript https://youtu.be/VIDEO_ID
/root/clawd/yt-transcript VIDEO_ID
```

## 特点

- **双重备用系统**：首先尝试使用 Supadata API，如果失败则切换到 yt-dlp
- **自动生成字幕**：即使没有手动添加的字幕也能正常工作
- **干净的输出**：返回适合分析的纯文本字幕
- **快速**：API 方法可在几秒钟内完成提取

## 使用场景

- 在不观看视频的情况下总结视频内容
- 提取关键引文和见解
- 进行内容研究和分析
- 为视频创建书面摘要
- 提取教育类视频的内容

## 技术细节

- **主要工具**：Supadata API（速度快，格式清晰）
- **备用工具**：yt-dlp CLI（功能齐全，能处理特殊情况）
- **输出格式**：去除时间戳的纯文本字幕
- **API 密钥**：存储在 `.env` 文件中（键名为 `SUPADATA_API_KEY`）

## 示例工作流程

Rob 提供 YouTube 链接 → Alto 提取字幕 → 总结关键内容 → Rob 决定是否值得观看

每个视频可节省 10-30 分钟的时间！