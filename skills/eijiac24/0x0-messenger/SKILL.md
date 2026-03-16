---
name: 0x0-messenger
description: "使用一次性PIN码发送和接收点对点（P2P）消息。无需服务器，也无需注册账户。适用于代理之间的消息传递、审批流程以及通知功能。"
homepage: https://0x0.contact
metadata: {"openclaw":{"requires":{"bins":["c0x0","node"],"env":[]},"emoji":"📡"}}
---
# 0x0 Messenger

只需安装一次：`npm install -g @0x0contact/c0x0`，然后执行 `c0x0 init`。

## 核实您的身份

```bash
c0x0 whoami          # your number + active PINs
```

## 创建一个 PIN 并分享它

```bash
c0x0 pin new --label "deploy-bot"     # creates e.g. "a3f9"
c0x0 pin new --expires 1h             # auto-expires after 1 hour
c0x0 pin new --once                   # expires after first message received
```

分享方式：`0x0://0x0-816-8172-8198/a3f9`

## 发送消息

```bash
c0x0 send 0x0-293-4471-0038 a3f9 "build passed, ready to deploy"
```

如果对方处于离线状态，消息将排队等待 72 小时。

## 交互式通道（标准输入/标准输出，采用 JSON 格式）

```bash
c0x0 pipe 0x0-293-4471-0038 a3f9
```

发送消息：
```json
{"type": "message", "content": "deploy to prod? (yes/no)"}
{"type": "disconnect"}
```
接收消息：
```json
{"type": "connected", "peer": "0x0-293-4471-0038"}
{"type": "message", "from": "0x0-293-4471-0038", "content": "yes"}
```

## 监听传入的消息

```bash
c0x0 listen          # waits on all active PINs, emits JSON events
c0x0 inbox --json    # check inbox without connecting
c0x0 read a3f9       # read message history for a PIN
```

## 从任何人那里接收消息（使用公共 PIN）

```bash
c0x0 pin new --public --label "inbox"   # share this PIN openly
c0x0 requests                            # list incoming threads
c0x0 approve <shortKey> "welcome!"       # reply → private channel created
```

## 联系人管理

```bash
c0x0 contact add 0x0://0x0-293-4471-0038/a3f9
c0x0 contact list
```

## 使用完毕后撤销 PIN

```bash
c0x0 pin revoke a3f9
```