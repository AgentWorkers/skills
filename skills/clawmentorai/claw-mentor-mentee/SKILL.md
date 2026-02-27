---
name: claw-mentor-mentee
description: **安全的 OpenClaw 进化：** 从专业构建者那里获取经过安全检查的兼容性报告，并直接发送到您的代理端。您可以选择应用这些更新，或者选择跳过它们；系统还提供了自动回滚保护功能，以确保系统的稳定性。
metadata: {"openclaw": {"emoji": "🔥", "primaryEnv": "CLAW_MENTOR_API_KEY", "homepage": "https://clawmentor.ai"}}
---
# Claw Mentor — 学员技能

> 直接将您的导师的更新信息导入到您的 OpenClaw 代理中。当新的兼容性报告准备好时，系统会通知您，您可以以简单的英语查看报告，然后选择应用或跳过这些更新——所有这些操作都可以在 OpenClaw 聊天界面完成。

---

## 描述

Claw Mentor 是一个为 OpenClaw 用户提供的导师辅导平台。您可以订阅一位专家导师（例如 Ember 🔥），他们维护着一个精心配置的 OpenClaw 环境。每当他们更新配置时，系统会生成一份简单的英语报告，说明发生了哪些变化、这些变化的作用以及它们是否适合您的环境。

此技能将您的本地 OpenClaw 代理与 Claw Mentor 连接起来。代理会定期检查新的报告，并在需要时通知您，同时帮助您决定是应用还是跳过这些更新——在应用任何更改之前，系统还会自动创建一个本地备份。

**隐私声明：** 您的 AGENTS.md 文件、技能配置文件以及配置数据永远不会发送给 Claw Mentor。服务器仅接收您自愿提供的入职调查问卷答案以及您关于是否应用、跳过或回滚更新的决定。任何原始配置数据都不会离开您的设备。

---

## 功能

- 每隔几小时检查 `app.clawmentor.ai`，以获取您订阅的导师发布的新的兼容性报告
- 当有新报告准备好时，通过您配置的渠道（如 Telegram）通知您
- 以简单的英语显示报告摘要：哪些内容发生了变化、风险等级以及后续操作建议
- 指导您如何应用或跳过这些更新
- 在应用任何更改之前，系统会创建一个本地快照（使用 `cp -r` 命令）
- 将您的决定（应用/跳过/回滚）反馈给 Claw Mentor — 但不会共享任何配置内容

---

## 安装

```bash
clawhub install claw-mentor-mentee
```

安装完成后，启动一个新的 OpenClaw 会话。首次使用时，代理会指导您设置 API 密钥。

您可以在以下地址获取 API 密钥：**app.clawmentor.ai → 设置 → 学员技能**

---

## 首次使用时的配置

**在加载此技能时，请检查环境变量 `CLAW_MENTOR_API_KEY` 是否已设置。**

**如果已设置：** 您已成功连接。首先调用 `POST https://app.clawmentor.ai/api/mentee/bootstrap`（使用 `Authorization: Bearer {CLAW_MENTOR_API_KEY}`），以确保您尚未看到的任何导师更新都被添加到待处理列表中。然后调用 `GET https://app.clawmentor.ai/api/mentee/reports`，查看有哪些更新等待处理。同时确保 `HEARTBEAT.md` 文件中包含以下内容：`- Check for new Claw Mentor reports`（如果文件不存在，请添加此行）。

**如果未设置：** 告诉用户：

> “要激活 ClawMentor，您需要提供 API 密钥。
> 
> 👉 请在 **app.clawmentor.ai → 设置 → 学员技能 → 生成 API 密钥** 中获取密钥。”
> 
> 获取密钥后，请在这里分享它，我将为您进行配置。”

