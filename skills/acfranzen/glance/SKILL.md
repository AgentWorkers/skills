---
name: glance
description: "创建、更新和管理 Glance 仪表板小部件。适用于用户需要以下操作的情况：向仪表板添加内容、创建新的小部件、以可视化方式跟踪数据、显示指标/统计信息、展示 API 数据或监控使用情况。"
metadata:
  openclaw:
    emoji: "🖥️"
    homepage: "https://github.com/acfranzen/glance"
    requires:
      env: ["GLANCE_URL"]
      bins: ["curl"]
    primaryEnv: GLANCE_URL
---

# Glance

这是一个可扩展的AI个人仪表盘工具，支持使用自然语言创建自定义小部件，数据收集工作由AI完成。

## 主要功能

- **自定义小部件**：通过AI自动生成JSX代码来创建小部件。
- **数据更新**：AI会定期收集数据并更新到缓存中。
- **仪表盘导出/导入**：可以共享小部件的配置信息。
- **凭证管理**：提供安全的API密钥存储功能。
- **实时更新**：支持通过Webhook触发的小部件即时刷新。

## 快速入门

仪表盘的运行地址为：**http://localhost:3333**

## 配置

请编辑`.env.local`文件：

## 在macOS上安装服务

## 环境变量

| 变量          | 描述                                      | 默认值                          |
|-----------------|-----------------------------------------|-------------------------------------------|
| `PORT`         | 服务器端口                                      | `3333`                          |
| `AUTH_TOKEN`     | API认证所需的令牌                        |                                  |
| `DATABASE_PATH`    | SQLite数据库路径                            | `./data/glance.db`                    |
| `OPENCLAW_GATEWAY_URL` | 用于Webhook的OpenClaw网关地址               |                                      |
| `OPENCLAW_TOKEN`     | OpenClaw认证令牌                             |                                  |

## 系统要求

- Node.js 20及以上版本
- npm或pnpm
- SQLite（已包含在项目中）

---

# 小部件开发

用于创建和管理仪表盘小部件。大多数小部件使用`agent_refresh`机制——数据收集工作由用户自行完成。

## 快速入门

## AI结构化输出生成（必选）

在生成小部件定义时，请使用`docs/schemas/widget-schema.json`中的JSON模式，并指定AI模型的结构化输出格式：
- **Anthropic**：使用`tool_use`命令并指定模式。
- **OpenAI**：使用`response_format: { type: "json_schema", schema }`。

该模式确保在生成过程中所有字段都得到正确填充；格式不正确的数据将无法通过验证。

### 必需字段

每个小部件都必须包含以下字段（模式会强制要求）：

| 字段            | 类型                                      | 备注                          |
|-----------------|-----------------------------------------|-------------------------------------------|
| `name`           | 字符串                                      | 非空，且对用户可见                     |
| `slug`           | 小部件的唯一标识符（小写Kebab-case格式）             |                              |
| `source_code`       | 包含小部件功能的有效JSX代码                   |                              |
| `default_size`       | 小部件的默认尺寸（网格单位）                     |                              |
| `min_size`       | 小部件的最小尺寸（网格单位）                     |                              |
| `fetch.type`       | 数据获取方式（可选值：`server_code`、`webhook`、`agent_refresh`）   |                              |
| `fetchinstructions` | 数据获取的具体指令（仅当`fetch.type`为`agent_refresh`时需要） |                              |
| `fetch.schedule`    | 数据获取的调度时间（仅当`fetch.type`为`agent_refresh`时需要） |                              |
| `data_schema.type`     | 数据结构的JSON模式                         |                              |
| `data_schema.properties` | 数据字段的配置信息                         |                              |
| `credentials`     | 用于存储凭证的数组                         | 如果不需要凭证，则使用`[]`                   |

### 示例：一个有效的小部件定义

---

## ⚠️ 小部件创建注意事项

在认为小部件创建完成之前，必须完成以下所有步骤：

## 参考资料

- **完整的SDK文档**：请参阅Glance仓库中的`docs/widget-sdk.md`。
- **组件列表**：请参阅[references/components.md](references/components.md)。

## 小部件包结构

