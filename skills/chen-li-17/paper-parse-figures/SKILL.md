---
name: paper-parse
description: 将学术PDF论文解析为Markdown格式，并提取其中的图表。
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "requires": { "bins": ["uv"] },
      },
  }
---
# Paper Parse

使用 PyMuPDF 将学术 PDF 论文解析为结构化的 Markdown 格式，并提取其中的图表。

## 使用方法

```bash
uv run {baseDir}/scripts/parse_paper.py --pdf /path/to/paper.pdf [--output-dir ./output]
```

## 输出结果

该工具会生成以下文件：

- `{paper_name}_content.md`：完整的论文内容（Markdown 格式）
- `{paper_name}_parsed.json`：结构化的元数据，包括：
  - 论文标题
  - 页数
  - 提取的图表（附带图例和文件路径）
- `cover_title_authors.png`：首页截图（突出显示标题和作者信息）
- `figures/`：包含高分辨率图表截图的目录

## 示例

```bash
uv run scripts/parse_paper.py --pdf ~/papers/my-paper.pdf --output-dir ./parsed
```

输出文件结构：
```
./parsed/
├── my-paper_content.md
├── my-paper_parsed.json
└── figures/
    ├── figure_1.png
    ├── figure_2.png
    └── ...
```

## 所需依赖库

- PyMuPDF (fitz)：用于 PDF 的解析和渲染
- pymupdf4llm：用于将 PDF 转换为 Markdown 格式

这些依赖库会通过 uv 工具中的内联脚本自动进行管理。