---
name: exa-plus
version: 1.0.0
description: 通过 Exa AI 实现的神经网络搜索功能。可以搜索个人、公司、新闻、研究资料以及代码。支持深度搜索、领域筛选和日期范围限定。
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["curl","jq"]}}}
---

# Exa - 神经网络搜索工具

这是一个强大的、基于人工智能的搜索工具，可以查询 LinkedIn、新闻、研究论文等资源。

## 设置

创建文件 `~/.clawdbot/credentials/exa/config.json`：
```json
{"apiKey": "your-exa-api-key"}
```

## 命令

### 常规搜索
```bash
bash scripts/search.sh "query" [options]
```

可选参数（作为环境变量）：
- `NUM=10` - 搜索结果数量（最多 100 条）
- `TYPE=auto` - 搜索类型：自动、神经网络、快速、深度
- `CATEGORY=` - 分类：新闻、公司、人物、研究论文、GitHub 代码、推文、PDF 文件、财务报告
- `DOMAINS=` - 需要包含的域名（用逗号分隔）
- `EXCLUDE=` - 需要排除的域名（用逗号分隔）
- `SINCE=` - 发布时间（ISO 格式）
- `UNTIL=` - 发布时间（ISO 格式）
- `LOCATION=NL` - 用户位置（国家代码）

### 示例

```bash
# Basic search
bash scripts/search.sh "AI agents 2024"

# LinkedIn people search
CATEGORY=people bash scripts/search.sh "software engineer Amsterdam"

# Company search
CATEGORY=company bash scripts/search.sh "fintech startup Netherlands"

# News from specific domain
CATEGORY=news DOMAINS="reuters.com,bbc.com" bash scripts/search.sh "Netherlands"

# Research papers
CATEGORY="research paper" bash scripts/search.sh "transformer architecture"

# Deep search (comprehensive)
TYPE=deep bash scripts/search.sh "climate change solutions"

# Date-filtered news
CATEGORY=news SINCE="2026-01-01" bash scripts/search.sh "tech layoffs"
```

### 获取内容
从 URL 中提取完整文本：
```bash
bash scripts/content.sh "url1" "url2"
```