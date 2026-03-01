---
name: universal-command
description: "只需定义一次命令，即可自动部署到 CLI（命令行界面）、API（应用程序编程接口）和 MCP（管理控制平台）中。在为 Supernal 构建新的命令/工具时，请使用此方法——这样可以确保所有接口的一致性。**切勿重新设计这种模式**，请直接使用该软件包。"
---
# @supernal/universal-command

**一次定义，处处可用。** 为 CLI、API 和 MCP 接口提供统一的数据源。

## ⚠️ 重要提示：请使用此方案，切勿重新开发**

如果您正在为 Supernal 开发命令，请**使用此包**，切勿单独为 CLI、API 或 MCP 创建实现。

## 安装

```bash
npm install @supernal/universal-command
```

## 快速入门

### 定义命令

```typescript
import { UniversalCommand } from '@supernal/universal-command';

export const userCreate = new UniversalCommand({
  name: 'user create',
  description: 'Create a new user',
  
  input: {
    parameters: [
      { name: 'name', type: 'string', required: true },
      { name: 'email', type: 'string', required: true },
      { name: 'role', type: 'string', default: 'user', enum: ['user', 'admin'] },
    ],
  },
  
  output: { type: 'json' },
  
  handler: async (args, context) => {
    return await createUser(args);
  },
});
```

### 在所有地方部署

```typescript
// CLI
program.addCommand(userCreate.toCLI());
// → mycli user create --name "Alice" --email "alice@example.com"

// Next.js API
export const POST = userCreate.toNextAPI();
// → POST /api/users/create

// MCP Tool
const mcpTool = userCreate.toMCP();
// → user_create tool for AI agents
```

## 核心概念

### 单一处理程序

只需编写一次逻辑代码。处理程序会接收经过验证的参数并返回结果：

```typescript
handler: async (args, context) => {
  // This same code runs for CLI, API, and MCP
  return await doThing(args);
}
```

### 输入规范

只需定义一次参数即可——验证规则、CLI 选项、API 参数以及 MCP 规范会自动生成：

```typescript
input: {
  parameters: [
    { name: 'id', type: 'string', required: true },
    { name: 'status', type: 'string', enum: ['draft', 'active', 'done'] },
    { name: 'limit', type: 'number', min: 1, max: 100, default: 10 },
  ],
}
```

### 接口特定选项

根据需要为不同接口覆盖行为：

```typescript
cli: {
  format: (data) => formatForTerminal(data),
  streaming: true,
},

api: {
  method: 'GET',
  cacheControl: { maxAge: 300 },
  auth: { required: true, roles: ['admin'] },
},

mcp: {
  resourceLinks: ['export://results'],
},
```

## 注册表模式

对于多个命令：

```typescript
import { CommandRegistry } from '@supernal/universal-command';

const registry = new CommandRegistry();
registry.register(userCreate);
registry.register(userList);
registry.register(userDelete);

// Generate all CLI commands
for (const cmd of registry.getAll()) {
  program.addCommand(cmd.toCLI());
}

// Generate all API routes
await generateNextRoutes(registry, { outputDir: 'app/api' });

// Generate MCP server
const server = createMCPServer(registry);
```

## 运行时服务器

对于无需代码生成的简单场景：

```typescript
import { createRuntimeServer } from '@supernal/universal-command';

const server = createRuntimeServer();
server.register(userCreate);
server.register(userList);

// Serve as Next.js
export const GET = server.getNextHandlers().GET;
export const POST = server.getNextHandlers().POST;

// Or as Express
app.use('/api', server.getExpressRouter());

// Or as MCP
await server.startMCP({ name: 'my-server', transport: 'stdio' });
```

## 执行上下文

了解调用命令的接口：

```typescript
handler: async (args, context) => {
  if (context.interface === 'cli') {
    // CLI-specific logic
  } else if (context.interface === 'api') {
    const userId = context.request.headers.get('x-user-id');
  }
  return result;
}
```

## 测试

只需测试一次，即可在所有地方正常使用：

```typescript
import { userCreate } from './user-create';

test('creates user', async () => {
  const result = await userCreate.execute(
    { name: 'Alice', email: 'alice@example.com' },
    { interface: 'test' }
  );
  expect(result.name).toBe('Alice');
});
```

## 架构

```
┌─────────────────────────────────────────┐
│      UniversalCommand Definition        │
│  name, description, input, handler      │
└────────────────┬────────────────────────┘
                 │
        ┌────────┼────────┐
        ▼        ▼        ▼
     ┌─────┐  ┌─────┐  ┌─────┐
     │ CLI │  │ API │  │ MCP │
     └─────┘  └─────┘  └─────┘
```

## 适用场景

✅ 开发新的 Supernal 命令/工具  
✅ 为现有逻辑添加 CLI 接口  
✅ 向 AI 代理（MCP）暴露功能  
✅ 使用一致的模式创建 REST API  

❌ 简单的一次性脚本（不推荐使用）  
❌ 需要使用第三方集成方案的场景  

## 与 `sc` 和 `si` 的集成

`sc`（supernal-coding）和 `si`（supernal-interface）在内部都使用了 `universal-command`。在为这些工具添加新命令时，只需将其定义为 `UniversalCommands` 即可。

## API 参考

```typescript
class UniversalCommand<TInput, TOutput> {
  execute(args: TInput, context: ExecutionContext): Promise<TOutput>;
  toCLI(): Command;           // Commander.js Command
  toNextAPI(): NextAPIRoute;  // Next.js route handler
  toExpressAPI(): ExpressRoute;
  toMCP(): MCPToolDefinition;
  validateArgs(args: unknown): ValidationResult<TInput>;
}

class CommandRegistry {
  register(command: UniversalCommand): void;
  getAll(): UniversalCommand[];
}

function createRuntimeServer(): RuntimeServer;
function generateNextRoutes(registry: CommandRegistry, options: CodegenOptions): Promise<void>;
function createMCPServer(registry: CommandRegistry, options: MCPOptions): MCPServer;
```

## 来源

- 包名：`@supernal/universal-command`  
- npm：https://www.npmjs.com/package/@supernal/universal-command

---

*请勿重新开发此方案，直接使用它！*