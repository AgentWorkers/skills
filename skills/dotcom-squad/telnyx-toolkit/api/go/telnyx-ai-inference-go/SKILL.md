---
name: telnyx-ai-inference-go
description: >-
  Access Telnyx LLM inference APIs, embeddings, and AI analytics for call
  insights and summaries. This skill provides Go SDK examples.
metadata:
  author: telnyx
  product: ai-inference
  language: go
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx AI 推理 - Go

## 安装

```bash
go get github.com/team-telnyx/telnyx-go
```

## 设置

```go
import (
  "context"
  "fmt"
  "os"

  "github.com/team-telnyx/telnyx-go"
  "github.com/team-telnyx/telnyx-go/option"
)

client := telnyx.NewClient(
  option.WithAPIKey(os.Getenv("TELNYX_API_KEY")),
)
```

以下所有示例均假设 `client` 已按上述方式初始化。

## 列出对话记录

检索用户配置的所有 AI 对话记录。

`GET /ai/conversations`

```go
	conversations, err := client.AI.Conversations.List(context.TODO(), telnyx.AIConversationListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", conversations.Data)
```

## 创建对话记录

创建一个新的 AI 对话记录。

`POST /ai/conversations`

```go
	conversation, err := client.AI.Conversations.New(context.TODO(), telnyx.AIConversationNewParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", conversation.ID)
```

## 获取洞察模板组

获取所有洞察模板组。

`GET /ai/conversations/insight-groups`

