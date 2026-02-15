# Web 部署

将网站、Web 应用程序和 API 部署到生产环境。

## 本地预览流程

```bash
# Static site
npx http-server ./dist -p 8080 -c-1

# Next.js
npm run dev          # Development (hot reload)
npm run build && npm run start  # Production preview

# FastAPI
uvicorn app.main:app --reload --port 8000

# Vite-based
npm run dev          # Dev server
npm run build && npx serve dist  # Production preview
```

## 部署目标

### Vercel（前端 / Next.js / 静态网站）

```bash
# First time setup
npx vercel link

# Preview deployment
npx vercel

# Production deployment
npx vercel --prod

# Environment variables
npx vercel env add SECRET_KEY
```

**适用场景：** Next.js 应用程序、React 单页应用（SPA）、静态网站、无服务器函数。

**配置方式：** 使用 `vercel.json` 文件（Next.js 通常不需要此配置文件）  
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "nextjs"
}
```

### Railway（后端 / API / 数据库）

```bash
# First time setup
railway login
railway init

# Deploy
railway up

# Add database
railway add --plugin postgresql

# Environment variables
railway variables set SECRET_KEY=value

# View logs
railway logs
```

**适用场景：** 后端 API、数据库、长时间运行的进程、Docker 容器。

### GitHub Pages（静态网站）

```bash
# Using gh-pages package
npm install -D gh-pages
# Add to package.json scripts: "deploy": "gh-pages -d dist"
npm run build && npm run deploy
```

**适用场景：** 文档、简单的静态网站、项目页面。

### Canvas（Clawdbot 工作区）

将应用部署到 `~/clawd/canvas/` 目录，通过 clawdbot 代理进行本地预览。
```bash
cp -r ./dist/* ~/clawd/canvas/my-project/
```

## 部署前检查清单

- [ ] 本地构建成功（`npm run build` / `python -m build`）
- [ ] 无 TypeScript 或代码格式检查（lint）错误
- [ ] 测试通过
- [ ] 环境变量已配置到目标平台
- [ ] `.env` 和 `secret` 文件未包含在 Git 代码库中
- [ ] 如果是公开网站，已配置 `robots.txt` 和 `sitemap.xml`
- [ ] 已设置favicon 和元标签
- [ ] 已配置 HTTPS（Vercel/Railway 会自动处理）
- [ ] 已配置错误页面（404、500 状态码）
- [ ] 性能优化：图片已压缩，代码已分割，避免生成过大的文件包

## 回滚机制

```bash
# Vercel — redeploy previous
npx vercel rollback

# Railway — redeploy previous
railway rollback

# Git-based — revert and push
git revert HEAD && git push
```

## 域名设置

```bash
# Vercel
npx vercel domains add mydomain.com

# DNS: Point CNAME to cname.vercel-dns.com
# Or A record to 76.76.21.21
```