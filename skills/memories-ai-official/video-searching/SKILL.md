---
name: video-searching
description: 通过 Memories.ai 视频搜索 API，可以在 YouTube、TikTok、Instagram 和 X/Twitter 上搜索并分析视频。
user-invocable: true
metadata: {"openclaw":{"os":["darwin","linux"],"homepage":"https://api-tools.memories.ai/agents/video-searching-api","requires":{"bins":["curl","jq"],"env":["MEMORIES_API_KEY"]}}}
---
# 视频搜索功能

当用户请求查找、比较或分析社交媒体视频（如 YouTube、TikTok、Instagram、Twitter/X）时，或明确使用 `/video_search` 命令时，可以使用此功能。

该功能会调用 Memories.ai 的视频搜索 API — 该 API 通过令牌认证进行身份验证，并能在多个平台上进行搜索，最终以 SSE 格式返回结构化结果。

## 触发条件

在满足以下任一条件时，执行此流程：
1. 消息以 `/video_search` 开头。
2. 用户请求视频来源、趋势、创作者或品牌分析，并希望获取具体的视频链接。

如果使用 `/video_search` 但没有提供查询内容，请提示用户补充查询信息。

## 执行流程

1. **解析查询内容**：
   - 如果查询内容以 `/video_search` 开头，将其去除，使用剩余部分作为查询字符串。
   - 如果查询内容为自由格式，直接将用户输入的消息作为查询字符串。

2. **构建 API 请求 JSON 数据**：
   - `query`（必填）：用户的搜索关键词。
   - `platforms`（可选）：`youtube`、`tiktok`、`instagram`、`twitter` 中的一个或多个平台 — 仅在用户指定平台时设置。
   - `max_results`（可选，默认值 10）：返回的视频结果数量。
   - `time_frame`（可选）：`past_24h`、`past_week`、`past_month`、`past_year` — 仅在用户指定时间范围时设置。
   - `max_steps`（可选，默认值 10）：代理执行的最大迭代次数。
   - `enable_clarification`（可选，默认值 false）：如果用户查询不明确，设置为 `true` 以请求进一步说明。

3. **调用运行脚本**：
   ```
   <skill_dir>/scripts/run_video_query.sh \
     --query "<query>" \
     [--platforms "youtube,tiktok"] \
     [--max-results 10] \
     [--time-frame past_week] \
     [--enable-clarification]
   ```

4. 使用 `background: true` 启动执行流程。

5. 每 2–4 秒使用 `process` 命令进行一次轮询，直到任务完成。

6. **解析 API 返回的结果**：
   - `started`：发送消息 “🔍 开始视频搜索...”。
   - `progress`：从 `message` 字段发送简明的进度更新（如果上次更新时间距离现在小于 3 秒，则跳过更新）。
   - `complete`：发送最终格式化的响应结果（详见下文）。
   - `clarification`：直接向用户询问需要进一步说明的内容；将此作为最终响应。
   - `error`：发送简明的错误原因，并提供下一步可操作的解决方案。

7. **注意**：不要将原始的 `tool_call` 或 `tool_result` 事件直接发送给用户。

## 最终响应格式

- 当任务状态为 `complete` 时：
  - 提供一段简短的总结（来自 `answer` 字段）。
  - 显示排名前 5 个视频的详细信息：
    - `title`（视频标题）
    - `url`（视频链接）
    - `platform`（平台标识，例如 🎬 YouTube、🎵 TikTok、📸 Instagram、🐦 X）
    - 一条简短的 `relevance_note`（相关性说明）
    - 主要指标（如观看次数、点赞数、互动率等，如有的话）。
  - 在页面底部显示执行时间：`⏱ {execution_time_seconds}s · {steps_taken} 步骤 · {tools_used}`

- 当任务状态为 `clarification` 时：
  - 直接向用户询问需要进一步说明的内容，并提供相应的选项。
  - 将此作为当前任务的最终响应。

- 当任务状态为 `error` 时：
  - 发送简明的错误原因，并提供下一步可操作的解决方案。

## 安全性与备用方案：
1. 如果 `MEMORIES_API_KEY` 未设置，提示用户：“⚠️ 请在 OpenClaw 环境变量中设置 `MEMORIES_API_KEY` 以使用此功能。”
   > 请访问 https://api-tools.memories.ai 获取 API 密钥。
2. 如果 API 返回非 SSE 格式的错误（HTTP 4xx/5xx 状态码），显示错误信息。
3. 绝不允许伪造视频链接或数据指标。
4. 如果 API 无法访问，建议检查网络连接和 API 的运行状态。