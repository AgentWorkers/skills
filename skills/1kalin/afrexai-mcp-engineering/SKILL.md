# MCP工程——完整的模型上下文协议系统

构建、集成、保护并扩展MCP服务器和客户端。从第一个服务器到生产环境的多工具架构。

## 使用场景

- 构建MCP服务器（支持任何编程语言）
- 将MCP工具集成到AI代理中
- 调试MCP连接/认证问题
- 设计多服务器架构
- 保护MCP端点以确保生产环境的安全
- 评估使用哪些MCP服务器

---

## 第1阶段：MCP基础

### 什么是MCP
模型上下文协议（Model Context Protocol）是AI代理调用外部工具的标准化方式。可以将其视为“AI的USB”——一个协议，支持任何工具。

### 架构
```
Agent (Client) ←→ MCP Transport ←→ MCP Server ←→ External Service
                   (stdio/HTTP)      (your code)    (API, DB, file system)
```

### 核心概念
| 概念 | 功能 | 示例 |
|---------|-------------|---------|
| **服务器** | 提供工具、资源和提示 | 一个封装了GitHub API的服务器 |
| **客户端** | 发现并调用服务器的功能 | OpenClaw、Claude Desktop、Cursor |
| **工具** | 具有类型化参数的可调用函数 | `create_issue(title, body, labels)` |
| **资源** | 代理可以访问的只读数据 | `file://workspace/config.json` |
| **提示** | 可重用的提示模板 | `summarize_pr(pr_url)` |
| **传输方式** | 客户端与服务器之间的通信方式 | stdio（本地）或HTTP+SSE（远程） |

### 传输方式选择
| 因素 | stdio | HTTP/SSE | Streamable HTTP |
|--------|-------|----------|-----------------|
| 设置复杂性 | 低 | 中等 | 中等 |
| 多客户端支持 | 不支持 | 支持 | 支持 |
| 远程访问 | 不支持 | 支持 | 支持 |
| 流式传输 | 通过stdio | SSE | 支持 |
| 是否需要认证 | 本地无需 | 需要 | 需要 |
| 适用场景 | 本地开发、单个代理 | 生产环境、共享使用 | 现代生产环境 |

**规则：** 开发阶段使用stdio。生产环境或多个代理时切换到HTTP。

---

## 第2阶段：构建你的第一个MCP服务器

### 服务器的基本YAML配置
```yaml
server_name: "[service]-mcp"
description: "[What this server does in one sentence]"
transport: stdio | http
tools:
  - name: "[verb_noun]"
    description: "[What it does — be specific for LLM tool selection]"
    params:
      - name: "[param]"
        type: "string | number | boolean | object | array"
        required: true | false
        description: "[What this param controls]"
    returns: "[What the tool returns]"
    error_cases:
      - "[When/how it fails]"
resources:
  - uri: "[protocol://path]"
    description: "[What data this exposes]"
external_dependencies:
  - "[API/service this wraps]"
auth_required: true | false
auth_method: "api_key | oauth2 | none"
```

### TypeScript服务器模板（使用stdio）
```typescript
// server.ts — minimal MCP server
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "my-service",
  version: "1.0.0",
});

// Define a tool
server.tool(
  "get_item",                          // tool name (verb_noun)
  "Fetch an item by ID",               // description (LLM reads this)
  { id: z.string().describe("Item ID") }, // params with descriptions
  async ({ id }) => {
    try {
      const result = await fetchItem(id);
      return {
        content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      };
    } catch (error) {
      return {
        content: [{ type: "text", text: `Error: ${error.message}` }],
        isError: true,
      };
    }
  }
);

// Define a resource
server.resource(
  "config",
  "config://app",
  async (uri) => ({
    contents: [{ uri: uri.href, mimeType: "application/json", text: JSON.stringify(config) }],
  })
);

// Start
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Python服务器模板（使用stdio）
```python
# server.py — minimal MCP server
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import json

