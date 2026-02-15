---
name: telnyx-ai-assistants-javascript
description: >-
  Create and manage AI voice assistants with custom personalities, knowledge
  bases, and tool integrations. This skill provides JavaScript SDK examples.
metadata:
  author: telnyx
  product: ai-assistants
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx AI 助手 - JavaScript

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

以下所有示例均假设 `client` 已经按照上述方式初始化。

## 列出助手

检索用户配置的所有 AI 助手。

`GET /ai/assistants`

```javascript
const assistantsList = await client.ai.assistants.list();

console.log(assistantsList.data);
```

## 创建助手

创建一个新的 AI 助手。

`POST /ai/assistants` — 必需参数：`name`、`model`、`instructions`

```javascript
const assistant = await client.ai.assistants.create({
  instructions: 'instructions',
  model: 'model',
  name: 'name',
});

console.log(assistant.id);
```

## 获取助手信息

通过 `assistant_id` 检索 AI 助手的配置信息。

`GET /ai/assistants/{assistant_id}`

```javascript
const assistant = await client.ai.assistants.retrieve('assistant_id');

console.log(assistant.id);
```

## 更新助手信息

更新 AI 助手的属性。

`POST /ai/assistants/{assistant_id}`

```javascript
const assistant = await client.ai.assistants.update('assistant_id');

console.log(assistant.id);
```

## 删除助手

通过 `assistant_id` 删除 AI 助手。

`DELETE /ai/assistants/{assistant_id}`

```javascript
const assistant = await client.ai.assistants.delete('assistant_id');

console.log(assistant.id);
```

## 助手聊天（测试版）

此端点允许客户端向特定的 AI 助手发送聊天消息。

`POST /ai/assistants/{assistant_id}/chat` — 必需参数：`content`、`conversation_id`

```javascript
const response = await client.ai.assistants.chat('assistant_id', {
  content: 'Tell me a joke about cats',
  conversation_id: '42b20469-1215-4a9a-8964-c36f66b406f4',
});

console.log(response.content);
```

## 助手短信聊天

为助手发送短信。

`POST /ai/assistants/{assistant_id}/chat/sms` — 必需参数：`from`、`to`

```javascript
const response = await client.ai.assistants.sendSMS('assistant_id', { from: 'from', to: 'to' });

console.log(response.conversation_id);
```

## 复制助手

复制现有的助手（不包括电话和消息设置）。

`POST /ai/assistants/{assistant_id}/clone`

```javascript
const assistant = await client.ai.assistants.clone('assistant_id');

console.log(assistant.id);
```

## 从外部提供商导入助手

从外部提供商导入助手。

`POST /ai/assistants/import` — 必需参数：`provider`、`api_key_ref`

```javascript
const assistantsList = await client.ai.assistants.imports({
  api_key_ref: 'api_key_ref',
  provider: 'elevenlabs',
});

console.log(assistantsList.data);
```

## 列出计划事件

获取助手的计划事件（支持分页和过滤）

`GET /ai/assistants/{assistant_id}/scheduled_events`

```javascript
// Automatically fetches more pages as needed.
for await (const scheduledEventListResponse of client.ai.assistants.scheduledEvents.list(
  'assistant_id',
)) {
  console.log(scheduledEventListResponse);
}
```

## 创建计划事件

为助手创建计划事件。

`POST /ai/assistants/{assistant_id}/scheduled_events` — 必需参数：`telnyx_conversation_channel`、`telnyx_end_user_target`、`telnyx_agent_target`、`scheduled_at_fixed_datetime`

```javascript
const scheduledEventResponse = await client.ai.assistants.scheduledEvents.create('assistant_id', {
  scheduled_at_fixed_datetime: '2025-04-15T13:07:28.764Z',
  telnyx_agent_target: 'telnyx_agent_target',
  telnyx_conversation_channel: 'phone_call',
  telnyx_end_user_target: 'telnyx_end_user_target',
});

console.log(scheduledEventResponse);
```

## 获取计划事件信息

通过事件 ID 检索计划事件信息。

`GET /ai/assistants/{assistant_id}/scheduled_events/{event_id}`

```javascript
const scheduledEventResponse = await client.ai.assistants.scheduledEvents.retrieve('event_id', {
  assistant_id: 'assistant_id',
});

console.log(scheduledEventResponse);
```

## 删除计划事件

如果事件尚未执行，此操作将取消该事件。

`DELETE /ai/assistants/{assistant_id}/scheduled_events/{event_id}`

```javascript
await client.ai.assistants.scheduledEvents.delete('event_id', { assistant_id: 'assistant_id' });
```

## 列出助手测试（支持分页）

