---
name: telnyx-ai-assistants-java
description: >-
  Create and manage AI voice assistants with custom personalities, knowledge
  bases, and tool integrations. This skill provides Java SDK examples.
metadata:
  author: telnyx
  product: ai-assistants
  language: java
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx AI 辅助工具 - Java

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

## 列出辅助工具

检索用户配置的所有 AI 辅助工具。

`GET /ai/assistants`

```java
import com.telnyx.sdk.models.ai.assistants.AssistantListParams;
import com.telnyx.sdk.models.ai.assistants.AssistantsList;

AssistantsList assistantsList = client.ai().assistants().list();
```

## 创建辅助工具

创建一个新的 AI 辅助工具。

`POST /ai/assistants` — 必需参数：`name`、`model`、`instructions`

```java
import com.telnyx.sdk.models.ai.assistants.AssistantCreateParams;
import com.telnyx.sdk.models.ai.assistants.InferenceEmbedding;

AssistantCreateParams params = AssistantCreateParams.builder()
    .instructions("instructions")
    .model("model")
    .name("name")
    .build();
InferenceEmbedding assistant = client.ai().assistants().create(params);
```

## 获取辅助工具信息

通过 `assistant_id` 检索 AI 辅助工具的配置信息。

`GET /ai/assistants/{assistant_id}`

```java
import com.telnyx.sdk.models.ai.assistants.AssistantRetrieveParams;
import com.telnyx.sdk.models.ai.assistants.InferenceEmbedding;

InferenceEmbedding assistant = client.ai().assistants().retrieve("assistant_id");
```

## 更新辅助工具

更新 AI 辅助工具的属性。

`POST /ai/assistants/{assistant_id}`

```java
import com.telnyx.sdk.models.ai.assistants.AssistantUpdateParams;
import com.telnyx.sdk.models.ai.assistants.InferenceEmbedding;

InferenceEmbedding assistant = client.ai().assistants().update("assistant_id");
```

## 删除辅助工具

通过 `assistant_id` 删除 AI 辅助工具。

`DELETE /ai/assistants/{assistant_id}`

```java
import com.telnyx.sdk.models.ai.assistants.AssistantDeleteParams;
import com.telnyx.sdk.models.ai.assistants.AssistantDeleteResponse;

AssistantDeleteResponse assistant = client.ai().assistants().delete("assistant_id");
```

## 辅助工具聊天（测试版）

此端点允许客户端向特定的 AI 辅助工具发送聊天消息。

`POST /ai/assistants/{assistant_id}/chat` — 必需参数：`content`、`conversation_id`

```java
import com.telnyx.sdk.models.ai.assistants.AssistantChatParams;
import com.telnyx.sdk.models.ai.assistants.AssistantChatResponse;

AssistantChatParams params = AssistantChatParams.builder()
    .assistantId("assistant_id")
    .content("Tell me a joke about cats")
    .conversationId("42b20469-1215-4a9a-8964-c36f66b406f4")
    .build();
AssistantChatResponse response = client.ai().assistants().chat(params);
```

## 辅助工具短信聊天

为辅助工具发送短信。

`POST /ai/assistants/{assistant_id}/chat/sms` — 必需参数：`from`、`to`

```java
import com.telnyx.sdk.models.ai.assistants.AssistantSendSmsParams;
import com.telnyx.sdk.models.ai.assistants.AssistantSendSmsResponse;

AssistantSendSmsParams params = AssistantSendSmsParams.builder()
    .assistantId("assistant_id")
    .from("from")
    .to("to")
    .build();
AssistantSendSmsResponse response = client.ai().assistants().sendSms(params);
```

## 复制辅助工具

复制现有的辅助工具（不包括电话和消息设置）。

`POST /ai/assistants/{assistant_id}/clone`

```java
import com.telnyx.sdk.models.ai.assistants.AssistantCloneParams;
import com.telnyx.sdk.models.ai.assistants.InferenceEmbedding;

InferenceEmbedding assistant = client.ai().assistants().clone("assistant_id");
```

## 从外部提供商导入辅助工具

从外部提供商导入辅助工具。

`POST /ai/assistants/import` — 必需参数：`provider`、`api_key_ref`

```java
import com.telnyx.sdk.models.ai.assistants.AssistantImportsParams;
import com.telnyx.sdk.models.ai.assistants.AssistantsList;

AssistantImportsParams params = AssistantImportsParams.builder()
    .apiKeyRef("api_key_ref")
    .provider(AssistantImportsParams.Provider.ELEVENLABS)
    .build();
AssistantsList assistantsList = client.ai().assistants().imports(params);
```

