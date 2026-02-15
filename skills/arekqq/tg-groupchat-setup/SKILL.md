---
name: telegram-groupchat-setup
description: >
  Configure a MoltBot agent to participate in a Telegram group chat.
  Automates adding the group to the allowlist, setting mention patterns,
  and configuring sender permissions — all via a single gateway config patch.
  Use when the user wants to set up their bot in a Telegram group,
  enable cross-bot communication, or configure group mention gating.

---

# Telegram群组聊天设置

本技能用于自动化配置MoltBot代理在Telegram群组中的运行。

## 功能说明

1. 将Telegram群组添加到网关的允许列表中，并设置`requireMention: true`。
2. 配置`groupAllowFrom`，指定允许发送消息的用户ID或@用户名。
3. 通过Telegram Bot API自动检测机器人的名称和@用户名。
4. 设置`mentionPatterns`，使机器人能够响应其名称和@用户名的提及。
5. 应用配置更改并重启网关。

## 先决条件（手动步骤）

在运行此技能之前，用户需要完成以下操作：
1. **创建Telegram群组**，并将机器人添加到该群组中。
2. 在@BotFather中禁用隐私模式：
   进入`/mybots` → 选择机器人 → 机器人设置 → 群组隐私 → 关闭隐私模式
   （详情请参阅`references/telegram-privacy-mode.md`）
3. 知道群组的ID（Telegram群组的ID为负数）。
4. 知道被允许触发机器人的用户ID或@用户名。

## 使用方法

用户需要提供以下信息：
- `group_id`：Telegram群组的ID（例如：`-1001234567890`）
- `allowed_users`：可以触发机器人的Telegram用户ID或@用户名列表

示例命令：
> “在我的Telegram群组`-1001234567890`中设置机器人。允许用户`123456789`和`@some_user`向我发送消息。”

## 实现步骤

### 第1步：检测机器人信息

运行检测脚本以获取机器人的名称和@用户名：

```bash
bash skills/groupchat-setup/scripts/detect_bot_info.sh
```

该脚本从网关配置中读取机器人令牌，并返回机器人的`name`和`username`。
如果脚本不可用，则从网关配置的`channelsTelegram.botToken`中提取机器人令牌，并调用`https://api.telegram.org/bot<TOKEN>/getMe`来获取这些信息。

### 第2步：构建提及模式

根据检测到的机器人信息，构建提及模式：
- `@<username>`（例如：`@my_awesome_bot`）
- `<name>`（小写形式）（例如：`mybot`）
- `@<name>`（小写形式）（例如：`@mybot`）

去除重复项。这些模式是区分大小写的正则表达式。

### 第3步：应用配置更改

使用`gateway`工具，执行`action: "config.patch"`命令来应用配置更改：

```json
{
  "channels": {
    "telegram": {
      "groups": {
        "<group_id>": {
          "requireMention": true
        }
      },
      "groupAllowFrom": ["<user1>", "<user2>"]
    }
  },
  "messages": {
    "groupChat": {
      "mentionPatterns": ["@bot_username", "bot_name", "@bot_name"]
    }
  }
}
```

**注意：** 如果`groupAllowFrom`或`mentionPatterns`已有值，请将其合并（不要覆盖原有值）。首先使用`gateway action: "config.get"`读取当前配置，合并数组后再进行更新。

### 第4步：确认设置

网关重启后，向群组发送测试消息以确认设置是否成功：

> “✅ 机器人已配置完成！当有人提及我的名称时，我会做出响应。允许发送消息的用户：[列表]。”

## 注意事项

- `requireMention: true`表示机器人仅在被明确提及时才会响应，不会对所有消息进行响应。
- `groupAllowFrom`限制了可以触发机器人的发送者。如果没有设置此选项，来自未知发送者的消息可能会被忽略。
- `groupPolicy: "allowlist"`是Telegram的默认设置——只有明确列出的群组才会被允许。
- 隐私模式是Telegram端面的设置，无法通过API更改。用户需要在@BotFather中进行配置。
- 对于包含多个机器人的群组（例如两个MoltBot代理），每个机器人都需要在其自己的网关上独立执行此设置。