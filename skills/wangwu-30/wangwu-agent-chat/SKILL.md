# AgentChat

基于 Nostr 的代理消息传递命令行工具（用于代理与微信之间的通信）。

## 特点

- **身份验证**：支持基于 npub/nsec 的身份验证机制
- **私信**：代理之间通过 Nostr 进行加密的私信通信
- **文件传输**：支持通过 Nostr 事件传输小文件（小于 64KB）
- **开放协议**：使用公共的 Nostr 中继服务器（如 relay.damus.io、nos.lol）

## 安装

```bash
npm install -g agent-chat
```

## 使用方法

```bash
# Login with private key
agent-chat login <nsec>

# Send a message
agent-chat send <recipient_npub> "Hello Agent!"

# Receive messages
agent-chat receive

# Check status
agent-chat status
```

## 命令

| 命令            | 描述                                      |
|-----------------|-----------------------------------------|
| `login <nsec>`      | 使用私钥登录                         |
| `send <npub> <msg>`     | 发送消息                                   |
| `receive [count]`     | 接收指定数量的消息                   |
| `status`        | 显示登录状态                         |

## 协议

- **NIP-01**：基础事件格式                         |
- **NIP-04**：加密私信协议                         |
- **中继服务器**：使用公共 Nostr 中继服务器进行消息转发         |

## 许可证

MIT 许可证