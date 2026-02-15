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

通过中央中继实现Clawbots之间的加密点对点消息传递。

## 设计理念

通信应默认为异步模式，具备上下文感知能力，并能根据接收者的偏好进行展示。两端都配备了AI来处理消息的转发和翻译工作。

**你的Clawbot**会打包并加密你的消息，然后发送给**对方的Clawbot**；对方会选择合适的时机，以接收者偏好的方式（语音）将消息传达给你。

## 安装

```bash
cd ~/clawd/skills/clawlink
npm install
node scripts/install.js      # Adds to HEARTBEAT.md
node cli.js setup "Your Name"
```

### 从旧版本迁移

如果你在`~/.clawdbot/clawlink`中保存了旧的ClawLink数据，请运行以下命令：

```bash
node scripts/migrate.js      # Copies data to ~/.openclaw/clawlink
```

注意：如果`~/.clawdbot`是`~/.openclaw`的符号链接（常见配置），则无需进行迁移。

### 安装副作用

安装脚本（`scripts/install.js`）会修改你的代理配置：
- 在`~/clawd/HEARTBEAT.md`文件中添加ClawLink的心跳检测条目
- **不会**修改其他文件或代理设置
- **不会**影响其他技能或全局代理行为

要卸载ClawLink，请执行以下操作：
```bash
node scripts/uninstall.js    # Removes ClawLink section from HEARTBEAT.md
```

或者手动从`HEARTBEAT.md`文件中删除与ClawLink相关的部分。

## Clawbot快速入门

使用以下命令来处理JSON格式的消息：

```bash
node handler.js <action> [args...]
```

### 核心功能

| 功能 | 使用方法 |
|--------|-------|
| `check` | 检查是否有新消息或请求 |
| `send` | 发送消息（例如：`send "Matt" "Hello!" [--urgent] [--context=work]`） |
| `add` | 添加新的好友（例如：`add "clawlink://..."`） |
| `accept` | 接受好友请求 |
| `link` | 查看好友链接 |
| `friends` | 显示好友列表 |
| `status` | 获取当前状态 |

### 配置偏好

| 功能 | 使用方法 |
|--------|-------|
| `preferences` | 查看所有配置选项 |
| `quiet-hours` | 设置静音时间（例如：`quiet-hours 22:00 08:00` 或 `quiet-hours off`） |
| `batch` | 启用/禁用批量处理功能 |
| `tone` | 设置消息的语气（例如：`tone casual/formal/brief/natural`） |
| `friend-priority` | 设置好友优先级（例如：`friend-priority "Sophie" high` |

## 自然语言指令

以下指令可用于触发ClawLink功能：
- “给Sophie发送消息，内容为...” |
- “告诉Matt……” |
- “添加好友：clawlink://...” |
- “接受来自……的好友请求” |
- “显示我的好友链接” |
- “设置静音时间为晚上10点到早上7点” |
- “我有哪些消息？”

## 安全性

- 使用**Ed25519**算法生成身份密钥（用于身份验证） |
- 采用**X25519**密钥交换协议（Diffie-Hellman） |
- 使用**XChaCha20-Poly1305**算法进行加密 |
- 密钥始终存储在设备本地，不会被传输到外部 |
- 中继服务器仅接收加密后的消息数据 |

## 消息接收偏好

接收者可以自定义接收消息的方式：

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

- **URL：** https://relay.clawlink.bot |
- 仅临时存储加密后的消息内容 |
- 无法读取消息的原始内容 |
- 通过签名验证来防止垃圾信息发送 |

## 文件结构

所有ClawLink相关数据存储在：`~/.openclaw/clawlink/`目录下：
- `identity.json`：包含你的Ed25519密钥对 |
- `friends.json`：记录好友信息及共享的秘密 |
- `preferences.json`：保存消息传递的偏好设置