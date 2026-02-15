---
name: instapaper-import
description: 将来自 Instapaper 导出的阅读笔记导入 slipbox。当用户粘贴包含文章标题和笔记的 Instapaper 高亮内容时，该功能会自动执行：从头部解析文章标题/URL，提取用户自己的笔记（纯文本行），忽略原始的高亮内容，然后针对每条笔记运行 slipbot 处理程序。
---

# 从 Instapaper 导入内容

解析 Instapaper 中的高亮内容，并将其转换为用户笔记的形式（以 Slipbox 格式存储）。

## 输入格式

```
# [[Article Title](url)]
> Original highlight from article (SKIP)
User's note about the highlight (IMPORT)
> Another highlight (SKIP)
Another user note (IMPORT)
```

**关键区别：**
- 以 `>` 开头的行：表示原文的高亮部分 → **跳过这些行**
- 纯文本行：表示用户的想法或总结 → **将这些行导入为笔记**

## 解析规则

### 标题行
1. 从 `# [[标题](链接)]` 中提取标题。
2. 链接可以是 `instapaper-private://...`（私有链接）或普通链接。
3. 文章类型：`article`。
4. 作者：`null`（Instapaper 不提供作者信息）。

### 内容行
1. 以 `>` 开头的行：表示原文的高亮部分 → **跳过这些行**。
2. `>` 后面的纯文本行：表示用户的笔记 → **将这些行导入**。
3. 空行：跳过。
4. 每条用户笔记都会成为一条独立的 Slipbox 条目。

## 工作流程
1. **解析标题行**：提取文章标题和链接。
2. **提取用户笔记**：收集所有不以 `>` 开头的纯文本行。
3. **预检查**：向用户显示文章标题和笔记数量，并请求确认。
4. **确认后**：对每条笔记执行以下操作：
   - 使用 `slipbot` 创建笔记：前缀为 `-`。
   - 指定笔记的来源为 `~ 文章, {标题}`。
   - 由 `slipbot` 负责处理文件的命名、添加标签、处理链接以及更新图表。
5. **报告**：显示创建的笔记数量。

## 示例

**输入：**
```
# [[How to Learn Faster](https://example.com/article)]
> Get feedback more often
To learn faster we need faster feedback loops.
> Latent learning occurs without reinforcement
Testing yourself proactively speeds up learning.
```

**提取的笔记：**
1. “要更快地学习，我们需要更快的反馈循环。”
2. “主动进行自我测试可以加快学习速度。”

**Slipbot 的执行内容：**
```
- To learn faster we need faster feedback loops. ~ article, How to Learn Faster
- Testing yourself proactively speeds up learning. ~ article, How to Learn Faster
```

## 特殊情况
- **没有用户笔记**（只有 `>` 行）：报告“没有笔记可供导入”。
- **多行用户笔记**：将每段文字视为独立的笔记。
- **包含特殊字符的标题**：保持原样作为来源元数据。