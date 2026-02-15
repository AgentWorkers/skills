---
name: OpenClaw Minecraft
version: 0.1.0
specialty: minecraft-control
category: tools
description: 通过 Mineflayer 控制器 API，利用 JSON 操作和基于 Cron 表达式的自动化机制来控制 Minecraft 机器人。
---

# Mineflayer控制器技能

使用此技能通过控制器API创建和控制Minecraft机器人。控制器仅执行JSON格式的指令。切勿将API密钥或其他敏感信息发送给控制器。机器人会在本地执行大型语言模型（LLM）的推理，并仅发送相应的操作指令。

## 首先进行注册（开放注册）
如果启用了开放注册功能，机器人可以自行生成访问令牌：
```bash
curl -sS -X POST "https://56eb-125-246-120-211.ngrok-free.app/v1/auth/open/register" \
  -H "Content-Type: application/json" \
  -d '{"agentName":"andy"}'
```

建议：将响应结果保存在`memory/mc-auth.json`文件中，并在后续请求中重复使用该`accessToken`。

## 要求
- 基础URL：`https://56eb-125-246-120-211.ngrok-free.app/v1`
- `MC_CONTROLLER_TOKEN`（机器人专属的JWT令牌）

要获取JWT令牌，操作员需要使用管理员密钥调用`POST /v1/auth/register`接口，并将返回的`accessToken`分享给机器人。令牌可以通过`POST /v1/auth/refresh`接口进行更新。

如果您不希望共享管理员密钥，控制器可以提供`POST /v1/auth/proxy/register`接口（该接口支持白名单和速率限制功能）。在这种情况下，机器人需要使用`proxyKey`来请求访问令牌。

如果启用了开放注册功能（`POST /v1/auth/open/register`），机器人无需使用`proxyKey`即可请求访问令牌。但这种方式安全性较低，仅应在您允许公开访问的情况下使用。

## 安全规则
- 绝不要将LLM API密钥发送给控制器。
- 仅控制由您的令牌授权的机器人。
- 除非有必要中断正在运行的任务，否则建议使用`queue: queue`模式。

## 工作流程
1. 确保机器人存在；如果不存在，请先创建它。
2. 将机器人连接到Minecraft服务器。
3. 读取机器人的当前状态。
4. 发送操作指令。
5. 监查任务状态或订阅相关事件。

## 自主循环
对于自主运行模式，重复以下步骤：
1. `GET /bots/{botId}/state`（获取机器人状态）
2. 如果`metadata.currentTaskId`已设置，稍作等待后继续循环。
3. 确定一组安全的操作指令（5到10条），并通过`POST /bots/{botId}/act-batch`发送。
4. 根据需要使用`mode: until`或`mode: loop`模式来控制操作的执行（每条指令可设置`timeoutMs`超时时间）。

## Cron任务集成
该项目使用Gateway cron（而非heartbeat）来实现自主循环功能。

安装此技能后，请确保：
- 将工作区的`CRON_PROMPT.md`文件替换为`skills/openclaw-minecraft/CRON_PROMPT.md`（无论是否存在原有文件）。
- 设置一个每30秒执行一次的Cron任务，该任务会指示机器人执行`CRON_PROMPT.md`文件中的指令。

## API接口说明

### 创建机器人
```bash
curl -sS -X POST "https://56eb-125-246-120-211.ngrok-free.app/v1/bots" \
  -H "Authorization: Bearer $MC_CONTROLLER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"botId":"<botId>","username":"<botId>"}'
```

### 连接机器人
```bash
curl -sS -X POST "https://56eb-125-246-120-211.ngrok-free.app/v1/bots/<botId>/connect" \
  -H "Authorization: Bearer $MC_CONTROLLER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"host":"127.0.0.1","port":25565,"version":"1.21.9"}'
```

### 读取机器人状态
```bash
curl -sS -X GET "https://56eb-125-246-120-211.ngrok-free.app/v1/bots/<botId>/state" \
  -H "Authorization: Bearer $MC_CONTROLLER_TOKEN"
```

### 发送批量操作指令（循环执行）
```bash
curl -sS -X POST "https://56eb-125-246-120-211.ngrok-free.app/v1/bots/<botId>/act-batch" \
  -H "Authorization: Bearer $MC_CONTROLLER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "actions":[
      {
        "action":"chat",
        "params":{"message":"hello"},
        "mode":"loop",
        "intervalMs":2000,
        "maxIterations":3
      }
    ]
  }'
```

### 发送批量操作指令（直到完成）
```bash
curl -sS -X POST "https://56eb-125-246-120-211.ngrok-free.app/v1/bots/<botId>/act-batch" \
  -H "Authorization: Bearer $MC_CONTROLLER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "actions":[
      {
        "action":"move_to",
        "params":{"x":10,"y":64,"z":-12},
        "mode":"until",
        "stopCondition":{"type":"reach_position","radius":1.5},
        "timeoutMs":60000
      }
    ]
  }'
```

## 操作指南
- 将自然语言指令转换为JSON格式的批量操作指令。
- 如果目标需要多个步骤，请按顺序将它们包含在同一批指令中。
- 每批指令应包含5到10条操作。
- 对于需要持续执行的操作（如导航、重复任务），使用`mode: until`模式。
- 对于周期性任务（如扫描、聊天等），使用`mode: loop`模式。
- 仅支持以下操作指令：`chat`、`move_to`、`move_relative`、`move`、`dig`、`place`、`equip`、`use_item`、`attack`、`follow`、`jump`。

## 已知限制
- 目前仅支持JSON格式的数据传输；不支持媒体文件或附件。
- 由于网络连接问题或机器人缺少所需物品，某些操作可能会失败。