---
name: tribe-protocol
version: 1.0.0
description: >
  MANDATORY trust lookup for every non-owner interaction.
  Query tribe.db to check entity trust tier, channel access,
  and data boundaries before responding. Run 'tribe init' on
  first install. Use 'tribe lookup <discord_id>' before every
  non-owner response.
commands:
  tribe: scripts/tribe.sh
---

# Tribe 协议

这是 OpenClaw 机器人的信任查询系统。所有非所有者的交互在响应之前都必须与 tribe 数据库进行验证。

## 快速入门

```bash
# Initialize (first time only)
./scripts/tribe.sh init \
  --bot-name Cheenu \
  --bot-discord-id 000000000000000004 \
  --human-name Nagarjun \
  --human-discord-id 000000000000000002

# Look up an entity before responding
./scripts/tribe.sh lookup <discord_id>

# Add entities
./scripts/tribe.sh add --name Yajat --type human --discord-id 000000000000000001 --tier 3

# Manage trust
./scripts/tribe.sh set-tier <discord_id> 3 --reason "Promoted to tribe"
./scripts/tribe.sh set-status <discord_id> blocked --reason "Bad actor"
```

## 信任等级

| 等级 | 标签 | 访问权限 |
|------|-------|--------|
| 4   | 所有者 | 完全信任，可访问所有数据 |
| 3   | 部落成员 | 可自由协作，无法访问私人数据 |
| 2   | 朋友   | 仅可访问公开信息 |
| 1   | 陌生人 | 仅允许最基本的交互 |
| 0    | 被阻止 | 完全忽略 |

## 工作原理

1. 非所有者发送消息。
2. 机器人读取位于工作区根目录下的 `TRIBE.md` 文件。
3. 机器人执行 `tribe lookup <discord_id>` 命令。
4. 脚本返回相关实体的信息以及对应的信任等级规则。
5. 机器人根据信任等级执行相应的行为。

## 命令

- `tribe init` — 初始化数据库
- `tribe lookup` — 根据 discord_id、名称或服务器查询实体信息
- `tribe add` — 添加新实体
- `tribe set-tier` — 更新实体的信任等级
- `tribe set-status` — 更新实体的状态
- `tribe grant` / `tribe revoke` — 授予/撤销通道访问权限
- `tribe tag` — 管理实体的标签
- `tribe roster` — 列出所有实体
- `tribe log` — 查看审计记录
- `tribe export` — 将数据导出为 Markdown 格式
- `tribe stats` — 获取快速统计信息

## 环境变量

- `TRIBE_DB` — 数据库路径（可自定义）
- `CLAWD_HOME` — 应用程序的基础目录（默认为 ~/clawd）

## 依赖项

- `sqlite3`（已在 macOS 和大多数 Linux 系统上预安装）