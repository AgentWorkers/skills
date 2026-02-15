---
name: chatgpt-apps
description: **完整的 ChatGPT 应用程序构建工具**  
- 允许您创建、设计、实现、测试并部署 ChatGPT 应用程序。  
- 支持与 MCP 服务器（MCP Servers）集成，可添加各种组件（Widgets）和实现身份验证（Auth）功能。  
- 支持数据库集成（Database Integration），确保应用程序的数据安全与高效管理。  
- 提供自动化部署（Automated Deployment）功能，简化应用程序的上线流程。
homepage: https://github.com/hollaugo/prompt-circle-claude-plugins
user-invocable: true
---

# ChatGPT 应用程序构建器

这是一个从概念到生产环境，用于构建、测试和部署 ChatGPT 应用程序的完整工作流程。

## 命令

- `/chatgpt-apps new` - 创建一个新的 ChatGPT 应用程序
- `/chatgpt-apps add-tool` - 为应用程序添加一个 MCP 工具
- `/chatgpt-apps add-widget` - 为应用程序添加一个插件（widget）
- `/chatgpt-apps add-auth` - 配置认证
- `/chatgpt-apps add-database` - 设置数据库
- `/chatgpt-apps validate` - 验证应用程序
- `/chatgpt-apps test` - 运行测试
- `/chatgpt-apps deploy` - 部署到生产环境
- `/chatgpt-apps resume` - 恢复对应用程序的编辑

---

## 目录

