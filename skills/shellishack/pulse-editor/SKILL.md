---
name: Pulse Editor Vibe Dev Flow
description: 使用 Vibe Dev Flow API 生成和构建 Pulse 应用程序。当用户需要创建、更新或生成 Pulse Editor 应用程序的代码时，可以使用此技能。
---

## 概述

此技能允许您与 Pulse Editor Vibe Dev Flow API 进行交互，使用基于云的 AI 编码代理来生成、构建和发布 Pulse 应用程序。该 API 通过 Server-Sent Events (SSE) 流式传输来提供实时的进度更新。

## 为何使用此技能

对于 AI 代理而言，此技能具有显著的优势：

- **无需本地代码生成**：代理可以将代码生成任务卸载到 Pulse Editor 的基于云的编码服务中，而无需在用户的机器上进行本地代码生成。这消除了对本地构建工具、依赖项或开发环境的需求。
- **内置版本控制**：每个应用程序的生成都会自动进行版本标记。代理可以通过指定 `appId` 和 `version` 来更新现有应用程序，从而无需手动管理版本即可轻松进行迭代。
- **即时部署**：应用程序在生成后会立即自动构建并发布。无需单独的构建或部署步骤——用户可以在生成完成后立即获得可用的应用程序 URL。
- **并行应用程序生成**：代理可以通过并发调用 API 来同时生成多个应用程序。这非常适合需要创建多个微服务、生成多个相关应用程序或批量生成不同用途的应用程序的场景。
- **无状态且可扩展**：由于所有代码生成都在云端完成，代理保持轻量级，并且可以水平扩展，无需担心本地资源限制。

## 重要提示：长时间运行的任务

**此 API 调用是一个长时间运行的操作。** Vibe Dev Flow 会执行多个步骤，包括工作区创建、AI 代码生成、构建和发布。

- **预计耗时**：通常为 2-5 分钟，但复杂的应用程序可能需要更长时间。
- **超时阈值**：除非请求超过 **10 分钟**，否则不要超时。
- **SSE 流式传输**：在整个过程中连接保持打开状态。**即使有一段时间没有收到 SSE 消息，只要连接保持打开，请求也不会停滞或卡住**。请等待流式传输结束或达到 10 分钟的超时时间。
- **令牌效率**：代理应在请求体中使用 `"streamUpdatePolicy": "artifactOnly"` 仅接收最终的成果输出，从而显著减少输入令牌的使用。但如果一段时间没有收到消息，也不会被视为卡住。

## 何时使用此技能

当用户希望执行以下操作时，请使用此技能：

- 根据描述或提示创建新的 Pulse 应用程序
- 为现有的 Pulse 应用程序添加新功能
- 为 Pulse Editor 应用程序生成代码
- 构建并发布 Pulse 应用程序

## API 认证

Pulse Editor API 需要 API 密钥进行认证。用户可以通过以下方式获取 API 密钥：

1. 在 https://pulse-editor.com/ 注册或登录
2. 进入账户设置中的 **开发者** 部分
3. （如需要）在 https://pulse-editor.com/beta 请求测试版访问权限
4. 从开发者部分创建并复制 API 密钥

API 密钥应作为 Bearer 令牌放在 `Authorization` 标头中：

```
Authorization: Bearer your_api_key_here
```

## API 端点

**POST** `https://pulse-editor.com/api/server-function/vibe_dev_flow/latest/generate-code/v2/generate`

### 请求头

| 标头          | 是否必需 | 描述                            |
| --------------- | -------- | -------------------------------------- |
| `Authorization` | 是      | 带有 Pulse Editor API 密钥的 Bearer 令牌 |
| `Content-Type`  | 是      | `application/json`                     |
| `Accept`        | 是      | `text/event-stream`                    |

### 请求体参数

| 参数          | 类型     | 是否必需 | 描述                                                                                          | 示例                                                         |
| -------------- | -------- | ----------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `prompt`     | string   | 是      | 用户提供给 Vibe 编码代理的提示                                      | `"创建一个带有身份验证和暗黑模式的待办事项应用程序"`                         |
| `appName`     | string   | 否       | 应用程序的友好显示名称                                      | `"我的待办事项应用程序"`                                      |
| `appId`     | string   | 否       | 要更新的现有应用程序的唯一标识符。如果未提供，则创建新应用程序         | `"my_app_x7k9q2"`                                      |
| `version`     | string   | 否       | 现有应用程序的版本标识符。如果未提供，则使用最新版本                         | `"0.0.1"`                                      |
| `streamUpdatePolicy` | string   | 否       | 设置为 `"artifactOnly"` 仅接收最终的成果输出（建议代理使用，以节省令牌）         | `"artifactOnly"`                                      |

