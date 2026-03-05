---
name: vexa
description: "将机器人发送到 Zoom、Google Meet 和 Microsoft Teams 会议中，获取实时转录内容、会议记录和报告。支持自托管或云部署，无需使用任何外部 API。"
---
## 以聊天为导向的交互方式

**直接与用户交流**，就像进行自然对话一样。不要输出内部推理过程、计划摘要或程序性说明（例如：“我需要...”、“根据该技能...”、“我会通知...”）。只回复你实际会对用户说的话——要亲切、自然且简洁明了。

## 用于会议聊天的纯文本格式

在向会议聊天工具（如 Google Meet、Teams 等）发送消息时，**必须使用纯文本**，不要使用 Markdown 格式。这些聊天工具无法解析 Markdown，因此星号、井号标题、反引号和项目符号会显示为难看的原始字符。请使用换行符和空格来组织内容。

可以使用以下命令行工具（CLI）：
- `node skills/vexa/scripts/vexa.mjs ...`
- `node skills/vexa/scripts/onboard.mjs ...`
- `node skills/vexa/scripts/ingest.mjs ...`
- `node skills/vexa/scripts/audit.mjs ...`

## 环境配置

为 OpenClaw 进程（或 shell）设置以下环境变量：
- `VEXA_API_KEY`（必填）
- `VEXA_BASE_URL`（可选的环境变量，优先于端点配置）

### 端点切换（生产环境 / 本地开发环境）

CLI 支持存储在 `secrets/vexa-endpoints.json` 文件中的命名端点。默认端点为：`prod`（https://api.cloud.vexa.ai）和 `local`（http://localhost:8000）。
- 列出所有端点及当前使用的环境：`node skills/vexa/scripts/vexa.mjs env:list`
- 切换到本地开发环境：`node skills/vexa/scripts/vexa.mjs env:use local`
- 切换到生产环境：`node skills/vexa/scripts/vexa.mjs env:use prod`
- 添加自定义端点：`node skills/vexa/scripts/vexa.mjs env:set staging --url https://staging.vexa.ai`
- 删除端点：`node skills/vexa/scripts/vexa.mjs env:remove staging`

优先级顺序：`VEXA_BASE_URL` 环境变量 > `vexa-endpoints.json` 中指定的端点 > 默认的生产环境 URL。

## 首先检查 secrets 文件（在开始任何初始化操作之前）

**务必先执行**：`node skills/vexa/scripts/onboard.mjs --check-secrets`
- 如果输出结果为 `{"secrets_ok": true}`，则表示 secrets 文件存在，可以直接跳过初始化流程，使用常规操作。
- 如果输出结果为 `{"secrets_ok": false}`，则需要执行初始化流程，并加载 `references/onboarding-flow.md` 文件。

**Webhook 的主动设置**：每当 secrets 文件存在且正在使用 Vexa 时，运行 `node skills/vexa/scripts/onboard.mjs --check-webhook`。如果 `webhook_configured` 的值为 `false`，建议添加相应的 webhook 配置（详见 `references/webhook-setup.md`）。有关初始化过程中的具体要求（如 webhook 配置、流程验证和模拟 webhook 功能），请参考 `references/onboarding-flow.md`。

**如果 secrets 文件缺失**：请用户从 https://vexa.ai/dashboard/api-keys 获取 API 密钥，并将其粘贴到聊天中；你也可以将获取到的路径和格式信息提供给用户，以便他们手动添加到 `skills/vexa/secrets/vexa.env` 文件中（这样更安全）。

**Secrets 文件的位置**：`skills/vexa/secrets/` 目录用于存储环境配置文件和 `vexa-state.json`。在将技能发布到 ClawHub 时，请确保此目录被排除在版本控制范围之外。

**针对每个端点的 API 密钥**：CLI 支持为每个端点创建单独的环境配置文件（例如 `vexa-prod.env`、`vexa-local.env` 等）。使用 `env:use` 选项切换端点时，系统会自动加载对应的环境文件；如果没有特定端点的配置文件，则会使用 `vexa.env` 文件。

**非交互式使用（用于脚本执行）**：`onboard.mjs --api_key <key> --persist yes --meeting_url "<url>" --language en --wait_seconds 60 --poll_every_seconds 10`

## 快速工作流程

### 1) 用户提供会议链接 → 发送机器人

- 在成功发送机器人后，**主动运行 `--check-webhook` 命令**。如果尚未配置 webhook，建议用户设置该功能，以便自动生成会议报告。
- 解析并规范化会议链接（或提供会议 ID）：
  - `node skills/vexa/scripts/vexa.mjs parse:meeting-url --meeting_url "https://meet.google.com/abc-defg-hij"`
- 直接从链接启动机器人：
  - `node skills/vexa/scripts/vexa.mjs bots:start --meeting_url "https://meet.google.com/abc-defg-hij" --bot_name "Claw" --language en`
  - `node skills/vexa/scripts/vexa.mjs bots:start --meeting_url "https://teams.live.com/meet/9387167464734?p=qxJanYOcdjN4d6UlGa" --bot_name "Claw" --language en`

### 2) 从日历链接启动机器人

如果使用日历工具（例如 gog），可以执行以下操作：
1. 获取即将举行的会议信息。
2. 提取会议链接（Google Meet/Teams）。
3. 对于每个选定的会议，调用 `bots:start --meeting_url ...` 命令启动机器人。
4. （可选）将会议标题保存到 Vexa 的元数据中：
   - `meetings:update --name "<calendar title>" --notes "source: calendar"`