## 列出计划事件

获取辅助工具的计划事件（支持分页和过滤）

`GET /ai/assistants/{assistant_id}/scheduled_events`

```java
import com.telnyx.sdk.models.ai.assistants.scheduledevents.ScheduledEventListPage;
import com.telnyx.sdk.models.ai.assistants.scheduledevents.ScheduledEventListParams;

ScheduledEventListPage page = client.ai().assistants().scheduledEvents().list("assistant_id");
```

## 创建计划事件

为辅助工具创建计划事件。

`POST /ai/assistants/{assistant_id}/scheduled_events` — 必需参数：`telnyx_conversation_channel`、`telnyx_end_user_target`、`telnyx_agent_target`、`scheduled_at_fixed_datetime`

```java
import com.telnyx.sdk.models.ai.assistants.scheduledevents.ConversationChannelType;
import com.telnyx.sdk.models.ai.assistants.scheduledevents.ScheduledEventCreateParams;
import com.telnyx.sdk.models.ai.assistants.scheduledevents.ScheduledEventResponse;
import java.time.OffsetDateTime;

ScheduledEventCreateParams params = ScheduledEventCreateParams.builder()
    .assistantId("assistant_id")
    .scheduledAtFixedDatetime(OffsetDateTime.parse("2025-04-15T13:07:28.764Z"))
    .telnyxAgentTarget("telnyx_agent_target")
    .telnyxConversationChannel(ConversationChannelType.PHONE_CALL)
    .telnyxEndUserTarget("telnyx_end_user_target")
    .build();
ScheduledEventResponse scheduledEventResponse = client.ai().assistants().scheduledEvents().create(params);
```

## 获取计划事件信息

通过事件 ID 检索计划事件的信息。

`GET /ai/assistants/{assistant_id}/scheduled_events/{event_id}`

```java
import com.telnyx.sdk.models.ai.assistants.scheduledevents.ScheduledEventResponse;
import com.telnyx.sdk.models.ai.assistants.scheduledevents.ScheduledEventRetrieveParams;

ScheduledEventRetrieveParams params = ScheduledEventRetrieveParams.builder()
    .assistantId("assistant_id")
    .eventId("event_id")
    .build();
ScheduledEventResponse scheduledEventResponse = client.ai().assistants().scheduledEvents().retrieve(params);
```

## 删除计划事件

如果事件尚未执行，此操作将取消该事件。

`DELETE /ai/assistants/{assistant_id}/scheduled_events/{event_id}`

```java
import com.telnyx.sdk.models.ai.assistants.scheduledevents.ScheduledEventDeleteParams;

ScheduledEventDeleteParams params = ScheduledEventDeleteParams.builder()
    .assistantId("assistant_id")
    .eventId("event_id")
    .build();
client.ai().assistants().scheduledEvents().delete(params);
```

## 列出辅助工具测试（支持分页）

检索辅助工具测试的列表（支持可选过滤）

`GET /ai/assistants/tests`

```java
import com.telnyx.sdk.models.ai.assistants.tests.TestListPage;
import com.telnyx.sdk.models.ai.assistants.tests.TestListParams;

TestListPage page = client.ai().assistants().tests().list();
```

## 创建新的辅助工具测试

创建用于评估 AI 辅助工具性能的测试配置。

`POST /ai/assistants/tests` — 必需参数：`name`、`destination`、`instructions`、`rubric`

```java
import com.telnyx.sdk.models.ai.assistants.tests.AssistantTest;
import com.telnyx.sdk.models.ai.assistants.tests.TestCreateParams;

TestCreateParams params = TestCreateParams.builder()
    .destination("+15551234567")
    .instructions("Act as a frustrated customer who received a damaged product. Ask for a refund and escalate if not satisfied with the initial response.")
    .name("Customer Support Bot Test")
    .addRubric(TestCreateParams.Rubric.builder()
        .criteria("Assistant responds within 30 seconds")
        .name("Response Time")
        .build())
    .addRubric(TestCreateParams.Rubric.builder()
        .criteria("Provides correct product information")
        .name("Accuracy")
        .build())
    .build();
AssistantTest assistantTest = client.ai().assistants().tests().create(params);
```

## 获取所有测试套件名称

检索当前用户可用的所有测试套件名称。

`GET /ai/assistants/tests/test-suites`

```java
import com.telnyx.sdk.models.ai.assistants.tests.testsuites.TestSuiteListParams;
import com.telnyx.sdk.models.ai.assistants.tests.testsuites.TestSuiteListResponse;

TestSuiteListResponse testSuites = client.ai().assistants().tests().testSuites().list();
```

