---
name: telnyx-ai-inference-java
description: >-
  Access Telnyx LLM inference APIs, embeddings, and AI analytics for call
  insights and summaries. This skill provides Java SDK examples.
metadata:
  author: telnyx
  product: ai-inference
  language: java
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx AI 推理 - Java

## 安装

```text
// See https://github.com/team-telnyx/telnyx-java for Maven/Gradle setup
```

## 设置

```java
import com.telnyx.sdk.client.TelnyxClient;
import com.telnyx.sdk.client.okhttp.TelnyxOkHttpClient;

TelnyxClient client = TelnyxOkHttpClient.fromEnv();
```

以下所有示例均假设 `client` 已按上述方式初始化。

## 列出对话记录

检索用户配置的所有 AI 对话记录。

`GET /ai/conversations`

```java
import com.telnyx.sdk.models.ai.conversations.ConversationListParams;
import com.telnyx.sdk.models.ai.conversations.ConversationListResponse;

ConversationListResponse conversations = client.ai().conversations().list();
```

## 创建对话记录

创建一个新的 AI 对话记录。

`POST /ai/conversations`

```java
import com.telnyx.sdk.models.ai.conversations.Conversation;
import com.telnyx.sdk.models.ai.conversations.ConversationCreateParams;

Conversation conversation = client.ai().conversations().create();
```

## 获取洞察模板组

获取所有洞察模板组。

`GET /ai/conversations/insight-groups`

```java
import com.telnyx.sdk.models.ai.conversations.insightgroups.InsightGroupRetrieveInsightGroupsPage;
import com.telnyx.sdk.models.ai.conversations.insightgroups.InsightGroupRetrieveInsightGroupsParams;

InsightGroupRetrieveInsightGroupsPage page = client.ai().conversations().insightGroups().retrieveInsightGroups();
```

## 创建洞察模板组

创建一个新的洞察模板组。

`POST /ai/conversations/insight-groups` — 必需参数：`name`

```java
import com.telnyx.sdk.models.ai.conversations.insightgroups.InsightGroupInsightGroupsParams;
import com.telnyx.sdk.models.ai.conversations.insightgroups.InsightTemplateGroupDetail;

InsightGroupInsightGroupsParams params = InsightGroupInsightGroupsParams.builder()
    .name("name")
    .build();
InsightTemplateGroupDetail insightTemplateGroupDetail = client.ai().conversations().insightGroups().insightGroups(params);
```

## 获取洞察模板组

通过 ID 获取洞察模板组。

`GET /ai/conversations/insight-groups/{group_id}`

```java
import com.telnyx.sdk.models.ai.conversations.insightgroups.InsightGroupRetrieveParams;
import com.telnyx.sdk.models.ai.conversations.insightgroups.InsightTemplateGroupDetail;

InsightTemplateGroupDetail insightTemplateGroupDetail = client.ai().conversations().insightGroups().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 更新洞察模板组

更新洞察模板组。

`PUT /ai/conversations/insight-groups/{group_id}`

```java
import com.telnyx.sdk.models.ai.conversations.insightgroups.InsightGroupUpdateParams;
import com.telnyx.sdk.models.ai.conversations.insightgroups.InsightTemplateGroupDetail;

