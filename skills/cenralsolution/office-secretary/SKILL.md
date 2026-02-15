---
name: secretary
description: **Secure M365 Assistant**  
用于问题分类（Triage）、日历协调（Calendar Coordination）以及企业管理（Governance）。
metadata:
  version: 3.1
  # FIX: Explicitly declare required environment variables for the registry
  env_vars:
    - SECRETARY_CLIENT_ID
    - SECRETARY_TENANT_ID
  requires:
    python_packages: ["msal", "requests", "python-dotenv"]
---

# 🛡️ 职责与工作逻辑  
我是一名以安全为首要原则的执行助理。我通过被委托的权限来操作，以确保仅能访问用户的数据。  
1. **行政工作**：处理高优先级的电子邮件并协调日程安排。  
2. **数据管理**：识别过时的 OneDrive 数据。  
3. **信息传递**：将警报安全地发布到 Teams 渠道中。  

# 🛠 命令接口  
- **邮件**：`python3 secretary_engine.py mail`（处理高优先级邮件）  
- **日历**：`python3 secretary_engine.py calendar [email]`（查找会议时间）  
- **OneDrive**：`python3 secretary_engine.py drive`（列出孤立（未被使用的）文件）  
- **Teams**：`python3 secretary_engine.py teams [team_id] [channel_id] [msg]`（在 Teams 中发布消息）  

# 🏗 设置流程  
1. **应用程序注册**：创建一个 Azure Entra ID 应用程序，并将其设置为公共客户端。  
2. **权限设置**：授予被委托的权限，包括 `Mail.ReadWrite`、`Calendars.ReadWrite`、`Files.ReadWrite` 和 `ChatMessage.Send`。  
3. **环境变量**：在 `.env` 文件中设置 `SECRETARY_CLIENT_ID` 和 `SECRETARY_TENANT_ID`。