---
name: scheduler
description: "安排任务和命令在特定时间运行。可以按照 Cron 表达式来执行 shell 命令、代理任务（agent tasks）、API 调用以及自动化操作。已在 Telegram 和 Discord 上进行过测试。"
tags: [cron, scheduler, automation, tasks, commands, telegram, discord]
metadata:
  openclaw:
    summary: "**Scheduler:** Run commands and tasks on a schedule — shell scripts, agent tasks, API calls, file ops. Natural language, native cron, zero dependencies."
    emoji: "calendar"
user-invocable: true
command-dispatch: prompt
---

# 调度器

使用自然语言按照预定时间表执行任务和命令。可以运行 shell 命令、代理任务、API 健康检查、文件操作以及自动化操作——无论是单次执行还是定期执行。

## 使用方法

```
/schedule run npm test in 5 minutes
/schedule git pull origin main tomorrow at 6am
/schedule generate weekly sales report every monday at 9am
/schedule check https://api.example.com/health every 30m
/schedule clean /tmp files every day at 3am silently
/schedule back up database every sunday at 2am
/schedule restart server in 10 minutes silently
/schedule list
/schedule cancel <jobId>
```

## 代理指令

当用户触发 `/schedule` 时，系统会判断用户的意图：

- **列出** → 调用 `cron.list` 显示当前已安排的任务。
- **取消/删除/移除 `<jobId>` → 使用该 `jobId` 调用 `cron.remove`。
- **其他所有操作** → 创建一个新的定时任务（具体步骤见下文）。

---

### 第一步：解析输入

从输入中提取四个关键信息：**要执行的任务（WHAT）**、**执行时间（WHEN）**、**是否重复执行（RECURRENCE）**、**结果展示方式（DELIVERY）**。

#### 确定任务类型（WHAT）

将用户的请求分类为不同的任务类型：

| 任务类型 | 触发词 | 代理操作 |
|---|---|---|
| Shell 命令 | `run`、`execute`、`do`、类似命令的语法（`npm`、`git`、`docker`、`curl`、`python`） | 使用 Bash 工具执行命令 |
| 代理任务 | `generate`、`summarize`、`analyze`、`write`、`create`、`compile`、`review` | 使用可用的代理工具执行任务 |
| API/健康检查 | `check`、`ping`、`hit`、`call`、URL 模式（`https://...`） | 获取 URL 并报告状态 |
| 文件操作 | `clean`、`back up`、`copy`、`move`、`archive`、`compress` | 使用可用工具执行文件操作 |
| 自定义提示 | 其他所有操作 | 作为自由形式的代理任务执行 |

**WHAT** 会成为 `payload.message`——这是代理执行任务的明确指令。

#### 确定执行时间（WHEN）

使用与 `remindme` 技能相同的时间解析规则：

**第一层：模式匹配**

扫描以下模式（首次匹配有效）：

**相对时间** — `in <数字> <单位>`：
| 模式 | 时间长度 |
|---|---|
| `in Ns`、`in N seconds` | N 秒 |
| `in Nm`、`in N min`、`in N minutes` | N 分钟 |
| `in Nh`、`in N hours` | N 小时 |
| `in Nd`、`in N days` | N * 24 小时 |
| `in Nw`、`in N weeks` | N * 7 天 |

**绝对时间** — `at <时间>`：
| 模式 | 含义 |
|---|---|
| `at HH:MM`、`at H:MMam/pm` | 今天该时间（如果过去则明天） |
| `at Ham/pm`、`at HH` | 今天这个小时 |

**指定日期**：
| 模式 | 含义 |
|---|---|
| `tomorrow` | 下一个工作日，默认为上午 9 点 |
| `tonight` | 今天晚上 8 点 |
| `next monday..sunday` | 下一次发生的时间，默认为上午 9 点 |

**重复执行** — `every <模式>`：
| 模式 | 时间安排 |
|---|---|
| `every Nm/Nh/Nd` | `kind: "every"`，`everyMs: N * 单位毫秒` |
| `every day at <时间>` | `kind: "cron"`，`expr: "M H * * *"` |
| `every <weekday> at <时间>` | `kind: "cron"`，`expr: "M H * * DOW"` |
| `every weekend at <时间>` | `kind: "cron"`，`expr: "M H * * 0,6"` |
| `every hour` | `kind: "every"`，`everyMs: 3600000` |

