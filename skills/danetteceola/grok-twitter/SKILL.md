---
name: grok-twitter
description: 使用 Grok AI 查询并汇总 Twitter/X 的相关信息。当用户询问 Twitter 的热门趋势、推文、X 平台的内容，或需要 Twitter 相关信息的汇总时，可以使用此功能。
---
# 使用 Grok AI 查询和汇总 Twitter/X 的信息

## 设置

配置所需的环境变量：

```bash
export GROK_API_KEY="your-api-key-here"
export GROK_API_URL="https://api.cheaprouter.club/v1/chat/completions"  # optional
export GROK_MODEL="grok-4.20-beta"  # optional
```

## 使用方法

使用与 Twitter 相关的命令来运行查询脚本：

```bash
python3 scripts/query_grok.py "Summarize recent tweets about [topic]"
```

## 示例

```bash
# Get trending topics
python3 scripts/query_grok.py "What are the top trending topics on Twitter right now?"

# Summarize tweets about a topic
python3 scripts/query_grok.py "Summarize recent tweets about AI developments"

# Get information about a specific user
python3 scripts/query_grok.py "What has @elonmusk been tweeting about recently?"
```

## 注意事项

- Grok 可实时访问 Twitter/X 的数据
- 非常适合获取当前事件和热门信息
- 查询结果由 Grok AI 模型生成