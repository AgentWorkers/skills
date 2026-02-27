---
name: to-do
description: 赋予你的人工智能在未来执行任务的能力。你可以安排延迟提示和一次性提醒，这些提醒会自动在指定时刻唤醒代理程序，以执行工作流程、检查系统或发送通知。
metadata: {"clawdbot":{"emoji":"⏰","requires":{"bins":["node"],"env":["OPENCLAW_BIN","OPENCLAW_TZ"]}}}
---
# 技能：临时任务管理（To-Do Tasks）

<identity>
一个跨平台任务调度器，使用操作系统的原生调度器（Linux/macOS 上的 `at`，Windows 上的 `schtasks`）来安排一次性延迟任务。它可以在未来的某个确切时间唤醒代理，并注入完整的上下文信息。</identity>

<goal>
安排、列出和管理那些会在用户所在时区精确时间执行的临时任务——确保代理在醒来时能够接收到包含所有必要信息的任务指令，确保任务能够正确路由且没有任何歧义。</goal>

---

## 必需的环境变量

| 变量 | 描述 | 示例 |
|---|---|---|
| `OPENCLAW_BIN` | `openclaw` 可执行文件的绝对路径 | `/usr/bin/openclaw` 或 `C:\Program Files\OpenClaw\openclaw.exe` |
| `OPENCLAW_TZ` | 用户的 IANA 时区 | `America/Mexico_City`、`Europe/Madrid`、`Asia/Tokyo` |

如果缺少这两个变量中的任何一个，该技能将无法启动。

> **为什么需要 `OPENCLAW_TZ`？** 服务器可能运行在 UTC 时区，而用户可能位于不同的时区。这个变量确保了“安排在 15:00”是指用户所在时区的 15:00，而不是服务器的时区。</solution>

---

## 命令

```bash
# Schedule a task (timezone is optional — defaults to OPENCLAW_TZ)
node skills/to-do/to-do.js schedule "<YYYY-MM-DD HH:mm>" "<instruction>" "<user_id>" "<channel>" ["<timezone>"]

# Get current time in user's timezone
node skills/to-do/to-do.js now ["<timezone>"]

# List pending tasks
node skills/to-do/to-do.js list

# Delete a task by ID
node skills/to-do/to-do.js delete <ID>
```

---

## 指令说明

<instructions>

<always>
- 在处理任何相对时间（如“明天”、“两小时后”、“今晚”）之前，先运行 `now` 命令。服务器的时间并不等于用户的时间。请使用 `now` 的输出结果作为“今天”、“明天”和“现在”的时间参考。
- 在调用 `schedule` 之前，将自然语言描述转换为绝对的 `YYYY-MM-DD HH:mm` 格式的时间戳。
- 编写任务指令时，要假设对方对相关背景一无所知。未来的你将在一个完全隔离的会话中执行任务，且不会记得这次交流的任何内容。
- 每条指令中都必须包含：文件的完整路径或 URL、完整的名称（不要使用代词）、需要执行的具体操作，以及所需的技能或工具。
- 确保在指令中注入当前会话的 `user_id` 和 `channel`，以便任务能够正确路由。
- 在执行 `delete` 命令之前，先运行 `list` 命令以确认任务 ID 是否正确。</always>

<never>
- 在执行 `schedule` 命令之前，**必须先运行 `now` 命令**。 → 相反，应先运行 `now` 确认日期和时间，然后再进行调度。
- **不要安排含糊不清的指令**。 → 应要求用户先提供详细信息后再创建任务（参见下面的触发条件）。
- 在任务指令中**不要使用代词**（如“他”、“她”、“他们”）。 → 应使用完整的名称和明确的参照对象。
- 在删除任务时**不要猜测任务 ID**。 → 应先运行 `list` 命令确认 ID，然后再删除任务。
- **不要使用服务器的系统时间来解析相对时间**。 → 应始终使用 `now` 命令的输出结果作为时间参考。</never>

</instructions>

---

