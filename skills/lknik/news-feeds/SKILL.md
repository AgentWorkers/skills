---
name: news-feeds
description: 从主要的RSS源（BBC、路透社、美联社、半岛电视台、NPR、卫报、德国之声）获取最新的新闻标题。
metadata: {"openclaw":{"requires":{"bins":["python3"]}}}
---

# 新闻推送技能

该技能可以从主要的国际RSS源获取当前的新闻标题和摘要。无需使用API密钥，也不依赖任何第三方库，仅使用Python的标准库和HTTP协议。

## 可用命令

### 命令：news
**功能：** 从所有配置的RSS源（或指定来源）获取最新的新闻标题。
**执行方式：**
```bash
python3 scripts/news.py
```

### 命令：news from a specific source
**功能：** 仅从指定的来源获取新闻标题。
**执行方式：**
```bash
python3 scripts/news.py --source bbc
python3 scripts/news.py --source reuters
python3 scripts/news.py --source ap
python3 scripts/news.py --source guardian
python3 scripts/news.py --source aljazeera
python3 scripts/news.py --source npr
python3 scripts/news.py --source dw
```

### 命令：news by topic
**功能：** 根据特定主题或关键词筛选新闻标题。
**执行方式：**
```bash
python3 scripts/news.py --topic "climate"
python3 scripts/news.py --source bbc --topic "ukraine"
```

### 命令：news with more items
**功能：** 控制每个RSS源显示的新闻数量（默认为8条）。
**执行方式：**
```bash
python3 scripts/news.py --limit 20
```

### 命令：list sources
**功能：** 显示所有可用的RSS源及其分类。
**执行方式：**
```bash
python3 scripts/news.py --list-sources
```

## 可用来源

| 来源            | 分类                                      |
|-----------------|------------------------------------------------|
| bbc             | 时事、世界、商业、科技、科学、健康                   |
| reuters        | 时事、世界、商业、科技、科学、健康                   |
| ap              | 时事                                         |
| guardian        | 时事、世界、商业、科技、科学                         |
| aljazeera       | 时事                                         |
| npr             | 时事                                         |
| dw              | 时事                                         |

## 使用场景

- 用户想要获取最新新闻、时事动态或新闻标题
- 用户需要每日新闻简报或摘要
- 用户询问“世界上正在发生什么”
- 用户想了解特定主题的新闻
- 用户请求早晨新闻简报

## 输出格式

返回Markdown格式的内容，包含新闻标题、简短描述、发布时间以及链接，并按来源进行分组显示。