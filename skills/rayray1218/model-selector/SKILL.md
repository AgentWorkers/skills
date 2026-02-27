---
name: Semantic Model Orchestrator
description: 这是一种强大的模型路由技术，它能够分析用户的查询意图和成本效益，从而在执行之前选择最合适的 large language model（LLM）版本——无论是 Elite、Balanced 还是 Basic 版本。
version: 1.0.0
author: Ray
tags: [llm-ops, routing, efficiency, selection]
---
# 语义模型调度器（Semantic Model Orchestrator）

该技能为AI代理提供了一个智能的中间层，用于决定应由哪个模型层级来处理特定任务。通过语义分析，它将查询分为**高级（Elite）**、**中等（Balanced）**或**基础（Basic）**三个级别。

## 主要特性
- **语义意图识别（Semantic Intent Recognition）**：利用向量嵌入技术来检测查询的复杂性。
- **成本效益调度（Cost-Efficiency Orchestration）**：将查询路由到相应级别的模型（高级、中等或基础模型）。
- **针对ClawHub进行了优化（ClawHub Optimized）**：为Claude 3.5 Sonnet、GPT-4o-mini和DeepSeek提供了默认的模型层级。
- **动态调整机制（Rolling Adjustment）**：内置逻辑可根据用户历史数据优化查询关键词的匹配度。
- **支持多种模型提供商（Multi-Provider Support）**：支持OpenAI、Anthropic、Gemini和DeepSeek等模型。

## 模型层级
- **高级（Elite）**：`anthropic/claude-3-5-sonnet-latest`
- **中等（Balanced）**：`openai/gpt-4o-mini`
- **基础（Basic）**：`deepseek/deepseek-chat`

## 使用方法
将此技能添加到您的代理功能列表中。代理在调用主要的LLM（大型语言模型）之前，会先调用`get_optimal_model`工具来优化性能和资源使用。

### 示例工具调用
```python
result = router.analyze_and_route("Design a high-scalable microservices architecture for a fintech app.")
# Returns: {"tier": "ELITE", "suggested_model": "anthropic/claude-3-5-sonnet-latest"}
```