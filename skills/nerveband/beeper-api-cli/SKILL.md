---
name: beeper-api-cli
description: 通过 Beeper CLI 读取和发送消息。支持 WhatsApp、Telegram、Signal、Instagram、Twitter/X、LinkedIn、Facebook Messenger 等平台。
metadata: {"clawdbot":{"emoji":"💬","os":["darwin","linux"]}}
---

# beeper-api-cli

这是一个专为大型语言模型（LLM）设计的封装工具，它基于Beeper CLI，能够读取和发送消息到所有已连接的聊天网络。

## ⚠️ 重要提示：消息发送政策

**🚨 未经用户明确许可，严禁发送任何消息！**

**所有消息发送必须遵循的协议：**
1. **始终先显示完整的消息草稿** - 显示全部内容
2. **等待用户的明确口头许可** - 例如：“发送吧”、“看起来不错”等
3. **切勿擅自发送消息** - 即使用户只是说了“起草消息”
4. **适用于所有平台**：WhatsApp、Telegram、Signal、Instagram、Twitter、Facebook、LinkedIn等
5. **没有任何例外** - 这适用于新消息、回复和转发

此规则不可协商，并适用于所有与Beeper相关的发送命令。

## 快速入门

### 第一步：从Beeper桌面应用程序获取令牌
```
1. Open Beeper Desktop
2. Settings → Advanced → API
3. Enable API access
4. Copy the Bearer token
```

### 第二步：设置环境变量
```bash
# REQUIRED: Set your token
export BEEPER_TOKEN="paste-your-token-here"

# OPTIONAL: Override default localhost URL
export BEEPER_API_URL="http://[::1]:23373"  # Default
```

### 第三步：使用CLI
```bash
# Use the skill wrapper (recommended)
~/clawd/skills/beeper-api-cli/beeper.sh chats list --output json

# Or use the binary directly
/Users/ashrafali/clawd/beeper-api-cli/beeper chats list --output json
```

**⚠️ 重要提示：** 如果未设置`BEEPER_TOKEN`，所有命令都会因“未经授权”而失败。

## 先决条件

### 1. 必须运行Beeper桌面应用程序
CLI需要连接到Beeper桌面应用程序的本地API服务器。

### 2. 在Beeper桌面应用程序中启用API访问
**⚠️ 必须先配置API令牌！**
1. 打开**Beeper桌面应用程序**
2. 转到**设置 → 高级 → API**
3. **启用API访问**
4. **生成并复制Bearer令牌**
5. （可选）配置允许的IP地址
   - 默认情况下：仅允许`localhost`（127.0.0.1 / ::1）
   - 如果从远程机器运行CLI，请将其IP地址添加到Beeper的设置中

### 第三步：设置环境变量
在CLI能够正常工作之前，必须设置令牌：

```bash
# REQUIRED: Set your token from Beeper Desktop
export BEEPER_TOKEN="your-token-from-beeper-settings"

# OPTIONAL: Override API URL (default: http://[::1]:23373)
export BEEPER_API_URL="http://[::1]:23373"
```

**获取令牌的位置：**
- Beeper桌面应用程序 → 设置 → 高级 → API → 复制Bearer令牌

**重要提示：**
- ❌ 如果未设置`BEEPER_TOKEN`，CLI将无法工作
- ⚠️ 默认API地址是`localhost`（`http://[::1]:23373`）
- 🔒 如果从其他机器访问，请：
  1. 将该机器的IP地址添加到Beeper的设置中
  2. 更新`BEEPER_API_URL`以使用正确的主机IP地址

## 命令

### 列出所有聊天记录
```bash
# JSON output (LLM-friendly)
~/clawd/skills/beeper-api-cli/beeper.sh chats list --output json

# Human-readable text
~/clawd/skills/beeper-api-cli/beeper.sh chats list --output text

# Markdown format
~/clawd/skills/beeper-api-cli/beeper.sh chats list --output markdown
```

**示例JSON输出：**
```json
[
  {
    "id": "!wcn4YMCOtKUEtxYXYAq1:beeper.local",
    "title": "beeper-api-cli - Lion Bot",
    "type": "group",
    "network": "Telegram",
    "unreadCount": 15
  }
]
```

### 获取特定聊天记录
```bash
~/clawd/skills/beeper-api-cli/beeper.sh chats get <chat-id> --output json
```

### 从聊天记录中读取消息
```bash
# Get last 50 messages (default)
~/clawd/skills/beeper-api-cli/beeper.sh messages list --chat-id <chat-id>

# Get specific number of messages
~/clawd/skills/beeper-api-cli/beeper.sh messages list --chat-id <chat-id> --limit 20 --output json
```

**示例JSON输出：**
```json
[
  {
    "id": "42113",
    "chatID": "!wcn4YMCOtKUEtxYXYAq1:beeper.local",
    "senderName": "ClawdBot",
    "text": "Hello world!",
    "timestamp": "2026-01-19T22:17:38.000Z",
    "isSender": true
  }
]
```

