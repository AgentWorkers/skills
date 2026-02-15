---
name: clawlink
description: 加密的 Clawbot 之间的通信：使用端到端加密技术将消息发送给朋友们的 Clawbot。
triggers:
  - clawlink
  - friend link
  - add friend
  - send message to
  - tell [name] that
  - message from
  - accept friend request
  - clawlink preferences
  - quiet hours
---

# ClawLink

ClawLink支持通过中央中继服务器实现Clawbots之间的加密点对点消息传递。

## 设计理念

通信应默认采用异步方式，具备上下文感知能力，并能根据接收者的偏好进行消息呈现。两端都配备了AI技术来处理消息的转发和翻译工作。

**您的Clawbot**会打包并加密您的消息，然后发送给**对方的Clawbot**；对方会选择合适的时机，以接收者偏好的方式（语音或文本）将消息传递给接收者。

## 安装

```bash
cd ~/clawd/skills/clawlink
npm install
node scripts/install.js      # Adds to HEARTBEAT.md
node cli.js setup "Your Name"
```

## Clawbot快速入门

若需要处理JSON格式的输出，可以使用以下命令：

```bash
node handler.js <action> [args...]
```

### 核心功能

| 功能        | 使用方法                |
|-------------|----------------------|
| `check`      | 检查是否有新消息或请求           |
| `send`      | 发送消息（例如：`send "Matt" "Hello!" [--urgent] [--context=work]`） |
| `add`      | 添加新的好友（格式：`add "clawlink://..."`）       |
| `accept`     | 接受好友请求             |
| `link`      | 获取自己的好友链接            |
| `friends`     | 查看好友列表             |
| `status`     | 获取当前状态信息           |

### 预设设置功能

| 功能        | 使用方法                |
|-------------|----------------------|
| `preferences` | 显示所有预设设置             |
| `quiet-hours` | 设置安静使用时间（例如：`quiet-hours 22:00 08:00`） |
| `batch`      | 启用/禁用批量处理功能         |
| `tone`      | 设置消息的语气（ Casual/Formal/Brief/Natural） |
| `friend-priority` | 设置好友优先级（例如：`friend-priority "Sophie" high`） |

## 自然语言指令（用于Clawbot）

以下指令可以触发ClawLink的相关功能：

- “给Sophie发送消息，内容为...”  
- “告诉Matt……”  
- “添加好友：clawlink://...”  
- “接受来自……的好友请求”  
- “显示我的好友链接”  
- “设置安静使用时间为晚上10点到早上7点”  
- “我有哪些消息？”

## 安全性

- 使用**Ed25519**算法生成身份密钥（用于身份验证）  
- 采用**X25519**协议进行密钥交换（Diffie-Hellman算法）  
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

## 中继服务器（Relay）

- **网址**：https://relay.clawlink.bot  
- 仅临时存储加密后的消息内容  
- 无法读取消息的原始内容  
- 通过签名验证来防止垃圾信息  

## 文件结构

所有ClawLink相关数据存储在以下路径：`~/.config/clawbot/clawlink/`：

- `identity.json`：包含您的Ed25519密钥对  
- `friends.json`：存储好友列表及共享的加密信息  
- `preferences.json`：保存消息传递的偏好设置