---
name: nutrient-document-processing
description: 适用于与Agent Skills兼容的产品的通用（非OpenClaw）营养数据（Nutrient Data）处理技能。特别适用于Claude Code、Codex CLI、Gemini CLI、Cursor、Windsurf、OpenCode和Copilot等环境。支持完整的工作流程，包括：转换PDF/Office文档和图片格式、进行OCR识别、提取文本/表格/键值对信息、使用AI技术对个人信息（PII）进行脱敏处理、添加水印、进行数字签名、填写表单、合并/拆分/重新排序页面，以及支持API调用和信用信息核查等功能。优先推荐使用MCP服务器模式，同时提供API/curl作为备用方案。该技能可通过以下关键词激活：PDF、document、convert、extract、OCR、redact、watermark、sign、merge、split、compress、form fill、document processing、MCP。
  Universal (non-OpenClaw) Nutrient DWS document-processing skill for Agent Skills-compatible products.
  Best for Claude Code, Codex CLI, Gemini CLI, Cursor, Windsurf, OpenCode, and Copilot environments.
  Supports full workflows: convert PDF/Office/images, OCR, extract text/tables/key-values, redact PII
  (pattern + AI), watermark, digitally sign, form fill, merge/split/reorder pages, and API usage/credit
  checks. Prefers MCP server mode, with direct API/curl fallback. Activates on keywords: PDF, document,
  convert, extract, OCR, redact, watermark, sign, merge, split, compress, form fill, document processing, MCP.
homepage: https://www.nutrient.io/api/
repository: https://github.com/PSPDFKit-labs/nutrient-agent-skill
license: Apache-2.0
compatibility: >-
  Requires Node.js 18+ and an internet connection. Works with Claude Code, Codex CLI, Gemini CLI,
  OpenCode, Cursor, Windsurf, GitHub Copilot, Amp, or any Agent Skills-compatible product.
  Alternatively, use curl for direct API access without Node.js.
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "requires":
          {
            "anyBins": ["npx", "curl"],
            "env": ["NUTRIENT_API_KEY", "NUTRIENT_DWS_API_KEY"],
          },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "@nutrient-sdk/dws-mcp-server",
              "label": "Install Nutrient DWS MCP Server (optional)",
            },
          ],
      },
  }
---
# 营养文档处理（通用代理技能）

