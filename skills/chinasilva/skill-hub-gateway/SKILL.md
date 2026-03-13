---
name: skill-hub-gateway
description: 统一网关技能，支持异步执行/轮询、门户用户管理以及遥测反馈工作流程。
version: 2.4.2
metadata:
  openclaw:
    skillKey: skill-hub-gateway
    emoji: "🧩"
    homepage: https://gateway.binaryworks.app
    requires:
      bins:
        - node
---
# 技能中心网关（Skill Hub Gateway）

**默认 API 基础 URL：** `https://gateway-api.binaryworks.app`  
**默认站点基础 URL（用于上传路由）：** `https://gateway.binaryworks.app`  
**中文文档：** `SKILL.zh-CN.md`  

## 版本检查协议（Version Check Protocol）  

- **官方最新版本来源：** `GET /skills/manifest.json` → `data.version`  
- **本地当前版本来源：** 安装的 `SKILL.md` 文件中的 `version` 字段  
- **版本比较方式：** 使用语义版本号格式（`major.minor.patch`）  
- **检查频率：** 会话开始时检查一次，同一会话内最多每 24 小时检查一次  
- **如果版本检查失败（网络问题/超时/解析错误）：** 不阻塞运行时执行，继续当前工作流程，并在下一个允许的检查窗口重新尝试。  

## 代理决策流程（Agent Decision Flow）  

- 如果 `latest_version > current_version`，则读取本文档中“发布说明”（Release Notes）对应的部分内容来生成 `update_summary`。  
- 代理应向用户显示：  
  - `current_version`  
  - `latest_version`  
  - `update_summary`  
- **用户选项：**  
  - **立即更新（Update now）**  
  - **稍后在此会话中提醒我（Remind me later in this session）**  
- **如果用户选择“稍后在此会话中提醒我”：** 在新会话开始前，不再重复提示同一目标版本的更新操作。  

## 首次使用指南（First-Time Onboarding，install_code）  

脚本默认自动完成入职流程：  
1. 发送 `POST /agent/install-code/issue` 请求，参数包含 `{"channel":"local"}` 或 `{"channel":"clawhub"}`。  
2. 读取 `data.install_code`。  
3. 发送 `POST /agent/bootstrap` 请求，参数包含 `{"agent_uid":"<agent_uid>","install_code":"<install_code>"}`。  
4. 读取 `data.api_key`，然后使用 `X-API-Key` 或 `Authorization: Bearer <api_key>` 调用运行时 API。  

**手动覆盖方式：**  
- 你仍然可以显式提供 `api_key`。  
- 如果省略了 `agent_uid` 和 `owner_uid_hint`，脚本会从当前工作区路径中获取默认值。  

## 旧版运行时契约（Legacy Runtime Contract，兼容性）  

- **执行命令：** `POST /skill/execute`  
- **查询状态：** `GET /skill/runs/:run_id`  

## 门户操作（Portal Actions，用户操作流程）  

**操作目录（每个操作对应单一默认路径）：**  
- `portal.me` → `GET /user/me`  
- `portal.balance` → `GET /user/points/balance`  
- `portal.ledger.query` → `GET /user/points/ledger`  
- `portal_usage.query` → `GET /user/usage`  
- `portal.skill.execute` → `POST /user/skills/execute`  
- `portal.skill.poll` → `GET /user/skills/runs/:runId`  
- `portal.skill.presentation` → `GET /user/skills/runs/:runId/presentation`  
- `portal.voucher.redeem` → `POST /user/vouchers/redeem`（写入操作）  
- `portal.recharge.create` → `POST /user/recharge/orders`（写入操作）  
- `portal.recharge.get` → `GET /user/recharge/orders/:orderId`  

**写入操作的安全性检查：**  
- `portal.voucher.redeem` 和 `portal.recharge.create` 操作要求 `payload.confirm` 的值为 `true`。  
- 如果 `confirm` 缺失或不是 `true`，操作执行器会本地拒绝请求，不会发送写入数据。  

## 载荷契约（Payload Contract）  

**默认载荷规范：**  
- `payload.input` 是 `portal.skill.execute` 的主要输入对象。  
- `payload.request_id` 是可选字段，按原样传递。  
- 查询操作直接使用 `payload` 中的字段作为查询参数（如 `date_from`、`date_to`、`service_id`、`channel`）。  

