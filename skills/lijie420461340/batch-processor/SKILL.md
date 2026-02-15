---
name: batch-processor
description: **批量处理多个文档，并支持并行执行**
author: claude-office-skills
version: "1.0"
tags: ['batch', 'bulk', 'parallel', 'automation']
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: Custom
  url: https://github.com/claude-office-skills/skills
  stars: N/A
---

# 批量处理技能

## 概述

该技能支持高效地批量处理文档——通过并行执行和进度跟踪，实现对数百个文件进行转换、转换、提取或分析等操作。

## 使用方法

1. 描述您想要完成的任务。
2. 提供所需的输入数据或文件。
3. 我将执行相应的操作。

**示例提示：**
- “将100个PDF文件转换为Word文档”
- “从文件夹中的所有图片中提取文本”
- “批量重命名和组织文件”
- “批量更新文档的页眉/页脚”

## 领域知识


### 批量处理模式


```
Input: [file1, file2, ..., fileN]
         │
         ▼
    ┌─────────────┐
    │  Parallel   │  ← Process multiple files concurrently
    │  Workers    │
    └─────────────┘
         │
         ▼
Output: [result1, result2, ..., resultN]
```

### Python实现


```python
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from tqdm import tqdm

def process_file(file_path: Path) -> dict:
    """Process a single file."""
    # Your processing logic here
    return {"path": str(file_path), "status": "success"}

def batch_process(input_dir: str, pattern: str = "*.*", max_workers: int = 4):
    """Process all matching files in directory."""
    
    files = list(Path(input_dir).glob(pattern))
    results = []
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_file, f): f for f in files}
        
        for future in tqdm(as_completed(futures), total=len(files)):
            file = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append({"path": str(file), "error": str(e)})
    
    return results

# Usage
results = batch_process("/documents/invoices", "*.pdf", max_workers=8)
print(f"Processed {len(results)} files")
```

### 错误处理与恢复


```python
import json
from pathlib import Path

class BatchProcessor:
    def __init__(self, checkpoint_file: str = "checkpoint.json"):
        self.checkpoint_file = checkpoint_file
        self.processed = self._load_checkpoint()
    
    def _load_checkpoint(self):
        if Path(self.checkpoint_file).exists():
            return json.load(open(self.checkpoint_file))
        return {}
    
    def _save_checkpoint(self):
        json.dump(self.processed, open(self.checkpoint_file, "w"))
    
    def process(self, files: list, processor_func):
        for file in files:
            if str(file) in self.processed:
                continue  # Skip already processed
            
            try:
                result = processor_func(file)
                self.processed[str(file)] = {"status": "success", **result}
            except Exception as e:
                self.processed[str(file)] = {"status": "error", "error": str(e)}
            
            self._save_checkpoint()  # Resume-safe
```


## 最佳实践

1. **使用进度条（tqdm）向用户提供反馈**
2. **为耗时较长的任务设置检查点**
3. **设置合理的工作者数量（CPU核心）**
4. **记录失败情况以供后续查看**

## 安装


```bash
# Install required dependencies
pip install python-docx openpyxl python-pptx reportlab jinja2
```

## 资源

- [自定义仓库](https://github.com/claude-office-skills/skills)
- [Claude Office Skills Hub](https://github.com/claude-office-skills/skills)