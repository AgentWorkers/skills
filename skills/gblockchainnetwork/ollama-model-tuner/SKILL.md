---
summary: "Ollama Model Tuner: Locally fine-tune prompts, LoRAs, and models with Ollama for custom tasks."
description: "Optimize Ollama models/prompts using local datasets, eval metrics, and iterative tuning. No cloud needed."
triggers:
  - "tune ollama"
  - "optimize ollama model"
  - "fine-tune local LLM"
  - "ollama prompt engineer"
read_when:
  - "ollama tune" in message
  - "model fine-tune" in message
---

# Ollama 模型调优器 v1.0.0

## 🎯 主要功能
- 提供提示工程（prompt engineering）和 A/B 测试功能
- 允许用户自定义模型文件（modelfile customization）
- 使用本地数据进行 LoRA（Low-Rank Autoencoder）微调
- 支持性能基准测试（performance benchmarking）

## 🚀 快速入门
```
!ollama-model-tuner --model llama3 --dataset ./data.json --task classification
```

## 相关文件
- `scripts/tune.py`：基于 Python 的调优工具，包含评估循环（eval loop）
- `prompts/system.md`：基础系统提示（system prompts）文件

## 支持的环境与格式
- Ollama 版本：0.3 及以上
- Python 版本：3.10 及以上
- 数据集格式：JSONL 或 CSV

（注：由于文件内容主要为代码和配置信息，翻译时未添加过多的解释性文字。若需要进一步说明某些技术细节或功能，可在此基础上进行补充。）