### 发送消息
```bash
# ⚠️ REQUIRES USER APPROVAL FIRST - see Message Sending Policy above
~/clawd/skills/beeper-api-cli/beeper.sh send --chat-id <chat-id> --message "Your message here"
```

**示例输出：**
```json
{
  "success": true,
  "message_id": "msg_123",
  "chat_id": "!wcn4YMCOtKUEtxYXYAq1:beeper.local"
}
```

### 搜索消息
```bash
# Search across all chats
~/clawd/skills/beeper-api-cli/beeper.sh search --query "keyword" --limit 10 --output json
```

### 自动发现API地址
```bash
~/clawd/skills/beeper-api-cli/beeper.sh discover
```

## LLM工作流程

### 查找聊天记录并发送消息
```bash
# 1. List chats to find the right one
CHATS=$(~/clawd/skills/beeper-api-cli/beeper.sh chats list --output json)

# 2. Extract chat ID (using jq)
CHAT_ID=$(echo "$CHATS" | jq -r '.[] | select(.title | contains("Project")) | .id')

# 3. Send message
~/clawd/skills/beeper-api-cli/beeper.sh send --chat-id "$CHAT_ID" --message "Update ready!"
```

### 获取对话上下文
```bash
# Get recent messages for context
~/clawd/skills/beeper-api-cli/beeper.sh messages list --chat-id <chat-id> --limit 20 --output json | jq
```

### 监控未读消息
```bash
# Get all chats with unread count
~/clawd/skills/beeper-api-cli/beeper.sh chats list --output json | jq '.[] | select(.unreadCount > 0) | {title, network, unread: .unreadCount}'
```

## 输出格式

### JSON（默认格式 - 优化后的LLM格式）
- 结构化数据，便于解析
- 非常适合程序化使用
- 可通过`jq`进行过滤

### 文本格式（人类可读）
```
ID: !wcn4YMCOtKUEtxYXYAq1:beeper.local
Title: beeper-api-cli - Lion Bot
Type: group
Network: Telegram
Unread: 15
```

### Markdown格式（用于文档）
```markdown
## beeper-api-cli - Lion Bot

- **ID**: !wcn4YMCOtKUEtxYXYAq1:beeper.local
- **Type**: group
- **Network**: Telegram
- **Unread**: 15
```

## 聊天记录ID格式

不同平台使用不同的ID格式：

- **Telegram**：`!wcn4YMCOtKUEtxYXYAq1:beeper.local`
- **WhatsApp**：电话号码格式（例如，`15551234567@s.whatsapp.net`
- **Signal**：电话号码（例如，`+15551234567`
- **Instagram/Twitter**：平台特定的ID

使用`chats list`命令来获取您聊天记录的确切格式。

## 环境变量

### 必须设置的配置项

**在使用CLI之前，必须设置以下环境变量：**

#### BEEPER_TOKEN（必需）
```bash
export BEEPER_TOKEN="your-bearer-token-from-beeper-desktop"
```

**获取令牌的方法：**
1. 打开Beeper桌面应用程序
2. 转到设置 → 高级 → API
3. 启用API访问
4. **复制设置中显示的Bearer令牌**
5. 将其设置为环境变量

**如果没有这个令牌，CLI将返回“未经授权”的错误。**

#### BEEPER_API_URL（可选）
```bash
export BEEPER_API_URL="http://[::1]:23373"  # Default value
```

**默认行为：**
- 使用`http://[::1]:23373`（IPv6下的localhost）
- 当CLI与Beeper桌面在同一台机器上运行时，此地址有效

**何时需要更改：**
- 从**远程机器**运行CLI时
- Beeper桌面位于不同的主机上时
- 使用自定义端口时

**如果从远程机器运行：**
1. 找到运行Beeper桌面应用程序的机器的IP地址
2. 在Beeper桌面应用程序 → 设置 → 高级 → API中添加该远程机器的IP地址
3. 将`BEEPER_API_URL`设置为：`http://<beeper-host-ip>:23373`

**远程访问示例：**
```bash
export BEEPER_API_URL="http://192.168.1.100:23373"
export BEEPER_TOKEN="your-token-here"
```

### Skill封装工具的行为

Skill封装工具（`beeper.sh`）将：
- ✅ 使用环境变量中的`$BEEPER_TOKEN`（您必须设置这个变量！）
- ✅ 如果未设置`BEEPER_TOKEN`，则默认使用`http://[::1]:23373`
- ❌ 如果未设置`BEEPER_TOKEN`，将会导致错误

## 故障排除

### “连接被拒绝”
```bash
# Check if Beeper Desktop is running
ps aux | grep -i beeper

# Start Beeper Desktop
open -a "Beeper Desktop"  # macOS
```

