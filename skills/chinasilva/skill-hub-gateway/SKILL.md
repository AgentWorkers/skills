---
name: skill-hub-gateway
description: 统一网关技能，用于异步执行和轮询工作流程。
version: 2.3.2
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

默认 API 基本 URL：`https://gateway-api.binaryworks.app`

中文文档：`SKILL.zh-CN.md`

## 版本检查协议（Agent）

- 官方最新版本信息来源：`GET /skills/manifest.json`（返回 `data.version`）。
- 本地当前版本信息来源：已安装的 `SKILL.md` 文件中的 `version` 字段。
- 使用语义版本号（`major.minor.patch`）来比较版本。
- 检查频率：在会话开始时检查一次，同一会话内最多每 24 小时检查一次。
- 如果版本检查失败（网络问题、超时或解析错误），不要阻止运行时执行，继续当前工作流程，并在下一个允许的检查时间窗口重新尝试。

## Agent 的决策流程

- 如果 `latest_version` 大于 `current_version`，则读取本文档中 “发布说明”（Release Notes）部分对应的更新内容，生成 `update_summary`。
- Agent 应向用户显示：
  - `current_version`
  - `latest_version`
  - `update_summary`
- 用户可以选择：
  - `立即更新`（Update now）
  - `稍后提醒我`（Remind me later in this session）
- 如果用户选择 “稍后提醒我”，则在同一会话内不再重复提示相同版本的更新信息，直到会话结束。

## 首次使用时的引导流程（install_code）

脚本默认会自动完成引导流程：

1. 发送 `POST /agent/install-code/issue` 请求，参数为 `{"channel":"local"}` 或 `{"channel":"clawhub"}`。
2. 读取 `data.install_code` 的内容。
3. 发送 `POST /agent/bootstrap` 请求，参数为 `{"agent_uid":"<agent_uid>","install_code":"<install_code>"}`。
4. 读取 `data.api_key`，然后使用 `X-API-Key` 或 `Authorization: Bearer <api_key>` 来调用运行时 API。

**手动设置**：

- 你也可以显式提供 `api_key`。
- 如果省略了 `agent_uid` 和 `owner_uid_hint`，脚本会从当前工作区路径中获取默认值。

## 运行时契约（Runtime Contract, V2）

- 执行操作：`POST /skill/execute`
- 查询运行状态：`GET /skill/runs/:run_id`
- 基于图像的功能支持 `image_url`，支持文件上传和 URL 模式。如果使用 URL 模式，`image_url` 必须是直接的图像文件 URL（响应的 `Content-Type` 应为 `image/*`），不能是网页 URL。
- 运行状态有两种：`succeeded`（成功）和 `failed`（失败）。
- 成功时返回 `output`；失败时返回 `error`（包含 `code` 和 `message`）。

## 输入源说明

- 基于图像的功能（如 `human_detect`、`image_tagging` 以及所有 Roboflow 的图像相关功能）接受上传的图像或显式的 `image_url`。
- 所提供的 CLI 脚本（`scripts/execute.mjs` / `scripts/poll.mjs`）不包含上传参数，它们仅发送你提供的 JSON 输入。
- 该技能支持用户上传的媒体文件/文档，用于以下功能：
  - 使用 `image_url` 的图像处理功能
  - 使用 `audio_url` 的语音识别（ASR）功能
  - 使用 `file_url` 的 Markdown 转换功能
- 运行时可能会在调用功能之前将上传的文件转换为临时对象 URL。
- 如果客户端使用 URL 模式，请提供可直接下载的 `image_url`、`audio_url` 或 `file_url`。本地文件系统路径和网页 URL 是无效的。
- 对于 `bootstrap`/`execute`/`poll` 操作的失败情况，请保留响应 JSON 中的 `request_id`。脚本的 stderr 会记录 `status`、`code`、`message` 和 `request_id` 以便故障排查。

## 功能 ID

- `human_detect`（人脸检测）
- `image_tagging`（图像标注）
- `tts_report`（文本转语音）
- `embeddings`（嵌入功能）
- `reranker`（排名功能）
- `asr`（自动语音识别）
- `tts_low_cost`（低成本语音合成）
- `markdown_convert`（Markdown 转换）
- `face-detect`（人脸检测）
- `person-detect`（人物检测）
- `hand-detect`（手部检测）
- `body-keypoints-2d`（2D 身体关键点）
- `body-contour-63pt`（63 点身体轮廓）
- `face-keypoints-106pt`（106 点面部关键点）
- `head-pose`（头部姿态）
- `face-feature-classification`（面部特征分类）
- `face-action-classification`（面部动作分类）
- `face-image-quality`（面部图像质量）
- `face-emotion-recognition`（面部情绪识别）
- `face-physical-attributes`（面部物理属性）
- `face-social-attributes`（面部社交属性）
- `political-figure-recognition`（政治人物识别）
- `designated-person-recognition`（指定人物识别）
- `exhibit-image-recognition`（展览图像识别）
- `person-instance-segmentation`（人物实例分割）
- `person-semantic-segmentation`（人物语义分割）
- `concert-cutout`（音乐会人物剪裁）
- `full-body-matting`（全身抠图）
- `head-matting`（头部抠图）
- `product-cutout`（产品抠图）

## 所包含的文件

- `scripts/execute.mjs`（CLI 参数：`[api_key] [capability] [input_json] [base_url] [agent_uid] [owner_uid_hint]`）
- `scripts/poll.mjs`（CLI 参数：`[api_key] <run_id> [base_url] [agent_uid] [owner_uid_hint]`）
- `scripts/runtime-auth.mjs`（用于自动引导的辅助脚本）
- `references/capabilities.json`（功能参考文档）
- `references/openapi.json`（OpenAPI 参考文档）
- `SKILL.zh-CN.md`（中文文档）

## 发布说明（Release Notes）

发布新版本时，请在此处添加新内容。Agent 的更新摘要必须根据此部分生成。

### 2.3.2（2026-03-10）

**新增内容**

- 使功能参考文档与运行时行为保持一致：主机流程支持文件上传/聊天附件，运行时可能会将上传内容转换为 URL 格式。
- 同步包级 OpenAPI 版本与 `SKILL` 文档中的版本信息，以避免发布元数据不一致的问题。
- 添加了包级测试机制，以防止未来文档版本不匹配的情况。

**变更/行为影响**

- 无。

**迁移说明**

- 现有的运行时 API 调用保持不变。
- 如果你的集成从文档中读取功能描述，请刷新缓存文档以获取更新后的上传说明。

### 2.3.1（2026-03-10）

**新增内容**

- 明确了上传行为：CLI 脚本本身不执行上传操作，上传功能由主机客户端负责。
- 在 CLI 脚本中添加了结构化的错误日志记录（`status`、`code`、`message`、`request_id`），以便于排查 `bootstrap`/`execute`/`poll` 操作的故障。

**变更/行为影响**

- 无。

**迁移说明**

- 现有的 API 调用保持不变。
- 如果你解析脚本的错误日志，请允许新的 JSON 格式错误记录。

### 2.3.0（2026-03-10）

**新增内容**

- 基于 `/skills/manifest.json` 添加了正式的版本检查协议。
- 增加了 Agent 的更新确认流程（“立即更新”/“稍后提醒我”）。
- 将此 “发布说明” 部分定义为向用户展示更新摘要的官方来源。

**变更/行为影响**

- 无。

**迁移说明**

- 现有的集成可以继续使用现有的运行时 API 调用。
- 要启用更新通知，Agent 实现需要解析此部分内容，并将安装的版本与 `data.version` 进行比较。