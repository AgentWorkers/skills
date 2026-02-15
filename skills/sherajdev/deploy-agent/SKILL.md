---
name: deploy-agent
description: 多步骤部署代理，适用于全栈应用程序。流程包括：构建（Build）→ 测试（Test）→ 推送到 GitHub → 通过 Cloudflare Pages 发布；每个步骤均需要人工审核。
metadata:
  clawdbot:
    emoji: "🚀"
    requires:
      bins: ["gh", "wrangler", "git"]
---

# deploy-agent

通过多步骤工作流程部署全栈应用程序，每个步骤都需要人工审批。

## 快速入门

```bash
# Install via ClawdHub
clawdhub install deploy-agent

# Initialize a new deployment
deploy-agent init my-app

# Check status
deploy-agent status my-app

# Continue through steps
deploy-agent continue my-app
```

## 工作流程步骤

| 步骤 | 命令 | 说明 | 是否需要审批 |
|------|---------|-------------|-------------------|
| 1 | `deploy-agent init <名称>` | 启动部署 | ✅ 设计阶段 |
| 2 | `deploy-agent build <名称>` | 构建应用程序 | ✅ 测试之前 |
| 3 | `deploy-agent test <名称>` | 在本地测试 | ✅ 上推到 GitHub 之前 |
| 4 | `deploy-agent push <名称>` | 将代码推送到 GitHub | ✅ 上推到 Cloudflare 之前 |
| 5 | `deploy-agent deploy <名称>` | 部署到 Cloudflare | ✅ 最终步骤 |

## 命令

### 初始化部署
```bash
deploy-agent init my-app
```
创建一个新的部署状态并等待设计输入。

### 检查状态
```bash
deploy-agent status my-app
```
显示当前步骤、审批情况和部署信息。

### 继续
```bash
deploy-agent continue my-app
```
获取当前步骤的下一步操作指南。

### 构建（步骤 2）
```bash
deploy-agent build my-app
```
使用 C.R.A.B 完成设计后，运行此命令来构建应用程序。

### 测试（步骤 3）
```bash
deploy-agent test my-app
```
在上推之前验证应用程序是否在本地正常运行。

### 推送到 GitHub（步骤 4）
```bash
deploy-agent push my-app [repo-name]
```
创建 GitHub 仓库并推送代码。默认仓库名称 = 应用程序名称。

### 部署到 Cloudflare（步骤 5）
```bash
deploy-agent deploy my-app [custom-domain]
```
将应用程序部署到 Cloudflare Pages。默认域名：`{名称}.sheraj.org`

### 取消
```bash
deploy-agent cancel my-app
```
中止部署并清理相关资源。

### 列出所有部署
```bash
deploy-agent list
```
显示所有正在进行的部署。

## 示例会话

```bash
# Start new deployment
$ deploy-agent init my-blog
🚀 Deployment initialized: my-blog
Step 1: Design your app with C.R.A.B

# ... design phase with C.R.A.B ...

$ deploy-agent build my-blog
🚀 Build complete! Step 2: Local Testing
Start dev server: cd my-blog && npm run dev

# ... test locally ...

$ deploy-agent push my-blog
🚀 GitHub repository ready!
Say 'deploy-agent deploy my-blog' to deploy to Cloudflare

$ deploy-agent deploy my-blog my-blog.sheraj.org
🎉 Deployment complete!
App live at: https://my-blog.sheraj.org
```

## 状态管理

状态存储在：`~/.clawdbot/skills/deploy-agent/state/{部署名称}.json`

```json
{
  "name": "my-blog",
  "step": 5,
  "status": "deployed",
  "created_at": "2026-01-18T08:00:00Z",
  "repo_url": "https://github.com/user/my-blog",
  "domain": "https://my-blog.sheraj.org"
}
```

## 所需工具

| 工具 | 用途 |
|------|---------|
| `gh` | 创建和管理 GitHub 仓库 |
| `wrangler` | 部署到 Cloudflare Pages |
| `git` | 版本控制 |
| `jq` | JSON 解析（用于状态管理） |

## 配置

Cloudflare 令牌应配置在 `~/.wrangler.toml` 文件中：
```toml
[account]
api_token = "your-cloudflare-token"
```

## 注意事项

- 每次部署都是独立的 |
- 状态会在会话之间保持一致 |
- 每个关键步骤都需要人工审批 |
- 可以随时使用 “cancel” 命令中止部署 |

---

## Next.js + Cloudflare D1 部署指南

本节介绍了在 Cloudflare Pages 上部署 Next.js 应用程序时常见的陷阱及解决方法。

### 部署前的检查清单

| 检查项 | 命令 | 失败时的解决方法 |
|-------|---------|---------------|
| Next.js 版本 | `npm list next` | `npm install next@15.5.2` |
| `package-lock.json` 文件同步 | `rm -rf node_modules package-lock.json && npm install` | 提交 `package-lock.json` 文件 |
| Cloudflare 适配器 | `npm list @cloudflare/next-on-pages` | `npm install -D @cloudflare/next-on-pages` |
| 是否安装了 wrangler | `npm list wrangler` | `npm install -D wrangler` |

### 必需的配置文件

**1. package.json**
```json
{
  "dependencies": {
    "next": "15.5.2",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@cloudflare/next-on-pages": "^1.13.16",
    "wrangler": "^4.x"
  }
}
```

**2. wrangler.toml**
```toml
name = "my-app"
compatibility_date = "2026-01-18"
compatibility_flags = ["nodejs_compat"]

[[d1_databases]]
binding = "DB"
database_name = "my-db"
database_id = "your-db-id"
```

**3. API 路由（每个文件）**
```typescript
import { getRequestContext } from '@cloudflare/next-on-pages';

export const runtime = 'edge';

export async function GET() {
  const { env } = getRequestContext();
  const { results } = await env.DB.prepare("SELECT * FROM tasks").all();
  return Response.json({ data: results });
}
```

### Cloudflare Pages 的构建设置

| 设置 | 值 |
|---------|-------|
| 构建命令 | `npx @cloudflare/next-on-pages` |
| 输出目录 | `.vercel/output/static` |
| 是否启用函数 | 启用（对于 D1 API 路由） |

### 常见问题及解决方法

| 问题 | 错误信息 | 解决方法 |
|-------|-------|-----|
| `package-lock.json` 文件不匹配 | `npm ci` 只能在 `package.json` 和 `package-lock.json` 文件一致时安装包 | `rm -rf node_modules package-lock.json && npm install && git add package-lock.json` |
| Next.js 版本 | `peer next@">=14.3.0 && <=15.5.2"`（来自 @cloudflare/next-on-pages） | 将版本降级为 `next: "15.5.2"` |
| API 路由未配置为 Edge 运行模式 | “以下路由未配置为 Edge 运行模式” | 添加 `export const runtime = 'edge';` |
| D1 访问模式 | 使用 `context.env.DB` | 应使用 `getRequestContext().env.DB` |
| 类型定义缺失 | TypeScript 报错 | 创建 `env.d.ts` 文件并定义 `CloudflareEnv` 接口 |

### CSS 问题（滚动条闪烁）
```css
html {
  overflow-x: hidden;
  scrollbar-gutter: stable;
}
body {
  overflow-x: hidden;
}
```

### 部署后的操作

1. 登录 Cloudflare 控制台 → 设置 → 函数
2. 添加 D1 相关配置：变量名 `DB` → 选择相应的数据库

### 参考文档

- 完整指南：`docs/issues/nextjs-cloudflare-d1-deployment.md`
- Cloudflare 官方文档：https://developers.cloudflare.com/pages/framework-guides/nextjs/