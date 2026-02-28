---
name: zai-usage
version: 1.1.0
description: 监控 Z.AI GLM 编码计划的使用情况与配额限制。跟踪令牌消耗量，查看重置时间，并检查订阅状态。
author: openclaw
license: MIT
keywords:
  - z.ai
  - glm
  - usage
  - quota
  - monitoring
  - tokens
homepage: https://z.ai
repository: https://github.com/openclaw/skills
---
# Z.AI 使用监控

实时跟踪您在 Z.AI 上的 GLM 编码计划使用情况。

## 快速入门

```bash
# Check usage
~/.openclaw/skills/zai-usage/scripts/usage-summary.sh

# Quick status
~/.openclaw/skills/zai-usage/scripts/quick-check.sh
```

## 设置

1. 从 https://z.ai/manage-apikey/subscription 获取您的 JWT 令牌：
   - 打开 DevTools（F12）
   - 转到 “Application” → “Local Storage” → “z-ai-open-platform-token-production”

2. 将令牌保存到 `~/.openclaw/secrets/zai.env` 文件中：
   ```
   ZAI_JWT_TOKEN=eyJhbGci...
   ```

## 显示内容

- **5 小时配额** - 令牌使用情况（会自动重置）
- **月度配额** - 每月的令牌分配量
- **Web 工具** - 搜索/读取功能的调用限制
- **计划级别** - Lite/Pro 订阅状态

## 状态图标

| 图标 | 使用情况 |
|------|-------|
| ✅ | < 50% |
| ⚠️ | 50-80% |
| 🔴 | > 80% |

## 命令

您可以执行以下命令来获取信息：
- “我们的 Z.AI 使用情况如何？”
- “检查剩余的信用额度”
- “我们的信用额度是否快用完了？”

## 所需工具

- `curl` - 用于发送 HTTP 请求
- `jq` - 用于解析 JSON 数据
- `bc` - 用于格式化数字（可选）

## 参考资源

- https://github.com/zereraz/tokensight
- https://www.reddit.com/r/ZaiGLM/comments/1pmb7fj/how_to_check_zai_coding_usage/