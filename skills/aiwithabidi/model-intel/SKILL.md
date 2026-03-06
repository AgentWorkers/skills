---
name: model-intel
description: Live LLM model intelligence from OpenRouter. Compare pricing, search models by name, find the best model for any task — code, reasoning, creative, fast, cheap, vision, long-context. Real-time data from 200+ models. Use when choosing models, comparing costs, or auditing your AI stack.
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+, OpenRouter API key
metadata: {"openclaw": {"emoji": "\ud83d\udcca", "requires": {"env": ["OPENROUTER_API_KEY"]}, "primaryEnv": "OPENROUTER_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---

# Model Intel 🧠💰

这是一个实时大语言模型（LLM），其智能表现、定价信息及与其他模型的对比数据均来自 OpenRouter。

## 使用场景

- 为特定任务（如编程、推理、创造性任务等）寻找最适合的模型；
- 比较不同模型的定价和功能；
- 查看当前可用的模型及其支持的上下文长度；
- 回答“哪个模型价格最低且能完成某项任务？”

## 使用方法

```bash
# List top models by provider
python3 {baseDir}/scripts/model_intel.py list

# Search by name
python3 {baseDir}/scripts/model_intel.py search "claude"

# Side-by-side comparison
python3 {baseDir}/scripts/model_intel.py compare "claude-opus" "gpt-4o"

# Best model for a use case
python3 {baseDir}/scripts/model_intel.py best fast
python3 {baseDir}/scripts/model_intel.py best code
python3 {baseDir}/scripts/model_intel.py best reasoning
python3 {baseDir}/scripts/model_intel.py best cheap
python3 {baseDir}/scripts/model_intel.py best vision

# Pricing details
python3 {baseDir}/scripts/model_intel.py price "gemini-flash"
```

## 适用场景示例

| 命令          | 适用场景                |
|---------------|----------------------|
| `best fast`      | 需要最低延迟的场景           |
| `best cheap`      | 预算有限的用户             |
| `best code`      | 编程相关任务             |
| `best reasoning` | 复杂逻辑/数学计算需求         |
| `best vision`      | 图像理解相关任务           |
| `best long-context` | 处理长篇文档的场景           |

## 开发者信息

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发  
[YouTube 频道](https://youtube.com/@aiwithabidi) | [GitHub 仓库](https://github.com/aiwithabidi)  
该模型是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)