---
name: telnyx-ai-inference-python
description: >-
  Access Telnyx LLM inference APIs, embeddings, and AI analytics for call
  insights and summaries. This skill provides Python SDK examples.
metadata:
  author: telnyx
  product: ai-inference
  language: python
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx AI 推理 - Python

## 安装

```bash
pip install telnyx
```

## 设置

```python
import os
from telnyx import Telnyx

client = Telnyx(
    api_key=os.environ.get("TELNYX_API_KEY"),  # This is the default and can be omitted
)
```

以下所有示例均假设 `client` 已按上述方式初始化。

## 列出对话记录

检索用户配置的所有 AI 对话记录。

`GET /ai/conversations`

```python
conversations = client.ai.conversations.list()
print(conversations.data)
```

## 创建对话记录

创建一个新的 AI 对话记录。

`POST /ai/conversations`

```python
conversation = client.ai.conversations.create()
print(conversation.id)
```

## 获取洞察模板组

获取所有洞察模板组。

`GET /ai/conversations/insight-groups`

```python
page = client.ai.conversations.insight_groups.retrieve_insight_groups()
page = page.data[0]
print(page.id)
```

## 创建洞察模板组

创建一个新的洞察模板组。

`POST /ai/conversations/insight-groups` — 必需参数：`name`

```python
insight_template_group_detail = client.ai.conversations.insight_groups.insight_groups(
    name="name",
)
print(insight_template_group_detail.data)
```

## 获取洞察模板组

通过 ID 获取洞察模板组。

`GET /ai/conversations/insight-groups/{group_id}`

```python
insight_template_group_detail = client.ai.conversations.insight_groups.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(insight_template_group_detail.data)
```

## 更新洞察模板组

更新洞察模板组。

`PUT /ai/conversations/insight-groups/{group_id}`

```python
insight_template_group_detail = client.ai.conversations.insight_groups.update(
    group_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(insight_template_group_detail.data)
```

## 删除洞察模板组

通过 ID 删除洞察模板组。

`DELETE /ai/conversations/insight-groups/{group_id}`

```python
client.ai.conversations.insight_groups.delete(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
```

## 将洞察模板分配给组

将某个洞察模板分配给一个组。

`POST /ai/conversations/insight-groups/{group_id}/insights/{insight_id}/assign`

```python
client.ai.conversations.insight_groups.insights.assign(
    insight_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    group_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
```

## 从组中解除洞察模板的分配

从组中移除某个洞察模板。

`DELETE /ai/conversations/insight-groups/{group_id}/insights/{insight_id}/unassign`

```python
client.ai.conversations.insight_groups.insights.delete_unassign(
    insight_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    group_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
```

## 获取洞察模板

获取所有洞察模板。

`GET /ai/conversations/insights`

```python
page = client.ai.conversations.insights.list()
page = page.data[0]
print(page.id)
```

## 创建洞察模板

创建一个新的洞察模板。

`POST /ai/conversations/insights` — 必需参数：`instructions`, `name`

```python
insight_template_detail = client.ai.conversations.insights.create(
    instructions="instructions",
    name="name",
)
print(insight_template_detail.data)
```

## 获取洞察模板

通过 ID 获取某个洞察模板。

`GET /ai/conversations/insights/{insight_id}`

```python
insight_template_detail = client.ai.conversations.insights.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(insight_template_detail.data)
```

## 更新洞察模板

更新某个洞察模板。

`PUT /ai/conversations/insights/{insight_id}`

```python
insight_template_detail = client.ai.conversations.insights.update(
    insight_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(insight_template_detail.data)
```

## 删除洞察模板

通过 ID 删除某个洞察模板。

`DELETE /ai/conversations/insights/{insight_id}`

```python
client.ai.conversations.insights.delete(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
```

## 获取对话记录

通过 ID 获取特定的 AI 对话记录。

`GET /ai/conversations/{conversation_id}`

```python
conversation = client.ai.conversations.retrieve(
    "conversation_id",
)
print(conversation.data)
```

## 更新对话元数据

更新特定对话记录的元数据。

`PUT /ai/conversations/{conversation_id}`

```python
conversation = client.ai.conversations.update(
    conversation_id="conversation_id",
)
print(conversation.data)
```

## 删除对话记录

通过 ID 删除特定的对话记录。

`DELETE /ai/conversations/{conversation_id}`

```python
client.ai.conversations.delete(
    "conversation_id",
)
```

## 获取对话记录的洞察信息

检索特定对话记录的洞察信息。

`GET /ai/conversations/{conversation_id}/conversations-insights`

```python
response = client.ai.conversations.retrieve_conversations_insights(
    "conversation_id",
)
print(response.data)
```

## 创建消息

向对话记录中添加新消息。

`POST /ai/conversations/{conversation_id}/message` — 必需参数：`role`

```python
client.ai.conversations.add_message(
    conversation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    role="role",
)
```

## 获取对话记录中的消息

检索特定对话记录中的所有消息，包括助手执行的操作。

`GET /ai/conversations/{conversation_id}/messages`

```python
messages = client.ai.conversations.messages.list(
    "conversation_id",
)
print(messages.data)
```

## 根据状态获取任务

根据查询字符串，检索用户的所有任务（状态包括：`queued`, `processing`, `failed`, `success`, `partial_success`）。

