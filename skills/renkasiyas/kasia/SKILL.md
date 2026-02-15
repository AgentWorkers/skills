---
name: kasia
description: 在 Kaspa 区块链上，使用 Kasia 协议发送和接收加密的消息。适用于以下场景：用户需要向他人发送消息、查看 Kasia 对话记录、阅读加密消息、通过消息进行支付，或管理 Kasia 交易（即“handshakes”）。此功能需要配置好 `kasia-mcp` 和 `kaspa-mcp` 服务器（这些服务器通常通过 `mcporter` 进行管理）。
---

# Kasia — 在Kaspa区块链上进行加密通信

通过Kasia协议在Kaspa区块链上发送和接收加密消息。该工具使用`mcporter`来调用`kasia-mcp`系列工具。

## 前提条件

- 已安装`mcporter`（通过`npm install -g mcporter`安装）。
- `kasia-mcp`已构建并配置在`config/mcporter.json`文件中。
- `kaspa-mcp`已配置（使用相同的钱包）——用于广播交易。
- 在`mcporter`配置中设置了钱包的助记词或私钥。

运行`scripts/setup.sh`以自动完成配置：
```bash
scripts/setup.sh /path/to/kasia-mcp --mnemonic "your twelve word phrase" --network mainnet
```

验证：`mcporter list kasia`（应显示8个可用的工具）

## 工具

在 workspace目录中，通过`mcporter call kasia.<tool>`来调用相应的工具。

### 读取操作（无需进行交易）

| 工具 | 功能 | 示例 |
|------|---------|---------|
| `kasia_get_conversations` | 列出所有对话及其状态 | `mcporter call kasia.kasia_get_conversations` |
| `kasia_get_requests` | 查看待处理的握手请求 | `mcporter call kasia.kasia_get_requests` |
| `kasia_get_messages` | 读取解密后的消息 | `mcporter call kasia.kasia_get_messages address="kaspa:q..."` |
| `kasia_read_self_stash` | 读取加密的私人数据 | `mcporter call kasia.kasia_read_self_stash scope="notes"` |

### 写入操作（分为两步：生成数据包 → 广播）

写入操作会生成数据包及相应的广播指令。需要使用`kaspa.send_kaspa`来完成广播：
```bash
# Step 1: Generate payload
mcporter call kasia.kasia_send_handshake address="kaspa:q..."
# Returns: { action, to, amount, payload, instructions }

# Step 2: Broadcast (use the returned values)
mcporter call 'kaspa.send_kaspa(to: "kaspa:q...", amount: "0.2", payload: "<hex>")'
```

| 工具 | 功能 |
|------|---------|
| `kasia_send_handshake` | 启动与他人的对话 |
| `kasia_accept_handshake` | 接受来自他人的握手请求 |
| `kasia_send_message` | 在活跃的对话中发送加密消息 |
| `kasia_write_self_stash` | 将加密的私人数据存储到链上 |

## 对话流程

1. **查看请求**：使用`kasia_get_requests`查看待处理的握手请求。
2. **开始或接受对话**：使用`kasia_send_handshake`或`kasia_accept_handshake`，然后通过`kaspa.send_kaspa`进行广播。
3. **聊天**：使用`kasia_send_message`发送消息，并通过`kasia_get_messages`接收回复。
4. **支付**：直接使用`kaspa.send_kaspa`进行支付（无需专门的Kasia工具）。

## 对话状态

- `pending_outgoing`：您发送了握手请求，正在等待对方接受。
- `pending_incoming`：有人向您发送了握手请求，您需要接受。
- `active`：双方已完成握手，可以互相发送消息。

## 背景轮询

为了实现实时消息传递，可以设置一个后台轮询程序：

1. 创建一个轮询脚本，每隔N秒调用一次`kasia_get_messages`。
2. 记录已处理的交易ID以避免重复接收相同消息。
3. 将新消息写入文件（例如`memory/kasia-new-messages.jsonl`）。
4. 使用cron作业或心跳检测机制将新消息发送给用户。

有关完整的协议规范和索引器API详情，请参阅`references/protocol.md`。

## 重要注意事项

- **仅限主网使用**：`kasia-mcp`仅支持主网环境（测试网不支持加密通信）。
- **写入操作分为两步**：写入工具生成数据包，必须通过`kaspa.send_kaspa`进行广播。
- **使用相同的钱包**：`kasia-mcp`和`kaspa-mcp`必须使用相同的助记词或私钥。
- **费用**：每条消息都视为一次交易，最低费用约为0.2 KAS。