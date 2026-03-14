---
name: ai-task-hub
description: 这是一个AI任务中心，支持图像分析、背景去除、语音转文本、文本转语音、Markdown格式转换等功能，同时还提供了异步执行、任务监控以及任务展示等 orchestration（协调）功能。当用户需要使用托管的AI服务时，该平台可以处理用户的身份验证、费用结算、支付流程以及风险控制等事务。
version: 3.1.1
metadata:
  openclaw:
    skillKey: ai-task-hub
    emoji: "🧩"
    homepage: https://gateway.binaryworks.app
    requires:
      bins:
        - node
      env:
        - AGENT_TASK_TOKEN
    primaryEnv: AGENT_TASK_TOKEN
---
# AI任务中心  
（Formerly `skill-hub-gateway`）  

**公共包功能说明：**  
- 仅负责协调 `portal.skill.execute`、`portal.skill.poll` 和 `portal.skill.presentation` 这三个操作。  
- 该包内部不处理 `api_key` 或 `userToken` 的交换。  
- 也不负责充值或支付流程。  
- 假设宿主运行时会提供临时生成的任务令牌（task tokens）和附件URL。  

**中文文档：** `SKILL.zh-CN.md`  

## 适用场景：**  
当用户需要执行以下操作时，请使用此技能：  
- 从图像中检测人物、面部、手部特征或标签；  
- 去除图片背景或生成产品/肖像的裁剪图；  
- 将上传的音频转录为文本（语音转文本）；  
- 根据文本生成语音（文本转语音）；  
- 将上传的文件转换为Markdown格式；  
- 启动异步任务并后续检查运行状态；  
- 获取渲染后的视觉输出（如叠加层、遮罩图、裁剪图）；  
- 运行嵌入或重新排序任务以支持数据检索流程。  

## 常见请求示例：**  
- “从这张图片中检测面部并返回边界框。”  
- “为这张图片添加标签并总结主要对象。”  
- “去除这张产品照片的背景。”  
- “从这张肖像图片中生成清晰的裁剪图。”  
- “将这段会议音频转录为文本。”  
- “根据这段文字生成语音。”  
- “将这个PDF文件转换为Markdown格式。”  
- “现在启动这个任务，稍后检查其运行状态。”  
- “获取任务`run_456`的渲染输出文件（叠加层、遮罩图）。  
- “为这个文本列表生成嵌入向量并重新排序结果。”  

## 便于搜索的别名：**  
- **视觉处理相关功能**：`face_detection`、`human_detection`、`person_detection`、`image_tagging`  
- **背景处理相关功能**：`remove_background`、`background Removal`、`cutout`、`matting`、`product-cutout`  
- **语音处理相关功能**：`speech_to_text`、`audio_transcription`  
- **文本转语音相关功能**：`text_to_speech`、`voice_generation`  
- **文件格式转换相关功能**：`document_tomarkdown`、`file_tomarkdown`、`markdownConversion`  
- **任务状态查询相关功能**：`check_job_status`、`poll_long_running_task`、`async_run_status`  
- **渲染输出相关功能**：`rendered_output`、`overlay`、`mask`、`cutout_files`  
- **嵌入/重新排序相关功能**：`vectorization`、`semantic_vectors`、`relevance_reranking`  

## 运行时协议：**  
默认API基础URL：`https://gateway-api.binaryworks.app`  

**端点映射：**  
- `portal.skill.execute` → `POST /agent/skill/execute`  
- `portal.skill.poll` → `GET /agent/skill/runs/:run_id`  
- `portal.skill.presentation` → `GET /agent/skill/runs/:run_id/presentation`  

## 认证协议（由宿主管理）：**  
所有请求必须包含以下字段：  
- `X-Agent-Task-Token: <jwt_or_paseto>`  

**推荐的令牌字段：**  
- `sub`（用户ID）  
- `agent_uid`  
- `conversation_id`  
- `scope`（`execute`/`poll`/`presentation`）  
- `exp`  
- `jti`  

**`scripts/skill.mjs`脚本的命令参数顺序：**  
- `[agent_task_token] <action> <payload_json> [base_url]`  
- 如果省略了`agent_task_token`参数，脚本会从环境变量中读取该值。  

**有效载荷规范：**  
- `portal.skill.execute`：有效载荷需要包含 `capability` 和 `input`。  
- `payload.request_id` 是可选字段，会传递给服务器。  
- `portal.skill.poll` 和 `portal.skill.presentation`：有效载荷需要包含 `run_id`。  
- `portal.skill.presentation` 支持 `include_files` 参数（默认值为 `true`）。  

**附件处理规则：**  
- 建议使用明确的附件URL（`image_url`、`audio_url`、`file_url`）。  
- `attachment.url` 会根据具体功能映射到相应的媒体字段。  
- 在发布的包版本中，本地文件路径（`file_path`）不可使用。  
- 宿主必须先上传聊天附件，再传递相应的URL。  
- 宿主上传附件的示例端点：`/api/blob/upload-file`  

**错误处理：**  
保留原始的错误信息（包括 `request_id`、`data`、`error`）。  
当出现 `POINTS_INSUFFICIENT` 错误时，将错误详情（`error.details.recharge_url`）一并传递给客户端。  

**配套文件：**  
- `scripts/skill.mjs`  
- `scripts/agent-task-auth.mjs`  
- `scripts/attachment-normalize.mjs`  
- `scripts/telemetry.mjs`（兼容性补丁）  
- `references/capabilities.json`  
- `references/openapi.json`  
- `SKILL.zh-CN.md`