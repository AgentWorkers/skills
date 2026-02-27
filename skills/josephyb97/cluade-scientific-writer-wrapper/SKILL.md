---
name: scientific-writer
description: 这款由人工智能驱动的科学写作工具能够生成可用于发表的论文、科研资助申请、海报等文档。它整合了实时的研究数据以及经过验证的引用信息，帮助用户提升写作质量。
metadata:
  {
    "openclaw": {
      "emoji": "🔬",
      "requires": {
        "bins": ["python3", "pip"],
        "env": ["ANTHROPIC_API_KEY"]
      }
    }
  }
---
# Scientific Writer

这是一款基于人工智能的科学写作工具，它将深入的研究成果与格式规范的输出内容相结合。

## 安装

```bash
pip install scientific-writer
```

## 先决条件

- Python 3.10-3.12
- ANTHROPIC_API_KEY（必需）
- OPENROUTER_API_KEY（用于研究查询，可选）

设置 API 密钥：
```bash
export ANTHROPIC_API_KEY='your_key'
# or create .env file
echo "ANTHROPIC_API_KEY=your_key" > .env
```

## 使用方法

### 作为 Python API 使用

```python
import asyncio
from scientific_writer import generate_paper

async def main():
    async for update in generate_paper(
        query="Create a Nature paper on CRISPR gene editing...",
        data_files=["editing_efficiency.csv", "western_blot.png"]
    ):
        if update["type"] == "progress":
            print(f"[{update['stage']}] {update['message']}")
        else:
            print(f"✓ PDF: {update['files']['pdf_final']}")

asyncio.run(main())
```

### 通过 OpenClaw 执行

```bash
# Run scientific writer
python3 -c "
import asyncio
from scientific_writer import generate_paper

async def main():
    async for update in generate_paper(
        query='Create a paper on your topic...',
        data_files=[]
    ):
        print(update)

asyncio.run(main())
"
```

## 可用的功能（当作为插件使用时）

- `scientific-schematics` - 人工智能绘图功能（用于生成图表，支持 CONSORT、神经网络等模型）
- `research-lookup` - 实时文献搜索
- `peer-review` - 系统化的手稿评估服务
- `citation-management` - 文献引用管理（支持 BibTeX 格式）
- `clinical-reports` - 医学报告生成
- `research-grants` - 提供 NSF、NIH、DOE 等机构的科研基金申请支持
- `scientific-slides` - 科研报告幻灯片制作
- `latex-posters` - 会议海报生成
- `hypothesis-generation` - 科学假设的辅助生成工具

## 输出结果

- 科学论文（符合 Nature、Science、NeurIPS 等期刊的格式）
- 科研基金申请书（NSF、NIH、DOE 等机构要求的格式）
- 会议海报（LaTeX 格式）
- 文献综述
- 医学报告

## 注意事项

- 使用该工具需要 ANTHROPIC_API_KEY。
- 请将数据文件保存在 `data/` 文件夹中（图片文件存放在 `figures/` 子文件夹中，其他数据文件存放在 `data/` 子文件夹中）。
- 所有输出结果将保存在 `writing_outputs/` 文件夹中。