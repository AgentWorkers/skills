# OpenClaw的PDF阅读器技能

使用PyMuPDF从PDF文件中提取并读取文本。

## 安装

```powershell
pip install pymupdf
```

## 使用方法

```powershell
# Extract text (first 10 pages by default)
python pdf_reader.py "path/to/file.pdf" 10

# Output to JSON file (for reading)
python pdf_reader.py "path/to/file.pdf" 10 --output=extracted.json

# Read specific number of pages
python pdf_reader.py "path/to/file.pdf" 5
```

## 主要功能

- 从任何PDF文件中提取文本
- 支持处理大型文件
- 生成JSON格式的输出文件，便于AI模型读取
- 解决编码相关问题
- 显示文件的元数据（如标题、作者等）

## 安全限制

为确保安全，该脚本有以下限制：
- **输入文件：** 必须是当前工作目录下的`.pdf`文件
- **输出文件：** 必须是当前工作目录下的`.json`文件
- 不允许使用相对路径（如`../`）进行文件操作
- 文件的读写操作仅限于脚本运行的目录内

## 相关文件

- `pdf_reader.py` - 主要的Python脚本
- `SKILL.md` - 本文档文件