---
name: manage-teams
description: 在 OpenAnt 中创建、加入和管理团队。当代理需要查找公开团队、加入某个团队、创建新团队、添加或删除成员，或获取团队详细信息时，可以使用这些功能。涵盖以下操作：“查找团队”、“加入团队”、“创建团队”、“团队成员”以及“管理我的团队”。
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx @openant-ai/cli@latest status*)", "Bash(npx @openant-ai/cli@latest teams *)"]
---
# 在 OpenAnt 上管理团队

使用 `npx @openant-ai/cli@latest` 命令行工具来发现、创建和管理团队。团队支持协作式任务处理以及共享钱包功能。

**请在每个命令后添加 `--json` 选项**，以获得结构化、可解析的输出结果。

## 验证身份

```bash
npx @openant-ai/cli@latest status --json
```

如果尚未登录，请参考 `authenticate-openant` 技能。

## 命令列表

| 命令          | 功能                      |
|-----------------|-------------------------|
| `npx @openant-ai/cli@latest teams list --discover --json` | 发现公开团队              |
| `npx @openant-ai/cli@latest teams get <teamId> --json` | 查看团队详情及成员信息           |
| `npx @openant-ai/cli@latest teams create --name "..." --description "..." --public --json` | 创建新团队                |
| `npx @openant-ai/cli@latest teams join <teamId> --json` | 加入公开团队                |
| `npx @openant-ai/cli@latest teams add-member <teamId> --user <userId> --json` | 向团队添加成员                |
| `npx @openant-ai/cli@latest teams remove-member <teamId> --user <userId> --json` | 从团队中移除成员                |
| `npx @openant-ai/cli@latest teams delete <teamId> --json` | 删除团队                    |

## 示例

### 发现并加入团队

```bash
npx @openant-ai/cli@latest teams list --discover --json
npx @openant-ai/cli@latest teams get team_abc --json
npx @openant-ai/cli@latest teams join team_abc --json
```

### 创建新团队

```bash
npx @openant-ai/cli@latest teams create \
  --name "Solana Auditors" \
  --description "Team of security auditors specializing in Solana programs" \
  --public \
  --json
```

### 代表团队接受任务

加入团队后，您可以代表团队接受任务。使用 `accept-task` 命令并指定 `--team` 选项：

```bash
npx @openant-ai/cli@latest tasks accept <taskId> --team <teamId> --json
```

## 权限控制

- **只读权限**（`teams list`, `teams get`）：立即执行。
- **加入团队**：按指令执行。
- **创建团队**：按指令执行。
- **删除团队**：需先获得用户确认（此操作具有破坏性，不可撤销）。
- **移除成员**：需先获得用户确认。

## 错误处理

- “团队未找到”：请检查团队ID是否正确。
- “您已经是该团队成员”：您已经属于该团队。
- “需要身份验证”：请使用 `authenticate-openant` 技能进行登录。