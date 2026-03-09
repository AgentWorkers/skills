---
name: vexa
description: "将机器人发送到 Zoom、Google Meet 和 Microsoft Teams 会议中，获取实时转录内容、会议记录和报告。该功能支持与 Vexa Cloud 集成，也可与用户自托管的服务器配合使用。"
---
## 以聊天为导向的交互

**直接与用户对话**，就像进行自然聊天一样。不要输出内部推理过程、计划摘要或程序性说明（例如：“我需要...”、“根据该技能...”、“我将通知...”）。只回复你实际会对用户说的话——保持对话式、亲切且简洁。

## 用于会议聊天的纯文本格式

在向会议聊天工具（如 Google Meet、Teams 等）发送消息时，**始终使用纯文本**，不要使用 markdown。这些聊天工具无法渲染 markdown 格式，因此星号、井号标题、反引号和项目符号会显示为难看的原始字符。请使用换行符和空格来组织内容。

可以使用以下 CLI 命令：
- `node skills/vexa/scripts/vexa.mjs ...`
- `node skills/vexa/scripts/onboard.mjs ...`
- `node skills/vexa/scripts/ingest.mjs ...`
- `node skills/vexa/scripts/audit.mjs ...`

## 环境配置

**必需项：** `VEXA_API_KEY` — 请从 https://vexa.ai/dashboard/api-keys 获取您的 API 密钥

将 `VEXA_API_KEY` 设置在您的环境变量中，或者手动创建 `skills/vexa/secrets/vexa.env` 文件，内容如下：
```
VEXA_API_KEY=your_key_here
```

**可选项：** `VEXA_BASE_URL`（环境变量优先级高于端点配置）

### 端点切换（生产环境 / 本地开发环境）

CLI 支持存储在 `secrets/vexa-endpoints.json` 中的命名端点。默认端点为：`prod`（https://api.cloud.vexa.ai）和 `local`（http://localhost:8000）。

- 列出所有端点及当前使用的环境：`node skills/vexa/scripts/vexa.mjs env:list`
- 切换到本地开发环境：`node skills/vexa/scripts/vexa.mjs env:use local`
- 切换到生产环境：`node skills/vexa/scripts/vexa.mjs env:use prod`
- 添加自定义端点：`node skills/vexa/scripts/vexa.mjs env:set staging --url https://staging.vexa.ai`
- 删除端点：`node skills/vexa/scripts/vexa.mjs env:remove staging`

优先级顺序：`VEXA_BASE_URL` 环境变量 > `vexa-endpoints.json` 中指定的端点 > 默认的生产环境 URL。

## 首先检查 secrets（在开始任何初始化操作之前）

**务必先执行以下操作：** `node skills/vexa/scripts/onboard.mjs --check-secrets`

- 如果输出结果为 `{"secrets_ok": true}`，则表示 secrets 存在，可以直接跳过初始化流程，使用常规操作。
- 如果输出结果为 `{"secrets_ok": false}`，则需要执行初始化流程，并加载 `references/onboarding-flow.md`。

**Webhook 设置：** 当 secrets 存在且您正在使用 Vexa 时，运行 `node skills/vexa/scripts/onboard.mjs --check-webhook`。如果 `webhook_configured` 的值为 `false`，建议添加相应的映射配置（详见 `references/webhook-setup.md`）。有关初始化的详细信息（包括 webhook 要求和流程验证），请参考 `references/onboarding-flow.md`。

**如果 secrets 丢失：** 建议用户从 https://vexa.ai/dashboard/api-keys 获取 API 密钥并自行设置。用户应该将 `VEXA_API_KEY` 设置在环境变量中，或者手动创建 `skills/vexa/secrets/vexa.env` 文件（格式为 `VEXA_API_KEY=their_key_here`）。切勿要求用户在聊天中直接输入 API 密钥。

**Secrets 的存储位置：** `skills/vexa/secrets/` 目录用于存放环境配置文件和 `vexa-state.json`。在将技能发布到 ClawHub 时，请确保排除 `secrets/` 目录。

