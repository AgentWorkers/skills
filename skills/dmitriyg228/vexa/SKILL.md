---
name: vexa
description: "将 Vexa 机器人发送到会议中，并端到端地操作会议记录工作流程（包括会议期间和会议结束后）：解析会议链接、请求/停止机器人的参与、读取实时/最终的会议记录、生成基本的会议报告、设置 Webhook 通知机制以及丰富会议元数据。当用户提供 Google Meet/Teams 的会议链接、请求从日历事件中自动加入会议，或需要从 Vexa 获取会议记录、进行会议内容总结或更新知识库时，可使用该功能。会议结束后，会生成一份包含会议信息、会议记录以及总结/决策/行动事项占位符的报告。请注意：删除会议记录（即清除相关数据）属于破坏性操作，因此需要用户的明确确认。"
---

## 以聊天为导向的交互方式

**直接与用户对话**，就像在自然聊天中一样。不要输出内部推理过程、计划摘要或程序性说明（例如：“我需要...”、“根据该技能...”、“我会通知...”）。只回复你实际会对用户说的话——保持对话的亲切感和简洁性。

使用提供的 CLI 命令：
- `node skills/vexa/scripts/vexa.mjs ...`
- `node skills/vexa/scripts/onboard.mjs ...`
- `node skills/vexa/scripts/ingest.mjs ...`
- `node skills/vexa/scripts/audit.mjs ...`

## 环境配置

针对 OpenClaw 进程（或 shell）的配置参数：
- `VEXA_API_KEY`（必需）
- `VEXA_BASE_URL`（可选，默认为 `https://api.cloud.vexa.ai`）

## 首先检查密钥（在任何入职流程之前）

**务必先执行以下操作：** `node skills/vexa/scripts/onboard.mjs --check-secrets`

- 如果输出结果为 `{"secrets_ok": true}`，则表示密钥存在，可以直接跳过入职流程，按常规流程操作。
- 如果输出结果为 `{"secrets_ok": false}`，则需要执行入职流程，并加载 `references/onboarding-flow.md` 文件。

**Webhook 的主动设置：** 当密钥存在且正在使用 Vexa 时，运行 `node skills/vexa/scripts/onboard.mjs --check-webhook`。如果 `webhook_configured` 的值为 `false`，建议添加相应的 webhook 配置（详见 `references/webhook-setup.md`）。有关入职流程的详细信息（包括 webhook 要求、流程验证和模拟 webhook 的使用方法），请参考 `references/onboarding-flow.md`。