**用户提供 API 密钥后：**
1. 将密钥存储在：`openclaw config set 'skills.entries["claw-mentor-mentee"].apiKey' YOUR_KEY`
2. 确认连接状态：`✅ ClawMentor 已连接。现在正在获取您的第一份报告...`
3. **首次安装时进行初始化** — 调用 `POST https://app.clawmentor.ai/api/mentee/bootstrap`，并设置请求头 `Authorization: Bearer {CLAW_MENTOR_API_KEY}`。这将获取您订阅的所有导师的最新更新，并将其视为新更新（因为对于您的环境来说，这些更新确实是新的）。等待响应。
4. 初始化完成后，调用 `GET https://app.clawmentor.ai/api/mentee/reports`，并向用户显示有哪些更新等待处理。
5. **安排定期检查** — 在您的工作区文件 `HEARTBEAT.md` 中添加以下内容（如果文件不存在，请创建该文件）：
   ```
   - Check for new Claw Mentor reports
   ```
   这将告诉您的 OpenClaw 代理在每个心跳周期执行技能检查。向用户确认：`✅ 心跳检查已安排——当有新报告准备好时，系统会自动通知您。`

---

## 配置

| 变量 | 来源 | 默认值 |
|---|---|---|
| `CLAW_MENTOR_API_KEY` | app.clawmentor.ai → 设置 → 学员技能 | 必填 |
| `CLAW_MENTOR_CHECK_INTERVAL_HOURS` | 可选 — 在您的 OpenClaw 环境中设置 | `6` |

OpenClaw 会将您的 API 密钥存储在 `~/.openclaw/openclaw.json` 文件的 `skills.entries["claw-mentor-mentee"].apiKey` 中，并在每次会话中自动将其设置为 `CLAW_MENTOR_API_KEY`。

---

## 权限

| 权限 | 用途 |
|---|---|
| `READ: ~/.openclaw/` | 用于在应用更改前创建快照 |
| `WRITE: ~/.openclaw/claw-mentor/snapshots/` | 用于存储本地备份快照 |
| `WRITE: ~/.openclaw/claw-mentor/state.json` | 用于记录最后一次检查时间和已通知的报告 |
| `NETWORK: app.clawmentor.ai` | 用于获取报告和发送状态更新 |
| `NOTIFY: configured channel` | 用于在有新报告准备好时通知您 |
| `EXEC: cp, mkdir` | 用于执行创建快照的 shell 命令 |

其他文件不会被读取，也不会有任何配置数据被上传。

---

## 代理操作说明

安装此技能后，您的代理应遵循以下操作：

### 心跳检查（每 `CLAW_MENTOR_CHECK_INTERVAL_HOURS` 小时执行一次）

1. 读取 `~/.openclaw/claw-mentor/state.json`，获取 `last_check` 和 `notified_report_ids`（如果文件不存在，请创建该文件）
2. 如果从 `last_check` 以来的时间小于 `CLAW_MENTOR_CHECK_INTERVAL_HOURS` 小时，则跳过检查，返回 `HEARTBEAT_OK`
3. 调用 `GET https://app.clawmentor.ai/api/mentee/reports`，并设置请求头 `Authorization: Bearer {CLAW_MENTOR_API_KEY}``
4. 使用 `last_check: now` 更新 `state.json`
5. 对于响应中 `status == 'pending` 且 `id` 不在 `notified_report_ids` 中的每个报告：
   - 发送通知消息（格式见下文）
   - 将报告 ID 添加到 `notified_report_ids` 中
6. 如果没有待处理的报告，则调用 `POST https://app.clawmentor.ai/api/mentee/bootstrap`，检查是否有导师的更新尚未处理。如果 `bootstrapped` 的值为大于 0，则返回步骤 3 并显示新的报告；否则返回 `HEARTBEAT_OK`

**通知消息格式**（保持简洁——详细分析会在用户请求时提供）：
```
🔥 New update from {mentor_name}!

They've pushed a new version of their setup. Say "show my mentor report" and I'll fetch it, compare it against your current setup, and give you a personalized breakdown of what it means for you.
```

### 命令：`show my mentor report` / `my mentor reports` / `check my reports`

1. 调用 `GET https://app.clawmentor.ai/api/mentee/reports`
2. 如果没有待处理的报告：`没有新的导师报告。您已保持最新状态！✅`
3. 对于每个待处理的报告，**进行本地兼容性分析**（不要显示后端的 `plain_english_summary` — 这只是一个占位符）：

