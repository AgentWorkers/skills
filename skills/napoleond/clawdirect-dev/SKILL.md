---
name: clawdirect-dev
description: 使用基于 ATXP 的认证机制，按照 ClawDirect 的设计模式来构建面向代理（agents）的 Web 用户界面。在开发需要 AI 代理通过 MCP 工具进行交互的网站、实现基于 Cookie 的代理认证功能，或为 Web 应用程序创建代理技能时，可以运用这一技能。该技能提供了使用 @longrun/turtle、Express、SQLite 和 ATXP 的模板支持。
---

# ClawDirect-Dev

使用基于ATXP的认证机制来构建面向代理的Web体验。

**参考实现**: https://github.com/napoleond/clawdirect

## 什么是ATXP？

ATXP（Agent Transaction Protocol，代理事务协议）允许AI代理进行身份验证并支付服务费用。在构建面向代理的网站时，ATXP提供了以下功能：

- **代理身份验证**：确定发起请求的代理是谁
- **费用结算**：对高级操作进行收费（可选）
- **MCP集成**：提供代理可以编程调用的工具

有关ATXP的更多详细信息，请访问：https://skills.sh/atxp-dev/cli/atxp

## 代理的交互方式

代理可以通过两种方式与您的网站进行交互：

1. **浏览器**：代理使用浏览器自动化工具访问您的网站，点击按钮、填写表单并浏览页面——就像人类用户一样。
2. **MCP工具**：代理直接调用您的MCP端点来执行编程操作（如身份验证、支付等）。

基于cookie的认证机制可以桥接这两种交互方式：代理通过MCP获取认证cookie，然后在浏览过程中使用该cookie。

**重要提示**：代理的浏览器通常无法直接设置仅限HTTP的cookie。推荐的做法是让代理通过查询字符串传递cookie值（例如：`?myapp_cookie=XYZ`），然后由服务器设置cookie并重定向到一个新的URL。

## 架构概述

```
┌──────────────────────────────────────────────────────────────────┐
│                         AI Agent                                 │
│  ┌─────────────────────┐         ┌─────────────────────────┐    │
│  │   Browser Tool      │         │   MCP Client            │    │
│  │   (visits website)  │         │   (calls tools)         │    │
│  └─────────┬───────────┘         └───────────┬─────────────┘    │
└────────────┼─────────────────────────────────┼──────────────────┘
             │                                 │
             ▼                                 ▼
┌────────────────────────────────────────────────────────────────┐
│                    Your Application                             │
│  ┌─────────────────────┐    ┌─────────────────────────┐        │
│  │   Web Server        │    │   MCP Server            │        │
│  │   (Express)         │    │   (@longrun/turtle)     │        │
│  │                     │    │                         │        │
│  │   - Serves UI       │    │   - yourapp_cookie      │        │
│  │   - Cookie auth     │    │   - yourapp_action      │        │
│  └─────────┬───────────┘    └───────────┬─────────────┘        │
│            │                            │                       │
│            └──────────┬─────────────────┘                       │
│                       ▼                                         │
│              ┌─────────────────┐                                │
│              │     SQLite      │                                │
│              │   auth_cookies  │                                │
│              └─────────────────┘                                │
└─────────────────────────────────────────────────────────────────┘
```

## 构建步骤

1. **与您的网站一起创建MCP服务器**
2. **在MCP服务器中实现cookie认证机制**
3. **在您的Web API中使用cookie进行身份验证**
4. **为您的网站发布一个代理技能**

## 第一步：项目设置

使用所需的开发工具包初始化一个Node.js项目：

```bash
mkdir my-agent-app && cd my-agent-app
npm init -y
npm install @longrun/turtle @atxp/server @atxp/express better-sqlite3 express cors dotenv zod
npm install -D typescript @types/node @types/express @types/cors @types/better-sqlite3 tsx
```

创建`tsconfig.json`文件：
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"]
}
```

创建`.env`文件：
```
FUNDING_DESTINATION_ATXP=<your_atxp_account>
PORT=3001
```

## 第二步：使用cookie认证的数据库

创建`src/db.ts`文件：
```typescript
import Database from 'better-sqlite3';
import crypto from 'crypto';

const DB_PATH = process.env.DB_PATH || './data.db';
let db: Database.Database;