## 数据获取方式选择

| 数据获取方式        | 适用场景                        | 数据来源                        |
|-------------------|----------------------------------|-------------------------------------------|
| `server_code`       | 小部件直接调用API                        | 小部件 → 服务器 → API                    |
| `agent_refresh`       | 代理定期从外部服务获取数据                   | 代理 → POST到缓存 → 小部件读取                |
| `webhook`        | 外部服务推送数据                         | 外部服务 → POST到缓存 → 小部件读取                |

**建议大多数小部件使用`agent_refresh`方式**——代理会定期从外部服务获取数据并更新到缓存中。

## 第1步：创建小部件定义

**`data_schema`（必填）**用于定义数据结构。缓存中的POST请求会依据此结构进行验证；格式不正确的数据会导致400错误。

> ⚠️ 创建小部件时务必包含`data_schema`字段。这可以确保：
- 缓存中的数据能够被正确验证（格式不匹配时返回400错误）。
- 文档中能清晰说明预期的数据结构。
- AI代理知道如何生成正确的数据格式。

## 第2步：将小部件添加到仪表盘

## 第3步：更新缓存（针对`agent_refresh`方式）

**注意**：如果小部件包含`dataSchema`字段，缓存端点会依据该结构验证数据。格式错误的数据会导致400错误。在数据发送到缓存之前，请务必检查小部件的配置。

## 第4步：浏览器验证（必选）

**提示**：每个小部件在创建和更新后都必须通过浏览器进行验证。

**验证检查项（全部必须满足）：**
- 小部件能正确显示在仪表盘上。
- 标题显示正确。
- 数据能够正确渲染（无加载延迟）。
- 显示的数据与缓存中的数据一致。
- 无错误提示或布局异常。
- “更新时间”字段显示了最新的时间戳。

**常见问题及解决方法：**
| 问题            | 原因                                      | 解决方法                                      |
|-----------------|----------------------------------|-------------------------------------------|
| “正在等待数据...”       | 缓存为空                                      | 向`/api/widgets/{slug}/cache`发送数据请求                 |
| 小部件未显示        | 小部件未添加到仪表盘中                         | 使用`POST /api/widgets/instances`命令添加小部件           |
| 数据错误/过时        | 小部件的slug与数据库中的不符                         | 确保slug与数据库中的匹配                 |
| 布局异常        | `source_code`中的JSX代码有语法错误                         | 检查JSX代码的语法                   |
| 数据获取失败        | 数据验证失败                                     | 修复数据验证问题后再报告成功                 |

## `agent_refresh`方式的小部件代码模板

对于使用`agent_refresh`的小部件，请使用`serverData`属性（而非`useData`钩子）：

**重要提示：**`CustomWidgetWrapper`框架提供了以下功能：
- 带有标题的`<Card>`容器。
- 提供刷新按钮和“更新时间”显示功能。
- 支持加载/错误状态显示。

你的小部件代码只需负责渲染内容——不需要包含`Card`、`CardHeader`或`footer`元素。

**关键区别**：`agent_refresh`方式的小部件通过`serverData`属性接收数据，而不是通过`useData()`函数。代理会将数据发送到`/api/widgets/{slug}/cache`。

## 服务器端代码（旧版本替代方案）

**建议优先使用`agentrefresh`方式**。仅在需要在渲染时执行代码的情况下（较为罕见）才使用`server_code`方式。

## 可用的函数/变量

- `fetch`、`getCredential/provider`、`params`、`console`
- **不建议使用**：`require`、`eval`、`fs`、`process`、`global`。

## 代理数据更新规则

**重要提示**：对于`agentrefresh`方式的小部件，数据收集工作由用户（即OpenClaw代理）完成。
- 用户需要设置定时任务来定期收集数据。
- 使用自己的工具（如pty、exec、浏览器等）来获取数据。
- 将获取到的数据解析为结构化的JSON格式。
- 将数据发送到缓存端点，以便小部件能够显示。

## `agent_refresh`小部件的实现步骤

