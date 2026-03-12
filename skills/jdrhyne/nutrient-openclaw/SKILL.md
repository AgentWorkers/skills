---
name: nutrient-openclaw
description: OpenClaw-native Nutrient DWS document-processing skill with full workflow coverage via built-in `nutrient_*` tools: convert PDF/Office/images, OCR, extract text/tables/key-values, redact PII (pattern + AI), watermark, digitally sign, and check API usage/credits. Triggers on OpenClaw tool names (`nutrient_convert_to_pdf`, `nutrient_extract_text`, etc.), "OpenClaw plugin", "Nutrient OpenClaw", and document-processing requests in OpenClaw chats. For non-OpenClaw environments, use the Universal Nutrient Document Processing skill instead.
homepage: https://www.nutrient.io/api/
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "requires":
          {
            "config":
              ["plugins.entries.nutrient-openclaw.config.apiKey"],
          },
        "install":
          [
            {
              "id": "nutrient-openclaw",
              "kind": "plugin",
              "package": "@nutrient-sdk/nutrient-openclaw",
              "label": "Install Nutrient OpenClaw plugin",
            },
          ],
      },
  }
---

# 营养素文档处理（OpenClaw原生功能）

专为OpenClaw用户设计。您可以直接在OpenClaw对话框中处理文档——支持PDF转换、文本/表格提取、OCR识别、个人身份信息（PII）的隐藏处理、数字签名以及水印添加等功能，这些功能均通过原生的`nutrient_*`工具实现。

## 安装

```bash
openclaw plugins install @nutrient-sdk/nutrient-openclaw
```

配置您的API密钥：

```yaml
plugins:
  entries:
    nutrient-openclaw:
      config:
        apiKey: "your-api-key-here"
```

您可以在[nutrient.io/api](https://www.nutrient.io/api/)获取API密钥。

## 可用工具

| 工具 | 描述 |
|------|-------------|
| `nutrient_convert_to_pdf` | 将DOCX、XLSX、PPTX、HTML文件或图片转换为PDF格式 |
| `nutrient_convert_to_image` | 将PDF页面渲染为PNG、JPEG或WebP格式 |
| `nutrient_convert_to_office` | 将PDF转换为DOCX、XLSX或PPTX格式 |
| `nutrient_extract_text` | 提取文档中的文本、表格或键值对 |
| `nutrient_ocr` | 对扫描的PDF文件或图片进行OCR识别 |
| `nutrient_watermark` | 为PDF文件添加文本或图片水印 |
| `nutrient_redact` | 通过预设模式隐藏文档中的个人身份信息（如SSN、电子邮件地址、电话号码） |
| `nutrient_ai_redact` | 利用人工智能技术检测并隐藏个人身份信息 |
| `nutrient_sign` | 为PDF文件添加数字签名 |
| `nutrient_check_credits` | 检查您的API信用额度和使用情况 |

## 示例指令

**转换：** “将此Word文档转换为PDF格式”  
**提取：** “从这张扫描的收据中提取所有文本” / “从该PDF文件中提取表格内容”  
**隐藏信息：** “隐藏文档中的所有个人身份信息” / “删除电子邮件地址和电话号码”  
**添加水印：** “为该PDF文件添加‘机密’水印”  
**签名：** “以Jonathan Rhyne的名义签署此合同”  

## 链接

- [npm包](https://www.npmjs.com/package/@nutrient-sdk/nutrient-openclaw)  
- [GitHub仓库](https://github.com/PSPDFKit-labs/nutrient-openclaw)  
- [Nutrient API文档](https://www.nutrient.io/)