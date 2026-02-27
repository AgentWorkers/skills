---
name: mee6
# A skill for controlling the Mee6 Discord bot (leveling, moderation, custom commands).
description: "通过 Discord 消息工具执行 Mee6 操作（频道=discord）。"
metadata:
  { "openclaw": { "emoji": "🤖", "requires": { "config": ["channels.discord.token"] } } }
---
# Mee6（Discord机器人）

使用`message`工具的方式与使用`discord`技能完全相同，但命令的目标是Mee6机器人。这个技能的存在纯粹是为了为代理提供一个关于Mee6常见操作以及机器人特定功能的参考。

* 请始终设置`channel: "discord"`。
* 消息应以服务器的前缀（通常是`!`）开头。
* 如有需要，可以通过ID或`@Mee6`来提及Mee6。
* 权限控制是通过与`discord`技能相同的`channels.discord.actions.*`配置来处理的；不需要额外的权限。

## 常见命令

- **查看等级** – `!level @user`
- **给予经验值** – `!give-xp @user <amount>`
- **创建角色** – `!role create <rolename>`
- **启用插件** – `!plugins enable <plugin-name>`
- **禁用插件** – `!plugins disable <plugin-name>`
- **设置前缀** – `!prefix <new-prefix>`

> 代理仅应在用户明确请求与Mee6机器人交互时发送相关命令。避免发送与Discord其他操作无关的原始命令；对于其他所有情况，请使用通用的`discord`技能。