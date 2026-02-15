---
name: xai-search
description: 使用 xAI 的 Grok API 结合代理搜索工具（agent-based search tools），可以实时搜索 X/Twitter 以及整个互联网上的内容。
metadata: {"clawdbot":{"emoji":"🔍"}}
---

# xAI 搜索（Grok API）

使用 xAI 的智能搜索功能实时查询 X/Twitter 和网页内容。该功能基于 Grok 的 `web_search` 和 `x_search` 工具实现。

**文档链接：** https://docs.x.ai/docs/

## 必备条件

- 环境变量 `XAI_API_KEY`
- Python 3 及 xai-sdk：`pip install xai-sdk`

## 快速使用（curl 命令）

### 网页搜索
```bash
curl -s https://api.x.ai/v1/chat/completions \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-3-fast",
    "messages": [{"role": "user", "content": "YOUR QUERY HERE"}],
    "tools": [{"type": "function", "function": {"name": "web_search"}}]
  }' | jq -r '.choices[0].message.content'
```

### X/Twitter 搜索
```bash
curl -s https://api.x.ai/v1/chat/completions \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-3-fast",
    "messages": [{"role": "user", "content": "YOUR QUERY HERE"}],
    "tools": [{"type": "function", "function": {"name": "x_search"}}]
  }' | jq -r '.choices[0].message.content'
```

### 综合搜索（网页 + X/Twitter）
```bash
curl -s https://api.x.ai/v1/chat/completions \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-3-fast",
    "messages": [{"role": "user", "content": "YOUR QUERY HERE"}],
    "tools": [
      {"type": "function", "function": {"name": "web_search"}},
      {"type": "function", "function": {"name": "x_search"}}
    ]
  }' | jq -r '.choices[0].message.content'
```

## 辅助脚本

为方便使用，请运行 `scripts/` 目录下的 `xai-search.py` 脚本：

```bash
# Web search (adjust path to your skill location)
python ~/.clawdbot/skills/xai-search/scripts/xai-search.py web "latest news about AI"

# X/Twitter search  
python ~/.clawdbot/skills/xai-search/scripts/xai-search.py x "what are people saying about Clawdbot"

# Both
python ~/.clawdbot/skills/xai-search/scripts/xai-search.py both "current events today"
```

## 模型

- `grok-3-fast`：快速搜索模型，适用于简单查询
- `grok-4-1-fast`：推理模型，更适合复杂查询

## X/Twitter 搜索过滤器

您可以通过以下方式过滤搜索结果：
- `allowed_xHandles` / `excluded_xHandles`：限制搜索范围至特定账户
- `from_date` / `to_date`：时间范围（ISO8601 格式）
- `enable_image_understanding`：分析帖子中的图片
- `enable_video_understanding`：分析帖子中的视频

## 网页搜索过滤器

- `allowed_domains` / `excluded_domains`：限制搜索范围至特定网站
- `enable_image_understanding`：分析页面中的图片

## 使用建议

- 对于突发新闻：使用 X/Twitter 搜索
- 对于事实性或研究性查询：使用网页搜索
- 对于情感分析或观点提取：使用 X/Twitter 搜索
- 系统会根据需要多次发起搜索请求（智能搜索机制）