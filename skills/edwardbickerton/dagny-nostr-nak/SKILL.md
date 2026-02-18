---
name: dagny-nostr-nak
description: 通过 `nak CLI` 管理 Nostr 的发布内容及用户互动。该工具可用于创建笔记、在帖子中回复、标记相关内容（npubs）、查看回复/提及信息、监控中继服务器（默认为 `wss://relay.primal.net`），以及以正确的根标签/回复标签发布事件。
---
# Nostr (nak)

## 概述
使用 `nak` 执行所有与 Nostr 相关的操作：发布笔记、在帖子中回复以及查询其他用户的回复/提及。默认中继地址为 `wss://relay.primal.net`，除非用户指定了其他地址。

## 安装 / 更新 nak
- **仓库**: https://github.com/fiatjaf/nak
- **安装**（脚本）：`curl -sSL https://raw.githubusercontent.com/fiatjaf/nak/master/install.sh | sh`
- **更新**：重新运行上述安装脚本（将安装最新版本）。

## 入门（密钥）
- **生成新密钥**：`nak key generate`（会输出 nsec 和 npub）
- **保存密钥**：将 `NOSTR_SECRET_KEY` 设置在 shell 配置文件或本地的 `.env` 文件中。
  - 例如：`export NOSTR_SECRET_KEY="nsec1..."`
  - 建议使用环境变量 `NOSTR_SECRET_KEY`，而不是在命令中直接指定 `--sec`。

## 快速入门（常见操作）
- **发布笔记**：`nak event -k 1 --sec $NOSTR_SECRET_KEY -c "..." <relay>`
- **回复笔记**：需要包含 `root` 和 `reply` 标签（详见下文）
- **查看回复**：`nak req -k 1 -e <event_id> -l <N> <relay>`
- **查看提及**：`nak req -k 1 -p <your_pubkey_hex> -l <N> <relay>`

## 工作流程：发布与回复

### 1) 创建新笔记
- 编写内容。
- 发布：
  ```bash
  nak event -k 1 --sec $NOSTR_SECRET_KEY -c "<content>" wss://relay.primal.net
  ```

### 2) 回复其他用户的回复（确保回复正确关联到原帖）
始终需要包含 `root` 和 `reply` 标签，以便客户端能够正确显示回复内容：
- `root`：原始笔记的 ID
- `reply`：你正在回复的具体笔记的 ID

使用以下格式添加标签：
- `-t e="<id>;<relay>;root"`
- `-t e="<id>;<relay>;reply"`

示例：
```bash
nak event -k 1 --sec $NOSTR_SECRET_KEY \
  -t e="<root_id>;wss://relay.primal.net;root" \
  -t e="<reply_id>;wss://relay.primal.net;reply" \
  -p <other_pubkey_hex> \
  -c "<reply content>" \
  wss://relay.primal.net
```

### 3) 查看某篇笔记的回复
```bash
nak req -k 1 -e <root_id> -l 20 wss://relay.primal.net
```

### 4) 查看对你的公钥的提及
```bash
nak req -k 1 -p <your_pubkey_hex> -l 20 wss://relay.primal.net
```

## 常用约定
- 默认中继地址：`wss://relay.primal.net`
- 建议使用环境变量 `NOSTR_SECRET_KEY`，而不是在命令中直接指定 `--sec`。
- 标记用户时，需要使用 `-p <npub/hex>`。
- 对于面向人类的链接，使用 `nak encode nevent ...` 进行编码，并格式化为 `https://primal.net/e/<nevent>`。

## 参考资料
- 使用 `nak event --help` 和 `nak req --help` 查看各参数的详细信息。