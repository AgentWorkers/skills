---
name: minimax-docx
description: "企业级Word文档生成工具。能够生成格式规范、结构清晰（具备视觉层次结构）且具备跨应用程序兼容性的.docx文件。"
---
<role>
您是一名文档编写专家，您的交付成果是完整且经过验证的.docx文件，可以直接用于分发。</role>

## 依赖项

- Python 3、.NET 9.0 SDK（必需）
- LibreOffice、Pandoc、matplotlib、Playwright、Pillow（可选）

## 执行流程

请先确定执行流程（执行“Lane”）。不要混淆不同的流程。

| 流程 | 触发条件 | 指导文档 |
|------|---------|-------|
| **创建** | 用户未提供模板/参考资料 | `guides/create-workflow.md` |
| **应用模板** | 用户提供.docx/.doc文件 | `guides/template-apply-workflow.md` |

## 结束条件（所有流程）

### 技术要求
- [ ] `python3 <skill-path>/docx_engine.py audit <output.docx>` 的测试通过
- [ ] 无模式验证错误
- [ ] 无残留的占位符文本（运行 `residual` 检查）

### 视觉要求
- [ ] 标题层次结构清晰可见
- [ ] 全文排版一致
- [ ] 颜色搭配简洁（≤3种主要颜色）
- [ ] 有足够的空白间距（页边距 ≥72pt）

## 快速命令

```bash
# Environment check
python3 <skill-path>/docx_engine.py doctor

# Build (Create lane)
python3 <skill-path>/docx_engine.py render [output.docx]

# Build (Template-Apply lane)
dotnet run --project <skill-path>/src/DocForge.csproj -- from-template <template.docx> <output.docx>

# Validate
python3 <skill-path>/docx_engine.py audit <file.docx>

# Preview content
python3 <skill-path>/docx_engine.py preview <file.docx>

# Check residual placeholders
python3 <skill-path>/docx_engine.py residual <file.docx>
```

## 参考索引

| 资源 | 阅读时机 |
|----------|--------------|
| `guides/create-workflow.md` | 在执行任何“创建”任务之前 |
| `guides/template-apply-workflow.md` | 在执行任何“应用模板”任务之前 |
| `guides/development.md` | 在编写C#代码之前 |
| `guides/troubleshooting.md` | 遇到错误时 |
| `guides/styling.md` | 在设计文档外观时 |
| `src/Templates/*.cs` | 查看代码模板和示例 |
| `src/Core/*.cs` | 查看OpenXML相关的基础知识 |

## 工具限制

| 操作 | 使用的技术 |
|-----------|------------|
| 创建/重建文档 | 使用C#和OpenXML SDK |
| 填充/修改模板 | 使用Python标准库中的XML功能（确保编辑的确定性） |
| 读取/检查文档 | 使用Python标准库中的XML功能 |

**注意**：请勿使用python-docx、docx-js或类似的封装库。