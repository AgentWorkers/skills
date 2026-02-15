---
name: telnyx-ai-assistants-ruby
description: >-
  Create and manage AI voice assistants with custom personalities, knowledge
  bases, and tool integrations. This skill provides Ruby SDK examples.
metadata:
  author: telnyx
  product: ai-assistants
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx AI 助手 - Ruby

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

以下所有示例均假设 `client` 已按照上述方式初始化。

## 列出助手

检索用户配置的所有 AI 助手。

`GET /ai/assistants`

```ruby
assistants_list = client.ai.assistants.list

puts(assistants_list)
```

## 创建助手

创建一个新的 AI 助手。

`POST /ai/assistants` — 必需参数：`name`、`model`、`instructions`

```ruby
assistant = client.ai.assistants.create(instructions: "instructions", model: "model", name: "name")

puts(assistant)
```

## 获取助手信息

通过 `assistant_id` 检索 AI 助手的配置信息。

`GET /ai/assistants/{assistant_id}`

```ruby
assistant = client.ai.assistants.retrieve("assistant_id")

puts(assistant)
```

## 更新助手信息

更新 AI 助手的属性。

`POST /ai/assistants/{assistant_id}`

```ruby
assistant = client.ai.assistants.update("assistant_id")

puts(assistant)
```

## 删除助手

通过 `assistant_id` 删除 AI 助手。

`DELETE /ai/assistants/{assistant_id}`

```ruby
assistant = client.ai.assistants.delete("assistant_id")

puts(assistant)
```

## 助手聊天（测试版）

此端点允许客户端向特定的 AI 助手发送聊天消息。

`POST /ai/assistants/{assistant_id}/chat` — 必需参数：`content`、`conversation_id`

```ruby
response = client.ai.assistants.chat(
  "assistant_id",
  content: "Tell me a joke about cats",
  conversation_id: "42b20469-1215-4a9a-8964-c36f66b406f4"
)

puts(response)
```

## 助手短信聊天

为助手发送短信。

`POST /ai/assistants/{assistant_id}/chat/sms` — 必需参数：`from`、`to`

```ruby
response = client.ai.assistants.send_sms("assistant_id", from: "from", to: "to")

puts(response)
```

## 复制助手

复制现有的助手（不包括电话和消息设置）。

`POST /ai/assistants/{assistant_id}/clone`

```ruby
assistant = client.ai.assistants.clone_("assistant_id")

puts(assistant)
```

## 从外部提供商导入助手

从外部提供商导入助手。

`POST /ai/assistants/import` — 必需参数：`provider`、`api_key_ref`

```ruby
assistants_list = client.ai.assistants.imports(api_key_ref: "api_key_ref", provider: :elevenlabs)

puts(assistants_list)
```

## 列出计划事件

获取助手的计划事件（支持分页和过滤）

`GET /ai/assistants/{assistant_id}/scheduled_events`

```ruby
page = client.ai.assistants.scheduled_events.list("assistant_id")

puts(page)
```

## 创建计划事件

为助手创建计划事件。

`POST /ai/assistants/{assistant_id}/scheduled_events` — 必需参数：`telnyx_conversation_channel`、`telnyx_end_user_target`、`telnyx_agent_target`、`scheduled_at_fixed_datetime`

```ruby
scheduled_event_response = client.ai.assistants.scheduled_events.create(
  "assistant_id",
  scheduled_at_fixed_datetime: "2025-04-15T13:07:28.764Z",
  telnyx_agent_target: "telnyx_agent_target",
  telnyx_conversation_channel: :phone_call,
  telnyx_end_user_target: "telnyx_end_user_target"
)

puts(scheduled_event_response)
```

## 获取计划事件信息

通过事件 ID 检索计划事件信息。

`GET /ai/assistants/{assistant_id}/scheduled_events/{event_id}`

```ruby
scheduled_event_response = client.ai.assistants.scheduled_events.retrieve("event_id", assistant_id: "assistant_id")

puts(scheduled_event_response)
```

## 删除计划事件

如果事件尚未执行，此操作将取消该事件。

`DELETE /ai/assistants/{assistant_id}/scheduled_events/{event_id}`

```ruby
result = client.ai.assistants.scheduled_events.delete("event_id", assistant_id: "assistant_id")

puts(result)
```