export function getDb(): Database.Database {
  if (!db) {
    db = new Database(DB_PATH);
    db.pragma('journal_mode = WAL');

    // Auth cookies table - maps cookies to ATXP accounts
    db.exec(`
      CREATE TABLE IF NOT EXISTS auth_cookies (
        cookie_value TEXT PRIMARY KEY,
        atxp_account TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);

    // Add your app's tables here
  }
  return db;
}

export function createAuthCookie(atxpAccount: string): string {
  const cookieValue = crypto.randomBytes(32).toString('hex');
  getDb().prepare(`
    INSERT INTO auth_cookies (cookie_value, atxp_account)
    VALUES (?, ?)
  `).run(cookieValue, atxpAccount);
  return cookieValue;
}

export function getAtxpAccountFromCookie(cookieValue: string): string | null {
  const result = getDb().prepare(`
    SELECT atxp_account FROM auth_cookies WHERE cookie_value = ?
  `).get(cookieValue) as { atxp_account: string } | undefined;
  return result?.atxp_account || null;
}
```

## 第三步：使用cookie认证的MCP工具

创建`src/tools.ts`文件：
```typescript
import { defineTool } from '@longrun/turtle';
import { z } from 'zod';
import { requirePayment, atxpAccountId } from '@atxp/server';
import BigNumber from 'bignumber.js';
import { createAuthCookie } from './db.js';

// Cookie tool - agents call this to get browser auth
export const cookieTool = defineTool(
  'myapp_cookie',  // Replace 'myapp' with your app name
  'Get an authentication cookie for browser use. Set this cookie to authenticate when using the web interface.',
  z.object({}),
  async () => {
    // Free but requires ATXP auth
    const accountId = atxpAccountId();
    if (!accountId) {
      throw new Error('Authentication required');
    }

    const cookie = createAuthCookie(accountId);

    return JSON.stringify({
      cookie,
      instructions: 'To authenticate in a browser, navigate to https://your-domain.com?myapp_cookie=<cookie_value> - the server will set the HTTP-only cookie and redirect. Alternatively, set the cookie directly if your browser tool supports it.'
    });
  }
);

// Example paid tool
export const paidActionTool = defineTool(
  'myapp_action',
  'Perform some action. Cost: $0.10',
  z.object({
    input: z.string().describe('Input for the action')
  }),
  async ({ input }) => {
    await requirePayment({ price: new BigNumber(0.10) });

    const accountId = atxpAccountId();
    if (!accountId) {
      throw new Error('Authentication required');
    }

    // Your action logic here
    return JSON.stringify({ success: true, input });
  }
);

export const allTools = [cookieTool, paidActionTool];
```

## 第四步：使用cookie验证的Express API

创建`src/api.ts`文件：
```typescript
import { Router, Request, Response } from 'express';
import { getAtxpAccountFromCookie } from './db.js';

export const apiRouter = Router();

// Helper to extract cookie
function getCookieValue(req: Request, cookieName: string): string | null {
  const cookieHeader = req.headers.cookie;
  if (!cookieHeader) return null;

  const cookies = cookieHeader.split(';').map(c => c.trim());
  for (const cookie of cookies) {
    if (cookie.startsWith(`${cookieName}=`)) {
      return cookie.substring(cookieName.length + 1);
    }
  }
  return null;
}

// Middleware to require cookie auth
function requireCookieAuth(req: Request, res: Response, next: Function) {
  const cookieValue = getCookieValue(req, 'myapp_cookie');

  if (!cookieValue) {
    res.status(401).json({
      error: 'Authentication required',
      message: 'Use the myapp_cookie MCP tool to get an authentication cookie'
    });
    return;
  }

  const atxpAccount = getAtxpAccountFromCookie(cookieValue);
  if (!atxpAccount) {
    res.status(401).json({
      error: 'Invalid cookie',
      message: 'Your cookie is invalid or expired. Get a new one via the MCP tool.'
    });
    return;
  }

  // Attach account to request for use in handlers
  (req as any).atxpAccount = atxpAccount;
  next();
}

// Public endpoint (no auth)
apiRouter.get('/api/public', (_req: Request, res: Response) => {
  res.json({ message: 'Public data' });
});

// Protected endpoint (requires cookie auth)
apiRouter.post('/api/protected', requireCookieAuth, (req: Request, res: Response) => {
  const account = (req as any).atxpAccount;
  res.json({ message: 'Authenticated action', account });
});
```

## 第五步：服务器入口点

创建`src/index.ts`文件：
```typescript
import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { createServer } from '@longrun/turtle';
import { atxpExpress } from '@atxp/express';
import { getDb } from './db.js';
import { allTools } from './tools.js';
import { apiRouter } from './api.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const FUNDING_DESTINATION = process.env.FUNDING_DESTINATION_ATXP;
if (!FUNDING_DESTINATION) {
  throw new Error('FUNDING_DESTINATION_ATXP is required');
}

const PORT = process.env.PORT ? parseInt(process.env.PORT) : 3001;

async function main() {
  // Initialize database
  getDb();

  // Create MCP server
  const mcpServer = createServer({
    name: 'myapp',
    version: '1.0.0',
    tools: allTools
  });

  // Create Express app
  const app = express();
  app.use(cors());
  app.use(express.json());

  // Cookie bootstrap middleware - handles ?myapp_cookie=XYZ for agent browsers
  // Agent browsers often can't set HTTP-only cookies directly, so they pass the cookie
  // value in the query string and the server sets it, then redirects to clean URL
  app.use((req, res, next) => {
    const cookieValue = req.query.myapp_cookie;
    if (typeof cookieValue === 'string' && cookieValue.length > 0) {
      res.cookie('myapp_cookie', cookieValue, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'lax',
        path: '/',
        maxAge: 30 * 24 * 60 * 60 * 1000 // 30 days
      });
      const url = new URL(req.originalUrl, `http://${req.headers.host}`);
      url.searchParams.delete('myapp_cookie');
      res.redirect(302, url.pathname + url.search || '/');
      return;
    }
    next();
  });

  // Mount MCP server with ATXP at /mcp
  app.use('/mcp', atxpExpress({
    fundingDestination: FUNDING_DESTINATION,
    handler: mcpServer.handler
  }));

  // Mount API routes
  app.use(apiRouter);

  // Serve static frontend (if you have one)
  app.use(express.static(join(__dirname, '..', 'public')));

  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
    console.log(`  - MCP endpoint: http://localhost:${PORT}/mcp`);
    console.log(`  - API endpoint: http://localhost:${PORT}/api`);
  });
}

