---
name: senior-prompt-engineer
description: 此技能适用于以下场景：用户请求“优化提示语”、“设计提示模板”、“评估大型语言模型（LLM）的输出”、“构建智能代理系统”、“实现基于检索的生成（RAG）技术”、“创建少量样本数据”、“分析令牌使用情况”或“设计人工智能工作流程”。该技能可用于提示工程模式、LLM评估框架、智能代理架构以及结构化输出的设计。
---

# 高级提示工程师

提示工程模式、大型语言模型（LLM）评估框架以及代理系统设计。

## 目录

- [快速入门](#quick-start)
- [工具概述](#tools-overview)
  - [提示优化器](#1-prompt-optimizer)
  - [RAG 评估器](#2-rag-evaluator)
  - [代理编排器](#3-agent-orchestrator)
- [提示工程工作流程](#prompt-engineering-workflows)
  - [提示优化工作流程](#prompt-optimization-workflow)
  - [少量样本示例设计](#few-shot-example-design-workflow)
  - [结构化输出设计](#structured-output-design-workflow)
- [参考文档](#reference-documentation)
- [常见模式快速参考](#common-patterns-quick-reference)

---

## 快速入门

```bash
# Analyze and optimize a prompt file
python scripts/prompt_optimizer.py prompts/my_prompt.txt --analyze

# Evaluate RAG retrieval quality
python scripts/rag_evaluator.py --contexts contexts.json --questions questions.json

# Visualize agent workflow from definition
python scripts/agent_orchestrator.py agent_config.yaml --visualize
```

---

## 工具概述

### 1. 提示优化器

分析提示文本的效率、清晰度和结构，并生成优化后的版本。

**输入：** 提示文本文件或字符串
**输出：** 包含优化建议的分析报告

**使用方法：**
```bash
# Analyze a prompt file
python scripts/prompt_optimizer.py prompt.txt --analyze

# Output:
# Token count: 847
# Estimated cost: $0.0025 (GPT-4)
# Clarity score: 72/100
# Issues found:
#   - Ambiguous instruction at line 3
#   - Missing output format specification
#   - Redundant context (lines 12-15 repeat lines 5-8)
# Suggestions:
#   1. Add explicit output format: "Respond in JSON with keys: ..."
#   2. Remove redundant context to save 89 tokens
#   3. Clarify "analyze" -> "list the top 3 issues with severity ratings"

# Generate optimized version
python scripts/prompt_optimizer.py prompt.txt --optimize --output optimized.txt

# Count tokens for cost estimation
python scripts/prompt_optimizer.py prompt.txt --tokens --model gpt-4

# Extract and manage few-shot examples
python scripts/prompt_optimizer.py prompt.txt --extract-examples --output examples.json
```

---

### 2. RAG 评估器

通过测量上下文相关性和答案的准确性来评估检索增强生成（Retrieval-Augmented Generation）的质量。

**输入：** 检索到的上下文（JSON格式）以及问题/答案
**输出：** 评估指标和质量报告

**使用方法：**
```bash
# Evaluate retrieval quality
python scripts/rag_evaluator.py --contexts retrieved.json --questions eval_set.json

# Output:
# === RAG Evaluation Report ===
# Questions evaluated: 50
#
# Retrieval Metrics:
#   Context Relevance: 0.78 (target: >0.80)
#   Retrieval Precision@5: 0.72
#   Coverage: 0.85
#
# Generation Metrics:
#   Answer Faithfulness: 0.91
#   Groundedness: 0.88
#
# Issues Found:
#   - 8 questions had no relevant context in top-5
#   - 3 answers contained information not in context
#
# Recommendations:
#   1. Improve chunking strategy for technical documents
#   2. Add metadata filtering for date-sensitive queries

# Evaluate with custom metrics
python scripts/rag_evaluator.py --contexts retrieved.json --questions eval_set.json \
    --metrics relevance,faithfulness,coverage

# Export detailed results
python scripts/rag_evaluator.py --contexts retrieved.json --questions eval_set.json \
    --output report.json --verbose
```

---

### 3. 代理编排器

解析代理定义并可视化执行流程，验证工具配置。

**输入：** 代理配置文件（YAML/JSON格式）
**输出：** 工作流程可视化结果和验证报告

**使用方法：**
```bash
# Validate agent configuration
python scripts/agent_orchestrator.py agent.yaml --validate

# Output:
# === Agent Validation Report ===
# Agent: research_assistant
# Pattern: ReAct
#
# Tools (4 registered):
#   [OK] web_search - API key configured
#   [OK] calculator - No config needed
#   [WARN] file_reader - Missing allowed_paths
#   [OK] summarizer - Prompt template valid
#
# Flow Analysis:
#   Max depth: 5 iterations
#   Estimated tokens/run: 2,400-4,800
#   Potential infinite loop: No
#
# Recommendations:
#   1. Add allowed_paths to file_reader for security
#   2. Consider adding early exit condition for simple queries

# Visualize agent workflow (ASCII)
python scripts/agent_orchestrator.py agent.yaml --visualize

# Output:
# ┌─────────────────────────────────────────┐
# │            research_assistant           │
# │              (ReAct Pattern)            │
# └─────────────────┬───────────────────────┘
#                   │
#          ┌────────▼────────┐
#          │   User Query    │
#          └────────┬────────┘
#                   │
#          ┌────────▼────────┐
#          │     Think       │◄──────┐
#          └────────┬────────┘       │
#                   │                │
#          ┌────────▼────────┐       │
#          │   Select Tool   │       │
#          └────────┬────────┘       │
#                   │                │
#     ┌─────────────┼─────────────┐  │
#     ▼             ▼             ▼  │
# [web_search] [calculator] [file_reader]
#     │             │             │  │
#     └─────────────┼─────────────┘  │
#                   │                │
#          ┌────────▼────────┐       │
#          │    Observe      │───────┘
#          └────────┬────────┘
#                   │
#          ┌────────▼────────┐
#          │  Final Answer   │
#          └─────────────────┘

# Export workflow as Mermaid diagram
python scripts/agent_orchestrator.py agent.yaml --visualize --format mermaid
```

---

## 提示工程工作流程

### 提示优化工作流程

用于提升现有提示的性能或降低生成所需的令牌数量。

**步骤 1：确定当前提示的基准**
```bash
python scripts/prompt_optimizer.py current_prompt.txt --analyze --output baseline.json
```

**步骤 2：识别问题**
查看分析报告，找出以下问题：
- 令牌浪费（冗余指令、冗长的示例）
- 模糊的指令（输出格式不明确、动词使用不当）
- 缺失的约束条件（没有长度限制、没有格式规范）

**步骤 3：应用优化模式**
| 问题 | 应用的模式 |
|-------|------------------|
| 输出格式不明确 | 添加明确的格式规范 |
| 冗长内容 | 提取为少量样本示例 |
| 结果不一致 | 添加角色/人物设定 |
| 缺少边缘情况 | 设置约束条件 |

**步骤 4：生成优化后的版本**
```bash
python scripts/prompt_optimizer.py current_prompt.txt --optimize --output optimized.txt
```

**步骤 5：比较结果**
```bash
python scripts/prompt_optimizer.py optimized.txt --analyze --compare baseline.json
# Shows: token reduction, clarity improvement, issues resolved
```

**步骤 6：用测试用例进行验证**
将两个版本的提示应用于测试集，并比较输出结果。

---

### 少量样本示例设计工作流程

用于为上下文学习创建示例。

**步骤 1：明确任务要求**
```
Task: Extract product entities from customer reviews
Input: Review text
Output: JSON with {product_name, sentiment, features_mentioned}
```

**步骤 2：选择多样化的示例（建议选择 3-5 个）**
| 示例类型 | 目的 |
|--------------|---------|
| 简单案例 | 展示基本模式 |
| 边缘案例 | 处理模糊性 |
| 复杂案例 | 多个实体 |
| 负面案例 | 明确指出不应提取的内容 |

**步骤 3：保持格式一致性**
```
Example 1:
Input: "Love my new iPhone 15, the camera is amazing!"
Output: {"product_name": "iPhone 15", "sentiment": "positive", "features_mentioned": ["camera"]}

Example 2:
Input: "The laptop was okay but battery life is terrible."
Output: {"product_name": "laptop", "sentiment": "mixed", "features_mentioned": ["battery life"]}
```

**步骤 4：验证示例质量**
```bash
python scripts/prompt_optimizer.py prompt_with_examples.txt --validate-examples
# Checks: consistency, coverage, format alignment
```

**步骤 5：用保留的案例进行测试**
确保模型能够泛化到未提供的示例情况。

---

### 结构化输出设计工作流程

当需要可靠的 JSON/XML 结构化响应时使用。

**步骤 1：定义数据结构**
```json
{
  "type": "object",
  "properties": {
    "summary": {"type": "string", "maxLength": 200},
    "sentiment": {"enum": ["positive", "negative", "neutral"]},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1}
  },
  "required": ["summary", "sentiment"]
}
```

**步骤 2：在提示中包含数据结构信息**
```
Respond with JSON matching this schema:
- summary (string, max 200 chars): Brief summary of the content
- sentiment (enum): One of "positive", "negative", "neutral"
- confidence (number 0-1): Your confidence in the sentiment
```

**步骤 3：强制执行格式规范**
```
IMPORTANT: Respond ONLY with valid JSON. No markdown, no explanation.
Start your response with { and end with }
```

**步骤 4：验证输出结果**
```bash
python scripts/prompt_optimizer.py structured_prompt.txt --validate-schema schema.json
```

---

## 参考文档

| 文件 | 包含内容 | 用户查询时提供链接 |
|------|----------|---------------------------|
| `references/prompt_engineering_patterns.md` | 10 种提示工程模式及输入/输出示例 | “使用哪种模式？”，“少量样本示例”，“思维链”，“角色提示” |
| `references/llm_evaluation_frameworks.md` | 评估指标、评分方法、A/B 测试 | “如何进行评估？”，“如何衡量质量？”，“如何比较不同提示？” |
| `references/agentic_system_design.md` | 代理系统架构（ReAct、Plan-Execute、工具使用） | “构建代理”，“调用工具”，“多代理系统” |

---

## 常见模式快速参考

| 模式 | 使用场景 | 示例 |
|---------|-------------|---------|
| **零样本（Zero-shot）** | 任务简单且定义明确 | “将这封邮件分类为垃圾邮件或非垃圾邮件” |
| **少量样本（Few-shot）** | 任务复杂且需要统一的输出格式 | 在执行任务前提供 3-5 个示例 |
| **思维链（Chain-of-Thought）** | 需要推理、多步骤逻辑 | “请逐步思考...” |
| **角色提示（Role Prompting）** | 需要专家知识或特定视角 | “你是一名税务专家...” |
| **结构化输出（Structured Output）** | 需要可解析的 JSON/XML 格式 | 包含数据结构 + 强制执行格式规范 |

---

## 常用命令

```bash
# Prompt Analysis
python scripts/prompt_optimizer.py prompt.txt --analyze          # Full analysis
python scripts/prompt_optimizer.py prompt.txt --tokens           # Token count only
python scripts/prompt_optimizer.py prompt.txt --optimize         # Generate optimized version

# RAG Evaluation
python scripts/rag_evaluator.py --contexts ctx.json --questions q.json  # Evaluate
python scripts/rag_evaluator.py --contexts ctx.json --compare baseline  # Compare to baseline

# Agent Development
python scripts/agent_orchestrator.py agent.yaml --validate       # Validate config
python scripts/agent_orchestrator.py agent.yaml --visualize      # Show workflow
python scripts/agent_orchestrator.py agent.yaml --estimate-cost  # Token estimation
```