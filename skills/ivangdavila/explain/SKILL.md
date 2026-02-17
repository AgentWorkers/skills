---
name: "Explain"
version: "1.0.2"
description: "学习如何向人类解释事物。根据不同的主题调整解释的格式、深度和风格。"
changelog: "Restructured with auxiliary files; added Quick Reference"
---
## 自适应解释偏好设置

**适用范围：** 仅针对面向人类的解释内容。记录哪些解释有效，哪些无效。

### 快速参考

| 文件          | 用途                                      |
|--------------|-----------------------------------------|
| `formats.md`     | 用于判断项目符号、纯文本或标题格式的使用效果                   |
| `depth.md`     | 根据用户反馈调整解释的详细程度                         |
| `analogies.md`     | 分析类比在解释中的辅助作用（是帮助还是干扰）                 |
| `domains.md`     | 概述代码、概念、调试及决策过程中的常见模式                 |
| `dimensions.md`     | 列出所有可追踪的解释维度                         |

### 核心流程
1. **观察**：注意解释内容是有效还是引发了用户的困惑。
2. **获取用户反馈**：用户表示“明白了”表示解释有效；表示“等等？”则表示解释无效。
3. **记录模式**：当连续收到两次或以上相同的反馈时，记录该模式。
4. **确认**：只有在用户明确表示“理解”后，才将该解释内容存储到记忆中。

### 默认设置（在用户学习新偏好之前）
- 首先提供直接答案，随后再提供相关背景信息。
- 解释内容的长度应与问题长度相匹配（简单问题对应简短答案）。
- 对于复杂主题，每次解释一个概念。
- 提供适当的详细程度：询问用户“需要更多细节吗？”而不是直接提供大量信息。

---

## 记忆存储

这些偏好设置会保存在 `~/explain/memory.md` 文件中。首次使用时需要创建该文件：

```markdown
## Format
<!-- Format: "topic: preference (level)" -->
<!-- Ex: code: bullets (confirmed), concepts: prose (pattern) -->

## Depth
<!-- Format: "topic: depth (level)" -->
<!-- Ex: React: deep (confirmed), Git: tldr (pattern) -->

## Examples
<!-- Format: "topic: example-style (level)" -->
<!-- Ex: SQL: always examples (confirmed), theory: minimal (pattern) -->

## Jargon
<!-- Format: "domain: jargon-level (level)" -->
<!-- Ex: programming: full jargon (confirmed), finance: simplify (pattern) -->

## Never
<!-- Approaches that fail. Format: "approach (level)" -->
<!-- Ex: walls of text (confirmed), over-analogizing (pattern) -->
```

*解释状态的层级：*  
- 模式（连续收到两次或以上反馈） → 确认（用户明确表示理解） → 固定（通过后续反馈得到强化）