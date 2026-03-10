---
name: kb-collector
description: >
  **知识库收集器（Knowledge Base Collector）**  
  - 可将YouTube视频、网页内容及文本保存到Obsidian数据库中，并提供人工智能摘要功能。  
  - 具备自动转录视频内容的能力；  
  - 支持定期（每周/每月）生成汇总邮件；  
  - 还支持夜间自动执行数据收集与整理工作。
---
# KB Collector

知识库收集器——将YouTube视频、URL以及文本内容自动转录并总结后保存到Obsidian中。

## 功能

- **YouTube视频收集**：下载音频文件，使用Whisper进行转录，并自动生成摘要。
- **URL收集**：获取网页内容并对其进行总结。
- **纯文本保存**：直接保存文本文件，并添加标签。
- **摘要生成**：每周/每月/每年发送电子邮件进行内容回顾。
- **夜间研究**：自动跟踪AI/大语言模型（LLM）及技术趋势。

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

## 使用方法（Bash版本 - 过时版本）

```bash
# Collect YouTube
./scripts/collect.sh "https://youtu.be/xxxxx" "stock,investing" youtube

# Collect URL
./scripts/collect.sh "https://example.com/article" "python,api" url

# Collect plain text
./scripts/collect.sh "My note" "tag1,tag2" text
```

## 夜间研究功能（新功能！）

自动跟踪AI/大语言模型（LLM）及技术趋势——每天运行并将结果保存到Obsidian中。

```bash
# Save to Obsidian only
./scripts/nightly-research.sh --save

# Save to Obsidian AND send email
./scripts/nightly-research.sh --save --send

# Send email only
./scripts/nightly-research.sh --send
```

### 功能特点
- 可搜索多个信息源（如Hacker News、Reddit、Twitter）。
- 可选择使用大语言模型（LLM）生成内容摘要。
- 保存内容时会添加标签。
- 可选择通过电子邮件接收每周/每月/每年的内容摘要。

### Cron作业设置（可选）

```bash
# Run every night at 10 PM
0 22 * * * /path/to/nightly-research.sh --save --send
```

## 配置

请编辑脚本以进行个性化设置：

```python
VAULT_PATH = os.path.expanduser("~/Documents/YourVault")
NOTE_AUTHOR = "YourName"
```

## 输出格式

保存的笔记文件路径为：`{VAULT_PATH}/yyyy-mm-dd-title.md`

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

- `yt-dlp`：用于下载YouTube视频。
- `faster-whisper`：用于文本转录。
- `requests` 和 `beautifulsoup4`：用于获取网页内容。
- （可选）`openai/anthropic`：用于生成AI摘要。

## 致谢

这是一款专为Obsidian设计的自动化笔记记录工具。