---
name: telnyx-ai-inference-javascript
description: >-
  Access Telnyx LLM inference APIs, embeddings, and AI analytics for call
  insights and summaries. This skill provides JavaScript SDK examples.
metadata:
  author: telnyx
  product: ai-inference
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx AI 推理 - JavaScript

## 安装

```bash
npm install telnyx
```

## 设置

```javascript
import Telnyx from 'telnyx';

const client = new Telnyx({
  apiKey: process.env['TELNYX_API_KEY'], // This is the default and can be omitted
});
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 列出对话记录

检索用户配置的所有 AI 对话记录。

`GET /ai/conversations`

```javascript
const conversations = await client.ai.conversations.list();

console.log(conversations.data);
```

## 创建对话记录

创建一个新的 AI 对话记录。

`POST /ai/conversations`

```javascript
const conversation = await client.ai.conversations.create();

console.log(conversation.id);
```

## 获取洞察模板组

获取所有洞察模板组。

`GET /ai/conversations/insight-groups`

```javascript
// Automatically fetches more pages as needed.
for await (const insightTemplateGroup of client.ai.conversations.insightGroups.retrieveInsightGroups()) {
  console.log(insightTemplateGroup.id);
}
```

## 创建洞察模板组

创建一个新的洞察模板组。

`POST /ai/conversations/insight-groups` — 必需参数：`name`

```javascript
const insightTemplateGroupDetail = await client.ai.conversations.insightGroups.insightGroups({
  name: 'name',
});

