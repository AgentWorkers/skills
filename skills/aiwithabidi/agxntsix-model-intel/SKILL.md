---
name: Model Intel
version: 1.0.0
description: OpenRouter 提供的实时大语言模型（LLM）智能服务及其定价方案
author: aiwithabidi
---
# Model Intel 🧠

这是一个来自 OpenRouter 的实时大语言模型（LLM）智能服务。您可以比较不同模型的价格，搜索适合各种任务的模型（包括代码生成、推理、创意表达、快速响应、低成本模型、视觉处理以及支持长上下文理解的模型）。这些模型使用的是实时数据，而非过时的训练结果。

## 使用方法

```bash
# List top models by provider
python3 scripts/model_intel.py list

# Search by name
python3 scripts/model_intel.py search "claude"

# Side-by-side comparison
python3 scripts/model_intel.py compare "claude-opus" "gpt-4o"

# Best model for a use case
python3 scripts/model_intel.py best fast
python3 scripts/model_intel.py best code
python3 scripts/model_intel.py best reasoning
python3 scripts/model_intel.py best cheap
python3 scripts/model_intel.py best vision

# Pricing details
python3 scripts/model_intel.py price "gemini-flash"
```

## 系统要求

- 需要设置 `OPENROUTER_API_KEY` 环境变量
- 确保您的系统安装了 Python 3.10 或更高版本
- 需要安装 `requests` 包

## 开发者信息

该服务由 **AgxntSix** 开发，AgxntSix 是由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 创建的人工智能运维工具。更多信息请访问：[agxntsix.ai](https://www.agxntsix.ai)。该服务是 OpenClaw 代理工具套件（**AgxntSix Skill Suite**）的一部分。