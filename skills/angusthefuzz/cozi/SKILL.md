---
name: cozi
description: 与 Cozi Family Organizer 进行交互（管理购物清单、待办事项清单以及物品信息）。这是一个用于家庭事务管理的非官方 API 客户端。
metadata:
  openclaw:
    emoji: 📋
    requires:
      bins: [node]
      env: [COZI_EMAIL, COZI_PASSWORD]
---
# Cozi Skill

这是一个非官方的 Cozi Family Organizer API 客户端，用于管理购物清单和待办事项列表。

⚠️ **重要提示：** 本工具使用了非官方的 API（通过逆向工程实现的）。Cozi 可能会随时更改该 API 的接口。

## 环境变量

请将这些环境变量设置到您的代理程序的 `.env` 文件（位于 `~/.openclaw/.env`）中，或者创建一个专门用于本技能的 `.env` 文件（位于 `~/.openclaw/skills/cozi/.env`）：

- `COZI_EMAIL` — 您的 Cozi 账户邮箱
- `COZI_PASSWORD` — 您的 Cozi 账户密码

该脚本仅会从 `.env` 文件中读取 `COZI_EMAIL` 和 `COZI_PASSWORD` 变量；其他变量将被忽略。

## 命令

```bash
# Lists
node ~/.openclaw/skills/cozi/scripts/cozi.js lists                    # Show all lists
node ~/.openclaw/skills/cozi/scripts/cozi.js list <listId>            # Show specific list
node ~/.openclaw/skills/cozi/scripts/cozi.js add <listId> "item text"  # Add item
node ~/.openclaw/skills/cozi/scripts/cozi.js check <listId> <itemId>   # Mark complete
node ~/.openclaw/skills/cozi/scripts/cozi.js uncheck <listId> <itemId> # Mark incomplete
node ~/.openclaw/skills/cozi/scripts/cozi.js remove <listId> <itemId>  # Remove item
node ~/.openclaw/skills/cozi/scripts/cozi.js new-list "title" [type]   # Create list (shopping|todo)
node ~/.openclaw/skills/cozi/scripts/cozi.js delete-list <listId>      # Delete list

# Calendar
node ~/.openclaw/skills/cozi/scripts/cozi.js calendar [year] [month]   # Show month (defaults to current)
node ~/.openclaw/skills/cozi/scripts/cozi.js cal [year] [month]         # Alias
node ~/.openclaw/skills/cozi/scripts/cozi.js add-appt YYYY-MM-DD HH:MM HH:MM "subject" [location] [notes]
node ~/.openclaw/skills/cozi/scripts/cozi.js remove-appt <year> <month> <apptId>
```

## 示例

```bash
# See all lists and their items
node ~/.openclaw/skills/cozi/scripts/cozi.js lists

# Add milk to the shopping list
node ~/.openclaw/skills/cozi/scripts/cozi.js add abc123 "Organic milk"

# Mark item as bought
node ~/.openclaw/skills/cozi/scripts/cozi.js check abc123 item456

# Create a new todo list
node ~/.openclaw/skills/cozi/scripts/cozi.js new-list "Weekend chores" todo

# View this month's calendar
node ~/.openclaw/skills/cozi/scripts/cozi.js cal

# View specific month
node ~/.openclaw/skills/cozi/scripts/cozi.js cal 2026 3

# Add an appointment
node ~/.openclaw/skills/cozi/scripts/cozi.js add-appt 2026-02-20 14:00 15:30 "Doctor appointment" "Rochester General"
```

## 会话缓存

该脚本会将您的会话令牌缓存到 `~/.openclaw/skills/cozi/.session.json` 文件中，以避免每次调用时都需要重新进行身份验证。令牌会过期，必要时系统会自动重新进行身份验证。

## API 详情

- 基本 URL：`https://rest.cozi.com/api/ext/2207`
- 认证方式：使用用户名/密码登录生成的令牌（Bearer token）
- 列表相关接口：`/api/ext/2004/{accountId}/list/`

本工具基于 [cozi-api-client](https://github.com/BrandCast-Signage/cozi-api-client) 和 [py-cozi](https://github.com/Wetzel402/py-cozi) 开发。