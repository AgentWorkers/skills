---
name: nutrient-openclaw
description: >
  **OpenClaw原生PDF/文档处理功能（适用于Nutrient DWS）**  
  专为OpenClaw用户设计，提供PDF转换、OCR识别、文本/表格提取、个人身份信息（PII）保护、水印添加、数字签名等功能。这些功能通过OpenClaw内置的`nutrient_*`工具实现，例如`nutrient_convert_to_pdf`、`nutrient_extract_text`等。当用户触发与OpenClaw相关的操作（如插件使用、聊天中的文档处理请求）时，该功能会被激活。文件处理过程通过网络由Nutrient DWS完成，因此仅适用于允许使用第三方文档处理服务的场景。在非OpenClaw环境中，请使用通用的Nutrient文档处理功能。
  OpenClaw-native PDF/document processing skill for Nutrient DWS. Best for
  OpenClaw users who need PDF conversion, OCR, text/table extraction, PII
  redaction, watermarking, digital signatures, and API credit checks via built-in
  `nutrient_*` tools. Triggers on OpenClaw tool names
  (`nutrient_convert_to_pdf`, `nutrient_extract_text`, etc.), "OpenClaw plugin",
  "Nutrient OpenClaw", and document-processing requests in OpenClaw chats. Files
  are processed by Nutrient DWS over the network, so use it only when
  third-party document processing is acceptable. For non-OpenClaw environments,
  use the Universal Nutrient Document Processing skill instead.
homepage: https://www.nutrient.io/api/
clawdis:
  emoji: "📄"
  requires:
    config:
      - plugins.entries.nutrient-openclaw.config.apiKey
  install:
    - id: nutrient-openclaw
      kind: node
      package: "@nutrient-sdk/nutrient-openclaw"
      label: Install Nutrient OpenClaw package
  links:
    homepage: https://www.nutrient.io/api/
    repository: https://github.com/PSPDFKit-labs/nutrient-openclaw
    documentation: https://www.nutrient.io/api/documentation/security
  config:
    example: |
      plugins:
        entries:
          nutrient-openclaw:
            config:
              apiKey: "your-api-key-here"
---
# 营养成分文档处理（OpenClaw原生功能）

专为OpenClaw用户设计。您可以直接在OpenClaw对话框中处理文档——支持PDF转换、文本/表格提取、OCR识别、个人身份信息（PII）的脱敏处理、数字签名以及水印添加等功能，这些功能均通过原生的`nutrient_*`工具实现。

## 安装

在OpenClaw内部推荐的安装流程如下：

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

## 数据处理

- `nutrient_*`工具会将文件或提取的文档内容发送到Nutrient的数据处理服务（DWS）进行进一步处理。
- 在使用生产环境中的敏感文档之前，请务必查阅Nutrient的[处理器API安全指南](https://www.nutrient.io/api/documentation/security)和[隐私政策](https://www.nutrient.io/api/processor-api/)。
- Nutrient确保其托管的处理器API使用HTTPS进行数据传输，并且在处理完成后不会永久存储输入或输出文件；在上传敏感资料之前，请确认这符合您组织的安全要求。
- 建议从非敏感的样本文件开始使用，并使用权限最低的API密钥进行测试。

## 可用工具

| 工具 | 功能描述 |
|------|-------------|
| `nutrient_convert_to_pdf` | 将DOCX、XLSX、PPTX、HTML或图片格式的文件转换为PDF |
| `nutrient_convert_to_image` | 将PDF页面转换为PNG、JPEG或WebP格式的图片 |
| `nutrient_convert_to_office` | 将PDF转换为DOCX、XLSX或PPTX格式 |
| `nutrient_extract_text` | 提取文档中的文本、表格或键值对 |
| `nutrient_ocr` | 对扫描的PDF或图片进行OCR识别 |
| `nutrient_watermark` | 为PDF添加文本或图片水印 |
| `nutrient_redact` | 根据预设规则（如SSN、电子邮件、电话号码等）对文档内容进行脱敏 |
| `nutrient_ai_redact` | 利用人工智能技术检测并删除文档中的个人身份信息 |
| `nutrient_sign` | 为PDF文档添加数字签名 |
| `nutrient_check_credits` | 检查您的API使用额度和剩余信用 |

## 示例指令

- **转换：** “将此Word文档转换为PDF”
- **提取：** “从这张扫描的收据中提取所有文本” / “从该PDF文件中提取表格数据”
- **脱敏：** “从该文档中删除所有个人身份信息” / “移除电子邮件地址和电话号码”
- **水印：** “为该PDF添加‘机密’水印”
- **签名：** “以‘Jonathan Rhyne’的名义签署此合同”

## 链接

- [npm包](https://www.npmjs.com/package/@nutrient-sdk/nutrient-openclaw)
- [GitHub仓库](https://github.com/PSPDFKit-labs/nutrient-openclaw)
- [Nutrient API文档](https://www.nutrient.io/)