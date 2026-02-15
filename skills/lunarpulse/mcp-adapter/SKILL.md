---
name: mcp-integration
description: 使用 Model Context Protocol（MCP）服务器来访问外部工具和数据源。使 AI 代理能够从配置好的 MCP 服务器中发现并执行相应的工具（如法律数据库、API、数据库连接器、天气服务等）。
license: MIT
---

# MCP集成使用指南

## 概述

使用MCP集成插件可以发现并执行外部MCP服务器提供的工具。该功能允许您访问法律数据库、查询API、搜索数据库，并与任何提供MCP接口的服务进行集成。

该插件提供了一个统一的`mcp`工具，具有以下两个操作：
- `list` - 从所有连接的服务器中发现可用的工具
- `call` - 带参数执行特定工具

---

# 流程

## 🔍 第1阶段：工具发现

### 1.1 检查可用工具

**首先列出所有可用的工具**，以查看哪些MCP服务器已连接以及它们提供了哪些功能。

**操作：**
```
{
  tool: "mcp",
  args: {
    action: "list"
  }
}
```

**响应结构：**
```json
[
  {
    "id": "server:toolname",
    "server": "server-name",
    "name": "tool-name", 
    "description": "What this tool does",
    "inputSchema": {
      "type": "object",
      "properties": {...},
      "required": [...]
    }
  }
]
```

### 1.2 了解工具规范

对于每个工具，请检查以下内容：
- **id**：格式为`"server:toolname"` - 用冒号分隔服务器名称和工具名称
- **description**：了解工具的功能
- **inputSchema**：定义参数的JSON规范
  - `properties`：包含参数及其类型和描述的字典
  - `required`：必需参数的列表

### 1.3 将工具与用户请求匹配

常见的工具命名模式包括：
- `search_*` - 查找或搜索操作（例如`search_statute`、`search_users`）
- `get_*` - 获取特定数据（例如`get_statute_full_text`、`get_weather`）
- `query` - 执行查询（例如`database:query`）
- `analyze_*` - 分析操作（例如`analyze_law`）
- `resolve_*` - 解决引用问题（例如`resolve_citation`）

---

## 🎯 第2阶段：工具执行

### 2.1 验证参数

在调用工具之前：
1. 从`inputSchema.required`中识别所有必需的参数
2. 确认参数类型与规范匹配（字符串、数字、布尔值、数组、对象）
3. 检查约束条件（最小值、最大值、枚举值、模式）
4. 确保已获取用户提供的必要信息

### 2.2 构建工具调用

**操作：**
```
{
  tool: "mcp",
  args: {
    action: "call",
    server: "<server-name>",
    tool: "<tool-name>",
    args: {
      // Tool-specific parameters from inputSchema
    }
  }
}
```

**示例 - 韩国法律搜索：**
```
{
  tool: "mcp",
  args: {
    action: "call",
    server: "kr-legal",
    tool: "search_statute",
    args: {
      query: "연장근로 수당",
      limit: 5
    }
  }
}
```

### 2.3 解析响应

工具的响应遵循以下结构：
```json
{
  "content": [
    {
      "type": "text",
      "text": "JSON string or text result"
    }
  ],
  "isError": false
}
```

对于JSON响应：
```javascript
const data = JSON.parse(response.content[0].text);
// Access data.result, data.results, or direct properties
```

---

## 🔄 第3阶段：多步骤工作流程

### 3.1 链式调用工具

对于复杂的请求，按顺序执行多个工具：

**示例 - 法律研究工作流程：**
1. **搜索** - 使用`search_statute`查找相关法律
2. **获取** - 使用`get_statute_full_text`获取完整文本
3. **分析** - 使用`analyze_law`进行分析
4. **查找先例** - 使用`search_case_law`查找相关案例

每个步骤都会使用前一步的输出来指导下一步的调用。

### 3.2 维护上下文

在工具调用之间：
- 从每个响应中提取相关信息
- 将提取的数据作为后续调用的参数
- 逐步建立理解
- 向用户展示综合结果

---

## ⚠ 第4阶段：错误处理

### 4.1 常见错误

**“工具未找到：server:toolname”**
- 原因：服务器未连接或工具不存在
- 解决方案：运行`action: "list"`以验证可用工具
- 检查服务器和工具名称的拼写

**“工具参数无效”**
- 原因：缺少必需参数或参数类型错误
- 解决方案：查看列表响应中的`inputSchema`
- 确保提供了所有必需的参数，并且类型正确

**“服务器连接失败”**
- 原因：MCP服务器未运行或无法访问
- 解决方案：告知用户服务暂时不可用
- 如有可能，建议其他替代方案

### 4.2 错误响应格式

错误会返回如下信息：
```json
{
  "content": [{"type": "text", "text": "Error: message"}],
  "isError": true
}
```

**优雅地处理错误：**
- 清晰地解释问题所在
- 不要暴露技术实现细节
- 建议下一步操作或替代方案
- 避免过度重试

---

# 完整示例

## 用户请求：“查找关于加班费的韩国法律”

### 第1步：发现工具
```
{tool: "mcp", args: {action: "list"}}
```

响应显示`kr-legal:search_statute`，其中包含：
- 必需参数：`query`（字符串）
- 可选参数：`limit`（数字）、`category`（字符串）

### 第2步：执行搜索
```
{
  tool: "mcp",
  args: {
    action: "call",
    server: "kr-legal",
    tool: "search_statute",
    args: {
      query: "연장근로 수당",
      category: "노동법",
      limit: 5
    }
  }
}
```

### 第3步：解析并展示结果
```javascript
const data = JSON.parse(response.content[0].text);
// Present data.results to user
```

**面向用户的响应：**
```
Found 5 Korean statutes about overtime pay:

1. 근로기준법 제56조 (연장·야간 및 휴일 근로)
   - Overtime work requires 50% premium
   
2. 근로기준법 제50조 (근로시간)
   - Standard working hours: 40 hours per week

Would you like me to retrieve the full text of any statute?
```

---

# 快速参考

## 列出工具
```
{tool: "mcp", args: {action: "list"}}
```

## 调用工具
```
{
  tool: "mcp",
  args: {
    action: "call",
    server: "server-name",
    tool: "tool-name",
    args: {param1: "value1"}
  }
}
```

## 关键模式

**工具ID解析：** `"server:toolname"` → 用冒号分隔服务器名称和工具名称

**参数验证：** 检查`inputSchema.required`和`inputSchema.properties[param].type`

**响应解析：** 对于JSON响应，使用`JSON.parse(response.content[0].text)`进行解析

**错误检测：** 检查`response.isError === true`

---

# 参考文档

## 核心文档

- **插件README**：[README.md] - 安装和配置指南
- **实际示例**：[REAL_EXAMPLE_KR_LEGAL.md] - kr-legal的完整设置示例
- **API参考**：[API.md] - API技术细节
- **配置**：[CONFIGURATION.md] - 服务器配置指南
- **故障排除**：[TROUBLESHOOTING.md] - 常见问题及解决方法

## 使用示例

- **示例集合**：[EXAMPLES.md] - 包含13个实际示例：
  - 法律研究工作流程
  - 数据库查询
  - 天气服务集成
  - 多步骤复杂工作流程
  - 错误处理模式

---

**注意：** 当不确定有哪些可用工具时，请始终从`action: "list"`开始操作。