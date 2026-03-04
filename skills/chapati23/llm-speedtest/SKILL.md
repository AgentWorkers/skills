---
name: llm-speedtest
version: 1.0.0
description: "并行测试主要的 large language model (LLM) 提供商，并比较其实际的 API 延迟。使用 `/ping` 命令来执行测试。"
metadata:
  category: utility
  capabilities:
    - api
  dependencies: []
  interface: shell
openclaw:
  emoji: "⚡"
  requires:
    env:
      - ANTHROPIC_API_KEY (optional)
      - OPENAI_API_KEY (optional)
      - GEMINI_API_KEY (optional)
      - MINIMAX_API_KEY (optional)
      - XAI_API_KEY (optional)
author:
  name: chapati23
---
# LLM速度测试

同时测试主要的LLM（大型语言模型）提供商，并比较它们的实际API延迟（TTFT，即Total Round-Trip Time）。

## 使用场景

- 当用户输入`/ping`命令或询问模型的延迟/速度时
- 比较不同提供商的响应时间
- 检查某个特定提供商是否运行缓慢或出现故障

## 工作原理

脚本`scripts/ping.sh`会执行以下操作：

1. 从`pass shared/`目录中获取API密钥（用户可能需要根据自身环境调整密钥的获取方式）
2. 对每个提供商发送并行`curl`请求，请求内容仅包含简短的提示信息（例如“hi”，`max_tokens=1`）
3. 测量每个提供商的往返总时间
4. 按延迟对结果进行排序，并用颜色标记显示结果

## 输出格式

结果按延迟从快到慢排序，并用颜色标记表示：

- 🟢 **< 2秒** — 非常快
- 🟡 **2–5秒** — 一般
- 🔴 **5–30秒** — 较慢
- ⚫ **超过30秒** — 超时

## 测试的模型

| 提供商 | 模型        |
|----------|-----------|
| Anthropic | Claude Sonnet 4   |
| Anthropic | Claude Opus 4   |
| OpenAI | GPT-4o-mini   |
| Google | Gemini 2.5 Flash |
| MiniMax | MiniMax-M1    |
| xAI | Grok 3 Mini Fast |

## 成本

每次测试的成本约为0.0001美元（每个模型使用1个令牌，属于最便宜的套餐）。

## 注意事项

此工具使用`pass shared/`目录来获取API密钥。如果您未使用`pass`目录，需要自行修改`scripts/ping.sh`脚本，以便从环境变量或其他密钥管理工具中获取密钥。