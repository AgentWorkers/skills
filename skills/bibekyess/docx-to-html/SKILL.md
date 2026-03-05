---
name: docx-to-html
description: "每当用户拥有一个 DOCX 文件（.docx）并希望对其进行转换、阅读、查看、提取内容或以任何方式处理它（包括总结、在浏览器中显示、提取表格或列表，或将文件数据输入到 AI 流程中）时，请使用此技能。对于任何涉及 DOCX 文件的任务，即使请求看起来很简单，也请始终使用此技能。触发条件包括：'convert docx'、'open word file'、'read word document'、'extract tables from docx'，或任何提及 DOCX 文件名的操作。"
---
# DOCX 到 HTML 转换器

该技能提供了一种简单的方法，可以将 Microsoft Word (.docx) 文档转换为结构清晰、语义丰富的 HTML，使其适用于各种基于 Web 和 AI 的应用程序。

## 兼容性

- **Python 3**（用于转换封装脚本）
- **安装了 `mammoth` 的 Node.js**（核心转换引擎）

要安装 Node.js 依赖项，请从 `scripts/` 目录运行以下命令：
```bash
npm install
```

## 使用场景

- **基于浏览器的查看**：将 DOCX 文档转换为可在浏览器中显示的格式，而无需安装 Microsoft Word。
- **适用于 AI 的内容**：为大型语言模型（LLM）准备 DOCX 内容，用于摘要、问答和语义搜索等任务。
- **Web 集成**：将 Word 文档内容集成到 Web 应用程序、内容管理系统（CMS）或在线编辑器中。
- **数据提取**：从 DOCX 文件中提取结构化数据（表格、列表、标题）以用于自动化报告和分析。
- **搜索和索引**：通过将 DOCX 内容转换为易于索引的 HTML，实现全文搜索和矢量搜索。

## 工作流程

1. **定位 DOCX 文件**：确定要转换的 `.docx` 文件的路径。
2. **运行转换脚本**：从技能的 `scripts/` 目录执行 Python 封装脚本：
   ```bash
   python3 <skill-dir>/scripts/convert.py <input_path.docx> <output_path.html>
   ```
   请将 `<skill-dir>` 替换为实际安装此技能的路径。

3. **验证输出**：在浏览器中打开生成的 `.html` 文件并检查：
   - 标题（`<h1>`、`<h2>` 等）以正确的层次结构显示
   - 表格按预期显示行和列
   - 列表以项目符号或编号项的形式显示（而不是纯文本）
   - 粗体、斜体和内联格式得到保留
   - 图片可见（默认情况下以 base64 格式嵌入）

4. **处理 HTML**：使用生成的 HTML 进行进一步处理，如摘要、索引或显示。

## 搭配资源

- `scripts/docx-converter.js`：使用 `mammoth.js` 的核心 Node.js 转换逻辑。
- `scripts/convert.py`：用于调用 Node.js 转换器的 Python 封装脚本。
- `scripts/package.json`：Node.js 依赖项清单（包含 `mammoth`）。

## 技术细节

该转换过程依赖于 `mammoth.js`，它优先考虑文档的语义含义而非视觉呈现：

- **语义转换**：文档结构被映射到相应的 HTML 标签中——标题变为 `<h1>`/`<h2>`，列表变为 `<ul>`/`<ol>` 等。
- **基本样式**：粗体、斜体和常见的段落样式得到保留。
- **图片嵌入**：图片被提取并以 base64 数据 URI 的形式嵌入到 HTML 输出中。

## 故障排除

| 问题 | 可能原因 | 解决方法 |
|---|---|---|
| `node: command not found` | 未安装 Node.js | 安装 Node.js（版本 16 或更高） |
| `Cannot find module 'mammoth'` | npm 依赖项缺失 | 在 `scripts/` 目录中运行 `npm install` |
| 输出为空或混乱 | DOCX 文件损坏或受密码保护 | 尝试重新从 Microsoft Word 保存文件 |
| 图片缺失 | 嵌入的图片过大 | 查看 `docx-converter.js` 中 `mammoth.js` 对图片大小的限制 |

## 限制

- 原始 DOCX 文件中的高级或特定样式可能无法在 HTML 输出中完美再现。
- 如跟踪更改、注释或复杂布局元素等功能可能会被简化或省略。