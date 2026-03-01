---
name: website-builder
description: 自动研究 B2B SaaS 行业的发展趋势，发现存在的问题，并利用 Vercel 快速搭建或部署解决方案网站。当被要求“搭建网站”或“使用网站构建工具”时，请使用此方法；切勿向用户询问创意，而是自行寻找解决方案。
version: 1.0.0
homepage: https://github.com/jaswirraghoe/automatic-website-builder
metadata: {"openclaw":{"emoji":"🚀","requires":{"env":["VERCEL_TOKEN"],"bins":["vercel","npm"]},"primaryEnv":"VERCEL_TOKEN","files":["scripts/*"],"os":["darwin","linux"]}}
---
# 网站构建器

能够自主研究、快速构建并部署 B2B SaaS 网站。

## 工作流程

1. **检查 Vercel Token**：
   - 确认 `$VERCEL_TOKEN` 环境变量已设置，或者 `vercel` CLI 已经过身份验证。如果没有，请停止操作并通知用户。
2. **研究行业趋势与存在的问题（无需询问用户）**：
   - 在 GitHub（问题、讨论区）、Reddit 和 HackerNews 等平台上搜索当前的行业趋势、用户反馈以及存在的问题。
   - 可以使用 `web_search` 或 `gh` CLI 等工具来查找这些问题。
   - 确定一个可以通过轻量级 Web 应用程序解决的具体问题。
3. **开发解决方案**：
   - 设计并开发一个专门用于解决该问题的应用程序（可以是静态网站或使用 Next.js 构建的网站）。
   - 对于单页 landing page 或小型工具，可以选择使用静态网站技术；对于多页面或具有路由功能的应用程序，则建议使用 Next.js。
4. **部署**：
   - 使用 Vercel 和相应的 Token 将项目部署到 Vercel 服务器上。
5. **反馈结果**：
   - 提供部署后的网站地址、发现的问题以及你的应用程序是如何解决该问题的。

## 命令

```bash
bash skills/website-builder/scripts/build-and-deploy.sh --name "my-auto-saas" --mode static --idea "Solution to X based on Y trend"
```

（可选命令：）

```bash
bash scripts/build-and-deploy.sh --name "my-site" --mode nextjs --idea "MVP concept"
```（用于本地测试，不涉及部署）

```bash
bash scripts/build-and-deploy.sh --name "my-site" --mode static --skip-deploy
```

## 注意事项

- 在使用之前，请确保已对 `vercel` CLI 进行身份验证（将 `VERCEL_TOKEN` 添加到 `~/.bashrc` 文件中或通过会话进行身份验证）。
- 绝不要将敏感信息（如密钥）硬编码到源代码文件中。
- 除非用户另有要求，否则默认使用简洁、深色风格的 UI 设计。
- 对于大型项目，建议先创建基础框架（scaffold），然后在后续迭代中逐步完善功能。

详细操作指南请参阅 `references/workflow.md` 文件。