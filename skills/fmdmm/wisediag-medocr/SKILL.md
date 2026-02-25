---
name: wisediag-medocr
description: "使用 WiseDiag MedOcr API 将 PDF 文件转换为 Markdown 格式。该 API 支持表格识别、多列布局以及医学文档的 OCR（光学字符识别）功能。使用方法：上传 PDF 文件，然后输入 “Use MedOcr to process this” 来启动转换过程。"
registry:
  homepage: https://github.com/wisediag/medocr-skill
  author: WiseDiag
  credentials:
    required: true
    env_vars:
      - WISEDIAG_API_KEY
---
# WiseDiag MedOcr 技能

该技能可将 PDF 文件转换为 Markdown 格式。脚本负责处理 API 认证、文件上传、OCR 处理，并自动保存结果。

## ⚠️ 重要提示：如何使用此技能

**必须使用提供的脚本来处理文件。** **请勿直接调用任何 API 或 HTTP 端点。**

`scripts/medocr.py` 脚本负责所有操作：
- API 认证（从环境变量中读取 `WISEDIAG_API_KEY`）
- PDF 上传及 OCR 处理
- 将 Markdown 结果保存到 `WiseDiag-MedOcr-1.0.0/{filename}.md` 文件中

## 🔑 API 密钥设置（必需）

**获取您的 API 密钥：**
👉 https://chat.wisediag.com/apiKeyManage

```bash
export WISEDIAG_API_KEY=your_api_key
```

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

**要处理 PDF 文件，请运行：**

```bash
cd scripts
python medocr.py -i /path/to/input.pdf
```

脚本会自动将结果保存到 `WiseDiag-MedOcr-1.0.0/{filename}.md` 文件中。

**示例：**

```bash
python medocr.py -i /path/to/体检报告.pdf
# Output saved to: WiseDiag-MedOcr-1.0.0/体检报告.md
```

**使用自定义输出目录：**

```bash
python medocr.py -i /path/to/input.pdf -o /custom/output/dir
```

## 参数

| 标志 | 说明 |
|------|-------------|
| `-i, --input` | 输入 PDF 文件路径（必需） |
| `-o, --output` | 输出目录（默认：./WiseDiag-MedOcr-1.0.0） |
| `--dpi` | PDF 渲染 DPI，范围 72-600（默认：200） |

## 输出结果

脚本运行完成后，Markdown 文件会自动保存：
- 默认保存路径：`WiseDiag-MedOcr-1.0.0/{filename}.md`
- 文件名称与输入 PDF 文件的名称相同（例如：`报告.pdf` → `报告.md`）
- 无需额外保存操作——文件已保存在磁盘上

## 许可证

MIT 许可证