**媒体文件处理规范：**  
- 优先使用输入中已存在的显式 URL 字段（`image_url`、`audio_url`、`file_url`）。  
- 如果存在 `attachment.url`，将其映射到对应的媒体文件 URL 字段。  
- 如果存在 `file_path`，通过 `{site_base}/api/blob/upload` 自动上传；如果 `@vercel/blob/client` 不可用，则使用 `{site_base}/api/blob/upload-file` 作为备用方案；在执行前将 URL 重新填充到输入数据中。  
- 对于不包含 `@vercel/blob/client` 的代理运行时环境，你也可以通过后端（例如 Vercel Blob）预先上传媒体文件，并传递 `attachment.url` 或显式的 URL 字段。  
- `site_base_url` 是一个受保护的字段：运行时仅接受配置好的可信站点基础 URL（默认为 `https://gateway.binaryworks.app` 或环境变量 `SKILL_SITE_BASE_URL`）。  
- 在正常产品流程中，用户无需手动粘贴媒体文件 URL。  

**演示文件处理：**  
- `portal.skill.presentation` 支持 `include_files=true` 选项，以返回包含渲染后的文件 URL 的 `visual.files/assets`。  
- 除非明确禁用，否则 `portal-action.mjs` 默认会启用 `include_files=true`。  
- 图像处理会返回 `overlay`（带边框的图像），以及可选的 `mask` 或 `cutout` 资源。  
- 当配置了 blob 存储时，音频处理会将数据 URL 标准化为 `output.media_files/assets`（包含上传的文件 URL）。  

## 运行时认证桥接（Runtime Auth Bridge）  

**用户范围的操作使用固定的认证机制：**  
1. 解析运行时 API 的关键信息（`api_key`、`agent_uid`、`owner_uid_hint`、`base_url`）。  
2. 使用 `X-API-Key` 和 `x-agent-uid` 发送 `GET /agent/me` 请求以获取 `user_id`。  
3. 使用 `user_id` 和 `api_key` 发送 `POST /user/api-key-login` 请求以获取 `userToken`。  
4. 使用 `Authorization: Bearer <userToken>` 执行门户操作。  

**积分不足时的处理（Insufficient Points Recovery）**  
- 保持 `error.code` 和 `error.message` 不变。  
- 如果有 `error.details.recharge_url`，则将其保留并显示给用户。  
- 日志应建议用户使用 `portal.recharge.create` 或直接访问 `recharge_url`。  

## 打包文件（Bundled Files）：**  
- `scripts/execute.mjs`（命令行参数：`[api_key] [capability] [input_payload] [base_url] [agent_uid] [owner_uid_hint]`）  
- `scripts/poll.mjs`（命令行参数：`[api_key] <run_id> [base_url] [agent_uid] [owner_uid_hint]`）  
- `scripts/feedback.mjs`（命令行参数：`[api_key] [payload_json] [base_url] [agent_uid] [owner_uid_hint]`）  
- `scripts/telemetry.mjs`（共享的尽力收集遥测数据辅助脚本）  
- `scripts/runtime-auth.mjs`（共享的自动初始化辅助脚本）  
- `scripts/portal-auth.mjs`（API 密钥到用户会话的桥接脚本）  
- `scripts/portal-action.mjs`（命令行参数：`[api_key] <action> <payload_json> [base_url] [agent_uid] [owner_uid_hint]`）  
- `scripts/attachment-normalize.mjs`（媒体文件 URL/路径的规范化及上传处理）  
- `references/capabilities.json`  
- `references/openapi.json`  
- `SKILL.zh-CN.md`  

## 遥测与反馈（Telemetry and Feedback）**  
- 打包的脚本现在支持在认证/执行/查询/反馈流程中收集遥测数据。  
- 遥测操作是非阻塞的，即使遥测数据传输失败也不会影响运行时的正常退出。  
- 可选的环境变量：  
  - `SKILL_TELEMETRY_ENABLED`（默认值为 `true`）  
  - `SKILL_TELEMETRY_BASE_URL`（默认为运行时的 `base_url`）  
  - `SKILL_TELEMETRY_TIMEOUT_MS`（默认值为 `2000` 毫秒）  
- 反馈脚本通过 `POST /feedback/submit` 发送数据，并在元数据中附加 `agent_uid` 和 `owner_uid_hint`。  

