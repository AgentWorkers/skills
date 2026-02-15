---
name: telnyx-ai-assistants-go
description: >-
  Create and manage AI voice assistants with custom personalities, knowledge
  bases, and tool integrations. This skill provides Go SDK examples.
metadata:
  author: telnyx
  product: ai-assistants
  language: go
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx AI 助手 - Go

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

以下所有示例均假设 `client` 已按照上述方式初始化。

## 列出助手

检索用户配置的所有 AI 助手列表。

`GET /ai/assistants`

```go
	assistantsList, err := client.AI.Assistants.List(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", assistantsList.Data)
```

## 创建助手

创建一个新的 AI 助手。

`POST /ai/assistants` — 必需参数：`name`、`model`、`instructions`

```go
	assistant, err := client.AI.Assistants.New(context.TODO(), telnyx.AIAssistantNewParams{
		Instructions: "instructions",
		Model:        "model",
		Name:         "name",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", assistant.ID)
```

## 获取助手信息

通过 `assistant_id` 获取 AI 助手的配置信息。

`GET /ai/assistants/{assistant_id}`

```go
	assistant, err := client.AI.Assistants.Get(
		context.TODO(),
		"assistant_id",
		telnyx.AIAssistantGetParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", assistant.ID)
```

## 更新助手信息

更新 AI 助手的属性。

`POST /ai/assistants/{assistant_id}`

```go
	assistant, err := client.AI.Assistants.Update(
		context.TODO(),
		"assistant_id",
		telnyx.AIAssistantUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", assistant.ID)
```

## 删除助手

通过 `assistant_id` 删除 AI 助手。

`DELETE /ai/assistants/{assistant_id}`

```go
	assistant, err := client.AI.Assistants.Delete(context.TODO(), "assistant_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", assistant.ID)
```

## 助手聊天（测试版）

此端点允许客户端向特定的 AI 助手发送聊天消息。

`POST /ai/assistants/{assistant_id}/chat` — 必需参数：`content`、`conversation_id`

```go
	response, err := client.AI.Assistants.Chat(
		context.TODO(),
		"assistant_id",
		telnyx.AIAssistantChatParams{
			Content:        "Tell me a joke about cats",
			ConversationID: "42b20469-1215-4a9a-8964-c36f66b406f4",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Content)
```

## 助手短信聊天

为助手发送短信。

`POST /ai/assistants/{assistant_id}/chat/sms` — 必需参数：`from`、`to`

```go
	response, err := client.AI.Assistants.SendSMS(
		context.TODO(),
		"assistant_id",
		telnyx.AIAssistantSendSMSParams{
			From: "from",
			To:   "to",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.ConversationID)
```

## 复制助手

复制现有的助手（不包括电话和消息设置）。

`POST /ai/assistants/{assistant_id}/clone`

```go
	assistant, err := client.AI.Assistants.Clone(context.TODO(), "assistant_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", assistant.ID)
```

## 从外部提供商导入助手

从外部提供商导入助手。

`POST /ai/assistants/import` — 必需参数：`provider`、`api_key_ref`

```go
	assistantsList, err := client.AI.Assistants.Imports(context.TODO(), telnyx.AIAssistantImportsParams{
		APIKeyRef: "api_key_ref",
		Provider:  telnyx.AIAssistantImportsParamsProviderElevenlabs,
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", assistantsList.Data)
```

## 列出计划事件

获取助手的计划事件列表（支持分页和过滤）

`GET /ai/assistants/{assistant_id}/scheduled_events`