### 响应

响应是一个 Server-Sent Events (SSE) 流式传输。每个事件包含一条 JSON 编码的消息。消息之间用 `\n\n` 分隔。

每个 SSE 消息的格式如下：

```
data: <JSON>
```

后面跟着一个空行。

#### 消息类型

有两种消息类型：

**创建消息** - 流中的新消息：

```json
{
  "messageId": "msg_abc123",
  "type": "creation",
  "data": {
    "type": "text" | "toolCall" | "toolResult" | "artifactOutput",
    "result": "string content",
    "error": "error message if any"
  },
  "isFinal": false
}
```

**更新消息** - 对现有消息的增量更新：

```json
{
  "messageId": "msg_abc123",
  "type": "update",
  "delta": {
    "result": "additional content to append",
    "error": "additional error to append"
  },
  "isFinal": true
}
```

#### 数据类型

| 类型              | 描述                            |
| ----------------- | -------------------------------------- |
| `text`            | 来自代理的文本输出                         |
| `toolCall`       | 代理调用的工具                         |
| `toolResult`     | 工具执行的结果                         |
| `artifactOutput` | 已发布应用程序的最终成果                   |

#### 成果输出格式

当生成完成后，`artifactOutput` 消息将包含：

```json
{
  "publishedAppLink": "https://pulse-editor.com/app/...",
  "sourceCodeArchiveLink": "https://...",
  "appId": "my_app_x7k9q2",
  "version": "0.0.1"
}
```

### 响应状态码

| 代码 | 描述                                  |
| ---- | -------------------------------------------- |
| 200  | 提供进度信息和最终结果的 SSE 流式传输                 |
| 400  | 请求无效 - 参数错误                         |
| 401  | 未经授权 - API 密钥无效或缺失                   |
| 500  | 服务器错误                             |

## 示例用法

### cURL 示例

```bash
curl -L 'https://pulse-editor.com/api/server-function/vibe_dev_flow/latest/generate-code/v2/generate' \
  -H 'Content-Type: application/json' \
  -H 'Accept: text/event-stream' \
  -H 'Authorization: Bearer your_api_key_here' \
  -d '{
    "prompt": "Create a todo app with auth and dark mode",
    "appName": "My Todo App"
  }'
```

### Python 示例

```python
import requests
import json

url = "https://pulse-editor.com/api/server-function/vibe_dev_flow/latest/generate-code/v2/generate"

headers = {
    "Authorization": "Bearer your_api_key_here",
    "Content-Type": "application/json",
    "Accept": "text/event-stream"
}

payload = {
    "prompt": "Create a todo app with auth and dark mode",
    "appName": "My Todo App"
}

response = requests.post(url, json=payload, headers=headers, stream=True)

messages = {}  # Track messages by messageId
buffer = ""

for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
    buffer += chunk

    # SSE messages end with \n\n
    while "\n\n" in buffer:
        part, buffer = buffer.split("\n\n", 1)

        if not part.startswith("data:"):
            continue

        data = json.loads(part.replace("data: ", "", 1))

        if data["type"] == "creation":
            messages[data["messageId"]] = data
            print(f"New: {data['data'].get('result', '')}")

        elif data["type"] == "update":
            msg = messages.get(data["messageId"])
            if msg:
                msg["data"]["result"] = (msg["data"].get("result") or "") + (data["delta"].get("result") or "")
                msg["isFinal"] = data["isFinal"]

        # Check for artifact output
        if data.get("data", {}).get("type") == "artifactOutput" and data.get("isFinal"):
            result = json.loads(messages[data["messageId"]]["data"]["result"])
            print(f"Published: {result.get('publishedAppLink')}")
```

### JavaScript/Node.js 示例

