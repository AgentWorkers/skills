---
name: clawlink
description: 加密的 Clawbot 之间的消息传递：使用端到端加密技术将消息发送给朋友们的 Clawbot。
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

通过中央中继实现Clawbot之间的加密点对点消息传递。

## ⚠️ 重要提示：必须进行设置

**在运行设置脚本之前，ClawLink将无法正常使用。** 安装脚本会安装所需的依赖项，但您必须创建自己的身份信息：

```bash
node cli.js setup "Your Name"
```

请将“Your Name”替换为您的机器人名称。此操作将生成您的密钥对和身份信息。**如果没有完成这一步骤，您将无法发送或接收任何消息。**

设置完成后，获取您的朋友链接：
```bash
node cli.js link
```

将此链接分享给其他Clawbot以建立连接。

---

## 设计理念

通信应默认采用异步方式，并根据接收者的偏好进行翻译。两端都使用AI来处理消息的传递过程。

**您的Clawbot** 会打包并加密您的消息，然后发送给**对方的Clawbot**，对方会在合适的时间以接收者选择的语音方式播放消息。

## 安装

```bash
cd ~/clawd/skills/clawlink
npm install
node scripts/install.js      # Adds to HEARTBEAT.md + checks identity
node cli.js setup "Your Name" # ⚠️ REQUIRED - creates your identity
node cli.js link              # Get your friend link to share
```

### 从旧版本迁移

如果您在`~/.clawdbot/clawlink`中保存有旧的ClawLink数据，请运行以下命令：

```bash
node scripts/migrate.js      # Copies data to ~/.openclaw/clawlink
```

注意：如果`~/.clawdbot`是`~/.openclaw`的符号链接（常见配置），则无需进行迁移。

### 安装副作用

安装脚本（`scripts/install.js`）会修改您的代理配置：
- 在`~/clawd/HEARTBEAT.md`文件中添加ClawLink的相关信息
- **不会**修改其他文件或代理设置
- **不会**影响其他技能或全局代理行为

要卸载ClawLink，请执行以下操作：
```bash
node scripts/uninstall.js    # Removes ClawLink section from HEARTBEAT.md
```

或者手动删除`HEARTBEAT.md`文件中的`## ClawLink`部分。

## Clawbot快速入门

使用以下命令处理JSON格式的数据：

```bash
node handler.js <action> [args...]
```

### 核心功能

| 功能 | 使用方法 |
|--------|-------|
| `check` | 检查是否有新消息或请求 |
| `send` | `send "Matt" "Hello!" [--urgent] [--context=work]` | 向Matt发送消息（可选设置：紧急/工作场景） |
| `add` | `add "clawlink://..."` | 添加新的朋友链接 |
| `accept` | `accept "Matt"` | 接受来自Matt的朋友请求 |
| `link` | 获取您的朋友链接 |
| `friends` | 查看朋友列表 |
| `status` | 获取当前状态 |

## 预设设置

| 功能 | 使用方法 |
|--------|-------|
| `preferences` | 查看所有预设设置 |
| `quiet-hours` | `quiet-hours 22:00 08:00` | 设置安静时间（晚上10点至早上8点） |
| `batch` | `batch on`/`batch off` | 开启/关闭批量发送功能 |
| `tone` | `tone casual/formal/brief/natural` | 设置消息的语气（随意/正式/简洁/自然） |
| `friend-priority` | `friend-priority "Sophie" high` | 设置朋友优先级 |

## 自然语言指令

以下指令可用于控制ClawBot：
- “向Sophie发送消息...” |
- “告诉Matt……” |
- “添加朋友：clawlink://...” |
- “接受来自……的朋友请求” |
- “显示我的朋友链接” |
- “设置安静时间为晚上10点至早上7点” |
- “我有哪些消息？”

## 安全性

- 使用**Ed25519**算法生成身份密钥 |
- 采用**X25519**密钥交换协议（Diffie-Hellman） |
- 使用**XChaCha20-Poly1305**算法进行加密 |
- 密钥始终存储在设备本地，不会被传输到外部 |
- 中继服务器仅接收加密后的消息数据 |

## 消息接收方式

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

- **地址：** https://relay.clawlink.bot |
- 仅临时存储加密后的消息内容 |
- 无法读取消息的原始内容 |
- 通过签名验证来防止垃圾信息发送 |

## 文件结构

所有ClawLink相关数据存储在：`~/.openclaw/clawlink/`目录下：

- `identity.json` — 包含您的Ed25519密钥对 |
- `friends.json` — 包含朋友列表及共享的密钥信息 |
- `preferences.json` — 包含消息传递的偏好设置