### 3) 会议期间或会议结束后读取会议记录

- 获取当前的会议记录：
  - `node skills/vexa/scripts/vexa.mjs transcripts:get --platform google_meet --native_meeting_id abc-defg-hij`
- 对于实时流媒体，可以使用 Vexa 的 WebSocket API（详情请参阅 `references/user-api-guide-notes.md`）。
- 在记录准备好后，总结并保存关键信息。

### 4) 停止机器人

- `node skills/vexa/scripts/vexa.mjs bots:stop --meeting_url "<url>"`

### 5) 生成会议报告（会议结束后）

在停止机器人或会议结束后，生成一份基本的会议报告：
- `node skills/vexa/scripts/vexa.mjs report --meeting_url "https://meet.google.com/abc-defg-hij"`
- 或 `node skills/vexa/scripts/ingest.mjs --meeting_url "<url>"`

报告内容会保存到 `memory/meetings/YYYY-MM-DD-<slug>.md` 文件中，包括会议信息、总结内容、关键决策、待办事项和完整会议记录。

### 6) 获取或更新 Ultravox 语音代理系统的提示语

语音代理系统的提示语决定了 Vexa 机器人在会议中的行为（例如语气、语言以及触发时的功能）。该提示语是针对每个用户单独设置的，并在下次启动机器人时生效。

- 获取当前的提示语（默认值为服务提供的默认值）：
  - `node skills/vexa/scripts/vexa.mjs voice-agent:config:get`
- 设置自定义提示语：
  - `node skills/vexa/scripts/vexa.mjs voice-agent:config:set --prompt "您是 Vexa，一个简洁的会议助手..."`
- 重置为服务提供的默认提示语：
  - `node skills/vexa/scripts/vexa.mjs voice-agent:config:reset`

**注意**：更新后的提示语仅对**下次启动的机器人**生效，不会影响已经在会议中运行的机器人。

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

## 录音管理

- 列出所有会议录音：
  - `node skills/vexa/scripts/vexa.mjs recordings:list [--limit 50] [--offset 0] [--meeting_id <db_id>]`
- 获取单个录音文件：
  - `node skills/vexa/scripts/vexa.mjs recordings:get <recording_id>`
- 删除录音文件：
  - `node skills/vexa/scripts/vexa.mjs recordings:delete <recording_id> --confirm DELETE`
- 获取媒体文件的下载链接：
  - `node skills/vexa/scripts/vexa.mjs recordings:download <recording_id> <media_file_id>`
- 获取录音文件的配置信息：
  - `node skills/vexa/scripts/vexa.mjs recordings:config:get`
- 更新录音配置：
  - `node skills/vexa/scripts/vexa.mjs recordings:config:update --enabled true --capturemodes audio,video`

## 会议数据打包（会议结束后）

一次性获取会议的所有相关信息（包括会议记录、录音文件和分享链接）：
- `node skills/vexa/scripts/vexa.mjs meetings:bundle --meeting_url "https://meet.google.com/abc-defg-hij"`
- `node skills/vexa/scripts/vexa.mjs meetings:bundle --platform zoom --native_meeting_id 1234567890`

可选参数：
- `--segments`：包含会议记录的片段（默认不包含，以减少输出大小）
- `--no-share`：跳过生成分享链接
- `--no-recordings`：跳过记录的元数据
- `--download-urls`：获取每个录音文件的下载链接
- `--ttl_seconds 3600`：设置分享链接的有效时间（TTL）

## Webhook（会议结束 → 生成报告）

当 Vexa 发送 “会议结束” 的 webhook 信号时，`scripts/vexa-transform.mjs` 脚本会指示代理生成会议报告。有关 webhook 配置的详细信息，请参阅 `references/webhook-setup.md`。需要设置 `hookstransformsDir` 为工作区的根目录，并指定 `transform.module` 为 `skills/vexa/scripts/vexa-transform.mjs`。

## OpenClaw 数据导入辅助工具

- 生成基本的会议报告（包含会议信息、会议记录以及总结/决策/待办事项的占位符）：
  - `node skills/vexa/scripts/vexa.mjs report --meeting_url "<url>"`
  - `node skills/vexa/scripts/ingest.mjs --meeting_url "<url>"`（或 `--platform` + `--native_meeting_id`)
- 审查会议记录，找出可能的测试调用或需要清理的会议：
  - `node skills/vexa/scripts/audit.mjs`

## 平台支持

- 支持的平台包括：`google_meet`、`teams`、`zoom`
- Teams 平台的 `native_meeting_id` 必须是数字 ID。
- 使用 Teams 机器人时需要输入密码（来自会议 URL 的 `?p=` 参数）。
- Zoom 平台的 `native_meeting_id` 是 10-11 位的数字 ID；密码（`?pwd=`）是可选的。

## 删除操作的安全性

`DELETE /meetings/{platform}/{native_meeting_id}` 命令用于删除会议记录并对数据进行匿名处理。

**规则**：
1. 未经用户明确请求，切勿删除任何会议记录。
2. 必须先验证 `platform` 和 `native_meeting_id` 的值。
- 尽可能使用非破坏性的数据清理方式（例如 `meetings:update`）。
- 使用以下命令时需要输入确认信息：
  - `node skills/vexa/scripts/vexa.mjs meetings:delete --platform google_meet --native_meeting_id abc-defg-hij --confirm DELETE`