---
name: sequential-read-preread
description: "分析源材料，并将其分割成具有语义意义的片段，以便顺序阅读。"
user-invocable: false
---

# 预读阶段 — 语义分块

您正在执行顺序阅读会话的预读阶段。您的任务是分析源材料，将其分割成语义块，并为后续的阅读做好准备。

## 输入参数

您将收到以下信息：
- `SESSION_ID` — 会话标识符
- `SOURCE_FILE` — 源文本文件的路径
- `BASE_DIR` — `sequential_read` 技能目录的路径

## 执行步骤

### 1. 读取源文件

使用 `read` 工具读取整个源文件，了解其结构、长度和类型（小说、散文、文章、诗歌、非小说类等）。

### 2. 选择分块策略

根据材料类型选择合适的分块方法：

| 材料类型 | 默认分块方法 |
|---|---|
| 有章节的小说 | 每章一个块（非常短的章节可合并） |
| 无章节的小说 | 根据场景划分或按段落边界划分（每块约300-400行） |
| 散文/文章 | 按章节或论点划分 |
| 有章节的非小说类作品 | 每章一个块 |
| 诗歌 | 按诗节或整首诗划分 |
| 短篇小说 | 根据叙事节奏划分（2-5个块） |

**关键约束：**
- 每个块必须包含完整的原始文本，不得删减或总结内容。
- 分块必须保持顺序。
- 每个块都应是一个有意义的阅读单元（不能是句子或段落中间的一部分）。
- 考虑阅读节奏：悬念式的结尾可能更适合与下一节内容搭配阅读。

### 3. 判断是否需要使用结构化分块方式

如果源文件太大而无法完全容纳在您的处理范围内（大约超过200,000个字符），则使用结构化分块工具作为备用方案：

```bash
python3 {BASE_DIR}/scripts/chunk_manager.py structural-chunk {SESSION_ID} {SOURCE_FILE}
```

该工具会自动根据章节标记、场景划分和段落边界对文件进行分块（每块约300-400行），并将所有分块保存到会话目录中。

如果使用结构化分块方式，请跳至步骤5。

### 4. 保存分块（语义分块方法）

对于每个分块：
1. 将分块内容写入临时文件：
   ```bash
   # Write chunk text to temp file (use the read tool to get the text, write tool to save it)
   ```

2. 通过 `chunk_manager` 保存分块信息：
   ```bash
   python3 {BASE_DIR}/scripts/chunk_manager.py save {SESSION_ID} {N} \
     --text-file /tmp/chunk_N.md \
     --meta '{"tone":"<tone>","intensity":"<low|medium|high>","themes":["<theme1>","<theme2>"],"adjacent_relationship":"<relationship to previous/next chunk>"}'
   ```

   元数据字段包括：
   - **语气**：描述性字符串（例如：“忧郁的”、“论辩性的”、“轻松的”、“紧张的”）
   - **难度等级**：低/中/高（表示在情感或智力上的要求）
   - **主题**：1-4个主题标签
   - **相邻关系**：说明该分块与其他分块之间的联系（例如：“解决上一章的悬念”、“新的论点”、“场景的延续”）

### 5. 更新会话状态

```bash
python3 {BASE_DIR}/scripts/session_manager.py update {SESSION_ID} --set status=chunked
```

### 6. 初始化阅读状态

```bash
python3 {BASE_DIR}/scripts/state_manager.py init {SESSION_ID}
```

### 7. 编写分块说明

在会话目录中创建一个名为 `chunking_notes.md` 的文件，说明以下内容：
- 创建了多少个分块及其原因
- 选择的分块方法及其理由
- 源文件中的任何特殊结构特征（如不常见的格式、嵌入的文档等）

保存文件路径为：`{WORKSPACE}/memory/sequential_read/{SESSION_ID}/chunking_notes.md`

## 完成

完成所有步骤后，预读阶段就结束了。接下来可以开始阅读阶段了。