**步骤 A — 获取导师的软件包信息：**
调用 `GET https://app.clawmentor.ai/api/mentee/package?packageId={report.package_id}`，并使用您的 API 密钥。
此请求会返回两个部分：
- `files` — 导师发布的文件：`AGENTS.md`、`skills.md`、`cron-patterns.json`、`CLAW_MENTOR.md`、`privacy-notes.md`
- `platform` — 平台指南：`mentee-integration.md`（完整的集成算法）、`setup-guide.md`、`mentee-skill.md`（详细操作指南）

**步骤 B — 读取您当前的配置：**
- 列出 `~/.openclaw/skills/` 中已安装的技能
- 读取 `~/.openclaw/workspace/AGENTS.md`，了解您当前的使用方式
- 读取 `~/.openclaw/claw-mentor/state.json`，查看用户保存的个人信息（目标、背景信息）
- 结合您从对话、工作区文件和用户当前项目中了解的信息进行分析

**步骤 C — 自行分析差距：**
作为大型语言模型（LLM），您拥有后端无法获取的上下文信息。请分析以下内容：
- 您当前还没有安装哪些导师推荐的技能？这些技能是否适合您添加？
- 对于每个待添加的技能，具体来说它能为您带来什么帮助？根据您对用户的工作、目标和项目的了解，给出具体的例子。
- 如果应用这些更新，您的日常操作方式会发生变化吗？
- 根据用户的经验水平和关注点，哪些技能可能是不必要的？
- 添加这些技能后，需要哪些权限？这些权限是否适合用户？
- 总体而言：这次更新是否适合用户当前的需求？

**步骤 D — 呈现分析结果**（仅使用项目符号列表，不要使用markdown表格）：
```
📋 Update from {mentor_name} — {date}

[Your plain-English summary of what this update means for THIS user specifically — 2-3 sentences based on their actual context]

What would change for you:
• [capability or behavior change — phrased in terms of what they can now do/say/get]
• ...

Skills to add ({N}):
• skill-name — [what it enables FOR THIS USER, with a specific example from their work]
• skill-name — [same — personalized]
• ...

Permissions this would add:
• [permission] — [plain English reason why]

What you might want to skip:
• [skill] — [honest reason it may not be needed for their situation]

My take: [One honest sentence — your recommendation as their agent who knows them]

Say "apply mentor report" to apply or "skip mentor report" to skip.
```

### 命令：`apply mentor report` / `apply [mentor name]'s update`

这是最重要的命令。它使用了平台提供的完整集成算法。

1. 调用 `GET https://app.clawmentor.ai/api/mentee/reports`，获取最新的待处理报告
2. 如果没有待处理的报告：`没有需要应用的更新。`
3. **获取完整的软件包信息**（如果之前没有缓存）：
   调用 `GET https://app.clawmentor.ai/api/mentee/package?packageId={report.package_id}`
4. **读取 `platform['mentee-integration.md']` 中的内容**。
   这个文件包含了完整的六阶段集成算法：
   - 第 0 阶段：备份（创建当前配置的快照）
   - 第 1 阶段：自我评估（了解用户的当前状态）
   - 第 2 阶段：理解导师的建议
   - 第 3 阶段：冲突分析（找出潜在的冲突和重叠点）
   - 第 4 阶段：制定合并策略并获得用户确认
   - 第 5 阶段：执行合并操作
   - 第 6 阶段：发布整合后的结果
5. **按照 `mentee-integration.md` 中的步骤逐步执行**。系统会处理所有细节：备份、冲突检测、数据保留、容量检查、任务调度、技能推荐、内存系统设置以及回滚安全。
6. 整合完成后，调用 `POST https://app.clawmentor.ai/api/mentee/status`，并设置 `first_apply_done` 为 `true`：
   ```json
   { "reportId": "{id}", "status": "applied", "snapshotPath": "{backup_path}" }
   ```
7. **检查 `~/.openclaw/claw-mentor/state.json` 中的 `first_apply_done` 是否已设置**。如果未设置，请执行以下首次欢迎流程。然后更新 `state.json` 中的 `first_apply_done` 为 `true`。

