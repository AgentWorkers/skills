---
name: intros
description: OpenClaw的社交网络。您的机器人可以找到相关的人，管理联系，并让您进行聊天——所有这些操作都可以在您现有的机器人平台上完成。
version: 1.5.2
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

这是一个集成在您的 OpenClaw 机器人中的社交网络。无需离开聊天界面，您就可以找到联合创始人、合作伙伴、导师和好友。

## 您将获得的功能

- **搜索功能**：可以按兴趣、技能或地理位置进行搜索；也可以让系统为您推荐合适的人。
- **隐私保护**：在双方都同意之前，您的信息将保持隐藏状态。
- **即时通讯**：通过您的机器人直接与联系人进行聊天。
- ** Telegram 通知**：当有人给您发消息、提出连接请求或接受您的连接时，系统会立即通知您。
- **每日使用限制**：每天最多查看 10 个个人资料和接收 3 个连接请求，以确保使用更加合理。

## 快速入门

1. 对您的机器人说 “Join Intros”，它会要求您选择一个用户名。
2. 将验证码发送到 Telegram 上的 @Intros_verify_bot 进行验证。
3. 对您的机器人说 “Create my Intros profile”，系统会引导您完成个人资料的创建。
4. 说 “Who should I connect with?”（我应该和谁建立联系？），系统就会开始为您推荐合适的人。

就这样，剩下的工作都由机器人来完成。

## 可用的命令

| 操作 | 对应的命令 |
|---|---|
| 加入社交网络 | “Join Intros” |
| 创建个人资料 | “Create my Intros profile” |
| 寻找合作伙伴 | “Find co-founders in Mumbai” 或 “Search AI engineers” |
| 获取推荐 | “Who should I connect with?” 或 “Suggest people” |
| 浏览所有用户资料 | “Browse profiles” |
| 与某人建立联系 | “Connect with sarah_bot” |
| 处理连接请求 | “Show connection requests” / “Accept john_bot” |
| 发送消息 | “Message sam_bot Hey, want to collaborate?” |
| 查看消息记录 | “Chat with sarah_bot” 或 “Show my conversations” |
| 查看使用限制 | “Show my limits” |
| 查看谁看过我的个人资料 | “Who viewed my profile?” |

---

## 设置（详细步骤）

### 第一步：注册
**重要提示**：在运行注册命令之前，请用户选择一个唯一的用户名（小写，不含空格，类似 Twitter 的用户名）。同时询问他们的 Telegram 机器人用户名（例如 @MyBot），这有助于在通知中显示 “Open Bot” 深链接按钮。

```bash
python3 ~/.openclaw/skills/intros/scripts/intros.py register --bot-id 'chosen_username' --bot-username 'MyBot'
```

### 第二步：验证
将验证码发送到 Telegram 上的 @Intros_verify_bot。这还将启用自动通知功能——您会收到关于新连接、新消息和每日推荐的建议的通知。

### 第三步：创建个人资料
```bash
python3 ~/.openclaw/skills/intros/scripts/intros.py profile create --name "Your Name" --interests "AI, startups" --looking-for "Co-founders" --location "Mumbai" --bio "Your bio here"
```

## 命令详解

### 个人资料管理
```bash
# Create/update profile
python3 ~/.openclaw/skills/intros/scripts/intros.py profile create --name "Name" --interests "AI, music" --looking-for "Collaborators" --location "City" --bio "About me"

# View my profile
python3 ~/.openclaw/skills/intros/scripts/intros.py profile me

# View someone's profile
python3 ~/.openclaw/skills/intros/scripts/intros.py profile view <bot_id>
```

### 搜索功能
```bash
# Free-text search (searches across name, interests, looking_for, location, bio)
python3 ~/.openclaw/skills/intros/scripts/intros.py search AI engineer Mumbai

# Browse all profiles (no query = newest first)
python3 ~/.openclaw/skills/intros/scripts/intros.py search

# Pagination
python3 ~/.openclaw/skills/intros/scripts/intros.py search AI --page 2

# Get recommended profiles (auto-matched based on YOUR profile)
python3 ~/.openclaw/skills/intros/scripts/intros.py recommend

# Legacy filters still work
python3 ~/.openclaw/skills/intros/scripts/intros.py search --interests "AI" --location "India"
```

### 查看访问者信息
```bash
# See who viewed your profile
python3 ~/.openclaw/skills/intros/scripts/intros.py visitors
```

### 建立联系
```bash
# Send connection request
python3 ~/.openclaw/skills/intros/scripts/intros.py connect <bot_id>

# View pending requests
python3 ~/.openclaw/skills/intros/scripts/intros.py requests

# Accept a request
python3 ~/.openclaw/skills/intros/scripts/intros.py accept <bot_id>

# Decline a request (silent)
python3 ~/.openclaw/skills/intros/scripts/intros.py decline <bot_id>

# View all connections
python3 ~/.openclaw/skills/intros/scripts/intros.py connections
```

### 即时通讯
建立联系后，您可以向联系人发送消息。

```bash
# Send a message to a connection (max 500 characters)
python3 ~/.openclaw/skills/intros/scripts/intros.py message send <bot_id> "Your message here"

# Read conversation with someone
python3 ~/.openclaw/skills/intros/scripts/intros.py message read <bot_id>

# List all conversations
python3 ~/.openclaw/skills/intros/scripts/intros.py message list
```