server = Server("my-service")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_item",
            description="Fetch an item by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "Item ID"}
                },
                "required": ["id"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_item":
        result = await fetch_item(arguments["id"])
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### 工具设计规则
1. **使用动词-名词的命名规则**：例如`create_issue`、`search_docs`、`update_config`，避免使用`issue`或`doStuff`。
2. **描述非常重要**：LLM（大型语言模型）会根据描述来选择工具，请确保描述准确无误，并说明在什么情况下不应使用该工具。
3. **细化工具功能**：使用`search_issues`、`get_issue`、`create_issue`等具体函数，而不是使用`manage_issues`这样的通用函数。
4. **返回结构化数据**：使用JSON格式，让LLM能够自行格式化数据。
5. **为LLM提供错误信息**：明确说明出错的原因以及下一步该怎么做。
6. **尽可能实现幂等操作**：使用`create_or_update`而不是`create`，以防止重复请求导致数据重复。
7. **限制输出大小**：分页或截断输出内容，避免响应过大导致问题。
8. **在描述中提供示例**：例如“搜索问题：search_issues(query='bug label:critical')”。

### 工具描述质量检查清单
- [ ] 清晰说明工具的功能（而不仅仅是名称）
- [ ] 明确指出使用场景和禁止使用的场景
- [ ] 每个参数都有详细的格式说明
- [ ] 返回的数据格式有文档记录
- [ ] 提到边缘情况（如无结果、找不到数据等）

---

## 第3阶段：HTTP传输与生产环境服务器

### HTTP服务器模板（TypeScript）
```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import express from "express";

const app = express();
app.use(express.json());

const server = new McpServer({ name: "my-service", version: "1.0.0" });
// ... register tools ...

app.post("/mcp", async (req, res) => {
  const transport = new StreamableHTTPServerTransport("/mcp", res);
  await server.connect(transport);
  await transport.handleRequest(req, res);
});

app.listen(3001, () => console.log("MCP server on :3001"));
```

### 认证方式

#### API密钥（最简单的方式）
```typescript
// Middleware
function authMiddleware(req, res, next) {
  const key = req.headers["x-api-key"] || req.headers.authorization?.replace("Bearer ", "");
  if (!key || !validKeys.has(key)) {
    return res.status(401).json({ error: "Invalid API key" });
  }
  req.userId = keyToUser.get(key);
  next();
}
```

#### OAuth 2.0（用于用户级访问）
```yaml
# MCP OAuth flow
1. Client requests tool → server returns 401 with auth URL
2. User completes OAuth in browser → gets access token
3. Client stores token, includes in subsequent requests
4. Server validates token, calls external API on user's behalf
```

### 生产环境检查清单
- [ ] 对每个客户端/密钥实施速率限制
- [ ] 请求验证（执行前检查请求格式）
- [ ] 详细记录日志（包含请求ID、工具名称、延迟时间、状态）
- [ ] 健康检查端点（/health）
- [ ] 优雅地关闭正在进行的请求
- [ ] 外部调用超时处理（防止工具挂起）
- [ ] 限制输出大小（截断过长的响应）
- [ ] 错误分类（4xx表示客户端问题，5xx表示服务器问题）
- [ ] 如果浏览器客户端连接，则启用CORS
- [ ] 生产环境使用TLS（始终使用HTTPS）

---

## 第4阶段：客户端集成

### OpenClaw配置
```yaml
# In openclaw config — stdio server
mcpServers:
  my-service:
    command: "node"
    args: ["path/to/server.js"]
    env:
      API_KEY: "{{env.MY_SERVICE_API_KEY}}"
```

### Claude Desktop配置
```yaml
# HTTP server
mcpServers:
  my-service:
    url: "https://mcp.myservice.com/mcp"
    headers:
      Authorization: "Bearer {{env.MY_SERVICE_TOKEN}}"
```

### 客户端选择工具时的注意事项
当连接多个MCP服务器时，代理会看到所有工具。帮助代理正确选择工具：
1. **使用唯一的工具名称**：必要时添加前缀（例如`github_search`和`jira_search`）。
2. **提供清晰的描述**：避免不同服务器上的类似工具混淆。
3. **避免工具数量过多**：每个服务器上的工具数量建议控制在20-30个以内，否则代理可能会感到困惑。

### 多服务器架构
```
Agent
├── github-mcp (code: create_pr, search_code, list_issues)
├── slack-mcp (comms: send_message, search_messages)
├── postgres-mcp (data: query, list_tables)
└── internal-mcp (business: get_customer, update_pipeline)
```

**原则：** 每个域名对应一个服务器。不要构建一个庞大的中央服务器。

---

## 第5阶段：测试MCP服务器

### 测试层次结构
```
        /  E2E  \        Agent actually uses the tool
       / Integration \    Tool calls real API (sandbox)
      /    Unit       \   Business logic without MCP layer
```

### 单元测试
```typescript
// Test the tool handler directly, no MCP transport
describe("get_item", () => {
  it("returns item when found", async () => {
    mockDb.findById.mockResolvedValue({ id: "123", name: "Test" });
    const result = await getItemHandler({ id: "123" });
    expect(result.content[0].text).toContain("Test");
  });

  it("returns error for missing item", async () => {
    mockDb.findById.mockResolvedValue(null);
    const result = await getItemHandler({ id: "missing" });
    expect(result.isError).toBe(true);
  });

  it("handles API timeout gracefully", async () => {
    mockDb.findById.mockRejectedValue(new Error("timeout"));
    const result = await getItemHandler({ id: "123" });
    expect(result.isError).toBe(true);
    expect(result.content[0].text).toContain("try again");
  });
});
```

### 使用MCP Inspector进行集成测试
```bash
# Use the MCP Inspector to manually test
npx @modelcontextprotocol/inspector node server.js

# Or use mcporter for CLI testing
mcporter call my-service.get_item id=123
mcporter list my-service --schema  # verify tool schemas
```

### 每个工具的测试检查清单
- [ ] 正常路径下返回预期的格式
- [ ] 缺少必要参数时返回明确的错误信息
- [ ] 参数类型错误时返回明确的错误信息
- [ ] 处理找不到数据的情况（不要抛出异常，而是返回错误信息）
- [ ] 处理速率限制/配额超出的情况
- [ ] 处理认证失败的情况（如令牌过期、密钥无效）
- [ ] 适当截断过长的响应
- [ ] 处理外部API调用超时的情况
- [ ] 处理并发调用带来的干扰

---

## 第6阶段：常见的MCP服务器模式

### 1. API封装器（最常用的方式）
将现有的REST/GraphQL API封装为MCP工具。
**关键决策：**
- 通常将一个API端点映射为一个MCP工具。
- 简化参数（代理不需要所有的API选项）。
- 聚合相关的请求（例如，获取用户信息和用户的仓库信息可以合并为一个工具）。
- 在安全的情况下使用缓存（减少API调用次数）。

### 2. 数据库查询
```
Database → MCP Server → Agent
```
**安全规则：**
- 默认情况下只允许读取操作。写入操作需要明确授权。
- 仅使用参数化查询。严禁将代理输入直接插入SQL语句。
- 所有查询都设置行数限制（代理可以根据需要请求更多数据）。
- 提供数据库模式作为资源，让代理能够了解表和列的结构。

### 3. 文件系统
```
File System → MCP Server → Agent
```
**安全规则：**
- 将文件系统限制在特定目录内。禁止访问上级目录（`../`）。
- 默认情况下只允许读取操作。写入操作需要额外的权限。
- 限制读取文件的大小。避免通过MCP传输大于1GB的文件。

### 4. 多步骤工作流程
某些工具需要协调多个步骤：
```typescript
server.tool("deploy_service", "Build, test, and deploy a service", {
  service: z.string(),
  environment: z.enum(["staging", "production"]),
}, async ({ service, environment }) => {
  // Step 1: Build
  const buildResult = await build(service);
  if (!buildResult.success) return error(`Build failed: ${buildResult.error}`);

  // Step 2: Test
  const testResult = await runTests(service);
  if (!testResult.success) return error(`Tests failed: ${testResult.summary}`);

  // Step 3: Deploy (only if build + tests pass)
  if (environment === "production") {
    // Extra safety: require confirmation resource
    return {
      content: [{
        type: "text",
        text: `Ready to deploy ${service} to production. Tests: ${testResult.passed}/${testResult.total} passed. Call confirm_deploy to proceed.`
      }]
    };
  }
  const deployResult = await deploy(service, environment);
  return success(`Deployed ${service} to ${environment}: ${deployResult.url}`);
});
```

### 5. 聚合器服务器
将多个数据源整合为一个统一的工具：
```
GitHub + Jira + PagerDuty → DevOps MCP Server → Agent
```
例如，一个`get_service_status`工具可以查询三个数据源并返回统一的视图。

---

## 第7阶段：安全与加固

### 威胁模型
| 威胁 | 风险 | 对策 |
|--------|------|------------|
| 通过工具输出注入恶意代码 | 代理在API响应中执行恶意指令 | 对输出进行清理，移除HTML和脚本 |
| 权限过高 | 工具拥有不应拥有的写入权限 | 为每个工具设置最小权限 |
| 数据泄露 | 代理将敏感数据发送到错误的工具 | 使用工具访问列表和审计日志 |
| 服务拒绝攻击 | 代理无限循环调用工具 | 实施速率限制和断路器机制 |
| 凭据泄露 | API密钥出现在工具响应中 | 从输出中移除敏感字段 |
| SSRF（跨站请求伪造） | 代理提供的URL指向内部网络 | 使用URL访问列表，禁止访问私有IP地址 |

### 安全检查清单
- [ ] 每个工具都只具有最低必要的权限。
- [ ] 写入操作需要明确授权或通过功能开关控制。
- [ ] API密钥/敏感信息绝不能出现在工具响应中。
- [ ] 输出内容经过清理（去除HTML和可执行代码）。
- [ ] 对每个工具和每个客户端实施速率限制。
- [ ] 记录日志：记录谁在何时使用了哪个工具以及使用了哪些参数。
- [ ] 在任何外部调用前验证输入。
- [ ] 验证URL参数，防止SSRF攻击。
- [ ] 对每个外部调用设置超时限制（默认为30秒）。
- [ ] 实施断路器机制：如果某个工具的错误率超过50%，则暂时禁用该工具。

### 应避免的危险工具模式
```
❌ server.tool("execute_sql", ..., async ({ query }) => db.raw(query))
❌ server.tool("run_command", ..., async ({ cmd }) => exec(cmd))
❌ server.tool("fetch_url", ..., async ({ url }) => fetch(url))  // SSRF
❌ server.tool("write_file", ..., async ({ path, content }) => fs.writeFile(path, content))
```

### 安全的替代方案
```
✅ Parameterized queries with allowlisted tables
✅ Predefined commands with argument validation
✅ URL allowlist + no private IP ranges
✅ Write to specific directory + filename validation
```

---

## 第8阶段：调试与故障排除

### 常见问题及解决方法

| 症状 | 可能的原因 | 解决方法 |
|---------|-------------|-----|
| 工具在代理中未显示 | 数据库模式错误或服务器未连接 | 检查`mcporter list`或客户端日志 |
| “连接被拒绝” | 服务器未运行或端口设置错误 | 确认服务器进程是否启动，检查端口是否正确 |
| 工具超时 | 外部API响应缓慢或挂起 | 设置超时机制，检查API的健康状态 |
| “参数无效” | 客户端和服务器之间的数据格式不匹配 | 使用`--schema`参数验证数据格式 |
| 代理选择了错误的工具 | 描述不够明确 | 重新编写工具描述，并添加使用提示 |
| 代理无限循环调用工具 | 工具返回了难以理解的错误信息 | 返回更清晰的错误信息，并提示“不要重试” |
| 响应过大导致崩溃 | 未对输出进行截断 | 添加分页或字符长度限制 |
| 认证错误频繁发生 | 令牌过期 | 实现令牌刷新机制 |

### 调试流程
1. **确认服务器是否启动**：运行`node server.js`，检查是否无错误。
2. **列出所有工具**：使用`mcporter list my-server --schema`，确认所有工具是否都已注册。
3. **直接调用工具**：使用`mcporter call my-server.tool_name param=value`，检查是否返回预期的输出。
4. **检查客户端配置**：确认服务器路径/URL是否正确，环境变量是否设置正确。
5. **查看客户端日志**：大多数客户端会记录MCP连接相关的错误。
6. **使用Inspector进行调试**：使用`npx @modelcontextprotocol/inspector`进行交互式调试。

### 日志记录格式
```typescript
server.tool("my_tool", description, schema, async (params) => {
  const requestId = crypto.randomUUID().slice(0, 8);
  console.error(`[${requestId}] my_tool called:`, JSON.stringify(params));
  const start = Date.now();
  try {
    const result = await doWork(params);
    console.error(`[${requestId}] my_tool success: ${Date.now() - start}ms`);
    return success(result);
  } catch (error) {
    console.error(`[${requestId}] my_tool error: ${error.message} (${Date.now() - start}ms)`);
    return errorResponse(error.message);
  }
});
```

注意：在使用stdio传输方式时，使用`console.error`记录日志（stdout用于MCP协议通信）。

---

## 第9阶段：MCP服务器选择指南

### 评估现有的MCP服务器

根据以下维度评分（0-5分）：
| 维度 | 需要检查的内容 |
|-----------|--------------|
| **维护情况** | 最后一次提交时间是否在3个月内？问题是否得到解决？版本是否高于1.0？ |
| **安全性** | 是否没有使用原始SQL或执行命令？是否实现了认证？是否对输入进行了验证？ |
| **代码质量** | 所有工具的JSON模式是否完整？描述是否清晰有用？ |
| **测试情况** | 是否有测试用例？持续集成（CI）是否通过？ |
| **文档齐全性** | 是否有安装指南？工具是否有详细的描述？是否有示例？ |
| **轻量级程度** | 依赖项是否最少？启动速度是否快速？ |

**得分低于15分**：建议自行构建。**得分15-24分**：使用时需谨慎。**得分25分及以上**：可以使用。

### 常见的MCP服务器类别
| 类别 | 使用场景 | 示例 |
|----------|----------|---------|
| 代码相关 | GitHub、GitLab、代码搜索 | github-mcp、gitlab-mcp |
| 数据相关 | PostgreSQL、SQLite、Snowflake | postgres-mcp、sqlite-mcp |
| 沟通工具 | Slack、Discord、电子邮件 | slack-mcp、gmail-mcp |
| 文档管理 | Notion、Confluence、Google Docs | notion-mcp、gdocs-mcp |
| DevOps工具 | AWS、GCP、Kubernetes、Terraform | aws-mcp、k8s-mcp |
| 搜索工具 | Brave、Google、向量存储 | brave-search、rag-mcp |
| 文件管理 | 本地文件系统、S3、Google Drive | filesystem-mcp、s3-mcp |
| 客户关系管理（CRM） | HubSpot、Salesforce | hubspot-mcp、sfdc-mcp |

---

## 第10阶段：架构模式

### 单个代理+多个服务器
**适用场景：** 大多数使用场景。简单且高效。

### 网关模式
**适用场景：** 企业级应用、多租户环境、合规性要求。

### 每个域名对应一个代理
**适用场景：** 复杂的工作流程或专用代理。

### 工具数量建议
| 工具总数 | 建议 |
|-------------|---------------|
| 1-10个 | 适合。代理可以良好处理。 |
| 10-20个 | 可以。确保每个工具的描述清晰。 |
| 20-30个 | 注意：需要按服务器分组并审查工具描述。 |
| 30-50个 | 存在风险：考虑使用每个域名对应一个代理的模式。 |
| 超过50个 | 危险：代理可能会选择错误的工具。建议分割服务器或使用网关。 |

---

## 第11阶段：发布MCP服务器

### 包结构
```
my-mcp-server/
├── src/
│   ├── server.ts        # MCP server entry
│   ├── tools/           # Tool handlers
│   │   ├── search.ts
│   │   └── create.ts
│   ├── auth.ts          # Auth middleware
│   └── config.ts        # Configuration
├── tests/
│   ├── tools.test.ts
│   └── integration.test.ts
├── package.json
├── tsconfig.json
├── README.md            # Setup + tool docs
└── LICENSE
```

### MCP服务器的README模板
```markdown
# [Service] MCP Server

[One sentence: what this enables]

## Quick Start
[3 steps max to get running]

## Tools
| Tool | Description | Params |
|------|-------------|--------|
[Table of all tools]

## Configuration
[Env vars, auth setup]

## Examples
[2-3 real usage examples with agent conversation]
```

### 使用npm发布MCP服务器
```bash
# package.json
{
  "name": "@myorg/service-mcp",
  "version": "1.0.0",
  "bin": { "service-mcp": "./dist/server.js" },
  "files": ["dist"],
  "keywords": ["mcp", "model-context-protocol", "ai-tools"]
}

npm publish
```

---

## 质量评估（0-100分）

| 维度 | 权重 | 评分标准 |
|-----------|--------|--------------|
| 工具设计 | 20% | 名称、描述、功能细化、参数设置 |
| 安全性 | 20% | 认证机制、输入验证、输出清理、最小权限设置 |
| 可靠性 | 15% | 错误处理、超时处理、断路器机制 |
| 测试 | 15% | 单元测试和集成测试的覆盖范围、边缘情况处理 |
| 文档齐全性 | 10% | 安装指南、工具文档、示例是否完整 |
| 性能 | 10% | 响应时间、输出大小、缓存效果 |
| 可维护性 | 10% | 代码结构、类型设计、日志记录 |

**得分0-40分**：不适合生产环境。**得分40-70分**：使用时有注意事项。**得分70-90分**：性能良好。**得分90分及以上**：非常优秀。

---

## 常见错误及解决方法

| 常见错误 | 解决方法 |
|---------|-----|
| 所有工具都集中在一个工具中 | 将功能拆分为多个专门的工具 |
| 工具描述模糊不清 | 编写描述时像是在向新员工解释功能一样详细 |
| 未处理错误 | 所有外部调用都使用try/catch语句 |
| 返回原始的API响应 | 将输出格式调整为适合代理使用的格式 |
| 未设置速率限制 | 为每个工具和每个客户端设置速率限制 |
| 未限制输出大小 | 对输出进行分页或截断 |
| 硬编码的认证信息 | 使用环境变量或秘密管理工具来存储认证信息 |
| 未记录日志 | 无法调试问题是因为看不到日志 |
| 仅测试正常情况 | 需要测试错误情况、超时情况和边缘情况 |
| 在未确认的情况下就开始开发 | 先查找现有的MCP服务器解决方案 |

---

## 常用命令
- “为[服务]构建一个MCP服务器” → 使用第2阶段的模板
- “向我的MCP服务器添加一个工具” → 遵循工具设计规则
- “保护我的MCP服务器” → 按照第7阶段的检查清单操作
- “调试MCP连接问题” → 使用第8阶段的调试流程
- “评估这个MCP服务器” → 使用第9阶段的评估标准
- “设计多服务器架构” → 参考第10阶段的架构模式
- “发布我的MCP服务器” | 遵循第11阶段的发布流程
- “将REST API转换为MCP格式” | 使用第6阶段的封装方法
- “为我的MCP服务器添加认证机制” | 遵循第3阶段的认证规则
- “测试我的MCP服务器” | 使用第5阶段的检查清单
- “工具数量太多怎么办？” | 参考第10阶段的工具数量建议
- “审查我的工具描述” | 使用第2阶段的描述质量检查清单