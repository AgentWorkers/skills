---
name: peer-review
description: |
  Multi-model peer review layer using local LLMs via Ollama to catch errors in cloud model output.
  Fan-out critiques to 2-3 local models, aggregate flags, synthesize consensus.

  Use when: validating trade analyses, reviewing agent output quality, testing local model accuracy,
  checking any high-stakes Claude output before publishing or acting on it.

  Don't use when: simple fact-checking (just search the web), tasks that don't benefit from
  multi-model consensus, time-critical decisions where 60s latency is unacceptable,
  reviewing trivial or low-stakes content.

  Negative examples:
  - "Check if this date is correct" → No. Just web search it.
  - "Review my grocery list" → No. Not worth multi-model inference.
  - "I need this answer in 5 seconds" → No. Peer review adds 30-60s latency.

  Edge cases:
  - Short text (<50 words) → Models may not find meaningful issues. Consider skipping.
  - Highly technical domain → Local models may lack domain knowledge. Weight flags lower.
  - Creative writing → Factual review doesn't apply well. Use only for logical consistency.
version: "1.0"
---

# 同行评审 —— 本地大语言模型（LLM）的批判性检查层

> **假设：** 本地大语言模型能够检测出云服务输出中至少30%的错误，同时误报率低于50%。

---

## 架构

```
Cloud Model (Claude) produces analysis
        │
        ▼
┌────────────────────────┐
│   Peer Review Fan-Out  │
├────────────────────────┤
│  Drift (Mistral 7B)   │──► Critique A
│  Pip (TinyLlama 1.1B) │──► Critique B
│  Lume (Llama 3.1 8B)  │──► Critique C
└────────────────────────┘
        │
        ▼
  Aggregator (consensus logic)
        │
        ▼
  Final: original + flagged issues
```

---

## Swarm机器人的角色

| 机器人 | 模型 | 角色 | 优势 |
|-----|-------|------|-----------|
| **Drift** 🌊 | Mistral 7B | 系统化的分析者 | 能够进行结构化推理，发现逻辑上的漏洞 |
| **Pip** 🐣 | TinyLlama 1.1B | 快速检查工具 | 可快速进行基本验证，延迟低 |
| **Lume** 💡 | Llama 3.1 8B | 深度思考者 | 能够进行细致的分析，发现微妙的问题 |

---

## 脚本

| 脚本 | 用途 |
|--------|---------|
| `scripts/peer-review.sh` | 将单个输入发送给所有模型，并收集它们的评审意见 |
| `scripts/peer-review-batch.sh` | 对样本集执行同行评审 |
| `scripts/seed-test-corpus.sh` | 生成用于测试的错误样本集 |

### 使用方法

```bash
# Single file review
bash scripts/peer-review.sh <input_file> [output_dir]

# Batch review
bash scripts/peer-review-batch.sh <corpus_dir> [results_dir]

# Generate test corpus
bash scripts/seed-test-corpus.sh [count] [output_dir]
```

这些脚本位于 `workspace/scripts/` 目录下，未包含在技能包中以避免重复。

---

## 评审提示模板

```
You are a skeptical reviewer. Analyze the following text for errors.

For each issue found, output JSON:
{"category": "factual|logical|missing|overconfidence|hallucinated_source",
 "quote": "...", "issue": "...", "confidence": 0-100}

If no issues found, output: {"issues": []}

TEXT:
---
{cloud_output}
---
```

---

## 错误类别

| 类别 | 描述 | 例子 |
|----------|-------------|---------|
| **事实错误** | 数字、日期、名称错误 | “比特币于2010年推出” |
| **逻辑错误** | 论述不连贯、结论缺乏依据 | “因为X在上升，所以Y会下降” |
| **信息缺失** | 忽略了重要背景信息 | 忽略了关键的反对意见 |
| **过度自信** | 未经证实就下定论 | “这件事肯定会发生”（即使只有55%的概率） |
| **引用虚假来源** | 引用了不存在的来源 | “根据2024年路透社的报道...” |

---

## Discord工作流程

1. 将分析结果发布到 **#the-deep**（或 #swarm-lab）频道 |
2. Drift、Pip和Lume分别给出各自的评审意见 |
3. Celeste负责整合这些评审意见：去除重复的标记，并根据模型的可信度对它们进行加权 |
4. 如果至少有2个模型达成共识，则该标记被视为高可信度的错误 |
5. 最终结果会附带建议：`发布` | `修订` | `标记为人工审核` |

---

## 成功标准

| 结果 | 真正错误检测率（TPR） | 假正率（FPR） | 决策 |
|---------|-----|-----|----------|
| **通过** | ≥50% | <30% | 作为默认检查层使用 |
| **基本通过** | ≥30% | <50% | 作为可选检查层使用 |
| **效果一般** | 20–30% | 50–70% | 需要优化评审提示并重新测试 |
| **失败** | <20% | >70% | 放弃当前方法 |

### 评分规则
- 如果某个标记确实指出了一个错误（即使解释不够完善），则视为**真正错误**（True Positive） |
- 如果被标记的内容实际上是正确的，则视为**假正误**（False Positive） |
- 不同模型之间重复的标记在计算TPR时只计算一次，但会影响共识指标的统计结果 |

---

## 所需依赖项

- 需要在本地运行Ollama，并加载以下模型：`mistral:7b`、`tinyllama:1.1b`、`llama3.1:8b` |
- 需要安装`jq`和`curl`工具 |
- 结果存储在`experiments/peer-review-results/`目录中 |

---

## 集成方式

当同行评审通过验证后：
- 将该功能打包为Reef API的端点：`POST /review` |
- 在发布任何分析结果之前，代理程序会调用该API进行评审 |
- 可配置参数：模型选择、共识阈值、错误类别等 |
- 所有评审记录会保存在`#reef-logs`日志中，并附带TPR统计信息