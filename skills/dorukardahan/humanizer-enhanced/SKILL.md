---
name: humanizer-enhanced
description: >
  **高级AI文本人性化工具——专为博客内容设计**  
  该工具能够检测并去除34种典型的AI写作模式，为文本增添自然、人性化的语气，并处理与加密货币/Web3领域相关的语言特征。  
  当用户输入“humanize this”（使文本更自然）、“remove AI patterns”（去除AI写作痕迹）或请求优化博客文章、稿件时，即可使用该工具。  
  **主要功能：**  
  - 基于维基百科列出的28种AI写作特征，识别并修正文本中的AI痕迹  
  - 识别6种与加密货币/Web3领域相关的特定语言模式  
  - 提供严重程度评分（高/中/低）  
  - 自动修复文本中的数据来源引用错误  
  - 为文本注入“灵魂”与个性化元素  
  - 支持批量处理功能  
  **适用场景：**  
  - 博客文章、新闻稿件、技术文档的优化  
  - 需要提升文本自然度、减少AI痕迹的场合  
  **使用说明：**  
  只需在命令行中输入相应指令，即可轻松应用该工具。
metadata:
  version: 1.2.0
  author: 0G Labs content team
---
# Humanizer增强版：识别并消除AI写作痕迹

本版本能够识别并去除文本中由AI生成的痕迹，同时通过添加个性化元素，使内容看起来更像是人类撰写的。

## 快速入门

```text
/humanizer                    # Humanize current file or selection
/humanizer path/to/file.md    # Humanize specific file
/humanizer --scan             # Scan only, don't edit (show issues)
/humanizer --batch drafts/    # Process all .md files in directory
```

---

## 处理流程

### 第1步：扫描文本中的模式

识别文本中的所有AI写作模式，并根据严重程度进行分类：
- **高**：明显的AI写作特征，必须修复（如负向平行结构、聊天机器人风格的语句、过度使用破折号、模糊的表述方式、避免使用连词）
- **中**：常见的AI写作模式，建议修复（如“三原则”（重复使用三个相同的词或短语）、过度强调重要性）
- **低**：较轻微的AI痕迹，如有时间可选择性修复（如标题首字母大写、过度使用粗体）

### 第2步：展示检测结果

向用户展示检测结果的摘要：

```text
## Humanizer scan results

HIGH (3 issues)
- Line 45: Negative parallelism "isn't X. It's Y"
- Line 89: Em dash overuse (5 instances)
- Line 120: "Research shows" without attribution

MEDIUM (5 issues)
- Line 23: Rule of three pattern
- Line 67: Copula avoidance "serves as"
...

LOW (2 issues)
- Line 12: Title case heading
...

Total: 10 issues found
Estimated humanization: ~15 edits needed
```

### 第3步：用户确认后进行修复

询问用户：“是否要修复所有问题？还是逐一查看？”

### 第4步：增添人文色彩

修复模式后，检查文本是否具有自然的人文色彩。缺乏人文色彩的文本仍然可能被识别为AI生成。详细指南请参阅`references/communication-crypto-soul-patterns.md`。

### 第5步：可读性检查

使用Flesch-Kincaid可读性评分标准进行评估：开发者内容的目标分数为10-12分，普通读者内容的目标分数为8-10分。如果评分过高（过于复杂），请简化长句并替换专业术语。

### 第6步：检查破折号的使用

在完成其他所有修复后，再次检查文本中破折号（—）的使用情况。Humanizer在修复过程中可能会重新引入破折号，因此需要删除那些在修复过程中添加的破折号。

---

## 模式分类表

所有34种AI写作模式都配有修改前后的示例，详细信息请参见以下参考文件：

