---
name: telnyx-ai-inference-ruby
description: >-
  Access Telnyx LLM inference APIs, embeddings, and AI analytics for call
  insights and summaries. This skill provides Ruby SDK examples.
metadata:
  author: telnyx
  product: ai-inference
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx AI 推理 - Ruby

## 安装

```bash
gem install telnyx
```

## 设置

```ruby
require "telnyx"

client = Telnyx::Client.new(
  api_key: ENV["TELNYX_API_KEY"], # This is the default and can be omitted
)
```

以下所有示例均假设 `client` 已按上述方式初始化。

## 列出对话记录

检索用户配置的所有 AI 对话记录。

`GET /ai/conversations`

```ruby
conversations = client.ai.conversations.list

puts(conversations)
```

## 创建对话记录

创建一个新的 AI 对话记录。

`POST /ai/conversations`

```ruby
conversation = client.ai.conversations.create

puts(conversation)
```

## 获取洞察模板组

获取所有洞察模板组。

`GET /ai/conversations/insight-groups`

```ruby
page = client.ai.conversations.insight_groups.retrieve_insight_groups

puts(page)
```

## 创建洞察模板组

创建一个新的洞察模板组。

`POST /ai/conversations/insight-groups` — 必需参数：`name`

```ruby
insight_template_group_detail = client.ai.conversations.insight_groups.insight_groups(name: "name")

puts(insight_template_group_detail)
```

## 获取洞察模板组

通过 ID 获取洞察模板组。

`GET /ai/conversations/insight-groups/{group_id}`

```ruby
insight_template_group_detail = client.ai.conversations.insight_groups.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(insight_template_group_detail)
```

## 更新洞察模板组

更新洞察模板组。

`PUT /ai/conversations/insight-groups/{group_id}`

```ruby
insight_template_group_detail = client.ai.conversations.insight_groups.update("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(insight_template_group_detail)
```

## 删除洞察模板组

通过 ID 删除洞察模板组。

`DELETE /ai/conversations/insight-groups/{group_id}`

```ruby
result = client.ai.conversations.insight_groups.delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(result)
```

## 将洞察模板分配给组

将某个洞察模板分配给指定的组。

`POST /ai/conversations/insight-groups/{group_id}/insights/{insight_id}/assign`

```ruby
result = client.ai.conversations.insight_groups.insights.assign(
  "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
  group_id: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"
)

puts(result)
```

## 从组中解除洞察模板的分配

从组中移除某个洞察模板。

`DELETE /ai/conversations/insight-groups/{group_id}/insights/{insight_id}/unassign`

```ruby
result = client.ai.conversations.insight_groups.insights.delete_unassign(
  "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
  group_id: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"
)

puts(result)
```

## 获取所有洞察模板

获取所有已创建的洞察模板。

`GET /ai/conversations/insights`

```ruby
page = client.ai.conversations.insights.list

puts(page)
```

## 创建新的洞察模板

创建一个新的洞察模板。

`POST /ai/conversations/insights` — 必需参数：`instructions`, `name`

```ruby
insight_template_detail = client.ai.conversations.insights.create(instructions: "instructions", name: "name")

puts(insight_template_detail)
```

## 获取洞察模板

通过 ID 获取特定的洞察模板。

`GET /ai/conversations/insights/{insight_id}`

```ruby
insight_template_detail = client.ai.conversations.insights.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(insight_template_detail)
```

## 更新洞察模板

更新现有的洞察模板。

`PUT /ai/conversations/insights/{insight_id}`

```ruby
insight_template_detail = client.ai.conversations.insights.update("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(insight_template_detail)
```

## 删除洞察模板

通过 ID 删除特定的洞察模板。

`DELETE /ai/conversations/insights/{insight_id}`

```ruby
result = client.ai.conversations.insights.delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(result)
```

## 获取对话记录

通过 ID 获取特定的 AI 对话记录。

`GET /ai/conversations/{conversation_id}`

```ruby
conversation = client.ai.conversations.retrieve("conversation_id")

puts(conversation)
```

## 更新对话元数据

更新指定对话记录的元数据。

`PUT /ai/conversations/{conversation_id}`

```ruby
conversation = client.ai.conversations.update("conversation_id")

puts(conversation)
```

## 删除对话记录

通过 ID 删除指定的对话记录。

`DELETE /ai/conversations/{conversation_id}`

```ruby
result = client.ai.conversations.delete("conversation_id")

puts(result)
```

## 获取对话记录的洞察结果

检索指定对话记录的所有洞察结果。

`GET /ai/conversations/{conversation_id}/conversations-insights`

```ruby
response = client.ai.conversations.retrieve_conversations_insights("conversation_id")

puts(response)
```

## 创建消息

向对话记录中添加新消息。

`POST /ai/conversations/{conversation_id}/message` — 必需参数：`role`

```ruby
result = client.ai.conversations.add_message("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e", role: "role")

puts(result)
```

## 获取对话记录中的消息

检索指定对话记录中的所有消息，包括助手执行的操作。

`GET /ai/conversations/{conversation_id}/messages`

```ruby
messages = client.ai.conversations.messages.list("conversation_id")

puts(messages)
```

## 根据状态获取任务

