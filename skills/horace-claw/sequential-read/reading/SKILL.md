---
name: sequential-read-reading
description: "**按顺序读取数据块并生成结构化的反馈信息**"
user-invocable: false
---

# 阅读阶段 — 顺序阅读与反思

您正在执行顺序阅读任务的阅读阶段。您需要按顺序阅读每个阅读片段，并在每个片段之后撰写一份结构化的反思。整个过程由系统自动完成。

## 输入参数

系统将提供以下信息：
- `SESSION_ID` — 会话标识符
- `BASE_DIR` — `sequential_read` 技能目录的路径
- `LENS` — 可选的阅读视角/角色（可选，可设置为 `null`）

## 核心原则

**您无法预知后续内容**。每份反思都必须从当前阅读阶段的视角来撰写，不得引用后续片段的内容。您的预测可能会错误——这正是本次练习的目的所在。

## 阅读循环

对于会话中的每个片段，请重复以下步骤：

### 1. 检查进度

```bash
python3 {BASE_DIR}/scripts/state_manager.py get {SESSION_ID}
```

读取 `current_chunk`，并与 `total_chunks`（来自 `session.json`）进行比较。如果 `current_chunk` 大于或等于 `total_chunks`，则表示阅读阶段已完成——直接跳转到下面的“结束阶段”。

### 2. 获取上下文信息

```bash
python3 {BASE_DIR}/scripts/state_manager.py get-context {SESSION_ID}
```

系统会提供以下信息：
- 您的长期阅读记忆（摘要、关键信息、主题、疑问、预测）
- 最近 2-3 段落的完整反思内容
- 对之前反思的任何注释
- 下一个片段的元数据

### 3. 阅读下一个片段

```bash
python3 {BASE_DIR}/scripts/chunk_manager.py get {SESSION_ID} {NEXT_CHUNK_NUMBER}
```

仔细阅读当前片段，给自己足够的时间来理解内容。

### 4. 撰写反思

阅读位于 `{BASE_DIR}/templates/reflection.prompt.md` 的反思模板（只需在第一次迭代时阅读此文件）。

根据模板内容填写以下信息：
- `{source_title}` — 原始文件的名称
- `{chunk_number}` / `{total_chunks}` — 当前阅读进度
- `{lensInstruction}` — 如果指定了阅读视角：`您正在以 **{lens}** 的视角来阅读这段内容。请让这种视角影响您的思考和问题。`如果没有指定阅读视角，则留空。`
- 第 2 步中获取的上下文信息
- 第 3 步中读取的片段内容

按照模板结构撰写您的反思：
1. **理解** — 文本的主要内容或论点
2. **反应** — 您的真实感受（包括正面和负面的观点）
3. **分析** — 对写作技巧的观察
4. **疑问** — 对后续内容的预测
5. **修正** — 对之前内容的重新思考
6. **注释** — 如果当前片段对之前的内容有所补充或修正（请注明对应的片段编号）

**写作指南**：
- 表达要具体，避免使用笼统的描述。例如：“对话显得生硬”可以写成：“咖啡馆场景中的对话显得很生硬——角色们以一种不符合现实的方式大声解释自己的动机。”
- 混乱、无聊或沮丧都是正常的反应。不要强行表现出不符合自己真实感受的情绪。
- 在修正之前的观点时，要明确指出具体发生了什么变化以及原因。
- 引用原文时要谨慎——仅使用那些具有代表性的语句，而不仅仅是观点本身。
- 预测应具体明确：“我认为 X 会发生，因为 Y” 而不是 “我想知道会发生什么”。

**质量要求**：
- 每份反思都必须包含对文本的真诚、深入的分析。占位符文本、简略的描述或泛泛而谈的内容都是不可接受的。
- 每个部分（理解、反应、分析、疑问、修正）都应包含至少 2-3 句有意义的分析。
- 整篇反思的篇幅应至少为 20 行。如果发现自己的反思篇幅过短，说明您可能没有认真阅读——请放慢速度，更加专注地思考所读内容。
- 即使是第 30 个片段的反思，其质量也同样重要。整个练习的目的是记录整个阅读过程，而不仅仅是最初几段的体验。

### 5. 保存反思

将反思内容写入临时文件，然后再保存到最终文件中：

```bash
python3 {BASE_DIR}/scripts/state_manager.py save-reflection {SESSION_ID} {CHUNK_NUMBER} --file /tmp/reflection.md
```

### 6. 保存注释（如有）

如果您的反思中包含对之前片段的注释，请将它们保存下来：

```bash
# Write annotation text to temp file first
python3 {BASE_DIR}/scripts/state_manager.py save-annotation {SESSION_ID} {ANNOTATED_CHUNK_NUMBER} --file /tmp/annotation.md
```

### 7. 重复循环

返回步骤 1，继续阅读下一个片段。**不要中途询问用户任何问题**。请一次性完整地处理所有片段。

## 结束阶段

当所有片段都阅读完毕后：

```bash
python3 {BASE_DIR}/scripts/session_manager.py update {SESSION_ID} --set status=read
```

阅读阶段结束。接下来进入文本的综合分析阶段。

## 恢复中断的会话

如果您正在恢复一个中途中断的会话，状态管理系统会精确记录您之前的阅读进度。`current_chunk` 变量会告诉您最后一篇被反思的片段编号。只需从 `current_chunk + 1` 开始继续阅读即可。