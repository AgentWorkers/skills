---
name: pdfagent
description: 自托管的PDF处理及转换服务，支持按使用量计费的输出方式。
version: 0.1.0
---
# PDF Agent

**概述**  
`pdfagent` 是一个用于执行 PDF 操作的工具（合并、分割、压缩、转换、OCR 等），并会详细记录操作过程中的使用情况（如执行时间等）。  
该工具非常适合在本地环境中进行自托管处理，因为输入文件和输出文件都需要保存在磁盘上。  
`pdfagent` 的源代码位于 `pdfagent/` 目录下，可通过 `uv run` 命令从 `scripts/pdfagent_cli.py` 文件中执行（无需通过 PyPI 发布）。  

**系统要求**  
- 确保已安装 `uv` 并将其添加到系统的 `PATH` 环境变量中。  
- 根据具体命令的需求，还需要安装以下系统工具：`qpdf`、`ghostscript`、`poppler`（用于 `pdftoppm`）、`libreoffice`、`chromium`（用于将 HTML 文件转换为 PDF）以及 `ocrmypdf`。  

**核心用法**  
- **合并 PDF 文件并记录使用情况：**  
  `uv run {baseDir}/scripts/pdfagent_cli.py merge file1.pdf file2.pdf --out merged.pdf --json`  

- **按指定范围分割 PDF 文件：**  
  `uv run {baseDir}/scripts/pdfagent_cli.py split input.pdf --range "1-3,5" --out-dir out_dir --json`  

- **使用预设设置压缩 PDF 文件：**  
  `uv run {baseDir}/scripts/pdfagent_cli.py compress input.pdf --preset ebook --out compressed.pdf --json`  

- **将图像转换为 PDF 文件：**  
  `uv run {baseDir}/scripts/pdfagent_cli.py jpg-to-pdf image1.jpg image2.png --out output.pdf --json`  

- **对扫描后的 PDF 文件进行 OCR 处理：**  
  `uv run {baseDir}/scripts/pdfagent_cli.py ocr scan.pdf --lang eng --out scan_ocr.pdf --json`  

- **支持多步骤操作的代理模式：**  
  `uv run {baseDir}/scripts/pdfagent_cli.py agent "merge then rotate 90 degrees every other page" -i file1.pdf -i file2.pdf --out out.pdf --json`  

- **检查依赖项及二进制文件是否可用：**  
  `uv run {baseDir}/scripts/pdfagent_cli.py doctor --json`  

**注意事项**  
- 使用 `--json` 选项可生成机器可读的输出格式（包含操作详细信息和输出文件信息）。  
- 对于加密的 PDF 文件，可以通过 `--password` 或为每个文件指定 `--passwords` 参数来解密。  
- 如果某些转换工具缺失，`pdfagent` 会使用默认的替代路径，并在输出或日志中提示这一点。  
- 部分命令可能需要额外的 Python 库作为依赖项：  
  `uv run --with pdf2docx --with camelot-py[cv] --with pdfplumber --with pyhanko {baseDir}/scripts/pdfagent_cli.py <command> ...`