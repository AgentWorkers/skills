---
name: model-intel
version: 1.0.0
description: OpenRouter 提供了实时大语言模型（LLM）的定价信息与功能。用户可以查看各类模型列表，通过名称进行搜索，对比不同模型的性能，从而为特定应用场景选择最合适的模型，并查看其详细定价信息。所有数据均实时更新，可通过 OpenRouter 的 API 获取。相关功能包括：模型定价查询、模型性能对比、寻找最经济实惠的模型、模型成本统计、LLM 模型之间的详细对比，以及查看当前可用的所有模型。
license: MIT
compatibility:
  openclaw: ">=0.10"
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      env: ["OPENROUTER_API_KEY"]
---
# Model Intel 🧠💰

这是一个实时大型语言模型（LLM）模型，提供智能服务——包括定价、功能介绍以及与其他模型的对比信息，均由 OpenRouter 提供。

## 使用场景

- 为特定任务（如编码、推理、创造性任务、高效率需求或低成本需求）寻找最适合的模型；
- 比较不同模型的定价和功能；
- 查看当前可用的模型及其支持的上下文长度；
- 回答“哪个模型能够以最低的成本完成某项任务？”

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

## 适用场景

| 命令            | 适用场景                          |
|-----------------|--------------------------------------|
| `best fast`       | 需要最低延迟的场景                      |
| `best cheap`       | 预算有限的情况                        |
| `best code`       | 用于编程任务的模型                      |
| `best reasoning`    | 复杂逻辑或数学运算的场景                   |
| `best vision`      | 图像理解相关的任务                      |
| `best long-context`   | 处理长篇文档的场景                     |

## 开发者信息

该模型由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 共同开发。  
更多相关信息可访问 [YouTube](https://youtube.com/@aiwithabidi) 和 [GitHub](https://github.com/aiwithabidi)。  
该模型是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)