## 获取测试套件运行历史

检索特定测试套件的运行历史（支持分页和过滤）

`GET /ai/assistants/tests/test-suites/{suite_name}/runs`

```java
import com.telnyx.sdk.models.ai.assistants.tests.testsuites.runs.RunListPage;
import com.telnyx.sdk.models.ai.assistants.tests.testsuites.runs.RunListParams;

RunListPage page = client.ai().assistants().tests().testSuites().runs().list("suite_name");
```

## 触发测试套件执行

批量执行特定测试套件中的所有测试。

`POST /ai/assistants/tests/test-suites/{suite_name}/runs`

```java
import com.telnyx.sdk.models.ai.assistants.tests.runs.TestRunResponse;
import com.telnyx.sdk.models.ai.assistants.tests.testsuites.runs.RunTriggerParams;

List<TestRunResponse> testRunResponses = client.ai().assistants().tests().testSuites().runs().trigger("suite_name");
```

## 获取辅助工具测试信息

检索特定辅助工具测试的详细信息。

`GET /ai/assistants/tests/{test_id}`

```java
import com.telnyx.sdk.models.ai.assistants.tests.AssistantTest;
import com.telnyx.sdk.models.ai.assistants.tests.TestRetrieveParams;

AssistantTest assistantTest = client.ai().assistants().tests().retrieve("test_id");
```

## 更新辅助工具测试配置

更新现有辅助工具测试的配置。

`PUT /ai/assistants/tests/{test_id}`

```java
import com.telnyx.sdk.models.ai.assistants.tests.AssistantTest;
import com.telnyx.sdk.models.ai.assistants.tests.TestUpdateParams;

AssistantTest assistantTest = client.ai().assistants().tests().update("test_id");
```

## 删除辅助工具测试

永久删除辅助工具测试及其所有相关数据。

`DELETE /ai/assistants/tests/{test_id}`

```java
import com.telnyx.sdk.models.ai.assistants.tests.TestDeleteParams;

client.ai().assistants().tests().delete("test_id");
```

## 获取特定测试的运行历史

检索特定辅助工具测试的运行历史（支持分页和过滤）。

`GET /ai/assistants/tests/{test_id}/runs`

```java
import com.telnyx.sdk.models.ai.assistants.tests.runs.RunListPage;
import com.telnyx.sdk.models.ai.assistants.tests.runs.RunListParams;

RunListPage page = client.ai().assistants().tests().runs().list("test_id");
```

## 触发手动测试运行

立即执行特定的辅助工具测试。

`POST /ai/assistants/tests/{test_id}/runs`

```java
import com.telnyx.sdk.models.ai.assistants.tests.runs.RunTriggerParams;
import com.telnyx.sdk.models.ai.assistants.tests.runs.TestRunResponse;

TestRunResponse testRunResponse = client.ai().assistants().tests().runs().trigger("test_id");
```

## 获取特定测试运行的详细信息

检索特定测试运行的详细信息。

`GET /ai/assistants/tests/{test_id}/runs/{run_id}`

```java
import com.telnyx.sdk.models.ai.assistants.tests.runs.RunRetrieveParams;
import com.telnyx.sdk.models.ai.assistants.tests.runs.TestRunResponse;

RunRetrieveParams params = RunRetrieveParams.builder()
    .testId("test_id")
    .runId("run_id")
    .build();
TestRunResponse testRunResponse = client.ai().assistants().tests().runs().retrieve(params);
```

## 获取辅助工具的所有版本

检索特定辅助工具的所有版本及其完整配置和元数据。

`GET /ai/assistants/{assistant_id}/versions`

```java
import com.telnyx.sdk.models.ai.assistants.AssistantsList;
import com.telnyx.sdk.models.ai.assistants.versions.VersionListParams;

AssistantsList assistantsList = client.ai().assistants().versions().list("assistant_id");
```

## 获取特定辅助工具的版本

通过 `assistant_id` 和 `version_id` 获取特定版本的辅助工具。

`GET /ai/assistants/{assistant_id}/versions/{version_id}`

```java
import com.telnyx.sdk.models.ai.assistants.InferenceEmbedding;
import com.telnyx.sdk.models.ai.assistants.versions.VersionRetrieveParams;

VersionRetrieveParams params = VersionRetrieveParams.builder()
    .assistantId("assistant_id")
    .versionId("version_id")
    .build();
InferenceEmbedding assistant = client.ai().assistants().versions().retrieve(params);
```

## 更新特定辅助工具的版本

更新特定辅助工具版本的配置。

`POST /ai/assistants/{assistant_id}/versions/{version_id}`

