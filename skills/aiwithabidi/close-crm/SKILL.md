---
name: close-crm
description: "Close CRM — 用于管理潜在客户、联系人、销售机会、任务以及各种业务活动。这是一款集成了电话和电子邮件功能的销售客户关系管理（Sales CRM）工具。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "📞", "requires": {"env": ["CLOSE_API_KEY"]}, "primaryEnv": "CLOSE_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 📞 Close CRM

这是一款集成了电话和电子邮件功能的销售CRM系统，用于管理潜在客户（leads）、联系人（contacts）、销售机会（opportunities）以及任务（tasks）。

## 主要功能

- **潜在客户（Leads）**：列出潜在客户、创建新客户、查看详细信息。
- **联系人（Contacts）**：管理联系人的信息。
- **销售机会（Opportunities）**：跟踪销售机会及其价值。
- **任务（Tasks）**：创建和管理任务。
- **活动（Activities）**：查看活动日志。

## 系统要求

| 变量          | 是否必需 | 说明                          |
|--------------|---------|---------------------------------------------|
| `CLOSE_API_KEY`    | ✅      | Close CRM的API密钥/令牌                |
|              |         |                                      |

## 快速入门

```bash
python3 {baseDir}/scripts/close-crm.py leads --limit 10
python3 {baseDir}/scripts/close-crm.py lead-create "Acme Corp" --contact-name John --contact-email john@acme.com
python3 {baseDir}/scripts/close-crm.py opportunities
python3 {baseDir}/scripts/close-crm.py me
```

## 开发者信息

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 共同开发  
[YouTube频道](https://youtube.com/@aiwithabidi) | [GitHub仓库](https://github.com/aiwithabidi)  
该工具是 **AgxntSix Skill Suite** 的一部分，专为OpenClaw代理设计。

📅 **需要帮助为您的企业设置OpenClaw吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)