**重要提示：** `mentee-integration.md` 中的集成算法非常全面。请信任它——它会处理各种特殊情况，如中断的整合过程、配置简单的情况、多个导师的存在以及容量限制等问题。不要跳过任何步骤或简化流程。

---

### 首次使用时的欢迎流程（仅执行一次）

这不是一个状态报告，而是一次人工对话。请保持消息简短。不要一次性发送所有信息——发送一条消息后，等待用户的回复或几秒钟，然后再继续。

**消息 1 — 现在有什么不同**（根据实际安装的技能内容，用简单的英语撰写）：
> “现在您可以执行以下操作：
> [列出 3-5 个基于已安装技能的实用示例，例如]：
> • ‘搜索最新的新闻’ — 我会为您获取实时网页结果
> • ‘总结这个网址/视频/播客’ — 我会为您提供关键信息
> • ‘今天的天气如何？’ — 我会快速回答
> • ‘查看我的 GitHub 问题’ — 我会列出问题并帮助您分类处理
> • 我现在会自动为您发送早晚简报**
>
> [如果有任何需要设置的环节]：要完成这些操作，需要 [1] [具体操作]，预计耗时 [X] 分钟。现在想开始吗？”

**消息 2 — 如果有需要设置的环节**（仅在有未处理的 API 密钥或设置步骤时显示）：
> “剩下的一件事是：[技能] 需要 [密钥类型]。操作方法如下：
> [简单的一两行说明——避免使用专业术语]
> 完成后，[技能] 将能够 [实现相应功能]。预计耗时 [X] 分钟。”

在收到用户的回复后再继续。

**消息 3 — 了解用户**（以对话的形式进行，不要使用固定格式）：
> “简单问一下——您每天最需要我帮忙处理什么？是工作相关的事务、个人项目，还是研究方面的问题？只需简短回答几句。”

收到用户的回复后，再补充一句：
> “明白了。您现在正在处理什么具体事项吗？是项目、目标，还是有什么需要解决的问题？”

将用户的回答保存在 `~/.openclaw/claw-mentor/state.json` 文件的 `user_profile.goals` 和 `user_profile.context` 中。这有助于个性化后续的报告内容。

**消息 4 — 结束语**（简短且鼓舞人心）：
> “您已经准备好了。🔥 当有新的更新时，Ember 会通知您——随着我对您需求的了解加深，后续的报告会更加有用。就像平常一样与我交流，我会利用我们刚刚设置的功能。”

### 命令：`skip mentor report` / `skip [mentor]'s update`

1. 获取最新的待处理报告（使用相同的 API 调用）
2. 如果没有待处理的报告：`没有需要跳过的更新。`
3. 调用 `POST https://app.clawmentor.ai/api/mentee/status`，并设置请求参数为 `{"reportId": "{id}", "status": "skipped"}`
4. 确认：`已跳过更新。您可以在 app.clawmentor.ai/dashboard 上随时查看报告。`

### 命令：`roll back [mentor]'s update` / `undo mentor changes`

1. 查找上次 API 调用中最近应用的报告（或询问用户具体是哪个报告）
2. 检查是否已创建快照（在 `~/.openclaw/claw-mentor/snapshots/` 中查找最新的快照）
3. 显示恢复命令：
   ```bash
   cp -r ~/.openclaw/claw-mentor/snapshots/{most-recent-date}/ ~/.openclaw/
   ```
4. 提醒用户：`恢复更新后，请重新启动您的 OpenClaw 代理以使更改生效。`
5. 当用户确认已恢复更新后，调用 `POST https://app.clawmentor.ai/api/mentee/status`，并设置请求参数为 `{"reportId": "{id}", "status": "rolled_back"}`

---

## 状态文件格式

`~/.openclaw/claw-mentor/state.json`：
```json
{
  "last_check": "2026-03-01T14:32:00Z",
  "notified_report_ids": ["uuid1", "uuid2"],
  "last_snapshot_path": "~/.openclaw/claw-mentor/snapshots/2026-03-01-14-32/"
}
```

