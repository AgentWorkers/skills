---
name: azure-ai-evaluation-py
description: |
  Azure AI Evaluation SDK for Python. Use for evaluating generative AI applications with quality, safety, and custom evaluators.
  Triggers: "azure-ai-evaluation", "evaluators", "GroundednessEvaluator", "evaluate", "AI quality metrics".
package: azure-ai-evaluation
---

# Azure AI Evaluation SDK for Python

使用内置和自定义的评估工具来评估生成式AI应用程序的性能。

## 安装

```bash
pip install azure-ai-evaluation

# With remote evaluation support
pip install azure-ai-evaluation[remote]
```

## 环境变量

```bash
# For AI-assisted evaluators
AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini

# For Foundry project integration
AIPROJECT_CONNECTION_STRING=<your-connection-string>
```

## 内置评估工具

### 质量评估工具（AI辅助型）

```python
from azure.ai.evaluation import (
    GroundednessEvaluator,
    RelevanceEvaluator,
    CoherenceEvaluator,
    FluencyEvaluator,
    SimilarityEvaluator,
    RetrievalEvaluator
)

# Initialize with Azure OpenAI model config
model_config = {
    "azure_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
    "api_key": os.environ["AZURE_OPENAI_API_KEY"],
    "azure_deployment": os.environ["AZURE_OPENAI_DEPLOYMENT"]
}

groundedness = GroundednessEvaluator(model_config)
relevance = RelevanceEvaluator(model_config)
coherence = CoherenceEvaluator(model_config)
```

### 质量评估工具（基于自然语言处理）

```python
from azure.ai.evaluation import (
    F1ScoreEvaluator,
    RougeScoreEvaluator,
    BleuScoreEvaluator,
    GleuScoreEvaluator,
    MeteorScoreEvaluator
)

f1 = F1ScoreEvaluator()
rouge = RougeScoreEvaluator()
bleu = BleuScoreEvaluator()
```

### 安全评估工具

```python
from azure.ai.evaluation import (
    ViolenceEvaluator,
    SexualEvaluator,
    SelfHarmEvaluator,
    HateUnfairnessEvaluator,
    IndirectAttackEvaluator,
    ProtectedMaterialEvaluator
)

violence = ViolenceEvaluator(azure_ai_project=project_scope)
sexual = SexualEvaluator(azure_ai_project=project_scope)
```

## 单行评估

```python
from azure.ai.evaluation import GroundednessEvaluator

groundedness = GroundednessEvaluator(model_config)

result = groundedness(
    query="What is Azure AI?",
    context="Azure AI is Microsoft's AI platform...",
    response="Azure AI provides AI services and tools."
)

print(f"Groundedness score: {result['groundedness']}")
print(f"Reason: {result['groundedness_reason']}")
```

## 使用 `evaluate()` 进行批量评估

```python
from azure.ai.evaluation import evaluate

result = evaluate(
    data="test_data.jsonl",
    evaluators={
        "groundedness": groundedness,
        "relevance": relevance,
        "coherence": coherence
    },
    evaluator_config={
        "default": {
            "column_mapping": {
                "query": "${data.query}",
                "context": "${data.context}",
                "response": "${data.response}"
            }
        }
    }
)

print(result["metrics"])
```

## 综合评估工具

```python
from azure.ai.evaluation import QAEvaluator, ContentSafetyEvaluator

# All quality metrics in one
qa_evaluator = QAEvaluator(model_config)

# All safety metrics in one
safety_evaluator = ContentSafetyEvaluator(azure_ai_project=project_scope)

result = evaluate(
    data="data.jsonl",
    evaluators={
        "qa": qa_evaluator,
        "content_safety": safety_evaluator
    }
)
```

## 评估应用程序目标

```python
from azure.ai.evaluation import evaluate
from my_app import chat_app  # Your application

result = evaluate(
    data="queries.jsonl",
    target=chat_app,  # Callable that takes query, returns response
    evaluators={
        "groundedness": groundedness
    },
    evaluator_config={
        "default": {
            "column_mapping": {
                "query": "${data.query}",
                "context": "${outputs.context}",
                "response": "${outputs.response}"
            }
        }
    }
)
```

## 自定义评估工具

### 基于代码的评估工具

```python
from azure.ai.evaluation import evaluator

@evaluator
def word_count_evaluator(response: str) -> dict:
    return {"word_count": len(response.split())}

# Use in evaluate()
result = evaluate(
    data="data.jsonl",
    evaluators={"word_count": word_count_evaluator}
)
```

### 基于提示的评估工具

```python
from azure.ai.evaluation import PromptChatTarget

class CustomEvaluator:
    def __init__(self, model_config):
        self.model = PromptChatTarget(model_config)
    
    def __call__(self, query: str, response: str) -> dict:
        prompt = f"Rate this response 1-5: Query: {query}, Response: {response}"
        result = self.model.send_prompt(prompt)
        return {"custom_score": int(result)}
```

## 将结果记录到Foundry项目中

```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project = AIProjectClient.from_connection_string(
    conn_str=os.environ["AIPROJECT_CONNECTION_STRING"],
    credential=DefaultAzureCredential()
)

result = evaluate(
    data="data.jsonl",
    evaluators={"groundedness": groundedness},
    azure_ai_project=project.scope  # Logs results to Foundry
)

print(f"View results: {result['studio_url']}")
```

## 评估工具参考

| 评估工具 | 类型 | 指标          |
|-----------|------|--------------|
| `GroundednessEvaluator` | AI   | 信息真实性（1-5分）   |
| `RelevanceEvaluator` | AI   | 相关性（1-5分）     |
| `CoherenceEvaluator` | AI   | 逻辑连贯性（1-5分）   |
| `FluencyEvaluator` | AI   | 表达流畅性（1-5分）   |
| `SimilarityEvaluator` | AI   | 相似度（1-5分）     |
| `RetrievalEvaluator` | AI   | 文本检索能力（1-5分）   |
| `F1ScoreEvaluator` | NLP   | F1分数（0-1）      |
| `RougeScoreEvaluator` | NLP   | Rouge分数       |
| `ViolenceEvaluator` | 安全性 | 暴力内容（0-7分）    |
| `SexualEvaluator` | 安全性 | 性相关内容（0-7分）    |
| `SelfHarmEvaluator` | 安全性 | 自伤行为（0-7分）    |
| `HateUnfairnessEvaluator` | 安全性 | 恶意与不公平内容（0-7分） |
| `QAEvaluator` | 综合型 | 所有质量指标     |
| `ContentSafetyEvaluator` | 综合型 | 所有安全性指标     |

## 最佳实践

1. **使用综合评估工具** 进行全面评估。
2. **正确映射数据列** — 数据列不匹配会导致评估失败。
3. **将结果记录到Foundry项目中**，以便跟踪和比较不同运行结果。
4. **为特定领域创建自定义评估工具**。
5. **在有真实答案的情况下使用基于自然语言处理的评估工具**。
6. **使用安全性评估工具** 需要Azure AI项目的权限。
7. **批量评估** 比单行评估更高效。

## 参考文件

| 文件 | 内容          |
|------|--------------|
| [references/built-in-evaluators.md](references/built-in-evaluators.md) | AI辅助型、基于自然语言处理和安全性评估工具的详细说明及配置表 |
| [references/custom-evaluators.md](references/custom-evaluators.md) | 如何创建基于代码和提示的自定义评估工具及测试方法 |
| [scripts/run_batch_evaluation.py](scripts/run_batch_evaluation.py) | 用于运行批量评估的CLI工具（包括质量、安全性和自定义评估） |