```java
import com.telnyx.sdk.models.ai.assistants.InferenceEmbedding;
import com.telnyx.sdk.models.ai.assistants.versions.UpdateAssistant;
import com.telnyx.sdk.models.ai.assistants.versions.VersionUpdateParams;

VersionUpdateParams params = VersionUpdateParams.builder()
    .assistantId("assistant_id")
    .versionId("version_id")
    .updateAssistant(UpdateAssistant.builder().build())
    .build();
InferenceEmbedding assistant = client.ai().assistants().versions().update(params);
```

## 删除特定辅助工具的版本

永久删除特定版本的辅助工具。

`DELETE /ai/assistants/{assistant_id}/versions/{version_id}`

```java
import com.telnyx.sdk.models.ai.assistants.versions.VersionDeleteParams;

VersionDeleteParams params = VersionDeleteParams.builder()
    .assistantId("assistant_id")
    .versionId("version_id")
    .build();
client.ai().assistants().versions().delete(params);
```

## 将辅助工具版本提升为主版本

将特定版本提升为辅助工具的主/当前版本。

`POST /ai/assistants/{assistant_id}/versions/{version_id}/promote`

```java
import com.telnyx.sdk.models.ai.assistants.InferenceEmbedding;
import com.telnyx.sdk.models.ai.assistants.versions.VersionPromoteParams;

VersionPromoteParams params = VersionPromoteParams.builder()
    .assistantId("assistant_id")
    .versionId("version_id")
    .build();
InferenceEmbedding assistant = client.ai().assistants().versions().promote(params);
```

## 获取辅助工具的 Canary 部署配置

获取辅助工具的 Canary 部署配置。

`GET /ai/assistants/{assistant_id}/canary-deploys`

```java
import com.telnyx.sdk.models.ai.assistants.canarydeploys.CanaryDeployResponse;
import com.telnyx.sdk.models.ai.assistants.canarydeploys.CanaryDeployRetrieveParams;

CanaryDeployResponse canaryDeployResponse = client.ai().assistants().canaryDeploys().retrieve("assistant_id");
```

## 创建 Canary 部署配置

为辅助工具创建 Canary 部署配置。

`POST /ai/assistants/{assistant_id}/canary-deploys` — 必需参数：`versions`

```java
import com.telnyx.sdk.models.ai.assistants.canarydeploys.CanaryDeploy;
import com.telnyx.sdk.models.ai.assistants.canarydeploys.CanaryDeployCreateParams;
import com.telnyx.sdk.models.ai.assistants.canarydeploys.CanaryDeployResponse;
import com.telnyx.sdk.models.ai.assistants.canarydeploys.VersionConfig;

CanaryDeployCreateParams params = CanaryDeployCreateParams.builder()
    .assistantId("assistant_id")
    .canaryDeploy(CanaryDeploy.builder()
        .addVersion(VersionConfig.builder()
            .percentage(1.0)
            .versionId("version_id")
            .build())
        .build())
    .build();
CanaryDeployResponse canaryDeployResponse = client.ai().assistants().canaryDeploys().create(params);
```

## 更新 Canary 部署配置

更新辅助工具的 Canary 部署配置。

`PUT /ai/assistants/{assistant_id}/canary-deploys` — 必需参数：`versions`

```java
import com.telnyx.sdk.models.ai.assistants.canarydeploys.CanaryDeploy;
import com.telnyx.sdk.models.ai.assistants.canarydeploys.CanaryDeployResponse;
import com.telnyx.sdk.models.ai.assistants.canarydeploys.CanaryDeployUpdateParams;
import com.telnyx.sdk.models.ai.assistants.canarydeploys.VersionConfig;

CanaryDeployUpdateParams params = CanaryDeployUpdateParams.builder()
    .assistantId("assistant_id")
    .canaryDeploy(CanaryDeploy.builder()
        .addVersion(VersionConfig.builder()
            .percentage(1.0)
            .versionId("version_id")
            .build())
        .build())
    .build();
CanaryDeployResponse canaryDeployResponse = client.ai().assistants().canaryDeploys().update(params);
```

## 删除 Canary 部署配置

删除辅助工具的 Canary 部署配置。

`DELETE /ai/assistants/{assistant_id}/canary-deploys`

```java
import com.telnyx.sdk.models.ai.assistants.canarydeploys.CanaryDeployDeleteParams;

client.ai().assistants().canaryDeploys().delete("assistant_id");
```

## 获取辅助工具的 Texml 文件

通过 `assistant_id` 获取辅助工具的 Texml 文件。