## 列出助手测试（支持分页）

检索助手测试的列表（支持可选的过滤功能）。

`GET /ai/assistants/tests`

```ruby
page = client.ai.assistants.tests.list

puts(page)
```

## 创建新的助手测试

创建用于评估 AI 助手性能的测试配置。

`POST /ai/assistants/tests` — 必需参数：`name`、`destination`、`instructions`、`rubric`

```ruby
assistant_test = client.ai.assistants.tests.create(
  destination: "+15551234567",
  instructions: "Act as a frustrated customer who received a damaged product. Ask for a refund and escalate if not satisfied with the initial response.",
  name: "Customer Support Bot Test",
  rubric: [
    {criteria: "Assistant responds within 30 seconds", name: "Response Time"},
    {criteria: "Provides correct product information", name: "Accuracy"}
  ]
)

puts(assistant_test)
```

## 获取所有测试套件名称

检索当前用户可用的所有测试套件名称。

`GET /ai/assistants/tests/test-suites`

```ruby
test_suites = client.ai.assistants.tests.test_suites.list

puts(test_suites)
```

## 获取测试套件运行历史

检索特定测试套件的运行历史（支持分页和过滤选项）。

`GET /ai/assistants/tests/test-suites/{suite_name}/runs`

```ruby
page = client.ai.assistants.tests.test_suites.runs.list("suite_name")

puts(page)
```

## 触发测试套件执行

批量执行特定测试套件中的所有测试。

`POST /ai/assistants/tests/test-suites/{suite_name}/runs`

```ruby
test_run_responses = client.ai.assistants.tests.test_suites.runs.trigger("suite_name")

puts(test_run_responses)
```

## 获取助手测试信息

检索特定助手测试的详细信息。

`GET /ai/assistants/tests/{test_id}`

```ruby
assistant_test = client.ai.assistants.tests.retrieve("test_id")

puts(assistant_test)
```

## 更新助手测试配置

更新现有助手测试的配置。

`PUT /ai/assistants/tests/{test_id}`

```ruby
assistant_test = client.ai.assistants.tests.update("test_id")

puts(assistant_test)
```

## 删除助手测试

永久删除助手测试及其所有关联数据。

`DELETE /ai/assistants/tests/{test_id}`

```ruby
result = client.ai.assistants.tests.delete("test_id")

puts(result)
```

## 获取特定测试的运行历史

检索特定助手测试的运行历史（支持分页和过滤选项）。

`GET /ai/assistants/tests/{test_id}/runs`

```ruby
page = client.ai.assistants.tests.runs.list("test_id")

puts(page)
```

## 触发手动测试运行

立即执行特定的助手测试。

`POST /ai/assistants/tests/{test_id}/runs`

```ruby
test_run_response = client.ai.assistants.tests.runs.trigger("test_id")

puts(test_run_response)
```

## 获取特定测试运行的详细信息

检索特定测试运行的详细信息。

`GET /ai/assistants/tests/{test_id}/runs/{run_id}`

```ruby
test_run_response = client.ai.assistants.tests.runs.retrieve("run_id", test_id: "test_id")

puts(test_run_response)
```

## 获取助手的所有版本

检索特定助手的所有版本及其完整配置和元数据。

`GET /ai/assistants/{assistant_id}/versions`

```ruby
assistants_list = client.ai.assistants.versions.list("assistant_id")

puts(assistants_list)
```

## 获取特定助手版本

通过 `assistant_id` 和 `version_id` 获取特定版本的助手信息。

`GET /ai/assistants/{assistant_id}/versions/{version_id}`

```ruby
assistant = client.ai.assistants.versions.retrieve("version_id", assistant_id: "assistant_id")

puts(assistant)
```

## 更新特定助手版本

更新特定助手版本的配置。

`POST /ai/assistants/{assistant_id}/versions/{version_id}`

```ruby
assistant = client.ai.assistants.versions.update("version_id", assistant_id: "assistant_id")

puts(assistant)
```

## 删除特定助手版本

永久删除特定版本的助手。

`DELETE /ai/assistants/{assistant_id}/versions/{version_id}`

```ruby
result = client.ai.assistants.versions.delete("version_id", assistant_id: "assistant_id")

puts(result)
```

## 将助手版本提升为主版本