| 模式 | 严重程度 | 参考文件 |
|----------|----------|----------------|
| 1. 过度强调重要性 | 中 | `references/content-patterns.md` |
| 2. 宣传性语言 | 中 | `references/content-patterns.md` |
| 3. 表面化的分析 | 中 | `references/content-patterns.md` |
| 4. 模糊的表述方式 | 高 | `references/content-patterns.md` |
| 5. 公式化的挑战描述 | 中 | `references/content-patterns.md` |
| 6. 普遍性的正面结论 | 中 | `references/content-patterns.md` |
| 7. AI特有的词汇 | 中 | `references/language-style-patterns.md` |
| 8. 避免使用连词 | 高 | `references/language-style-patterns.md` |
| 9. 负向平行结构 | 高 | `references/language-style-patterns.md` |
| 10. “三原则”（重复使用三个相同的词或短语） | 中 | `references/language-style-patterns.md` |
| 11. 过度使用同义词 | 中 | `references/language-style-patterns.md` |
| 12. 错误的范围描述 | 低 | `references/language-style-patterns.md` |
| 13. 过度使用破折号 | 高 | `references/language-style-patterns.md` |
| 14. 过度使用粗体 | 低 | `references/language-style-patterns.md` |
| 15. 行内标题列表 | 中 | `references/language-style-patterns.md` |
| 16. 标题首字母大写 | 低 | `references/language-style-patterns.md` |
| 17. 弧引号的使用 | 低 | `references/language-style-patterns.md` |
| 18. 聊天机器人风格的语句 | 高 | `references/communication-crypto-soul-patterns.md` |
| 19. 关于知识范围的免责声明 | 高 | `references/communication-crypto-soul-patterns.md` |
| 20. 过分谄媚的语气 | 中 | `references/communication-crypto-soul-patterns.md` |
| 21. 过度使用委婉语 | 中 | `references/communication-crypto-soul-patterns.md` |
| 22. 填充性语句 | 中 | `references/communication-crypto-soul-patterns.md` |
| 23. 过度的炒作语言 | 高 | `references/communication-crypto-soul-patterns.md` |
| 24. 模糊的“生态系统”描述 | 中 | `references/communication-crypto-soul-patterns.md` |
| 25. 无根据的统计数据 | 高 | `references/communication-crypto-soul-patterns.md` |
| 26. 过分强调“无缝”或“无摩擦”的体验 | 中 | `references/communication-crypto-soul-patterns.md` |
| 27. 抽象的“赋能”表述 | 中 | `references/communication-crypto-soul-patterns.md` |
| 28. 虚假的去中心化声明 | 高 | `references/communication-crypto-soul-patterns.md` |
| 29. 元叙述（过度描述过程） | 高 | `references/communication-crypto-soul-patterns.md` |
| 30. 错误的受众定位 | 中 | `references/communication-crypto-soul-patterns.md` |
| 31. 用括号定义术语 | 中 | `references/communication-crypto-soul-patterns.md` |
| 32. 顺序编号 | 中 | `references/communication-crypto-soul-patterns.md` |
| 33. 重复使用的过渡词（如“It's worth noting”） | 中 | `references/communication-crypto-soul-patterns.md` |
| 34. 段落结构完全相同 | 高 | `references/communication-crypto-soul-patterns.md` |
| 人文色彩与个性化指南 | — | `references/communication-crypto-soul-patterns.md` |

---

## 严重程度参考

| 严重程度 | 模式 | 处理方式 |
|----------|----------|--------|
| 高 | 负向平行结构、过度使用破折号、聊天机器人风格的语句、模糊的表述方式、避免使用连词、过度炒作、无根据的统计数据、元叙述、段落结构完全相同、虚假的去中心化描述、关于知识范围的免责声明 | 必须修复 |
| 中 | “三原则”、过度强调重要性、宣传性语言、表面化的分析、AI特有的词汇、谄媚的语气、过度使用委婉语、填充性语句、错误的受众定位、用括号定义术语、顺序编号、重复使用的过渡词、“无缝”/“无摩擦”的表述 | 建议修复 |
| 低 | 标题首字母大写、过度使用粗体、错误的范围描述 | 如有时间可选择性修复 |

---

## 快速参考：查找与替换规则

| 需要替换的内容 | 替换为 |
|------|---------|
| `—`（破折号） | `, ` 或 `. ` |
| `serves as` / `stands as` | `is` |
| `isn't X. It's Y` | 重写为简单陈述 |
| `crucial` / `vital` / `pivotal` | 保留“重要”或删除 |
| `Furthermore,` / `Moreover,` | 保留“Also”或删除 |
| `It is important to note` | 删除 |
| `Research shows` | 添加具体来源 |
| “landscape”（抽象表述） | 请使用具体描述 |
| “revolutionizing” / “game-changing” | 请描述实际效果 |
| “seamless” / “frictionless” | 请描述实际的用户体验 |
| “In this article, we'll explore” | 删除 |
| “Let's dive in” / “Let's take a look” | 删除 |
| “First,... Second,... Third,...” | 请调整段落过渡方式 |
| “It's worth noting” / “Notably,” | 删除 |
| “delve” | 请改为“look at”或“examine” |
| “Additionally” | 删除 |

---

## 批量处理模式

如需批量处理多个文件，请参考以下代码：

```bash
# Scan all markdown files in drafts/
/humanizer --scan drafts/*.md

# Fix all files (with confirmation)
/humanizer --batch drafts/
```

## 资料来源

本工具的开发基于以下资源：
- [维基百科：AI写作的特征](https://en.wikipedia.org/wiki/Wikipedia:Signs_of.AI_writing)
- [GitHub项目：blader/humanizer](https://github.com/blader/humanizer)
- 关于加密货币/Web3领域AI写作模式的原创研究

关键见解：“大型语言模型（LLMs）通过统计算法来预测接下来应该使用的内容，其结果往往是适用于最广泛情况的最可能表达方式。”

---

*版本1.2.0 | 专为0G Labs的内容团队开发*