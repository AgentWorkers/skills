---
name: docusign
description: "DocuSign电子签名功能：通过REST API管理信封、模板、接收者及签名流程  
**概述：**  
DocuSign提供了强大的电子签名解决方案，允许用户通过REST API轻松地创建、管理和执行电子签名流程。用户可以自定义信封内容、模板格式、指定接收者，并控制签名流程的各个环节（如签名顺序、签名者的权限等）。这些功能极大地提升了电子签名的便捷性和灵活性，适用于各种业务场景。  
**主要功能：**  
1. **信封管理：** 创建和编辑用于存放电子文档的信封，包括设置信封的名称、描述、附件列表等。  
2. **模板设计：** 定义电子签名所需的文档结构和格式，包括表格、表格数据、图片等元素。  
3. **接收者管理：** 添加或删除签名接收者，并设置他们的权限（如仅查看、编辑或完全访问文档）。  
4. **签名流程控制：** 定义签名者的顺序、签名提示信息等，支持多签名者的协同签名。  
5. **文档上传与下载：** 通过API上传电子文档，并在签名完成后下载签名后的文档。  
**API接口示例：**  
以下是一个简单的API接口示例，用于上传电子文档到DocuSign服务器：  
```json
POST /api/documents/upload
{
  "documentId": "D20231234567890",
  "file": {
    "url": "path/to/your/electronic/document.pdf",
    "filename": "example_document.pdf"
  },
  "options": {
    "format": "pdf",
    "security": {
      "password": "your_password"
    }
}
```
**注意事项：**  
- 请确保使用正确的API版本和参数格式。  
- 为敏感数据（如密码）使用安全的传输方式（如HTTPS）。  
- 查阅DocuSign官方文档以获取详细的API文档和使用说明。  
**应用场景：**  
- 合同签署：企业内部或跨企业的合同签署流程。  
- 申请表处理：用户提交申请表后，系统自动发送电子签名链接。  
- 电子发票：生成包含签名字段的电子发票。  
**优势：**  
- 高度集成性：可与现有的业务系统无缝集成。  
- 强大的自定义功能：满足各种个性化需求。  
- 安全性：符合行业标准的数据加密和存储机制。  
通过DocuSign的REST API，您可以轻松实现电子签名的自动化和标准化管理，提升工作效率和用户体验。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "✍️", "requires": {"env": ["DOCUSIGN_ACCESS_TOKEN", "DOCUSIGN_ACCOUNT_ID", "DOCUSIGN_BASE_URL"]}, "primaryEnv": "DOCUSIGN_ACCESS_TOKEN", "homepage": "https://www.agxntsix.ai"}}
---
# ✍️ DocuSign

DocuSign电子签名功能——通过REST API管理信封、模板、收件人及签名流程

## 所需参数

| 参数          | 是否必填 | 说明                          |
|--------------|---------|---------------------------------------------|
| `DOCUSIGN_ACCESS_TOKEN` | ✅     | OAuth访问令牌                        |
| `DOCUSIGN_ACCOUNT_ID` | ✅     | 账户ID                          |
| `DOCUSIGN_BASE_URL` | ✅     | 基础URL（默认：demo）                     |

## 快速入门

```bash
# List envelopes
python3 {{baseDir}}/scripts/docusign.py envelopes --from_date <value> --status <value>

# Get envelope
python3 {{baseDir}}/scripts/docusign.py envelope-get id <value>

# Create envelope
python3 {{baseDir}}/scripts/docusign.py envelope-create --subject <value> --templateId <value> --status <value>

# Void envelope
python3 {{baseDir}}/scripts/docusign.py envelope-void id <value> --voidedReason <value>

# List recipients
python3 {{baseDir}}/scripts/docusign.py recipients id <value>

# List documents
python3 {{baseDir}}/scripts/docusign.py documents id <value>

# List templates
python3 {{baseDir}}/scripts/docusign.py templates --search_text <value>

# Get template
python3 {{baseDir}}/scripts/docusign.py template-get id <value>
```

## 所有命令

| 命令           | 说明                          |
|-----------------|---------------------------------------------|
| `envelopes`     | 列出所有信封                        |
| `envelope-get`    | 获取指定信封                        |
| `envelope-create`  | 创建新信封                        |
| `envelope-void`    | 删除信封                          |
| `recipients`    | 列出所有收件人                        |
| `documents`     | 列出所有文档                        |
| `templates`     | 列出所有模板                        |
| `template-get`    | 获取指定模板                        |
| `audit-events`   | 获取审计事件记录                   |
| `folders`     | 列出所有文件夹                        |
| `users`     | 列出所有用户                        |

## 输出格式

所有命令默认以JSON格式输出。若需可读性更强的输出格式，可使用`--human`选项。

```bash
python3 {{baseDir}}/scripts/docusign.py <command> --human
```

## 脚本参考

| 脚本          | 说明                          |
|-----------------|---------------------------------------------|
| `{{baseDir}}/scripts/docusign.py` | 主要命令行工具（包含所有命令）            |

## 致谢

本工具由[M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi)和[agxntsix.ai](https://www.agxntsix.ai)开发。  
更多内容请访问[YouTube频道](https://youtube.com/@aiwithabidi)及[GitHub仓库](https://github.com/aiwithabidi)。  
本工具属于**AgxntSix Skill Suite**的一部分，专为OpenClaw代理设计。  

📅 **需要帮助为您的企业配置OpenClaw吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)