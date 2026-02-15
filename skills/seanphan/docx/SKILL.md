---
name: docx
description: "提供全面的文档创建、编辑和分析功能，支持版本控制（跟踪更改）、添加注释、保持格式不变以及文本提取。当Claude需要处理专业文档（.docx格式文件）时，可以执行以下操作：  
(1) 创建新文档；  
(2) 修改或编辑文档内容；  
(3) 查看并处理已记录的更改；  
(4) 添加注释；  
以及完成其他与文档相关的任务。"
license: Proprietary. LICENSE.txt has complete terms
---

# DOCX文件的创建、编辑与分析

## 概述

用户可能会要求你创建、编辑或分析.docx文件的内容。.docx文件本质上是一个ZIP压缩包，其中包含XML文件和其他可读或可编辑的资源。针对不同的任务，有多种工具和工作流程可供选择。

## 工作流程决策树

### 阅读/分析内容
可以使用以下“文本提取”或“原始XML访问”方法：

### 创建新文档
使用“创建新的Word文档”工作流程

### 编辑现有文档
- **自己的文档 + 简单修改**
  使用“基本OOXML编辑”工作流程

- **他人的文档**
  推荐使用“标记修改工作流程”

- **法律、学术、商业或政府文档**
  必须使用“标记修改工作流程”

## 阅读与分析内容

### 文本提取
如果只需要阅读文档的文本内容，可以使用pandoc将文档转换为markdown格式。pandoc在保留文档结构方面表现出色，并且能够显示标记的修改内容：

```bash
# Convert document to markdown with tracked changes
pandoc --track-changes=all path-to-file.docx -o output.md
# Options: --track-changes=accept/reject/all
```

### 原始XML访问
当需要访问文档中的注释、复杂格式、文档结构、嵌入媒体和元数据时，需要直接操作原始XML。为此，你需要解压文档并读取其原始XML内容：

#### 解压文档
`python ooxml/scripts/unpack.py <office_file> <output_directory>`

#### 主要文件结构
* `word/document.xml` - 主文档内容
* `word/comments.xml` - 文档.xml中引用的注释
* `word/media/` - 嵌入的图片和媒体文件
- 标记的修改内容使用 `<w:ins>`（插入）和 `<w:del>`（删除）标签

## 创建新的Word文档

要从零开始创建新的Word文档，可以使用**docx-js**，它允许你使用JavaScript/TypeScript来生成Word文档。

### 工作流程
1. **强制要求 - 完整阅读文件**：务必从头到尾阅读[`docx-js.md`](docx-js.md)（约500行）。在开始创建文档之前，请务必阅读完整文件内容，以了解详细的语法规范、格式规则和最佳实践。
2. 使用`Document`、`Paragraph`、`TextRun`组件创建一个JavaScript/TypeScript脚本（假设所有依赖项都已安装；如果没有，请参考下面的依赖项说明）。
3. 使用`Packer.toBuffer()`将脚本导出为.docx格式。

## 编辑现有的Word文档

在编辑现有的Word文档时，可以使用**Document库**（一个用于处理OOXML的Python库）。该库会自动处理基础设施设置，并提供文档操作的方法。对于复杂的情况，你可以直接通过库访问底层DOM。

### 工作流程
1. **强制要求 - 完整阅读文件**：务必从头到尾阅读[`ooxml.md`](ooxml.md)（约600行）。在开始编辑文档之前，请务必阅读完整文件内容，以了解Document库的API和XML格式规范。
2. 解压文档：`python ooxml/scripts/unpack.py <office_file> <output_directory>`
3. 使用Document库创建并运行Python脚本（详见ooxml.md中的“Document库”部分）。
4. 将最终文档打包：`python ooxml/scripts/pack.py <input_directory> <office_file>`

Document库提供了常见操作的高级方法，同时也支持直接访问底层DOM以处理复杂情况。

## 用于文档审查的标记修改工作流程

此工作流程允许你在将修改内容应用到OOXML之前，使用markdown格式规划详细的修改内容。**重要提示**：对于所有标记的修改，必须系统地逐一实现它们。

**分批策略**：将相关的修改内容分成每批3-10条的批次进行。这样既能方便调试，又能保持效率。在处理下一批之前，请先测试每一批修改。

**编辑原则**：仅标记实际发生变化的文本。重复未更改的文本会使得修改内容难以审查，并显得不专业。修改操作应分为以下几部分：[未更改的文本] + [删除内容] + [插入内容] + [未更改的文本]。为了保留未更改文本的原始RSID，可以从原始文档中提取 `<w:r>` 元素并重新使用它。

**示例**：将句子中的“30 days”修改为“60 days”：
```python
# BAD - Replaces entire sentence
'<w:del><w:r><w:delText>The term is 30 days.</w:delText></w:r></w:del><w:ins><w:r><w:t>The term is 60 days.</w:t></w:r></w:ins>'

# GOOD - Only marks what changed, preserves original <w:r> for unchanged text
'<w:r w:rsidR="00AB12CD"><w:t>The term is </w:t></w:r><w:del><w:r><w:delText>30</w:delText></w:r></w:del><w:ins><w:r><w:t>60</w:t></w:r></w:ins><w:r w:rsidR="00AB12CD"><w:t> days.</w:t></w:r>'
```

