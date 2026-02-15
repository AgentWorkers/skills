---
name: xmtp-cli-send
description: 通过 XMTP CLI 向某个地址或群组发送消息。适用于发送消息或等待回复的场景。
license: MIT
metadata:
  author: xmtp
  version: "1.0.0"
---

# CLI send

通过命令行向钱包地址或群组发送消息。

## 使用场景

- 向某个地址或群组发送消息
- 发送消息并等待回复（交互式操作或脚本执行）

## 使用规则

- `send-messages`：`send` 命令后需要指定目标地址/群组ID、消息内容、是否等待回复以及超时时间

## 快速入门

```bash
# Send to address
xmtp send --target 0x1234... --message "Hello!"

# Send to group
xmtp send --group-id <group-id> --message "Welcome!"

# Send and wait for response
xmtp send --target 0x1234... --wait --timeout 60000
```

详情请参阅 `rules/send-messages.md` 文件。