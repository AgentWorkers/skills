---
name: xmtp-cli-debug
description: 从 XMTP CLI 获取调试和诊断信息。适用于解决地址问题、检查收件箱内容或获取一般信息时使用。
license: MIT
metadata:
  author: xmtp
  version: "1.0.0"
---

# CLI调试

获取调试和诊断信息：包括一般信息、将地址解析为收件箱ID、检查地址或收件箱内容。

## 使用场景

- 获取CLI/客户端的一般信息
- 将以太坊地址解析为收件箱ID
- 检查地址或收件箱的详细信息
- 验证安装情况或密钥包的状态

## 使用规则

- 命令格式：`info-resolve-address-inbox`，后跟参数 `debug info`、`address`、`inbox`、`resolve`、`installations` 或 `key-package` 及相关选项

## 快速入门

```bash
xmtp debug info
xmtp debug resolve --address 0x1234...
xmtp debug address --address 0x1234...
xmtp debug inbox --inbox-id abc...
```

详情请参阅 `rules/info-resolve-address-inbox.md` 文件。