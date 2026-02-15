---
name: pdf-process-mineru
description: 基于本地 MinerU 的 PDF 文档解析工具，支持将 PDF 文件转换为 Markdown、JSON 以及其他机器可读的格式。
---

## 工具列表

### 1. pdf_to_markdown

将 PDF 文档转换为 Markdown 格式，同时保留文档结构、公式、表格和图片。

**描述**：使用 MinerU 对 PDF 文档进行解析，并以 Markdown 格式输出，支持 OCR、公式识别、表格提取等功能。

**参数**：
- `file_path` (字符串，必填)：PDF 文件的绝对路径
- `output_dir` (字符串，必填)：输出目录的绝对路径
- `backend` (字符串，可选)：解析后端，可选值：`hybrid-auto-engine`（默认）、`pipeline`、`vlm-auto-engine`
- `language` (字符串，可选)：OCR 语言代码，例如 `en`（英语）、`ch`（中文）、`ja`（日语）等，默认为自动检测
- `enable_formula` (布尔值，可选)：是否启用公式识别，默认为 `true`
- `enable_table` (布尔值，可选)：是否启用表格提取，默认为 `true`
- `start_page` (整数，可选)：起始页码（从 0 开始），默认为 0
- `end_page` (整数，可选)：结束页码（从 0 开始），默认为 `-1` 表示解析所有页面

**返回值**：
```json
{
  "success": true,
  "output_path": "/path/to/output",
  "markdown_content": "Converted Markdown content...",
  "images": ["List of image paths"],
  "tables": ["List of table information"],
  "formula_count": 10
}
```

**示例**：
```bash
python .claude/skills/pdf-process/script/pdf_parser.py \
  '{"name": "pdf_to_markdown", "arguments": {"file_path": "/path/to/document.pdf", "output_dir": "/path/to/output"}}'

# Use specific backend
python .claude/skills/pdf-process/script/pdf_parser.py \
  '{"name": "pdf_to_markdown", "arguments": {"file_path": "/path/to/document.pdf", "output_dir": "/path/to/output", "backend": "pipeline"}}'

# Parse specific pages
python .claude/skills/pdf-process/script/pdf_parser.py \
  '{"name": "pdf_to_markdown", "arguments": {"file_path": "/path/to/document.pdf", "output_dir": "/path/to/output", "start_page": 0, "end_page": 5}}'
```

---

### 2. pdf_to_json

将 PDF 文档转换为 JSON 格式，包含详细的布局和结构信息。

**描述**：使用 MinerU 对 PDF 文档进行解析，并以 JSON 格式输出，其中包含文本块、图片、表格、公式等结构化信息。

**参数**：
- `file_path` (字符串，必填)：PDF 文件的绝对路径
- `output_dir` (字符串，必填)：输出目录的绝对路径
- `backend` (字符串，可选)：解析后端，可选值：`hybrid-auto-engine`（默认）、`pipeline`、`vlm-auto-engine`
- `language` (字符串，可选)：OCR 语言代码，例如 `en`（英语）、`ch`（中文）、`ja`（日语）等，默认为自动检测
- `enable_formula` (布尔值，可选)：是否启用公式识别，默认为 `true`
- `enable_table` (布尔值，可选)：是否启用表格提取，默认为 `true`
- `start_page` (整数，可选)：起始页码（从 0 开始），默认为 0
- `end_page` (整数，可选)：结束页码（从 0 开始），默认为 `-1` 表示解析所有页面

**返回值**：
```json
{
  "success": true,
  "output_path": "/path/to/output.json",
  "pages": [
    {
      "page_no": 0,
      "page_size": [595, 842],
      "blocks": [
        {
          "type": "text",
          "text": "Text content",
          "bbox": [x, y, x, y]
        }
      ],
      "images": [],
      "tables": [],
      "formulas": []
    }
  ],
  "metadata": {
    "total_pages": 10,
    "author": "Author",
    "title": "Title"
  }
}
```

**示例**：
```bash
python .claude/skills/pdf-process/script/pdf_parser.py \
  '{"name": "pdf_to_json", "arguments": {"file_path": "/path/to/document.pdf", "output_dir": "/path/to/output"}}'

# Use specific backend and language
python .claude/skills/pdf-process/script/pdf_parser.py \
  '{"name": "pdf_to_json", "arguments": {"file_path": "/path/to/document.pdf", "output_dir": "/path/to/output", "backend": "hybrid-auto-engine", "language": "ch"}}'
```

---

## 安装说明

### 1. 安装 MinerU

```bash
# Update pip and install uv
pip install --upgrade pip
pip install uv

# Install MinerU (including all features)
uv pip install -U "mineru[all]"
```

### 2. 验证安装

```bash
# Check if MinerU is installed successfully
mineru --version

# Test basic functionality
mineru --help
```

### 3. 系统要求

- **Python 版本**：3.10-3.13
- **操作系统**：Linux / Windows / macOS 14.0+
- **内存**：
  - 使用 `pipeline` 后端：至少需要 16GB 内存，建议使用 32GB 或更多
  - 使用 `hybrid/vlm` 后端：至少需要 16GB 内存，建议使用 32GB 或更多
- **磁盘空间**：至少需要 20GB（建议使用 SSD）
- **GPU**（可选）：
  - `pipeline` 后端：支持仅使用 CPU
  - `hybrid/vlm` 后端：需要 NVIDIA GPU（Volta 架构及以上）或 Apple Silicon

## 使用场景

1. **学术论文解析**：提取公式、表格和图片等结构化内容
2. **技术文档转换**：将 PDF 文档转换为 Markdown 格式以便版本控制和在线发布
3. **OCR 处理**：处理扫描的 PDF 文件和损坏的 PDF 文件
4. **多语言文档**：支持 109 种语言的 OCR 识别
5. **批量处理**：批量转换多个 PDF 文档

## 后端选择建议

- **hybrid-auto-engine**（默认）：准确性和速度平衡，适用于大多数场景
- **pipeline**：适用于仅使用 CPU 的环境，兼容性最佳
- **vlm-auto-engine**：准确率最高，需要 GPU 加速

## 注意事项

1. **文件路径**：所有路径必须是绝对路径
2. **输出目录**：如果目录不存在，系统会自动创建该目录
3. **性能**：使用 GPU 可显著提高解析速度
4. **页码**：页码从 0 开始计数
5. **内存**：处理大型文档时可能会消耗更多内存

## 故障排除

### 常见问题

1. **安装失败**：
   - 确保使用 Python 3.10-3.13
   - Windows 仅支持 Python 3.10-3.12（ray 不支持 3.13）
   - 使用 `uv pip install` 可以解决大多数依赖项冲突

2. **内存不足**：
   - 使用 `pipeline` 后端
   - 限制解析页码范围（通过 `start_page` 和 `end_page` 参数）
   - 减少虚拟内存分配

3. **解析速度慢**：
   - 启用 GPU 加速
   - 使用 `hybrid-auto-engine` 后端
   - 关闭不必要的功能（如公式识别、表格提取）

4. **OCR 准确率低**：
   - 指定正确的文档语言
   - 确保所选后端支持 OCR（使用 `pipeline` 或 `hybrid-*` 后端）

## 相关资源

- MinerU 官方文档：https://opendatalab.github.io/MinerU/
- MinerU GitHub 仓库：https://github.com/opendatalab/MinerU
- 在线演示：https://mineru.net/