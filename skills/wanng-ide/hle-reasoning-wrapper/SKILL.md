---
name: hle-reasoning-wrapper
description: 将HLE基准测试相关的问题封装在一个结构化的“思维链”（Chain-of-Thought, CoT）推理过程中。在回答HLE问题时使用这种方法，以确保逻辑的严谨性和格式的一致性。
---
# HLE 推理框架（HLE Reasoning Framework）

该框架用于规范人类最后考试（HLE）问题的推理过程。

## 使用方法

```javascript
const hle = require('./index');
const prompt = hle.formatPrompt("What is the speed of light?");
// Use prompt with LLM
const result = hle.validateOutput(llmResponse);
```

## 工作原理

1. **格式化问题提示**：为问题添加所需的结构（包括“思考过程”和“答案”两部分）。
2. **验证输出结果**：确保模型按照规定的结构生成了答案。