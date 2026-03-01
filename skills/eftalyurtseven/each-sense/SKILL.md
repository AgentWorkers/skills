---
name: each-sense
description: `each::sense` 是一个用于生成型内容的智能平台，它是一个集成的 AI 代理，能够生成营销素材、广告、产品图片、视频以及创意内容。该平台熟悉各种 AI 模型，并能自动为您的任务选择最适合的模型。您可以将其用于任何创意内容生成的需求。
metadata:
  author: eachlabs
  version: "1.0"
---
# each::sense – 用于生成式媒体的智能工具

each::sense 是一个集成的 AI 代理，能够生成图像、视频，构建工作流程，并进行对话式交互。它使用 Claude 作为核心调度器，可以访问 200 多个 AI 模型。

**在以下情况下使用 each::sense：**
- 需要营销素材和广告创意
- 需要产品图片和电子商务视觉素材
- 需要视频内容（广告、用户生成内容 UGC、社交媒体）
- 需要任何创意内容的生成
- 需要结合多个 AI 模型的多步骤工作流程

## 认证

```
Header: X-API-Key: <your-api-key>
```

请在 [eachlabs.ai](https://eachlabs.ai) 获取您的 API 密钥 → API 密钥。

将 `EACHLABS_API_KEY` 环境变量设置为相应的值。

## 基本 URL

```
https://sense.eachlabs.run
```

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a portrait of a woman with golden hour lighting",
    "mode": "max"
  }'
```

该端点会返回服务器发送的事件（Server-Sent Events, SSE），其中包含实时进度和最终生成的输出结果。

## 请求格式

```json
{
  "message": "string (required) - User's request",
  "session_id": "string (optional) - Session ID for conversation history and multi-turn chats",
  "mode": "string (optional, default: 'max') - Quality mode: 'max' or 'eco'",
  "behavior": "string (optional, default: 'agent') - Behavior: 'agent', 'plan', or 'ask'",
  "model": "string (optional, default: 'auto') - Model slug or 'auto' for AI selection",
  "image_urls": "array[string] (optional) - Image URLs for editing/processing",
  "workflow_id": "string (optional) - Enables workflow building mode",
  "version_id": "string (optional) - Required with workflow_id",
  "web_search": "boolean (optional, default: true) - Enable/disable web search",
  "enable_safety_checker": "boolean (optional, default: true) - Set to false to allow NSFW content generation"
}
```

### 参数详情

| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `message` | 字符串 | 必填 | 自然语言请求 |
| `session_id` | 字符串 | 可空 | 会话 ID，用于记录对话历史。用于继续之前的对话、处理澄清请求以及迭代优化输出 |
| `mode` | 字符串 | "max" | `max`：最高质量；`eco`：最快/最经济 |
| `behavior` | 字符串 | "agent" | `agent`：自动执行；`plan`：先解释；`ask`：先询问 |
| `model` | 字符串 | "auto" | 指定模型名称或使用 "auto" 选择 AI 模型 |
| `image_urls` | 数组 | 可空 | 需要处理/编辑的图片 URL |
| `workflow_id` | 字符串 | 可空 | 启用工作流程构建模式 |
| `version_id` | 字符串 | 可空 | 工作流程版本，与 `workflow_id` 一起使用 |
| `web_search` | 布尔值 | `true` | 允许进行网络搜索 |
| `enable_safety_checker` | 布尔值 | `true` | 设置为 `false` 可以生成不适宜工作场所的内容 |

## 模式

在生成内容之前，代理会询问用户是追求高质量还是快速/低成本：
- **“您想要快速且低成本的结果，还是高质量的结果？”**
- **“快速草图还是高级输出？”**

### MAX 模式（默认）
使用最高质量的模型。适用于最终输出、面向客户的工作，以及质量要求较高的场景。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{"message": "Create a product shot", "mode": "max"}'
```