检索助手测试的列表（支持可选的过滤条件）

`GET /ai/assistants/tests`

```javascript
// Automatically fetches more pages as needed.
for await (const assistantTest of client.ai.assistants.tests.list()) {
  console.log(assistantTest.test_id);
}
```

## 创建新的助手测试

创建用于评估 AI 助手性能的测试配置。

`POST /ai/assistants/tests` — 必需参数：`name`、`destination`、`instructions`、`rubric`

```javascript
const assistantTest = await client.ai.assistants.tests.create({
  destination: '+15551234567',
  instructions:
    'Act as a frustrated customer who received a damaged product. Ask for a refund and escalate if not satisfied with the initial response.',
  name: 'Customer Support Bot Test',
  rubric: [
    { criteria: 'Assistant responds within 30 seconds', name: 'Response Time' },
    { criteria: 'Provides correct product information', name: 'Accuracy' },
  ],
});

console.log(assistantTest.test_id);
```

## 获取所有测试套件名称

检索当前用户可用的所有测试套件名称。

`GET /ai/assistants/tests/test-suites`

```javascript
const testSuites = await client.ai.assistants.tests.testSuites.list();

console.log(testSuites.data);
```

## 获取测试套件运行历史

检索特定测试套件的运行历史（支持分页和过滤选项）。

`GET /ai/assistants/tests/test-suites/{suite_name}/runs`

```javascript
// Automatically fetches more pages as needed.
for await (const testRunResponse of client.ai.assistants.tests.testSuites.runs.list('suite_name')) {
  console.log(testRunResponse.run_id);
}
```

## 触发测试套件执行

批量执行特定测试套件中的所有测试。

`POST /ai/assistants/tests/test-suites/{suite_name}/runs`

```javascript
const testRunResponses = await client.ai.assistants.tests.testSuites.runs.trigger('suite_name');

console.log(testRunResponses);
```

## 获取助手测试信息

检索特定助手测试的详细信息。

`GET /ai/assistants/tests/{test_id}`

```javascript
const assistantTest = await client.ai.assistants.tests.retrieve('test_id');

console.log(assistantTest.test_id);
```

## 更新助手测试配置

更新现有助手测试的配置。

`PUT /ai/assistants/tests/{test_id}`

```javascript
const assistantTest = await client.ai.assistants.tests.update('test_id');

console.log(assistantTest.test_id);
```

## 删除助手测试

永久删除助手测试及其所有相关数据。

`DELETE /ai/assistants/tests/{test_id}`

```javascript
await client.ai.assistants.tests.delete('test_id');
```

## 获取特定测试的运行历史

检索特定助手测试的运行历史（支持过滤选项）。

`GET /ai/assistants/tests/{test_id}/runs`

```javascript
// Automatically fetches more pages as needed.
for await (const testRunResponse of client.ai.assistants.tests.runs.list('test_id')) {
  console.log(testRunResponse.run_id);
}
```

## 触发手动测试运行

立即执行特定的助手测试。

`POST /ai/assistants/tests/{test_id}/runs`

```javascript
const testRunResponse = await client.ai.assistants.tests.runs.trigger('test_id');

console.log(testRunResponse.run_id);
```

## 获取特定测试运行的详细信息

检索特定测试运行的详细信息。

`GET /ai/assistants/tests/{test_id}/runs/{run_id}`

```javascript
const testRunResponse = await client.ai.assistants.tests.runs.retrieve('run_id', {
  test_id: 'test_id',
});

console.log(testRunResponse.run_id);
```

## 获取助手的所有版本

检索特定助手的所有版本及其完整配置和元数据。

`GET /ai/assistants/{assistant_id}/versions`

```javascript
const assistantsList = await client.ai.assistants.versions.list('assistant_id');

console.log(assistantsList.data);
```

## 获取特定助手版本

通过 `assistant_id` 和 `version_id` 获取特定版本的助手信息。

`GET /ai/assistants/{assistant_id}/versions/{version_id}`

```javascript
const assistant = await client.ai.assistants.versions.retrieve('version_id', {
  assistant_id: 'assistant_id',
});

console.log(assistant.id);
```

## 更新特定助手版本

更新特定助手版本的配置。

`POST /ai/assistants/{assistant_id}/versions/{version_id}`

```javascript
const assistant = await client.ai.assistants.versions.update('version_id', {
  assistant_id: 'assistant_id',
});

console.log(assistant.id);
```

## 删除特定助手版本

永久删除特定版本的助手。

`DELETE /ai/assistants/{assistant_id}/versions/{version_id}`

```javascript
await client.ai.assistants.versions.delete('version_id', { assistant_id: 'assistant_id' });
```

