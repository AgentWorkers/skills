---
name: pandadoc
description: "PandaDoc — 通过 REST API 管理文档、模板、联系人和电子签名"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🐼", "requires": {"env": ["PANDADOC_API_KEY"]}, "primaryEnv": "PANDADOC_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🐼 PandaDoc

PandaDoc — 通过 REST API 管理文档、模板、联系人和电子签名

## 必需条件

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `PANDADOC_API_KEY` | ✅ | 来自 app.pandadoc.com 的 API 密钥 |

## 快速入门

```bash
# List documents
python3 {{baseDir}}/scripts/pandadoc.py documents --status <value> --q <value> --tag <value>

# Get document details
python3 {{baseDir}}/scripts/pandadoc.py document-get id <value>

# Create document
python3 {{baseDir}}/scripts/pandadoc.py document-create --name <value> --template_uuid <value> --recipients <value>

# Send document
python3 {{baseDir}}/scripts/pandadoc.py document-send id <value> --message <value> --subject <value>

# Get status
python3 {{baseDir}}/scripts/pandadoc.py document-status id <value>

# Delete document
python3 {{baseDir}}/scripts/pandadoc.py document-delete id <value>

# Create sharing link
python3 {{baseDir}}/scripts/pandadoc.py document-link id <value> --recipient <value>

# List templates
python3 {{baseDir}}/scripts/pandadoc.py templates --q <value>
```

## 所有命令

| 命令 | 说明 |
|---------|-------------|
| `documents` | 列出所有文档 |
| `document-get` | 获取文档详情 |
| `document-create` | 创建新文档 |
| `document-send` | 发送文档 |
| `document-status` | 获取文档状态 |
| `document-delete` | 删除文档 |
| `document-link` | 生成文档共享链接 |
| `templates` | 列出所有模板 |
| `template-get` | 获取模板详情 |
| `contacts` | 列出所有联系人 |
| `contact-create` | 创建新联系人 |
| `folders` | 列出所有文件夹 |
| `webhooks` | 列出所有 Webhook 设置 |

## 输出格式

所有命令默认以 JSON 格式输出。若需可读的格式输出，请添加 `--human` 参数。

```bash
python3 {{baseDir}}/scripts/pandadoc.py <command> --human
```

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{{baseDir}}/scripts/pandadoc.py` | 主要命令行工具（包含所有命令） |

## 致谢

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) | [agxntsix.ai](https://www.agxntsix.ai) 开发  
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi) 提供支持  
PandaDoc 是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。  

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)