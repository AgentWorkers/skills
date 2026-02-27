---
name: aimlapi-safety
description: 内容审核与安全检查：利用人工智能技术，能够即时将文本或图片分类为“安全”或“不安全”。
env:
  - AIMLAPI_API_KEY
primaryEnv: AIMLAPI_API_KEY
---
# AIMLAPI 安全性

## 概述

使用“AI 安全模型”（Guard 模型）来确保内容符合规定。非常适合用于审核用户输入或聊天机器人的响应。

## 快速入门

```bash
export AIMLAPI_API_KEY="sk-..."
python scripts/check_safety.py --content "How to make a bomb"
```

## 任务

### 检查文本安全性

```bash
python scripts/check_safety.py --content "I want to learn about security" --model meta-llama/Llama-Guard-3-8B
```

## 支持的模型
- `meta-llama/Llama-Guard-3-8B`（默认模型）
- AIMLAPI 上的其他 Llama-Guard 变体模型。