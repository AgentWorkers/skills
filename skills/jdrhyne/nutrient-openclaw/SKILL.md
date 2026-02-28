---
name: nutrient-openclaw
description: OpenClaw原生PDF/文档处理技能，专为Nutrient DWS平台设计。非常适合需要PDF转换、OCR识别、文本/表格提取、个人身份信息（PII）保护、水印添加、数字签名功能，以及通过内置的`nutrient_*`工具进行API信用检查的OpenClaw用户。该技能会在使用OpenClaw工具（如`nutrient_convert_to_pdf`、`nutrient_extract_text`等）时触发，也可应用于“OpenClaw插件”及OpenClaw聊天中的文档处理请求。对于非OpenClaw环境，请使用通用的Nutrient文档处理技能。
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

## 参数说明

- `nutrient_extract_textlanguage`参数应以字符串形式传递。
- 如需支持多种OCR语言，请使用逗号分隔的字符串（例如：`english,german`）。

## 可用工具

| 工具 | 描述 |
|------|-------------|
| `nutrient_convert_to_pdf` | 将DOCX、XLSX、PPTX、HTML或图片转换为PDF格式 |
| `nutrient_convert_to_image` | 将PDF页面渲染为PNG、JPEG或WebP格式 |
| `nutrient_convert_to_office` | 将PDF转换为DOCX、XLSX或PPTX格式 |
| `nutrient_extract_text` | 提取文本、表格或键值对内容 |
| `nutrient_ocr` | 对扫描的PDF或图片进行OCR识别 |
| `nutrient_watermark` | 为PDF添加文本或图片水印 |
| `nutrient_redact` | 根据预设规则隐藏文档中的个人身份信息（如SSN、电子邮件、电话号码） |
| `nutrient_ai_redact` | 利用人工智能技术检测并隐藏个人身份信息 |
| `nutrient_sign` | 为PDF文档添加数字签名 |
| `nutrient_check_credits` | 检查API的信用余额和使用情况 |

## 示例命令

**转换：** “将此Word文档转换为PDF格式”
**提取：** “从这张扫描的收据中提取所有文本”
**隐藏信息：** “从该文档中隐藏所有个人身份信息”
**添加水印：** “为该PDF添加‘机密’水印”
**签名：** “以‘Jonathan Rhyne’的名义签署此合同”

## 链接

- [npm包](https://www.npmjs.com/package/@nutrient-sdk/nutrient-openclaw)
- [GitHub仓库](https://github.com/PSPDFKit-labs/nutrient-openclaw)
- [Nutrient API文档](https://www.nutrient.io/)