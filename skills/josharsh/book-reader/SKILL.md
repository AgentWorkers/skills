# book-reader

该工具支持从多种来源读取电子书（格式包括 EPUB、PDF 和 TXT），并具备进度跟踪功能。

## 目的

使人工智能代理能够阅读完整长度的书籍，用于学习、内容总结和知识提取。

## 主要功能

- **多种来源支持**：Anna’s Archive、Project Gutenberg、本地文件
- **格式兼容性**：EPUB、PDF、TXT
- **进度跟踪**：自动记录阅读进度
- **智能分块阅读**：将书籍内容分成易于理解的章节进行阅读
- **摘要生成**：在阅读过程中提取关键信息

## 所需工具

- `curl` 或 `wget`：用于下载书籍
- `pandoc`：将 EPUB 格式转换为文本格式（可选，必要时可使用 Python 作为替代方案）
- `pdftotext`（属于 poppler-utils 工具包）：用于提取 PDF 文件中的文本内容
- Python 3 及 `ebooklib` 和 `beautifulsoup4` 库（用于 EPUB 文件的解析）

## 使用方法

### 搜索书籍

```bash
./book-reader.sh search "Thinking Fast and Slow"
```

### 下载书籍

```bash
./book-reader.sh download <book-id> [output-file]
```

### 阅读书籍（支持进度跟踪）

```bash
./book-reader.sh read <file> [--from-page N] [--pages N]
```

### 查看阅读进度

```bash
./book-reader.sh status
```

## 安装方法

```bash
# Install dependencies
sudo apt-get install poppler-utils pandoc  # Linux
# brew install poppler pandoc  # macOS

pip3 install ebooklib beautifulsoup4 lxml

# Make executable
chmod +x book-reader.sh
```

## 书籍来源

1. **Project Gutenberg**（包含 7 万多本公共领域的书籍）：
   - API：https://gutendex.com
   - 免费、合法，无数字版权管理（DRM）限制

2. **Anna’s Archive**（包含数百万本书籍、论文和漫画）：
   - 使用范围存在法律灰色地带，请谨慎使用

3. **本地文件**：用户自己的 EPUB 或 PDF 文件库

## 阅读状态记录

阅读进度信息会保存在 `~/.openclaw/workspace/memory/reading-state.json` 文件中：

```json
{
  "currentBook": "Thinking, Fast and Slow",
  "file": "/path/to/book.epub",
  "totalPages": 499,
  "pagesRead": 127,
  "lastRead": 1770957900,
  "bookmarks": [50, 200],
  "notes": "Interesting insight about System 1 vs System 2..."
}
```

## 示例工作流程

```bash
# Find the book
./book-reader.sh search "Daniel Kahneman Thinking"

# Download it
./book-reader.sh download 12345 ~/books/thinking-fast-slow.epub

# Start reading
./book-reader.sh read ~/books/thinking-fast-slow.epub --pages 50

# Continue later
./book-reader.sh read ~/books/thinking-fast-slow.epub --pages 50

# Check progress
./book-reader.sh status
```

## 隐私与伦理规范

- 公共领域的书籍（Project Gutenberg）：完全合法
- 有版权保护的书籍：请遵守当地法律法规
- 如发现有价值的书籍，请考虑购买以支持作者
- 仅用于个人学习，禁止进行任何形式的再分发

## 注意事项

- PDF 文件的 OCR 转换质量可能不稳定
- 该工具不支持受数字版权管理（DRM）保护的书籍
- 大型 PDF 文件的解析速度可能较慢
- EPUB 格式的书籍在转换为纯文本时可能存在格式问题

---

**请合理使用该工具，并在可能的情况下支持作者。**