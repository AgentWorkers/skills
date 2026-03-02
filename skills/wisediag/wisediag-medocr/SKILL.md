---
name: wisediag-medocr
description: "**PDF OCR** — 通过 WiseDiag 云 API 将 PDF 文件转换为 Markdown 格式。支持表格识别、多列布局以及高精度的文本提取。**使用方法**：上传 PDF 文件，然后输入 “Use WiseOCR to OCR this” 来执行 OCR 转换。"
registry:
  homepage: https://github.com/wisediag/WiseOCR
  author: wisediag
  credentials:
    required: true
    env_vars:
      - WISEDIAG_API_KEY
---
# ⚠️ 隐私警告

**重要提示 - 安装前请阅读：**

此工具会**将您的文件上传到WiseDiag的云服务器**进行OCR处理。

**请勿对敏感或机密文件使用此工具**，除非：
- 您信任WiseDiag的数据处理政策；
- 您同意文件内容会被传输并远程处理。

**对于敏感文件，请使用离线/本地的OCR工具。**

---

# WiseOCR工具（由WiseDiag提供）

这是一个高精度的OCR工具，可以将PDF文件转换为Markdown格式。处理完成后，Markdown结果会自动保存到磁盘上——无需额外保存操作。

## 安装

```bash
pip install -r requirements.txt
```

## 🔑 API密钥设置（必需）

**获取您的API密钥：** 👉 [https://console.wisediag.com/apiKeyManage](https://s.wisediag.com/xsu9x0jq)

API密钥必须设置为环境变量。脚本会自动读取该密钥。

```bash
export WISEDIAG_API_KEY=your_api_key
```

## 如何处理PDF文件（分步操作）

**请勿直接调用任何API或HTTP端点。** **仅使用以下脚本。**

步骤1：设置API密钥（如果尚未设置）：

```bash
export WISEDIAG_API_KEY=your_api_key
```

步骤2：使用输入的PDF文件运行脚本：

```bash
cd scripts
python3 wiseocr.py -i "/path/to/input_filename.pdf"
```

**重要提示：** 如果输入文件已被复制或重命名（例如复制到临时路径），请务必使用原始文件名（不包括扩展名）并加上`-n`参数，以确保输出文件名正确：

```bash
python3 wiseocr.py -i "/tmp/ocr_input.pdf" -n "my_report"
# Output saved to: ~/.openclaw/workspace/WiseOCR/my_report.md
```

Markdown结果会自动保存到`~/.openclaw/workspace/WiseOCR/{name}.md`文件夹中。无需额外保存操作。

## 参数

| 参数 | 说明 |
|------|-------------|
| `-i, --input` | 输入PDF文件的路径（必需） |
| `-n, --name` | 输出文件的原始文件名（不包括扩展名，建议在输入文件被复制或重命名时使用） |
| `-o, --output` | 输出目录（默认：~/openclaw/workspace/WiseOCR） |
| `--dpi` | PDF渲染的DPI值，范围72-600（默认：200） |

## 数据隐私

**您的文件将经历以下处理流程：**
1. 文件被上传到WiseDiag的OCR API；
2. 文件在WiseDiag服务器上进行处理；
3. 处理结果会返回给您；
4. 文件不会永久存储在WiseDiag服务器上。

**对于敏感文件，请使用离线/本地的OCR工具。**

## 许可证

MIT许可证