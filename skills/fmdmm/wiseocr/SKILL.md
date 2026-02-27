---
name: wiseocr
description: "使用 WiseOCR API（由 WiseDiag 提供）将 PDF 文件转换为 Markdown 格式。该 API 支持表格识别、多列布局以及医疗文档的 OCR 处理。使用方法：上传 PDF 文件，然后输入 “Use WiseOCR to process this” 进行转换。"
registry:
  homepage: https://github.com/fmdmm/WiseOCR
  author: fmdmm
  credentials:
    required: true
    env_vars:
      - WISEDIAG_API_KEY
---
# ⚠️ 隐私警告

**重要提示 - 安装前请阅读：**

此工具会将您的文件上传到 WiseDiag 的云服务器进行 OCR 处理。

**请勿对敏感或机密文件使用此工具**，除非：
- 您信任 WiseDiag 的数据保护政策；
- 您同意文件内容会被传输并远程处理。

**对于敏感文件，请使用离线/本地的 OCR 工具。**

---

# WiseOCR 工具（由 WiseDiag 提供支持）

该工具可将 PDF 文件转换为 Markdown 格式。脚本负责处理 API 认证、文件上传、OCR 处理，并自动保存结果。

## ⚠️ 重要说明：如何使用此工具

**您必须使用提供的脚本来处理文件，切勿直接调用任何 API 或 HTTP 端点。**

`scripts/wiseocr.py` 脚本会完成所有操作：
- API 认证（从环境变量中读取 `WISEDIAG_API_KEY`）
- PDF 文件上传及 OCR 处理
- 将转换后的 Markdown 文件保存到 `WiseOCR/{filename}.md` 目录中

## 🔑 API 密钥设置（必需）

**获取您的 API 密钥：**
👉 [https://console.wisediag.com/apiKeyManage](https://s.wisediag.com/xsu9x0jq)

```bash
export WISEDIAG_API_KEY=your_api_key
```

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

**要转换 PDF 文件，请运行：**

```bash
cd scripts
python wiseocr.py -i /path/to/input.pdf -n original_filename
```

**重要提示：** 使用 `-n` 参数时，请传入原始文件的名称（不包含扩展名），以确保输出文件的名称正确。如果上传的文件已被重命名（例如为 `ocr_input.pdf`），`-n` 会确保输出文件使用原始文件名。

脚本会自动将结果保存到 `WiseOCR/{name}.md` 目录中。

**示例：**

```bash
python wiseocr.py -i /tmp/ocr_input.pdf -n medical_report
# Output saved to: WiseOCR/medical_report.md
```

**如果需要自定义输出目录：**

```bash
python wiseocr.py -i /path/to/input.pdf -n medical_report -o /custom/output/dir
```

## 参数说明

| 参数 | 说明 |
|------|-------------|
| `-i, --input` | 输入 PDF 文件路径（必需） |
| `-n, --name` | 输出文件的原始文件名（不包含扩展名，推荐使用） |
| `-o, --output` | 输出目录（默认：./WiseOCR） |
| `--dpi` | PDF 文件的渲染 DPI 值（72-600，默认：200） |

## 输出结果

脚本运行完成后，Markdown 文件会自动保存：
- 默认保存路径：`WiseOCR/{name}.md`
- 文件名会根据 `-n` 参数确定（例如：`-n report` → `report.md`），否则使用原始文件名 |
- 无需额外保存操作——文件已保存在指定目录中

## 数据隐私

**关于您的文件：**
1. 文件会被上传到 WiseDiag 的 OCR API（地址：`https://openapi.wisediag.com`） |
2. 文件会在 WiseDiag 服务器上进行处理 |
3. 处理结果会返回给您 |
4. 文件不会永久存储在 WiseDiag 服务器上。

**对于敏感文件，请使用离线/本地的 OCR 工具。**

## 许可证**

MIT 许可证