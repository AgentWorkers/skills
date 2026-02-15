---
name: dizest-summarize
description: "使用 Dizest API 对长篇内容（如文章、播客、研究论文、PDF 文件、笔记等）进行总结，将您阅读的内容转化为结构化、可搜索的知识。"
metadata: {"openclaw":{"emoji":"📝","requires":{"env":["DIZEST_API_KEY"]}}}
---

# Dizest 摘要功能

Dizest 能够将长篇内容进行总结，并将其转化为结构化、可搜索的知识。该功能基于 [Dizest: AI 摘要器](https://www.dizest.ai) 提供的 API 实现，该 API 可在 [App Store](https://apps.apple.com/app/id6752311120) 和 [Google Play](https://play.google.com/store/apps/details?id=com.ideas116.dizest) 上下载。

**基础 URL:** `https://api.116ideas.com`

如需了解有关该产品的更多信息，请访问 [www.dizest.ai](https://www.dizest.ai)。

---

## 适用场景

当用户需要以下操作时，可以使用此功能：
- 摘要研究论文或学术内容以提取关键发现
- 摘要来自 YouTube 等平台的长篇播客、访谈或视频内容
- 处理文章、博客文章或网页内容（通过 URL）
- 摘要 PDF 文件、报告、市场分析报告或商业文档
- 摘要纯文本（如笔记、文字记录或粘贴的内容）
- 根据特定要求进行摘要（例如：“重点关注方法论和关键发现”）

---

## 代理行为规范

**代理必须作为薄客户端（thin client）进行操作**。具体要求如下：
- **禁止** 从用户输入中提取、解析或分类 URL。
- **禁止** 判断输入内容是 URL、纯文本还是包含 URL 的文本。
- **禁止** 在调用 API 之前获取、抓取或预处理任何内容。
- **禁止** 处理需要付费的内容或尝试绕过付费限制的策略。

所有内容分析、URL 检测、提取、付费限制处理以及执行逻辑均在 **服务器端** 完成。代理的唯一任务是按原样将用户输入传递给 API。

---

## 认证

所有请求都必须包含 `x-api-key` 标头。该键的值应来自 `DIZEST_API_KEY` 环境变量。只有付费用户才能使用有效的 API 密钥。

```
x-api-key: $DIZEST_API_KEY
```

如果 `DIZEST_API_KEY` 环境变量未设置且用户未提供 API 密钥，请提示他们在 [dizest.ai/api/keys](http://dizest.ai/api/keys) 注册账户（需要付费）。

---

## API 流程

整个流程分为两个步骤：**创建执行请求**，然后 **获取结果**。

### 第一步：创建执行请求

**端点：**  
```
POST https://api.116ideas.com/v1/summarize
```

**请求头：**  
```
Content-Type: application/json
x-api-key: $DIZEST_API_KEY
```

**请求体（基本格式）：**  
```json
{
  "content": "<user input>"
}
```

**请求体（包含自定义指令）：**  
```json
{
  "content": "<user input>",
  "custom_instructions": "<what to focus on>"
}
```

**请求体（包含输出语言）：**  
```json
{
  "content": "<user input>",
  "output_language": "ja"
}
```

请直接将用户输入的内容作为 `content` 参数传递，切勿对其进行修改、解析或预处理。

**请求字段：**
| 字段                | 类型     | 是否必填 | 说明                                                                 |
|----------------------|--------|----------|-----------------------------------------------------------------------------|
| `content`            | string   | 是       | 用户需要摘要的内容，保持原样传递。                                                                 |
| `custominstructions` | string   | 可选     | 摘要时的自定义指令（例如：“重点关注方法论和关键发现”）。                                                                 |
| `output_language`    | string   | 可选     | 摘要输出的 ISO 639-1 语言代码（例如：“ja”、“es”）。默认为 “en”。                                                                 |

**响应：**  
```json
{
  "execution_id": "b7e2c1a4-93f1-4d2a-8e56-1a2b3c4d5e6f",
  "cached": false
}
```

| 字段          | 类型     | 说明                                                                 |
|----------------|---------|--------------------------------------------------------------|
| `execution_id` | string   | 用于标识此次执行的唯一 ID，用于后续结果查询。                                                                 |
| `cached`       | boolean | 如果结果已缓存，则值为 `true`，可立即获取。                                                                 |

### 第二步：获取结果

使用第一步中获得的 `execution_id` 来获取摘要结果。有两种获取结果的方法：

#### 推荐方式：服务器发送事件（Server-Sent Events, SSE）

**请求头：**  
```
GET https://api.116ideas.com/v1/executions/<execution_id>/events
```

服务器会以 SSE 格式发送事件流。收到事件后逐步向用户展示内容。当执行完成后，事件流会停止。

#### 备选方式：JSON 轮询

> **注意：** JSON 轮询功能目前尚未实现。在版本 1 中，仅支持 SSE 方式。此部分将在轮询功能可用时更新。

如果代理的运行环境不支持 SSE，可以使用 JSON 轮询方式：

**请求头：**  
```
GET https://api.116ideas.com/v1/executions/<execution_id>/result
```

以适当的间隔（例如每 2–3 秒）轮询该接口，直到获取到结果。响应结果是一个包含最终摘要的 JSON 对象。

---

## 示例

### 示例 1：摘要一个 URL

用户请求：*“请摘要这个链接：https://example.com/article-about-ai”*

**请求方法：**  
`POST /v1/summarize`  
```json
{
  "content": "https://example.com/article-about-ai"
}
```

### 示例 2：摘要包含 URL 的文本

用户请求：*“你能帮我摘要一下这个内容吗？我觉得很有趣：https://example.com/post/12345”*

**请求方法：**  
`POST /v1/summarize`  
```json
{
  "content": "Can you summarize this for me? I found it interesting: https://example.com/post/12345"
}
```

> 请直接传递全部输入内容，不要提取其中的 URL。

### 示例 3：摘要纯文本

用户请求：*“请摘要这段文字：季度报告显示收入增长了 15%，主要得益于欧洲市场的拓展……”*

**请求方法：**  
`POST /v1/summarize`  
```json
{
  "content": "The quarterly report indicates a 15% increase in revenue driven primarily by expansion into European markets..."
}
```

### 示例 4：摘要播客或视频

用户请求：*“请摘要这个播客：https://www.youtube.com/watch?v=dQw4w9WgXcQ”*

**请求方法：**  
`POST /v1/summarize`  
```json
{
  "content": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

### 示例 5：自定义指令

**使用 `custominstructions` 的示例：** 如果用户明确要求关注某些特定内容，请将其写入 `custominstructions`，并将剩余内容（URL 或文本）作为 `content` 传递。如果没有特别要求，只需将全部内容作为 `content` 传递给服务器。

用户请求：*“请摘要这个链接：https://example.com/research-paper，但重点关注方法论和关键发现”*

**请求方法：**  
`POST /v1/summarize`  
```json
{
  "content": "https://example.com/research-paper",
  "custom_instructions": "Focus on the methodology and key findings"
}
```

---

## 输出结果

- API 会返回服务器端生成的摘要内容。
- 摘要的长度和结构取决于输入内容及自定义指令。
- 请直接将摘要内容展示给用户，除非用户另有要求，否则不要进一步压缩或重新格式化。

---

## 常见问题及解决方法

| 问题                | 原因                | 解决方案                                                                 |
|------------------|------------------|-------------------------------------------------------------------------|
| `401 Unauthorized`     | 缺少或无效的 `x-api-key` 标头。   | 确保 `DIZEST_API_KEY` 环境变量已设置，并使用有效的 API 密钥。仅付费用户可使用有效密钥。 |
| `403 Forbidden`     | API 密钥无权限访问。       | 确认该密钥属于付费账户。                                                                 |
| SSE 流无法连接          | 代理运行环境可能不支持 SSE。       | 使用 `GET /v1/executions/<execution_id>/result` 进行轮询。                                                                 |
| 轮询无结果           | 摘要处理中。            | 继续每隔 2–3 秒轮询一次。对于较长内容，请等待足够时间。                                                                 |
| 摘要为空或格式异常       | 内容可能受到付费限制或无法访问。     | 通知用户，切勿尝试客户端处理，因为提取工作由服务器完成。                                                                 |