### 标记修改工作流程

1. **获取带有标记修改的markdown格式**：将文档转换为包含标记修改的markdown格式：
   ```bash
   pandoc --track-changes=all path-to-file.docx -o current.md
   ```

2. **识别并分组修改内容**：仔细阅读文档，识别所有需要修改的内容，并将它们分组到合理的批次中：
   - **定位修改位置的方法**（用于在XML中查找修改位置）：
     - 节目/标题编号（例如：“Section 3.2”、“Article IV”）
     - 如果有编号，则使用段落标识符
     - 使用带有唯一上下文的grep模式
     - 文档结构（例如：“第一段”、“签名块”
     - **注意：不要使用markdown中的行号**——它们与XML结构不对应

   **分组修改内容**（每批包含3-10条相关修改）：
     - 按节分组：“批次1：第2节的修改”，“批次2：第5节的更新”
     - 按类型分组：“批次1：日期修正”，“批次2：政党名称的更改”
     - 按复杂性分组：先处理简单的文本替换，再处理复杂的结构修改
     - 按顺序分组：“批次1：第1-3页”，“批次2：第4-6页”

3. **阅读文档并解压**：
   - **强制要求 - 完整阅读文件**：务必从头到尾阅读[`ooxml.md`](ooxml.md)（约600行）。请特别注意“Document库”和“标记修改模式”部分。
   - **解压文档**：`python ooxml/scripts/unpack.py <file.docx> <dir>`
   - **注意建议的RSID**：解压脚本会提供一个RSID，用于标记修改内容。请将此RSID复制到步骤4b中使用。

4. **分批实施修改**：按逻辑（按节、按类型或按位置）分组修改内容，并在单个脚本中一起实施这些修改。这样做：
   - 便于调试（较小的批次更容易定位错误）
   - 可实现逐步推进
   - 保持效率（每批3-10条修改效果较好）

**建议的分组方式**：
   - 按文档节分组（例如：“第3节的修改”、“定义”、“终止条款”）
   - 按修改类型分组（例如：“日期修改”、“政党名称更新”、“法律术语替换”）
   - 按位置分组（例如：“第1-3页的修改”、“文档前半部分的修改”）

   对于每一组修改内容：
   - **a. 将文本映射到XML**：使用grep在`word/document.xml`中查找文本，确认文本是如何分布在 `<w:r>` 元素中的。
   - **b. 创建并运行脚本**：使用`get_node`找到相关节点，实施修改，然后调用`doc.save()`。具体方法请参阅ooxml.md中的“Document库”部分。
   - **注意**：在编写脚本之前，请务必使用`grep word/document.xml`获取当前的行号并验证文本内容。每次运行脚本后，行号可能会发生变化。

5. **打包文档**：所有批次完成后，将解压后的目录转换回.docx格式：
   ```bash
   python ooxml/scripts/pack.py unpacked reviewed-document.docx
   ```

6. **最终验证**：对整个文档进行全面的检查：
   - 将最终文档转换为markdown格式：
     ```bash
     pandoc --track-changes=all reviewed-document.docx -o verification.md
     ```
   - 确认所有修改内容都正确应用：
     ```bash
     grep "original phrase" verification.md  # Should NOT find it
     grep "replacement phrase" verification.md  # Should find it
     ```
   - 确保没有引入任何意外的修改

## 将文档转换为图像

为了可视化分析Word文档，可以使用两步流程将其转换为图像：

1. **将DOCX转换为PDF**：
   ```bash
   soffice --headless --convert-to pdf document.docx
   ```

2. **将PDF页面转换为JPEG图像**：
   ```bash
   pdftoppm -jpeg -r 150 document.pdf page
   ```
   这会生成如`page-1.jpg`、`page-2.jpg`等文件。

**选项**：
- `-r 150`：设置分辨率为150 DPI（根据质量和大小需求进行调整）
- `-jpeg`：输出JPEG格式（如需要PNG格式，请使用`-png`）
- `-f N`：指定要转换的起始页码（例如，`-f 2`表示从第2页开始转换）
- `-l N`：指定要转换的结束页码（例如，`-l 5`表示在第5页停止）
- `page`：输出文件的前缀

**示例**：针对特定范围的转换：
```bash
pdftoppm -jpeg -r 150 -f 2 -l 5 document.pdf page  # Converts only pages 2-5
```

## 代码风格指南
**重要提示**：在编写与DOCX操作相关的代码时：
- 代码应简洁明了
- 避免使用冗长的变量名和多余的代码操作
- 避免不必要的`print`语句

## 依赖项

**必需的依赖项（如果尚未安装，请安装）**：
- **pandoc**：`sudo apt-get install pandoc`（用于文本提取）
- **docx**：`npm install -g docx`（用于创建新文档）
- **LibreOffice**：`sudo apt-get install libreoffice`（用于PDF转换）
- **Poppler**：`sudo apt-get install poppler-utils`（用于使用pdftoppm将PDF转换为图像）
- **defusedxml**：`pip install defusedxml`（用于安全地解析XML）