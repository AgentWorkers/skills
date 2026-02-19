---
name: pdf-reader
description: 从PDF文件中提取文本、在其中进行搜索，并生成摘要。
homepage: "https://pymupdf.readthedocs.io"
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "requires": { "bins": ["python3"], "pip": ["PyMuPDF"] },
        "install":
          [
            {
              "id": "pymupdf",
              "kind": "pip",
              "package": "PyMuPDF",
              "label": "Install PyMuPDF",
            },
          ],
        "version": "1.1.0",
      },
  }
---
# PDF阅读器技能

`pdf-reader`技能提供了使用PyMuPDF（fitz）从PDF文件中提取文本和检索元数据的功能。

## 工具API

该技能提供了两个命令：

### extract
从指定的PDF文件中提取纯文本。

- **参数：**
  - `file_path` (字符串，必填)：要提取文本的PDF文件路径。
  - `--max_pages` (整数，可选)：要提取的最大页面数。

**用法：**
```bash
python3 skills/pdf-reader/reader.py extract /path/to/document.pdf
python3 skills/pdf-reader/reader.py extract /path/to/document.pdf --max_pages 5
```

**输出：** PDF文件中的纯文本内容。

### metadata
检索有关文档的元数据。

- **参数：**
  - `file_path` (字符串，必填)：PDF文件的路径。

**用法：**
```bash
python3 skills/pdf-reader/reader.py metadata /path/to/document.pdf
```

**输出：** 包含以下PDF元数据的JSON对象：
- `title`：文档标题
- `author`：文档作者
- `subject`：文档主题
- `creator`：创建PDF的应用程序
- `producer`：PDF生成器
- `creationDate`：创建日期
- `modDate`：修改日期
- `format`：PDF格式版本
- `encryption`：加密信息（如果有的话）

## 实现说明

- 使用**PyMuPDF**（导入为`pymupdf`）进行快速、可靠的PDF处理
- 支持加密的PDF文件（如果需要密码，则会返回错误）
- 通过`max_pages`选项高效处理大型PDF文件
- 元数据命令返回结构化的JSON数据

## 示例

```bash
# Extract text from first 3 pages
python3 skills/pdf-reader/reader.py extract report.pdf --max_pages 3

# Get document metadata
python3 skills/pdf-reader/reader.py metadata report.pdf
# Output:
# {
#   "title": "Annual Report 2024",
#   "author": "John Doe",
#   "creationDate": "D:20240115120000",
#   ...
# }
```

## 错误处理

- 如果文件未找到或不是有效的PDF文件，会返回错误消息
- 如果PDF文件被加密且需要密码，会返回错误
- 能够优雅地处理损坏或格式错误的PDF文件