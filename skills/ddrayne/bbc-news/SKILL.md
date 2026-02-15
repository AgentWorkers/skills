---
name: bbc-news
description: 通过 RSS 源获取并显示 BBC 新闻的各个板块和地区的新闻内容。当用户请求 BBC 新闻、英国新闻头条、BBC 的世界新闻，或特定 BBC 板块（科技、商业、政治、科学、健康、娱乐、英国地区新闻或世界各地区新闻）时，可以使用该功能。
---

# BBC News

从BBC News的不同板块和地区获取头条新闻。

## 快速入门

获取头条新闻：
```bash
python3 scripts/bbc_news.py
```

从特定板块获取新闻：
```bash
python3 scripts/bbc_news.py uk
python3 scripts/bbc_news.py world
python3 scripts/bbc_news.py technology
```

列出所有可用板块：
```bash
python3 scripts/bbc_news.py --list
```

## 可用板块

### 主要板块
- `top` - 头条新闻（默认）
- `uk` - 英国新闻
- `world` - 世界新闻
- `business` - 商业新闻
- `politics` - 政治新闻
- `health` - 健康新闻
- `education` - 教育新闻
- `science` - 科学与环境
- `technology` - 科技新闻
- `entertainment` - 娱乐与艺术

### 英国地区板块
- `england` - 英格兰新闻
- `scotland` - 苏格兰新闻
- `wales` - 威尔士新闻
- `northern-ireland` - 北爱尔兰新闻

### 世界地区板块
- `africa` - 非洲新闻
- `asia` - 亚洲新闻
- `australia` - 澳大利亚新闻
- `europe` - 欧洲新闻
- `latin-america` - 拉丁美洲新闻
- `middle-east` - 中东新闻
- `us-canada` - 美国与加拿大新闻

## 选项

**限制新闻数量：**
```bash
python3 scripts/bbc_news.py world --limit 5
```

**JSON输出：**
```bash
python3 scripts/bbc_news.py technology --json
```

## 示例

获取英国的前5条新闻：
```bash
python3 scripts/bbc_news.py uk --limit 5
```

以JSON格式获取苏格兰新闻：
```bash
python3 scripts/bbc_news.py scotland --json
```

获取最新的科技头条：
```bash
python3 scripts/bbc_news.py technology --limit 3
```

## 依赖项

需要 `feedparser`：
```bash
pip3 install feedparser
```

## 资源

### scripts/bbc_news.py
一个Python命令行工具，用于从RSS源获取并显示BBC News的新闻。支持所有主要的BBC板块和地区，支持文本和JSON两种输出格式。

### references/feeds.md
按板块和地区整理的BBC News RSS源URL列表。