**针对每个端点的 API 密钥：** CLI 支持为每个端点配置单独的环境文件（例如 `vexa-prod.env`、`vexa-local.env` 等）。使用 `env:use` 选项切换端点时，系统会自动加载对应的 `vexa-<name>.env` 文件。如果不存在特定端点的配置文件，则会使用 `vexa.env` 文件。

**非交互式使用（用于脚本执行）：** `onboard.mjs --api_key <key> --persist yes --meeting_url "<url>" --language en --wait_seconds 60 --poll_every_seconds 10`

## 快速工作流程

### 1) 用户提供会议链接 → 发送机器人

- 在成功发送机器人后，**主动运行 `--check-webhook` 命令**。如果尚未配置 webhook，建议用户设置 webhook，以便在会议结束后自动生成报告。
- 解析/规范化会议链接（或提供明确的会议 ID）：
  - `node skills/vexa/scripts/vexa.mjs parse:meeting-url --meeting_url "https://meet.google.com/abc-defg-hij"`
- 直接从链接启动机器人：
  - `node skills/vexa/scripts/vexa.mjs bots:start --meeting_url "https://meet.google.com/abc-defg-hij" --bot_name "Claw" --language en`
  - `node skills/vexa/scripts/vexa.mjs bots:start --meeting_url "https://teams.live.com/meet/9387167464734?p=qxJanYOcdjN4d6UlGa" --bot_name "Claw" --language en`

### 2) 从日历链接启动机器人

如果使用日历工具（例如 Gog），可以执行以下操作：
1. 获取即将召开的会议。
2. 提取会议链接（Google Meet/Teams）。
3. 对于每个选定的会议，调用 `bots:start --meeting_url ...` 命令启动机器人。
4. （可选）将会议标题保存到 Vexa 的元数据中：
   - `meetings:update --name "<calendar title>" --notes "source: calendar"`

### 3) 会议期间或会议结束后读取会议记录

- 获取当前的会议记录：
  - `node skills/vexa/scripts/vexa.mjs transcripts:get --platform google_meet --native_meeting_id abc-defg-hij`
- 对于实时流媒体转录，可以使用 Vexa 的 WebSocket API（详情请参阅 `references/user-api-guide-notes.md`）。
- 在记录准备好后，总结并保存关键信息。

### 4) 停止机器人

- `node skills/vexa/scripts/vexa.mjs bots:stop --meeting_url "<url>"`

### 5) 生成会议报告（会议结束后）

在停止机器人或会议结束后，生成会议报告：
- `node skills/vexa/scripts/vexa.mjs report --meeting_url "https://meet.google.com/abc-defg-hij"`
- 或者 `node skills/vexa/scripts/ingest.mjs --meeting_url "<url>"`

报告内容会被保存到 `memory/meetings/YYYY-MM-DD-<slug>.md` 文件中，包括会议信息、总结内容、关键决策、待办事项和完整记录。

### 6) 获取或更新 Ultravox 语音代理系统的提示语

语音代理系统的提示语决定了 Vexa 机器人在会议中的行为（例如个性、语言以及触发时的行为）。该提示语是针对每个用户单独设置的，并在下次启动机器人时生效。

- 获取当前的提示语（默认为系统默认设置）：
  - `node skills/vexa/scripts/vexa.mjs voice-agent:config:get`
- 设置自定义提示语：
  - `node skills/vexa/scripts/vexa.mjs voice-agent:config:set --prompt "您是 Vexa，一个简洁的会议助手..."`
- 重置为系统默认设置：
  - `node skills/vexa/scripts/vexa.mjs voice-agent:config:reset`

**注意：** 更新后的提示语仅对**下次启动的机器人**生效，不会影响正在会议中的机器人。

## 核心命令

- 查看机器人状态：
  - `node skills/vexa/scripts/vexa.mjs bots:status`
- 启动机器人（指定会议参数）：
  - `node skills/vexa/scripts/vexa.mjs bots:start --platform google_meet --native_meeting_id abc-defg-hij --bot_name "Claw" --language en`
- 更新机器人的语言设置：
  - `node skills/vexa/scripts/vexa.mjs bots:config:update --platform google_meet --native_meeting_id abc-defg-hij --language es`
- 列出所有会议：
  - `node skills/vexa/scripts/vexa.mjs meetings:list`