根据查询字符串，检索用户的所有任务（状态包括：`queued`, `processing`, `failed`, `success`, `partial_success`）。

`GET /ai/embeddings`

```ruby
embeddings = client.ai.embeddings.list

puts(embeddings)
```

## 嵌入文档

使用嵌入模型对 Telnyx 存储桶中的文档进行嵌入处理。

`POST /ai/embeddings` — 必需参数：`bucket_name`

```ruby
embedding_response = client.ai.embeddings.create(bucket_name: "bucket_name")

puts(embedding_response)
```

## 列出嵌入桶

获取用户所有的嵌入桶。

`GET /ai/embeddings/buckets`

```ruby
buckets = client.ai.embeddings.buckets.list

puts(buckets)
```

## 获取桶的文件级嵌入状态

获取指定用户桶中所有嵌入文件的状态信息。

`GET /ai/embeddings/buckets/{bucket_name}`

```ruby
bucket = client.ai.embeddings.buckets.retrieve("bucket_name")

puts(bucket)
```

## 禁用嵌入桶的 AI 功能

删除桶中的所有嵌入数据，并将其恢复为普通存储模式。

`DELETE /ai/embeddings/buckets/{bucket_name}`

```ruby
result = client.ai.embeddings.buckets.delete("bucket_name")

puts(result)
```

## 搜索文档

对 Telnyx 存储桶中的文档进行相似性搜索，返回与查询内容最相似的 `num_docs` 个文档片段。

`POST /ai/embeddings/similarity-search` — 必需参数：`bucket_name`, `query`

```ruby
response = client.ai.embeddings.similarity_search(bucket_name: "bucket_name", query: "query")

puts(response)
```

## 嵌入 URL 内容

从指定的 URL 嵌入网页内容（包括同一域名下的最多 5 层子页面）。

`POST /ai/embeddings/url` — 必需参数：`url`, `bucket_name`

```ruby
embedding_response = client.ai.embeddings.url(bucket_name: "bucket_name", url: "url")

puts(embedding_response)
```

## 获取嵌入任务的状态

检查当前嵌入任务的进度。

`GET /ai/embeddings/{task_id}`

```ruby
embedding = client.ai.embeddings.retrieve("task_id")

puts(embedding)
```

## 列出所有集群

获取所有已创建的集群信息。

`GET /ai/clusters`

```ruby
page = client.ai.clusters.list

puts(page)
```

## 计算新集群

启动后台任务，对 [嵌入存储桶](https://developers.telnyx.com/api-reference/embeddings/embed-documents) 中的数据进行聚类分析。

`POST /ai/clusters` — 必需参数：`bucket`

```ruby
response = client.ai.clusters.compute(bucket: "bucket")

puts(response)
```

## 获取集群信息

获取特定集群的详细信息。

`GET /ai/clusters/{task_id}`

```ruby
cluster = client.ai.clusters.retrieve("task_id")

puts(cluster)
```

## 删除集群

删除指定的集群。

`DELETE /ai/clusters/{task_id}`

```ruby
result = client.ai.clusters.delete("task_id")

puts(result)
```

## 获取集群可视化结果

获取指定集群的可视化信息。

`GET /ai/clusters/{task_id}/graph`

```ruby
response = client.ai.clusters.fetch_graph("task_id")

puts(response)
```

## 将语音转录为文本

将语音内容转录为文本。

`POST /ai/audio/transcriptions`

```ruby
response = client.ai.audio.transcribe(model: :"distil-whisper/distil-large-v2")

puts(response)
```

## 创建聊天完成结果

使用语言模型生成聊天完成结果。

`POST /ai/chat/completions` — 必需参数：`messages`

```ruby
response = client.ai.chat.create_completion(
  messages: [{content: "You are a friendly chatbot.", role: :system}, {content: "Hello, world!", role: :user}]
)

puts(response)
```

## 列出微调任务

检索用户创建的所有微调任务。

`GET /ai/fine_tuning/jobs`

```ruby
jobs = client.ai.fine_tuning.jobs.list

puts(jobs)
```

## 创建微调任务

创建一个新的微调任务。

`POST /ai/fine_tuning/jobs` — 必需参数：`model`, `training_file`

```ruby
fine_tuning_job = client.ai.fine_tuning.jobs.create(model: "model", training_file: "training_file")

puts(fine_tuning_job)
```

## 获取微调任务信息

通过 `job_id` 获取特定的微调任务信息。

`GET /ai/fine_tuning/jobs/{job_id}`

```ruby
fine_tuning_job = client.ai.fine_tuning.jobs.retrieve("job_id")

puts(fine_tuning_job)
```

## 取消微调任务

取消指定的微调任务。

`POST /ai/fine_tuning/jobs/{job_id}/cancel`

```ruby
fine_tuning_job = client.ai.fine_tuning.jobs.cancel("job_id")

puts(fine_tuning_job)
```

## 获取可用模型

此接口返回所有可用的开源模型和 OpenAI 模型。

`GET /ai/models`

```ruby
response = client.ai.retrieve_models

puts(response)
```

## 概述文件内容

生成文件内容的摘要。

`POST /ai/summarize` — 必需参数：`bucket`, `filename`

```ruby
response = client.ai.summarize(bucket: "bucket", filename: "filename")

puts(response)
```
```