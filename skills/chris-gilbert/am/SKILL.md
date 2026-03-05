---
name: am — Agent Messenger
description: >
  当用户或代理需要执行以下操作时，应使用此技能：  
  - “向另一个代理发送消息”  
  - “发送加密的私信”  
  - “检查是否有新消息”  
  - “监听传入的消息”  
  - “设置代理身份”  
  - “添加中继代理”  
  - “获取我的公钥”  
  - “分享我的公钥”  
  - “与其他代理进行通信”  
  - “向另一个代理发送消息”  
  - “建立安全的代理通信机制”  
  - “通过 Nostr 与其他代理协调”。  
  本文档提供了使用 `am` CLI 进行 NIP-17 加密代理间通信的完整指南。
version: 0.1.0
---
# am — 代理消息传递工具（Agent Messenger）

`am` 是一个命令行工具（CLI），用于通过 Nostr 协议实现代理之间的端到端（E2E）加密通信。每个代理都持有一对 secp256k1 密钥。消息采用 NIP-17 加密格式进行传输，因此中继操作员无法查看发送者身份、接收者信息或消息内容。该工具不提供任何交互式提示，默认输出格式为 JSON，非常适合程序化使用。

## 先决条件

请确认 `am` 已经安装：

```bash
am --version
```

如果未安装，请从源代码进行构建：

```bash
git clone https://github.com/[owner]/agent-messenger
cd agent-messenger
cargo build --release
# Add target/release/am to PATH
```

## 首次使用设置

以下是三个步骤，帮助您快速开始使用 `am`：

**1. 生成代理身份：**

```bash
am identity generate --name default
```

执行该命令后，系统会生成一个代理身份。请保存生成的 `npub` 公钥地址，并将其分享给需要与该代理通信的其他代理或人员。

**2. 添加至少一个中继节点：**

```bash
am relay add wss://relay.damus.io
```

为了提高消息传输的可靠性，可以添加多个中继节点：

```bash
am relay add wss://nos.lol
am relay add wss://relay.nostr.band
```

**3. 验证设置是否正确：**

```bash
am identity show
am relay list
```

## 发送消息

**发送消息：**

```bash
am send --to <npub> "message content"
```

**从标准输入（stdin）传递数据**（适用于结构化数据或其他命令的输出）：

```bash
echo '{"task":"analyze","target":"file.rs"}' | am send --to npub1abc...
some-command | am send --to npub1abc...
```

**使用指定的代理身份发送消息：**

```bash
am send --identity research --to npub1abc... "message from research identity"
```

**成功发送消息后的输出：**

```json
{"to":"npub1abc...","event_id":"<hex>"}
```

## 接收消息

**实时接收消息**：当消息到达时，系统会以 NDJSON 格式输出：

```bash
am listen
```

**批量获取消息并退出程序：**

```bash
am listen --once
```

**根据 Unix 时间戳获取消息：**

```bash
am listen --once --since 1700000000
```

**限制返回的消息数量：**

```bash
am listen --once --limit 10
```

每条接收到的消息会以 JSON 对象的形式显示在控制台：

```json
{"from":"npub1xyz...","content":"hello","created_at":1700000000,"event_id":"<hex>"}
```

## JSON 输出与解析

所有命令的默认输出格式为 JSON。若需要以人类可读的格式查看输出，可以使用 `--format text` 选项：

```bash
# Get own npub
NPUB=$(am identity show | jq -r '.npub')

# Get content of latest message
am listen --once --limit 1 | jq -r '.content'

# Send result of a command
some-command | am send --to npub1abc...

# Collect batch messages into an array
messages=$(am listen --once | jq -s '.')
```

## 错误代码

| 代码 | 含义 |
|------|---------|
| 0 | 操作成功 |
| 1 | 一般错误 / 输入/输出错误 |
| 2 | 参数无效 |
| 3 | 网络/中继错误 |
| 4 | 加密/密钥错误 |
| 5 | 配置/TOML 文件错误 |

在自动化工作流程中，请务必检查程序的退出代码以判断操作是否成功：

```bash
am send --to npub1abc... "ping" || echo "Send failed with exit $?"
```

## 多个代理身份

您可以创建多个代理身份，以实现数据隔离（例如区分公开通信和内部协调）：

```bash
am identity generate --name public
am identity generate --name private
am identity list

am send --identity private --to npub1abc... "sensitive coordination"
```

## 配置管理

配置文件位于 `$XDG_CONFIG_HOME/am/config.toml`，代理身份信息存储在 `$XDG_DATA_HOME/am/identities/<name>.nsec` 文件中（文件权限设置为 0600）。

## 隐私保障

- **加密协议**：采用 NIP-17 加密标准，并结合 NIP-59 加密技术进行数据封装。
- **中继节点能看到的信息**：仅包括消息的传输类型（Kind:1059）以及发送者使用的临时密钥信息；发送者身份对中继节点是不可见的。
- **中继节点无法获取的信息**：发送者的 `npub` 公钥地址、消息内容以及发送者与接收者之间的关联信息。
- **密钥存储方式**：`nsec` 文件以明文形式存储，权限设置为 0600，确保文件安全；支持密码保护功能（版本 0.2）。

**注意：** 在版本 0.1 中不支持群组消息发送功能。版本 0.2 将支持多接收者加密消息的发送，格式为 `am send --to npub1 --to npub2 ...`。

## 额外资源

### 参考文档

- **`${CLAUDE_PLUGIN_ROOT}/skills/am/references/output-schemas.md`**：包含所有命令及其输出格式的 JSON 规范，包括 NDJSON 流式传输格式和错误信息。
- ** `${CLAUDE_PLUGIN_ROOT}/skills/am/references/workflows.md`**：提供了七种常见的代理工作流程示例，包括首次设置、代理间密钥交换、持续监听、结构化数据传输、请求/响应处理以及多代理身份管理。

### 示例脚本

- ** `${CLAUDE_PLUGIN_ROOT}/skills/am/examples/setup.sh`**：用于代理初始化的幂等性设置脚本。
- ** `${CLAUDE_PLUGIN_ROOT}/skills/am/examples/messaging.sh`**：包含发送和接收消息的示例代码，包括结构化 JSON 数据的处理方式。