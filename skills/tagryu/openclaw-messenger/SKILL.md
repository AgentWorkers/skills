---
name: openclaw-messenger
description: 在 OpenClaw 实例之间发送和接收消息。当您需要与另一台机器上的 OpenClaw 代理进行通信、向朋友的 OpenClaw 发送消息、管理 OpenClaw 联系人或设置实例间消息传递时，可以使用此功能。该功能支持联系人管理、发送 ping 请求以及基于 Webhook 的消息监听。
---
# OpenClaw Messenger

用于向其他 OpenClaw 实例发送消息并管理联系人。

## 快速入门

```bash
# 연락처 추가
node scripts/messenger.js contacts add --name "친구봇" --url "ws://192.168.1.50:18789" --token "abc123" --desc "친구의 OpenClaw"

# 메시지 보내기
node scripts/messenger.js send --to "친구봇" --message "안녕! 나는 Tames야" --from "Tames"

# 직접 URL로 보내기
node scripts/messenger.js send --url "ws://host:port" --token "token" --message "Hello!"

# 핑 테스트
node scripts/messenger.js ping --to "친구봇"

# 연락처 목록
node scripts/messenger.js contacts list
```

## 命令

- `send` — 发送消息（`--to`：指定联系人；`--url`/`--token`：直接指定目标地址或令牌）
- `contacts list` — 查看联系人列表
- `contacts add` — 添加联系人（`--name`、`--url`、`--token`、`--desc`）
- `contacts remove` — 删除联系人（`--name`）
- `ping` — 测试连接（`--to` 或 `--url`）
- `listen` — 启动消息接收服务器（`--port`，默认为 19900）

## 工作原理

1. 需要知道目标 OpenClaw 实例的 Gateway WebSocket URL 和令牌。
2. 通过 WebSocket 连接到目标实例，并以系统事件的形式发送消息。
3. 消息会作为系统事件被插入到目标实例的会话中。

## 安全性

- 令牌存储在 `contacts.json` 文件中（禁止外部访问）。
- 只有当对方同意共享令牌时，才能发送消息。
- 如果 Gateway 使用的是 loopback 绑定，则无法从外部访问该实例（需要使用 Tailscale 等工具）。

## 中继模式（类似 Kakao Chat 的功能 — 推荐！）

通过中继服务器，在不交换 IP 和令牌的情况下，仅使用 ID 来发送消息：

```bash
# 릴레이 서버 설정 (공개 서버)
node scripts/relay-client.js setup --relay https://circuit-website-revealed-detail.trycloudflare.com

# 등록
node scripts/relay-client.js register --id my-id --name "내 이름" --secret 비밀키

# 메시지 보내기
node scripts/relay-client.js send --to 상대ID --message "안녕!"

# 받은 메시지 확인
node scripts/relay-client.js poll

# 실시간 수신
node scripts/relay-client.js listen

# 사용자 목록
node scripts/relay-client.js users
```

## 所需依赖

- `ws` npm 包（在 skill 目录中运行 `npm install ws`）