---
name: cancel-task
description: 在 OpenAnt 中取消任务并收回托管的资金。只有任务创建者才能执行此操作。当用户希望终止任务、撤销悬赏、停止接收申请、关闭自己创建的任务或取回托管的代币时，可以使用此功能。此外，当用户表示“我改变主意了”、“关闭这个任务”或“算了”等意思时，也需要使用此技能。请务必在用户想要撤销或取消自己创建的任务时使用此功能，即使他们没有明确使用“取消”这个词。
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx @openant-ai/cli@latest status*)", "Bash(npx @openant-ai/cli@latest tasks cancel *)", "Bash(npx @openant-ai/cli@latest tasks get *)", "Bash(npx @openant-ai/cli@latest tasks settlement *)"]
---
# 在 OpenAnt 上取消任务

使用 `npx @openant-ai/cli@latest` 命令行工具来取消您创建的任务。取消操作会将任务从市场中移除，如果该任务已获得资助，系统会自动将托管的代币退还到您的钱包中。

**请在每个命令后添加 `--json` 选项**，以获得结构化、可解析的输出结果。

## 谁可以取消任务？

只有**任务创建者**才能取消任务。被分配任务的人无法取消任务——请使用 `leave-task` 命令来退出被分配的任务。

## 可取消的任务状态

| 状态 | 是否可以取消？ | 备注 |
|--------|-------------|-------|
| `DRAFT` | 可以 | 无需进行链上退款 |
| `OPEN` | 可以 | 托管的资金将会被退还 |
| `ASSIGNED` | 可以 | 被分配者将失去该任务；请先通知他们 |
| `SUBMITTED` | 不可以 | 任务正在等待您的审核——请先验证或拒绝它 |
| `COMPLETED` | 不可以 | 任务已经完成；资金已经释放 |
| `CANCELLED` | 不可以 | 任务已被取消 |

## 第一步：确认身份

```bash
npx @openant-ai/cli@latest status --json
```

如果您尚未登录，请参考 `authenticate-openant` 命令进行身份验证。

## 第二步：检查任务状态

在取消任务之前，请先核实任务当前的状态以及是否已经获得资助：

```bash
npx @openant-ai/cli@latest tasks get <taskId> --json
# Check: status, rewardAmount, rewardToken, assigneeId
```

如果任务处于 `ASSIGNED` 状态，请确认被分配者是否已经完成了实质性工作。在没有事先沟通的情况下中途取消任务可能不公平。

## 第三步：取消任务

```bash
npx @openant-ai/cli@latest tasks cancel <taskId> --json
# -> { "success": true, "data": { "id": "task_abc", "status": "CANCELLED" } }
```

## 第四步：验证链上退款（仅适用于已获得资助的任务）

对于已进行托管的资金，退款会自动完成。您可以通过以下命令来验证退款状态：

```bash
npx @openant-ai/cli@latest tasks settlement <taskId> --json
# -> { "data": { "status": "Refunded", "onChain": true } }
```

退款可能需要几秒钟才能在链上得到确认。

## 示例

### 取消一个开放性的悬赏任务

```bash
# Check the task first
npx @openant-ai/cli@latest tasks get task_abc123 --json

# Cancel it
npx @openant-ai/cli@latest tasks cancel task_abc123 --json
# -> { "success": true, "data": { "id": "task_abc123", "status": "CANCELLED" } }
```

### 验证退款是否已到账

```bash
npx @openant-ai/cli@latest tasks settlement task_abc123 --json
# -> { "data": { "status": "Refunded", "rewardAmount": 500, "mint": "EPjFW..." } }
```

## 注意事项

取消操作是**不可逆的**——在运行 `tasks cancel` 命令之前，请务必先与用户确认：

1. 显示任务标题、状态和奖励金额。
2. 如果任务已分配给他人，请说明当前有工作人员正在处理。
3. 明确征求用户的确认：“您确定要取消这个任务吗？托管的资金将会退还到您的钱包。”
4. 只有在用户确认后，才能执行取消操作。

## 绝对禁止的行为：

- **绝对不要在未审核提交结果的情况下取消已提交的任务**——工作人员已经完成了工作并正在等待付款。至少请先通过评论拒绝提交结果，然后再取消任务。
- **绝对不要代表被分配者取消任务**——被分配者应该使用 `tasks unassign` 命令，而不是 `tasks cancel`。此命令仅限任务创建者使用。
- **不要认为链上退款是立即完成的**——Solana 索引器需要时间来处理退款请求。请等待几秒钟后再查看退款状态。
- **绝对不要在未通知被分配者的情况下取消已分配的任务**——他们可能已经开始工作了。请先使用 `comment-on-task` 命令通知他们。
- **绝对不要为了避免支付合法完成的工作而取消任务**——如果工作已经完成且质量合格，请先进行验证。

## 后续操作：

- 要在取消任务前通知被分配者，请使用 `comment-on-task` 命令。
- 要查看退款后的钱包余额，请使用 `check-wallet` 命令。

## 错误处理：

- “需要身份验证” —— 请使用 `authenticate-openant` 命令进行身份验证。
- “任务未找到” —— 任务 ID 无效；请使用 `tasks get` 命令确认任务是否存在。
- “只有任务创建者才能取消任务” —— 您不是该任务的创建者。
- “任务当前状态不允许取消” —— 任务处于 `SUBMITTED`、`COMPLETED` 或 `CANCELLED` 状态；请使用 `tasks get` 命令核实任务状态。