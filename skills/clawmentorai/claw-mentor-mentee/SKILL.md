---
name: claw-mentor-mentee
description: 安全的 OpenClaw 进化：从专业开发者那里获取经过安全审查的兼容性报告，并直接发送到您的代理程序。您可以选择应用这些更新，或者选择跳过它们；系统还提供了自动回滚保护功能。
metadata: {"openclaw": {"emoji": "🔥", "primaryEnv": "CLAW_MENTOR_API_KEY", "homepage": "https://clawmentor.ai"}}
---
# Claw Mentor — 学员技能

> 直接将导师的更新信息同步到您的 OpenClaw 代理中。当新的兼容性报告准备好时，系统会通过 OpenClaw 聊天功能通知您，您可以查看报告内容并决定是否应用这些更新——所有操作均可在 OpenClaw 聊天界面完成。

---

## 描述

Claw Mentor 是一个专为 OpenClaw 用户设计的导师辅导平台。您可以订阅一位经验丰富的导师（例如 Ember 🔥），他们维护着一套精心配置的 OpenClaw 环境。每当导师更新配置时，系统会生成一份用简单易懂的英语编写的报告，说明具体变更内容、变更的作用以及这些变更是否适用于您的环境。

该技能将您的本地 OpenClaw 代理与 Claw Mentor 平台连接起来。代理会定期检查新的报告，通知您，并协助您决定是否应用这些变更；在应用变更之前，系统还会自动为您创建本地备份。

**隐私声明：** 您的 AGENTS.md 文件、技能配置文件以及配置数据绝不会被发送给 Claw Mentor。服务器仅接收您自愿提供的入职调查问卷信息以及您关于是否应用变更的决策（应用/跳过/回滚）。您的任何配置数据都不会离开您的设备。

---

## 功能概述

- 每隔几小时自动检查 `app.clawmentor.ai` 以获取导师发布的新的兼容性报告
- 当有新报告时，通过您配置的渠道（如 Telegram）通知您
- 以简洁的文字形式展示报告内容：包括变更内容、风险等级以及后续操作建议
- 指导您如何应用或跳过这些变更
- 在应用任何变更之前，系统会自动创建本地备份
- 将您的决策（应用/跳过/回滚）反馈给 Claw Mentor，但不会共享任何配置信息

---

## 安装过程

```bash
clawhub install claw-mentor-mentee
```

安装完成后，请启动一个新的 OpenClaw 会话。首次使用时，代理会指导您完成 API 密钥的设置。

API 密钥的获取地址：**app.clawmentor.ai → 设置 → 学员技能**

---

## 首次使用时的配置步骤

**在首次使用该技能时，请检查环境变量 `CLAW_MENTOR_API_KEY` 是否已设置。**

**如果已设置：** 系统已连接成功。立即通过调用 `GET https://app.clawmentor.ai/api/mentee/reports` 来查看待处理的报告。同时确保您的工作空间中的 `HEARTBEAT.md` 文件包含以下内容：`- Check for new Claw Mentor reports`（如果该行不存在，请添加它，以便系统能够定期检查报告）。**

**如果未设置：** 请告知用户：
> “要激活 ClawMentor 功能，您需要提供 API 密钥。
> 
> 👉 请前往 **app.clawmentor.ai → 设置 → 学员技能 → 生成 API 密钥** 获取 API 密钥。”
> 
> 获取密钥后，请将其分享给系统，系统会为您完成配置。”

**用户提供 API 密钥后：**
1. 将密钥存储在：`openclaw config set 'skills.entries["claw-mentor-mentee"].apiKey' YOUR_KEY`
2. 系统确认连接成功，并告知用户：“✅ ClawMentor 已连接成功。系统将每 `CLAW_MENTOR_CHECK_INTERVAL_HOURS` 小时检查一次新报告（默认值为 6 小时）。”
3. 立即查看待处理的报告：调用 `GET https://app.clawmentor.ai/api/mentee/reports` 并告知用户相关情况。
4. **安排定期检查**：在您的工作空间中的 `HEARTBEAT.md` 文件中添加以下内容（如果文件不存在，请创建该文件）：
   ```
   - Check for new Claw Mentor reports
   ```
   这条指令会告诉 OpenClaw 代理在每个心跳周期内自动检查新报告。

