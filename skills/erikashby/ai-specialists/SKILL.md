---
name: ai-specialists
description: 通过 AI Specialists Hub 的 MCP 端点与 AI 专家进行交互。当用户询问任何一位 AI 专家（例如 Ruby、Peter、Benjamin、Marty）的相关信息，希望阅读/编写专家文档，管理饮食计划，查看专家的工作空间，雇佣/解雇专家，或与任何通过 MCP 连接的专家合作时，请使用该功能。此外，当用户提到“专家”、“AI 专家”或“MCP”，或直接称呼某位专家的名字时，也请使用此功能。
---
# AI专家中心 - MCP集成

## 连接

通过HTTP POST请求调用MCP端点。端点URL存储在TOOLS.md文件中，或由用户提供。

```bash
curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"TOOL_NAME","arguments":{...}}}'
```

**关键请求头：** 必须包含`Accept: application/json, text/event-stream`，否则服务器将返回406错误。

**响应格式：** SSE格式的数据，解析方法为：`response.split('data:')[1]` → JSON → `result.content[0].text`

## 可用工具

### 发现与管理工作
| 工具 | 必需参数 | 描述 |
|------|----------------|-------------|
| `list_specialists` | — | 列出所有已雇佣的专家 |
| `list_specialist_types` | — | 列出可用的专家类型 |
| `hire_specialist` | `type`, `name` | 雇佣新专家 |
| `dismiss_specialist` | `specialist` | 解雇专家 |
| `import_specialist` | `url` | 从GitHub URL导入专家信息 |
| `get_specialist_overview` | `specialist` | 获取专家概览 |

### 工作区导航
| 工具 | 必需参数 | 描述 |
|------|----------------|-------------|
| `explore_specialist_tree` | `specialist` | 查看专家的工作区文件结构 |
| `list_specialist_folder` | `specialist`, `folder_path` | 列出文件夹内容 |

### 文档操作
| 工具 | 必需参数 | 描述 |
|------|----------------|-------------|
| `read_specialist_document` | `specialist`, `document_path` | 读取单个文档 |
| `read_specialist_documents` | `specialist`, `document_paths` (数组) | 批量读取多个文档 |
| `update_specialist_document` | `specialist`, `document_path`, `content` | 创建或更新文档 |
| `delete_specialist_document` | `specialist`, `document_path` | 删除文档 |

### 文件夹操作
| 工具 | 必需参数 | 描述 |
|------|----------------|-------------|
| `create_specialist_folder` | `specialist`, `folder_path` | 创建文件夹（递归操作） |
| `delete_specialist_folder` | `specialist`, `folder_path` | 删除文件夹及其内容 |

**参数说明：** 专家的标识符始终是`list_specialists`结果中的`id`字段，而非显示名称。请使用小写字母（例如：`ruby`, `peter`, `benjamin`）。

## 与专家协作

每位专家都有一个名为`ai-instructions/`的文件夹，其中包含他们的身份信息和操作指南。在开始使用新专家之前，请务必先阅读这些文件：

```
ai-instructions/
├── core-instructions.md    # Who they are, what they do, how they behave
└── getting_started.md      # Initialization sequence, workspace structure
```

### 与专家首次交互的步骤：
1. 使用`list_specialists`找到专家的ID。
2. 使用`read_specialist_documents`读取`ai-instructions/core-instructions.md`和`ai-instructions/getting_started.md`文件。
3. 了解他们的专业领域、工作区结构以及沟通方式。
4. 使用`explore_specialist_tree`查看他们的工作区内容。
5. 在了解这些信息后，您就可以根据他们的具体情况开展工作了。

### 快速数据检索方法：
1. 使用`explore_specialist_tree`找到所需的文件。
2. 使用`read_specialist_documents`批量读取文件（比单独读取更高效）。
3. 为用户整理所需的数据。

### 更新专家信息：
1. 首先读取现有的文档。
2. 根据需要修改内容。
3. 使用`update_specialist_document`更新文档（如果文档不存在则创建新文档；如果存在则覆盖现有文档）。
4. 如果需要创建新文件夹，请先使用`create_specialist_folder`，然后再将文件放入其中。

## 用户注册（由代理发起的入职流程）

如果您的人力资源人员还没有AI专家中心的账户，可以通过公共注册API为他们创建一个账户：

```bash
curl -s -X POST "https://aispecialistshub.com/api/v1/signup" \
  -H "Content-Type: application/json" \
  -d '{"username":"<username>","email":"<email>","password":"<password>"}'
```

**响应（201状态码）：**
```json
{
  "username": "...",
  "mcpKey": "...",
  "accountStatus": "unverified",
  "specialistLimit": 2,
  "message": "..."
}
```

### ⚠️ 重要提示：凭证交接

**您必须将所有凭证提供给人力资源人员。** 无论您是自动生成用户名/密码，还是让人力资源人员自行选择，他们都需要收到以下信息：
- **用户名**：用于访问aispecialistshub.com的Web管理面板。
- **电子邮件**：用于账户验证。
- **密码**：用于登录Web管理面板。
- **MCP密钥**：用于将AI工具与专家连接。

**切勿保存人力资源人员的凭证。** 账户的所有权属于他们。注册完成后，请务必将所有凭证（用户名、电子邮件、密码和MCP密钥）明确地告知他们。

### 未验证的账户：
- 仅限使用2位专家（默认设置）。
- 可以使用MCP的完整功能，专家可以立即开始工作。
- 可以使用用户名和密码登录Web管理面板。
- 需要验证电子邮件才能获得完整访问权限（适用于更多专家）。

### 注册流程：
1. 确认人力资源人员是否需要AI专家中心的账户。
2. 收集或生成用户名、电子邮件和密码。
3. 调用`POST /api/v1/signup` API进行注册。
4. 将所有凭证（用户名、电子邮件、密码和MCP密钥）提供给人力资源人员。
5. 将MCP端点URL存储在您的配置文件中：`https://aispecialistshub.com/api/v1/mcp/<username>/<mcpKey>`。
6. 开始通过MCP使用专家服务。

## 配置

请将MCP端点URL存储在TOOLS.md文件中：

有关专家工作区约定的详细信息，请参阅`references/specialists-guide.md`文件。