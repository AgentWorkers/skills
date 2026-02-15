---
name: batch-convert
description: 使用统一的流程批量将文档转换为多种格式
author: claude-office-skills
version: "1.0"
tags: [conversion, batch, automation, pipeline, formats]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
---

# 批量转换文档功能

## 概述

该功能支持使用统一的转换流程，批量将文档从一种格式转换为另一种格式。支持同时转换数百个文件，具有设置一致性、自动格式检测和并行处理等功能，从而实现最高效率。

## 使用方法

1. 指定源文件夹或文件。
2. 选择目标格式。
3. （可选）配置转换选项。
4. 系统会跟踪所有文件的转换进度并进行处理。

**示例命令**：
- “将此文件夹中的所有PDF文件转换为Word文档”。
- “将这些Markdown文件批量转换为PDF和HTML格式”。
- “处理所有Office格式的文件，并将其转换为Markdown格式”。
- “将此文件夹中的所有图片文件合并为一个PDF文件”。

## 相关领域知识

### 支持的格式转换矩阵

| 源格式 | 目标格式：DOCX | 目标格式：PDF | 目标格式：Markdown | 目标格式：HTML | 目标格式：PPTX |
|------|----------|---------|--------|----------|----------|
| DOCX | - | ✅ | ✅ | ✅ | - |
| PDF | ✅ | - | ✅ | ✅ | - |
| Markdown | ✅ | ✅ | - | ✅ | ✅ |
| HTML | ✅ | ✅ | ✅ | - | - |
| XLSX | - | ✅ | ✅ | ✅ | - |
| PPTX | - | ✅ | ✅ | ✅ | - |

### 核心转换流程

```python
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess
import os

class DocumentConverter:
    """Unified document conversion pipeline."""
    
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.converters = {
            ('md', 'docx'): self._md_to_docx,
            ('md', 'pdf'): self._md_to_pdf,
            ('md', 'html'): self._md_to_html,
            ('md', 'pptx'): self._md_to_pptx,
            ('docx', 'pdf'): self._docx_to_pdf,
            ('docx', 'md'): self._docx_to_md,
            ('pdf', 'docx'): self._pdf_to_docx,
            ('pdf', 'md'): self._pdf_to_md,
            ('xlsx', 'pdf'): self._xlsx_to_pdf,
            ('xlsx', 'md'): self._xlsx_to_md,
            ('pptx', 'pdf'): self._pptx_to_pdf,
            ('pptx', 'md'): self._pptx_to_md,
            ('html', 'md'): self._html_to_md,
            ('html', 'pdf'): self._html_to_pdf,
        }
    
    def convert(self, input_path, output_format, output_dir=None):
        """Convert single file to target format."""
        input_path = Path(input_path)
        input_format = input_path.suffix[1:].lower()
        
        if output_dir:
            output_path = Path(output_dir) / f"{input_path.stem}.{output_format}"
        else:
            output_path = input_path.with_suffix(f".{output_format}")
        
        converter_key = (input_format, output_format)
        if converter_key not in self.converters:
            raise ValueError(f"Conversion not supported: {input_format} -> {output_format}")
        
        converter = self.converters[converter_key]
        return converter(input_path, output_path)
    
    def batch_convert(self, input_dir, output_format, output_dir=None, 
                      file_pattern="*", recursive=False):
        """Batch convert all matching files."""
        input_path = Path(input_dir)
        output_path = Path(output_dir) if output_dir else input_path / "converted"
        output_path.mkdir(exist_ok=True)
        
        # Find files
        if recursive:
            files = list(input_path.rglob(file_pattern))
        else:
            files = list(input_path.glob(file_pattern))
        
        # Filter to supported formats
        supported_ext = ['.md', '.docx', '.pdf', '.xlsx', '.pptx', '.html']
        files = [f for f in files if f.suffix.lower() in supported_ext]
        
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_file = {
                executor.submit(self.convert, f, output_format, output_path): f
                for f in files
            }
            
            for future in as_completed(future_to_file):
                file = future_to_file[future]
                try:
                    result = future.result()
                    results.append({'file': str(file), 'status': 'success', 'output': str(result)})
                except Exception as e:
                    results.append({'file': str(file), 'status': 'error', 'error': str(e)})
        
        return results
```

### 转换器实现细节

