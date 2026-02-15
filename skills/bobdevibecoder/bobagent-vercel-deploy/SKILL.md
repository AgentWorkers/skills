---
name: vercel-deploy
description: 将应用程序和网站部署到 Vercel。当用户请求执行部署操作（如“部署我的应用程序”、“将其部署到生产环境”、“创建预览版本”、“部署后提供链接”或“立即上线”）时，请使用此技能。无需身份验证——系统会返回预览 URL 和可使用的部署链接。
metadata:
  author: vercel
  version: "1.0.0"
---

# Vercel 部署

您可以立即将任何项目部署到 Vercel 上，无需进行身份验证。

## 工作原理

1. 将您的项目打包成一个 tarball 文件（不包括 `node_modules` 和 `.git` 文件夹）。
2. 从 `package.json` 文件中自动检测所使用的框架。
3. 将打包后的文件上传到 Vercel 的部署服务。
4. 返回 **预览 URL**（实时站点）和 ** Claim URL**（用于将项目转移到您的 Vercel 账户）。

## 使用方法

```bash
bash /mnt/skills/user/vercel-deploy/scripts/deploy.sh [path]
```

**参数：**
- `path` - 需要部署的目录，或一个 `.tgz` 文件（默认为当前目录）。

**示例：**

```bash
# Deploy current directory
bash /mnt/skills/user/vercel-deploy/scripts/deploy.sh

# Deploy specific project
bash /mnt/skills/user/vercel-deploy/scripts/deploy.sh /path/to/project

# Deploy existing tarball
bash /mnt/skills/user/vercel-deploy/scripts/deploy.sh /path/to/project.tgz
```

## 输出结果

```
Preparing deployment...
Detected framework: nextjs
Creating deployment package...
Deploying...
✓ Deployment successful!

Preview URL: https://skill-deploy-abc123.vercel.app
Claim URL:   https://vercel.com/claim-deployment?code=...
```

该脚本还会在标准输出（stdout）中输出 JSON 数据，以便进行程序化处理：

```json
{
  "previewUrl": "https://skill-deploy-abc123.vercel.app",
  "claimUrl": "https://vercel.com/claim-deployment?code=...",
  "deploymentId": "dpl_...",
  "projectId": "prj_..."
}
```

## 框架检测

脚本会从 `package.json` 文件中自动检测所使用的框架。支持的框架包括：

- **React**：Next.js、Gatsby、Create React App、Remix、React Router
- **Vue**：Nuxt、Vitepress、Vuepress、Gridsome
- **Svelte**：SvelteKit、Svelte、Sapper
- **其他前端框架**：Astro、Solid Start、Angular、Ember、Preact、Docusaurus
- **后端框架**：Express、Hono、Fastify、NestJS、Elysia、h3、Nitro
- **构建工具**：Vite、Parcel
- **以及其他框架**：Blitz、Hydrogen、RedwoodJS、Storybook、Sanity 等。

对于没有 `package.json` 文件的静态 HTML 项目，系统会自动将框架设置为 `null`。

## 静态 HTML 项目

对于没有 `package.json` 文件的项目：
- 如果存在一个非 `index.html` 名称的 `.html` 文件，系统会自动将其重命名为 `index.html`。
- 这样可以确保页面能够通过根路径（`/`）被访问。

## 向用户展示结果

务必同时向用户展示预览 URL 和 Claim URL：

```
✓ Deployment successful!

Preview URL: https://skill-deploy-abc123.vercel.app
Claim URL:   https://vercel.com/claim-deployment?code=...

View your site at the Preview URL.
To transfer this deployment to your Vercel account, visit the Claim URL.
```

## 故障排除

### 网络访问错误

如果由于网络限制（在 claude.ai 上较为常见）导致部署失败，请告知用户：

```
Deployment failed due to network restrictions. To fix this:

1. Go to https://claude.ai/settings/capabilities
2. Add *.vercel.com to the allowed domains
3. Try deploying again
```