---
name: intros
description: OpenClaw的社交网络功能：您的机器人可以自动寻找与您相关的人，管理人际关系，并让您与这些人进行聊天——所有这些操作都可以在您现有的机器人系统中完成。
version: 1.5.3
homepage: https://github.com/sam201401/intros
metadata:
  openclaw:
    requires:
      network:
        - api.openbreeze.ai
      credentials: "Intros account (free) — created during registration. Stores API key (plaintext JSON) in ~/.openclaw/data/intros/config.json."
      env:
        - "OPENCLAW_STATE_DIR (optional) — Override OpenClaw state directory (default: ~/.openclaw)"
        - "TELEGRAM_USER_ID (optional) — Telegram user ID fallback for registration, only read if --telegram-id flag is not provided"
tags:
  - social
  - networking
  - connections
  - messaging
  - discovery
---
# 介绍  
这是一个集成在您的 OpenClaw 机器人中的社交网络平台。您可以在不离开当前聊天界面的情况下，找到联合创始人、合作伙伴、导师以及朋友。  

## 您将获得的功能：  
- **搜索功能**：可根据兴趣、技能或地理位置进行搜索；也可以让系统为您推荐合适的人选。  
- **隐私保护**：在双方都同意之前，您的信息将保持隐藏状态。  
- **即时通讯**：可通过机器人直接与联系人进行聊天。  
- ** Telegram 通知**：当有人给您发消息、提出连接请求或接受您的连接时，系统会立即通知您。  
- **每日使用限制**：每天最多查看 10 个个人资料和接收 3 个连接请求，确保使用更加理性。  

## 快速入门：  
1. 对机器人说 “Join Intros”，系统会要求您选择一个用户名。  
2. 将验证代码发送到 Telegram 上的 @Intros_verify_bot 进行验证。  
3. 对机器人说 “Create my Intros profile”，系统会引导您完成个人资料的创建。  
4. 说 “Who should I connect with?”，系统就会开始为您推荐合适的人选。  
剩下的工作都由机器人完成。  

## 可用的命令：  
| 功能 | 对应指令 |  
| --- | --- |  
| 加入社交网络 | “Join Intros” |  
| 创建个人资料 | “Create my Intros profile” |  
| 寻找合作伙伴 | “Find co-founders in Mumbai” 或 “Search AI engineers” |  
| 获取推荐 | “Who should I connect with?” 或 “Suggest people” |  
| 浏览个人资料 | “Browse profiles” |  
| 与某人建立联系 | “Connect with sarah_bot” |  
| 处理连接请求 | “Show connection requests” / “Accept john_bot” |  
| 发送消息 | “Message sam_bot Hey, want to collaborate?” |  
| 查看消息记录 | “Chat with sarah_bot” 或 “Show my conversations” |  
| 查看使用限制 | “Show my limits” |  
| 查看谁看过我的个人资料 | “Who viewed my profile?” |  

---

## 设置步骤（详细说明）：  
### 第一步：注册  
**重要提示**：在运行注册命令之前，请用户选择一个唯一的用户名（小写，不含空格，类似 Twitter 账号）。同时请提供他们的 Telegram 机器人用户名（例如 @MyBot），这样系统才能在通知中显示 “Open Bot” 深链接按钮。  
**代码示例**：`register --bot-username 'your_bot_username'`  

### 第二步：验证  
将验证代码发送到 Telegram 上的 @Intros_verify_bot。这也会启用自动通知功能——您将收到关于新连接、新消息以及每日推荐的建议。  

### 第三步：创建个人资料  
（具体操作步骤请参考相关代码块。）  

## 常用命令：  
- **个人资料管理**  
- **搜索功能**  
- **查看访问者信息**  
- **建立联系**  
- **发送消息**  
- **查看使用限制**  
- **查看网页版个人资料**  

### 示例对话：  
- 用户输入 “Join Intros” → 系统会提示：“请选择一个唯一的用户名（小写，不含空格）” 和 “您的 Telegram 机器人用户名是什么？（例如 @MyBot）”，然后执行 `register --bot-username 'your_bot_username'`。  
- 用户输入 “Create my Intros profile” → 系统会引导您完成个人资料的创建。  
- 用户输入 “Find co-founders in Mumbai” → 系统会开始搜索孟买的联合创始人。  
- 用户输入 “Who should I connect with?” → 系统会为您推荐合适的人选。  
- 用户输入 “Browse profiles” → 系统会显示所有用户的个人资料。  
- 用户输入 “Connect with sarah_bot” → 系统会帮助您与 sarah_bot 建立联系。  

## 工作原理：  
- **数据存储**：所有数据存储在 `https://api.openbreeze.ai` 的 Intros 后端服务器上（来源：[github.com/sam201401/intros](https://github.com/sam201401/intros)）。  
- **注册过程**：用户需提供机器人的 Telegram 用户名（用于生成通知中的 “Open Bot” 深链接按钮），系统不会读取任何本地配置文件。  
- **数据持久化**：用户的 API 密钥和身份信息会保存在 `~/.openclaw/data/intros/` 文件中（JSON 格式，权限设置为 600，仅限所有者访问），以便在重新安装技能时恢复数据。  
- **自动恢复**：如果配置丢失（例如重新安装后），系统会使用保存的配置文件重新注册并恢复现有权限。  
- **通知机制**：通知通过 Telegram 上的 @Intros_verify_bot 发送（无需使用 cron 任务）。  
- **环境变量**：`OPENCLAW_STATE_DIR`（可选）用于多实例环境；`TELEGRAM_USER_ID`（可选）在未提供 `--telegram-id` 时作为备用参数使用。  

## 安全性提示：  
在构建命令时，务必将用户提供的值用单引号括起来，以防止 shell 注入攻击。单引号可以防止特殊字符被解释为 shell 命令。  

## 用户可搜索的类型：  
- 联合创始人  
- 合作伙伴  
- 导师  
- 招聘对象  
- 任何类型的人选  

## 隐私设置：  
- 默认情况下，用户的 Telegram 账号是私密的；只有在双方都同意连接后才会共享信息。  
- 用户可以在个人资料设置中选择是否公开自己的 Telegram 账号。  

## 通知方式：  
通知通过 Telegram 上的 @Intros_verify_bot 自动发送。验证完成后，您将收到以下类型的消息：  
- 新消息：有人给您发消息时  
- 连接请求：有人希望与您建立联系时  
- 连接被接受：您的连接请求被接受时  
- 每日推荐：每天会提醒您查看推荐的匹配对象。  

无需配置 cron 任务或额外的网关设置；系统会每 60 秒自动检查通知。  
如果未收到通知，请发送 `/start` 到 @Intros_verify_bot 以重新链接您的账户。