```go
	page, err := client.AI.Conversations.InsightGroups.GetInsightGroups(context.TODO(), telnyx.AIConversationInsightGroupGetInsightGroupsParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建洞察模板组

创建一个新的洞察模板组。

`POST /ai/conversations/insight-groups` — 必需参数：`name`

```go
	insightTemplateGroupDetail, err := client.AI.Conversations.InsightGroups.InsightGroups(context.TODO(), telnyx.AIConversationInsightGroupInsightGroupsParams{
		Name: "name",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", insightTemplateGroupDetail.Data)
```

## 获取洞察模板组

通过 ID 获取洞察模板组。

`GET /ai/conversations/insight-groups/{group_id}`

```go
	insightTemplateGroupDetail, err := client.AI.Conversations.InsightGroups.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", insightTemplateGroupDetail.Data)
```

## 更新洞察模板组

更新一个洞察模板组。

`PUT /ai/conversations/insight-groups/{group_id}`

```go
	insightTemplateGroupDetail, err := client.AI.Conversations.InsightGroups.Update(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.AIConversationInsightGroupUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", insightTemplateGroupDetail.Data)
```

## 删除洞察模板组

通过 ID 删除一个洞察模板组。

`DELETE /ai/conversations/insight-groups/{group_id}`

```go
	err := client.AI.Conversations.InsightGroups.Delete(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
```

## 将洞察模板分配给组

将一个洞察模板分配给一个组。

`POST /ai/conversations/insight-groups/{group_id}/insights/{insight_id}/assign`

```go
	err := client.AI.Conversations.InsightGroups.Insights.Assign(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.AIConversationInsightGroupInsightAssignParams{
			GroupID: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		},
	)
	if err != nil {
		panic(err.Error())
	}
```

## 从组中解除洞察模板的分配

从组中移除一个洞察模板。

`DELETE /ai/conversations/insight-groups/{group_id}/insights/{insight_id}/unassign`

```go
	err := client.AI.Conversations.InsightGroups.Insights.DeleteUnassign(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.AIConversationInsightGroupInsightDeleteUnassignParams{
			GroupID: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		},
	)
	if err != nil {
		panic(err.Error())
	}
```

## 获取洞察模板

获取所有洞察模板。

`GET /ai/conversations/insights`

```go
	page, err := client.AI.Conversations.Insights.List(context.TODO(), telnyx.AIConversationInsightListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建洞察模板

创建一个新的洞察模板。

`POST /ai/conversations/insights` — 必需参数：`instructions`, `name`

```go
	insightTemplateDetail, err := client.AI.Conversations.Insights.New(context.TODO(), telnyx.AIConversationInsightNewParams{
		Instructions: "instructions",
		Name:         "name",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", insightTemplateDetail.Data)
```

## 获取洞察模板

通过 ID 获取一个洞察模板。

`GET /ai/conversations/insights/{insight_id}`

```go
	insightTemplateDetail, err := client.AI.Conversations.Insights.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", insightTemplateDetail.Data)
```

## 更新洞察模板

更新一个洞察模板。

`PUT /ai/conversations/insights/{insight_id}`

```go
	insightTemplateDetail, err := client.AI.Conversations.Insights.Update(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.AIConversationInsightUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", insightTemplateDetail.Data)
```

## 删除洞察模板

通过 ID 删除一个洞察模板。

`DELETE /ai/conversations/insights/{insight_id}`

```go
	err := client.AI.Conversations.Insights.Delete(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
```

## 获取对话记录

通过 ID 获取特定的 AI 对话记录。

`GET /ai/conversations/{conversation_id}`

```go
	conversation, err := client.AI.Conversations.Get(context.TODO(), "conversation_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", conversation.Data)
```

## 更新对话元数据

更新特定对话记录的元数据。

`PUT /ai/conversations/{conversation_id}`

```go
	conversation, err := client.AI.Conversations.Update(
		context.TODO(),
		"conversation_id",
		telnyx.AIConversationUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", conversation.Data)
```

## 删除对话记录

通过 ID 删除特定的对话记录。

`DELETE /ai/conversations/{conversation_id}`

```go
	err := client.AI.Conversations.Delete(context.TODO(), "conversation_id")
	if err != nil {
		panic(err.Error())
	}
```

## 获取对话记录的洞察结果

检索特定对话记录的洞察结果。

`GET /ai/conversations/{conversation_id}/conversations-insights`

```go
	response, err := client.AI.Conversations.GetConversationsInsights(context.TODO(), "conversation_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 创建消息

向对话记录中添加新消息。

`POST /ai/conversations/{conversation_id}/message` — 必需参数：`role`

```go
	err := client.AI.Conversations.AddMessage(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.AIConversationAddMessageParams{
			Role: "role",
		},
	)
	if err != nil {
		panic(err.Error())
	}
```

## 获取对话记录中的消息

检索特定对话记录中的消息，包括助手执行的工具调用。

`GET /ai/conversations/{conversation_id}/messages`

```go
	messages, err := client.AI.Conversations.Messages.List(context.TODO(), "conversation_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", messages.Data)
```

## 根据状态获取任务

根据查询字符串，检索用户的所有任务（状态为 `queued`, `processing`, `failed`, `success` 或 `partial_success`）。

`GET /ai/embeddings`

```go
	embeddings, err := client.AI.Embeddings.List(context.TODO(), telnyx.AIEmbeddingListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", embeddings.Data)
```

## 嵌入文档

使用嵌入模型对 Telnyx 存储桶中的文档进行嵌入处理。

`POST /ai/embeddings` — 必需参数：`bucket_name`

```go
	embeddingResponse, err := client.AI.Embeddings.New(context.TODO(), telnyx.AIEmbeddingNewParams{
		BucketName: "bucket_name",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", embeddingResponse.Data)
```

## 列出嵌入桶

获取用户的所有嵌入桶。

`GET /ai/embeddings/buckets`

```go
	buckets, err := client.AI.Embeddings.Buckets.List(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", buckets.Data)
```

## 获取桶的文件级嵌入状态

获取指定用户桶中的所有嵌入文件及其处理状态。

`GET /ai/embeddings/buckets/{bucket_name}`

```go
	bucket, err := client.AI.Embeddings.Buckets.Get(context.TODO(), "bucket_name")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", bucket.Data)
```

## 禁用嵌入桶的 AI 功能

删除整个桶的嵌入数据，并将其恢复为普通存储模式。

`DELETE /ai/embeddings/buckets/{bucket_name}`

```go
	err := client.AI.Embeddings.Buckets.Delete(context.TODO(), "bucket_name")
	if err != nil {
		panic(err.Error())
	}
```

## 搜索文档

对 Telnyx 存储桶中的文档进行相似性搜索，返回与查询内容最相似的 `num_docs` 个文档片段。

`POST /ai/embeddings/similarity-search` — 必需参数：`bucket_name`, `query`

```go
	response, err := client.AI.Embeddings.SimilaritySearch(context.TODO(), telnyx.AIEmbeddingSimilaritySearchParams{
		BucketName: "bucket_name",
		Query:      "query",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 嵌入 URL 内容

从指定的 URL 嵌入网页内容，包括同一域名下的最多 5 层子页面。

`POST /ai/embeddings/url` — 必需参数：`url`, `bucket_name`

```go
	embeddingResponse, err := client.AI.Embeddings.URL(context.TODO(), telnyx.AIEmbeddingURLParams{
		BucketName: "bucket_name",
		URL:        "url",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", embeddingResponse.Data)
```

## 获取嵌入任务的状态

检查当前嵌入任务的进度。

`GET /ai/embeddings/{task_id}`

```go
	embedding, err := client.AI.Embeddings.Get(context.TODO(), "task_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", embedding.Data)
```

## 列出所有集群

获取所有集群信息。

`GET /ai/clusters`

```go
	page, err := client.AI.Clusters.List(context.TODO(), telnyx.AIClusterListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 计算新集群

启动后台任务，对 [嵌入存储桶](https://developers.telnyx.com/api-reference/embeddings/embed-documents) 中的数据进行聚类分析。

`POST /ai/clusters` — 必需参数：`bucket`

```go
	response, err := client.AI.Clusters.Compute(context.TODO(), telnyx.AIClusterComputeParams{
		Bucket: "bucket",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 获取集群信息

`GET /ai/clusters/{task_id}`

```go
	cluster, err := client.AI.Clusters.Get(
		context.TODO(),
		"task_id",
		telnyx.AIClusterGetParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", cluster.Data)
```

## 删除集群

删除一个集群。

`DELETE /ai/clusters/{task_id}`

```go
	err := client.AI.Clusters.Delete(context.TODO(), "task_id")
	if err != nil {
		panic(err.Error())
	}
```

## 获取集群可视化信息

`GET /ai/clusters/{task_id}/graph`

```go
	response, err := client.AI.Clusters.FetchGraph(
		context.TODO(),
		"task_id",
		telnyx.AIClusterFetchGraphParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response)
```

## 将语音转录为文本

将语音内容转录为文本。

`POST /ai/audio/transcriptions`

```go
	response, err := client.AI.Audio.Transcribe(context.TODO(), telnyx.AIAudioTranscribeParams{
		Model: telnyx.AIAudioTranscribeParamsModelDistilWhisperDistilLargeV2,
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Text)
```

## 创建聊天完成结果

与语言模型进行聊天交互。

`POST /ai/chat/completions` — 必需参数：`messages`

```go
	response, err := client.AI.Chat.NewCompletion(context.TODO(), telnyx.AIChatNewCompletionParams{
		Messages: []telnyx.AIChatNewCompletionParamsMessage{{
			Role: "system",
			Content: telnyx.AIChatNewCompletionParamsMessageContentUnion{
				OfString: telnyx.String("You are a friendly chatbot."),
			},
		}, {
			Role: "user",
			Content: telnyx.AIChatNewCompletionParamsMessageContentUnion{
				OfString: telnyx.String("Hello, world!"),
			},
		}},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response)
```

## 列出微调作业

检索用户创建的所有微调作业。

`GET /ai/fine_tuning/jobs`

```go
	jobs, err := client.AI.FineTuning.Jobs.List(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", jobs.Data)
```

## 创建微调作业

创建一个新的微调作业。

`POST /ai/fine_tuning/jobs` — 必需参数：`model`, `training_file`

```go
	fineTuningJob, err := client.AI.FineTuning.Jobs.New(context.TODO(), telnyx.AIFineTuningJobNewParams{
		Model:        "model",
		TrainingFile: "training_file",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", fineTuningJob.ID)
```

## 获取微调作业信息

通过 `job_id` 获取微调作业的详细信息。

`GET /ai/fine_tuning/jobs/{job_id}`

```go
	fineTuningJob, err := client.AI.FineTuning.Jobs.Get(context.TODO(), "job_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", fineTuningJob.ID)
```

## 取消微调作业

取消一个微调作业。

`POST /ai/fine_tuning/jobs/{job_id}/cancel`

```go
	fineTuningJob, err := client.AI.FineTuning.Jobs.Cancel(context.TODO(), "job_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", fineTuningJob.ID)
```

## 获取可用模型

此端点返回可用的开源模型和 OpenAI 模型的列表。

`GET /ai/models`

```go
	response, err := client.AI.GetModels(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 摘要文件内容

生成文件内容的摘要。

`POST /ai/summarize` — 必需参数：`bucket`, `filename`

```go
	response, err := client.AI.Summarize(context.TODO(), telnyx.AISummarizeParams{
		Bucket:   "bucket",
		Filename: "filename",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```