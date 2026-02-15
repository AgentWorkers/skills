---
name: secretary
description: **为分类、日历和治理功能提供安全的 M365 自动化解决方案。**
metadata:
  version: 3.0
  requires:
    python_packages: ["msal", "requests", "python-dotenv"]
---

# 🛡️ 角色与逻辑  
我是一名以安全为首要原则的执行助理。我通过被委托的权限来操作，以确保仅能访问用户的数据。  
1. **行政事务**：处理高优先级的电子邮件以及协调日程安排。  
2. **数据管理**：自动识别过期的 OneDrive 数据。  
3. **沟通协作**：将警报信息安全地发布到 Teams 渠道中。  

# 🛠 命令接口  
- **邮件**：`python3 secretary_engine.py mail`（处理高优先级的邮件）  
- **日历**：`python3 secretary_engine.py calendar [email]`（查找会议时间）  
- **OneDrive**：`python3 secretary_engine.py drive`（列出孤立（未被使用的）文件）  
- **Teams**：`python3 secretary_engine.py teams [team_id] [channel_id] [msg]`（在指定的 Teams 渠道中发送消息）  

# 🏗 设置  
1. **应用注册**：创建一个 Azure Entra ID 应用程序，并将其设置为公共客户端（Public Client）。  
2. **权限设置**：授予被委托的权限，包括 `Mail.ReadWrite`、`Calendars.ReadWrite`、`Files.ReadWrite` 和 `ChatMessage.Send`。  
3. **环境变量**：在 `.env` 文件中配置 `SECRETARY_CLIENT_ID` 和 `SECRETARY_TENANT_ID`。