### ECO 模式
使用快速且成本效益高的模型。适用于原型设计、草图制作以及大量内容生成。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{"message": "Create a product shot", "mode": "eco"}'
```

## 行为模式

### Agent（默认）
自动执行请求，选择最佳模型并生成输出。

```json
{"message": "Generate a sunset video", "behavior": "agent"}
```

### Plan
在执行前先解释操作步骤。适用于需要查看处理方式的复杂请求。

```json
{"message": "Create a marketing video for my bakery", "behavior": "plan"}
```

### Ask
在继续之前总是会询问用户需要澄清的问题。适用于希望拥有最大控制权的场景。

```json
{"message": "Generate a portrait", "behavior": "ask"}
```

## 会话管理

使用 `session_id` 在多个请求之间保持对话历史和上下文。这可以实现：
- **多轮对话**：无需重复上下文即可跟进之前的请求
- **迭代优化**：请求对之前生成的内容进行修改
- **澄清流程**：响应 `clarification_needed` 事件并继续对话
- **上下文感知**：AI 会记住之前的生成结果、用户偏好和指令

### 工作原理

在请求中提供唯一的 `session_id`。具有相同 `session_id` 的所有请求都会共享对话历史。

```bash
# Use any unique string as session_id
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a portrait",
    "session_id": "my-chat-session-123"
  }'
```

### 示例：迭代生成

```bash
# First request - generate initial image
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a logo for a coffee shop called Brew Lab",
    "session_id": "logo-project-001"
  }'

# Follow-up - modify the result (same session_id)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make it more minimalist and change the color to dark green",
    "session_id": "logo-project-001"
  }'

# Another follow-up - request variation (same session_id)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 3 variations of this logo",
    "session_id": "logo-project-001"
  }'
```

### 示例：处理澄清请求

```bash
# Ambiguous request - AI will ask for clarification
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Edit this image",
    "session_id": "edit-task-001",
    "image_urls": ["https://example.com/photo.jpg"]
  }'
# Response: clarification_needed event asking what edit to make

# Respond to clarification (same session_id)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the background and make it transparent",
    "session_id": "edit-task-001",
    "image_urls": ["https://example.com/photo.jpg"]
  }'
```

### 会话持久化

- 会话会被持久化，可以随时恢复
- 每个会话都会保留完整的对话历史
- 使用会话与 each::sense 构建类似聊天的体验
- 您可以自行控制 `session_id`——为相关请求使用任何唯一的字符串

## 使用场景示例

### 1. 图像生成

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a professional headshot of a business executive, studio lighting",
    "mode": "max"
  }'
```

### 2. 视频生成

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 5 second video of a sunset over the ocean",
    "mode": "max"
  }'
```

### 3. 图像编辑（使用上传的图片）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the background from this image",
    "image_urls": ["https://example.com/my-photo.jpg"]
  }'
```

### 4. 图像转视频动画

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Animate this image with gentle camera movement",
    "image_urls": ["https://example.com/landscape.jpg"]
  }'
```

### 5. 直接执行模型（跳过 AI 选择）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "A cyberpunk city at night with neon lights",
    "model": "flux-2-max"
  }'
```

### 6. 产品摄影

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a product shot of a coffee mug on a wooden table with morning light",
    "mode": "max"
  }'
```

### 7. 营销素材

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a social media ad for a fitness app, show someone working out with energetic vibes",
    "mode": "max"
  }'
```

### 8. 多轮对话

```bash
# First request with a session_id
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Edit this image",
    "session_id": "user-123-chat",
    "image_urls": ["https://example.com/photo.jpg"]
  }'

# Response includes clarification_needed asking what edit to make
# Follow-up with same session_id
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the background",
    "session_id": "user-123-chat",
    "image_urls": ["https://example.com/photo.jpg"]
  }'
```

### 9. 复杂工作流程（用户生成内容 UGC 视频）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 30 second UGC video with a consistent presenter explaining why fitness is important. The presenter is a 30-year-old fit woman with brown hair in workout clothes, gym background.",
    "mode": "max"
  }'
