---
name: kindle-import
description: 将来自 Kindle HTML 导出文件的阅读笔记导入到 slipbox 中。当用户发送 Kindle 笔记本导出文件（HTML/XHTML 格式）时，系统会解析书籍的标题和作者信息，仅提取用户的笔记内容（忽略高亮标记），随后针对每条笔记运行 slipbot 工具进行处理。
---

# Kindle 导入功能

该功能用于解析 Kindle 笔记本导出的 HTML 文件，并为用户创建相应的笔记条目。

## 输入格式

Kindle 导出的文件为 XHTML 格式，其结构如下：

```html
<div class="bookTitle">Book Title Here</div>
<div class="authors">Author Name</div>
...
<div class="sectionHeading">Chapter/Section Name</div>
<div class="noteHeading">Highlight (yellow) - Section > Page X</div>
<div class="noteText">Highlighted text from book</div>
<div class="noteHeading">Note - Section > Page X</div>
<div class="noteText">User's own note</div>
```

**关键区分：**
- 以 “Highlight” 开头的 `noteHeading` 表示书籍正文，应被**跳过**；
- 以 “Note” 开头的 `noteHeading` 表示用户的个人笔记，应被**导入**。

## 解析规则

### 元数据提取
1. 书籍标题：从 `.bookTitle` 元素中获取。
2. 作者：从 `.authors` 元素中获取。
3. 文件类型：确定为 “book”。

### 内容提取
1. 查找所有的 `noteHeading` 元素。
2. 如果标题以 “Note” 开头，则获取其后的 `noteText` 内容并**导入**；
3. 如果标题以 “Highlight” 开头，则**跳过**该部分内容。
4. 部分章节信息（例如 “Client-side/Stateless Sessions > Page 28”）可以忽略。

## 工作流程
1. **解析文件**：提取书籍标题和作者信息。
2. **提取用户笔记**：仅导入以 “Note” 开头的笔记条目（忽略以 “Highlight” 开头的条目）。
3. **预检查**：向用户显示书籍标题、作者以及笔记数量，并请求用户确认。
4. **确认后**：针对每条笔记，调用 slipbot 进行处理：
   - 笔记类型：前缀为 “-”；
   - 来源信息：`~ book, {title} by {author}`；
   - 由 slipbot 负责处理文件名、标签、链接以及图表的更新。
5. **报告**：生成导入的笔记数量。

## 示例

**输入文件元数据：**
- 标题：《JWT 手册》（The JWT Handbook）
- 作者：Sebastian E Peyrott

**解析后的笔记条目：**
```
Highlight (yellow) - Page 28: "This is easily solved by..." → SKIP
Note - Page 28: "Applications should not allow unsigned JWTs..." → IMPORT
```

**Slipbot 调用示例：**
```
- Applications should not allow unsigned JWTs to be considered valid. ~ book, The JWT Handbook by Sebastian E Peyrott
```

## 特殊情况处理
- **没有用户笔记**（只有书籍正文）：报告 “没有笔记需要导入”。
- **有多位作者**：保留文件中的原始作者信息。
- **作者信息缺失**：使用 “未知” 作为作者名称。
- **标题或内容中包含特殊字符**：在存储前进行解码（例如将 “&” 转换为 “与”）。
- **HTML 实体**：在存储前进行解码（如将 “&” 转换为 “与” 等符号）。

## 支持的文件类型
- 从 Kindle 应用程序导出的 `.html` 文件。
- 结构相同的 XHTML 文件。
- 通过 Telegram 发送的文件（格式为 application/xml 或 text/plain）。