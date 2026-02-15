---
name: conversation-summary
description: 生成支持增量更新的对话内容摘要。
emoji: 📝
author: lyue82665-droid
version: 1.0.0
license: MIT
requires:
  bins:
    - python3
  pip:
    - requests
tools:
  - name: summarize_conversation
    description: Generate a summary for conversation content.
    parameters:
      type: object
      properties:
        chat_list:
          type: string
          description: "JSON formatted conversation list, e.g., [{\"role\":\"user\",\"content\":\"hello\"}]"
        history_summary:
          type: string
          description: "Previous summary for incremental update (optional)"
      required: [chat_list]
---

# 会话摘要 - 代理指令

使用此技能来生成会话内容的摘要。

## 使用方法

当用户请求以下内容时：
- “总结这次会话”
- “生成一个摘要”
- “我们讨论了什么”

请使用 `summarize_conversation` 工具来调用摘要 API。

## 调用方法

```bash
python3 scripts/conversation_summary.py '<chat_list_json>' '<history_summary>'
```

### 参数

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| chat_list | 字符串 | 是 | 以 JSON 格式表示的会话内容 |
| history_summary | 字符串 | 否 | 用于增量更新的先前摘要 |

### chat_list 格式示例

```json
[
  {"role": "user", "content": "How is the weather today?"},
  {"role": "assistant", "content": "It is sunny, 25 degrees."}
]
```

## 响应

脚本将返回包含以下内容的 JSON 数据：
- `status`: “completed” 或 “error”
- `summary`: 生成的会话摘要
- `error`: 如果失败，则返回错误信息

## 错误处理

- 如果 API 返回非零代码，请向用户报告错误信息
- 如果请求失败，请检查网络连接
- 在调用之前确保 `chat_list` 是有效的 JSON 格式