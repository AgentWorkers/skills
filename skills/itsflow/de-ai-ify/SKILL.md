---
name: de-ai-ify
description: **将 AI 生成的行话去除，还原文本的自然语言表达**
version: 1.0.0
author: theflohart
tags: [writing, editing, voice, ai-detection]
---

# 去除文本中的AI痕迹，还原自然的人类语言风格

本工具用于去除文本中由AI生成的表述，让您的写作更加贴近自然的人类语言风格。

## 使用方法

```
/de-ai-ify <file_path>
```

## 被删除的内容

### 1. 过度使用的过渡词
- “Moreover”（此外）、“Furthermore”（而且）、“Additionally”（另外）、“Nevertheless”（然而）
- 过度使用“However”（然而）
- 以“While X, Y”开头的句子结构

### 2. AI常用的陈词滥调
- “In today's fast-paced world”（在当今快节奏的世界里）
- “Let's dive deep”（让我们深入探讨）
- “Unlock your potential”（释放您的潜力）
- “Harness the power of”（利用……的力量）

### 3. 模棱两可的表述
- “It's important to note”（需要注意的是）
- “It's worth mentioning”（值得一提的是）
- 模糊的量化词：various（各种的）、numerous（众多的）、myriad（无数的）

### 4. 企业常用的术语
- “utilize”（利用）→ “使用”
- “facilitate”（促进）→ “帮助”
- “optimize”（优化）→ “改进”
- “leverage”（利用）→ “使用”

### 5. 机械化的写作模式
- 用反问句后紧接着给出答案
- 过于刻板的平行结构
- 总是使用三个例子
- 强调性的表述方式

## 被添加的内容

### 自然的语言风格
- 句子长度多样化
- 交谈式的语气
- 直接的表达方式
- 具体的例子

### 人类语言的特点
- 自然的过渡
- 自信的陈述
- 个人化的视角
- 真实的表达方式

## 处理流程
1. **阅读原始文件**
2. **创建带有“-HUMAN”后缀的副本**
3. **应用去AI化处理**
4. **提供修改日志**

## 输出结果
- 一份具有自然人类语言风格的新的文件
- 显示修改内容的修改日志
- 需要添加具体例子的部分列表

## 示例对比

**修改前（AI风格）：** “在当今快速发展的数字环境中，重要的是要认识到，有效利用AI不仅仅意味着使用尖端技术，更重要的是利用其变革潜力，从而开启前所未有的机会。”

**修改后（人类风格）：** “AI在特定任务中发挥最佳作用。专注于它擅长的方面：编写代码、分析数据和回答问题。”