**当密钥缺失时：** 要求用户从 [https://vexa.ai/dashboard/api-keys](https://vexa.ai/dashboard/api-keys) 获取密钥，并将其粘贴到聊天中；你也可以将密钥的路径和格式提供给他们，以便他们手动添加（这样更安全，尤其是用户不愿意直接粘贴密钥的情况下）。

**密钥存储位置：** `skills/vexa/secrets/` 目录下存放 `vexa.env`（API 密钥）和 `vexa-state.json` 文件。在将技能发布到 ClawHub 时，请确保排除 `secrets/` 目录。

**非交互式使用（用于脚本执行）：** `onboard.mjs --api_key <key> --persist yes --meeting_url "<url>" --language en --wait_seconds 60 --poll_every_seconds 10`

## 快速工作流程

### 1) 用户提供会议链接 → 发送机器人

- 在成功发送机器人后，**主动** 运行 `--check-webhook` 命令。如果尚未配置 webhook，建议用户设置 webhook 以自动触发会议报告的生成。
- 解析/规范化会议链接（或提供明确的会议 ID）：
  - `node skills/vexa/scripts/vexa.mjs parse:meeting-url --meeting_url "https://meet.google.com/abc-defg-hij"`
- 直接从链接启动机器人：
  - `node skills/vexa/scripts/vexa.mjs bots:start --meeting_url "https://meet.google.com/abc-defg-hij" --bot_name "Claw" --language en`
  - `node skills/vexa/scripts/vexa.mjs bots:start --meeting_url "https://teams.live.com/meet/9387167464734?p=qxJanYOcdjN4d6UlGa" --bot_name "Claw" --language en`

### 2) 从日历会议链接启动机器人

如果使用日历工具（例如 Google Meet），可以执行以下操作：
1. 获取即将进行的会议信息。
2. 提取会议链接（Google Meet 或 Teams）。
3. 对于每个选定的会议，调用 `bots:start --meeting_url ...` 命令启动机器人。
4. （可选）将会议标题保存到 Vexa 的元数据中：
   - `meetings:update --name "<calendar title>" --notes "source: calendar"`

### 3) 会议期间或会议结束后读取会议记录

- 获取当前的会议记录：
  - `node skills/vexa/scripts/vexa.mjs transcripts:get --platform google_meet --native_meeting_id abc-defg-hij`
- 对于实时流媒体，可以使用 Vexa 的 WebSocket API（详细信息请参阅 `references/user-api-guide-notes.md`）。
- 会议记录准备好后，总结并存储关键内容。

### 4) 停止机器人

- `node skills/vexa/scripts/vexa.mjs bots:stop --meeting_url "<url>"`

### 5) 生成会议报告（会议结束后）

在停止机器人或会议结束后，生成一份基本的会议报告：
- `node skills/vexa/scripts/vexa.mjs report --meeting_url "https://meet.google.com/abc-defg-hij"`
- 或 `node skills/vexa/scripts/ingest.mjs --meeting_url "<url>"`

报告内容会保存到 `memory/meetings/YYYY-MM-DD-<slug>.md` 文件中，包括会议信息、总结要点、关键决策、行动事项以及完整的会议记录。

## 核心命令

- 查看机器人状态：
  - `node skills/vexa/scripts/vexa.mjs bots:status`
- 启动机器人（指定参数）：
  - `node skills/vexa/scripts/vexa.mjs bots:start --platform google_meet --native_meeting_id abc-defg-hij --bot_name "Claw" --language en`
- 更新机器人的语言设置：
  - `node skills/vexa/scripts/vexa.mjs bots:config:update --platform google_meet --native_meeting_id abc-defg-hij --language es`
- 列出所有会议：
  - `node skills/vexa/scripts/vexa.mjs meetings:list`
- 更新会议元数据（标题、参与者、语言、备注）：
  - `node skills/vexa/scripts/vexa.mjs meetings:update --platform google_meet --native_meeting_id abc-defg-hij --name "Weekly Product Sync" --participants "Alice,Bob" --languages "en" --notes "Action items captured"`
- 生成分享链接：
  - `node skills/vexa/scripts/vexa.mjs transcripts:share --platform google_meet --native_meeting_id abc-defg-hij --ttl_seconds 3600`
- 设置 Vexa 用户的 webhook 地址：
  - `node skills/vexa/scripts/vexa.mjs user:webhook:set --webhook_url https://your-public-url/hooks/vexa`

## Webhook（会议结束 → 生成报告）

当 Vexa 发送 “会议结束” 的 webhook 信号时，`scripts/vexa-transform.mjs` 脚本会指示代理生成报告。有关 webhook 配置的详细信息，请参阅 `references/webhook-setup.md`。需要设置 `hookstransformsDir` 为工作区的根目录，并指定 `transform.module` 为 `skills/vexa/scripts/vexa-transform.mjs`。

## OpenClaw 数据导入辅助工具

- 生成基本的会议报告（包含会议信息、会议记录以及总结/决策/行动事项的占位符）：
  - `node skills/vexa/scripts/vexa.mjs report --meeting_url "<url>"`
  - `node skills/vexa/scripts/ingest.mjs --meeting_url "<url>"`（或 `--platform` + `--native_meeting_id`）
- 审查会议记录，找出可能的测试调用或需要清理的会议：
  - `node skills/vexa/scripts/audit.mjs`

## 平台支持

- 支持的平台：`google_meet`、`teams`
- Teams 平台的 `native_meeting_id` 必须是数字格式的 ID。
- 在 Teams 中使用机器人需要输入密码（通过 URL 中的 `?p=` 参数获取）。

## 删除操作的安全性（严格限制）

`DELETE /meetings/{platform}/{native_meeting_id}` 命令会删除会议记录并匿名化数据。

**规则：**
1. 未经用户明确请求，严禁删除任何会议记录。
2. 必须先验证 `platform` 和 `native_meeting_id` 的准确性。
3. 尽可能使用非破坏性的数据清理方式（例如 `meetings:update` 命令）。
4. 使用保护性机制：
   - `node skills/vexa/scripts/vexa.mjs meetings:delete --platform google_meet --native_meeting_id abc-defg-hij --confirm DELETE`