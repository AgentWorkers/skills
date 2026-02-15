---
name: google-calendar
description: **管理 Google 日历**：用于创建、更新和查询事件，以及安排日程和查看用户的可用时间。当用户提到日历、会议、预约或 Google 日历时，请使用此功能。
---

# Google 日历

## 首次设置

1. 检查 `~/.config/google-calendar-skill/client.json` 文件是否存在（如果存在，则直接跳到第 2 步；如果不存在，请引导用户参考源代码仓库中的 SETUP.md 文件）。
2. 运行 `bun run auth.ts login` — 这将打开浏览器，用户需要登录他们的 Google 账户。
3. 登录成功后，脚本会显示用户的认证邮箱地址，请将其展示给用户。
4. 询问用户这个账户的用途（例如：“工作”或“个人”），以及可选的账户**目的**（例如：“工作会议”或“个人用途”）。然后执行以下操作：
   ```bash
   bun run auth.ts label <chosen-name> [purpose]
   ```
   如果用户没有提供账户用途，可以根据他们的描述进行猜测，并更新 `config.json` 文件中的 `accounts.<label>.purpose` 字段。
5. 询问用户是否要连接另一个 Google 账户。如果是，请重复第 2 步的操作。
6. 对于每个账户，确保 `config.json` 文件中都记录了该账户的用途。
7. 列出用户的日历，以便他们查看可用的日历（会为所有账户列出日历信息；输出结果会标明账户名称）：
   ```bash
   bun run calendar.ts calendars
   ```

## 工作目录

所有命令都必须从 `scripts/` 目录下执行。请确定相对于此 SKILL.md 文件的路径：

```bash
cd "$(dirname "<path-to-this-SKILL.md>")/scripts"
```

## 认证命令

这些命令需要在 `scripts/` 目录下执行。访问令牌会在过期后自动刷新。所有认证命令都支持 `--account <别名>` 参数（默认值为 `default`）。

| 命令                                      | 描述                                                                                   |
| -------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `bun run auth.ts login`                      | 启动 OAuth 登录流程（打开浏览器）                                                          |
| `bun run auth.ts status`                     | 检查认证状态                                                               |
| `bun run auth.ts accounts`                   | 列出所有已认证的账户及其邮箱地址                                               |
| `bun run auth.ts label <名称> [描述]` | 重命名账户；描述可设置为账户的用途（默认情况下会重命名为 `default`）                         |
| `bun run auth.ts refresh`                    | 强制刷新访问令牌                                                            |
| `bun run auth.ts revoke`                     | 撤销令牌并删除本地凭证                                                |
| `bun run auth.ts token`                      | 打印有效的访问令牌（令牌会自动刷新）                                               |

## 日历命令

这些命令也需要在 `scripts/` 目录下执行。

- `list, get, update, delete, calendars, freebusy` — 这些命令不支持 `--account` 参数。脚本会为所有连接的账户执行操作，并在输出中注明账户名称（例如：`── work ──`, `── personal ──`）。
- `create, quick` — 这些命令需要 `--account <别名>` 参数（默认值为 `default`）。创建事件时，脚本会从 `config.json` 文件中选择相应的账户。
- 共享参数：`--calendar <ID>`（默认值为 `primary`）。仅 `create` 和 `quick` 命令支持此参数。

| 命令                                                              | 描述                                     |
| -------------------------------------------------------------------- | ----------------------------------------------- |
| `bun run calendar.ts list [--from 日期] [--to 日期] [--max N]`       | 列出所有账户的即将发生的事件（结果会标明账户名称）    |
| `bun run calendar.ts get <事件ID>`                                  | 获取事件详情（尝试查询所有账户的信息，结果会标明账户名称） |
| `bun run calendar.ts create --summary "..." [选项] --account X`   | 在账户 X 上创建事件                    |
| `bun run calendar.ts quick "文本" --account X`                       | 在账户 X 上快速创建事件                          |
| `bun run calendar.ts update <事件ID> [--summary ...] [--start ...] [--attendees ...] [--add-attendees ...] [--remove-attendees ...]` | 更新事件信息（尝试查询所有账户的信息） |
| `bun run calendar.ts delete <事件ID>`                               | 删除事件（尝试查询所有账户的信息）            |
| `bun run calendar.ts calendars`                                      | 列出所有账户的日历信息（结果会标明账户名称）      |
| `bun run calendar.ts freebusy --from 日期 --to 日期`                 | 查看账户的日程安排（结果会标明账户名称）               |

### 创建事件的参数

请使用以下参数名称，CLI 不支持别名：

