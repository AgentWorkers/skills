---
name: aeo-prompt-question-finder
description: 查找与任何主题相关的问题型谷歌自动完成建议。在主题词前添加问题修饰词（如“什么”、“如何”、“为什么”等），然后返回实际的自动完成建议。这些建议对于AEO提示研究、内容构思以及了解人们对该主题的兴趣非常有用。当用户想要发现人们搜索的问题、寻找内容角度，或针对某个主题进行关键词/提示研究时，可以使用此功能。
---
# 问题提示查找器

通过使用特定的问题修饰符查询 Google 自动完成功能，可以发现人们对某个主题会提出哪些问题。

## 使用方法

从 `skill` 目录中运行该脚本：

```bash
python3 scripts/find_questions.py "travel itinerary"
```

### 参数选项

- `--modifiers what how why should` — 覆盖默认的修饰符（默认值：what, how, why, should, can, does, is, when, where, which, will, are, do）
- `--delay 0.5` — 请求之间的延迟时间（批量处理多个主题时，建议使用 0.5–1.0 秒）
- `--json` — 以 JSON 格式输出结果，便于程序化使用
- `--volume` — 通过 DataForSEO 获取该主题的平均每月搜索量（从 macOS Keychain 中读取凭据：`dataforseo-login` / `dataforseo-password`，或环境变量 `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD`）
- `--location 2840` — DataForSEO 的地理位置代码（默认值：2840 = 美国）
- `--lang en` — 用于查询搜索量的语言代码（默认值：en）

### 使用示例

```bash
# Default modifiers (what, how, why)
python3 scripts/find_questions.py "protein powder"

# Custom modifiers
python3 scripts/find_questions.py "travel itinerary" --modifiers what how why should when

# JSON output
python3 scripts/find_questions.py "travel itinerary" --json
```

## 速率限制

Google 自动完成功能属于非官方接口。单次查询（10 个请求）是安全的。但在批量或并行处理多个主题时，务必使用 `--delay 0.5` 或更长的延迟时间，以避免临时 IP 被封禁。

## 工作原理

对于每个指定的修饰符，脚本会向 `https://suggestqueries.google.com/complete/search` 发送请求，格式为 `"{modifier} {topic}"`，并获取相应的自动完成建议结果。此过程无需使用 API 密钥。