`GET /ai/assistants/{assistant_id}/texml`

```java
import com.telnyx.sdk.models.ai.assistants.AssistantGetTexmlParams;

String response = client.ai().assistants().getTexml("assistant_id");
```

## 测试辅助工具

测试辅助工具的 Webhook 功能。

`POST /ai/assistants/{assistant_id}/tools/{tool_id}/test`

```java
import com.telnyx.sdk.models.ai.assistants.tools.ToolTestParams;
import com.telnyx.sdk.models.ai.assistants.tools.ToolTestResponse;

ToolTestParams params = ToolTestParams.builder()
    .assistantId("assistant_id")
    .toolId("tool_id")
    .build();
ToolTestResponse response = client.ai().assistants().tools().test(params);
```

## 列出集成

列出所有可用的集成。

`GET /ai/integrations`

```java
import com.telnyx.sdk.models.ai.integrations.IntegrationListParams;
import com.telnyx.sdk.models.ai.integrations.IntegrationListResponse;

IntegrationListResponse integrations = client.ai().integrations().list();
```

## 列出用户设置的集成

列出用户设置的集成。

`GET /ai/integrations/connections`

```java
import com.telnyx.sdk.models.ai.integrations.connections.ConnectionListParams;
import com.telnyx.sdk.models.ai.integrations.connections.ConnectionListResponse;

ConnectionListResponse connections = client.ai().integrations().connections().list();
```

## 根据 ID 获取用户集成连接信息

获取用户设置的集成连接信息。

`GET /ai/integrations/connections/{user_connection_id}`

```java
import com.telnyx.sdk.models.ai.integrations.connections.ConnectionRetrieveParams;
import com.telnyx.sdk.models.ai.integrations.connections.ConnectionRetrieveResponse;

ConnectionRetrieveResponse connection = client.ai().integrations().connections().retrieve("user_connection_id");
```

## 删除集成连接

删除特定的集成连接。

`DELETE /ai/integrations/connections/{user_connection_id}`

```java
import com.telnyx.sdk.models.ai.integrations.connections.ConnectionDeleteParams;

client.ai().integrations().connections().delete("user_connection_id");
```

## 根据 ID 获取集成信息

检索集成的详细信息。

`GET /ai/integrations/{integration_id}`

```java
import com.telnyx.sdk.models.ai.integrations.IntegrationRetrieveParams;
import com.telnyx.sdk.models.ai.integrations.IntegrationRetrieveResponse;

IntegrationRetrieveResponse integration = client.ai().integrations().retrieve("integration_id");
```

## 列出 MCP 服务器

检索 MCP 服务器的列表。

`GET /ai/mcp_servers`

```java
import com.telnyx.sdk.models.ai.mcpservers.McpServerListPage;
import com.telnyx.sdk.models.ai.mcpservers.McpServerListParams;

McpServerListPage page = client.ai().mcpServers().list();
```

## 创建 MCP 服务器

创建一个新的 MCP 服务器。

`POST /ai/mcp_servers` — 必需参数：`name`、`type`、`url`

```java
import com.telnyx.sdk.models.ai.mcpservers.McpServerCreateParams;
import com.telnyx.sdk.models.ai.mcpservers.McpServerCreateResponse;

McpServerCreateParams params = McpServerCreateParams.builder()
    .name("name")
    .type("type")
    .url("url")
    .build();
McpServerCreateResponse mcpServer = client.ai().mcpServers().create(params);
```

## 获取 MCP 服务器信息

检索特定 MCP 服务器的详细信息。

`GET /ai/mcp_servers/{mcp_server_id}`

```java
import com.telnyx.sdk.models.ai.mcpservers.McpServerRetrieveParams;
import com.telnyx.sdk.models.ai.mcpservers.McpServerRetrieveResponse;

McpServerRetrieveResponse mcpServer = client.ai().mcpServers().retrieve("mcp_server_id");
```

## 更新 MCP 服务器

更新现有的 MCP 服务器。

`PUT /ai/mcp_servers/{mcp_server_id}`

```java
import com.telnyx.sdk.models.ai.mcpservers.McpServerUpdateParams;
import com.telnyx.sdk.models.ai.mcpservers.McpServerUpdateResponse;

McpServerUpdateResponse mcpServer = client.ai().mcpServers().update("mcp_server_id");
```

## 删除 MCP 服务器

删除特定的 MCP 服务器。

`DELETE /ai/mcp_servers/{mcp_server_id}`

```java
import com.telnyx.sdk.models.ai.mcpservers.McpServerDeleteParams;

client.ai().mcpServers().delete("mcp_server_id");
```
```