将特定版本提升为助手的主/当前版本。

`POST /ai/assistants/{assistant_id}/versions/{version_id}/promote`

```ruby
assistant = client.ai.assistants.versions.promote("version_id", assistant_id: "assistant_id")

puts(assistant)
```

## 获取 Canary 部署配置

获取助手的 Canary 部署配置。

`GET /ai/assistants/{assistant_id}/canary-deploys`

```ruby
canary_deploy_response = client.ai.assistants.canary_deploys.retrieve("assistant_id")

puts(canary_deploy_response)
```

## 创建 Canary 部署

为助手创建 Canary 部署配置。

`POST /ai/assistants/{assistant_id}/canary-deploys` — 必需参数：`versions`

```ruby
canary_deploy_response = client.ai.assistants.canary_deploys.create(
  "assistant_id",
  versions: [{percentage: 1, version_id: "version_id"}]
)

puts(canary_deploy_response)
```

## 更新 Canary 部署配置

更新助手的 Canary 部署配置。

`PUT /ai/assistants/{assistant_id}/canary-deploys` — 必需参数：`versions`

```ruby
canary_deploy_response = client.ai.assistants.canary_deploys.update(
  "assistant_id",
  versions: [{percentage: 1, version_id: "version_id"}]
)

puts(canary_deploy_response)
```

## 删除 Canary 部署配置

删除助手的 Canary 部署配置。

`DELETE /ai/assistants/{assistant_id}/canary-deploys`

```ruby
result = client.ai.assistants.canary_deploys.delete("assistant_id")

puts(result)
```

## 获取助手的 Texml 文件

通过 `assistant_id` 获取助手的 Texml 文件。

`GET /ai/assistants/{assistant_id}/texml`

```ruby
response = client.ai.assistants.get_texml("assistant_id")

puts(response)
```

## 测试助手工具

测试助手的 Webhook 工具。

`POST /ai/assistants/{assistant_id}/tools/{tool_id}/test`

```ruby
response = client.ai.assistants.tools.test_("tool_id", assistant_id: "assistant_id")

puts(response)
```

## 列出集成

列出所有可用的集成。

`GET /ai/integrations`

```ruby
integrations = client.ai.integrations.list

puts(integrations)
```

## 列出用户集成

列出用户的集成设置。

`GET /ai/integrations/connections`

```ruby
connections = client.ai.integrations.connections.list

puts(connections)
```

## 根据 ID 获取用户集成连接信息

获取用户的集成连接信息。

`GET /ai/integrations/connections/{user_connection_id}`

```ruby
connection = client.ai.integrations.connections.retrieve("user_connection_id")

puts(connection)
```

## 删除集成连接

删除特定的集成连接。

`DELETE /ai/integrations/connections/{user_connection_id}`

```ruby
result = client.ai.integrations.connections.delete("user_connection_id")

puts(result)
```

## 根据 ID 获取集成信息

检索集成的详细信息。

`GET /ai/integrations/{integration_id}`

```ruby
integration = client.ai.integrations.retrieve("integration_id")

puts(integration)
```

## 列出 MCP 服务器

列出所有的 MCP 服务器。

`GET /ai/mcp_servers`

```ruby
page = client.ai.mcp_servers.list

puts(page)
```

## 创建 MCP 服务器

创建新的 MCP 服务器。

`POST /ai/mcp_servers` — 必需参数：`name`、`type`、`url`

```ruby
mcp_server = client.ai.mcp_servers.create(name: "name", type: "type", url: "url")

puts(mcp_server)
```

## 获取 MCP 服务器信息

检索特定 MCP 服务器的详细信息。

`GET /ai/mcp_servers/{mcp_server_id}`

```ruby
mcp_server = client.ai.mcp_servers.retrieve("mcp_server_id")

puts(mcp_server)
```

## 更新 MCP 服务器

更新现有的 MCP 服务器。

`PUT /ai/mcp_servers/{mcp_server_id}`

```ruby
mcp_server = client.ai.mcp_servers.update("mcp_server_id")

puts(mcp_server)
```

## 删除 MCP 服务器

删除特定的 MCP 服务器。

`DELETE /ai/mcp_servers/{mcp_server_id}`

```ruby
result = client.ai.mcp_servers.delete("mcp_server_id")

puts(result)
```