InsightTemplateGroupDetail insightTemplateGroupDetail = client.ai().conversations().insightGroups().update("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 删除洞察模板组

通过 ID 删除洞察模板组。

`DELETE /ai/conversations/insight-groups/{group_id}`

```java
import com.telnyx.sdk.models.ai.conversations.insightgroups.InsightGroupDeleteParams;

client.ai().conversations().insightGroups().delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 将洞察模板分配给组

将某个洞察模板分配给指定的组。

`POST /ai/conversations/insight-groups/{group_id}/insights/{insight_id}/assign`

```java
import com.telnyx.sdk.models.ai.conversations.insightgroups.insights.InsightAssignParams;

InsightAssignParams params = InsightAssignParams.builder()
    .groupId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .insightId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .build();
client.ai().conversations().insightGroups().insights().assign(params);
```

## 从组中解除洞察模板的分配

从组中移除某个洞察模板。

`DELETE /ai/conversations/insight-groups/{group_id}/insights/{insight_id}/unassign`

```java
import com.telnyx.sdk.models.ai.conversations.insightgroups.insights.InsightDeleteUnassignParams;

InsightDeleteUnassignParams params = InsightDeleteUnassignParams.builder()
    .groupId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .insightId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .build();
client.ai().conversations().insightGroups().insights().deleteUnassign(params);
```

## 获取所有洞察模板

获取所有可用的洞察模板。

`GET /ai/conversations/insights`

```java
import com.telnyx.sdk.models.ai.conversations.insights.InsightListPage;
import com.telnyx.sdk.models.ai.conversations.insights.InsightListParams;

InsightListPage page = client.ai().conversations().insights().list();
```

## 创建洞察模板

创建一个新的洞察模板。

`POST /ai/conversations/insights` — 必需参数：`instructions`, `name`

```java
import com.telnyx.sdk.models.ai.conversations.insights.InsightCreateParams;
import com.telnyx.sdk.models.ai.conversations.insights.InsightTemplateDetail;

InsightCreateParams params = InsightCreateParams.builder()
    .instructions("instructions")
    .name("name")
    .build();
InsightTemplateDetail insightTemplateDetail = client.ai().conversations().insights().create(params);
```

## 获取洞察模板

通过 ID 获取特定的洞察模板。

`GET /ai/conversations/insights/{insight_id}`

```java
import com.telnyx.sdk.models.ai.conversations.insights.InsightRetrieveParams;
import com.telnyx.sdk.models.ai.conversations.insights.InsightTemplateDetail;

InsightTemplateDetail insightTemplateDetail = client.ai().conversations().insights().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 更新洞察模板

更新现有的洞察模板。

`PUT /ai/conversations/insights/{insight_id}`

```java
import com.telnyx.sdk.models.ai.conversations.insights.InsightTemplateDetail;
import com.telnyx.sdk.models.ai.conversations.insights.InsightUpdateParams;

InsightTemplateDetail insightTemplateDetail = client.ai().conversations().insights().update("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 删除洞察模板

通过 ID 删除特定的洞察模板。

`DELETE /ai/conversations/insights/{insight_id}`

```java
import com.telnyx.sdk.models.ai.conversations.insights.InsightDeleteParams;

client.ai().conversations().insights().delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 获取对话记录

通过 ID 获取特定的 AI 对话记录。

`GET /ai/conversations/{conversation_id}`

```java
import com.telnyx.sdk.models.ai.conversations.ConversationRetrieveParams;
import com.telnyx.sdk.models.ai.conversations.ConversationRetrieveResponse;

ConversationRetrieveResponse conversation = client.ai().conversations().retrieve("conversation_id");
```

## 更新对话元数据

更新特定对话记录的元数据。

`PUT /ai/conversations/{conversation_id}`

```java
import com.telnyx.sdk.models.ai.conversations.ConversationUpdateParams;
import com.telnyx.sdk.models.ai.conversations.ConversationUpdateResponse;

ConversationUpdateResponse conversation = client.ai().conversations().update("conversation_id");
```

## 删除对话记录

通过 ID 删除特定的对话记录。

`DELETE /ai/conversations/{conversation_id}`

```java
import com.telnyx.sdk.models.ai.conversations.ConversationDeleteParams;

client.ai().conversations().delete("conversation_id");
```

## 获取对话记录的洞察结果

检索特定对话记录的洞察结果。

`GET /ai/conversations/{conversation_id}/conversations-insights`

```java
import com.telnyx.sdk.models.ai.conversations.ConversationRetrieveConversationsInsightsParams;
import com.telnyx.sdk.models.ai.conversations.ConversationRetrieveConversationsInsightsResponse;

ConversationRetrieveConversationsInsightsResponse response = client.ai().conversations().retrieveConversationsInsights("conversation_id");
```

## 创建消息

向对话记录中添加新消息。

`POST /ai/conversations/{conversation_id}/message` — 必需参数：`role`

```java
import com.telnyx.sdk.models.ai.conversations.ConversationAddMessageParams;

ConversationAddMessageParams params = ConversationAddMessageParams.builder()
    .conversationId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .role("role")
    .build();
client.ai().conversations().addMessage(params);
```

## 获取对话记录中的消息

检索特定对话记录中的所有消息，包括助手执行的操作（如工具调用）。

`GET /ai/conversations/{conversation_id}/messages`

```java
import com.telnyx.sdk.models.ai.conversations.messages.MessageListParams;
import com.telnyx.sdk.models.ai.conversations.messages.MessageListResponse;

MessageListResponse messages = client.ai().conversations().messages().list("conversation_id");
```

## 根据状态获取任务

根据查询字符串，检索用户的所有任务（状态为 `queued`, `processing`, `failed`, `success` 或 `partial_success`）。

`GET /ai/embeddings`

```java
import com.telnyx.sdk.models.ai.embeddings.EmbeddingListParams;
import com.telnyx.sdk.models.ai.embeddings.EmbeddingListResponse;

EmbeddingListResponse embeddings = client.ai().embeddings().list();
```

## 嵌入文档

使用嵌入模型对 Telnyx 存储桶中的文档进行嵌入处理。

`POST /ai/embeddings` — 必需参数：`bucket_name`

```java
import com.telnyx.sdk.models.ai.embeddings.EmbeddingCreateParams;
import com.telnyx.sdk.models.ai.embeddings.EmbeddingResponse;

EmbeddingCreateParams params = EmbeddingCreateParams.builder()
    .bucketName("bucket_name")
    .build();
EmbeddingResponse embeddingResponse = client.ai().embeddings().create(params);
```

## 列出嵌入桶

获取用户所有的嵌入桶。

`GET /ai/embeddings/buckets`

```java
import com.telnyx.sdk.models.ai.embeddings.buckets.BucketListParams;
import com.telnyx.sdk.models.ai.embeddings.buckets.BucketListResponse;

BucketListResponse buckets = client.ai().embeddings().buckets().list();
```

## 获取桶的文件级嵌入状态

获取指定用户桶中所有文件的嵌入状态。

`GET /ai/embeddings/buckets/{bucket_name}`

```java
import com.telnyx.sdk.models.ai.embeddings.buckets.BucketRetrieveParams;
import com.telnyx.sdk.models.ai.embeddings.buckets.BucketRetrieveResponse;

BucketRetrieveResponse bucket = client.ai().embeddings().buckets().retrieve("bucket_name");
```

## 禁用嵌入功能

删除整个桶的嵌入数据，并将其恢复为普通存储模式。

`DELETE /ai/embeddings/buckets/{bucket_name}`

```java
import com.telnyx.sdk.models.ai.embeddings.buckets.BucketDeleteParams;

client.ai().embeddings().buckets().delete("bucket_name");
```

## 搜索文档

对 Telnyx 存储桶中的文档进行相似性搜索，返回与查询内容最相似的 `num_docs` 个文档片段。

`POST /ai/embeddings/similarity-search` — 必需参数：`bucket_name`, `query`

```java
import com.telnyx.sdk.models.ai.embeddings.EmbeddingSimilaritySearchParams;
import com.telnyx.sdk.models.ai.embeddings.EmbeddingSimilaritySearchResponse;

EmbeddingSimilaritySearchParams params = EmbeddingSimilaritySearchParams.builder()
    .bucketName("bucket_name")
    .query("query")
    .build();
EmbeddingSimilaritySearchResponse response = client.ai().embeddings().similaritySearch(params);
```

## 嵌入 URL 内容

从指定的 URL 嵌入网页内容（包括同一域名下的最多 5 层子页面）。

`POST /ai/embeddings/url` — 必需参数：`url`, `bucket_name`

```java
import com.telnyx.sdk.models.ai.embeddings.EmbeddingResponse;
import com.telnyx.sdk.models.ai.embeddings.EmbeddingUrlParams;

EmbeddingUrlParams params = EmbeddingUrlParams.builder()
    .bucketName("bucket_name")
    .url("url")
    .build();
EmbeddingResponse embeddingResponse = client.ai().embeddings().url(params);
```

## 获取嵌入任务的状态

检查当前嵌入任务的状态。

`GET /ai/embeddings/{task_id}`

```java
import com.telnyx.sdk.models.ai.embeddings.EmbeddingRetrieveParams;
import com.telnyx.sdk.models.ai.embeddings.EmbeddingRetrieveResponse;

EmbeddingRetrieveResponse embedding = client.ai().embeddings().retrieve("task_id");
```

## 列出所有集群

获取所有现有的集群信息。

`GET /ai/clusters`

```java
import com.telnyx.sdk.models.ai.clusters.ClusterListPage;
import com.telnyx.sdk.models.ai.clusters.ClusterListParams;

ClusterListPage page = client.ai().clusters().list();
```

## 计算新集群

启动后台任务，对 [嵌入存储桶](https://developers.telnyx.com/api-reference/embeddings/embed-documents) 中的数据进行聚类分析。

`POST /ai/clusters` — 必需参数：`bucket`

```java
import com.telnyx.sdk.models.ai.clusters.ClusterComputeParams;
import com.telnyx.sdk.models.ai.clusters.ClusterComputeResponse;

ClusterComputeParams params = ClusterComputeParams.builder()
    .bucket("bucket")
    .build();
ClusterComputeResponse response = client.ai().clusters().compute(params);
```

## 获取集群信息

获取特定集群的详细信息。

`GET /ai/clusters/{task_id}`

```java
import com.telnyx.sdk.models.ai.clusters.ClusterRetrieveParams;
import com.telnyx.sdk.models.ai.clusters.ClusterRetrieveResponse;

ClusterRetrieveResponse cluster = client.ai().clusters().retrieve("task_id");
```

## 删除集群

删除指定的集群。

`DELETE /ai/clusters/{task_id}`

```java
import com.telnyx.sdk.models.ai.clusters.ClusterDeleteParams;

client.ai().clusters().delete("task_id");
```

## 获取集群可视化信息

获取特定集群的可视化图表。

`GET /ai/clusters/{task_id}/graph`

```java
import com.telnyx.sdk.core.http.HttpResponse;
import com.telnyx.sdk.models.ai.clusters.ClusterFetchGraphParams;

HttpResponse response = client.ai().clusters().fetchGraph("task_id");
```

## 将语音转换为文本

将语音转换为文本。

`POST /ai/audio/transcriptions`

```java
import com.telnyx.sdk.models.ai.audio.AudioTranscribeParams;
import com.telnyx.sdk.models.ai.audio.AudioTranscribeResponse;

AudioTranscribeParams params = AudioTranscribeParams.builder()
    .model(AudioTranscribeParams.Model.DISTIL_WHISPER_DISTIL_LARGE_V2)
    .build();
AudioTranscribeResponse response = client.ai().audio().transcribe(params);
```

## 创建聊天完成结果

使用语言模型生成聊天完成结果。

`POST /ai/chat/completions` — 必需参数：`messages`

```java
import com.telnyx.sdk.models.ai.chat.ChatCreateCompletionParams;
import com.telnyx.sdk.models.ai.chat.ChatCreateCompletionResponse;

ChatCreateCompletionParams params = ChatCreateCompletionParams.builder()
    .addMessage(ChatCreateCompletionParams.Message.builder()
        .content("You are a friendly chatbot.")
        .role(ChatCreateCompletionParams.Message.Role.SYSTEM)
        .build())
    .addMessage(ChatCreateCompletionParams.Message.builder()
        .content("Hello, world!")
        .role(ChatCreateCompletionParams.Message.Role.USER)
        .build())
    .build();
ChatCreateCompletionResponse response = client.ai().chat().createCompletion(params);
```

## 列出微调作业

检索用户创建的所有微调作业。

`GET /ai/fine_tuning/jobs`

```java
import com.telnyx.sdk.models.ai.finetuning.jobs.JobListParams;
import com.telnyx.sdk.models.ai.finetuning.jobs.JobListResponse;

JobListResponse jobs = client.ai().fineTuning().jobs().list();
```

## 创建微调作业

创建一个新的微调作业。

`POST /ai/fine_tuning/jobs` — 必需参数：`model`, `training_file`

```java
import com.telnyx.sdk.models.ai.finetuning.jobs.FineTuningJob;
import com.telnyx.sdk.models.ai.finetuning.jobs.JobCreateParams;

JobCreateParams params = JobCreateParams.builder()
    .model("model")
    .trainingFile("training_file")
    .build();
FineTuningJob fineTuningJob = client.ai().fineTuning().jobs().create(params);
```

## 获取微调作业信息

通过作业 ID 获取详细的微调作业信息。

`GET /ai/fine_tuning/jobs/{job_id}`

```java
import com.telnyx.sdk.models.ai.finetuning.jobs.FineTuningJob;
import com.telnyx.sdk.models.ai.finetuning.jobs.JobRetrieveParams;

FineTuningJob fineTuningJob = client.ai().fineTuning().jobs().retrieve("job_id");
```

## 取消微调作业

取消正在进行的微调作业。

`POST /ai/fine_tuning/jobs/{job_id}/cancel`

```java
import com.telnyx.sdk.models.ai.finetuning.jobs.FineTuningJob;
import com.telnyx.sdk.models.ai.finetuning.jobs.JobCancelParams;

FineTuningJob fineTuningJob = client.ai().fineTuning().jobs().cancel("job_id");
```

## 获取可用模型

此接口返回所有可用的开源模型和 OpenAI 模型。

`GET /ai/models`

```java
import com.telnyx.sdk.models.ai.AiRetrieveModelsParams;
import com.telnyx.sdk.models.ai.AiRetrieveModelsResponse;

AiRetrieveModelsResponse response = client.ai().retrieveModels();
```

## 摘要文件内容

生成文件的摘要。

`POST /ai/summarize` — 必需参数：`bucket`, `filename`

```java
import com.telnyx.sdk.models.ai.AiSummarizeParams;
import com.telnyx.sdk.models.ai.AiSummarizeResponse;

AiSummarizeParams params = AiSummarizeParams.builder()
    .bucket("bucket")
    .filename("filename")
    .build();
AiSummarizeResponse response = client.ai().summarize(params);
```
```