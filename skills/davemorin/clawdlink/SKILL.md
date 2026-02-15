---
name: clawphone
description: 加密的 Clawdbot 之间的通信：使用端到端加密技术将消息发送给朋友们的 Clawdbot。
triggers:
  - clawphone
  - friend link
  - add friend
  - send message to
  - tell [name] that
  - message from
  - accept friend request
  - clawphone preferences
  - quiet hours
---

# ClawPhone

通过中央中继实现Clawdbots之间的加密点对点消息传递。

## 设计理念

通信应默认为异步方式，具备上下文感知能力，并能根据接收者的偏好进行消息呈现。两端都使用了AI技术来处理消息的转发和翻译。

**您的Clawdbot**会加密您的消息，然后将其发送给**对方的Clawdbot**；对方会选择合适的时机，以接收者偏好的方式（语音或文本）将消息传递给接收者。

## 安装

```bash
cd ~/clawd/skills/clawphone
npm install
node scripts/install.js      # Adds to HEARTBEAT.md
node cli.js setup "Your Name"
```

## Clawdbot快速入门

使用以下代码块处理JSON格式的输出：

```bash
node handler.js <action> [args...]
```

### 核心功能

| 功能 | 用法 |
|--------|-------|
| `check` | 检查是否有新消息或请求 |
| `send` | `send "Matt" "Hello!" [--urgent] [--context=work]` | 向Matt发送消息（可选设置紧急级别或上下文） |
| `add` | `add "clawphone://..."` | 添加新的好友（通过URL） |
| `accept` | `accept "Matt"` | 接受好友请求 |
| `link` | 获取自己的好友链接 |
| `friends` | 查看好友列表 |
| `status` | 查看当前状态 |

### 预设功能

| 功能 | 用法 |
|--------|-------|
| `preferences` | 查看所有预设设置 |
| `quiet-hours` | `quiet-hours 22:00 08:00` | 设置安静时间（晚上10点至早上8点） |
| `batch` | `batch on` | 启用批量发送功能 |
| `tone` | `tone casual/formal/brief/natural` | 设置消息的语气（随意/正式/简洁/自然） |
| `friend-priority` | `friend-priority "Sophie" high` | 设置好友优先级 |

## 自然语言指令（用于Clawdbot）

以下指令可以触发ClawPhone功能：

- “给Sophie发送一条消息，内容是...”  
- “告诉Matt……”  
- “添加好友：clawphone://...”  
- “接受来自……的好友请求”  
- “显示我的好友链接”  
- “将安静时间设置为晚上10点至早上7点”  
- “我有哪些消息？”

## 安全性

- 使用**Ed25519**算法生成身份密钥（用于身份验证）  
- 采用**X25519**密钥交换协议（Diffie-Hellman）进行安全通信  
- 使用**XChaCha20-Poly1305**算法进行加密  
- 密钥始终存储在设备本地，不会被传输到外部  
- 中继服务器仅存储加密后的消息数据  

## 消息接收偏好设置

接收者可以自定义消息的接收方式：

```json
{
  "schedule": {
    "quietHours": { "enabled": true, "start": "22:00", "end": "08:00" },
    "batchDelivery": { "enabled": false, "times": ["09:00", "18:00"] }
  },
  "delivery": {
    "allowUrgentDuringQuiet": true,
    "summarizeFirst": true
  },
  "style": {
    "tone": "casual",
    "greetingStyle": "friendly"
  },
  "friends": {
    "Sophie Bakalar": { "priority": "high", "alwaysDeliver": true }
  }
}
```

## 中继服务器

- **URL:** https://clawphone-relay.vercel.app  
- 仅临时存储加密后的消息内容  
- 无法读取消息的原始内容  
- 通过签名验证来防止垃圾信息  

## 文件结构

所有ClawPhone相关数据存储在：`~/.config/clawdbot/clawphone/`目录下：

- `identity.json`：您的Ed25519密钥对  
- `friends.json`：包含好友信息及共享的加密密钥  
- `preferences.json`：消息传递的偏好设置