```python
# Markdown conversions (using Pandoc)
def _md_to_docx(self, input_path, output_path):
    subprocess.run(['pandoc', str(input_path), '-o', str(output_path)], check=True)
    return output_path

def _md_to_pdf(self, input_path, output_path):
    subprocess.run(['pandoc', str(input_path), '-o', str(output_path)], check=True)
    return output_path

def _md_to_html(self, input_path, output_path):
    subprocess.run(['pandoc', str(input_path), '-s', '-o', str(output_path)], check=True)
    return output_path

def _md_to_pptx(self, input_path, output_path):
    subprocess.run(['marp', str(input_path), '-o', str(output_path)], check=True)
    return output_path

# Office to Markdown (using markitdown)
def _docx_to_md(self, input_path, output_path):
    from markitdown import MarkItDown
    md = MarkItDown()
    result = md.convert(str(input_path))
    with open(output_path, 'w') as f:
        f.write(result.text_content)
    return output_path

def _xlsx_to_md(self, input_path, output_path):
    from markitdown import MarkItDown
    md = MarkItDown()
    result = md.convert(str(input_path))
    with open(output_path, 'w') as f:
        f.write(result.text_content)
    return output_path

def _pptx_to_md(self, input_path, output_path):
    from markitdown import MarkItDown
    md = MarkItDown()
    result = md.convert(str(input_path))
    with open(output_path, 'w') as f:
        f.write(result.text_content)
    return output_path

# PDF conversions
def _pdf_to_docx(self, input_path, output_path):
    from pdf2docx import Converter
    cv = Converter(str(input_path))
    cv.convert(str(output_path))
    cv.close()
    return output_path

def _pdf_to_md(self, input_path, output_path):
    from markitdown import MarkItDown
    md = MarkItDown()
    result = md.convert(str(input_path))
    with open(output_path, 'w') as f:
        f.write(result.text_content)
    return output_path

# Office to PDF (using LibreOffice)
def _docx_to_pdf(self, input_path, output_path):
    subprocess.run([
        'soffice', '--headless', '--convert-to', 'pdf',
        '--outdir', str(output_path.parent), str(input_path)
    ], check=True)
    return output_path

def _xlsx_to_pdf(self, input_path, output_path):
    subprocess.run([
        'soffice', '--headless', '--convert-to', 'pdf',
        '--outdir', str(output_path.parent), str(input_path)
    ], check=True)
    return output_path

def _pptx_to_pdf(self, input_path, output_path):
    subprocess.run([
        'soffice', '--headless', '--convert-to', 'pdf',
        '--outdir', str(output_path.parent), str(input_path)
    ], check=True)
    return output_path
```

### 进度跟踪机制

```python
from tqdm import tqdm

def batch_convert_with_progress(converter, input_dir, output_format, output_dir=None):
    """Batch convert with progress bar."""
    input_path = Path(input_dir)
    files = list(input_path.glob('*'))
    
    results = []
    for file in tqdm(files, desc=f"Converting to {output_format}"):
        try:
            result = converter.convert(file, output_format, output_dir)
            results.append({'file': str(file), 'status': 'success'})
        except Exception as e:
            results.append({'file': str(file), 'status': 'error', 'error': str(e)})
    
    return results
```

## 使用建议

1. **先测试样本文件**：在批量转换前先转换少量文件以确保转换正确。
2. **检查磁盘空间**：确保有足够的存储空间用于存放转换后的文件。
3. **使用并行处理**：通过多线程加速转换速度。
4. **优雅地处理错误**：记录错误信息并继续执行其他文件的转换。
5. **验证转换结果**：抽查部分转换后的文件以确保质量。

## 常见应用场景

- **文档导出**：将多种格式的文档统一转换为标准格式。
- **旧版文档迁移**：将旧格式的文档转换为现代格式。
- **报告生成**：自动生成各种格式的报告。

## 注意事项

- **部分格式组合可能不受支持**。
- 复杂的格式设置可能在转换过程中丢失。
- 大文件可能需要更长的转换时间。
- 某些格式的转换可能需要依赖外部工具（如LibreOffice、Pandoc）。
- 转换后的文档质量会受到源文档复杂度的影响。

## 安装说明

```bash
# Core dependencies
pip install pdf2docx markitdown python-docx openpyxl

# Pandoc (for MD conversions)
brew install pandoc  # macOS
apt install pandoc   # Ubuntu

# Marp (for PPTX)
npm install -g @marp-team/marp-cli

# LibreOffice (for Office formats)
brew install libreoffice  # macOS
apt install libreoffice   # Ubuntu
```

## 参考资源

- [Pandoc官方文档](https://pandoc.org/MANUAL.html)
- [Markitdown项目GitHub页面](https://github.com/microsoft/markitdown)
- [pdf2docx转换工具文档](https://pdf2docx.readthedocs.io/)
- [LibreOffice命令行工具指南](https://help.libreoffice.org/latest/en-US/text/shared/guide/start_parameters.html)