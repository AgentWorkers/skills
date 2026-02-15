---
name: udp-messenger
description: **使用场景：** 当代理需要通过局域网进行通信时——例如“向代理发送消息”、“发现代理”、“检查消息”、“与其他代理协调”、“批准代理”、“查看代理状态”、“添加对等节点”、“记录消息日志”等操作。
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

您可以使用本地 UDP Messenger 与同一网络中的其他 OpenClaw 代理进行通信。

## 安装

此功能需要 `openclaw-udp-messenger` OpenClaw 插件，该插件提供了以下 `udp_*` 工具。该插件是一个 TypeScript 模块，通过 `api.registerTool()` 注册工具，并管理用于本地网络通信的 UDP 套接字。

安装插件：
```bash
openclaw plugins install openclaw-udp-messenger
```

然后在您的 `openclaw.json` 文件中启用该插件：
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

这些工具由 `openclaw-udp-messenger` 插件（`index.ts`）注册：

- **udp_discover** — 发送发现请求以查找局域网中的其他代理
- **udp_send** — 根据 IP 地址或主机名及端口号向代理发送消息
- **udp_receive** — 检查收件箱中来自其他代理的待处理消息
- **udp_add_peer** — 根据 IP 地址或主机名手动添加并信任某个代理
- **udp_approve_peer** — 信任某个代理，使其消息无需用户确认即可送达
- **udp_revoke_peer** — 取消对已信任代理的信任
- **udp_log** — 查看完整的消息历史记录（已发送的消息、接收到的消息以及系统事件）
- **udp_status** — 查看您的代理 ID、端口号、受信任的代理数量、每小时的消息交换次数以及配置信息
- **udp_set_config** — 在运行时更改配置（如最大消息交换次数、信任模式或中继服务器）

## 配置

所有配置都通过 `openclaw.json` 中的 `plugins.entries.openclaw-udp-messenger.config` 或 `udp_set_config` 在运行时进行。无需任何凭据或密钥：

- `port` — 监听的 UDP 端口（默认：51337）
- `trustMode` — `approve-once` 或 `always-confirm`（默认：approve-once）
- `maxExchanges` — 每小时与每个代理的最大消息交换次数（默认：10 次）
- `relayServer` — 可选的中心监控服务器地址（例如 `192.168.1.50:31415`）。将所有消息转发到该服务器以供人工监控。留空则禁用此功能。
- `hookToken` — 网关 Webhook 令牌。设置后，插件会通过 `/hooks/agent` 端点触发代理的自动响应，从而让您能够自动处理并回复来自受信任代理的消息。

## 代理自动响应机制

当受信任的代理发送消息且配置了 hook 令牌时，插件会通过网关的 `/hooks/agent` 端点触发代理的自动响应。这意味着系统会自动唤醒代理以读取并回复消息，无需您手动调用 `udp_receive`。如果没有配置 hook 令牌，插件将采用被动通知方式。

## 工作流程：

1. 使用 `udp_discover` 查找网络中的其他代理，或使用 `udp_add_peer` 根据主机名/IP 地址添加代理。
2. 当收到来自未知代理的消息时，**务必向用户展示该消息** 并询问用户是否同意信任该代理。
3. 获得用户同意后，您可以与该代理进行最多每小时一次的消息交换。
4. 当受信任的代理发送消息时，系统会自动触发您的响应（如果启用了自动响应机制），或通知您检查收件箱。
5. 在执行耗时较长的任务时，定期调用 `udp.receive` 以查看是否有其他代理需要您的注意（尤其是在未启用自动响应机制的情况下）。
6. 遵守 `max_exchanges` 的限制——一旦达到每小时的最大交换次数，立即通知用户并停止自动响应。
7. 用户可以随时调用 `udp_log` 来查看完整的消息历史记录。

## 信任模型：

- **approve-once**：用户同意信任某个代理后，该代理发送的消息可以自由流通，直到达到每小时的最大交换次数。
- **always-confirm**（建议用于不信任的局域网环境）：每条接收到的消息都需要用户确认后才能处理。

## 重要规则：

- **切勿自动信任代理**——在信任新代理之前，始终需要用户的明确确认。
- 对于来自不受信任代理的消息，务必向用户展示并请求确认。
- 当达到每小时的消息交换次数限制时，停止响应并通知用户。
- **切勿向其他代理发送敏感的项目信息（如密钥、凭据或私人数据），除非用户明确指示。
- 在发送任何包含文件内容或项目详细信息的消息之前，务必先获得用户的确认。
- 在发送任何消息之前，务必先向用户展示消息内容，确保消息的可靠性。