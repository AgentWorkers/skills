---
name: prompt-optimizer
description: 使用58种经过验证的提示生成技术来评估、优化和提升提示的质量。当用户要求改进、优化或分析某个提示时；当提示需要更加清晰、具体或结构化时；或者当需要为不同的使用场景生成提示变体时，都可以采用这些技术。内容包括质量评估、有针对性的优化方法，以及基于CoT（Continued Training）、小样本学习（few-shot learning）、角色扮演（role-play）等技术的自动优化方法。
---
# Prompt Optimizer

这是一个基于 Node.js 的工具，实现了 `references/prompt-techniques.md` 文件中列出的 58 种经过验证的提示生成技术。

## 使用方法

### 1. 查看所有可用技术
可以查看全部 58 种技术及其对应的 ID 和描述。
```bash
node skills/prompt-optimizer/index.js list
```

### 2. 获取技术详情
可以查看特定技术的模板及其用途。
```bash
node skills/prompt-optimizer/index.js get <technique_name>
```
示例：`node skills/prompt-optimizer/index.js get "Chain of Thought"`

### 3. 优化提示内容
可以将特定技术的模板应用到你的提示生成逻辑中。
```bash
node skills/prompt-optimizer/index.js optimize "<your_prompt>" --technique "<technique_name>"
```
示例：
```bash
node skills/prompt-optimizer/index.js optimize "Write a python script to reverse a string" --technique "Chain of Thought"
```

## 参考资料
- `references/prompt-techniques.md`：所有提示生成技术的完整目录。
- `references/quality-framework.md`：用于手动评估提示质量的框架。