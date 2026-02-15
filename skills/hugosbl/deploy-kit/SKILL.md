# 部署工具包 — Web 应用部署技能

该工具包简化了通过 **Vercel**、**Railway** 和 **Supabase** 的命令行界面（CLI）来部署 Web 应用的过程。

## 适用场景

当用户需要部署应用程序、创建数据库、配置服务器托管环境或管理这些平台上的环境变量时，可以使用该技能。

## 主要工作流程

### 1. 检测项目类型

```bash
python3 skills/deploy-kit/scripts/deploy.py detect <chemin>
```

返回：检测到的项目框架、编程语言及关键配置文件。

### 2. 检查可用的 CLI 工具

```bash
python3 skills/deploy-kit/scripts/deploy.py check
```

如果缺少某个 CLI，会指导用户进行安装（请参阅相应文档）。

### 3. 推荐合适的平台

```bash
python3 skills/deploy-kit/scripts/deploy.py recommend <chemin>
```

| 项目类型 | 推荐平台 |
|---|---|
| 静态前端 / SSR（Next.js、Astro、Vite、Svelte、Nuxt） | **Vercel** |
| 后端 / API（Express、Flask、FastAPI、Django） | **Railway** |
| 全栈应用（结合 BDD 架构） | **Railway** + **Supabase** |
| BDD、认证、存储功能或边缘函数（Edge Functions） | **Supabase** |

### 4. 实施部署

```bash
python3 skills/deploy-kit/scripts/deploy.py deploy <chemin> --platform <vercel|railway|supabase>
```

⚠️ **在部署前务必获取用户确认。** 脚本还会要求用户进行交互式确认。

## 项目检测规则

| 检测到的文件 | 对应的框架 |
|---|---|
| `next.config.*` | Next.js |
| `astro.config.*` | Astro |
| `vite.config.*` | Vite |
| `svelte.config.*` | SvelteKit |
| `nuxt.config.*` | Nuxt |
| `remix.config.*` / `app/root.tsx` | Remix |
| `angular.json` | Angular |
| `requirements.txt` / `Pipfile` | Python 应用 |
| `manage.py` | Django 应用 |
| `package.json` → `scripts.start` | Node.js 应用 |
| `Dockerfile` | 使用 Docker 的项目 |
| `supabase/config.toml` | Supabase 项目 |

## 环境变量设置

- **Vercel**：使用 `vercel env add 变量名` 命令设置环境变量，或通过管理面板进行设置。
- **Railway**：使用 `railway variables set 变量名=值` 命令设置环境变量。
- **Supabase**：通过 `supabase secrets set 变量名=值` 命令设置敏感信息。

部署前务必检查 `.env` 或 `.env.local` 文件中是否存在相关环境变量。

## 自定义域名设置

- **Vercel**：使用 `vercel domains add 域名.com` 命令添加自定义域名。
- **Railway**：使用 `railway domain` 命令设置域名（系统会生成子域名），也可通过管理面板进行自定义。

## 详细参考资料

根据项目平台，可查阅以下文档：

- `skills/deploy-kit/references/vercel.md` — Vercel CLI 完整使用指南
- `skills/deploy-kit/references/railway.md` — Railway CLI 完整使用指南
- `skills/deploy-kit/references/supabase.md` — Supabase CLI 完整使用指南

## 常用命令

| 功能 | 对应命令 |
|---|---|
| 预发布部署（Vercel） | `vercel` |
| 生产环境部署（Vercel） | `vercel --prod` |
| 部署到 Railway 服务器 | `railway up` |
| 推送数据库数据到 Supabase | `supabase db push` |
| 部署边缘函数 | `supabase functions deploy <函数名称>` |
| 查看日志 | `vercel logs <日志地址>` / `railway logs` |
| 列出所有项目 | `vercel ls` / `railway list` |

## 使用规则

1. **未经用户明确授权，严禁进行任何部署操作**。
2. 在推荐部署方案之前，必须先检测项目信息。
3. 确保用户已安装并登录相应的 CLI 工具。
4. 如需执行高级命令，请先查阅相关平台文档。
5. 在正式部署前，建议先进行预发布测试。
6. 如果项目超出免费使用范围，请提前告知用户可能产生的费用。