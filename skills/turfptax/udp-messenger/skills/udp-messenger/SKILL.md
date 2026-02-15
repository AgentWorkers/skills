---
name: udp-messenger
description: **使用场景：**  
当代理需要通过本地网络进行通信时，可以使用以下功能：  
- “向代理发送消息”  
- “发现代理”  
- “检查是否有消息”  
- “与其他代理协调”  
- “批准代理”  
- “查询代理状态”  
- “添加代理”  
- “消息日志”
metadata:
  openclaw:
    requires:
      bins:
        - node
    homepage: https://github.com/turfptax/openclaw-udp-messenger
    install:
      npmSpec: openclaw-udp-messenger
      localPath: https://github.com/turfptax/openclaw-udp-messenger.git
---

# UDP Messenger — 本地代理通信

您可以使用本地UDP Messenger与同一网络中的其他OpenClaw代理进行通信。

## 安装

此功能需要`openclaw-udp-messenger`插件，该插件提供了以下`udp_*`工具。该插件是一个TypeScript模块，通过`api.registerTool()`注册工具，并管理用于本地网络通信的UDP套接字。

请安装该插件：
```bash
openclaw plugins install openclaw-udp-messenger
```

然后在您的`openclaw.json`文件中启用它：
```json
{
  "plugins": {
    "entries": {
      "openclaw-udp-messenger": {
        "enabled": true,
        "config": {
          "port": 51337,
          "trustMode": "approve-once",
          "maxExchanges": 10
        }
      }
    }
  }
}
```

## 可用工具

这些工具由`openclaw-udp-messenger`插件（`index.ts`）注册：

- **udp_discover** — 发送发现请求，以查找局域网中的其他代理
- **udp_send** — 根据IP地址或主机名及端口向代理发送消息
- **udp_receive** — 检查收件箱中来自其他代理的待处理消息
- **udp_add_peer** — 手动添加并信任某个代理（通过IP地址或主机名）
- **udp_approve_peer** — 信任某个代理，使其消息无需用户确认即可被接收
- **udp_revoke_peer** — 取消对已信任代理的信任
- **udp_log** — 查看完整的消息历史记录（已发送的消息、接收的消息以及系统事件）
- **udp_status** — 查看您的代理ID、使用的端口、已信任的代理数量、每小时的消息交换次数以及配置信息
- **udp_set_config** — 在运行时更改配置（如`max_exchanges`、`trust_mode`或`relay_server`）

## 配置

所有配置均通过`openclaw.json`中的`plugins.entries.openclaw-udp-messenger.config`文件或`udp_set_config`在运行时进行设置。无需任何凭证或密钥：

- `port` — 监听的UDP端口（默认：51337）
- `trustMode` — `approve-once`或`always-confirm`（默认：approve-once）
- `maxExchanges` — 每小时与每个代理的最大消息交换次数（默认：10次）
- `relayServer` — 可选的中央监控服务器地址（例如`192.168.1.50:31415`）：将所有消息转发到该服务器进行人工监控。留空则禁用此功能。
- `hookToken` — 网关Webhook令牌。设置此令牌后，插件会通过网关的`/hooks/agent`端点触发代理的响应机制，使您能够自动处理并回复来自受信任代理的消息。

## 代理响应机制

当受信任的代理发送消息且配置了`hookToken`时，插件会通过网关的`/hooks/agent`端点触发代理的响应。这意味着系统会自动唤醒代理以读取并回复消息——无需您手动调用`udp_receive`。如果没有配置`hookToken`，插件将采用被动通知方式。

**重要提示：** 启用代理响应机制需要同时满足`hooks.enabled: true`和`openclaw.json`中存在`hookToken`的条件。如果日志中显示`HTTP 405`错误，说明`hooks.enabled`未设置——请在配置文件中添加`"hooks": { "enabled": true, "token": "..." }`。

## 工作流程：

1. 使用`udp_discover`查找网络中的其他代理，或使用`udp_add_peer`按主机名/IP地址添加代理。
2. 当收到来自未知代理的消息时，**务必向用户展示该消息并询问是否要信任该代理**。
3. 被信任后，您可以与该代理进行消息交换（最多每小时交换10次）。
4. 当受信任的代理发送消息时，系统会自动触发您的响应（如果启用了响应机制），或者通知您查看收件箱。
5. 在执行耗时较长的任务时，定期检查`udp_receive`以确认是否有其他代理需要您的关注（特别是当未启用响应机制时）。
6. 遵守`max_exchanges`的限制——一旦达到每小时的最大交换次数，需通知用户并停止自动回复。
7. 用户可以随时使用`udp_log`查看完整的消息历史记录。

## 信任模型：

- **approve-once**：用户信任代理后，消息可以自由流通，直到达到每小时的最大交换次数。
- **always-confirm**（建议用于不受信任的局域网环境）：每条接收到的消息都需要用户确认后才能处理。

## 重要规则：

- **切勿自动信任代理**——在信任新代理之前，务必获得用户的明确确认。
- 对于来自不受信任代理的消息，务必向用户显示并请求确认。
- 一旦达到每小时的消息交换次数限制，立即停止响应并通知用户。
- **切勿向其他代理发送敏感项目信息（如机密数据、凭证或私人信息），除非用户明确指示。
- 在发送包含文件内容或项目详细信息的消息之前，务必先获得用户的确认。
- 在发送任何消息之前，务必先向用户展示消息内容。