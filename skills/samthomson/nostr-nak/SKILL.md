---
name: nostr-nak
description: 这是一个通用技能，用于使用支持PTY协议的Nostr Army Knife (nak) CLI工具。
---
# nostr-nak

这是一个用于使用 Nostr Army Knife (nak) CLI 工具的通用脚本。

## 重要技术说明（PTY 要求）
由于标准输出（stdout）的缓冲机制，`nak` 在非交互式环境中可能会卡住（无法正常运行）。**务必** 将 `nak` 命令封装在 `script` 脚本中，以强制使用伪 TTY（伪终端）环境：
```
script -q -c "nak req ..." /dev/null | cat
```

## 中继逻辑
如果未指定中继地址，系统会使用默认的中继地址：
- `wss://relay.damus.io`
- `wss://relay.primal.net`
- `wss://relay.nostr.band`

如果用户指定了中继地址，则会使用用户指定的地址。

## 身份验证处理
- **查询信息**：使用 `npub...` 或带有 `-a` 标志的十六进制公钥。
- **发布信息**：使用 `nsec...` 或带有 `--sec` 标志的十六进制私钥。

## 使用示例
获取最近 5 条笔记：
```
script -q -c "nak req -k 1 -a <npub> <relays> -l 5" /dev/null | cat
```