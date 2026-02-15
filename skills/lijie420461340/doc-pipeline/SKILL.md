---
name: doc-pipeline
description: 将文档操作链转换为可重用的管道（pipelines）
author: claude-office-skills
version: "1.0"
tags: ['pipeline', 'workflow', 'chain', 'automation']
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: Custom
  url: https://github.com/claude-office-skills/skills
  stars: N/A
---

# 文档处理管道技能（Doc Pipeline Skill）

## 概述

该技能用于构建文档处理管道，即通过将多个操作（如提取、转换、格式化等）串联起来，形成一个可重用的工作流程，实现数据在各处理阶段之间的顺畅流动。

## 使用方法

1. 描述您想要完成的目标。
2. 提供所需的输入数据或文件。
3. 我将执行相应的操作。

**示例提示：**
- “PDF → 提取文本 → 翻译 → 生成 DOCX 文件”
- “图片 → 光学字符识别（OCR） → 摘要生成 → 创建报告”
- “Excel 文件 → 分析数据 → 生成图表 → 创建 PowerPoint 演示文稿”
- “多个输入文件 → 合并 → 格式化 → 输出结果”

## 相关领域知识

### 管道架构（Pipeline Architecture）

```
Stage 1      Stage 2      Stage 3      Stage 4
┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐
│Extract│ → │Transform│ → │ AI   │ → │Output│
│ PDF  │    │  Data  │    │Analyze│   │ DOCX │
└──────┘    └──────┘    └──────┘    └──────┘
     │           │           │           │
     └───────────┴───────────┴───────────┘
                 Data Flow
```

### 管道专用语言（Pipeline DSL）

```yaml
# pipeline.yaml
name: contract-review-pipeline
description: Extract, analyze, and report on contracts

stages:
  - name: extract
    operation: pdf-extraction
    input: $input_file
    output: $extracted_text
    
  - name: analyze
    operation: ai-analyze
    input: $extracted_text
    prompt: "Review this contract for risks..."
    output: $analysis
    
  - name: report
    operation: docx-generation
    input: $analysis
    template: templates/review_report.docx
    output: $output_file
```

### Python 实现方式

```python
from typing import Callable, Any
from dataclasses import dataclass

@dataclass
class Stage:
    name: str
    operation: Callable
    
class Pipeline:
    def __init__(self, name: str):
        self.name = name
        self.stages: list[Stage] = []
    
    def add_stage(self, name: str, operation: Callable):
        self.stages.append(Stage(name, operation))
        return self  # Fluent API
    
    def run(self, input_data: Any) -> Any:
        data = input_data
        for stage in self.stages:
            print(f"Running stage: {stage.name}")
            data = stage.operation(data)
        return data

# Example usage
pipeline = Pipeline("contract-review")
pipeline.add_stage("extract", extract_pdf_text)
pipeline.add_stage("analyze", analyze_with_ai)
pipeline.add_stage("generate", create_docx_report)

result = pipeline.run("/path/to/contract.pdf")
```

### 高级功能：条件化管道（Advanced: Conditional Pipelines）

```python
class ConditionalPipeline(Pipeline):
    def add_conditional_stage(self, name: str, condition: Callable, 
                               if_true: Callable, if_false: Callable):
        def conditional_op(data):
            if condition(data):
                return if_true(data)
            return if_false(data)
        return self.add_stage(name, conditional_op)

# Usage
pipeline.add_conditional_stage(
    "ocr_if_needed",
    condition=lambda d: d.get("has_images"),
    if_true=run_ocr,
    if_false=lambda d: d
)
```

## 最佳实践

1. **确保每个处理阶段只负责一项具体任务（单一职责原则）**
2. **使用中间输出结果以便于调试**
3. **为每个处理阶段实现错误处理机制**
4. **通过 YAML/JSON 等格式化配置管道的运行参数**

## 安装方法

```bash
# Install required dependencies
pip install python-docx openpyxl python-pptx reportlab jinja2
```

## 资源链接

- [自定义代码仓库](https://github.com/claude-office-skills/skills)
- [Claude Office Skills 中心](https://github.com/claude-office-skills/skills)