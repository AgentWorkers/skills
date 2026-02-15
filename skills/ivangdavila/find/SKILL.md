---
name: Find
description: 使用渐进式搜索扩展、多源验证和迭代优化的方式，直到找到目标内容。
---

## 模式（Pattern）

```
Need → Clarify → Search → Validate → [Found? Deliver : Expand]
```

持续搜索，直到找到目标或耗尽所有可能。搜索时先从具体范围开始，逐步扩大搜索范围；在提供结果之前务必进行验证。

## 适用场景

- 用户需要查找特定信息
- 信息的位置或来源未知
- 用户提出类似“帮我找一下...”“我在哪里可以找到...”“我需要找到...”之类的请求

**不适用场景**：用户已经掌握的信息、简单的查询操作、浏览等场景。

## 准备工作（Setup）

在开始搜索之前，需要明确以下内容：

| 需要查找的内容 | 原因 |
|-------------|--------|
| 具体是什么？      | 避免找错对象 |
| 成功的标准     | 如何判断找到的内容是否符合要求？ |
| 限制条件     | 预算、地点、时间、格式等 |
| 是否已经尝试过？    | 避免重复无效的搜索路径 |

如果用户的描述不够明确，先提出一个具体问题以获取更多信息，然后再开始搜索。

## 搜索范围的扩展（Search Expansion）

搜索时先从具体范围开始；如果未找到目标，再逐步扩大搜索范围：

```
1. Obvious sources → Direct lookup, known locations
2. Specialized sources → Domain-specific databases, expert communities  
3. Alternative queries → Different words, related concepts
4. Indirect paths → Who would know? What links to this?
5. Ask human → More context, different angle
```

在每次扩展搜索范围时，尽可能同时尝试多个信息来源。

## 验证结果（Validation）

在提供结果之前，需要验证以下几点：
- 这是否真的是用户需要的内容？
- 信息来源是否可靠？
- 信息是否是最新的、有效的？
- 用户需要了解哪些注意事项？

如果有疑问，一定要如实告知用户，例如：“找到了X，但无法100%确定这是否符合您的需求。”

## 结果呈现（Delivery）

```
FOUND: [what]
WHERE: [source]
CONFIDENCE: [high/medium/low]
CAVEATS: [if any]
```

如果找到了多个结果，应进行总结并让用户自行选择。

## 未找到结果（Not Found）

如果所有搜索路径都已尝试过且仍未找到目标：
1. 报告已经尝试过的所有方法；
2. 提供最接近用户需求的替代方案；
3. 建议用户尝试其他方法或提供更多相关信息。

---

**相关概念**：  
- 如需重复搜索直到满足成功标准，请参考`loop`；  
- 对于多阶段的工作流程，请参考`cycle`。