`GET /ai/embeddings`

```python
embeddings = client.ai.embeddings.list()
print(embeddings.data)
```

## 嵌入文档

使用嵌入模型对 Telnyx 存储桶中的文档进行嵌入处理。

`POST /ai/embeddings` — 必需参数：`bucket_name`

```python
embedding_response = client.ai.embeddings.create(
    bucket_name="bucket_name",
)
print(embedding_response.data)
```

## 列出嵌入桶

获取用户的所有嵌入桶。

`GET /ai/embeddings/buckets`

```python
buckets = client.ai.embeddings.buckets.list()
print(buckets.data)
```

## 获取桶的文件级嵌入状态

获取指定用户桶中的所有嵌入文件及其处理状态。

`GET /ai/embeddings/buckets/{bucket_name}`

```python
bucket = client.ai.embeddings.buckets.retrieve(
    "bucket_name",
)
print(bucket.data)
```

## 禁用嵌入桶的 AI 功能

删除整个桶的嵌入数据，并将其恢复为普通存储模式。

`DELETE /ai/embeddings/buckets/{bucket_name}`

```python
client.ai.embeddings.buckets.delete(
    "bucket_name",
)
```

## 搜索文档

对 Telnyx 存储桶中的文档进行相似性搜索，返回与查询内容最相似的 `num_docs` 个文档片段。

`POST /ai/embeddings/similarity-search` — 必需参数：`bucket_name`, `query`

```python
response = client.ai.embeddings.similarity_search(
    bucket_name="bucket_name",
    query="query",
)
print(response.data)
```

## 嵌入 URL 内容

从指定的 URL 嵌入网页内容（包括同一域名下的最多 5 层子页面）。

`POST /ai/embeddings/url` — 必需参数：`url`, `bucket_name`

```python
embedding_response = client.ai.embeddings.url(
    bucket_name="bucket_name",
    url="url",
)
print(embedding_response.data)
```

## 获取嵌入任务的状态

检查当前嵌入任务的状态。

`GET /ai/embeddings/{task_id}`

```python
embedding = client.ai.embeddings.retrieve(
    "task_id",
)
print(embedding.data)
```

## 列出所有集群

获取所有集群信息。

`GET /ai/clusters`

```python
page = client.ai.clusters.list()
page = page.data[0]
print(page.task_id)
```

## 计算新集群

启动后台任务，对 [嵌入存储桶](https://developers.telnyx.com/api-reference/embeddings/embed-documents) 中的数据进行聚类分析。

`POST /ai/clusters` — 必需参数：`bucket`

```python
response = client.ai.clusters.compute(
    bucket="bucket",
)
print(response.data)
```

## 获取集群信息

获取某个集群的详细信息。

`GET /ai/clusters/{task_id}`

```python
cluster = client.ai.clusters.retrieve(
    task_id="task_id",
)
print(cluster.data)
```

## 删除集群

删除某个集群。

`DELETE /ai/clusters/{task_id}`

```python
client.ai.clusters.delete(
    "task_id",
)
```

## 获取集群可视化信息

获取某个集群的可视化图表。

`GET /ai/clusters/{task_id}/graph`

```python
response = client.ai.clusters.fetch_graph(
    task_id="task_id",
)
print(response)
content = response.read()
print(content)
```

## 将语音转录为文本

将语音内容转录为文本。

`POST /ai/audio/transcriptions`

```python
response = client.ai.audio.transcribe(
    model="distil-whisper/distil-large-v2",
)
print(response.text)
```

## 创建聊天完成结果

使用语言模型生成聊天完成结果。

`POST /ai/chat/completions` — 必需参数：`messages`

```python
response = client.ai.chat.create_completion(
    messages=[{
        "role": "system",
        "content": "You are a friendly chatbot.",
    }, {
        "role": "user",
        "content": "Hello, world!",
    }],
)
print(response)
```

## 列出微调任务

检索用户创建的所有微调任务。

`GET /ai/fine_tuning/jobs`

```python
jobs = client.ai.fine_tuning.jobs.list()
print(jobs.data)
```

## 创建微调任务

创建一个新的微调任务。

`POST /ai/fine_tuning/jobs` — 必需参数：`model`, `training_file`

```python
fine_tuning_job = client.ai.fine_tuning.jobs.create(
    model="model",
    training_file="training_file",
)
print(fine_tuning_job.id)
```

## 获取微调任务信息

通过 `job_id` 获取某个微调任务的详细信息。

`GET /ai/fine_tuning/jobs/{job_id}`

```python
fine_tuning_job = client.ai.fine_tuning.jobs.retrieve(
    "job_id",
)
print(fine_tuning_job.id)
```

## 取消微调任务

取消某个微调任务。

`POST /ai/fine_tuning/jobs/{job_id}/cancel`

```python
fine_tuning_job = client.ai.fine_tuning.jobs.cancel(
    "job_id",
)
print(fine_tuning_job.id)
```

## 获取可用模型

此接口返回可用的开源模型和 OpenAI 模型列表。

`GET /ai/models`

```python
response = client.ai.retrieve_models()
print(response.data)
```

## 概述文件内容

生成文件的摘要。

`POST /ai/summarize` — 必需参数：`bucket`, `filename`

```python
response = client.ai.summarize(
    bucket="bucket",
    filename="filename",
)
print(response.data)
```
```