**单位转换表**：
| 单位 | 毫秒 |
|---|---|
| 1 秒 | 1000 |
| 1 分钟 | 60000 |
| 1 小时 | 3600000 |
| 1 天 | 86400000 |
| 1 周 | 604800000 |

**第二层：俚语和缩写**

| 表达方式 | 对应含义 |
|---|---|
| `in a bit`、`shortly` | 30 分钟 |
| `in a while` | 1 小时 |
| `later`、`later today` | 3 小时后 |
| `end of day`、`eod` | 今天下午 5 点 |
| `end of week`、`eow` | 星期五下午 5 点 |
| `morning` | 上午 9 点 |
| `afternoon` | 下午 2 点 |
| `evening` | 下午 6 点 |
| `midnight` | 第二天凌晨 12 点 |
| `noon` | 中午 12 点 |

**第三层：避免歧义——询问而非猜测**

如果无法确定执行时间，请询问用户。切勿自行选择默认时间。

#### 确定结果展示方式（DELIVERY）

| 用户输入 | 结果展示方式 |
|---|---|
| `silently`、`quietly`、`in background`、`no output` | `"none"` — 无声执行，不返回结果 |
| 未指定，或 `report`、`show results`、`announce` | `"announce"` — 将任务结果发送到指定频道 |

### 第二步：计算调度时间

**时区规则：** 始终使用用户的 **本地时区**（系统时区），切勿使用 UTC 作为默认值。

**单次执行** → 使用包含用户本地时区偏移量的 ISO 8601 时间戳。
- 如果计算出的时间在过去，推迟到下一个时间点执行。

**定期执行（cron）** → 使用用户 IANA 时区的 5 字段 cron 表达式。

**定期执行（间隔）** → `kind: "every"`，`everyMs` 以毫秒为单位。

### 第三步：安全检查

在安排任务之前，检查任务是否涉及破坏性操作：

**需要用户确认的破坏性操作**：
- 文件删除：`rm`、`del`、`remove`、`wipe`、`clean`（除非是清理临时文件/缓存）
- 数据库操作：`drop`、`truncate`、`delete from`、`destroy`
- Git 操作：`reset --hard`、`push --force`、`branch -D`
- 系统操作：`kill`、`shutdown`、`reboot`、`format`
- 网络操作：`iptables`、`firewall`、`ufw`

如果检测到破坏性操作：
1. 警告用户：“此任务包含破坏性操作（`<命令>`）。您确定要安排这个任务吗？”
2. 只有在用户明确确认后才能继续执行。
3. 在任务名称中添加 `[CONFIRMED DESTRUCTIVE]` 以记录审计轨迹。

**无需确认的安全操作**：
- 仅读操作：`ls`、`cat`、`git status`、`git log`、`curl GET`、`ping`
- 构建/测试：`npm test`、`npm build`、`make`、`cargo test`
- 报告生成：`generate`、`summarize`、`analyze`、`compile report`

### 第四步：确定结果展示渠道

结果展示的优先级与 `remindme` 技能相同：

1. **用户明确指定** — 用户指定“在 Telegram 上”/“在 Discord 上”等。
2. **当前使用的频道** — 如果任务来自外部频道，则发送到该频道。
3. **默认频道** — 参考 `MEMORY.md` 中的设置。
4. **最后一个使用的外部频道** — 使用 `channel: "last"`。
5. **未指定频道且结果展示方式为“none”** — 任务将无声执行。
6. **未指定频道且结果展示方式为“announce”** — 询问用户：“任务结果应发送到哪里？”

### 第五步：调用 `cron.add`

**单次执行任务：**

```json
{
  "name": "Task: <short description>",
  "schedule": {
    "kind": "at",
    "at": "<ISO 8601 timestamp>"
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "SCHEDULED TASK: <detailed task instruction>. Execute this task now and report the results."
  },
  "delivery": {
    "mode": "announce",
    "channel": "<detected channel>",
    "to": "<detected target>",
    "bestEffort": true
  },
  "deleteAfterRun": true
}
```

**定期执行任务（cron）：**

```json
{
  "name": "Recurring Task: <short description>",
  "schedule": {
    "kind": "cron",
    "expr": "<cron expression>",
    "tz": "<IANA timezone>"
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "RECURRING TASK: <detailed task instruction>. Execute this task now and report the results."
  },
  "delivery": {
    "mode": "announce",
    "channel": "<detected channel>",
    "to": "<detected target>",
    "bestEffort": true
  }
}
```

