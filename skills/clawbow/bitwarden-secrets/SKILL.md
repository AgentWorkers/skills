---
name: bitwarden-secrets
description: 通过 `bw CLI` 安全地访问 Bitwarden 或 Vaultwarden 中的加密信息；默认情况下，输出内容会被屏蔽（即不显示具体的加密数据）。该工具可用于同步加密存储库、搜索存储项、检索元数据，以及在用户明确确认的情况下显示单个加密字段的内容。
---
# Bitwarden Secrets（默认设置为安全模式）

使用此技能通过 `bw` 命令与 Bitwarden/Vaultwarden 进行交互，以最大限度地减少秘密信息的意外泄露。

## 先决条件
- 已安装 `bw` 命令行工具（CLI）。
- 服务器已配置（使用 `bw config server <url>`）。
- 用户已登录（使用 `bw login --apikey`）并解锁（使用 `bw unlock`），以确保 `BW_SESSION` 可用。

## 命令
```bash
cd skills/bitwarden-secrets
python3 scripts/vw_cli.py status
python3 scripts/vw_cli.py sync
python3 scripts/vw_cli.py search --query google
python3 scripts/vw_cli.py get --id <item_id>
```

### 启动辅助工具（可选）
一步完成运行时变量加载、会话刷新和数据同步：
```bash
source scripts/vw_bootstrap.sh
# or after shell reload:
vw-openclaw-ready
```

### 显示秘密信息（仅限明确请求时）
默认情况下，聊天中不会显示秘密值。
只有在用户明确同意并临时修改安全策略的情况下，才能显示秘密信息：
```bash
export VW_REVEAL_ALLOW=1
python3 scripts/vw_cli.py reveal --id <item_id> --field password --confirm YES_REVEAL
unset VW_REVEAL_ALLOW
```

## 安全策略
- 默认输出结果会被屏蔽或仅显示元数据。
- 禁止批量导出秘密信息。
- 建议使用 ID 和标签来标识秘密，并仅获取所需的最少字段信息。
- 显示秘密信息需要同时满足以下两个条件：`VW_REVEAL_ALLOW=1` 以及 `--confirm YES_REVEAL`。