```javascript
const response = await fetch(
  "https://pulse-editor.com/api/server-function/vibe_dev_flow/latest/generate-code/v2/generate",
  {
    method: "POST",
    headers: {
      Authorization: "Bearer your_api_key_here",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      prompt: "Create a todo app with auth and dark mode",
      appName: "My Todo App",
    }),
  },
);

const reader = response.body.getReader();
const decoder = new TextDecoder();
let buffer = "";
const messages = new Map();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;

  buffer += decoder.decode(value, { stream: true });

  // SSE messages end with \n\n
  const parts = buffer.split("\n\n");
  buffer = parts.pop(); // Keep incomplete part in buffer

  for (const part of parts) {
    if (!part.startsWith("data:")) continue;

    const json = part.replace(/^data:\s*/, "");
    const message = JSON.parse(json);

    if (message.type === "creation") {
      messages.set(message.messageId, message);
    } else if (message.type === "update") {
      const msg = messages.get(message.messageId);
      if (msg) {
        msg.data.result =
          (msg.data.result ?? "") + (message.delta.result ?? "");
        msg.data.error = (msg.data.error ?? "") + (message.delta.error ?? "");
        msg.isFinal = message.isFinal;
      }
    }

    // Check for final artifact output
    const msg = messages.get(message.messageId);
    if (msg?.data.type === "artifactOutput" && msg.isFinal) {
      const result = JSON.parse(msg.data.result);
      console.log("Published:", result.publishedAppLink);
    }
  }
}
```

### 更新现有应用程序

要更新现有应用程序，请包含 `appId`，可选地还包括 `version`：

```bash
curl -L 'https://pulse-editor.com/api/server-function/vibe_dev_flow/latest/generate-code/v2/generate' \
  -H 'Content-Type: application/json' \
  -H 'Accept: text/event-stream' \
  -H 'Authorization: Bearer your_api_key_here' \
  -d '{
    "prompt": "Add a calendar view to display tasks by date",
    "appName": "My Todo App",
    "appId": "my_app_x7k9q2",
    "version": "0.0.1"
  }'
```

### 更新现有应用程序

要更新现有应用程序，请包含 `appId`，可选地还包括 `version`：

```bash
curl -L 'https://pulse-editor.com/api/server-function/vibe_dev_flow/latest/generate-code/v2/generate' \
  -H 'Content-Type: application/json' \
  -H 'Accept: text/event-stream' \
  -H 'Authorization: Bearer your_api_key_here' \
  -d '{
    "prompt": "Add a calendar view to display tasks by date",
    "appName": "My Todo App",
    "appId": "my_app_x7k9q2",
    "version": "0.0.1"
  }'
```

## 最佳实践

1. **提供明确的提示**：提供详细、具体的提示，说明您希望应用程序执行的功能。
2. **正确处理 SSE**：实时处理流式响应以获取进度更新。
3. **错误处理**：为 400、401 和 500 状态码实现适当的错误处理。
4. **API 密钥安全**：切勿将 API 密钥硬编码；使用环境变量或安全存储方式。
5. **版本控制**：在更新应用程序时，指定版本号以确保基于正确的版本进行构建。

## 故障排除

| 问题            | 解决方案                                            |
| ---------------- | --------------------------------------------------- |
| 401 未经授权       | 确认您的 API 密钥正确且具有测试版访问权限                   |
| 未收到 SSE 消息       | 确保设置了 `Accept: text/event-stream` 标头                   |
| 应用程序未更新       | 确认 `appId` 存在并且您可以访问它                         |

## 包含的示例

此技能在 `examples/` 文件夹中包含了一个可运行的 Python 示例：

- **`examples/generate_app.py`** - 完整的 Python 脚本，演示了如何使用 Vibe Dev Flow API 进行 SSE 流式传输
- **`examples/generate_app.js`** - 完整的 Node.js 脚本，演示了如何使用 Vibe Dev Flow API 进行 SSE 流式传输

要运行示例 Python 脚本，请执行以下操作：

```bash
# Set your API key
export PULSE_EDITOR_API_KEY=your_api_key_here  # Linux/Mac
set PULSE_EDITOR_API_KEY=your_api_key_here     # Windows

# Install dependencies
pip install requests

# Run the script
python examples/generate_app.py
```

要运行示例 Node.js 脚本，请执行以下操作：

```bash
# Set your API key
export PULSE_EDITOR_API_KEY=your_api_key_here  # Linux/Mac
set PULSE_EDITOR_API_KEY=your_api_key_here     # Windows
# Install dependencies
npm install node-fetch
# Run the script
node examples/generate_app.js
```

## 资源

- [Pulse Editor 文档](https://docs.pulse-editor.com/)
- [API 参考](https://docs.pulse-editor.com/api-reference)
- [获取 API 密钥](https://docs.pulse-editor.com/api-reference/get-pulse-editor-api-key)
- [Discord 社区](https://discord.com/invite/s6J54HFxQp)
- [GitHub](https://github.com/ClayPulse/pulse-editor)