---
name: free-scaling
version: 2.1.1
description: "使用 NVIDIA NIM 免费 tier 实现 $0 的测试时间扩展性。该系统能够根据模型能力的评估结果，智能地将问题路由到最适合的免费模型；仅在模型性能存在不确定性时才会升级到更高版本的模型。系统支持 15 个模型、7 个能力类别，并采用数据驱动的决策机制。适用于审计、代码审查、事实核查、合规性检查或任何需要判断的任务。"
---
# NIM集成系统（NIM Ensemble）

$0 使用NVIDIA的NIM免费 tier实现多模型推理。系统提供两种模式：

- **`smart_vote()`** — 智能决策模式：根据任务类型将请求路由到最合适的模型；仅在结果不确定时才会升级到更高层级的模型进行判断。平均每个问题需要调用1.2次API。
- **`vote()`** — 平衡集成模式：同时请求N个模型，并根据多数意见做出决策。这种方式简单直接，但会消耗更多的API调用资源。

## 设置流程

1. 访问[build.nvidia.com](https://build.nvidia.com)并登录（使用免费的NVIDIA账户）。
2. 选择任意一个模型（例如[Llama 3.3 70B](https://build.nvidia.com/meta/llama-3_3-70b-instruct)），然后点击“获取API密钥”（Get API Key）。
3. 一个API密钥即可用于所有NIM模型，无需为每个模型单独进行设置。
4. 将API密钥配置到您的环境中：
   ```bash
   export NVIDIA_API_KEY="nvapi-..."
   ```
5. 该系统不依赖任何第三方库（仅使用Python的标准库，要求Python版本为3.10或更高）。

## 快速入门

```python
from nim_ensemble import scale

# k=3: ask 3 diverse models, majority vote
result = scale("Is eval(input()) safe?", k=3, answer_patterns=["SAFE", "VULNERABLE"])
print(result.answer)      # VULNERABLE
print(result.calls_made)  # 3
print(result.confidence)  # 1.0

# k="auto": smart cascade (starts with 1, escalates on uncertainty)
result = scale("Is this correct?", k="auto", answer_patterns=["YES", "NO"])
```

## 命令行接口（CLI）

```bash
# Scale to k models
python3 -m nim_ensemble.cli scale "Is this code vulnerable?" -k 3 --answers "SAFE,VULNERABLE"
# → VULNERABLE (k=3, conf=100%, 3 calls, 1.2s)

# Single model (fastest)
python3 -m nim_ensemble.cli scale "Is 91 prime?" -k 1 --answers "YES,NO"

# Auto-scale (smart cascade)
python3 -m nim_ensemble.cli scale "Is this safe?" -k auto

# List models and panels
python3 -m nim_ensemble.cli models
python3 -m nim_ensemble.cli panels

# Benchmark all models on a question
python3 -m nim_ensemble.cli bench "Is 91 prime? YES or NO." --speed fast
```

## 智能决策机制的工作原理

```
Question → classify task type (code/compliance/reasoning/factual/nuance)
        → call best expert for that type (1 call)
        → confident? (weight ≥ 85%) → done
        → uncertain? → call arbiter (mistral-large, 100% all categories)
        → still split? → full panel, weighted vote by measured accuracy
```

大多数问题在第一步就能得到解决。那些“产生错误结果”的模型永远不会被调用，因为系统会根据模型的能力分布来避免使用这些模型。

## 模型能力评估

系统不会预先设定模型的能力评分，而是会根据具体任务来评估模型的性能：

```bash
# Profile specific models (3 trials each)
python3 -m nim_ensemble.capability_map --models llama-3.3 gemma-27b mistral-large --trials 3

# Profile all fast models
python3 -m nim_ensemble.capability_map --speed fast --trials 2
```

评估完成后，系统会生成`capability_map.json`文件，其中包含每个模型的准确率、响应时间、优势与劣势以及错误之间的关联信息。该文件会被自动加载，用于后续的智能路由决策。

**如果不进行模型能力评估**，系统会使用默认的配置（例如选择mistral-large模型作为仲裁者，并使用三个不同类型的模型组成评估小组）。通过能力评估，系统能够更好地规避某些模型的局限性。

## 默认的模型组合

不同的模型组合能够最大化系统的架构多样性（不同模型之间的错误可以相互抵消）：

| 组合名称 | 包含的模型 | 适用场景 |
|---------|-----------|---------|
| `general` | mistral-large, llama-3.3, gemma-27b | 通用场景 |
| `fast` | llama-3.3, nemotron-super-49b, gemma-27b | 需要快速响应的场景（响应时间<1.5秒） |
| `max` | 来自5个不同模型的组合 | 高风险决策场景 |
| `arbiter` | mistral-large | 在模型结果相同时的最终裁决者 |

对于特定任务的模型组合，可以通过运行`capability_map`命令来评估模型在您的数据集上的表现。

## Python API接口

```python
from nim_ensemble import scale, smart_vote, vote, call_model

# scale() — the core API, control k
result = scale("Is X safe?", k=3, answer_patterns=["SAFE", "VULNERABLE"])
result = scale("Is X safe?", k="auto")  # smart cascade
result = scale("Is X safe?", k=1)       # single model

# smart_vote() — cascade with task-type routing
result = smart_vote("Is X correct?", answer_patterns=["YES", "NO"])

# vote() — flat ensemble with named panels
result = vote("Is X true?", panel="general", answer_patterns=["YES", "NO"])

# call_model() — single model, raw access
from nim_ensemble import call_model
answer, raw = call_model("Is X true?", "mistral-large")
```

## 使用提示

为了获得最佳的结果，请遵循以下提示：

- 将答案直接写在第一行：“在第一行回答‘是’或‘否’，然后给出解释。”
- 明确提供答案选项：“回答‘安全’、‘不安全’或‘需要进一步审核’。”
- 问题中不仅要包含判断结果，还要提供相关的背景信息和证据。

## 系统架构

```
nim_ensemble/
├── __init__.py       # Public API: smart_vote, vote, call_model
├── cascade.py        # Smart cascade with capability routing
├── voter.py          # Flat ensemble voting engine
├── models.py         # Model registry + data-driven panels
├── parser.py         # Answer extraction (thinking models, word boundaries)
├── cli.py            # CLI interface
├── benchmark.py      # Single-trial model profiling
└── capability_map.py # Multi-trial profiling with error correlation
```

## 系统要求

- 需要设置`NVIDIA_API_KEY`环境变量（可在[build.nvidia.com](https://build.nvidia.com)免费获取）。
- 系统要求使用Python 3.10或更高版本。
- 该系统不依赖任何第三方库，仅使用Python的标准库（通过`urllib`进行API调用）。