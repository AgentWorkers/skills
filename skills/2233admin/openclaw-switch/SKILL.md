---
name: openclaw-switch
description: 在 OpenClaw 中管理多提供者模型切换和回退策略。“OpenClaw Switch” 功能帮助用户设置自动模型故障转移机制（例如：当遇到 429 错误（速率限制）时切换到备用模型），切换主模型，查看当前的回退策略，并配置心跳信号/子代理的路由规则。该功能支持与任何提供者（如 Gemini、OpenAI、Anthropic、NVIDIA、Ollama 等）配合使用。
metadata:
  openclaw:
    bin:
      openclaw-switch: scripts/openclaw-switch.sh
---
# OpenClaw Switch

OpenClaw Switch 是 OpenClaw 的一个缺失的模型管理工具，它用于切换模型、可视化备用模型链，并管理多提供者（multi-provider）的配置。

## 快速入门

```bash
# Show current model, fallback chain, heartbeat & subagent config
bash {baseDir}/scripts/openclaw-switch.sh status

# List all available models across all providers
bash {baseDir}/scripts/openclaw-switch.sh list

# Switch primary model (by number from list)
bash {baseDir}/scripts/openclaw-switch.sh switch 2

# Show fallback chain only
bash {baseDir}/scripts/openclaw-switch.sh fallback
```

## 工作原理

OpenClaw 本身支持 `model.fallbacks` 功能：当主模型返回错误（如 429、500 等）时，系统会自动尝试链中的下一个模型。OpenClaw Switch 帮助用户配置、可视化并切换这些备用模型链。

### 典型配置

在 `openclaw.json` 文件中注册多个提供者，每个提供者都需要配置自己的 API 密钥：

```json
{
  "models": {
    "providers": {
      "provider-a": { "apiKey": "...", "models": [{ "id": "model-1" }] },
      "provider-b": { "apiKey": "...", "models": [{ "id": "model-2" }] }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "provider-a/model-1",
        "fallbacks": ["provider-b/model-2"]
      }
    }
  }
}
```

### 使用场景

- **同一提供者，但使用不同的 API 密钥**（例如：付费的 Gemini 和免费的 Gemini）——将它们作为不同的提供者进行注册。
- **跨提供者故障转移**（例如：从 Gemini 转向 OpenAI，再转向本地的 Ollama）。
- **成本优化**——将心跳请求或子代理请求路由到更便宜或免费的模型。

## 安全性

该工具包含的脚本具有以下安全特性：
- **绝不通过网络传输** API 密钥或配置数据。
- **从不记录** 完整的 API 密钥（仅显示前 8 个字符）。
- **仅使用 `bash` 和 `python3` 的标准库**——**完全不依赖任何外部库**。
- 代码行数少于 150 行——**可在 2 分钟内完成全面审计**。