### “未经授权”或“令牌无效或缺失”

**这意味着您尚未设置`BEEPER_TOKEN`，或者令牌无效。**

**解决方法：**
```bash
# 1. Check if token is set
echo $BEEPER_TOKEN

# If empty or wrong, get a new token from Beeper Desktop:
# - Open Beeper Desktop
# - Settings → Advanced → API
# - Enable API if not already enabled
# - Copy the Bearer token shown
# - Set it in your environment:

export BEEPER_TOKEN="paste-the-token-here"

# Test it works:
~/clawd/skills/beeper-api-cli/beeper.sh chats list
```

**重要提示：**
- 令牌是在**Beeper桌面应用程序的设置**中生成的，而不是在这个CLI中生成的
- **必须从设置 → 高级 → API中准确复制令牌**
- 没有有效的令牌，**所有命令都无法执行**
- 除非在Beeper的设置中重新生成，否则令牌不会过期

### “聊天记录未找到”
```bash
# List all chats to find correct ID
~/clawd/skills/beeper-api-cli/beeper.sh chats list --output text | grep -i "search-term"
```

### 远程访问（CLI与Beeper桌面位于不同的机器上）

**如果您想从不同的计算机运行CLI：**

**1. 配置Beeper桌面应用程序以允许远程访问：**
```
- Open Beeper Desktop (on the machine running Beeper)
- Settings → Advanced → API
- Find the "Allowed IP Addresses" section
- Add the IP address of the machine running the CLI
- Example: 192.168.1.50
```

**2. 将`BEEPER_API_URL`设置为指向远程机器：**
```bash
# On the machine running the CLI:
export BEEPER_API_URL="http://<beeper-desktop-ip>:23373"
export BEEPER_TOKEN="your-token"

# Example:
export BEEPER_API_URL="http://192.168.1.100:23373"
```

**默认行为（仅限localhost）：**
- 默认URL：`http://[::1]:23373`（IPv6下的localhost）
- 仅当CLI与Beeper桌面在同一台机器上运行时有效
- **除非在Beeper的设置中配置了允许的IP地址，否则无法进行远程访问**

## 示例

### 示例1：检查未读消息
```bash
#!/bin/bash
BEEPER="$HOME/clawd/skills/beeper-api-cli/beeper.sh"

# Get chats with unread messages
$BEEPER chats list --output json | \
  jq -r '.[] | select(.unreadCount > 0) | "\(.title) (\(.network)): \(.unreadCount) unread"'
```

### 示例2：读取最近的消息
```bash
#!/bin/bash
BEEPER="$HOME/clawd/skills/beeper-api-cli/beeper.sh"
CHAT_ID="!wcn4YMCOtKUEtxYXYAq1:beeper.local"

# Get last 10 messages in readable format
$BEEPER messages list --chat-id "$CHAT_ID" --limit 10 --output text
```

### 示例3：搜索并回复消息
```bash
#!/bin/bash
BEEPER="$HOME/clawd/skills/beeper-api-cli/beeper.sh"

# Search for mentions
RESULTS=$($BEEPER search --query "@clawdbot" --limit 5 --output json)

# Process results and respond (LLM integration point)
echo "$RESULTS" | jq
```

## 与Clawdbot集成

当从Clawdbot工具中使用该工具时，环境变量已经配置好了：

```bash
# Direct usage from exec tool
~/clawd/skills/beeper-api-cli/beeper.sh chats list --output json
```

Skill封装工具会处理：
- ✅ 自动配置`BEEPER_API_URL`和`BEEPER_TOKEN`
- ✅ 检查所需的环境变量是否已设置
- ✅ 透明地传递所有CLI参数

## 二进制文件位置

- **Skill封装工具**：`~/clawd/skills/beeper-api-cli/beeper.sh`
- **Beeper CLI二进制文件**：`/Users/ashrafali/clawd/beeper-api-cli/beeper`
- **源代码**：https://github.com/nerveband/beeper-api-cli

## 特点

✅ 仅支持读写操作（与其他工具不同）
✅ 优化后的JSON输出格式，适合LLM处理
✅ 提供人类可读的文本和Markdown格式
✅ 自动发现Beeper桌面应用程序的API
### 跨平台二进制文件（macOS、Linux、Windows）
✅ 支持环境变量配置
✅ 提供详细的错误信息
✅ 适用于Unix管道操作

## 注意事项

- 该工具需要Beeper桌面应用程序正在运行
- 必须在Beeper桌面应用程序的设置中启用API访问
- 令牌存储在Clawdbot的配置文件中（已自动配置）
- 可访问所有连接到Beeper的聊天网络（WhatsApp、Telegram、Signal等）
- 使用JSON格式的输出进行LLM处理，使用文本格式供人类阅读

## 版本

最新版本（来自源代码的开发者构建）