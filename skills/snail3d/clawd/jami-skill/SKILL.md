---
name: jami
description: 通过 Jami (GNU Ring) 进行自动化呼叫。适用于简单的 VoIP 呼叫、消息传递以及无需基础设施的点对点通信。
---

# Jami呼叫功能

使用Jami（免费、去中心化、点对点的VoIP服务）自动化电话呼叫和消息发送。

## 快速入门

### 安装
```bash
# macOS - Download from jami.net or use Homebrew cask (if available)
brew install --cask jami

# Or download directly from https://jami.net/download/

# Linux
sudo apt install jami  # Debian/Ubuntu
```

### 设置
1. 安装Jami应用程序
2. 创建/注册Jami账户
3. 获取您的Jami ID（通常是一个长Hex字符串）
4. 在Clawdbot中进行配置

### 发起呼叫
```bash
jami account list                    # List registered accounts
jami call <jami_id> <contact_id>    # Initiate call
jami hangup <call_id>               # End call
```

### 发送消息
```bash
jami message send <contact_id> "Hello"
```

## 命令行接口（CLI）使用

### 账户管理
```bash
jami account list                    # List all accounts
jami account info <account_id>       # Show account details
jami account register <username>     # Register new account
jami account enable <account_id>     # Enable account
jami account disable <account_id>    # Disable account
```

### 呼叫功能
```bash
# Initiate call
jami call <account_id> <contact_id>

# List active calls
jami call list

# Get call status
jami call status <call_id>

# End call
jami hangup <call_id>

# Set volume
jami audio volume <volume_percent>
```

### 联系人管理及消息发送
```bash
# Add contact
jami contact add <account_id> <contact_id>

# List contacts
jami contact list <account_id>

# Send message
jami message send <contact_id> "Message text"

# Receive messages (daemon mode)
jami message listen
```

## 自动化呼叫示例

### 简单的出站呼叫
```bash
#!/bin/bash
ACCOUNT_ID="your_jami_account_id"
CONTACT_ID="contact_jami_id"

jami call $ACCOUNT_ID $CONTACT_ID
sleep 30  # Call duration
jami hangup
```

### 带消息的呼叫
```bash
#!/bin/bash
ACCOUNT_ID="your_account"
CONTACT_ID="contact_id"

# Call
jami call $ACCOUNT_ID $CONTACT_ID

# Send message during/after call
jami message send $CONTACT_ID "Automated call from Clawdbot"

# Hangup after message
sleep 5
jami hangup
```

### 接听来电
```bash
jami daemon --listening  # Start daemon
jami call list          # Monitor calls
```

## Clawdbot集成

### 配置（详见TOOLS.md）
```
## Jami Configuration
- Account ID: [your_jami_account_hex_id]
- Contacts: 
  - name: contact_jami_id (hex string)
  - name: contact_jami_id
```

### 在Clawdbot中的使用
```
"Make a call to [contact]"
"Send message to [contact]"
"Hang up current call"
"List my Jami contacts"
```

## Jami的工作原理

- **去中心化**：无需中央服务器，呼叫直接在用户之间进行。
- **DHT（分布式哈希表）**：用于查找联系人。
- **安全性**：内置加密机制。
- **免费**：完全免费，无需账户或订阅。
- **开源**：源代码公开可用。

## 限制

- 双方都需要安装Jami（或使用兼容的VoIP网络）。
- 不支持传统电话号码（使用Jami ID进行通信）。
- 需要互联网连接（依赖VoIP服务）。
- 音质受网络状况影响。
- 无内置的自动语音应答系统（需通过脚本实现）。

## 高级功能：自托管

对于需要更复杂的自动化呼叫功能，您可以自行托管SIP网关：
```bash
# Asterisk bridge (connect Jami to traditional phone systems)
# FreeSWITCH (lightweight alternative)
```

但对于简单的呼叫需求，使用Jami的CLI即可满足。

## 配置资源

- `scripts/jami_caller.sh`：通过CLI发起呼叫
- `scripts/jamilistener.sh`：监听来电
- `references/jami_api.md`：Jami CLI使用手册
- `assets/jami_ids.txt`：本地联系人数据库