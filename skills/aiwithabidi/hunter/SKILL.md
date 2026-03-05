---
name: hunter
description: "Hunter.io — 一个集电子邮件查找、电子邮件验证、域名搜索、作者信息查询以及潜在客户管理功能于一体的工具。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🔍", "requires": {"env": ["HUNTER_API_KEY"]}, "primaryEnv": "HUNTER_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🔍 Hunter.io

Hunter.io 是一个集电子邮件查找、电子邮件验证、域名搜索、作者信息查询以及潜在客户管理功能于一体的工具。

## 必需条件

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `HUNTER_API_KEY` | ✅ | Hunter.io 的 API 密钥 |


## 快速入门

```bash
# Find emails for a domain
python3 {{baseDir}}/scripts/hunter.py domain-search --domain <value> --limit "10" --type <value>

# Find specific person's email
python3 {{baseDir}}/scripts/hunter.py email-finder --domain <value> --first-name <value> --last-name <value>

# Verify an email address
python3 {{baseDir}}/scripts/hunter.py email-verifier --email <value>

# Count emails for domain
python3 {{baseDir}}/scripts/hunter.py email-count --domain <value>

# List saved leads
python3 {{baseDir}}/scripts/hunter.py list-leads --limit "20" --offset "0"

# Create a lead
python3 {{baseDir}}/scripts/hunter.py create-lead --email <value> --first-name <value> --last-name <value> --company <value>

# Update a lead
python3 {{baseDir}}/scripts/hunter.py update-lead <id> --email <value> --first-name <value> --last-name <value>

# Delete a lead
python3 {{baseDir}}/scripts/hunter.py delete-lead <id>

# List lead lists
python3 {{baseDir}}/scripts/hunter.py list-leads-lists

# Get account info & usage
python3 {{baseDir}}/scripts/hunter.py get-account

# Find author of article
python3 {{baseDir}}/scripts/hunter.py author-finder --url <value>
```


## 输出格式

所有命令默认以 JSON 格式输出结果。


## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/hunter.py` | 主要命令行工具（所有功能集成在一个脚本中） |


## 致谢

该工具由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
相关视频：[YouTube](https://youtube.com/@aiwithabidi)  
GitHub 仓库：[https://github.com/aiwithabidi]  
该工具属于 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)