console.log(insightTemplateGroupDetail.data);
```

## 获取洞察模板组

通过 ID 获取洞察模板组。

`GET /ai/conversations/insight-groups/{group_id}`

```javascript
const insightTemplateGroupDetail = await client.ai.conversations.insightGroups.retrieve(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(insightTemplateGroupDetail.data);
```

## 更新洞察模板组

更新洞察模板组。

`PUT /ai/conversations/insight-groups/{group_id}`

```javascript
const insightTemplateGroupDetail = await client.ai.conversations.insightGroups.update(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(insightTemplateGroupDetail.data);
```

## 删除洞察模板组

通过 ID 删除洞察模板组。

`DELETE /ai/conversations/insight-groups/{group_id}`

```javascript
await client.ai.conversations.insightGroups.delete('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');
```

## 将洞察模板分配给组

将某个洞察模板分配给指定的组。

`POST /ai/conversations/insight-groups/{group_id}/insights/{insight_id}/assign`

```javascript
await client.ai.conversations.insightGroups.insights.assign(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
  { group_id: '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e' },
);
```

## 从组中解除洞察模板的分配

从组中移除某个洞察模板。

`DELETE /ai/conversations/insight-groups/{group_id}/insights/{insight_id}/unassign`

```javascript
await client.ai.conversations.insightGroups.insights.deleteUnassign(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
  { group_id: '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e' },
);
```

## 获取所有洞察模板

获取所有洞察模板。

`GET /ai/conversations/insights`

```javascript
// Automatically fetches more pages as needed.
for await (const insightTemplate of client.ai.conversations.insights.list()) {
  console.log(insightTemplate.id);
}
```

## 创建洞察模板

创建一个新的洞察模板。

`POST /ai/conversations/insights` — 必需参数：`instructions`, `name`

```javascript
const insightTemplateDetail = await client.ai.conversations.insights.create({
  instructions: 'instructions',
  name: 'name',
});

console.log(insightTemplateDetail.data);
```

## 获取洞察模板

通过 ID 获取某个洞察模板。

`GET /ai/conversations/insights/{insight_id}`

```javascript
const insightTemplateDetail = await client.ai.conversations.insights.retrieve(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(insightTemplateDetail.data);
```

## 更新洞察模板

更新某个洞察模板。

`PUT /ai/conversations/insights/{insight_id}`

```javascript
const insightTemplateDetail = await client.ai.conversations.insights.update(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(insightTemplateDetail.data);
```

## 删除洞察模板

通过 ID 删除某个洞察模板。

`DELETE /ai/conversations/insights/{insight_id}`

```javascript
await client.ai.conversations.insights.delete('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');
```

## 获取对话记录

通过 ID 获取特定的 AI 对话记录。

`GET /ai/conversations/{conversation_id}`

```javascript
const conversation = await client.ai.conversations.retrieve('conversation_id');

console.log(conversation.data);
```

## 更新对话元数据

更新特定对话记录的元数据。

`PUT /ai/conversations/{conversation_id}`

```javascript
const conversation = await client.ai.conversations.update('conversation_id');

console.log(conversation.data);
```

## 删除对话记录

通过 ID 删除特定的对话记录。

`DELETE /ai/conversations/{conversation_id}`

```javascript
await client.ai.conversations.delete('conversation_id');
```

## 获取对话记录的洞察结果

检索特定对话记录的洞察结果。

`GET /ai/conversations/{conversation_id}/conversations-insights`

```javascript
const response = await client.ai.conversations.retrieveConversationsInsights('conversation_id');

console.log(response.data);
```

## 创建消息

向对话记录中添加新消息。

`POST /ai/conversations/{conversation_id}/message` — 必需参数：`role`

```javascript
await client.ai.conversations.addMessage('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e', { role: 'role' });
```

## 获取对话记录中的消息

检索特定对话记录中的所有消息，包括助手执行的工具调用。

`GET /ai/conversations/{conversation_id}/messages`

```javascript
const messages = await client.ai.conversations.messages.list('conversation_id');

console.log(messages.data);
```

## 根据状态获取任务

根据查询字符串，检索用户的所有任务（状态为 `queued`, `processing`, `failed`, `success` 或 `partial_success`）。

`GET /ai/embeddings`

```javascript
const embeddings = await client.ai.embeddings.list();

console.log(embeddings.data);
```

## 嵌入文档

使用嵌入模型对 Telnyx 存储桶中的文档进行嵌入处理。

`POST /ai/embeddings` — 必需参数：`bucket_name`

```javascript
const embeddingResponse = await client.ai.embeddings.create({ bucket_name: 'bucket_name' });

console.log(embeddingResponse.data);
```

## 列出嵌入桶

获取用户所有的嵌入桶。

`GET /ai/embeddings/buckets`

```javascript
const buckets = await client.ai.embeddings.buckets.list();

console.log(buckets.data);
```

## 获取桶的文件级嵌入状态

获取指定用户桶中的所有嵌入文件及其处理状态。

`GET /ai/embeddings/buckets/{bucket_name}`

```javascript
const bucket = await client.ai.embeddings.buckets.retrieve('bucket_name');

console.log(bucket.data);
```

## 禁用嵌入桶的 AI 功能

删除整个桶的嵌入数据，并将其恢复为普通存储模式。

`DELETE /ai/embeddings/buckets/{bucket_name}`

```javascript
await client.ai.embeddings.buckets.delete('bucket_name');
```

## 搜索文档

对 Telnyx 存储桶中的文档进行相似性搜索，返回与查询内容最相似的 `num_docs` 个文档片段。

`POST /ai/embeddings/similarity-search` — 必需参数：`bucket_name`, `query`

```javascript
const response = await client.ai.embeddings.similaritySearch({
  bucket_name: 'bucket_name',
  query: 'query',
});

console.log(response.data);
```

## 嵌入 URL 内容

从指定的 URL 嵌入网页内容，包括同一域名下的最多 5 层子页面。

`POST /ai/embeddings/url` — 必需参数：`url`, `bucket_name`

```javascript
const embeddingResponse = await client.ai.embeddings.url({
  bucket_name: 'bucket_name',
  url: 'url',
});

console.log(embeddingResponse.data);
```

## 获取嵌入任务的状态

检查当前嵌入任务的状态。

`GET /ai/embeddings/{task_id}`

```javascript
const embedding = await client.ai.embeddings.retrieve('task_id');

console.log(embedding.data);
```

## 列出所有集群

获取所有集群信息。

`GET /ai/clusters`

```javascript
// Automatically fetches more pages as needed.
for await (const clusterListResponse of client.ai.clusters.list()) {
  console.log(clusterListResponse.task_id);
}
```

## 计算新集群

启动后台任务，对 [嵌入存储桶](https://developers.telnyx.com/api-reference/embeddings/embed-documents) 中的数据进行聚类分析。

`POST /ai/clusters` — 必需参数：`bucket`

```javascript
const response = await client.ai.clusters.compute({ bucket: 'bucket' });

console.log(response.data);
```

## 获取集群信息

获取特定集群的详细信息。

`GET /ai/clusters/{task_id}`

```javascript
const cluster = await client.ai.clusters.retrieve('task_id');

console.log(cluster.data);
```

## 删除集群

删除指定的集群。

`DELETE /ai/clusters/{task_id}`

```javascript
await client.ai.clusters.delete('task_id');
```

## 获取集群可视化信息

获取特定集群的可视化图表。

`GET /ai/clusters/{task_id}/graph`

```javascript
const response = await client.ai.clusters.fetchGraph('task_id');

console.log(response);

const content = await response.blob();
console.log(content);
```

## 将语音转换为文本

将语音转换为文本。

`POST /ai/audio/transcriptions`

```javascript
const response = await client.ai.audio.transcribe({ model: 'distil-whisper/distil-large-v2' });

console.log(response.text);
```

## 创建聊天完成结果

使用语言模型生成聊天完成结果。

`POST /ai/chat/completions` — 必需参数：`messages`

```javascript
const response = await client.ai.chat.createCompletion({
  messages: [
    { role: 'system', content: 'You are a friendly chatbot.' },
    { role: 'user', content: 'Hello, world!' },
  ],
});

console.log(response);
```

## 列出微调作业

检索用户创建的所有微调作业。

`GET /ai/fine_tuning/jobs`

```javascript
const jobs = await client.ai.fineTuning.jobs.list();

console.log(jobs.data);
```

## 创建微调作业

创建一个新的微调作业。

`POST /ai/fine_tuning/jobs` — 必需参数：`model`, `training_file`

```javascript
const fineTuningJob = await client.ai.fineTuning.jobs.create({
  model: 'model',
  training_file: 'training_file',
});

console.log(fineTuningJob.id);
```

## 获取微调作业信息

通过 `job_id` 获取特定的微调作业信息。

`GET /ai/fine_tuning/jobs/{job_id}`

```javascript
const fineTuningJob = await client.ai.fineTuning.jobs.retrieve('job_id');

console.log(fineTuningJob.id);
```

## 取消微调作业

取消指定的微调作业。

`POST /ai/fine_tuning/jobs/{job_id}/cancel`

```javascript
const fineTuningJob = await client.ai.fineTuning.jobs.cancel('job_id');

console.log(fineTuningJob.id);
```

## 获取可用模型

此接口返回所有可用的开源模型和 OpenAI 模型。

`GET /ai/models`

```javascript
const response = await client.ai.retrieveModels();

console.log(response.data);
```

## 概述文件内容

生成文件内容的摘要。

`POST /ai/summarize` — 必需参数：`bucket`, `filename`

```javascript
const response = await client.ai.summarize({ bucket: 'bucket', filename: 'filename' });

console.log(response.data);
```