## 将特定版本提升为主版本

将特定版本提升为助手的主/当前版本。

`POST /ai/assistants/{assistant_id}/versions/{version_id}/promote`

```javascript
const assistant = await client.ai.assistants.versions.promote('version_id', {
  assistant_id: 'assistant_id',
});

console.log(assistant.id);
```

## 获取 Canary 部署配置

获取助手的 Canary 部署配置。

`GET /ai/assistants/{assistant_id}/canary-deploys`

```javascript
const canaryDeployResponse = await client.ai.assistants.canaryDeploys.retrieve('assistant_id');

console.log(canaryDeployResponse.assistant_id);
```

## 创建 Canary 部署

为助手创建 Canary 部署配置。

`POST /ai/assistants/{assistant_id}/canary-deploys` — 必需参数：`versions`

```javascript
const canaryDeployResponse = await client.ai.assistants.canaryDeploys.create('assistant_id', {
  versions: [{ percentage: 1, version_id: 'version_id' }],
});

console.log(canaryDeployResponse.assistant_id);
```

## 更新 Canary 部署配置

更新助手的 Canary 部署配置。

`PUT /ai/assistants/{assistant_id}/canary-deploys` — 必需参数：`versions`

```javascript
const canaryDeployResponse = await client.ai.assistants.canaryDeploys.update('assistant_id', {
  versions: [{ percentage: 1, version_id: 'version_id' }],
});

console.log(canaryDeployResponse.assistant_id);
```

## 删除 Canary 部署配置

删除助手的 Canary 部署配置。

`DELETE /ai/assistants/{assistant_id}/canary-deploys`

```javascript
await client.ai.assistants.canaryDeploys.delete('assistant_id');
```

## 获取助手的 Texml 文件

通过 `assistant_id` 获取助手的 Texml 文件。

`GET /ai/assistants/{assistant_id}/texml`

```javascript
const response = await client.ai.assistants.getTexml('assistant_id');

console.log(response);
```

## 测试助手工具

测试助手的 Webhook 工具。

`POST /ai/assistants/{assistant_id}/tools/{tool_id}/test`

```javascript
const response = await client.ai.assistants.tools.test('tool_id', { assistant_id: 'assistant_id' });

console.log(response.data);
```

## 列出集成

列出所有可用的集成。

`GET /ai/integrations`

```javascript
const integrations = await client.ai.integrations.list();

console.log(integrations.data);
```

## 列出用户集成

列出用户的集成设置。

`GET /ai/integrations/connections`

```javascript
const connections = await client.ai.integrations.connections.list();

console.log(connections.data);
```

## 根据 ID 获取用户集成连接信息

获取用户的集成连接信息。

`GET /ai/integrations/connections/{user_connection_id}`

```javascript
const connection = await client.ai.integrations.connections.retrieve('user_connection_id');

console.log(connection.data);
```

## 删除集成连接

删除特定的集成连接。

`DELETE /ai/integrations/connections/{user_connection_id}`

```javascript
await client.ai.integrations.connections.delete('user_connection_id');
```

## 根据 ID 获取集成详情

检索集成的详细信息。

`GET /ai/integrations/{integration_id}`

```javascript
const integration = await client.ai.integrations.retrieve('integration_id');

console.log(integration.id);
```

## 列出 MCP 服务器

列出所有的 MCP 服务器。

`GET /ai/mcp_servers`

```javascript
// Automatically fetches more pages as needed.
for await (const mcpServerListResponse of client.ai.mcpServers.list()) {
  console.log(mcpServerListResponse.id);
}
```

## 创建 MCP 服务器

创建一个新的 MCP 服务器。

`POST /ai/mcp_servers` — 必需参数：`name`、`type`、`url`

```javascript
const mcpServer = await client.ai.mcpServers.create({
  name: 'name',
  type: 'type',
  url: 'url',
});

console.log(mcpServer.id);
```

## 获取 MCP 服务器信息

检索特定 MCP 服务器的详细信息。

`GET /ai/mcp_servers/{mcp_server_id}`

```javascript
const mcpServer = await client.ai.mcpServers.retrieve('mcp_server_id');

console.log(mcpServer.id);
```

## 更新 MCP 服务器

更新现有的 MCP 服务器。

`PUT /ai/mcp_servers/{mcp_server_id}`

```javascript
const mcpServer = await client.ai.mcpServers.update('mcp_server_id');

console.log(mcpServer.id);
```

## 删除 MCP 服务器

删除特定的 MCP 服务器。

`DELETE /ai/mcp_servers/{mcp_server_id}`

```javascript
await client.ai.mcpServers.delete('mcp_server_id');
```
```