### 使用限制
```bash
# Check daily limits
python3 ~/.openclaw/skills/intros/scripts/intros.py limits
```

### 网页版个人资料
```bash
# Get link to web profile
python3 ~/.openclaw/skills/intros/scripts/intros.py web
```

## 使用示例

- 当用户说 “Join Intros” 时，系统会先询问 “请为这个社交网络选择一个唯一的用户名（小写，不含空格）” 和 “您的 Telegram 机器人用户名是什么？（例如 @MyBot）”，然后执行命令 `register --bot-id 'their_choice' --bot-username 'their_bot_username'`。
- 当用户说 “Create my Intros profile” 时，系统会引导您完成个人资料的创建。
- 当用户说 “Find co-founders” 时，系统会执行搜索联合创始人的命令。
- 当用户说 “Find people interested in AI” 时，系统会执行搜索对人工智能感兴趣的人的命令。
- 当用户说 “Find AI people in Mumbai” 时，系统会执行搜索位于孟买的对人工智能感兴趣的人的命令。
- 当用户说 “Who should I connect with?” 时，系统会执行推荐合适联系人的命令。
- 当用户说 “Suggest people for me” 时，系统会执行推荐合适联系人的命令。
- 当用户说 “Browse profiles” 时，系统会执行浏览所有用户资料的命令。
- 当用户说 “Connect with sarah_bot” 时，系统会执行与 sarah_bot 建立联系的命令。
- 当用户说 “Show connection requests” 时，系统会显示所有收到的连接请求。
- 当用户说 “Accept john_bot” 时，系统会执行接受 john_bot 的连接请求。
- 当用户说 “Show my connections” 时，系统会显示所有已建立的联系。
- 当用户说 “Show my limits” 时，系统会显示每日使用限制。
- 当用户说 “Message sam_bot Hello there!” 时，系统会执行向 sam_bot 发送消息的命令。
- 当用户说 “Send message to alice: Want to collaborate?” 时，系统会执行向 alice 发送消息的命令。
- 当用户说 “Read messages from john” 时，系统会显示与 john 的聊天记录。
- 当用户说 “Show my conversations” 时，系统会显示与所有联系人的聊天记录。

## 工作原理

- **API 服务器**：所有数据存储在 Intros 的后端服务器 `https://api.openbreeze.ai` 上（来源：[github.com/sam201401/intros](https://github.com/sam201401/intros)）。
- **注册**：在注册过程中，您需要提供机器人的 Telegram 用户名（通过参数 `--bot-username` 提供）。该信息仅用于在通知中显示 “Open Bot” 深链接按钮，不会读取任何本地配置文件。
- **数据持久化**：该技能会将您的 API 密钥和身份信息保存在 `~/.openclaw/data/intros/` 文件夹中（以纯文本 JSON 格式），这样在重新安装技能时也能恢复这些信息。删除该文件夹即可撤销保存的凭据。
- **自动恢复**：如果配置信息丢失（例如在重新安装后），系统会使用保存的身份文件重新注册，并恢复原有的凭据。
- **通知**：通知通过 Telegram 上的 @Intros_verify_bot 发送（服务器端处理，无需设置定时任务）。
- **环境变量**：`OPENCLAW_STATE_DIR`（可选）用于多实例环境，可覆盖 OpenClaw 的状态目录；`TELEGRAM_USER_ID`（可选）在未提供 `--telegram-id` 时作为备用参数使用。

## 安全性提示

**重要提示**：在构建命令时，务必将用户提供的值用单引号括起来，以防止 shell 注入攻击。单引号可以防止特殊字符被 shell 解释。

```bash
# Correct — single-quoted values
python3 ~/.openclaw/skills/intros/scripts/intros.py register --bot-id 'chosen_username'
python3 ~/.openclaw/skills/intros/scripts/intros.py connect 'some_user'
python3 ~/.openclaw/skills/intros/scripts/intros.py message send 'bob' 'Hello there!'
python3 ~/.openclaw/skills/intros/scripts/intros.py profile create --name 'Alice' --interests 'AI, startups'

# Wrong — unquoted or double-quoted user input
python3 ~/.openclaw/skills/intros/scripts/intros.py connect some_user
python3 ~/.openclaw/skills/intros/scripts/intros.py message send bob "$(echo injected)"
```

该脚本还会在服务器端验证所有 `bot_id` 参数（仅允许字母数字和下划线字符），作为额外的安全措施。

## 搜索类型

用户可以指定他们想要寻找的对象类型：
- 联合创始人
- 合作伙伴
- 导师
- 招聘对象
- 任意类型的人

## 隐私设置

- 默认情况下，用户的 Telegram 账号是私密的，只有在双方都同意建立联系后才会共享信息。
- 用户可以在个人资料设置中选择是否公开自己的 Telegram 账号。

## 通知机制

通知通过 Telegram 上的 @Intros_verify_bot 自动发送。验证完成后，您将收到以下类型的消息：
- **新消息**：当有人给您发消息时
- **连接请求**：当有人希望与您建立联系时
- **连接请求被接受**：当您的连接请求被接受时
- **每日推荐**：每天会收到一次推荐信息，提醒您查看新的推荐对象。

无需设置定时任务或中间件，系统会每 60 秒自动检查一次通知。

如果您没有收到通知，请发送 `/start` 到 @Intros_verify_bot 以重新链接您的账户。