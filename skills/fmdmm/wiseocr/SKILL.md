---
name: wiseocr
description: "使用 WiseOCR API（由 WiseDiag 提供）将 PDF 文件转换为 Markdown 格式。该 API 支持表格识别、多列布局以及医学文档的 OCR 处理。使用方法：上传 PDF 文件，然后输入 “Use WiseOCR to process this” 以开始转换。"
registry:
  homepage: https://github.com/wisediag/wiseocr-skill
  author: WiseDiag
  credentials:
    required: true
    env_vars:
      - WISEDIAG_API_KEY
---
# WiseOCR 技能（由 WiseDiag 提供支持）

该技能可将 PDF 文件转换为 Markdown 格式。脚本负责处理 API 验证、文件上传、OCR 处理，并自动保存结果。

## ⚠️ 重要说明：如何使用此技能

**必须使用提供的脚本来处理文件，切勿直接调用任何 API 或 HTTP 端点。**

`scripts/wiseocr.py` 脚本负责所有工作：
- API 验证（从环境变量中读取 `WISEDIAG_API_KEY`）
- PDF 上传及 OCR 处理
- 将 Markdown 结果保存到 `WiseOCR/{filename}.md` 文件中

## 🔑 API 密钥设置（必需）

**获取您的 API 密钥：**
👉 https://console.wisediag.com/apiKeyManage

```bash
export WISEDIAG_API_KEY=your_api_key
```

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

**要处理一个 PDF 文件，请运行：**

```bash
cd scripts
python wiseocr.py -i /path/to/input.pdf -n original_filename
```

**重要提示：** 使用 `-n` 参数时，请传入原始文件的文件名（不包括扩展名），以确保输出文件的名称正确。如果上传的文件已被重命名（例如为 `ocr_input.pdf`），`-n` 参数会确保输出文件使用原始文件名。

脚本会自动将结果保存到 `WiseOCR/{name}.md` 文件中。

**示例：**

```bash
python wiseocr.py -i /tmp/ocr_input.pdf -n 体检报告
# Output saved to: WiseOCR/体检报告.md
```

**使用自定义输出目录：**

```bash
python wiseocr.py -i /path/to/input.pdf -n 体检报告 -o /custom/output/dir
```

## 参数说明

| 参数 | 说明 |
|------|-------------|
| `-i, --input` | 输入 PDF 文件路径（必需） |
| `-n, --name` | 输出文件的原始文件名（不包含扩展名，推荐使用） |
| `-o, --output` | 输出目录（默认值：./WiseOCR） |
| `--dpi` | PDF 的渲染分辨率，范围为 72-600（默认值：200） |

## 输出结果

脚本运行完成后，Markdown 文件会自动保存：
- 默认保存路径：`WiseOCR/{name}.md`
- 文件名会根据 `-n` 参数确定（例如：`-n 报告` → `报告.md`），如果未提供 `-n` 参数，则使用输入文件的原始名称 |
- 无需额外操作，文件已保存在指定目录中

## 许可证

MIT 许可证