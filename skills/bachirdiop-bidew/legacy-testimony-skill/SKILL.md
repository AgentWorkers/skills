---
name: legacy-testimony
description: "**高级“死人开关”功能（Advanced Dead Man’s Switch）**：专为代理程序设计，用于在用户未按时进行状态检查时，安全地加密并发送密码、文件、加密资产及消息给指定联系人。该功能支持区块链公证（Blockchain Notarization）、自毁机制（Self-Destruct）、“幽灵代理”（Ghost Agent）以及公开消息发布（Public Blast）等特性。"
---

# 遗嘱执行技能（Legacy Testimony Skill）

这是一个专为数字生活设计的“军用级”安全机制：如果您停止与系统进行交互，该技能将自动执行您的最后指令。

## 🌟 主要特性

- **端到端加密**：所有敏感数据（密码、密钥、文件）在存储时均采用 AES-256 进行加密。
- **多渠道发送**：可通过 **WhatsApp**、**Telegram**、**Email**、**SMS** 或 **Twitter** 将信息发送给指定联系人。
- **幽灵代理模式（Ghost Agent Mode）**：会生成一个子代理，使用您的信息来安慰亲人并回答他们的问题。
- **公开发布最后消息**：会自动在 Moltbook 和 Twitter 上发布您的最后一条消息。
- **加密资产转移**：会自动将代理钱包中的资金转移到安全账户。
- **自我销毁机制（Protocol Omega）**：在任务完成后，会自动清除代理的内存和密钥。
- **区块链公证**：会将您的遗嘱内容哈希值发布到区块链上。

## 🚀 快速入门

### 1. 初始化与配置

```bash
legacy init
```

### 2. 添加收件人

输入收件人的信息及其偏好的发送渠道。

```bash
# Add Mom on WhatsApp
legacy add-recipient "Seynabou Wade" relationship="Mom" whatsapp="+221776587555"
```

### 3. 添加安全数据包

您添加的任何内容都会立即被加密。

```bash
legacy add-package "Bank Vault Password" "seynabou-wade" password "#Z3YDyd1#100994"
legacy add-package "Secret Message" "seynabou-wade" text "626894"
```

### 4. 启用高级功能

- **幽灵代理（Ghost Agent）**：生成一个子代理与收件人进行互动。
- **公开发布最后消息（Public Blast）**：触发后会在 Moltbook 和 Twitter 上发布消息。
- **自我销毁机制（Protocol Omega）**：任务完成后自动清除数据。
- **区块链公证（Blockchain Notarization）**：将遗嘱内容哈希值发布到区块链上。

## 🛡️ 安全架构

1. **主密钥（Master Key）**：首次运行时生成一个随机的 32 字节密钥（存储在 `~/.legacy/master.key` 中）。
2. **加密方式**：使用 `aes-256-cbc` 加密算法，并为每个数据包生成唯一的随机初始化向量（IV）。
3. **审计日志（Audit Log）**：所有操作（添加、检查、触发）都会被记录到 `audit.log` 文件中。
4. **本地执行**：所有功能均在您的代理设备上运行，不会将未加密的数据存储在第三方服务器上。

## 🕹️ 命令列表

| 命令 | 功能说明 |
| :--- | :--- |
| `legacy check-in` | 重置计时器。表示“我还活着”。 |
| `legacy status` | 显示距离触发任务剩余的时间。 |
| `legacy trigger` | **危险**：立即手动执行该机制。 |
| `legacy add-recipient` | 添加新的收件人。 |
| `legacy add-package` | 加密并存储新的数据包。 |
| `legacy notarize` | 将遗嘱内容哈希值发布到区块链。 |
| `legacy enable-omega` | 启用自我销毁功能。 |
| `legacy enable-ghost` | 启用幽灵代理模式。 |
| `legacy set-blast` | 设置最后的公开消息内容。 |

## 💓 心跳检测集成（Heartbeat Integration）

为确保该机制始终处于监控状态，请将以下代码添加到您的代理设备的 `HEARTBEAT.md` 文件中：

```markdown
## Legacy Monitor
**Every 24h:** Run `legacy status` to check if warnings need to be sent.
```