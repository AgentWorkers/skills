---
name: dagny-nostr-nak
description: 通过 nak CLI 管理 Nostr 的帖子和互动行为。该工具可用于创建笔记、在帖子讨论中回复、标记相关内容、查看回复/提及信息、监控中继服务器（默认为 wss://relay.primal.net），以及发布带有正确根标签/回复标签的事件。使用该工具需要具备 NOSTR_SECRET_KEY（nsec）的访问权限，以便进行签名和发布操作。
---
# Nostr (nak)

## 概述
使用 `nak` 来执行所有与 Nostr 相关的操作：发布笔记、在帖子中回复以及查询其他用户的回复/提及。默认中继地址为 `wss://relay.primal.net`，除非用户指定了其他地址。

## 安装 / 更新 nak
- **仓库**：https://github.com/fiatjaf/nak
- **安装**（脚本）：`curl -sSL https://raw.githubusercontent.com/fiatjaf/nak/master/install.sh | sh`
- **更新**：重新运行上述安装脚本（会安装最新版本）
- **提示**：如果需要了解脚本的具体功能，请在运行前先仔细阅读脚本内容。

## 注册（生成密钥）
- **生成新密钥**：`nak key generate`（会输出 nsec 和 npub）
- **保存密钥**：将 `NOSTR_SECRET_KEY` 保存在 shell 配置文件或具有受限权限的本地 `.env` 文件中。
  - 例如：`export NOSTR_SECRET_KEY="nsec1..."`
  - 可选：如果将密钥保存在本地文件中，可以使用 `chmod 600 .env` 来设置文件权限。
  - 建议使用环境变量 `NOSTR_SECRET_KEY`，而不是在命令中直接传递 `-sec` 参数。

## 快速入门（常见操作）
- **发布笔记**：`nak event -k 1 --sec $NOSTR_SECRET_KEY -c "..." <relay>`
- **回复笔记**：需要使用 `root` 和 `reply` 标签（详见下文）
- **查看回复**：`nak req -k 1 -e <event_id> -l <N> <relay>`
- **查看提及**：`nak req -k 1 -p <your_pubkey_hex> -l <N> <relay>`

## 工作流程：发布与回复

### 1) 创建新笔记
- 编写内容。
- 发布笔记：
  ```bash
  nak event -k 1 --sec $NOSTR_SECRET_KEY -c "<content>" wss://relay.primal.net
  ```

### 2) 回复其他用户的回复（确保回复正确关联到原始帖子）
回复时必须同时使用 `root` 和 `reply` 标签，以便客户端能够正确显示回复内容：
- `root`：原始笔记的 ID
- `reply`：你要回复的具体笔记的 ID

可以使用以下格式：
- `-t e="<id>;<relay>;root"`
- 或者
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

### 3) 查看对某篇笔记的回复
```bash
nak req -k 1 -e <root_id> -l 20 wss://relay.primal.net
```

### 4) 查看对你的公钥的提及
```bash
nak req -k 1 -p <your_pubkey_hex> -l 20 wss://relay.primal.net
```

## 常见约定
- 默认中继地址：`wss://relay.primal.net`
- 建议使用环境变量 `NOSTR_SECRET_KEY`，而不是在命令中直接传递 `-sec` 参数。
- 标记用户时，需要使用 `-p <npub/hex>`。
- 对于需要展示给用户的链接，可以使用 `nak encode nevent ...` 进行编码，格式为 `https://primal.net/e/<nevent>`。

## 参考资料
- 使用 `nak event --help` 和 `nak req --help` 查看各命令的详细参数和用法。