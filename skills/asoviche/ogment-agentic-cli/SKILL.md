# Ogment CLI 技能

通过 Ogment CLI 安全地调用 MCP 工具。该工具允许用户通过 Ogment 的管理层访问其连接的 SaaS 工具（如 Linear、Notion、Gmail、PostHog 等）。

## 使用场景

- 用户需要与其连接的 SaaS 服务进行交互（例如查看问题、文档、邮件或分析数据）。
- 需要调用需要身份验证/凭据的 MCP 工具。
- 需要了解用户可使用的集成功能。

## 核心工作流程

```
status → catalog → catalog <server> → catalog <server> <tool> → invoke
```

### 1. 检查连接状态（如有疑问）

```bash
ogment status
```

该命令会返回身份验证状态、连接状态以及可用的服务器列表。可以通过 `summary.status` 快速了解系统运行状况。

### 2. 查找服务器

```bash
ogment catalog
```

该命令会返回包含 `serverId` 和 `toolCount` 的服务器列表。后续调用时需要使用 `serverId`。

### 3. 列出服务器上的工具

```bash
ogment catalog <serverId>
```

该命令会返回服务器上的所有工具及其名称和描述。可以根据描述来选择所需的工具。

### 4. 查看工具的详细信息

```bash
ogment catalog <serverId> <toolName>
```

该命令会返回工具的输入结构（`inputSchema`），包括属性、类型、必填字段和描述。

### 5. 调用工具

```bash
ogment invoke <serverId>/<toolName> --input '<json>'
```

输入方式如下：
- 直接输入 JSON：`--input '{"query": "test"}`
- 从文件读取输入：`--input @path/to/input.json`
- 从标准输入读取：`echo '{}' | ogment invoke ... --input -`

## 输出格式

所有命令的输出都是结构化的 JSON 数据，包含以下字段：
- `ok`：表示操作是否成功（布尔值）
- `data`：操作结果
- `error`：错误信息
- `meta`：相关元数据
- `next_actions`：建议的后续操作

### 常用示例

- **按名称查找工具**：
```bash
ogment catalog <serverId> | jq '.data.tools[] | select(.name + .description | test("email"; "i"))
```

- **列出分配给用户的 issue**：
```bash
ogment invoke openclaw/Linear_list_issues --input '{"assignee": "me"}'
```

- **在 Notion 中搜索内容**：
```bash
ogment invoke openclaw/Notion_notion-search --input '{"query": "quarterly review", "query_type": "internal"}'
```

- **获取 Gmail 邮件**：
```bash
ogment invoke openclaw/gmail_listMessages --input '{"q": "is:unread", "maxResults": 10}'
```

## 注意事项与解决方法

- **服务器错误**：检查工具的输入结构，确保所有必填字段和类型都正确。
- **示例输入可能无效**：忽略示例输入，自行构造有效的输入数据。
- **服务器/工具 ID 大小写敏感**：请使用目录中显示的准确大小写。
- **空字符串可能导致错误**：在调用前验证输入内容。
- `--quiet` 选项会抑制所有输出信息，请谨慎使用。
- **无工具搜索/过滤功能**：可以使用 `jq` 进行本地过滤。

## 错误处理

- **工具未找到**：重新执行 `ogment catalog` 命令以重新查找工具。
- **输入格式错误**：检查 JSON 语法是否正确。
- **传输请求失败**：检查输入结构、必填字段和类型是否正确。
- **身份验证失败**：尝试重新登录。
- **HTTP 502 错误**：稍后重试操作。

## 使用前的检查事项

在调用工具之前，请确保：
1. 服务器存在（通过 `catalog` 命令确认）。
2. 工具存在（通过 `catalog <server>` 命令确认）。
3. 确认输入数据中的所有字段都符合工具的格式要求。
4. 确保所有字段类型匹配正确（例如数字与字符串）。
5. 使用目录中显示的准确大小写来指定服务器/工具 ID。