该技能适用于Claude Code/Codex/Gemini/Cursor/Windsurf等非OpenClaw代理。可通过[Nutrient DWS处理器API](https://www.nutrient.io/api/)对文档进行加工、转换、提取、OCR识别、编辑、签名和操作。

## 设置

您需要一个Nutrient DWS API密钥。您可以在<https://dashboard.nutrient.io/sign_up/?product=processor>免费获取一个密钥。

### 选项1：MCP服务器（推荐）

如果您的代理支持MCP（模型上下文协议），请使用Nutrient DWS MCP服务器。它以原生工具的形式提供所有操作功能。

**配置您的MCP客户端**（例如`claude_desktop_config.json`或`.mcp.json`）：

```json
{
  "mcpServers": {
    "nutrient-dws": {
      "command": "npx",
      "args": ["-y", "@nutrient-sdk/dws-mcp-server"],
      "env": {
        "NUTRIENT_DWS_API_KEY": "YOUR_API_KEY",
        "SANDBOX_PATH": "/path/to/working/directory"
      }
    }
  }
}
```

然后直接使用MCP工具（例如`convert_to_pdf`、`extract_text`、`redact`等）。

### 选项2：直接API调用（curl）

对于不支持MCP的代理，可以直接调用API：

```bash
export NUTRIENT_API_KEY="your_api_key_here"
```

所有请求均以multipart POST的形式发送到`https://api.nutrient.io/build`，并需要包含`instructions` JSON字段。

## 安全限制

- 该技能会将文档发送到Nutrient DWS API (`api.nutrient.io`) 进行处理。文档可能包含敏感数据——请确保您的Nutrient账户的数据处理政策符合要求。
- 该技能不会访问除处理所需文件之外的任何本地文件。
- 该技能不会在会话结束后保留API密钥或凭证。
- 在使用MCP服务器模式（`npx @nutrient-sdk/dws-mcp-server`）时，系统会在运行时从npm下载官方的Nutrient MCP服务器包。
- 所有API调用均需要明确的API密钥——不允许匿名访问。

## 操作功能

### 1. 文档转换

支持在PDF、DOCX、XLSX、PPTX、HTML和图像格式之间进行转换。

- **HTML转PDF：**
```bash
curl -X POST https://api.nutrient.io/build \
  -H "Authorization: Bearer $NUTRIENT_API_KEY" \
  -F "index.html=@index.html" \
  -F 'instructions={"parts":[{"html":"index.html"}]}' \
  -o output.pdf
```

- **DOCX转PDF：**
```bash
curl -X POST https://api.nutrient.io/build \
  -H "Authorization: Bearer $NUTRIENT_API_KEY" \
  -F "document.docx=@document.docx" \
  -F 'instructions={"parts":[{"file":"document.docx"}]}' \
  -o output.pdf
```

- **PDF转DOCX/XLSX/PPTX：**
```bash
curl -X POST https://api.nutrient.io/build \
  -H "Authorization: Bearer $NUTRIENT_API_KEY" \
  -F "document.pdf=@document.pdf" \
  -F 'instructions={"parts":[{"file":"document.pdf"}],"output":{"type":"docx"}}' \
  -o output.docx
```

- **图像转PDF：**
```bash
curl -X POST https://api.nutrient.io/build \
  -H "Authorization: Bearer $NUTRIENT_API_KEY" \
  -F "image.jpg=@image.jpg" \
  -F 'instructions={"parts":[{"file":"image.jpg"}]}' \
  -o output.pdf
```

### 2. 提取文本和数据

- **提取纯文本：**
```bash
curl -X POST https://api.nutrient.io/build \
  -H "Authorization: Bearer $NUTRIENT_API_KEY" \
  -F "document.pdf=@document.pdf" \
  -F 'instructions={"parts":[{"file":"document.pdf"}],"output":{"type":"text"}}' \
  -o output.txt
```

- **提取表格（格式为JSON、CSV或Excel）：**
```bash
curl -X POST https://api.nutrient.io/build \
  -H "Authorization: Bearer $NUTRIENT_API_KEY" \
  -F "document.pdf=@document.pdf" \
  -F 'instructions={"parts":[{"file":"document.pdf"}],"output":{"type":"xlsx"}}' \
  -o tables.xlsx
```

- **提取键值对：**
```bash
curl -X POST https://api.nutrient.io/build \
  -H "Authorization: Bearer $NUTRIENT_API_KEY" \
  -F "document.pdf=@document.pdf" \
  -F 'instructions={"parts":[{"file":"document.pdf"}],"actions":[{"type":"extraction","strategy":"key-values"}]}' \
  -o result.json
```

### 3. OCR扫描文档

对扫描的PDF或图像应用OCR识别，生成可搜索的PDF文件，其中文本可被选中。

**支持的语言：**英语、德语、法语、西班牙语、意大利语、葡萄牙语、荷兰语、瑞典语、丹麦语、挪威语、芬兰语、波兰语、捷克语、土耳其语、日语、韩语、简体中文、繁体中文、阿拉伯语、希伯来语、泰语、印地语、俄语等。

### 4. 遮盖敏感信息

- **基于模式的遮盖**（预设模式）：
```bash
curl -X POST https://api.nutrient.io/build \
  -H "Authorization: Bearer $NUTRIENT_API_KEY" \
  -F "document.pdf=@document.pdf" \
  -F 'instructions={"parts":[{"file":"document.pdf"}],"actions":[{"type":"redaction","strategy":"preset","preset":"social-security-number"}]}' \
  -o redacted.pdf
```

支持的预设模式包括：`social-security-number`（社会安全号码）、`credit-card-number`（信用卡号码）、`email-address`（电子邮件地址）、`north-american-phone-number`（北美电话号码）、`international-phone-number`（国际电话号码）、`date`（日期）、`url`（网址）、`ipv4`（IPv4地址）、`ipv6`（IPv6地址）、`mac-address`（MAC地址）、`us-zip-code`（美国邮政编码）、`vin`（车辆识别码）、`time`（时间）。

- **基于正则表达式的遮盖：**
```bash
curl -X POST https://api.nutrient.io/build \
  -H "Authorization: Bearer $NUTRIENT_API_KEY" \
  -F "document.pdf=@document.pdf" \
  -F 'instructions={"parts":[{"file":"document.pdf"}],"actions":[{"type":"redaction","strategy":"regex","regex":"\\b[A-Z]{2}\\d{6}\\b"}]}' \
  -o redacted.pdf
```

- **基于AI的个人信息（PII）遮盖：**
```bash
curl -X POST https://api.nutrient.io/build \
  -H "Authorization: Bearer $NUTRIENT_API_KEY" \
  -F "document.pdf=@document.pdf" \
  -F 'instructions={"parts":[{"file":"document.pdf"}],"actions":[{"type":"ai_redaction","criteria":"All personally identifiable information"}]}' \
  -o redacted.pdf
```

`criteria`字段支持自然语言描述，例如：“Names and phone numbers”（姓名和电话号码）、“Protected health information”（受保护的健康信息）、“Financial account numbers”（财务账户号码）。

### 5. 添加水印

- **文本水印：**
```bash
curl -X POST https://api.nutrient.io/build \
  -H "Authorization: Bearer $NUTRIENT_API_KEY" \
  -F "document.pdf=@document.pdf" \
  -F 'instructions={"parts":[{"file":"document.pdf"}],"actions":[{"type":"watermark","text":"CONFIDENTIAL","fontSize":48,"fontColor":"#FF0000","opacity":0.5,"rotation":45,"width":"50%","height":"50%"}]}' \
  -o watermarked.pdf
```

- **图像水印：**
```bash
curl -X POST https://api.nutrient.io/build \
  -H "Authorization: Bearer $NUTRIENT_API_KEY" \
  -F "document.pdf=@document.pdf" \
  -F "logo.png=@logo.png" \
  -F 'instructions={"parts":[{"file":"document.pdf"}],"actions":[{"type":"watermark","imagePath":"logo.png","width":"30%","height":"30%","opacity":0.3}]}' \
  -o watermarked.pdf
```

### 6. 数字签名

- **使用CMS签名对PDF进行签名：**
```bash
curl -X POST https://api.nutrient.io/build \
  -H "Authorization: Bearer $NUTRIENT_API_KEY" \
  -F "document.pdf=@document.pdf" \
  -F 'instructions={"parts":[{"file":"document.pdf"}],"actions":[{"type":"sign","signatureType":"cms","signerName":"John Doe","reason":"Approval","location":"New York"}]}' \
  -o signed.pdf
```

- **使用CAdES-B-LT进行签名（长期验证）：**
```bash
curl -X POST https://api.nutrient.io/build \
  -H "Authorization: Bearer $NUTRIENT_API_KEY" \
  -F "document.pdf=@document.pdf" \
  -F 'instructions={"parts":[{"file":"document.pdf"}],"actions":[{"type":"sign","signatureType":"cades","cadesLevel":"b-lt","signerName":"Jane Smith"}]}' \
  -o signed.pdf
```

### 7. 填写表单（即时JSON）

使用即时JSON格式填写PDF表单字段：
```bash
curl -X POST https://api.nutrient.io/build \
  -H "Authorization: Bearer $NUTRIENT_API_KEY" \
  -F "form.pdf=@form.pdf" \
  -F 'instructions={"parts":[{"file":"form.pdf"}],"actions":[{"type":"fillForm","fields":[{"name":"firstName","value":"John"},{"name":"lastName","value":"Doe"},{"name":"email","value":"john@example.com"}]}]}' \
  -o filled.pdf
```

### 8. 合并和分割PDF

- **合并多个PDF文件：**
```bash
curl -X POST https://api.nutrient.io/build \
  -H "Authorization: Bearer $NUTRIENT_API_KEY" \
  -F "doc1.pdf=@doc1.pdf" \
  -F "doc2.pdf=@doc2.pdf" \
  -F 'instructions={"parts":[{"file":"doc1.pdf"},{"file":"doc2.pdf"}]}' \
  -o merged.pdf
```

- **提取特定页面：**
```bash
curl -X POST https://api.nutrient.io/build \
  -H "Authorization: Bearer $NUTRIENT_API_KEY" \
  -F "document.pdf=@document.pdf" \
  -F 'instructions={"parts":[{"file":"document.pdf","pages":{"start":0,"end":4}}]}' \
  -o pages1-5.pdf
```

### 9. 将PDF页面渲染为图像

```bash
curl -X POST https://api.nutrient.io/build \
  -H "Authorization: Bearer $NUTRIENT_API_KEY" \
  -F "document.pdf=@document.pdf" \
  -F 'instructions={"parts":[{"file":"document.pdf","pages":{"start":0,"end":0}}],"output":{"type":"png","dpi":300}}' \
  -o page1.png
```

### 10. 检查剩余信用额度

```bash
curl -X GET https://api.nutrient.io/credits \
  -H "Authorization: Bearer $NUTRIENT_API_KEY"
```

## 最佳实践

1. **如果您的代理支持MCP，请使用MCP服务器**——它可自动处理文件读写、错误处理和沙箱环境。
2. **设置`SANDBOX_PATH`以限制文件访问范围**。
3. **在批量操作前检查剩余信用额度**，以避免中断。
4. **对于复杂的个人信息（PII），使用AI遮盖功能；对于已知模式，使用预设或正则表达式遮盖方式（更快、更经济）。
5. **链式操作**——API支持在一次调用中执行多个操作（例如先进行OCR识别，再遮盖信息）。

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| 401 Unauthorized | 确保您的API密钥有效且具有足够的信用额度 |
| 413 Payload Too Large | 文件大小不得超过100 MB |
| AI处理速度慢 | AI分析可能需要60–120秒，这是正常现象 |
| OCR识别质量差 | 尝试使用不同的语言参数或提高扫描质量 |
| 提取时缺少文本 | 先对扫描文档进行OCR识别 |

## 更多信息

- [完整API参考](references/REFERENCE.md) — 详细的API端点、参数和错误代码
- [API测试平台](https://dashboard.nutrient.io/processor-api/playground/) — 提供交互式API测试
- [API文档](https://www.nutrient.io/guides/dws-processor/) — 官方指南
- [MCP服务器仓库](https://github.com/PSPDFKit/nutrient-dws-mcp-server) — 源代码和问题跟踪