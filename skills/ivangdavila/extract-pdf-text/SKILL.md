---
name: Extract PDF Text
slug: extract-pdf-text
version: 1.0.2
homepage: https://clawic.com/skills/extract-pdf-text
description: 使用 PyMuPDF 从 PDF 文件中提取文本。能够解析表格、表单以及复杂的页面布局。支持对扫描文档进行光学字符识别（OCR）处理。
changelog: Remove internal build file that was accidentally included
metadata: {"clawdbot":{"emoji":"📄","requires":{"bins":["python3"],"pip":["pymupdf"]},"os":["linux","darwin","win32"],"install":[{"id":"pymupdf","kind":"pip","package":"PyMuPDF","label":"Install PyMuPDF"}]}}
---
## 使用场景

当需要从PDF文件中提取文本时，可以使用PyMuPDF（旧称：fitz）来实现快速、高效的本地文本提取。该工具适用于基于文本的文档、经过OCR处理的扫描页面、表单以及具有复杂布局的PDF文件。

## 快速参考

| 主题 | 文件名 |
|-------|------|
| 代码示例 | `examples.md` |
| OCR设置 | `ocr.md` |
| 故障排除 | `troubleshooting.md` |

## 核心规则

### 1. 先安装PyMuPDF

```bash
pip install PyMuPDF
```

导入方式：使用`fitz`（PyMuPDF的旧称）：
```python
import fitz  # PyMuPDF
```

### 2. 基本文本提取方法

```python
import fitz

doc = fitz.open("document.pdf")
text = ""
for page in doc:
    text += page.get_text()
doc.close()
```

### 3. 选择合适的方法

| PDF类型 | 提取方法 |
|----------|--------|
| 基于文本的PDF | `page.get_text()` — 速度快、准确率高 |
| 经过OCR处理的PDF | 使用pytesseract进行OCR处理 — 效率较低 |
| 混合类型的PDF | 需要逐页检查，并在必要时使用OCR |

### 4. 在使用OCR之前先检查是否有可提取的文本

```python
def needs_ocr(page):
    text = page.get_text().strip()
    return len(text) < 50  # Likely scanned if very little text
```

### 5. 优雅地处理错误

```python
try:
    doc = fitz.open(path)
except fitz.FileDataError:
    print("Invalid or corrupted PDF")
except fitz.PasswordError:
    doc = fitz.open(path, password="secret")
```

## 常见问题及解决方法

| 问题 | 原因 | 解决方案 |
|------|--------------|-----|
| 对纯文本PDF使用OCR | 处理速度慢且准确率低 | 先尝试使用`page.get_text()`方法 |
| 忘记关闭PDF文件 | 导致内存泄漏 | 使用`with`语句或`doc.close()`关闭文件 |
| 假设页面顺序正确 | 读取顺序错误 | 在`page.get_text()`方法中设置`sort=True`参数 |
| 忽略文件编码 | 文本显示乱码 | PyMuPDF支持UTF-8编码 |

## 使用范围

本文档提供了使用PyMuPDF提取PDF文本的详细步骤。

**注意：**  
- 本文档仅提供PyMuPDF的代码示例及OCR设置说明，不涉及其他高级功能。  
- 不会未经用户许可访问文件，也不会将数据发送到外部系统，也不会修改原始PDF文件。  

## 安全性与隐私保护

**所有处理操作均在本地完成：**  
- PyMuPDF完全在您的设备上运行，不会发起任何外部API调用，也不会将数据传输到外部服务器。  

## 输出格式

- **纯文本**  
- **结构化数据（字典格式）**  
- **JSON格式**  

## 完整示例代码

```python
import fitz

def extract_pdf(path):
    """Extract text from PDF, with OCR fallback for scanned pages."""
    doc = fitz.open(path)
    results = []
    
    for i, page in enumerate(doc):
        text = page.get_text()
        method = "text"
        
        # If very little text, might be scanned
        if len(text.strip()) < 50:
            # OCR would go here (see ocr.md)
            method = "needs_ocr"
        
        results.append({
            "page": i + 1,
            "text": text,
            "method": method
        })
    
    doc.close()
    return {
        "pages": len(results),
        "content": results,
        "word_count": sum(len(r["text"].split()) for r in results)
    }

# Usage
result = extract_pdf("document.pdf")
print(f"Extracted {result['word_count']} words from {result['pages']} pages")
```

## 反馈建议：  
- 如果本文档对您有帮助，请在ClawHub上点赞（star）：`clawhub star extract-pdf-text`  
- 如需获取最新更新，请执行`clawhub sync`命令。