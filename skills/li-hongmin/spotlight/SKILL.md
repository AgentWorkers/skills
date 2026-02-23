---
name: spotlight
description: 使用 macOS 的 Spotlight 索引功能（mdfind）来搜索文件和内容。当用户需要在 macOS 上搜索本地文件、文档或目录时，可以使用该工具。该功能支持在 PDF 文件、Word 文档、文本文件等中搜索文本内容，对于大型文档集合而言，其搜索速度远高于 grep。请注意，该工具仅适用于已启用 Spotlight 功能的 macOS 系统。
---
# Spotlight搜索

使用macOS的Spotlight索引系统来搜索本地文件。

## 使用场景

在以下情况下使用此技能：
- 用户请求在macOS上搜索文件或目录
- 需要查找包含特定文本的文档
- 需要在大量文档中搜索（比使用`grep`更快）
- 需要在PDF、Word文档或其他已索引的格式中搜索

## 快速入门

```bash
scripts/spotlight-search.sh <directory> <query> [--limit N]
```

**示例：**

```bash
# Search for "machine learning" in Documents
scripts/spotlight-search.sh ~/Documents "machine learning"

# Search research papers with limit
scripts/spotlight-search.sh ~/research "neural networks" --limit 10

# Search Chinese/Japanese content
scripts/spotlight-search.sh ~/璐璐研究 "留日" --limit 20
```

## 搜索功能

- **快速**：使用系统级别的Spotlight索引（无需扫描文件）
- **内容感知**：可以在PDF、docx、txt、md等格式中搜索
- **多语言支持**：支持中文、日文等多种语言
- **元数据显示**：返回文件路径、类型和大小

## 输出格式

```
🔍 在 /path/to/directory 中搜索: query

✅ 找到 N 个结果（最多显示 M 个）：

📄 /full/path/to/file.pdf [pdf, 2.3M]
📄 /full/path/to/document.txt [txt, 45K]
📁 /full/path/to/folder/
```

## 支持的文件类型

Spotlight自动索引以下类型的文件：
- 文本文件（txt、md、csv、json、xml等）
- 文档文件（pdf、docx、pages、rtf等）
- 代码文件（py、js、java、c等）
- 电子邮件和联系人信息
- 带有嵌入元数据的图片（支持OCR）

## 限制

- **仅限macOS**：需要启用Spotlight索引功能
- **仅索引已添加到索引的目录**：外部驱动器可能不会被索引
- **关键词搜索**：不是语义搜索（对于语义查询，请使用基于内容的搜索方式）
- **隐私保护**：尊重用户的隐私设置（被排除在索引之外的目录不会显示在搜索结果中）

## 检查索引状态

```bash
# Check if a volume is indexed
mdutil -s /path/to/volume

# Enable indexing (requires admin)
sudo mdutil -i on /path/to/volume
```

## 与大型语言模型（LLM）工作流的集成

**操作流程：搜索 + 提取 + 总结**
1. 使用`spotlight-search.sh`命令查找相关文件
2. 使用`read`工具从搜索结果中提取内容
3. 根据提取的内容总结或回答用户的问题

**示例工作流程：**

```
User: "Find all documents about machine learning in my research folder"

1. Run: spotlight-search.sh ~/research "machine learning" --limit 10
2. Read top 3-5 results with read tool
3. Summarize findings for user
```

## 高级查询语法

Spotlight支持以下高级查询操作符：

```bash
# Exact phrase
spotlight-search.sh ~/Documents "\"machine learning\""

# AND operator
spotlight-search.sh ~/Documents "neural AND networks"

# OR operator
spotlight-search.sh ~/Documents "AI OR artificial intelligence"

# Metadata queries
spotlight-search.sh ~/Documents "kMDItemContentType == 'com.adobe.pdf'"
```

## 故障排除

**未找到结果：**
- 检查目录是否已添加到索引：`mdutil -s /path`
- 等待索引完成（新文件可能需要几分钟时间）
- 确认系统偏好设置中已启用Spotlight

**搜索结果不正确：**
- Spotlight使用模糊匹配和同义词
- 使用精确短语进行搜索：`"精确短语"`
- 检查隐私设置（某些文件夹可能被排除在索引之外）

## 性能

- **即时响应**：利用预生成的索引，无需扫描文件
- **可扩展性强**：能够处理大量文件
- **低CPU占用**：相比`grep`或`ripgrep`，Spotlight对CPU资源的消耗较低

**性能对比：**

| 工具 | 速度 | 内容搜索 | 多语言支持 |
|------|-------|----------------|--------------|
| Spotlight | ⚡ 即时响应 | ✅ 支持 | ✅ 支持 |
| grep/ripgrep | 🐢 较慢 | ✅ 支持 | ✅ 支持 |
| find | ⚡ 快速 | ❌ 不支持 | 不支持 |

## 平台说明

- **仅限macOS**：此功能依赖于macOS的Spotlight系统
- **Linux替代方案**：可以使用`grep -r`或`ripgrep`
- **Windows替代方案**：可以使用Windows的搜索功能或Everything搜索工具