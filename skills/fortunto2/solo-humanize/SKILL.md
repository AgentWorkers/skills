---
name: solo-humanize
description: >
  **从文本中去除 AI 写作特征**  
  这些特征包括：破折号（–）、固定短语、过度使用的宣传性语言、刻意营造的“真实感”、以及遵循“三段式结构”的列表。  
  适用场景：当用户要求“让内容更具人性化”、“让语言听起来更自然”、或要求“去除 AI 生成的痕迹”时；也适用于 `/content-gen` 或 `/landing-gen` 生成内容后的处理步骤。
license: MIT
metadata:
  author: fortunto2
  version: "1.0.1"
  openclaw:
    emoji: "✍️"
allowed-tools: Read, Write, Edit, Glob, Grep
argument-hint: "[file-path or paste text]"
---
# /humanize

该工具用于去除用户界面文本中的人工写作痕迹，将文件或粘贴的文本改写得看起来像真人所写，同时确保内容与结构保持不变。

## 该工具的用途

大型语言模型（LLM）生成的文本通常具有明显的特征：使用破折号、固定短语、过度宣传的表述以及刻意营造的“真实性”。读者（以及搜索引擎如Google）能够察觉到这些痕迹。本工具能够识别并修改这些人为添加的元素。

## 使用场景

- 在执行 `/content-gen`、`/landing-gen`、`/video-promo` 等任务后，对输出内容进行润色；
- 在发布任何面向用户的文本（如博客文章、着陆页、电子邮件）之前；
- 在编辑将被人类阅读的 CLAUDE.md 或相关文档时；
- 也可以单独使用：`/humanize path/to/file.md`

## 输入格式

- **文件路径**：从 `$ARGUMENTS` 中获取，工具会直接读取并修改该文件；
- **无参数**：提示用户粘贴文本，工具会输出处理后的版本；
- 支持 `.md`、`.txt` 格式的文件，以及 `.tsx` 或 `.html` 文件中的纯文本内容。

## 常见问题及修改方法

### 1. 破折号使用过度（—）

破折号是人工智能写作最明显的标志。应将其替换为逗号、句号或冒号，或重新组织句子结构。

| 修改前 | 修改后 |
|--------|-------|
| "The tool — which is free — works great" | "The tool (which is free) works great" |
| "Three features — speed, security, simplicity" | "Three features: speed, security, simplicity" |
| "We built this — and it changed everything" | "We built this. It changed everything." |

**规则**：每500个单词最多使用1个破折号。最好完全避免使用破折号。

### 2. 固定短语

这些短语表明文本是由人工智能生成的。应将其删除或替换为更具体的表述。

**需删除的填充性短语**：
- "it's worth noting that" → 直接陈述事实
- "at the end of the day" → 省略
- "in today's world" / "in the modern landscape" → 省略
- "without further ado" → 省略
- "let's dive in" / "let's explore" → 省略

**需替换的过度宣传性表述**：
- "game-changer" → 具体改变了什么？
- "revolutionary" → 实际上有哪些新功能？
- "cutting-edge" → 描述技术的实际优势
- "seamless" → 可以表述为“无需配置即可使用”
- "leverage" → 可以表述为“使用该技术”
- "robust" → 可以表述为“能够处理某些特定情况”
- "streamline" → 可以表述为“将步骤从N减少到M”
- "empower" → 可以表述为“用户现在可以做什么”
- "unlock" → 可以表述为“实际具备哪些功能”

**需修改的刻意营造真实感的表达**：
- "to be honest" → 如果需要使用这句话，说明其余内容是否真实
- "let me be frank" → 直接表达观点
- "I have to say" → 直接说出想法
- "honestly" → 省略
- "the truth is" → 直接陈述事实

### 3. 三重结构（如“fast, secure, and scalable”）

人工智能喜欢使用三个并列的词组。实际写作中这些词组的数量会有所变化。

| 修改前 | 修改后 |
|--------|-------|
| "Fast, secure, and scalable" | "Fast and secure"（如果“scalable”尚未得到验证，则省略）
- "Build, deploy, and iterate" | "Build and ship"（如果指的是这个过程）
- 三个意思重复的列表项 | 保留一个清晰的核心点**

**规则**：如果在同一文档中发现了三个或更多的三重结构列表，至少删除其中一半。

### 4. 结构问题

人工智能生成的文本往往遵循固定的结构：标题 → 一句话引言 → 三个列表项 → 过渡句。实际写作中各部分的长度和结构更加灵活。

- **矛盾的表述**：
  “While X has limitations, it offers Y, making it Z.” → 应明确选择其中一方并直接说明。
- **不均衡的对比**：
  “On one hand X, on the other hand Y.” → 如果某一方明显更优，应直接指出。

### 5. 过分讨好的开头语

- "Great question!" → 省略
- "That's a fantastic idea!" → 省略，或直接说明这个想法的具体优点
- "Absolutely!" → 如果并非真心赞同，应省略
- "I'd be happy to help!" → 直接提供帮助

### 6. 被动语态和弱动词

- "It should be noted that" → 直接陈述事实
- "There are several factors that" → 应列出具体因素
- "It is important to" → 应说明原因
- "This can be achieved by" → 应直接表述为“通过……实现”

## 工作流程

1. **读取输入**：无论是文件路径还是粘贴的文本。
2. **检查问题**：根据上述类别逐一分析文本中的问题。
3. **进行修改**：修复问题，同时保持以下原则：
   - 技术准确性（代码、命令和技术术语保持不变）
   - 结构（标题、列表、代码块等保持原样）
   语气（如果原文较为随意，修改后也应保持同样的风格）
   长度（尽量保持与原文相同或更简短）

4. **展示修改内容**：
   ```
   Humanized: {file or "pasted text"}

   Changes:
     Em dashes:  {N} removed
     Stock phrases: {N} replaced
     Inflation: {N} deflated
     Triplets: {N} broken
     Sycophancy: {N} cut
     Total: {N} patterns fixed

   Before: {word count}
   After:  {word count}
   ```

5. **如果提供文件路径**：将处理后的文件写回原路径，并提供差异对比摘要。
   **如果提供粘贴的文本**：直接输出处理后的版本。

## 不可修改的内容

- 代码块和内联代码
- 技术术语、库名、命令行界面（CLI）命令
- 引用他人的话（需保持原样）
- 数字、日期、URL
- 标题结构（不得合并或拆分章节）
- 内容含义（仅允许重新表述，不得添加或删除任何内容）

## 特殊情况处理

- **文本过短（<50个单词）**：仅应用固定短语的过滤规则，跳过结构分析。
- **文本已非常干净**：报告“未发现人工智能痕迹”。
- **包含大量代码的文档**：跳过代码块，仅处理纯文本部分。
- **非英语文本**：同样应用破折号和结构规则，但忽略英语中的固定短语。