---

## 配置参数

| 参数 | 来源 | 默认值 |
|---|---|---|
| `CLAW_MENTOR_API_KEY` | app.clawmentor.ai → 设置 → 学员技能 | 必填 |
| `CLAW_MENTOR_CHECK_INTERVAL_HOURS` | 可选参数（在 OpenClaw 环境中设置） | `6` 小时 |

OpenClaw 会将您的 API 密钥存储在 `~/.openclaw/openclaw.json` 文件的 `skills.entries["claw-mentor-mentee"].apiKey` 中，并在每次会话中自动将其设置为 `CLAW_MENTOR_API_KEY`。

---

## 权限要求

| 权限 | 说明 |
|---|---|
| `READ: ~/.openclaw/` | 用于在应用变更前创建本地备份 |
| `WRITE: ~/.openclaw/claw-mentor/snapshots/` | 用于存储备份文件 |
| `WRITE: ~/.openclaw/claw-mentor/state.json` | 用于记录上次检查时间和已通知的报告 |
| `NETWORK: app.clawmentor.ai` | 用于获取报告和发送状态更新 |
| `NOTIFY: configured channel` | 用于在有新报告时发送通知 |
| `EXEC: cp, mkdir` | 用于执行创建备份所需的 shell 命令 |

系统不会读取其他文件，也不会上传任何配置数据。

---

## 代理操作指南

安装此技能后，您的 OpenClaw 代理应遵循以下操作规则：

### 定期检查报告（每 `CLAW_MENTOR_CHECK_INTERVAL_HOURS` 小时）

1. 读取 `~/.openclaw/claw-mentor/state.json` 文件，获取 `last_check` 和 `notified_report_ids`（如果文件不存在则创建）
2. 如果距离上次检查的时间小于 `CLAW_MENTOR_CHECK_INTERVAL_HOURS` 小时，则跳过检查，返回 `HEARTBEAT_OK`
3. 使用 `Authorization: Bearer {CLAW_MENTOR_API_KEY}` 的请求头调用 `GET https://app.clawmentor.ai/api/mentee/reports`
4. 更新 `state.json` 文件，将 `last_check` 设置为当前时间
5. 对于响应中 `status` 为 `pending` 且 `id` 不在 `notified_report_ids` 中的每个报告：
   - 发送通知消息（格式见下方）
   - 将报告 ID 添加到 `notified_report_ids` 列表中
6. 如果没有待处理的报告，则返回 `HEARTBEAT_OK`

**通知消息格式：**
```
🔥 New mentor update ready!

**{mentor_name}** · {risk_emoji} {risk_level_display} risk

{plain_english_summary}

Say **"show my mentor report"** to see the full details.
Or: **"apply mentor report"** / **"skip mentor report"**
```

风险等级 emoji：LOW → 🟢, MEDIUM → 🟡, HIGH → 🔴

### 命令说明：

- `show my mentor report` / `my mentor reports` / `check my reports`：  
  调用 `GET https://app.clawmentor.ai/api/mentee/reports`  
  如果没有待处理的报告：显示 “没有新的导师报告。您的数据是最新的！✅”
  如果有待处理的报告：显示所有待处理的报告内容

### 命令说明：

- `apply mentor report` / `apply [mentor name]'s update`：  
  这是最重要的命令。请仔细按照以下步骤操作：
  1. 调用 `GET https://app.clawmentor.ai/api/mentee/reports` 获取最新的待处理报告  
  2. 如果没有待处理的报告：显示 “没有需要应用的变更。”  
  3. 显示报告中的所有变更内容  
  4. 在应用任何变更之前，先创建本地备份：  
    ```bash
   SNAPSHOT_DATE=$(date +%Y-%m-%d-%H-%M)
   SNAPSHOT_PATH="$HOME/.openclaw/claw-mentor/snapshots/$SNAPSHOT_DATE/"
   mkdir -p "$SNAPSHOT_PATH"
   cp -r "$HOME/.openclaw/" "$SNAPSHOT_PATH"
   ```  
  5. 确认备份已保存：显示 “✅ 备份已保存至 `~/.openclaw/claw-mentor/snapshots/{date}/`”  
  6. 逐一指导用户应用每个变更（在用户的技能配置目录中进行手动操作）  
  7. 用户确认应用完成后，调用 `POST https://app.clawmentor.ai/api/mentee/status`  
    ```json
   { "reportId": "{id}", "status": "applied", "snapshotPath": "{SNAPSHOT_PATH}" }
   ```  
  8. 确认操作完成：显示 “✅ 变更已应用！您的使用记录已在 Claw Mentor 平台上更新。”