**定期执行（间隔）：**

```json
{
  "name": "Recurring Task: <short description>",
  "schedule": {
    "kind": "every",
    "everyMs": "<interval in milliseconds>"
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "RECURRING TASK: <detailed task instruction>. Execute this task now and report the results."
  },
  "delivery": {
    "mode": "<announce or none>",
    "channel": "<detected channel>",
    "to": "<detected target>",
    "bestEffort": true
  }
}
```

**无声执行任务（不显示结果）：**

```json
{
  "name": "Task: <short description>",
  "schedule": {
    "kind": "at",
    "at": "<ISO 8601 timestamp>"
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "SCHEDULED TASK (SILENT): <detailed task instruction>. Execute this task now. No delivery needed — log results only."
  },
  "deleteAfterRun": true
}
```

### 第六步：向用户确认

`cron.add` 成功执行后，回复用户：

```
Task scheduled!
Command: <task description>
Runs: <friendly time description> (<ISO timestamp or cron expression>)
Delivery: <channel or "silent">
Job ID: <jobId> (use "/schedule cancel <jobId>" to remove)
```

---

## 规则

1. **对于单次执行的任务，** 必须设置 `deleteAfterRun: true`。定期执行的任务可以省略此设置。
2. **始终使用 `sessionTarget: "isolated"` — 任务在独立的沙箱环境中执行。
3. **始终使用 `wakeMode: "now"` — 确保任务在预定时间执行。
4. **当结果展示方式为“announce”时，** 必须设置 `delivery.bestEffort: true`。
5. **切勿使用 `act:wait` 或循环来延迟任务执行。Cron 会自动处理时间控制。
6. **始终使用用户的本地时区**，切勿使用 UTC 作为默认值。
7. **对于定期执行的任务，** 不要设置 `deleteAfterRun`。
8. **务必返回 `jobId`，以便用户后续可以取消或查看任务状态。
9. **在安排破坏性任务之前必须获得用户确认**。切勿自动安排 `rm`、`drop`、`kill` 等操作。
10. **任务名称前缀** 必须加上 `Task:`（单次执行）或 `Recurring Task:`（定期执行），以便于审计和清理。

## 平台要求

此技能无需依赖任何外部库，因为它依赖于 OpenClaw 的内置功能：

- **Cron 调度**：`cron.add`、`cron.list`、`cron.remove` 是 OpenClaw 的内置代理工具。
- **任务执行**：定时执行的代理会话可以使用 Bash、文件工具和其他代理功能来执行命令。
- **结果发送**：OpenClaw 会在 `openclaw.json` 中存储频道凭据，此技能无需使用 API 密钥。
- **时区**：使用主机操作系统的本地时区。

## 安全与权限

此技能会创建带有 `payload.kind: "agentTurn"` 的 cron 任务，这些任务会在独立的代理会话中执行。以下安全措施会被强制执行：

- **`sessionTarget: "isolated"` — 每个定时任务都在独立的沙箱环境中执行，无法访问主会话的状态、历史记录或工具。
- **`deleteAfterRun: true` — 单次执行的任务执行完成后会自动删除，防止任务堆积。
- **破坏性操作需要确认** — 在安排修改或删除数据的命令（如 `rm`、`drop`、`kill` 等）之前，必须获得用户确认。
- **任务名称有明确前缀** — 所有任务名称前都会加上 `Task:` 或 `Recurring Task:`，便于通过 `cron.list` 进行审计。
- **此技能不是持续运行的** — 只有在用户触发 `/schedule` 时才会激活。
- **用户控制** — 每个任务都会返回一个 `jobId`，用户可以随时通过 `/schedule list` 查看或使用 `/schedule cancel <jobId>` 取消任务。
- **无权限升级** — 定时执行的代理会话继承与普通代理会话相同的权限和工具访问权限。

## 故障排除

- **任务未执行？** — 使用 `cron.list` 检查。确认调度时的代理是否正在运行。
- **命令失败？** — 查看代理的输出日志以获取错误详情。
- **如何查看无声执行的任务结果？** — 使用 `cron.list` 查看 `lastStatus` 和 `lastError` 字段。
- **任务过多？** — 参考 `references/TEMPLATES.md` 了解任务清理方法。

## 参考资料

有关复制模板和任务清理的详细信息，请参阅 `references/TEMPLATES.md`。