main().catch(console.error);
```

## 第六步：创建代理技能

为代理创建一个可以与您的应用程序交互的技能。具体结构如下：

```
my-skill/
└── SKILL.md
```

## SKILL.md模板

```markdown
---
name: myapp
description: Interact with MyApp. Use this skill to [describe what agents can do]. Requires ATXP authentication.
---

# MyApp

[Brief description] at **https://your-domain.com**

## Quick Start

1. Install ATXP: `npx skills add atxp-dev/cli --skill atxp`
2. Call MCP tools: `npx atxp-call https://your-domain.com/mcp <tool> [params]`

## Authentication

Get a cookie for browser use:

\`\`\`bash
npx atxp-call https://your-domain.com/mcp myapp_cookie '{}'
\`\`\`

If using a browser, navigate with the cookie in the query string:

\`\`\`
https://your-domain.com?myapp_cookie=<cookie_value>
\`\`\`

The server will set the HTTP-only cookie and redirect to clean the URL.

**Alternative** (if your browser tool supports direct cookie setting):
- **Cookie name**: `myapp_cookie`
- **Cookie value**: Value from tool response
- **Domain**: `your-domain.com`
- **Path**: `/`
- **HttpOnly**: `true`

## MCP Tools

| Tool | Description | Cost |
|------|-------------|------|
| `myapp_cookie` | Get auth cookie | Free |
| `myapp_action` | Perform action | $0.10 |

For ATXP details: https://skills.sh/atxp-dev/cli/atxp
```

## 部署

生成的代码可以部署到任何托管服务中：

- [Render](https://render.com) - 提供持久化存储的简单Node.js托管服务
- [Railway](https://railway.app) - 通过Git进行简单部署
- [Fly.io](https://fly.io) - 全球边缘部署服务
- [DigitalOcean App Platform](https://www.digitalocean.com/products/app-platform)
- [Heroku](https://heroku.com)

请确保您的托管服务满足以下要求：
- 支持Node.js 18及以上版本
- 提供用于SQLite的持久化存储（或更换为PostgreSQL）
- 支持环境变量配置

## 参考资料

完整的示例代码：https://github.com/napoleond/clawdirect

需要学习的重点文件：
- `src/tools.ts`：包含ATXP支付功能的MCP工具定义
- `src/db.ts`：cookie认证的数据库模式
- `src/api.ts`：包含cookie验证功能的Express路由
- `src/index.ts`：包含Turtle框架和ATXP认证的服务器设置
- `docs/agent-cookie-auth.md`：认证机制的详细文档

有关ATXP认证的更多信息，请访问：https://skills.sh/atxp-dev/cli/atxp

## 将您的项目添加到ClawDirect

当您的面向代理的网站准备就绪后，将其添加到https://claw.direct目录中，以便其他代理能够发现并使用它。

### 添加新条目

**费用**：0.50美元

**所需参数**：
- `url`（必填）：网站的唯一URL
- `name`（必填）：显示名称（最多100个字符）
- `description`（必填）：网站的功能描述（最多500个字符）
- `thumbnail`（必填）：Base64编码的图片
- `thumbnailMime`（必填）：图片格式（`image/png`、`image/jpeg`、`image/gif`、`image/webp`之一）

### 编辑现有条目

编辑您拥有的条目：

**费用**：0.10美元

**所需参数**：
- `url`（必填）：要编辑的条目的URL（必须由所有者提供）
- `description`（可选）：新的描述内容
- `thumbnail`（可选）：新的Base64编码图片
- `thumbnailMime`（可选）：新的图片格式（MIME类型）