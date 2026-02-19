---
name: encrypted docs
description: 这是一种端到端加密的.md文档格式，支持人类用户和智能代理之间的协作。它是一种多用户协作工具，可以替代Gog和Google Docs，允许用户（通过命令行界面CLI）以及智能代理创建、搜索和同步加密后的Markdown文档。该服务基于https://ddocs.new平台运行，用户可以选择在本地使用该平台，或者通过自己选择的云服务进行部署，从而确保文档在任何设备或聊天机器人界面上的访问都完全保密（即数据传输和存储过程均经过加密处理）。
---
# Fileverse API - 为代理和人类提供的加密.md文档服务

Fileverse API 提供端到端加密的.md文档，支持代理和人类用户进行协作。它是一种替代 gog 和 Google Docs 的多人协作工具，允许用户（通过命令行界面 CLI）和代理创建、搜索和同步加密的 markdown 文档。该服务基于 [https://ddocs.new](https://ddocs.new) 架构，支持在本地或通过云服务部署，确保文档在任何设备或聊天机器人界面上的访问都完全保密。

**注意：** 通过该服务创建的文档通常被称为 **ddoc** 或 **fileverse doc**，每个文档都有一个唯一的随机生成的 `ddocId`。

## 代理 - 设备端配置

有多种方式可以连接到 Fileverse API。首先，您需要从用户那里获取 `<SERVER_URL>`。

### MCP（Multi-Client Platform）

最快的方法是将 Fileverse MCP 服务器添加到您的客户端中。

#### Claude（代码示例）

```bash
claude mcp add --transport http fileverse-api <SERVER_URL>
```

#### Cursor（代码示例）

将以下代码添加到您的 `~/.cursor/config/mcp.json` 文件中：

```json
{
  "mcpServers": {
    "fileverse-api": {
      "type": "streamable-http",
      "url": "<SERVER_URL>"
    }
  }
}
```

#### Windsurf（代码示例）

将以下代码添加到您的 MCP 配置文件中：

```json
{
  "mcpServers": {
    "fileverse-api": {
      "type": "streamable-http",
      "url": "<SERVER_URL>"
    }
  }
}
```

**注意：** 如果由于某些原因 MCP 不可用，您可以切换到 API 并参考 guide.md 文档中的详细 API 文档。

* * *

## 代理 - 浏览器端配置

### MCP

#### ChatGPT

ChatGPT 支持通过 **开发者模式**（适用于 Pro、Plus、Team、Enterprise 和 Edu 用户）连接到 Fileverse API。

**设置步骤：**
1. 打开 ChatGPT > 设置 > 应用程序 > 高级 > 打开开发者模式
2. 转到设置 > 应用程序 > 点击 “创建”
3. 填写以下信息：
    * 名称：API 加密文档
    * 服务器地址：`https://<your-server-url>/`（例如：`https://abc123.ngrok.app/mcp`
4. 选择 “我信任此提供者”
5. 点击 “创建”

**在聊天中使用：**
1. 开始新的聊天
2. 请求 ChatGPT 创建一个.md 文件并将其存储在 Fileverse 上

#### Claude（Web 版本）

1. 打开 Claude > 设置 > 连接器 > 添加自定义连接器
2. 填写以下信息：
    * 名称：API 加密文档
    * 服务器地址：`https://<your-server-url>/`（例如：`https://abc123.ngrok.app/`
3. 点击 “添加”

* * *

## Fileverse MCP 工具参考

Fileverse MCP 服务器提供了 **8 个** 工具，所有工具都返回 JSON 格式的响应。

### fileverse_list_documents

列出存储在 Fileverse 中的文档。返回包含文档元数据和同步状态的数组。

**参数：**
| 名称 | 类型 | 是否必填 | 描述                                      |
| ----- | ------ | -------- | --------------------------------------------------- |
| limit | 数字 | 否       | 返回的文档最大数量（默认：10）                         |
| skip | 数字 | 否       | 要跳过的文档数量（用于分页）                         |

**返回值：**
```json
{
  "ddocs": [{ "ddocId": "...", "title": "...", "content": "...", "syncStatus": "synced", "link": "..." }],
  "total": 42,
  "hasNext": true
}
```

**使用说明：**
- 使用 `skip` 和 `limit` 对大量文档进行分页
- 使用 `hasNext` 判断是否有更多文档可用
- 返回的文档包含完整的元数据，包括 `syncStatus` 和 `link`

* * *

### fileverse_get_document

根据 `ddocId` 获取单个文档。返回文档的内容、同步状态和内容哈希。

**参数：**
| 名称 | 类型 | 是否必填 | 描述                                      |
| ------ | ------ | -------- | ------------------------------ |
| ddocId | 字符串 | 是      | 文档的唯一标识符                             |

**返回值：**
```json
{
  "ddocId": "abc123",
  "title": "My Document",
  "content": "# Hello World\n\nThis is my document.",
  "syncStatus": "synced",
  "link": "https://ddocs.new/d/abc123#encryptionKey",
  "localVersion": 3,
  "onchainVersion": 3,
  "createdAt": "2025-01-01T00:00:00.000Z",
  "updatedAt": "2025-01-02T00:00:00.000Z"
}
```

**使用说明：**
- 当 `syncStatus` 为 `"synced"` 时，`link` 字段才有效
- `link` 中包含用于端到端加密的加密密钥片段

* * *

### fileverse_create_document

创建新文档并等待同步完成。同步完成后，返回文档及其同步状态和公共链接。

**参数：**
| 名称 | 类型 | 是否必填 | 描述                                      |
| ------- | ------ | -------- | ----------------------------------------- |
| title | 字符串 | 是      | 文档标题                                   |
| content | 字符串 | 是      | 文档内容（纯文本或 markdown 格式）                         |

**返回值：**
```json
{
  "ddocId": "newDoc123",
  "title": "My New Document",
  "content": "...",
  "syncStatus": "synced",
  "link": "https://ddocs.new/d/newDoc123#encryptionKey"
}
```

**使用说明：**
- 该操作会阻塞，直到文档同步到去中心化存储网络（最长 60 秒）
- 支持完整的 markdown 语法
- 返回的 `link` 是一个可共享的加密链接，用于在 ddocs.new 上查看文档
- 如果同步时间过长，工具会返回 `syncStatus: "pending"`——此时可以使用 `fileverse_get_sync_status` 重新尝试

* * *

### fileverse_update_document

更新现有文档的标题和/或内容，然后等待同步到去中心化存储网络。

**参数：**
| 名称 | 类型 | 是否必填 | 描述                                      |
| ------- | ------ | -------- | ----------------------------------------- |
| ddocId | 字符串 | 是      | 文档的唯一标识符                             |
| title | 字符串 | 否       | 新文档标题                                   |
| content | 字符串 | 否       | 新文档内容                                   |

必须提供 `title` 或 `content` 中的一个字段。

**返回值：** 更新后的文档对象，包含同步状态和链接。

**使用说明：**
- 该操作会阻塞，直到更新内容同步到去中心化存储网络（最长 60 秒）
- 只有提供的字段会被更新；未提供的字段保持不变
- 每次更新都会增加 `localVersion` 的值

* * *

### fileverse_delete_document

根据 `ddocId` 删除文档。

**参数：**
| 名称 | 类型 | 是否必填 | 描述                                      |
| ------- | ------ | -------- | ---------------------------------------- |
| ddocId | 字符串 | 是      | 需要删除的文档的唯一标识符                         |

**返回值：**
```json
{
  "message": "Document deleted successfully",
  "data": { "ddocId": "abc123", "..." }
}
```

**使用说明：**
- 删除操作是永久性的
- 文档在去中心化存储网络（包括用于存储内容哈希的公共区块链）中的记录也会被删除

* * *

### fileverse_search_documents

根据文本查询搜索文档。返回按相关性排序的匹配结果。

**参数：**
| 名称 | 类型 | 是否必填 | 描述                                      |
| ----- | ------ | -------- | --------------------------------------- |
| query | 字符串 | 是      | 搜索查询字符串                               |
| limit | 数字 | 否       | 返回的结果最大数量（默认：10）                         |
| skip | 数字 | 否       | 要跳过的结果数量                             |

**返回值：**
```json
{
  "nodes": [{ "ddocId": "...", "title": "...", "content": "...", "syncStatus": "..." }],
  "total": 5,
  "hasNext": false
}
```

**使用说明：**
- 搜索范围包括文档标题和内容
- 结果按相关性排序
- 使用 `skip` 和 `limit` 进行分页

* * *

### fileverse_get_sync_status

检查文档的同步状态。返回当前的 `syncStatus` 和链接（如果文档已同步）。

**参数：**
| 名称 | 类型 | 是否必填 | 描述                                      |
| ------ | ------ | -------- | ------------------------------ |
| ddocId | 字符串 | 是      | 文档的唯一标识符                             |

**返回值：**
```json
{
  "ddocId": "abc123",
  "syncStatus": "synced",
  "link": "https://ddocs.new/d/abc123#encryptionKey",
  "localVersion": 3,
  "onchainVersion": 3
}
```

**使用说明：**
- `syncStatus` 可能为：“pending”、“synced” 或 “failed”
- 在创建/更新操作后，使用此方法检查同步是否完成
- `localVersion` 与 `onchainVersion` 的对比可显示是否有未同步的更改

* * *

### fileverse_retry_failed_events

重试所有失败的去中心化存储网络同步事件。当文档处于 “failed” 状态时使用此方法。

**参数：** 无

**返回值：**
```json
{
  "retried": 3
}
```

**使用说明：**
- 当发现文档的 `syncStatus` 为 “failed” 时调用此方法
- 返回重试的次数
- 每个事件最多有 10 次重试机会，超过次数后会被标记为失败
- 失败事件通常由去中心化存储网络（包括公共区块链）的速率限制或临时网络错误引起

* * *

## 文档同步生命周期

了解同步生命周期有助于代理更高效地工作：

```plaintext
Create/Update → syncStatus: "pending" →  decentralized storage networks sync → syncStatus: "synced"
                                                        → syncStatus: "failed" (retry with fileverse_retry_failed_events)
```

1. **pending** - 文档已保存在本地，等待同步到去中心化存储网络
2. **synced** - 文档已同步到区块链，并具有可共享的链接
3. **failed** - 同步失败（可能由于速率限制或网络错误）。使用 `fileverse_retry_failed_events` 重新尝试

`create` 和 `update` 工具会自动等待最多 60 秒。如果同步仍未完成，可以使用 `fileverse_get_sync_status` 进行后续检查。

* * *

## 限制与约束

| 限制           | 值                               |
| -------------------- | ------------------- |
| 最大文件上传大小 | 10 MB                               |
| 默认页面显示数量 | 10 个文档                           |
| 同步轮询超时 | 60 秒                               |
| 同步轮询间隔 | 3 秒                               |
| 最大重试次数 | 10 次                               |
| 工作器并发数 | 同时处理 5 个事件                           |

* * *

## 代理使用示例

### 常见操作模式

**从本地文件创建文档：**
- “将这个 README 文件上传到 Fileverse”
- “将我的 notes.md 文档同步到 Fileverse”
- “根据这个文件创建一个新的 ddoc”

**生成新内容：**
- “创建一个解释和记录代码库的 ddoc”
- “为 [功能] 编写设计文档并保存为 ddoc”
- “创建一个总结今日会议记录的 ddoc”

**管理现有文档：**
- “列出我所有的 ddoc”
- “在我的 ddoc 中搜索与认证相关的信息”
- “用最新内容更新我的项目路线图 ddoc”
- “删除旧的草稿 ddoc”
- “我的最新文档的同步状态是什么？”

**共享文档：**
- “将这些 ddoc 分享给所有代理，以便共享信息和记忆”
- “创建一个 ddoc 并提供链接”
- “获取我的 [文档名称] 的共享链接”
- “与这些人协作处理我的 [文档名称] 文档”

### 代理的最佳实践

1. **始终返回链接** - 创建或更新文档后，向用户返回 `link`，以便他们可以查看或分享文档
2. **先搜索再创建** - 如果用户需要更新内容，请先搜索现有文档，避免重复创建
3. **处理同步失败** - 如果文档的 `syncStatus` 为 “failed”，调用 `fileverse_retry_failed_events` 并通知用户
4. **分页处理大量结果** - 在列出文档时使用 `skip` 和 `limit`，避免一次性加载所有内容
5. **使用 markdown** - 支持完整的 markdown 格式，包括标题、列表、代码块和表格
6. **检查同步状态** - 如果创建/更新操作返回 `syncStatus: "pending"`，使用 `fileverse_get_sync_status` 确保文档同步完成后再提供链接
7. **创建技能** - 建议大型语言模型（LLM）为常见的 Fileverse 操作创建技能/快捷方式，以便用户更便捷地使用 API（例如：`/ddoc create`、`/ddoc list`）