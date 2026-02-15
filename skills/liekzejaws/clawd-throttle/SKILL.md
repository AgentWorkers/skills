---
name: clawd-throttle
description: 该系统将大型语言模型（LLM）的请求路由到8个提供商（Anthropic、Google、OpenAI、DeepSeek、xAI、Moonshot、Mistral、Ollama）中成本最低且性能最佳的模型。它能在1毫秒内根据8个维度对请求进行评分，并支持三种路由模式（eco、standard、gigachad）。同时，系统会记录所有路由决策以用于成本追踪。
homepage: https://github.com/liekzejaws/clawd-throttle
metadata: {"clawdbot":{"emoji":"\uD83C\uDFCE\uFE0F","requires":{"bins":["node"],"env":["ANTHROPIC_API_KEY","GOOGLE_AI_API_KEY"],"optionalEnv":["XAI_API_KEY","OPENAI_API_KEY","DEEPSEEK_API_KEY","MOONSHOT_API_KEY","MISTRAL_API_KEY"]},"install":[{"id":"clawd-throttle","kind":"node","script":"scripts/setup.ps1","label":"Setup Clawd Throttle (API keys + routing mode)"}]}}
---

# Clawd Throttle

该工具会将所有大型语言模型（LLM）的请求路由到能够处理这些请求的最便宜的模型，从而避免为简单的请求（如“hello”或“summarize this”）支付高昂的费用。

**支持8个提供商和25个以上的模型**：Anthropic（Claude）、Google（Geminii）、OpenAI（GPT/o-series）、xAI（Grok）、DeepSeek、Moonshot（Kimi）、Mistral以及Ollama（本地模型）。

## 工作原理

1. 当您输入提示语时，系统会从8个维度（词汇数量、代码存在情况、推理标记、简洁性指标、多步骤逻辑、问题数量、系统提示的复杂性、对话深度）对提示语进行评分，整个评分过程耗时不到1毫秒。
2. 根据您的活跃模式和配置的提供商，路由器会将提示语的难度等级（简单/标准/复杂）映射到相应的模型。
3. 系统会通过代理将请求发送到正确的API接口。
4. 路由决策和费用信息会被记录到一个本地的JSONL文件中。

## 路由模式

| 模式 | 简单 | 标准 | 复杂 |
|------|--------|----------|---------|
| **eco** | Grok 4.1 Fast | Gemini Flash | Haiku |
| **standard** | Grok 4.1 Fast | Haiku | Sonnet |
| **gigachad** | Haiku | Sonnet | Opus 4.6 |

每个模式都指定了首选模型；如果首选模型不可用，系统会尝试使用列表中的下一个可用模型。

## 可用命令

| 命令 | 功能 |
|---------|-------------|
| `route_request` | 向最便宜且能够处理请求的模型发送提示语并获取响应 |
| `classify.prompt` | 分析提示语的复杂性（无需调用LLM） |
| `get_routing_stats` | 查看费用节省情况和模型使用分布 |
| `get_config` | 查看当前配置（部分信息会被隐藏） |
| `set_mode` | 在运行时更改路由模式 |
| `get_recent_routing_log` | 查看最近的路由决策记录 |

## 特殊规则

- 心跳请求和摘要请求始终会被路由到最便宜的模型。
- 输入 `/opus`、`/sonnet`、`/haiku`、`/flash` 或 `/grok-fast` 可以强制使用特定的模型。
- 子代理的请求会自动降一级到更简单的模型。

## 设置步骤

1. 获取至少一个API密钥（Anthropic和Google需要API密钥；其他提供商可选）：
   - Anthropic: https://console.anthropic.com/settings/keys
   - Google AI: https://aistudio.google.com/app/apikey
   - xAI: https://console.x.ai
   - OpenAI: https://platform.openai.com/api-keys
   - DeepSeek: https://platform.deepseek.com
   - Moonshot: https://platform.moonshot.cn
   - Mistral: https://console.mistral.ai
2. 运行设置脚本：
   ```
   npm run setup
   ```
3. 选择您的路由模式（eco/standard/gigachad）。

## 隐私政策

- 提示语内容不会被存储，仅会记录其SHA-256哈希值。
- 所有数据都保存在本地目录 `~/.config/clawd-throttle/` 中。
- API密钥存储在您的本地配置文件中。