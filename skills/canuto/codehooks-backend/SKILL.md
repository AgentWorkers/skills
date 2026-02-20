---
name: codehooks-backend
description: 部署无服务器后端，用于处理 REST API 请求、Webhook 联动、数据存储、定时任务、队列作业以及自动化工作流程。
metadata: { "openclaw": { "emoji": "🪝", "requires": { "bins": ["coho"], "env": ["CODEHOOKS_ADMIN_TOKEN"] } } }
---
# Codehooks 后端技能

为您的 OpenClaw 代理提供一个无服务器的后端支持，用于处理 REST API、Webhook、数据存储、定时任务、队列处理以及自动化工作流程。

## 代理可以部署代码

通过此技能，您的代理可以编写 JavaScript/TypeScript 代码，并在 5 秒内将其部署到实时的无服务器后端环境中。无需人工干预——代理会自动进行迭代开发。

Codehooks 提供免费试用计划，付费计划也不会对流量或 API 调用收取额外费用——让您无需担心使用成本即可放心部署代码。

⚠️ **警告：** 此技能允许代理在实时服务器上部署和运行代码。请审查代理的操作，设置适当的权限，并监控使用情况。您对代理部署的所有代码负责。

## 该技能的功能包括：

- **REST API**，支持自动生成 OpenAPI/Swagger 文档
- **即时 CRUD API**，使用 `crudlify()` 实现并带有模式验证功能
- **Webhook 端点**，可供外部服务（如 Stripe、GitHub、Shopify 等）调用
- **持久化存储**（非关系型数据库 + 键值存储）
- **后台任务**，可全天候运行
- **队列处理**，用于异步处理
- **自动化工作流程**，支持重试、分支和状态管理

## 设置

**管理员只需执行一次：**
```bash
npm install -g codehooks
coho login
coho create openclaw-backend
coho add-admintoken
```

将管理员令牌提供给您的代理。

**代理使用：**
```bash
export CODEHOOKS_ADMIN_TOKEN="your-token-here"
coho deploy --admintoken $CODEHOOKS_ADMIN_TOKEN
```

现在，代理可以部署代码、查询数据以及管理后端了。

---

## 必备操作：加载开发环境

在开始构建之前，请运行以下命令：
```bash
coho prompt
```

该命令会输出完整的 Codehooks 开发环境信息——包括路由、数据库、队列、任务、工作流程以及完整的 codehooks-js API 信息。请将其复制到您的开发环境中，以便正确构建后端功能。

**macOS 快捷键：**
```bash
coho prompt | pbcopy
```

## 了解现有项目

在修改现有项目之前，请先全面了解项目状况：

```bash
# Returns JSON with collections, stats, recent deploys, and error logs
coho doctor

# Describe the app structure — collections, schemas, queues, files
coho describe
```

`coho doctor` 是最强大的诊断工具——它会返回结构化的 JSON 数据，包含数据库集合、文档数量、队列和工作者状态以及最近的错误日志。在加入现有项目或调试问题时，请务必运行此命令。

`coho describe` 可以提供项目的结构概览：显示存在的集合、它们的模式、已注册的队列以及已部署的文件。

---

## 代理可使用的命令

所有命令都支持 `--admintoken $CODEHOOKS_ADMIN_TOKEN` 选项（用于非交互式操作）。完整的 CLI 参考文档请参见：https://codehooks.io/docs/cli

| 命令 | 功能 |
|---------|--------------|
| `coho prompt` | 获取完整的开发环境信息 |
| `coho doctor` | 诊断项目状态（集合、统计信息、部署记录、错误日志） |
| `coho describe` | 描述应用程序结构（集合、模式、队列、文件） |
| `coho deploy` | 部署代码（5 秒内生效） |
| `coho info --examples` | 获取端点 URL 及相应的 cURL 示例 |
| `coho log -f` | 实时输出日志 |
| `coho query -c <collection> -q 'field=value'` | 查询数据库 |
| `coho queue-status` | 检查队列状态 |
| `coho workflow-status` | 检查工作流程状态 |
| `coho import -c <collection> --file data.json` | 导入数据 |
| `coho export -c <collection>` | 导出数据 |

---

## 代码示例

