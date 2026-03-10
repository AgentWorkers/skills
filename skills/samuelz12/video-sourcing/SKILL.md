---
name: video-sourcing
description: 使用固定的自启动运行时（self-bootstrap runtime），为 `/video_sourcing` 任务运行视频源获取代理（Video Sourcing Agent），并提供确定性强、简洁明了的聊天用户界面（chat UX）。
user-invocable: true
metadata: {"openclaw":{"os":["darwin","linux"],"homepage":"https://github.com/Memories-ai-labs/video-sourcing-agent","requires":{"bins":["git","uv"],"env":["GOOGLE_API_KEY","YOUTUBE_API_KEY"]}}}
---
# 视频来源处理技能

当用户请求查找、比较或分析来自社交媒体平台（如 YouTube、TikTok、Instagram、Twitter/X）的视频，或者明确调用 `/video_sourcing` 时，请使用此技能。

此工作流程需要在主机环境中运行（禁用沙箱模式）。如果未设置 `VIDEO_SOURCING_AGENT_ROOT`，运行器会自动从 `Memories-ai-labs/video-sourcing-agent@v0.2.5` 启动相应的运行时环境。

## 触发条件

在满足以下任一条件时运行此工作流程：
- 消息以 `/video_sourcing` 开头。
- 用户请求视频来源分析、趋势分析、创作者分析或品牌分析，并希望获得具体的视频链接。

如果使用 `/video_sourcing` 但没有提供查询内容，请提示用户提供相应的查询信息。

## 执行流程

1. **解析查询内容**：
   - 如果查询内容包含 `/video_sourcing`，则将其去除，仅使用剩余部分作为查询参数。
   - 如果查询内容为自由格式，直接使用用户的输入作为查询参数。
2. **默认执行模式**：
   - 使用 `--event-detail compact` 选项进行简洁的查询处理。
3. **用户请求调试或原始数据**：
   - 切换到 `--event-detail verbose` 选项以获取更详细的输出。

### `/video_sourcing` 的具体执行步骤

1. **构建命令**：
   - 使用以下命令构建执行脚本：`<skill_dir>/scripts/run_video_query.sh --query "<query>" --event-detail <compact|verbose> --ux-mode three_message --progress-gate-seconds 5`
2. **后台执行**：
   - 使用 `background: true` 选项在后台执行脚本，并设置 420 秒的超时时间。
3. **持续监控进程**：
   - 每 2-4 秒使用 `process` 命令检查进程状态，直到进程结束。
4. **解析输出结果**：
   - 解析生成的 NDJSON 数据，并仅显示与视频来源相关的事件。
   - 使用预设的助手语音发送以下消息：
     - `started`：表示视频来源处理已经开始。
     - `ux_progress`：读取 `summary` 字段中的进度信息，并以自然的语言更新进度状态（不要原样重复 `summary` 的内容）。
     - 每次进度更新都通过 Telegram 作为单独的消息发送给用户。
     - 如果进程遇到错误（`complete`、`clarification_needed`、`error`），则直接发送相应的错误消息。
5. **注意事项**：
   - 不要转发 `progress`、`tool_call` 或 `tool_result` 等中间事件。
   - 在所有消息中保持用户设定的 OpenClaw 语音风格（包括进度更新和最终结果）。
   - 如果当前运行会话仍在进行中，切勿再次启动新的任务。如果需要重试，请先使用 `process` 命令终止之前的会话。
6. **行为规范**：
   - **快速执行（<5 秒）**：仅发送两条消息（开始和完成消息）。
   **长时间执行（≥5 秒）**：以间隔一定的时间发送进度更新消息，最后发送完成消息。

### 自由格式的查询方式

- 保留现有的灵活处理方式。
- 不强制使用 `three_message` 选项，直接执行命令：`<skill_dir>/scripts/run_video_query.sh --query "<query>" --event-detail <compact|verbose>`。

## 最终响应格式

- 当进程完成时（`complete` 事件）：
  - 提供一段简短的总结性文字。
  - 默认情况下，仅显示排名前三的视频链接（包括标题、网址和简短的相关性说明）。
  - 同时列出使用的工具及其状态摘要。

- 如果找不到符合条件的视频（少于 3 个），则显示所有可用的视频链接。

- 如果遇到需要进一步澄清的情况（`clarification_needed` 事件），直接询问用户需要哪些额外的信息。

- 如果出现错误（`error` 事件），发送详细的错误原因，并提供下一步的操作建议。

## 安全性与故障处理

- 如果脚本因缺少环境变量或工具而失败，需明确指出缺失的组件（例如 `VIDEO_SOURCING_AGENT_ROOT`、`uv` 或 API 密钥）。
- 如果未设置 `VIDEO_SOURCING_AGENT_ROOT`，运行器会使用预设的路径：`~/.openclaw/data/video-sourcing-agent/v0.2.5`。
- `VIDEO_SOURCING_AGENT_ROOT` 仅用于本地开发环境的高级配置。
- 响应内容应保持简洁且具有指导性。
- 绝不允许伪造视频链接或相关数据。