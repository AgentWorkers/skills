---
name: nak
description: Nostr Army Knife (nak) CLI：使用此工具可以与Nostr网络进行交互、发布事件、查询中继节点、管理密钥，并执行高级Nostr操作，如NIP-46签名、NIP-60钱包管理以及Blossom文件上传等。
compatibility: Requires `nak` CLI (v0.15.3+ recommended).
---
# `nak` – Nostr 军用刀（Nostr Army Knife）

`nak` 是一个功能强大的命令行工具（CLI），用于与 Nostr 协议进行交互。它支持事件创建、签名、发布、查询、密钥管理等多种操作。

## 使用方法

### 1. 事件处理 (`nak event`)

生成、签名并发布事件。

```bash
# Publish a simple text note (Kind 1) to specific relays
nak event -c "Hello Nostr" wss://relay.damus.io wss://nos.lol

# Publish using a specific secret key (hex or nsec)
nak event -c "Authenticated message" --sec <nsec/hex> wss://relay.damus.io

# Reply to an event (Kind 1)
nak event -c "I agree!" -e <event_id> --sec <nsec/hex> wss://relay.damus.io

# Create a profile metadata event (Kind 0)
echo '{"name":"bob","about":"builder"}' | nak event -k 0 --sec <nsec/hex> wss://relay.damus.io

# Generate an event JSON without publishing (dry run)
nak event -c "Just checking" -k 1 --sec <nsec/hex>
```

### 2. 事件查询 (`nak req`)

订阅事件并过滤结果。

```bash
# Listen for all Kind 1 notes on a relay
nak req -k 1 wss://relay.damus.io

# Listen for a specific author
nak req -a <pubkey_hex> wss://relay.damus.io

# Listen for replies to a specific event (E-tag)
nak req -e <event_id> wss://relay.damus.io

# Fetch with a limit
nak req -k 1 --limit 10 wss://relay.damus.io

# Output is stream of ["EVENT", ...] JSON arrays.
# Pipe to jq for readability:
nak req -k 1 wss://relay.damus.io | jq
```

### 3. 事件获取 (`nak fetch`)

根据参考编号（NIP-19/NIP-05）获取特定事件。

```bash
# Fetch an event by nevent
nak fetch nevent1...

# Fetch a profile
nak fetch npub1...

# Fetch from specific relays
nak fetch npub1... --relay wss://relay.nostr.band
```

### 4. 密钥管理 (`nak key`, `nak encode`, `nak decode`)

用于管理密钥及 NIP-19 实体。

```bash
# Generate a new keypair
nak key generate

# Convert nsec to hex (or vice versa - automated detection)
nak decode nsec1...

# Encode a hex pubkey to npub
nak encode npub <hex_pubkey>

# Encode an event ID to nevent with relay hints
nak encode nevent <event_id> --relay wss://relay.damus.io
```

### 5. 加密/解密 (`nak encode`, `nak decode`)

实现消息的加密和解密功能。

```bash
# Encrypt a message for a recipient
nak encrypt --sec <sender_nsec> --target <recipient_pubkey> "Secret message"

# Decrypt a message
nak decrypt --sec <recipient_nsec> --source <sender_pubkey> <base64_ciphertext>
```

### 6. 现金钱包管理 (`nak wallet`)

用于管理由 Nostr 中继支持的 Cashu 钱包。

```bash
# Show balance (reloads from relays)
nak wallet --sec <nsec>

# Pay a Lightning invoice
nak wallet pay --sec <nsec> lnbc1...
```

### 7. Blossom 文件存储

用于与 Blossom 媒体服务器进行交互。

```bash
# Upload a file
nak blossom upload --server https://cdn.example.com --sec <nsec> ./image.png
```

## Agentic/MCP 模式

`nak` 提供了 `mcp` 命令，可用于启动 Model Context Protocol 服务器。
```bash
nak mcp
```
如果您希望将 `nak` 直接作为 MCP 工具使用，这个功能非常有用；但通常情况下，您会通过 `exec` 命令直接调用 `nak` 的各个 CLI 功能。

## 使用技巧

*   **管道传输（Piping）：** `nak` 支持管道传输（piping）功能。您可以将 JSON 数据通过管道传递给 `nak event` 命令进行签名，或将 `nak req` 的输出结果传递给其他工具。
*   **环境变量：**
    *   `NOSTR_SECRET_KEY`：设置此环境变量可避免每次使用时都手动输入 `--sec` 参数。