1. 使用`fetch.type = "agent_refresh"`创建小部件，并指定详细的`fetchinstructions`。
2. 设置一个定时任务，任务名称只需包含小部件的`slug`。
3. 当收到更新请求时，从数据库中获取`fetchinstructions`，然后启动一个子代理来执行数据收集任务。
4. 子代理可以使用各种工具（如`exec`执行shell命令、`pty`调用CLI工具、`browser`进行网页抓取等）来获取数据。
5. 将获取到的数据发送到缓存端点。

## 编写有效的`fetchinstructions`

`fetchinstructions`字段是获取数据方式的唯一依据。请确保指令编写清晰，以便所有子代理都能正确执行数据获取操作。

**示例指令：**
```json
{
  "emails": [{"id": "...", "from": "...", "subject": "...", "summary": "AI生成的内容", "unread": true}],
  "fetchedAt": "ISO时间戳"
}
```

**示例（正确用法）：**
```json
{
  "emails": [{"id": "...", "from": "...", "subject": "...", "summary": "AI生成的内容", "unread": true}],
  "fetchedAt": "ISO时间戳"
}
```

**示例（错误用法）：**
```json
{
  "emails": []
}
```

## 实际应用示例：Claude使用示例

这个小部件用于显示Claude CLI的使用情况。数据是通过在终端中运行`claude /status`命令并查看结果获得的。

**代理的调度任务：**每15分钟执行一次数据更新。

**作为代理，你的职责是**确保小部件显示的是缓存中的数据。

## 代理任务模板（用于数据更新）

在为小部件更新任务启动子代理时，务必包含浏览器验证步骤。

## 缓存端点

**对于`agentrefresh`方式的小部件，用户可以通过UI上的刷新按钮触发即时更新。**

当配置了`OPENCLAW_GATEWAY_URL`和`OPENCLAW_TOKEN`环境变量后，点击刷新按钮会：
1. 将更新请求存储到数据库中（作为轮询的备用方案）。
2. 立即通过`/api/sessions/wake`向OpenClaw发送更新通知。
3. 代理会立即开始更新指定的小部件。

**环境变量设置（添加到`.env.local`文件）：**
```
GLANCE_URL = http://localhost:3333
OPENCLAW_GATEWAY_URL = https://localhost:18789
OPENCLAW_TOKEN = d551fe97...
```

**工作原理：**
1. 用户点击刷新按钮。
2. Glance向`/api/widgets/{slug}/refresh`发送请求。
3. 如果配置了Webhook，Glance会立即通知OpenClaw更新小部件。
4. 代理会获取最新数据并更新到缓存中。
5. 小部件会重新渲染并显示更新后的数据。

**响应内容包含Webhook的状态信息：**
```
{
  "status": "更新成功"
}
```

**注意事项：**
- **务必包含`fetchedAt`时间戳**。
- **错误发生时不要覆盖缓存中的数据**——应使用缓存的旧数据。
- **使用主会话的定时任务**——确保数据收集工作由用户自己完成，而不是由单独的代理处理。

## 环境变量示例：

| 变量          | 描述                                      | 示例值                                      |
|-----------------|-----------------------------------------|-------------------------------------------|
| GLANCE_URL       | Glance服务器地址                             | http://localhost:3333                          |
| GLANCE_DATA      | SQLite数据库路径                             | /tmp/glance-test/data                          |
| OPENCLAW_GATEWAY_URL | 用于Webhook更新的OpenClaw网关地址             | https://localhost:18789                          |
| OPENCLAW_TOKEN     | OpenClaw认证令牌                             | d551fe97...                          |
```

## 最新更新（2026年2月）：

- **Webhook更新功能已生效**：Glance会向OpenClaw网关发送更新请求，代理会立即开始更新。
- **简单的定时任务消息**：只需发送`⚡ WIDGET REFRESH: {slug}`，代理会根据消息中的`slug`查找相应的更新指令。
- **AI生成的摘要**：对于邮件摘要，需要使用AI来生成；不能依赖外部API。
- **iCloud日历同步**：`gog calendar`不适用于iCloud，建议使用`/opt/homebrew/bin/icalBuddy`工具。
- **天气数据获取**：`wttr.in`是一个免费的日历同步工具，无需API密钥，数据格式为`wttr.in/City?format=j1`。