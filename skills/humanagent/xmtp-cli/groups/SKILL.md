---
name: xmtp-cli-groups
description: 通过命令行界面（CLI）创建和管理 XMTP 组以及发送私信（DMs）。适用于创建私信或组，或更新组元数据时使用。
license: MIT
metadata:
  author: xmtp
  version: "1.0.0"
---

# CLI 组管理

使用 XMTP CLI 创建私信（DM）和组，并更新组的元数据。

## 使用场景

- 创建带有目标收件人的私信
- 创建包含成员地址或收件箱 ID 的组
- 更新组名称或图片 URL

## 规则

- `create-dm-group` – 用于创建私信或组（区分私信和组，支持指定成员地址或成员收件箱 ID）
- `metadata` – 用于更新组的元数据（包括组 ID、名称和图片 URL）

## 快速入门

```bash
# Create DM
xmtp groups create --target 0x123...

# Create group
xmtp groups create --type group --name "Team" --member-addresses "0x123...,0x456..."
```

详情请参阅 `rules/create-dm-group.md` 和 `rules/metadata.md` 文件。