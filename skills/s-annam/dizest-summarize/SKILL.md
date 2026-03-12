---
name: dizest-summarize
description: "使用 Dizest API 概述长篇内容（如文章、播客、研究论文、PDF 文件、笔记等），将您阅读的内容转化为结构化且可搜索的知识。"
metadata: {"openclaw":{"emoji":"📝","requires":{"env":["DIZEST_API_KEY"]}}}
---
# Dizest 摘要功能

Dizest 可以将长篇内容转换为结构化、可搜索的知识摘要。该功能由 [Dizest: AI 摘要器](https://www.dizest.ai) 提供支持，该工具可在 [App Store](https://apps.apple.com/app/id6752311120) 和 [Google Play](https://play.google.com/store/apps/details?id=com.ideas116.dizest) 中下载。

**基础 URL:** `https://api.dizest.ai`

访问 [www.dizest.ai](https://www.dizest.ai) 以获取更多产品信息。

---

## 适用场景

当用户需要以下操作时，可以使用此功能：
- 摘要研究论文或学术内容，提取关键发现；
- 摘要来自 YouTube 等平台的长篇播客、采访或视频内容；
- 处理文章、博客文章或网页内容（通过 URL）；
- 摘要 PDF 文件、报告、市场分析报告或商业文档；
- 摘要纯文本（如笔记、转录内容或复制粘贴的文本）；
- 根据特定要求进行摘要处理（例如：“重点关注方法论和关键发现”）。

---

## 重要注意事项

**代理必须作为薄客户端（thin client）运行**：
- **不得** 从用户输入中提取、解析或分类 URL；
- **不得** 判断输入内容是 URL、纯文本还是包含 URL 的文本；
- **不得** 在调用 API 之前获取、抓取或预处理任何内容；
- **不得** 处理需要付费才能访问的内容或尝试任何变通方法。

所有内容分析、URL 检测、提取、付费墙处理以及执行逻辑均在 **服务器端** 完成。代理的唯一任务是按原样将用户输入传递给 API。

---

## 认证

所有请求都必须包含 `x-api-key` 请求头。该密钥应来自 `DIZEST_API_KEY` 环境变量。

---

**如果未设置 `DIZEST_API_KEY` 环境变量且用户未提供 API 密钥，请告知他们以下获取方法：**
1. 从 [dizest.ai](https://www.dizest.ai/#download) 下载 Dizest 应用（支持 iOS、Android 和 macOS 平台）；
2. 创建账户并登录；
3. 通过应用激活账户（只需一次设置）；
4. 在 [dizest.ai/api/keys](https://dizest.ai/api/keys) 生成 API 密钥（使用同一账户登录）。

生成 API 密钥需要通过应用激活账户。移动应用和桌面应用还提供更多功能，如浏览原始内容、离线查看摘要、整理资料库以及查看具有更高权限和高级功能的订阅计划。

---

## API 流程

API 流程分为两个步骤：**创建执行请求**，然后 **获取结果**。

### 第一步：创建执行请求

**端点：** [此处应填写端点地址](```
POST https://api.dizest.ai/v1/summarize
```

**请求头：** [此处应填写请求头信息](```
Content-Type: application/json
x-api-key: $DIZEST_API_KEY
```

**请求体（基本格式）：** [此处应填写基本请求体格式](```json
{
  "content": "<user input>"
}
```

**请求体（包含自定义指令）：** [此处应填写包含自定义指令的请求体格式](```json
{
  "content": "<user input>",
  "custom_instructions": "<what to focus on>"
}
```

**请求体（包含输出语言）：** [此处应填写包含输出语言的请求体格式](```json
{
  "content": "<user input>",
  "output_language": "ja"
}
```

直接将用户输入作为 `content` 参数传递，不得对其进行修改、解析或预处理。

**请求字段：**
| 字段                | 类型   | 是否必填 | 说明                                                                 |
|----------------------|--------|----------|-----------------------------------------------------------------------------|
| `content`            | string | 是      | 用户需要摘要的内容，原样传递，不得修改。             |
| `custominstructions`| string | 否       | 摘要的定制指令（例如：“重点关注方法论和关键发现”）。         |
| `output_language`    | string | 否       | 摘要输出的 ISO 639-1 语言代码（例如：“ja”、“es”）。默认为 “en”）。 |

**响应：** [此处应填写响应格式](```json
{
  "execution_id": "b7e2c1a4-93f1-4d2a-8e56-1a2b3c4d5e6f",
  "cached": false
}
```

| 字段          | 类型    | 说明                                                  |
|----------------|---------|--------------------------------------------------------------|
| `execution_id` | string  | 用于标识此请求的 UUID，用于后续结果查询。   |
| `cached`       | boolean | 如果结果已缓存且可立即获取，则设置为 `true`。        |

### 第二步：获取结果

使用第一步中的 `execution_id` 来获取摘要结果。有两种方法：
- **推荐方法：服务器发送事件（SSE）流**：[此处应填写相关代码](___CODE_BLOCK_7_)
  - 服务器会以 SSE 格式发送事件流，代理接收并逐步向用户展示内容。当摘要处理完成后，事件流会结束。
- **备用方法：JSON 轮询**：[此处应填写相关代码](___CODE_BLOCK_9_)
  - 如果代理不支持 SSE，可以使用此方法。请注意：在当前版本中，仅支持 SSE 方式。此部分将在支持轮询时更新。

如果代理运行环境不支持 SSE，可以使用 JSON 轮询方式：
- **请求头：** [此处应填写请求头信息](___CODE_BLOCK_10_)
- **轮询间隔：** 每 2–3 秒轮询一次，直到获取到结果。响应内容为包含最终摘要的 JSON 对象。

---

## 示例

### 示例 1：摘要一个 URL
用户请求：*“摘要这个链接：https://example.com/article-about-ai”*

**请求方法：** `POST /v1/summarize` [此处应填写请求路径](```json
{
  "content": "https://example.com/article-about-ai"
}
```

### 示例 2：摘要包含 URL 的文本
用户请求：*“你能帮我总结这个内容吗？我觉得这个链接很有趣：https://example.com/post/12345”*
**请求方法：** `POST /v1/summarize` [此处应填写请求路径](___CODE_BLOCK_12_)
> 请原样传递整个输入内容，不要提取其中的 URL。

### 示例 3：摘要纯文本
用户请求：*“总结这段文字：季度报告显示收入增长了 15%，主要得益于欧洲市场的扩张……”*
**请求方法：** `POST /v1/summarize` [此处应填写请求路径](```json
{
  "content": "The quarterly report indicates a 15% increase in revenue driven primarily by expansion into European markets..."
}
```

### 示例 4：摘要播客或视频
用户请求：*“摘要这个播客：https://www.youtube.com/watch?v=dQw4w9WgXcQ”*
**请求方法：** `POST /v1/summarize` [此处应填写请求路径](```json
{
  "content": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

### 示例 5：自定义指令
**如何使用 `custominstructions`：** 如果用户明确要求关注某些特定内容、强调某些部分或进行筛选，请将这些要求放入 `custominstructions` 中，并将剩余内容（URL 或文本）作为 `content` 传递。如果没有明确要求，只需将全部内容作为 `content` 传递给服务器。
用户请求：*“摘要这个链接：https://example.com/research-paper，但重点关注方法论和关键发现”*
**请求方法：** `POST /v1/summarize` [此处应填写请求路径](___CODE_BLOCK_15_

---

## 输出结果

- API 会返回服务器端生成的摘要。
- 摘要的长度和结构取决于输入内容及自定义指令。
- 请原样向用户展示摘要结果，除非用户另有要求，否则不要进一步压缩或重新格式化。

---

## 常见问题及解决方法

| 问题 | 原因 | 解决方案 |
|---|---|---|
| `401 Unauthorized` | 缺少或无效的 `x-api-key` 请求头。 | 确保 `DIZEST_API_KEY` 环境变量已设置，并使用有效的 API 密钥。请参考认证部分的设置步骤。 |
| `403 Forbidden` | API 密钥无访问权限。 | 确认该密钥属于已激活的账户。 |
| SSE 流无法连接 | 代理运行环境可能不支持 Server-Sent Events。 | 使用 `GET /v1/executions/<execution_id>/result` 进行轮询。 |
| 轮询无结果 | 摘要处理仍在进行中。 | 继续每 2–3 秒轮询一次。对于较长内容，请等待足够时间。 |
| 摘要为空或不符合预期 | 内容可能受到付费墙限制或无法访问。 | 请告知用户，不要尝试客户端解决方案——提取工作由服务器完成。 |