1. [创建新应用程序](#1-create-new-app)
2. [添加 MCP 工具](#2-add-mcp-tool)
3. [添加插件](#3-add-widget)
4. [添加认证](#4-add-authentication)
5. [添加数据库](#5-add-database)
6. [生成测试提示](#6-generate-golden-prompts)
7. [验证应用程序](#7-validate-app)
8. [测试应用程序](#8-test-app)
9. [部署应用程序](#9-deploy-app)
10. [恢复应用程序](#10-resume-app)

---

## 1. 创建新应用程序

**目的：** 从概念到可运行的代码，创建一个新的 ChatGPT 应用程序。

### 工作流程

#### 第一阶段：概念化

1. **询问应用程序想法**
   “您想构建什么样的 ChatGPT 应用程序？描述它的功能以及它解决的问题。”

2. **根据用户体验原则进行分析**
   - **对话性利用**：用户可以通过自然语言完成什么操作？
   - **原生集成**：该应用程序如何与 ChatGPT 的对话流程集成？
   - **组合性**：这些工具可以独立工作，并与其他应用程序结合使用吗？

3. **检查反模式**
   - 静态网站内容显示
   - 需要外部标签页的复杂多步骤工作流程
   - 重复 ChatGPT 的原生功能
   - 广告或附加销售

4. **定义用例**
   创建 3-5 个主要用例和用户故事。

#### 第二阶段：设计

1. **工具拓扑结构**
   - 查询工具（readOnlyHint: true）
   - 修改工具（destructiveHint: false）
   - 删除工具（destructiveHint: true）
   - 插件工具（返回包含 `_meta` 的 UI）
   - 外部 API 工具（openWorldHint: true）

2. **插件设计**
   对于每个插件：
   - `id` - 唯一标识符（使用 kebab-case 格式）
   - `name` - 显示名称
   - `description` - 显示的内容
   - `mockData` - 用于预览的示例数据

3. **数据模型**
   设计实体和关系。

4. **认证需求**
   - 单用户（无需认证）
   - 多用户（使用 Auth0 或 Supabase Auth）

#### 第三阶段：实现

使用以下结构生成完整的应用程序：

```
{app-name}/
├── package.json
├── tsconfig.server.json
├── setup.sh
├── START.sh
├── .env.example
├── .gitignore
└── server/
    └── index.ts
```

**关键要求：**
- 来自 `@modelcontextprotocol/sdk/server/index.js` 的 `Server` 类
- 用于会话管理的 `StreamableHTTPServerTransport`
- 插件 URI：`ui://widget/{widget-id}.html`
- 插件 MIME 类型：`text/html+skybridge`
- 工具响应中包含 `structuredContent`
- 工具中包含 `_meta` 和 `openai/outputTemplate`

#### 第四阶段：测试
- 运行设置：`./setup.sh`
- 启动开发模式：`./START.sh --dev`
- 预览插件：`http://localhost:3000/preview`
- 测试 MCP 连接

#### 第五阶段：部署
- 生成 Dockerfile 和 render.yaml
- 部署到 Render 环境
- 配置 ChatGPT 连接器

---

## 2. 添加 MCP 工具

**目的：** 为您的 ChatGPT 应用程序添加一个新的 MCP 工具。

### 工作流程

1. **收集信息**
   - 该工具的功能是什么？
   - 它需要哪些输入？
   - 它返回什么结果？

2. **分类工具类型**
   - **查询**（readOnlyHint: true）- 获取数据
   - **修改**（destructiveHint: false）- 创建/更新数据
   - **删除**（destructiveHint: true）- 删除数据
   - **插件** - 返回 UI 内容
   - **外部**（openWorldHint: true）- 调用外部 API

3. **设计输入模式**
   使用 Zod 模型创建输入结构，并指定相应的类型和描述。

4. **生成工具处理器**
   使用 `chatgpt-mcp-generator` 代理生成：
   - `server/tools/` 目录下的工具处理器
   - Zod 模型导出
   - 类型导出
   - 如果需要，还包括数据库查询

5. **注册工具**
   更新 `server/index.ts` 文件中的元数据：
   ```typescript
   {
     name: "my-tool",
     _meta: {
       "openai/toolInvocation/invoking": "Loading...",
       "openai/toolInvocation/invoked": "Done",
       "openai/outputTemplate": "ui://widget/my-widget.html", // if widget
     }
   }
   ```

6. **更新状态**
   将工具添加到 `.chatgpt-app/state.json` 文件中。

### 工具命名规则
使用 kebab-case 格式：`list-items`、`create-task`、`show-recipe-detail`

### 注释指南

| 场景 | readOnlyHint | destructiveHint | openWorldHint |
|----------|--------------|-----------------|---------------|
| 列出/获取 | true | false | false |
| 创建/更新 | false | false | false |
| 删除 | false | true | false |
| 外部 API | 变化较大 | 变化较大 | true |

---

## 3. 添加插件

**目的：** 添加内联 HTML 插件，支持 HTML/CSS/JS 以及与应用程序 SDK 的集成。

### 5 种插件类型

1. **卡片网格** - 显示多个项目
2. **统计仪表板** - 显示关键指标
3. **表格** - 以表格形式显示数据
4. **条形图** - 简单的可视化效果
5. **详细信息插件** - 显示单个项目的详细信息

### 工作流程

1. **收集信息**
   - 插件的用途和所需数据
   - 视觉设计（卡片、表格、图表等）
   - 需要的交互性

2. **定义数据结构**
   使用 TypeScript 接口文档化预期的数据结构。

3. **添加插件配置**
   ```typescript
   const widgets: WidgetConfig[] = [
     {
       id: "my-widget",
       name: "My Widget",
       description: "Displays data",
       templateUri: "ui://widget/my-widget.html",
       invoking: "Loading...",
       invoked: "Ready",
       mockData: { /* sample */ },
     },
   ];
   ```

4. **生成插件 HTML**
   生成 HTML 代码，包括：
   - 预览模式支持（`window.PREVIEW_DATA`）
   - OpenAI 应用程序 SDK 集成（`window.openai.toolOutput`）
   - 事件监听器（`openai:setglobals`）
   - 超时设置（100 毫秒，10 秒）

5. **创建/更新工具**
   通过 `widgetId` 将工具链接到插件。

6. **测试插件**
   在 `/preview/{widget-id}` 上使用模拟数据预览插件。

### 插件 HTML 结构

```javascript
(function() {
  let rendered = false;

  function render(data) {
    if (rendered || !data) return;
    rendered = true;
    // Render logic
  }

  function tryRender() {
    if (window.PREVIEW_DATA) { render(window.PREVIEW_DATA); return; }
    if (window.openai?.toolOutput) { render(window.openai.toolOutput); }
  }

  window.addEventListener('openai:set_globals', tryRender);

  const poll = setInterval(() => {
    if (window.openai?.toolOutput || window.PREVIEW_DATA) {
      tryRender();
      clearInterval(poll);
    }
  }, 100);
  setTimeout(() => clearInterval(poll), 10000);

  tryRender();
})();
```

---

## 4. 添加认证

**目的：** 使用 Auth0 或 Supabase Auth 配置认证。

### 何时添加认证
- 当应用程序支持多用户时
- 当需要为每个用户存储持久化私有数据时
- 当需要用户特定的 API 凭据时

### 提供者

**Auth0：**
- 企业级认证服务
- OAuth 2.1，PKCE 流程
- 社交登录（Google、GitHub 等）

**Supabase Auth：**
- 更简单的设置
- 默认使用电子邮件/密码
- 与 Supabase 数据库集成

### 工作流程

1. **根据需求选择提供者**
   根据用户需求选择合适的认证方式。

2. **指导设置**
   - **Auth0：** 创建应用程序，配置回调 URL，获取凭据
   - **Supabase：** 已经配置好了数据库连接

3. **生成认证代码**
   使用 `chatgpt-auth-generator` 代理生成：
   - 会话管理中间件
   - 用户主体提取
   - 令牌验证

4. **更新服务器**
   在服务器中添加认证中间件以保护路由。

5. **更新环境**
   ```bash
   # Auth0
   AUTH0_DOMAIN=your-tenant.auth0.com
   AUTH0_CLIENT_ID=...
   AUTH0_CLIENT_SECRET=...
   
   # Supabase (from database setup)
   SUPABASE_URL=...
   SUPABASE_ANON_KEY=...
   ```

6. **测试**
   验证登录流程和用户隔离机制。

---

## 5. 添加数据库

**目的：** 使用 Supabase 配置 PostgreSQL 数据库。

### 何时添加数据库
- 当需要存储用户数据时
- 当需要处理多实体关系时
- 当需要查询/过滤数据时

### 工作流程

1. **检查 Supabase 设置**
   确认账户和项目已创建。

2. **收集凭据**
   - 项目 URL
   - 公共访问密钥（anon key）
   - 服务端角色密钥（server-side）

3. **定义实体**
   为每个实体指定：
   - 字段和类型
   - 关系
   - 索引

4. **生成数据库模式**
   使用 `chatgpt-database-generator` 代理生成 SQL 语句：
   - `id`（UUID 主键）
   - `user_subject`（varchar，带索引）
   - `created_at`（timestamptz）
   - `updated_at`（timestamptz）
   - 用于用户隔离的 RLS（Row Level Security）策略

5. **设置连接池**
   ```typescript
   import { createClient } from '@supabase/supabase-js';
   
   const supabase = createClient(
     process.env.SUPABASE_URL!,
     process.env.SUPABASE_SERVICE_ROLE_KEY!
   );
   ```

6. **应用迁移**
   在 Supabase 控制面板或通过迁移工具执行 SQL 语句。

### 查询模式
始终通过 `user_subject` 进行过滤：

```typescript
const { data } = await supabase
  .from('tasks')
  .select('*')
  .eq('user_subject', userSubject);
```

## 6. 生成测试提示

**目的：** 生成测试提示，以确保 ChatGPT 能正确调用工具。

### 重要性
- 测量精确度和召回率
- 便于迭代
- 发布后进行监控

### 3 种提示类型

1. **直接提示** - 明确指定工具的调用
   - “显示我的任务列表”
   - “创建一个名为...的新任务”

2. **间接提示** - 基于结果，让 ChatGPT 自动推断工具
   - “我今天需要做什么？”
   - “帮我整理工作”

3. **否定提示** - 不应触发任何工具
   - “什么是任务？”
   - “告诉我关于项目管理的信息”

### 工作流程

1. **分析工具**
   查看每个工具的功能和输入参数。

2. **生成提示**
   为每个工具生成：
   - 5 个以上直接提示
   - 5 个以上间接提示
   - 3 个否定提示
   - 2 个边缘情况提示

3. **最佳实践**
   - 工具描述以 “在以下情况下使用...” 开头
   - 清晰说明工具的限制
   - 在描述中包含使用示例

4. **保存结果**
   将提示保存到 `.chatgpt-app/golden-prompts.json` 文件中：
   ```json
   {
     "toolName": {
       "direct": ["prompt1", "prompt2"],
       "indirect": ["prompt1", "prompt2"],
       "negative": ["prompt1", "prompt2"],
       "edge": ["prompt1", "prompt2"]
     }
   }
   ```

---

## 7. 验证应用程序

**目的：** 在部署前进行验证。

### 10 项验证检查

1. **必需文件**
   - `package.json`
   - `tsconfig.server.json`
   - `setup.sh`（可执行文件）
   - `START.sh`（可执行文件）
   - `server/index.ts`
   - `.env.example`

2. **服务器实现**
   - 使用 MCP SDK 中的 `Server` 类
   - 具有 `StreamableHTTPServerTransport`
   - 使用 Map 进行会话管理
   - 正确的请求处理程序

3. **插件配置**
   - `widgets` 数组存在
   - 每个插件都有 id、名称、描述和模板 URI
   - URI 符合 `ui://widget/{id}.html` 的模式

4. **工具响应格式**
   - 返回 `structuredContent`（而不仅仅是纯文本）
   - 插件工具包含 `_meta` 和 `openai/outputTemplate`

5. **资源处理程序格式**
   - MIME 类型：`text/html+skybridge`
   - 返回包含序列化和 CSP（Content Security Policy）的 `_meta` 标签

6. **插件 HTML 结构**
   - 支持预览模式
   - 为应用程序 SDK 提供事件监听器
   - 提供超时处理（100 毫秒，10 秒）

7. **端点存在性**
   - `/health` - 健康检查端点
   - `/preview` - 插件预览端点
   - `/preview/:widgetId` - 单个插件预览端点
   - `/mcp` - MCP 端点

8. **package.json 脚本**
   - 包含 `build:server` 脚本
   - 包含 `start` 脚本（设置为 HTTP_MODE=true）
   - 包含 `dev` 脚本（用于开发模式）
   - 不包含用于 Web 构建的脚本（web/、ui/、client/）

9. **注释验证**
   - `readOnlyHint` 设置正确
   - 对于删除操作，设置 `destructiveHint`
   - 对于外部 API，设置 `openWorldHint`

10. **数据库验证**（如果启用）
    - 表格包含必需的字段
    - `user_subject` 字段已索引
    - RLS 策略已启用

### 常见错误

| 错误 | 修复方法 |
|-------|-----|
| 缺少 structuredContent | 在工具响应中添加相应内容 |
| 插件 URI 错误 | 使用 `ui://widget/{id}.html` |
| 未配置会话管理 | 添加 `Map<string, Transport>` 中间件 |
| 缺少 `_meta` | 在工具定义和响应中添加 `_meta` |
| MIME 类型错误 | 使用 `text/html+skybridge` |

**注意：** 在进行其他验证之前，务必先检查文件是否存在！**

---

## 8. 测试应用程序

**目的：** 使用 MCP Inspector 和测试提示运行自动化测试。

### 4 类测试

1. **MCP 协议**
   - 服务器启动时无错误
   - 正确处理初始化
   - 正确列出所有工具
   - 正确列出所有资源

2. **模式验证**
   - 工具模式是有效的 Zod 格式
   - 必需字段已标记
   - 类型与实现匹配

3. **插件测试**
   - 所有插件都能在预览模式下正确显示
   - 模拟数据能正确加载
   - 控制台无错误输出

4. **测试提示**
   - 直接提示能正确触发相应的工具
   - 间接提示能按预期工作
   - 否定提示不会触发任何工具

### 工作流程

1. **以测试模式启动服务器**
   ```bash
   HTTP_MODE=true NODE_ENV=test npm run dev
   ```

2. **运行 MCP Inspector**
   测试协议合规性：
   - 初始化连接
   - 列出所有工具
   - 使用有效输入调用每个工具
   - 检查响应

3. **模式验证**
   确认模式文件能正确编译并与实现匹配

4. **测试提示**
   使用 ChatGPT 测试提示：
   - 记录调用了哪个工具
   - 与预期工具进行比较
   - 计算精确度和召回率

5. **生成报告**
   ```json
   {
     "passed": 42,
     "failed": 3,
     "categories": {
       "mcp": "✅",
       "schema": "✅",
       "widgets": "✅",
       "prompts": "⚠️ 3 failures"
     },
     "timing": "2.3s"
   }
   ```

### 处理失败
对于每个失败情况，说明：
- 什么出了问题
- 为什么失败
- 如何修复（附带代码示例）

---

## 9. 部署应用程序

**目的：** 将 ChatGPT 应用程序部署到 Render 环境，并进行健康检查。

### 先决条件

- ✅ 验证通过
- ✅ 测试通过
- ✅ Git 仓库已清理
- ✅ 环境变量已配置

### 工作流程

1. **飞行前检查**
   - 运行验证
   - 运行测试
   - 检查数据库连接（如果已启用）

2. **生成 render.yaml**
   ```yaml
   services:
     - type: web
       name: {app-name}
       runtime: docker
       plan: free
       healthCheckPath: /health
       envVars:
         - key: PORT
           value: 3000
         - key: HTTP_MODE
           value: true
         - key: NODE_ENV
           value: production
         - key: WIDGET_DOMAIN
           generateValue: true
         # Add auth/database vars if needed
   ```

3. **生成 Dockerfile**
   ```dockerfile
   FROM node:20-slim
   WORKDIR /app
   COPY package*.json ./
   RUN npm ci --only=production
   COPY dist ./dist
   EXPOSE 3000
   CMD ["node", "dist/server/index.js"]
   ```

4. **部署**
   **选项 A：自动化部署（如果 Render MCP 可用）**
   使用 Render MCP 代理进行部署。

   **选项 B：手动部署**
   - 将代码推送到 GitHub
   - 在 Render 控制面板中连接仓库
   - 设置环境变量
   - 部署应用程序

5. **验证部署**
   - 健康检查：`https://{app}.onrender.com/health`
   - MCP 端点：`https://{app}.onrender.com/mcp`
   - 工具能正常发现
   - 插件能正确显示

6. **配置 ChatGPT 连接器**
   - URL：`https://{app}.onrender.com/mcp`
   - 在 ChatGPT 中测试连接器的功能

---

## 10. 恢复应用程序的编辑

**目的：** 恢复对正在进行的 ChatGPT 应用程序的编辑。

### 工作流程

1. **加载状态**
   读取 `.chatgpt-app/state.json` 文件：
   ```json
   {
     "appName": "My Task Manager",
     "phase": "Implementation",
     "tools": ["list-tasks", "create-task"],
     "widgets": ["task-list"],
     "auth": false,
     "database": true,
     "validated": false,
     "deployed": false
   }
   ```

2. **显示进度**
   显示当前状态：
   - 应用程序名称
   - 当前阶段
   - 已完成的项（工具、插件）
   - 待处理的项（认证、验证、部署）

3. **提供下一步操作**
   根据当前阶段提供相应的操作建议：
   
   **概念阶段：**
   - “让我们设计工具和插件吧”
   - “我们开始实现吗？”

   **实现阶段：**
   - “再添加一个工具吗？”
   - “添加一个插件吗？”
   - “配置认证吗？”
   - “设置数据库吗？”

   **测试阶段：**
   - “生成测试提示吗？”
   - “运行测试吗？”
   - “运行测试吗？”

   **部署阶段：**
   - “部署到 Render 环境吗？”
   - “配置 ChatGPT 连接器吗？”

4. **继续工作**
   根据用户的选择，启动相应的流程。

---

## 最佳实践

1. **在每个重要步骤之后始终保存状态**
2. **在继续下一步之前进行验证**（尤其是在部署之前）
3. **使用代理工具生成代码**（如 `chatgpt-mcp-generator`、`chatgpt-auth-generator` 等）
4. **在每个阶段进行测试**（预览插件、测试工具、运行测试提示）
5. **保持用户交互体验** - 自然地引导用户完成整个流程
6. **在提供选择时解释各种选项的优缺点**（例如使用 Auth0 与 Supabase）
7. **在介绍新功能时提供示例**

---

## 状态管理

`.chatgpt-app/state.json` 文件用于跟踪应用程序的进度：

```json
{
  "appName": "string",
  "description": "string",
  "phase": "Concept" | "Implementation" | "Testing" | "Deployment",
  "tools": ["tool-name"],
  "widgets": ["widget-id"],
  "auth": {
    "enabled": boolean,
    "provider": "auth0" | "supabase" | null
  },
  "database": {
    "enabled": boolean,
    "entities": ["entity-name"]
  },
  "validated": boolean,
  "tested": boolean,
  "deployed": boolean,
  "deploymentUrl": "string | null",
  "goldenPromptsGenerated": boolean,
  "lastUpdated": "ISO timestamp"
}
```

---

## 命令参考

```bash
# Setup
./setup.sh

# Development
./START.sh --dev          # Dev mode with watch
./START.sh --preview      # Open preview in browser
./START.sh --stdio        # STDIO mode (testing)
./START.sh                # Production mode

# Testing
npm run validate          # Type checking
curl http://localhost:3000/health

# Deployment
git push origin main      # Trigger Render deploy
```

---

## 入门指南

当用户执行任何 `chatgpt-app` 命令时：

1. 检查 `.chatgpt-app/state.json` 文件是否存在
2. 如果存在 → 使用 **恢复应用程序** 流程
3. 如果不存在 → 使用 **创建新应用程序** 流程

始终引导用户按照以下自然流程进行操作：
**概念 → 实现 → 测试 → 部署**