```

## SSE 响应格式

该端点返回服务器发送的事件（Server-Sent Events, SSE），内容类型为 `text/event-stream`。

每个事件的格式如下：
```
data: {"type": "event_type", ...fields}\n\n
```

流式响应的结束标志如下：
```
data: [DONE]\n\n
```

### 事件类型

| 事件 | 描述 |
|-------|-------------|
| `thinking_delta` | AI 的实时推理过程 |
| `status` | 当前正在执行的操作 |
| `text_response` | 文本内容（解释、答案等） |
| `generation_response` | 生成的媒体 URL |
| `clarification_needed` | AI 需要更多信息 |
| `web_search_query` | 正在执行的网络搜索 |
| `web_search_citations` | 搜索结果的引用 |
| `workflow_created` | 新工作流程已创建 |
| `workflow_fetched` | 加载了现有工作流程 |
| `workflow_built` | 构建了工作流程定义 |
| `workflow_updated` | 工作流程已推送到 API |
| `execution_started` | 工作流程开始执行 |
| `execution_progress` | 执行过程中的进度更新 |
| `execution_completed` | 工作流程执行完成 |
| `tool_call` | 调用的工具详情 |
| `message` | 信息性消息 |
| `complete` | 包含总结的最终事件 |
| `error` | 发生了错误 |

### 关键事件示例

#### generation_response
生成的媒体 URL（主要输出）：
```json
{
  "type": "generation_response",
  "url": "https://storage.eachlabs.ai/outputs/abc123.png",
  "generations": ["https://storage.eachlabs.ai/outputs/abc123.png"],
  "total": 1,
  "model": "nano-banana-pro"
}
```

#### clarification_needed
AI 需要更多信息：
```json
{
  "type": "clarification_needed",
  "question": "What type of edit would you like to make to this image?",
  "options": ["Remove the background", "Apply a style transfer", "Upscale to higher resolution"],
  "context": "I can see your image but need to know the specific edit you want."
}
```

#### complete
包含总结的最终事件：
```json
{
  "type": "complete",
  "task_id": "chat_1708345678901",
  "status": "ok",
  "generations": ["https://storage.eachlabs.ai/outputs/abc123.png"],
  "model": "nano-banana-pro"
}
```

#### error
发生了错误：
```json
{
  "type": "error",
  "message": "Failed to generate image: Invalid aspect ratio"
}
```

## 模型别名

一些常用的简写名称及其对应的完整模型名称：

| 别名 | 对应的完整模型名称 |
|-------|-------------|
| flux max | flux-2-max |
| flux pro | flux-2-pro |
| gpt image | gpt-image-1-5 |
| nano banana pro | nano-banana-pro |
| seedream | seedream-4-5 |
| gemini imagen | gemini-imagen-4 |
| kling 3 | kling-3-0 |
| veo | veo3-1-text-to-video-fast |
| sora | sora-2 |
| hailuo | hailuo-2-3 |

## 错误处理

### HTTP 错误

| 错误代码 | 错误信息 | 原因 |
|------|----------|-------|
| 401 | `{"detail": "API 密钥是必需的。"}` | 缺少或无效的 API 密钥 |
| 500 | `{"detail": "错误信息"}` | 服务器内部错误 |
| 503 | `{"detail": "ChatAgent 不可用"}` | 服务暂时不可用 |

### 流式传输错误

```json
{"type": "error", "message": "Failed to execute model: Invalid parameters"}
```

| 错误信息 | 原因 | 解决方案 |
|--------------|-------|----------|
| `Failed to create prediction: HTTP 422` | 账户余额不足 | 请在 eachlabs.ai 充值 |
| `Failed to execute model: Invalid parameters` | 输入参数无效 | 检查模型参数 |
| `Model not found` | 模型名称无效 | 使用 "auto" 或有效的模型名称 |
| `Workflow execution timed out` | 超过 1 小时限制 | 将任务拆分为多个较小的工作流程 |

## 超时设置

**建议的客户端超时设置：** 将 HTTP 客户端超时设置为 **至少 10 分钟**。复杂场景可能需要依次运行多个 AI 模型（例如，生成用户生成内容 UGC 视频时可能需要运行 10 个以上模型），这可能需要几分钟时间。

```bash
# curl example with 10 minute timeout
curl --max-time 600 -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{"message": "Create a complex UGC video..."}'
```

**平台限制：**
- 流式连接在 1 小时无活动后会超时
- 工作流程执行在 1 小时后也会超时

## 调用限制

- 取决于您的 EachLabs API 密钥等级

## 最佳实践：
1. **使用 `session_id` 保持多轮对话的上下文**
2. **在原型设计和对成本敏感的应用中使用 ECO 模式**
3. **在明确需求时使用特定模型**（以加快执行速度）
4. **处理澄清请求** – 在同一会话中提供所需的信息
5. **提供清晰的提示** – 明确指定风格、情绪和构图要求
6. **监控 SSE 事件** – 使用 `thinking_delta` 了解进度，使用 `generation_response` 查看输出结果