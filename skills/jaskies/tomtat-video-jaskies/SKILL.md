---
name: tomtat-video
description: 从提供的链接中提取YouTube视频的摘要内容。当吴先生发送视频链接并请求您总结视频内容、提取关键信息或分析视频主题时，可以使用此功能。
---
# YouTube视频摘要功能

该功能可以帮助我从YouTube视频中提取字幕（transcript），并根据吴先生的要求对视频内容进行总结。

## 实现步骤

1. **获取数据：** 使用`scripts/get_transcript.sh`脚本从视频URL中提取字幕。
2. **处理内容：** 读取字幕文件（VTT格式），并过滤掉时间标记，仅保留纯文本内容。
3. **生成摘要：** 利用现有的AI模型，根据视频的主要内容、逻辑结构生成易于理解的摘要。

## 提取字幕的命令

```bash
bash skills/public/tomtat-video/scripts/get_transcript.sh "<URL_VIDEO>"
```

## 注意事项
- 该功能优先提取越南语字幕；如果不存在越南语字幕，则会提取英语字幕。
- 对于过长的视频，我会分段生成摘要，以确保不会遗漏重要信息。
- 提供的摘要会遵循Thanh Tình的专业风格，呈现得既专业又生动。