- 更新会议元数据（标题、参与者、语言、备注）：
  - `node skills/vexa/scripts/vexa.mjs meetings:update --platform google_meet --native_meeting_id abc-defg-hij --name "Weekly Product Sync" --participants "Alice,Bob" --languages "en" --notes "Action items captured"`
- 生成分享链接：
  - `node skills/vexa/scripts/vexa.mjs transcripts:share --platform google_meet --native_meeting_id abc-defg-hij --ttl_seconds 3600`
- 设置 Vexa 用户的 webhook 配置：
  - `node skills/vexa/scripts/vexa.mjs user:webhook:set --webhook_url https://your-public-url/hooks/vexa`

## 录音文件管理

- 列出所有录音文件：
  - `node skills/vexa/scripts/vexa.mjs recordings:list [--limit 50] [--offset 0] [--meeting_id <db_id>]`
- 获取单个录音文件：
  - `node skills/vexa/scripts/vexa.mjs recordings:get <recording_id>`
- 删除录音文件：
  - `node skills/vexa/scripts/vexa.mjs recordings:delete <recording_id> --confirm DELETE`
- 获取媒体文件的下载链接：
  - `node skills/vexa/scripts/vexa.mjs recordings:download <recording_id> <media_file_id>`
- 查看录音文件配置：
  - `node skills/vexa/scripts/vexa.mjs recordings:config:get`
- 更新录音文件配置：
  - `node skills/vexa/scripts/vexa.mjs recordings:config:update --enabled true --capturemodes audio,video`

## 会议信息汇总（会议结束后）

通过一次调用即可获取会议的所有相关信息（包括记录、录音文件和分享链接）：
- `node skills/vexa/scripts/vexa.mjs meetings:bundle --meeting_url "https://meet.google.com/abc-defg-hij"`
- `node skills/vexa/scripts/vexa.mjs meetings:bundle --platform zoom --native_meeting_id 1234567890`

**可选参数：**
- `--segments` — 包含会议记录的片段（默认不包含以减少输出大小）
- `--no-share` — 不生成分享链接
- `--no-recordings` — 不处理录音文件的元数据
- `--download-urls` — 获取每个录音文件的下载链接
- `--ttl_seconds 3600` — 设置分享链接的有效时间（TTL）

## Webhook（会议结束后触发报告）

可选功能：Vexa 可以通过发送 “会议结束” 的 webhook 来自动生成报告。用户需要手动配置他们的 `openclaw.json` 文件（详情请参阅 `references/webhook-setup.md`）。该技能不会自动修改用户的 `openclaw.json` 文件。希望使用此功能的用户需要自行在配置文件中添加 `hookstransformsDir` 和相应的映射配置。

## OpenClaw 数据导入辅助工具

- 生成会议报告（包含会议信息、记录和摘要/决策/待办事项的占位符）：
  - `node skills/vexa/scripts/vexa.mjs report --meeting_url "<url>"`
  - `node skills/vexa/scripts/ingest.mjs --meeting_url "<url>"`（或 `--platform` + `--native_meeting_id`)
- 审查会议记录，找出可能的测试通话或需要清理的会议：
  - `node skills/vexa/scripts/audit.mjs`

## 平台支持

- 支持的平台：`google_meet`、`teams`、`zoom`
- Teams 的 `native_meeting_id` 必须是数字 ID。
- 使用 Teams 机器人需要输入密码（来自会议链接中的 `?p=` 参数）。
- Zoom 的 `native_meeting_id` 是 10 到 11 位的数字 ID，密码（`?pwd=`）是可选的。

## 删除操作的安全性（严格限制）

`DELETE /meetings/{platform}/{native_meeting_id}` 命令会删除会议记录并对数据进行匿名处理。

**规则：**
1. 未经用户明确请求，切勿删除任何会议记录。
2. 首先验证 `platform` 和 `native_meeting_id` 的准确性。
3. 尽可能使用非破坏性的数据清理方式（例如 `meetings:update`）。
4. 使用以下命令时需要输入确认信息：
   - `node skills/vexa/scripts/vexa.mjs meetings:delete --platform google_meet --native_meeting_id abc-defg-hij --confirm DELETE`