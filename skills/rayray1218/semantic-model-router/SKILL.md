---
name: semantic-model-router
description: **Smart LLM Router** — 将每个查询路由到成本最低且性能最佳的模型。支持来自 Anthropic、OpenAI、Google、DeepSeek 和 xAI（Grok）的 17 个模型。采用预训练的机器学习分类器进行路由决策，无需额外获取 API 密钥。
version: 1.0.2
author: Ray
tags: [llm-ops, routing, cost-saving, openclaw, semantic-router, multi-model]
homepage: https://github.com/rayray1218/ClawSkill-Semantic-Router
files: ["scripts/model_router.py", "scripts/model_weights.py", "scripts/requirements.txt"]
dependencies:
  - sentence-transformers>=2.2.2
  - numpy>=1.24.0
---
# 语义模型路由器（Semantic Model Router）

这款智能大型语言模型（LLM）路由器能够通过将每个请求路由到最适合处理该请求的模型，从而将推理成本降低高达 **99%**。它基于预训练的机器学习分类器和语义嵌入技术运行，无需任何外部调用或API密钥。

## 安装

```bash
openclaw plugins install @rayray1218/semantic-model-router
```

## 快速入门

```python
from scripts.model_router import ModelRouter

router = ModelRouter()
res = router.route("Design a distributed caching layer for a fintech platform.")
print(res["report"])
# [ClawRouter] anthropic/claude-sonnet-4-6 (ELITE, ml, conf=0.97)
#              Cost: $3.0/M | Baseline: $10.0/M | Saved: 70.0%
```

## 路由原理

查询通过 **三阶段流程** 被分类到不同的模型层级：

1. **机器学习分类器**（主要阶段）：使用超过6,000个标注过的查询数据进行训练的逻辑回归模型。从 `model_weights.py` 文件中的嵌入权重加载后，响应时间小于1毫秒。
2. **语义嵌入**（备用方案）：通过 `sentence-transformers` 计算查询与目标模型意图向量之间的余弦相似度。
3. **关键词规则**（最后手段）：基于模式匹配进行判断，无需依赖任何外部资源。

| 模型层级 | 默认模型 | 常见任务类型 | 单次请求成本（美元） | 相比基准方案节省的成本百分比 |
|---|---|---|---|---|
| **基础级（BASIC）** | `deepseek/deepseek-chat` | 问候语、简单问答、闲聊 | 0.14美元 | **节省99%** |
| **平衡级（BALANCED）** | `openai/gpt-4o-mini` | 摘要生成、翻译、解释 | 0.15美元 | **节省99%** |
| **高级级（ELITE）** | `anthropic/claude-sonnet-4-6` | 复杂编程、架构分析、安全相关任务 | 3.00美元 | **节省70%** |

## 支持的模型（共17种，2026年2月验证）

### Anthropic
| 模型 | 单次请求输入成本（美元） | 单次请求输出成本（美元） |
|---|---|---|
| `anthropic/claude-sonnet-4-6` | 3.00 | 15.00 | ★ 高级级默认模型 |
| `anthropic/claude-opus-4-5` | 5.00 | 25.00 |
| `anthropic/claude-haiku-4-5` | 0.80 | 4.00 |

### OpenAI
| 模型 | 单次请求输入成本（美元） | 单次请求输出成本（美元） |
|---|---|---|
| `openai/gpt-5` | 1.25 | 10.00 |
| `openai/gpt-4o` | 2.50 | 10.00 |
| `openai/gpt-4o-mini` | 0.15 | 0.60 | **平衡级默认模型** |
| `openai/o3` | 2.00 | 8.00 |
| `openai/o4-mini` | 1.10 | 4.40 |

### Google
| 模型 | 单次请求输入成本（美元） | 单次请求输出成本（美元） |
|---|---|---|
| `google/gemini-3.0-pro` | 1.25 | 10.00 |
| `google/gemini-2.5-pro` | 1.25 | 10.00 |
| `google/gemini-2.5-flash` | 0.30 | 2.50 |
| `google/gemini-2.5-flash-lite` | 0.10 | 0.40 |

### DeepSeek
| 模型 | 单次请求输入成本（美元） | 单次请求输出成本（美元） |
|---|---|---|
| `deepseek/deepseek-chat`（V3.2） | 0.28 | 0.42 | ★ 基础级默认模型 |
| `deepseek/deepseek-reasoner`（V3.2） | 0.28 | 0.42 |

### xAI（Grok）
| 模型 | 单次请求输入成本（美元） | 单次请求输出成本（美元） |
|---|---|---|
| `xai/grok-3` | 3.00 | 15.00 |
| `xai/grok-3-mini` | 0.30 | 0.50 |

> 价格信息来源于各提供商的官方API文档，2026年2月验证。

## 运行时覆盖默认模型

```python
# Use GPT-5.2 for ELITE, Gemini Flash Lite for BASIC
router = ModelRouter(
    elite_model="openai/gpt-5.2",
    balanced_model="google/gemini-2.5-flash",
    basic_model="google/gemini-2.5-flash-lite",
)
```

## 列出所有可用模型（通过命令行接口）

```bash
python3 scripts/model_router.py --list-models
```

## 命令行接口使用方法

```bash
# Route a single query
python3 scripts/model_router.py "Implement AES encryption from scratch"

# Override ELITE model
python3 scripts/model_router.py --elite openai/gpt-5.2 "Write a compiler"

# Run full smoke-test
python3 scripts/model_router.py
```

## 动态关键词扩展功能

```python
router.add_keywords("ELITE", ["cryptographic proof", "zero-knowledge"])
```

## 示例输出结果

```
Query                                              Predicted  Expected   ✓  Cost Info
────────────────────────────────────────────────────────────────────────────────────
How are you doing today?                           BASIC      BASIC      ✓  $0.14/M  saved 98.6%
Summarize this article in three bullet points.     BALANCED   BALANCED   ✓  $0.15/M  saved 98.5%
Implement a thread-safe LRU cache in Python.       ELITE      ELITE      ✓  $3.0/M   saved 70.0%
```

## 安全性与隐私保护

- **无需任何外部调用**：所有分类操作均在本地完成。
- **无需API密钥**：该路由器本身不依赖任何外部API密钥。
- **模型参数透明化**：所有模型参数都存储在 `scripts/model_weights.py` 文件中，可随时审计。

---
*节省成本，更智能地分配请求处理任务。专为OpenClaw社区设计。*