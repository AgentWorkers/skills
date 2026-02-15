---
name: critpt-solver
description: 用于验证和执行针对 CritPt 基准测试问题的 Python 解决方案。当用户需要检查生成的解决方案或运行测试用例时，可以使用该工具。
---
# CritPt Solver

用于封装针对 CritPt 问题的 Python 执行逻辑。

## 使用方法

```javascript
const solver = require('./index');
const code = "..."; // Python code implementing answer(p)
const result = await solver.runPythonCode(code);
console.log(result);
```

## 工作原理

1. **生成结构化提示**：为大型语言模型（LLM）创建一个结构化的提示，以便其生成 Python 代码。
2. **生成代码**：（可选）调用大型语言模型，或等待大型语言模型自行调用该功能。
3. **验证代码**：检查代码的语法，并在可能的情况下使用测试值来执行 `answer(p)`。