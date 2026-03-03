---
name: kb-collector
description: 知识库收集器（Knowledge Base Collector）：能够将YouTube视频、网页链接以及文本内容保存到Obsidian数据库中，并提供人工智能生成的摘要。该工具具备自动转录视频内容的功能，可抓取网页信息，同时支持每周或每月生成汇总邮件。
---
# KB Collector

知识库收集器——将YouTube视频、URL以及纯文本内容保存到Obsidian中，并提供自动转录和摘要功能。

## 主要功能

- **YouTube视频收集**：下载音频文件，使用Whisper工具进行转录，并自动生成摘要。
- **URL内容收集**：获取并总结网页内容。
- **纯文本保存**：直接保存文本内容，并可添加标签。
- **内容汇总**：每周/每月/每年发送汇总邮件。

## 安装

```bash
# Install dependencies
pip install yt-dlp faster-whisper requests beautifulsoup4

# For AI summarization (optional)
pip install openai anthropic
```

## 使用方法（推荐使用Python版本）

```bash
# Collect YouTube video
python3 scripts/collect.py youtube "https://youtu.be/xxxxx" "stock,investing"

# Collect URL
python3 scripts/collect.py url "https://example.com/article" "python,api"

# Collect plain text
python3 scripts/collect.py text "My note content" "tag1,tag2"
```

## 使用方法（Bash版本）

```bash
# Collect YouTube
./scripts/collect.sh "https://youtu.be/xxxxx" "stock,investing" youtube

# Collect URL
./scripts/collect.sh "https://example.com/article" "python,api" url

# Collect text
./scripts/collect.sh "My note" "tag1,tag2" text
```

## 配置

请编辑脚本以进行个性化设置：

```python
VAULT_PATH = os.path.expanduser("~/Documents/YourVault")
NOTE_AUTHOR = "YourName"
```

## 输出格式

保存的笔记文件路径：`{VAULT_PATH}/yyyy-mm-dd-title.md`

```markdown
---
created: 2026-03-03T12:00:00
source: https://...
tags: [stock, investing]
author: George
---

# Title

> **TLDR:** Summary here...

---

Content...

---
*Saved: 2026-03-03*
```

## 所需依赖库

- `yt-dlp`：用于下载YouTube视频
- `faster-whisper`：用于转录音频
- `requests` + `beautifulsoup4`：用于获取网页内容
- 可选：`openai/anthropic`：用于智能摘要生成

## 致谢

这是一款专为Obsidian设计的自动化笔记记录工具。