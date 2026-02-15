---
name: volcengine-ai-text-ark-chat
description: 在 Volcengine ARK 中，提供了文本生成和聊天辅助功能。当用户需要撰写长篇文本、进行内容总结、信息提取、文本重写、问答交互，或优化聊天提示时，可以利用 ARK 的文本模型来获得帮助。
---

# volcengine-ai-text-ark-chat

在 Volcengine ARK 上执行文本聊天（text/chat）任务，使用稳定的默认参数和可复制的请求模板。

## 执行检查清单

1. 验证 `ARK_API_KEY`、端点 ID 和区域。
2. 明确任务类型（聊天、摘要、重写、提取）。
3. 设置安全的默认值（`temperature`、`max_tokens`、`top_p`）。
4. 返回输出结果以及所使用的关键参数。

## 最小请求模板

```bash
curl https://ark.cn-beijing.volces.com/api/v3/chat/completions \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ep-xxxx",
    "messages": [{"role":"user","content":"请总结这段文本"}],
    "temperature": 0.2
  }'
```

## 参考资料

- `references/sources.md`