- `skip mentor report` / `skip [mentor]'s update`：  
  1. 获取最新的待处理报告（使用相同的 API 调用）  
  2. 如果没有待处理的报告：显示 “无需应用任何变更。”  
  3. 调用 `POST https://app.clawmentor.ai/api/mentee/status`，传入 `{"reportId": "{id}", "status": "skipped"}`  
  4. 确认操作完成：显示 “已跳过该变更。您随时可以在 app.clawmentor.ai/dashboard 查看报告详情。”

- `roll back [mentor]'s update` / `undo mentor changes`：  
  1. 查找上次 API 调用中记录的最新应用报告（或询问用户具体是哪个报告）  
  2. 确认是否已创建备份（检查 `~/.openclaw/claw-mentor/snapshots/` 文件）  
  3. 显示恢复操作的命令：  
    ```bash
   cp -r ~/.openclaw/claw-mentor/snapshots/{most-recent-date}/ ~/.openclaw/
   ```  
  4. 提醒用户：“恢复操作完成后，请重启 OpenClaw 代理以使变更生效。”  
  5. 用户确认恢复完成后，调用 `POST https://app.clawmentor.ai/api/mentee/status`，传入 `{"reportId": "{id}", "status": "rolled_back"}`  

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

如果文件不存在，请在首次使用时创建该文件。

---

## API 参考

所有 API 端点地址：`https://app.clawmentor.ai`

### GET /api/mentee/reports  
**认证方式：** `Authorization: Bearer {CLAW_MENTOR_API_KEY}`  
**返回内容：**  
```json
{
  "user": { "id": "...", "email": "...", "tier": "starter" },
  "reports": [
    {
      "id": "uuid",
      "created_at": "2026-03-01T10:00:00Z",
      "risk_level": "low",
      "plain_english_summary": "...",
      "skills_to_add": [{ "name": "...", "what_it_does": "...", "permissions_it_needs": [] }],
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

### POST /api/mentee/status  
**认证方式：** `Authorization: Bearer {CLAW_MENTOR_API_KEY}`  
**请求体：** `{ "reportId": "uuid", "status": "applied|skipped|rolled_back", "snapshotPath": "~/.openclaw/..." }`  
**返回内容：** `{ "success": true, "reportId": "...", "status": "applied", "updated_at": "..." }`

---

## 常见问题及解决方法

- **`clawhub install` 被限制**：ClawHub 会对每个 IP 的下载次数进行限制。请等待 2–3 分钟后重试。如果安装过程中出现错误，可以运行 `clawhub install claw-mentor-mentee --force` 来覆盖旧文件。
- **“API 密钥无效”**：请前往 app.clawmentor.ai → 设置 → 学员技能 重新生成 API 密钥。
- **“未找到报告”**：可能是尚未生成报告，或者所有报告都已被应用或跳过。Claw Mentor 每天会自动检查报告——新报告通常会在导师更新后的 24 小时内生成。
- **备份创建失败**：请确保您的 OpenClaw 代理具有对 `~/.openclaw/` 目录的读写权限，并确认环境中包含 `cp` 和 `mkdir` 命令。
- **报告更新失败**：请检查 API 密钥是否正确，并确认您在 app.clawmentor.ai 上拥有有效的订阅权限。

---

## 项目来源

该项目为开源代码：[github.com/clawmentor/claw-mentor-mentee](https://github.com/clawmentor/claw-mentor-mentee)

如有任何问题或需要帮助，请在 GitHub 上提交 issue，或发送邮件至 hello@clawmentor.ai。