### 带有验证功能的即时 CRUD API
```javascript
import { app } from 'codehooks-js';
import * as Yup from 'yup';

const productSchema = Yup.object({
  name: Yup.string().required(),
  price: Yup.number().positive().required(),
  category: Yup.string().required()
});

// Creates GET, POST, PUT, DELETE endpoints automatically
// OpenAPI docs available at /.well-known/openapi
app.crudlify({ product: productSchema });

export default app.init();
```

### 存储传入数据的 Webhook
```javascript
import { app, Datastore } from 'codehooks-js';

// Allow webhook endpoint without JWT authentication
app.auth('/webhook', (req, res, next) => {
  next();
});

app.post('/webhook', async (req, res) => {
  const conn = await Datastore.open();
  await conn.insertOne('events', {
    ...req.body,
    receivedAt: new Date().toISOString()
  });
  res.json({ ok: true });
});

export default app.init();
```

### 每天上午 9 点运行的定时任务
```javascript
import { app, Datastore } from 'codehooks-js';

app.job('0 9 * * *', async (_, { jobId }) => {
  console.log(`Running job: ${jobId}`);
  const conn = await Datastore.open();
  const events = await conn.getMany('events', {}).toArray();
  console.log('Daily summary:', events.length, 'events');
});

export default app.init();
```

### 用于异步处理的队列工作者
```javascript
import { app, Datastore } from 'codehooks-js';

app.worker('processTask', async (req, res) => {
  const { task } = req.body.payload;
  const conn = await Datastore.open();
  await conn.updateOne('tasks', { _id: task.id }, { $set: { status: 'completed' } });
  res.end();
});

export default app.init();
```

### 具有重试功能的自动化工作流程
```javascript
import { app } from 'codehooks-js';

const workflow = app.createWorkflow('myTask', 'Process tasks autonomously', {
  begin: async function (state, goto) {
    console.log('Starting task:', state.taskId);
    goto('process', state);
  },
  process: async function (state, goto) {
    // Do work here - workflow handles retries and state
    state = { ...state, result: 'processed' };
    goto('complete', state);
  },
  complete: function (state, goto) {
    console.log('Done:', state.result);
    goto(null, state); // End workflow
  }
});

// Agent starts workflow via API
app.post('/start', async (req, res) => {
  const result = await workflow.start(req.body);
  res.json(result);
});

export default app.init();
```

---

## 重要注意事项：

- `getMany()` 方法返回数据流——当需要操作数据（排序、过滤、映射等）时，请使用 `.toArray()` 方法。
- **Webhook 签名验证**：使用 `req.rawBody` 而不是 `req.body`。
- **注意文件系统访问权限**：由于这是一个无服务器环境，`fs`、`path`、`os` 等模块不可用。
- **敏感信息管理**：使用 `process.env.VARIABLE_NAME` 来存储 API 密钥和敏感数据。
- **静态文件处理**：`app.static({ route: '/app', directory: '/public' })` 用于提供静态资源。
- **文件存储**：`app.storage({ route: '/docs', directory: '/uploads' })` 用于存储上传的文件。

---

## 开发流程：

1. 代理运行 `coho prompt` 以加载开发环境信息。
2. 对于现有项目，代理运行 `coho doctor` 和 `coho describe` 以了解已部署的内容。
3. 代理使用 Codehooks-js 的开发模式编写代码。
4. 代理运行 `coho deploy`（5 秒内部署代码）。
5. 代理使用 `coho log -f` 验证代码，或使用 `coho info --examples` 测试端点功能。
6. 代理会持续迭代开发——这种快速部署机制有助于提升开发效率。

---

## 适用场景：

- 当您需要为 Stripe、GitHub、Shopify 等服务提供可靠的 Webhook URL 时。
- 当您需要将数据存储在本地机器之外的持久化环境中时。
- 当您需要定时任务在设备关闭时仍能自动运行时。
- 当您希望将敏感的 API 集成到沙箱环境中时。
- 当您需要异步处理任务时。
- 当您需要实现具有重试机制的自动化多步骤工作流程时。

---

## 参考资源：

- **文档**：https://codehooks.io/docs
- **CLI 参考**：https://codehooks.io/docs/cli
- **AI 帮助**：运行 `coho prompt` 或访问 https://codehooks.io/llms.txt
- **模板**：https://github.com/RestDB/codehooks-io-templates
- **MCP 服务器**：https://github.com/RestDB/codehooks-mcp-server