---
name: rawugc-api
description: 调用 RawUGC 视频生成 API 来创建和管理 AI 视频（适用于 Sora 2 及其他模型）。当用户希望通过 RawUGC 生成 AI 视频、集成 RawUGC API、检查视频状态、列出视频内容，或进行文本转视频/图片转视频操作时，请使用该 API。
requires:
  env:
    - RAWUGC_API_KEY
compatibility: Requires RAWUGC_API_KEY (Bearer token for https://rawugc.com/api/v1). Obtain from RawUGC dashboard.
homepage: https://github.com/tfcbot/rawugc-skills
source: https://github.com/tfcbot/rawugc-skills
---
# RawUGC视频生成API

以下是代理程序调用RawUGC视频生成API所需了解的流程信息。所有请求都需要从RawUGC控制面板获取API密钥，该密钥需通过环境变量传递。

## 认证

- **环境变量**：从`RAWUGC_API_KEY`中读取API密钥。该密钥是在RawUGC控制面板中生成的，必须保密，切勿将其硬编码或记录在代码中。
- **请求头**：在每个请求中添加`Authorization: Bearer <RAWUGC_API_KEY>`。
- 如果`RAWUGC_API_KEY`缺失或为空，请告知用户他们需要设置该密钥，并从RawUGC控制面板获取它。

## 基础URL

- **生产版本**：`https://rawugc.com/api/v1`
- 以下所有路径都是相对于此基础URL的。

## 端点

### POST /videos/generate

用于启动视频生成。

**请求体（JSON）**：

| 字段 | 类型 | 是否必填 | 说明 |
|-------|------|----------|-------------|
| `model` | 字符串 | 是 | 可选值：`sora-2-text-to-video`、`sora-2-image-to-video`、`kling-2.6/motion-control`、`veo3`、`veo3_fast` |
| `prompt` | 字符串 | 对于`sora-2-text-to-video`和`veo3` | 文本描述（1–5000个字符）。必填 |
| `imageUrls` | 字符串数组 | 对于`sora-2-image-to-video`和`kling` | 图片URL数组（最多10个）。对于`sora-2-image-to-video`是必填的；对于`kling-2.6/motion-control`还需要`videoUrls` |
| `videoUrls` | 字符串数组 | 对于`kling` | 视频URL数组（最多1个）。仅对`kling-2.6/motion-control`是必填的 |
| `aspectRatio` | 字符串 | 可选 | `portrait`或`landscape`（某些模型还支持`16:9`、`9:16`、`Auto`） |
| `nFrames` | 字符串 | 可选 | 视频长度（`10`或`15`帧） |
| `selectedCharacter` | 字符串 | 可选 | 角色用户名（例如`rawugc.mia`） |
| `characterOrientation` | 字符串 | 可选 | `image`或`video` |
| `mode` | 字符串 | 可选 | 分辨率（`720p`或`1080p`，仅对支持的模型有效） |

**响应（201状态码）**：`taskId`、`model`、`status`（例如`pending`）、`creditsUsed`、`newBalance`、`estimatedCompletionTime`、`createdAt`。

### GET /videos/:taskId

用于获取视频生成任务的进度。

**请求参数**：`taskId`（来自`generate`响应）。

**响应（200状态码）**：`taskId`、`status`（`pending` | `processing` | `completed` | `failed`）、`model`、`prompt`、`creditsUsed`、`resultUrl`（当`status === 'completed'时）、`createdAt`、`completedAt`、`failCode`、`failMessage`、`progress`（0–100）。

### GET /videos`

列出用户的视频，支持可选过滤和分页。

**查询参数**：`status`（可选：`pending` | `processing` | `completed` | `failed`）、`limit`（1–100，默认50）、`page`（默认1）。

**响应（200状态码）**：`videos`（与`GET /videos/:taskId`返回的数据结构相同）、`pagination`：`total`、`page`、`pageSize`、`hasMore`。

## 错误

响应遵循RFC 7807问题详细信息规范（JSON格式）：`type`、`title`、`status`（HTTP状态码）、`detail`、可选`instance`、可选`errors`（特定字段的验证错误信息）。

| 状态码 | 含义 |
|--------|---------|
| 400 | 验证错误（请求体或参数无效）。向用户显示`detail`和`errors`。 |
| 401 | 认证错误（API密钥缺失或无效）。提示用户检查`RAWUGC_API_KEY`。 |
| 402 | 信用点数不足。用户需要在RawUGC控制面板中补充信用点数。 |
| 404 | 视频未找到（请求`GET /videos/:taskId`）。 |
| 429 | 超过请求频率限制。请按照响应中提示的时间间隔重试或稍后再次尝试。 |
| 500 | 服务器内部错误。建议重试或联系技术支持。 |

## 工作流程：生成后进行轮询

1. **生成视频**：使用`POST /videos/generate`发送请求，并记录返回的`taskId`。
2. **轮询**：定期调用`GET /videos/:taskId`（例如每10–30秒一次）。可以选择使用指数退避策略。
3. **完成视频**：当`status`为`completed`时，使用`resultUrl`获取视频；当`status`为`failed`时，向用户显示`failCode`和`failMessage`。

有关完整的请求/响应格式和状态码信息，请参阅[reference.md](reference.md)。