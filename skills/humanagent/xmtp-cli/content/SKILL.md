---
name: xmtp-cli-content
description: 通过命令行界面（CLI）演示 XMTP 的内容类型。这些内容类型可用于发送文本、Markdown 格式的文本、附件、交易数据、深度链接（deeplink），或迷你应用程序（miniapp）相关的数据。
license: MIT
metadata:
  author: xmtp
  version: "1.0.0"
---

# CLI（命令行界面）功能

演示多种XMTP内容类型：文本（支持回复/互动）、Markdown格式、附件、交易数据、深度链接（deeplink）以及迷你应用程序（miniapp）。

## 适用场景

- 发送或测试文本、Markdown格式的内容或附件
- 发送或测试交易数据、深度链接或迷你应用程序的内容

## 规则

- `content-types`：`content-text` / `markdown` / `attachment` / `transaction` / `deeplink` / `miniapp` 及其相关选项

## 快速入门

```bash
xmtp content text --target 0x1234...
xmtp content markdown --target 0x1234...
xmtp content attachment --target 0x1234...
xmtp content transaction --target 0x1234... --amount 0.1
```

详情请参阅 `rules/content-types.md` 文件。