- `--summary`（必填）：事件标题
- `--start`：事件开始时间
- `--end`：事件结束时间
- `--description`：事件描述
- `--location`：事件地点
- `--attendees`：参与者邮箱地址（用逗号分隔）
- `--all-day`：表示事件为全天事件

日期格式需符合 JavaScript 的解析规则。如果省略 `--start`，默认为当前时间后 1 小时；如果省略 `--end`，默认事件持续 1 小时。

```bash
# Timed event
bun run calendar.ts create --summary "Standup" --start "2026-02-07T10:00" --end "2026-02-07T10:30"
# All-day event
bun run calendar.ts create --summary "Vacation" --start "2026-03-01" --end "2026-03-05" --all-day
```

### 更新事件的参数

`--summary`, `--start`, `--end`, `--description`, `--location` 的参数与创建事件时使用的参数相同。这些参数用于更新事件信息。

参与者相关参数：
- `--attendees "a@b.com,c@d.com"`：用指定列表替换所有参与者
- `--add-attendees "e@f.com,g@h.com"`：向现有参与者列表中添加新参与者（重复的地址会被忽略）
- `--remove-attendees "a@b.com"`：从参与者列表中移除指定参与者
- `--no-notify`：不发送电子邮件邀请（默认情况下，参与者信息变更时会发送邀请）

```bash
# Add attendees to an existing event (sends invites)
bun run calendar.ts update abc123 --add-attendees "alice@example.com,bob@example.com"
# Replace all attendees without sending invites
bun run calendar.ts update abc123 --attendees "carol@example.com" --no-notify
# Remove an attendee
bun run calendar.ts update abc123 --remove-attendees "alice@example.com"
```

## 多个账户

每次登录操作都会将账户信息保存到 `default` 标签下。可以使用 `label` 参数为账户重新命名（可选地指定账户用途），然后再次登录以使用其他账户：

```bash
bun run auth.ts login
bun run auth.ts label work "Work meetings, standups"
bun run auth.ts login
bun run auth.ts label personal "Personal appointments, family"
```

`--account` 参数仅用于 `create` 和 `quick` 命令；其他日历命令会为所有账户执行操作，并在输出中注明账户名称：

```bash
bun run calendar.ts list
bun run calendar.ts create --summary "Dentist" --account personal --start "2026-02-10T09:00"
```

**账户管理**

- `bun run auth.ts accounts`：列出所有已认证的账户及其邮箱地址
- `bun run auth.ts label <新名称> [描述] --account <旧名称>`：重命名账户；描述可设置为账户的用途

## 账户配置（config.json）

该技能将账户的用途信息保存在与 `SKILL.md` 文件位于同一目录下的 `config.json` 文件中。执行 `label` 命令时，系统会创建或更新该文件。在重命名账户时，可以将描述作为第二个参数传递以设置账户的用途；之后也可以直接在 `config.json` 文件中修改该信息。

- **文件路径**：与 `SKILL.md` 文件位于同一文件夹，例如：`$(dirname "<path-to-this-SKILL.md>")/config.json`
- **文件格式**：
  ```json
  {
  	"accounts": {
  		"work": { "purpose": "Work meetings, standups, sprint reviews" },
  		"personal": { "purpose": "Personal appointments, family events" }
  	}
  }
  ```

**创建事件时的注意事项：** 在创建事件之前，请先读取 `config.json` 文件。根据用户的意图或账户的用途来选择 `--account` 参数（以及可选的日历）。如果用户没有指定账户，并且配置文件中只有一个账户，系统会自动使用该账户；如果有多个账户，则需要根据上下文或用户输入来选择账户。

**列出或修改事件时的注意事项：** 在列出或修改事件信息时，只需执行一次日历命令（不需要指定 `--account` 参数）。脚本会为所有连接的账户执行操作，并在输出中列出每个账户的日历信息。

## 工作流程

在处理用户的日历请求时，请按照以下流程操作：

```
- [ ] 1. cd into scripts/ directory
- [ ] 2. Check auth: bun run auth.ts accounts
- [ ] 3. If no accounts → run First-Time Setup above
- [ ] 4. **Creating events:** read config.json and pick --account; run create/quick with that --account. **Listing or changing events:** run the command with no --account (script iterates all accounts and labels output).
- [ ] 5. Run the appropriate calendar command (--account only for create/quick)
- [ ] 6. If 401 error → bun run auth.ts refresh [--account ...] → retry
- [ ] 7. If refresh fails → bun run auth.ts login [--account ...]
- [ ] 8. Parse and present results to user
```

## 其他资源

有关事件字段、查询参数、事件重复规则和参与者选项的详细信息，请参阅 [references/API.md](references/API.md)。