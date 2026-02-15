---
name: nutrient-openclaw
description: OpenClaw的文档处理功能：通过Nutrient DWS API，可以对PDF文件及Office文档进行转换、提取文本、OCR识别、内容编辑、签名以及添加水印等操作。适用于需要将文档（如DOCX/XLSX/PPTX格式）转换为PDF，或将PDF转换为图片或Office格式；从PDF中提取文本或表格；对扫描后的文档进行OCR识别；删除敏感信息或个人身份信息（PII）；添加水印；以及对文档进行数字签名等场景。该功能会在用户触发“转换为PDF”、“提取文本”、“进行OCR识别”、“删除敏感信息”、“添加水印”或“签署文档”等操作时自动执行。
---

# 营养成分文档处理

您可以直接在 OpenClaw 对话中处理文档——转换文件格式、提取文本、应用光学字符识别（OCR）技术、删除个人身份信息（PII）、添加签名以及为文件添加水印，所有这些操作都通过自然语言界面完成。

## 安装

```bash
openclaw plugins install @nutrient-sdk/nutrient-openclaw
```

配置您的 API 密钥：

```yaml
plugins:
  entries:
    nutrient-openclaw:
      config:
        apiKey: "your-api-key-here"
```

您可以在 [nutrient.io/api](https://www.nutrient.io/api/) 获取 API 密钥。

## 可用工具

| 工具 | 描述 |
|------|-------------|
| `nutrient_convert_to_pdf` | 将 DOCX、XLSX、PPTX、HTML 或图片格式的文件转换为 PDF |
| `nutrient_convert_to_image` | 将 PDF 页面渲染为 PNG、JPEG 或 WebP 格式 |
| `nutrient_convert_to_office` | 将 PDF 转换为 DOCX、XLSX 或 PPTX 格式 |
| `nutrient_extract_text` | 提取文档中的文本、表格或键值对 |
| `nutrient_ocr` | 对扫描的 PDF 或图片应用 OCR 技术 |
| `nutrient_watermark` | 为文件添加文本或图片水印 |
| `nutrient_redact` | 通过预设模式删除文档中的个人身份信息（如 SSN、电子邮件地址、电话号码） |
| `nutrient_ai_redact` | 基于人工智能的个人信息检测与删除功能 |
| `nutrient_sign` | 为 PDF 文档添加数字签名 |
| `nutrient_check_credits` | 检查您的 API 信用余额和使用情况 |

## 示例指令

**转换：** “将此 Word 文档转换为 PDF”

**提取：** “从这张扫描的收据中提取所有文本” / “从该 PDF 文件中提取表格”

**删除敏感信息：** “删除文档中的所有个人身份信息” / “移除电子邮件地址和电话号码”

**添加水印：** “为该 PDF 文件添加‘机密’水印”

**签名：** “以 Jonathan Rhyne 的身份签署此合同”

## 链接

- [npm 包](https://www.npmjs.com/package/@nutrient-sdk/nutrient-openclaw)
- [GitHub 仓库](https://github.com/PSPDFKit-labs/nutrient-openclaw)
- [Nutrient API](https://www.nutrient.io/)