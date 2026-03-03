---
name: jina-deepsearch
description: 通过 AIHubMix 访问 Jina DeepSearch API — 使用 curl 直接调用 HTTP API。
homepage: https://jina.ai/
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "env": ["AIHUBMIX_API_KEY"], "bins": ["curl"] },
        "install":
          [
            {
              "id": "config",
              "kind": "manual",
              "label": "Configure AIHUBMIX_API_KEY",
              "instructions": "Set AIHUBMIX_API_KEY environment variable. Get your key from https://aihubmix.com",
            },
          ],
      },
  }
---
# Jina DeepSearch

您可以通过 AIHubMix 使用 curl 访问 Jina 的 DeepSearch API。

## 快速入门

```bash
# Set your API key first
export AIHUBMIX_API_KEY="sk-..."

# Call the API directly with curl
curl https://aihubmix.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AIHUBMIX_API_KEY" \
  -d '{
    "model": "jina-deepsearch-v1",
    "messages": [{"role": "user", "content": "Your search query"}]
  }'
```

## 配置

设置 `AIHUBMIX_API_KEY` 环境变量。您可以从 https://aihubmix.com 获取您的 API 密钥。

## 模型

- `jina-deepsearch-v1` - Jina 的深度搜索模型