## 含糊的请求触发条件——在安排任务前请先询问用户

<vague_triggers>
如果用户的请求符合以下任何一种情况，请在安排任务之前**停止并询问用户**：

| 用户的请求 | 缺少哪些信息 |
|---|---|
| “提醒我明天下午 5 点发送邮件” | 需要发送给谁？邮件内容是什么？ |
| “稍后检查服务器” | 是哪个服务器？需要检查什么内容？ |
| “与他联系” | 联系谁？关于什么事情？通过哪个渠道？ |
| “明天做那件事” | 需要做什么？预期的结果是什么？ |

**规则：** 如果根据用户提供的信息无法生成一条完整的、自包含的指令，那么你就没有足够的信息来安排任务。</vague_triggers>

---

## 示例

<example id="goodInstruction">
  <input>User: “提醒我明天下午 5 点检查后端仓库的 PRs。”</input>
  <output>
    1. 运行 `now` → “🕒 当前时间（America/Mexico_City）：2026-02-26 下午 2:45” → 明天 = 2026-02-27
    2. 询问用户： “后端仓库是哪个？具体需要检查什么？”
    3. 用户确认： “是 GitHub 上的 ‘backend-api’ 仓库，需要检查认证模块是否有待处理的 PR。”
    4. 安排任务：
    ```bash
    node skills/to-do/to-do.js schedule "2026-02-27 17:00" \
      "Check the 'backend-api' repo on GitHub. If there are pending PRs for the authentication module, send Alice (alice@company.com) a Slack reminder to review them before the 5 PM deployment freeze. Reference deployment logs at /var/log/deploy.log." \
      "7684875449" "telegram"
    ```
    5. 使用以下格式确认任务信息。
  </output>
</example>

<example id="badInstruction">
  <input>“提醒他稍后推送代码。”</input>
  <output>
    ❌ 不能安排这个任务。缺少以下信息：需要推送代码给谁？哪个仓库？具体是哪个分支？“稍后”指的是什么时间？
    → 请用户先提供所有缺失的详细信息。</output>
</example>

<example id="time_resolution">
  <input>User: “设置一个两小时后的提醒。”</input>
  <output>
    1. 运行 `now` → “🕒 当前时间（America/Mexico_City）：2026-02-26 下午 2:45”
    2. 计算：2:45 + 2 小时 = 4:45
    3. 询问用户提醒内容（如果未指定）
    4. 使用绝对时间戳安排任务
  </output>
</example>

---

## 任务执行后的输出格式

任务安排完成后，回复用户时请自然地表达，但**必须包含以下确认信息**：

```
> `[Day, Month DD · HH:MM TZ]`
> *[Exact instruction left for the future agent]*
```

<example id="output">
已完成！以下是我为未来的自己留下的任务指令：

> **2026年2月27日，星期四，下午 5:00（CST）**
> *请检查 GitHub 上的 ‘backend-api’ 仓库。如果认证模块有未处理的 PR，通过 Slack 提醒 Alice 在下午 5 点的部署冻结之前查看它们。*
</example>

---

## 常见错误

| 错误 | 原因 | 解决方法 |
|---|---|---|
| 缺少必要的环境变量 | 未设置 `OPENCLAW_BIN` 或 `OPENCLAW_TZ` | 将这些变量添加到 `.env` 文件或 shell 配置文件中 |
| `at` 命令找不到 | Linux/macOS 上的 `atd` 守护进程未运行 | 使用 `sudo systemctl enable atd && sudo systemctl start atd` 启动 `atd` 守护进程 |
| 任务执行了但代理没有所需上下文 | 安排了含糊不清的指令 | 重新安排任务，确保指令信息完整 |
| 任务执行时间错误——提前或延迟 | 使用了服务器的时间而不是 `now` 的输出结果 | 必须先运行 `now` 命令；切勿依赖服务器的时间 |
| 删除了错误的任务 | 误删了任务 | 先运行 `list` 命令确认任务 ID，然后再删除任务 |