---
name: discord-toolkit
description: "错误：需要使用 `--action` 参数。当您需要使用 Discord 工具包的功能时，请使用该参数。该参数可在以下情况下触发：`discord toolkit`、`token`、`guild-id`、`channel-id`、`message`、`user-id`。"
---
# Discord 工具包

这是一个功能齐全的 Discord 机器人管理工具包，支持通过命令行使用 Discord REST API 和机器人令牌来发送消息、管理频道和角色、列出公会成员、创建富格式嵌入内容、管理反应效果以及自动化服务器管理任务。

## 产品描述

Discord 工具包允许您对 Discord 服务器进行完全的程序化控制：可以发送普通消息或富格式嵌入消息、管理频道（创建、删除、编辑）、列出和查询成员信息、管理角色、固定消息显示位置、添加反应效果以及执行各种服务器管理操作。该工具包支持格式化输出，便于与其他工具和自动化流程集成，非常适合用于通知机器人、服务器管理、社区工具开发以及 ChatOps 工作流程。

## 使用要求

- `list-guilds`：列出所有公会
- `list-channels`：列出所有频道
- `send-message`：发送消息
- `send-embed`：发送富格式嵌入内容
- `channel-messages`：在频道内发送消息
- `list-members`：列出所有成员
- `guild-info`：获取公会信息
- `get-user`：获取用户信息
- `create-channel`：创建新频道

**注意：** 需要在机器人设置中启用以下功能：** Server Members（服务器成员）和 Message Content（消息内容）。** 还需要使用适当的权限将机器人邀请到您的服务器。

## 可用命令

## 环境变量

| 变量        | 是否必填 | 说明                                      |
|------------|---------|-----------------------------------------|
| `DISCORD_BOT_TOKEN` | 是       | Discord 机器人令牌                          |
| `DISCORD_OUTPUT_FORMAT` | 否       | 输出格式：`table`、`json`、`markdown`                    |

## 使用示例

```bash
# Send a message
DISCORD_BOT_TOKEN=xxx discord-toolkit send 123456789 "Hello Discord! 🎮"

# Send a rich embed
DISCORD_BOT_TOKEN=xxx discord-toolkit embed 123456789 '{"title":"Server Status","description":"All systems operational","color":65280}'

# List channels
DISCORD_BOT_TOKEN=xxx discord-toolkit channels 987654321

# List members
DISCORD_BOT_TOKEN=xxx discord-toolkit members 987654321 100

# Add a role to a member
DISCORD_BOT_TOKEN=xxx discord-toolkit role add 987654321 111222333 444555666
```
---
💬 意见与功能请求：https://bytesagain.com/feedback
由 BytesAgain 提供支持 | bytesagain.com