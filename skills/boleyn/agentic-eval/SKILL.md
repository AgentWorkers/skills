---
name: agentic-eval
description: >
  用于评估和优化 AI 代理输出的模式与技术。在以下情况下可运用这些技能：
  - 实现自我评估与反思机制
  - 构建用于质量控制的评估-优化流程
  - 创建基于测试的代码优化工作流程
  - 设计基于评分标准或使用大型语言模型（LLM）作为评估工具的系统
  - 对代理的输出（代码、报告、分析结果）进行迭代改进
  - 测量并提升代理的响应质量
---
# 能力评估模式

通过迭代评估和优化实现自我提升的模式。

## 概述

评估模式使代理能够评估并改进自身的输出，从而超越单次生成的方式，进入迭代优化的循环。

```
Generate → Evaluate → Critique → Refine → Output
    ↑                              │
    └──────────────────────────────┘
```

## 适用场景

- **对质量要求极高的生成任务**：需要高准确性的代码、报告、分析等。
- **具有明确评估标准的工作**：存在明确的成功指标。
- **需要遵循特定标准的内容**：如样式指南、合规性、格式要求等。

---

## 模式 1：基本反思

代理通过自我批评来评估并改进其输出。

```python
def reflect_and_refine(task: str, criteria: list[str], max_iterations: int = 3) -> str:
    """Generate with reflection loop."""
    output = llm(f"Complete this task:\n{task}")
    
    for i in range(max_iterations):
        # Self-critique
        critique = llm(f"""
        Evaluate this output against criteria: {criteria}
        Output: {output}
        Rate each: PASS/FAIL with feedback as JSON.
        """)
        
        critique_data = json.loads(critique)
        all_pass = all(c["status"] == "PASS" for c in critique_data.values())
        if all_pass:
            return output
        
        # Refine based on critique
        failed = {k: v["feedback"] for k, v in critique_data.items() if v["status"] == "FAIL"}
        output = llm(f"Improve to address: {failed}\nOriginal: {output}")
    
    return output
```

**关键提示**：使用结构化的 JSON 格式输出，以便可靠地解析评估结果。

---

## 模式 2：评估器-优化器

将生成和评估过程分离为独立的组件，以明确各自的责任。

```python
class EvaluatorOptimizer:
    def __init__(self, score_threshold: float = 0.8):
        self.score_threshold = score_threshold
    
    def generate(self, task: str) -> str:
        return llm(f"Complete: {task}")
    
    def evaluate(self, output: str, task: str) -> dict:
        return json.loads(llm(f"""
        Evaluate output for task: {task}
        Output: {output}
        Return JSON: {{"overall_score": 0-1, "dimensions": {{"accuracy": ..., "clarity": ...}}}}
        """))
    
    def optimize(self, output: str, feedback: dict) -> str:
        return llm(f"Improve based on feedback: {feedback}\nOutput: {output}")
    
    def run(self, task: str, max_iterations: int = 3) -> str:
        output = self.generate(task)
        for _ in range(max_iterations):
            evaluation = self.evaluate(output, task)
            if evaluation["overall_score"] >= self.score_threshold:
                break
            output = self.optimize(output, evaluation)
        return output
```

---

## 模式 3：针对代码的反思

针对代码生成过程，采用测试驱动的优化循环。

```python
class CodeReflector:
    def reflect_and_fix(self, spec: str, max_iterations: int = 3) -> str:
        code = llm(f"Write Python code for: {spec}")
        tests = llm(f"Generate pytest tests for: {spec}\nCode: {code}")
        
        for _ in range(max_iterations):
            result = run_tests(code, tests)
            if result["success"]:
                return code
            code = llm(f"Fix error: {result['error']}\nCode: {code}")
        return code
```

---

## 评估策略

### 基于结果的评估
评估输出是否达到了预期的效果。

```python
def evaluate_outcome(task: str, output: str, expected: str) -> str:
    return llm(f"Does output achieve expected outcome? Task: {task}, Expected: {expected}, Output: {output}")
```

### 使用大型语言模型（LLM）进行评判
利用大型语言模型来比较和排名输出结果。

```python
def llm_judge(output_a: str, output_b: str, criteria: str) -> str:
    return llm(f"Compare outputs A and B for {criteria}. Which is better and why?")
```

### 基于评分标准的评估
根据加权维度对输出结果进行评分。

```python
RUBRIC = {
    "accuracy": {"weight": 0.4},
    "clarity": {"weight": 0.3},
    "completeness": {"weight": 0.3}
}

def evaluate_with_rubric(output: str, rubric: dict) -> float:
    scores = json.loads(llm(f"Rate 1-5 for each dimension: {list(rubric.keys())}\nOutput: {output}"))
    return sum(scores[d] * rubric[d]["weight"] for d in rubric) / 5
```

---

## 最佳实践

| 实践 | 原因 |
|----------|-----------|
| **明确的标准** | 事先定义具体、可衡量的评估标准。 |
| **迭代次数限制** | 设置最大迭代次数（3-5 次），以防止无限循环。 |
| **收敛性检查** | 如果输出分数在迭代过程中没有提升，则停止迭代。 |
| **记录历史数据** | 保留完整的迭代过程，以便调试和分析。 |
| **结构化的输出** | 使用 JSON 格式输出评估结果，确保数据可被可靠地解析。 |

---

## 快速上手检查清单

```markdown
## Evaluation Implementation Checklist

### Setup
- [ ] Define evaluation criteria/rubric
- [ ] Set score threshold for "good enough"
- [ ] Configure max iterations (default: 3)

### Implementation
- [ ] Implement generate() function
- [ ] Implement evaluate() function with structured output
- [ ] Implement optimize() function
- [ ] Wire up the refinement loop

### Safety
- [ ] Add convergence detection
- [ ] Log all iterations for debugging
- [ ] Handle evaluation parse failures gracefully
```