## 功能 ID（Capability IDs）：**  
- `human_detect`  
- `image_tagging`  
- `tts_report`  
- `embeddings`  
- `reranker`  
- `asr`  
- `tts_low_cost`  
- `markdown_convert`  
- `face-detect`  
- `person-detect`  
- `hand-detect`  
- `body-keypoints-2d`  
- `body-contour-63pt`  
- `face-keypoints-106pt`  
- `head-pose`  
- `face-feature-classification`  
- `face-action-classification`  
- `face-image-quality`  
- `face-emotion-recognition`  
- `face-physical-attributes`  
- `face-social-attributes`  
- `political-figure-recognition`  
- `designated-person-recognition`  
- `exhibit-image-recognition`  
- `person-instance-segmentation`  
- `person-semantic-segmentation`  
- `concert-cutout`  
- `full-body-matting`  
- `head-matting`  
- `product-cutout`  

## 发布说明（Release Notes）**  
发布新版本时，请在此处添加新内容。代理的更新摘要必须根据此部分生成。  

### 2.4.2（2026-03-12）  
**新增功能：**  
- 当 `@vercel_blob/client` 不可用时，为 `file_path` 流添加了 `./api/blob/upload-file` 的直接上传备用方案。  
- 为 `portal.skill.presentation` 添加了文件渲染功能（`visual.files/assets`），以处理 overlay/mask/cutout URL。  
- 当配置了 blob 存储时，音频输出被标准化为 `output.media_files/assets`（包含上传的文件 URL）。  

**兼容性/行为变更：**  
- 无。  

**迁移说明：**  
- 对于不包含 `@vercel_blob/client` 的代理运行时环境，仍按旧方式发送 `file_path`；运行时现在会回退到直接上传。  
- 要获取渲染后的文件，需要使用 `include_files=true` 调用 `portal.skill.presentation`，或依赖门户的默认设置。  

### 2.4.1（2026-03-12）  
**新增功能：**  
- 为 `attachment.url` 添加了服务器端的输入规范化处理（同时处理 `inputattachment.url` 和顶层的 `attachment.url`）。  
- 明确了媒体 URL 的优先级规则（当 `image_url`、`audio_url`、`file_url` 都存在时，优先使用它们）。  
- 对上传优先级的兼容性和行为进行了端到端的测试。  
- 为缺少 `@vercel/blob/client` 的运行时环境提供了备用上传方案。  

**兼容性/行为变更：**  
- 无。  

**迁移说明：**  
- 现有的 `portal-action.mjs` 工作流程保持兼容。  
- 在资源受限的代理运行时环境中，建议优先使用后端预上传功能，然后再传递 `attachment.url` 或显式的媒体文件 URL。  

### 2.4.0（2026-03-12）  
**新增功能：**  
- 为单技能用户操作流程添加了门户操作契约（`portal.me`、balance/ledger/usage`、execute/poll/presentation`、voucher 和 recharge 操作）。  
- 添加了写入操作的安全性检查：`portal.voucher.redeem` 和 `portal.recharge.create` 需要 `confirm=true`。  
- 添加了运行时认证桥接脚本 `portal-auth.mjs`。  
- 添加了操作执行脚本 `portal-action.mjs` 和媒体文件路径规范化脚本 `attachment-normalize.mjs`。  
- 规范化了积分不足时的错误处理逻辑，确保 `recharge_url` 被正确传递。  

**兼容性/行为变更：**  
- 当 `confirm=true` 缺失时，写入操作会立即失败。  
- 现有的 `execute.mjs` 和 `poll.mjs` 工作流程仍然可用。  
- 门户用户应使用 `portal-action.mjs` 来执行相关操作。  

### 2.3.4（2026-03-11）  
**新增功能：**  
- 在运行时脚本中添加了遥测数据收集功能（针对认证/执行/查询操作）。  
- 添加了 `scripts/feedback.mjs`，通过运行时认证（`X-API-Key`）发送结构化的反馈数据。  
- 添加了共享的遥测辅助脚本（`SKILL_TELEMETRY_*`）。  

**兼容性/行为变更：**  
- 无。  

**迁移说明：**  
- 现有的 `execute.mjs` 和 `poll.mjs` 工作流程保持不变。  
- 在资源受限的环境中运行脚本时，可以尝试使用 `/agent/telemetry/ingest` 和 `/telemetry/ingest` 进行遥测数据发送。  

### 2.3.3（2026-03-11）  
**新增功能：**  
- 规范了用户操作相关的指导说明，避免在媒体/文档输入中暴露手动输入的 URL/JSON 字段。  
- 更新了能力参考示例和描述，以匹配基于上传的交互体验。  
- 将 CLI 参数标签从 `input_json` 更改为 `input_payload`，以保持与结构化载荷的一致性。  

**兼容性/行为变更：**  
- 现有的运行时 API 调用保持不变。  
- 如果你的集成使用了自定义输入表单，建议使用文件/附件输入方式，而不是手动输入的 URL/JSON 字段。