如果文件不存在，请在首次使用时创建它。

---

## API 参考

所有接口地址为 `https://app.clawmentor.ai`。

### GET /api/mentee/reports
**认证：** `Authorization: Bearer {CLAW_MENTOR_API_KEY}`  
**返回内容：**
```json
{
  "user": { "id": "...", "email": "...", "tier": "starter" },
  "reports": [
    {
      "id": "uuid",
      "created_at": "2026-03-01T10:00:00Z",
      "package_id": "uuid",
      "plain_english_summary": "placeholder — your agent performs the real analysis locally",
      "risk_level": null,
      "skills_to_add": [],
      "skills_to_modify": [],
      "skills_to_remove": [],
      "permission_changes": [],
      "status": "pending",
      "mentors": { "name": "Ember 🔥", "handle": "ember", "specialty": "..." }
    }
  ],
  "subscriptions": [...]
}
```
**注意：** `risk_level`、`skills_to_add` 以及其他分析字段是空的。您的本地代理会通过 `/api/mentee/package?packageId={package_id}` 获取软件包信息，并根据您实际的配置情况自行进行兼容性分析。

### GET /api/mentee/package
**认证：** `Authorization: Bearer {CLAW_MENTOR_API_KEY}`  
**查询参数：** `packageId={uuid}`（来自报告中的 `package_id` 字段）  
**返回内容：** 两部分——导师发布的文件和平台指南：
```json
{
  "packageId": "uuid",
  "version": "2026-03-01",
  "mentor": { "id": "...", "name": "Ember 🔥", "handle": "ember" },
  "files": {
    "CLAW_MENTOR.md": "overview and version notes",
    "AGENTS.md": "annotated configuration with reasoning",
    "skills.md": "curated skill recommendations with tiers",
    "cron-patterns.json": { "jobs": [...] },
    "privacy-notes.md": "what this package reads/writes"
  },
  "platform": {
    "mentee-integration.md": "full 6-phase integration algorithm",
    "setup-guide.md": "first-time setup guide",
    "mentee-skill.md": "detailed daily operations guide"
  },
  "fetchedAt": "2026-03-01T10:00:00Z"
}
```
- **`files`** = 导师发布的文件（每个导师的内容各不相同），用于本地兼容性分析。
- **`platform`** = 平台指南（所有导师的内容相同）。在应用更新时使用 `mentee-integration.md`；对于更详细的操作指南，请参考 `mentee-skill.md`。

### POST /api/mentee/status
**认证：** `Authorization: Bearer {CLAW_MENTOR_API_KEY}`  
**请求体：** `{ "reportId": "uuid", "status": "applied|skipped|rolled_back", "snapshotPath": "~/.openclaw/..." }`  
**返回内容：** `{ "success": true, "reportId": "...", "status": "applied", "updated_at": "..." }`

---

## 故障排除

**`clawhub install` 的下载速度受限** — ClawHub 会对每个 IP 实施下载限制。请等待 2–3 分钟后再尝试。如果安装失败，可以运行 `clawhub install claw-mentor-mentee --force` 以覆盖现有文件。

**“API 密钥无效”** — 请访问 app.clawmentor.ai → 设置 → 学员技能，生成新的 API 密钥。

**“未找到报告”** — 可能是因为尚未生成报告，或者所有报告都已被应用或跳过。Claw Mentor 每天都会运行一次更新——新报告会在导师更新后的 24 小时内出现。

**快照生成失败** — 请确保您的 OpenClaw 代理具有访问 `~/.openclaw/` 文件系统的权限。检查您的环境中是否包含 `cp` 和 `mkdir` 命令。

**报告无法更新** — 请确认您的 API 密钥是否正确，并确保您在 app.clawmentor.ai 处拥有有效的订阅权限。

---

## 源代码

开源项目（可审核）：[github.com/clawmentor/claw-mentor-mentee](https://github.com/clawmentor/claw-mentor-mentee)

如有任何问题或疑问，请在 GitHub 上提交问题或发送电子邮件至 hello@clawmentor.ai。