```go
	page, err := client.AI.Assistants.ScheduledEvents.List(
		context.TODO(),
		"assistant_id",
		telnyx.AIAssistantScheduledEventListParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建计划事件

为助手创建计划事件。

`POST /ai/assistants/{assistant_id}/scheduled_events` — 必需参数：`telnyx_conversation_channel`、`telnyx_end_user_target`、`telnyx_agent_target`、`scheduled_at_fixed_datetime`

```go
	scheduledEventResponse, err := client.AI.Assistants.ScheduledEvents.New(
		context.TODO(),
		"assistant_id",
		telnyx.AIAssistantScheduledEventNewParams{
			ScheduledAtFixedDatetime:  time.Now(),
			TelnyxAgentTarget:         "telnyx_agent_target",
			TelnyxConversationChannel: telnyx.ConversationChannelTypePhoneCall,
			TelnyxEndUserTarget:       "telnyx_end_user_target",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", scheduledEventResponse)
```

## 获取计划事件信息

通过事件 ID 获取计划事件的信息。

`GET /ai/assistants/{assistant_id}/scheduled_events/{event_id}`

```go
	scheduledEventResponse, err := client.AI.Assistants.ScheduledEvents.Get(
		context.TODO(),
		"event_id",
		telnyx.AIAssistantScheduledEventGetParams{
			AssistantID: "assistant_id",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", scheduledEventResponse)
```

## 删除计划事件

如果事件尚未执行，此操作将取消该事件。

`DELETE /ai/assistants/{assistant_id}/scheduled_events/{event_id}`

```go
	err := client.AI.Assistants.ScheduledEvents.Delete(
		context.TODO(),
		"event_id",
		telnyx.AIAssistantScheduledEventDeleteParams{
			AssistantID: "assistant_id",
		},
	)
	if err != nil {
		panic(err.Error())
	}
```

## 列出助手测试（支持分页）

检索助手测试的列表（支持可选过滤）

`GET /ai/assistants/tests`

```go
	page, err := client.AI.Assistants.Tests.List(context.TODO(), telnyx.AIAssistantTestListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建新的助手测试

创建用于评估 AI 助手性能的测试配置。

`POST /ai/assistants/tests` — 必需参数：`name`、`destination`、`instructions`、`rubric`

```go
	assistantTest, err := client.AI.Assistants.Tests.New(context.TODO(), telnyx.AIAssistantTestNewParams{
		Destination:  "+15551234567",
		Instructions: "Act as a frustrated customer who received a damaged product. Ask for a refund and escalate if not satisfied with the initial response.",
		Name:         "Customer Support Bot Test",
		Rubric: []telnyx.AIAssistantTestNewParamsRubric{{
			Criteria: "Assistant responds within 30 seconds",
			Name:     "Response Time",
		}, {
			Criteria: "Provides correct product information",
			Name:     "Accuracy",
		}},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", assistantTest.TestID)
```

## 获取所有测试套件名称

检索当前用户可用的所有测试套件名称列表。

`GET /ai/assistants/tests/test-suites`

```go
	testSuites, err := client.AI.Assistants.Tests.TestSuites.List(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", testSuites.Data)
```

## 获取测试套件运行历史

检索特定测试套件的运行历史（支持分页和过滤）

`GET /ai/assistants/tests/test-suites/{suite_name}/runs`

```go
	page, err := client.AI.Assistants.Tests.TestSuites.Runs.List(
		context.TODO(),
		"suite_name",
		telnyx.AIAssistantTestTestSuiteRunListParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 触发测试套件执行

批量执行特定测试套件中的所有测试。

`POST /ai/assistants/tests/test-suites/{suite_name}/runs`

```go
	testRunResponses, err := client.AI.Assistants.Tests.TestSuites.Runs.Trigger(
		context.TODO(),
		"suite_name",
		telnyx.AIAssistantTestTestSuiteRunTriggerParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", testRunResponses)
```

## 获取助手测试信息

检索特定助手测试的详细信息。

`GET /ai/assistants/tests/{test_id}`

```go
	assistantTest, err := client.AI.Assistants.Tests.Get(context.TODO(), "test_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", assistantTest.TestID)
```

## 更新助手测试配置

更新现有的助手测试配置。

`PUT /ai/assistants/tests/{test_id}`

```go
	assistantTest, err := client.AI.Assistants.Tests.Update(
		context.TODO(),
		"test_id",
		telnyx.AIAssistantTestUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", assistantTest.TestID)
```

## 删除助手测试

永久删除助手测试及其所有相关数据。

`DELETE /ai/assistants/tests/{test_id}`

```go
	err := client.AI.Assistants.Tests.Delete(context.TODO(), "test_id")
	if err != nil {
		panic(err.Error())
	}
```

## 获取特定测试的运行历史

检索特定助手测试的运行历史（支持分页和过滤）

`GET /ai/assistants/tests/{test_id}/runs`

```go
	page, err := client.AI.Assistants.Tests.Runs.List(
		context.TODO(),
		"test_id",
		telnyx.AIAssistantTestRunListParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 触发手动测试运行

立即执行特定的助手测试。

`POST /ai/assistants/tests/{test_id}/runs`

```go
	testRunResponse, err := client.AI.Assistants.Tests.Runs.Trigger(
		context.TODO(),
		"test_id",
		telnyx.AIAssistantTestRunTriggerParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", testRunResponse.RunID)
```

## 获取特定测试运行的详细信息

检索特定测试运行的详细信息。

`GET /ai/assistants/tests/{test_id}/runs/{run_id}`

```go
	testRunResponse, err := client.AI.Assistants.Tests.Runs.Get(
		context.TODO(),
		"run_id",
		telnyx.AIAssistantTestRunGetParams{
			TestID: "test_id",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", testRunResponse.RunID)
```

## 获取助手的所有版本

检索特定助手的所有版本及其完整配置和元数据。

`GET /ai/assistants/{assistant_id}/versions`

```go
	assistantsList, err := client.AI.Assistants.Versions.List(context.TODO(), "assistant_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", assistantsList.Data)
```

## 获取特定助手版本

通过 `assistant_id` 和 `version_id` 获取特定版本的助手信息。

`GET /ai/assistants/{assistant_id}/versions/{version_id}`

```go
	assistant, err := client.AI.Assistants.Versions.Get(
		context.TODO(),
		"version_id",
		telnyx.AIAssistantVersionGetParams{
			AssistantID: "assistant_id",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", assistant.ID)
```

## 更新特定助手版本

更新特定助手版本的配置。

`POST /ai/assistants/{assistant_id}/versions/{version_id}`

```go
	assistant, err := client.AI.Assistants.Versions.Update(
		context.TODO(),
		"version_id",
		telnyx.AIAssistantVersionUpdateParams{
			AssistantID:     "assistant_id",
			UpdateAssistant: telnyx.UpdateAssistantParam{},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", assistant.ID)
```

## 删除特定助手版本

永久删除特定版本的助手。

`DELETE /ai/assistants/{assistant_id}/versions/{version_id}`

```go
	err := client.AI.Assistants.Versions.Delete(
		context.TODO(),
		"version_id",
		telnyx.AIAssistantVersionDeleteParams{
			AssistantID: "assistant_id",
		},
	)
	if err != nil {
		panic(err.Error())
	}
```

## 将助手版本提升为主版本

将特定版本提升为助手的主/当前版本。

`POST /ai/assistants/{assistant_id}/versions/{version_id}/promote`

```go
	assistant, err := client.AI.Assistants.Versions.Promote(
		context.TODO(),
		"version_id",
		telnyx.AIAssistantVersionPromoteParams{
			AssistantID: "assistant_id",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", assistant.ID)
```

## 获取 Canary 部署配置

获取助手的 Canary 部署配置。

`GET /ai/assistants/{assistant_id}/canary-deploys`

```go
	canaryDeployResponse, err := client.AI.Assistants.CanaryDeploys.Get(context.TODO(), "assistant_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", canaryDeployResponse.AssistantID)
```

## 创建 Canary 部署

为助手创建 Canary 部署配置。

`POST /ai/assistants/{assistant_id}/canary-deploys` — 必需参数：`versions`

```go
	canaryDeployResponse, err := client.AI.Assistants.CanaryDeploys.New(
		context.TODO(),
		"assistant_id",
		telnyx.AIAssistantCanaryDeployNewParams{
			CanaryDeploy: telnyx.CanaryDeployParam{
				Versions: []telnyx.VersionConfigParam{{
					Percentage: 1,
					VersionID:  "version_id",
				}},
			},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", canaryDeployResponse.AssistantID)
```

## 更新 Canary 部署配置

更新助手的 Canary 部署配置。

`PUT /ai/assistants/{assistant_id}/canary-deploys` — 必需参数：`versions`

```go
	canaryDeployResponse, err := client.AI.Assistants.CanaryDeploys.Update(
		context.TODO(),
		"assistant_id",
		telnyx.AIAssistantCanaryDeployUpdateParams{
			CanaryDeploy: telnyx.CanaryDeployParam{
				Versions: []telnyx.VersionConfigParam{{
					Percentage: 1,
					VersionID:  "version_id",
				}},
			},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", canaryDeployResponse.AssistantID)
```

## 删除 Canary 部署配置

删除助手的 Canary 部署配置。

`DELETE /ai/assistants/{assistant_id}/canary-deploys`

```go
	err := client.AI.Assistants.CanaryDeploys.Delete(context.TODO(), "assistant_id")
	if err != nil {
		panic(err.Error())
	}
```

## 获取助手的 Texml 文件

通过 `assistant_id` 获取助手的 Texml 文件。

`GET /ai/assistants/{assistant_id}/texml`

```go
	response, err := client.AI.Assistants.GetTexml(context.TODO(), "assistant_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response)
```

## 测试助手工具

测试助手的 Webhook 工具。

`POST /ai/assistants/{assistant_id}/tools/{tool_id}/test`

```go
	response, err := client.AI.Assistants.Tools.Test(
		context.TODO(),
		"tool_id",
		telnyx.AIAssistantToolTestParams{
			AssistantID: "assistant_id",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出集成

列出所有可用的集成。

`GET /ai/integrations`

```go
	integrations, err := client.AI.Integrations.List(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", integrations.Data)
```

## 列出用户集成

列出用户的集成设置。

`GET /ai/integrations/connections`

```go
	connections, err := client.AI.Integrations.Connections.List(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", connections.Data)
```

## 根据 ID 获取用户集成连接信息

获取用户的集成连接信息。

`GET /ai/integrations/connections/{user_connection_id}`

```go
	connection, err := client.AI.Integrations.Connections.Get(context.TODO(), "user_connection_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", connection.Data)
```

## 删除集成连接

删除特定的集成连接。

`DELETE /ai/integrations/connections/{user_connection_id}`

```go
	err := client.AI.Integrations.Connections.Delete(context.TODO(), "user_connection_id")
	if err != nil {
		panic(err.Error())
	}
```

## 根据 ID 获取集成信息

检索集成的详细信息。

`GET /ai/integrations/{integration_id}`

```go
	integration, err := client.AI.Integrations.Get(context.TODO(), "integration_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", integration.ID)
```

## 列出 MCP 服务器

列出所有的 MCP 服务器。

`GET /ai/mcp_servers`

```go
	page, err := client.AI.McpServers.List(context.TODO(), telnyx.AIMcpServerListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建 MCP 服务器

创建新的 MCP 服务器。

`POST /ai/mcp_servers` — 必需参数：`name`、`type`、`url`

```go
	mcpServer, err := client.AI.McpServers.New(context.TODO(), telnyx.AIMcpServerNewParams{
		Name: "name",
		Type: "type",
		URL:  "url",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", mcpServer.ID)
```

## 获取 MCP 服务器信息

检索特定 MCP 服务器的详细信息。

`GET /ai/mcp_servers/{mcp_server_id}`

```go
	mcpServer, err := client.AI.McpServers.Get(context.TODO(), "mcp_server_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", mcpServer.ID)
```

## 更新 MCP 服务器

更新现有的 MCP 服务器。

`PUT /ai/mcp_servers/{mcp_server_id}`

```go
	mcpServer, err := client.AI.McpServers.Update(
		context.TODO(),
		"mcp_server_id",
		telnyx.AIMcpServerUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", mcpServer.ID)
```

## 删除 MCP 服务器

删除特定的 MCP 服务器。

`DELETE /ai/mcp_servers/{mcp_server_id}`

```go
	err := client.AI.McpServers.Delete(context.TODO(), "mcp_server_id")
	if err != nil {
		panic(err.Error())
	}
```