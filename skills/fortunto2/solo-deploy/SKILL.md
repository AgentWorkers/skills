---
name: solo-deploy
description: >
  将项目部署到托管平台：  
  - 阅读 `stack.yaml` 文件以获取详细的配置信息；  
  - 检测系统中可用的本地 CLI 工具（如 Vercel、Wrangler、Supabase、Fly、SST 等）；  
  - 设置数据库；  
  - 推送代码；  
  - 验证部署是否成功。  
  此步骤应在用户请求“部署项目”、“将代码推送到生产环境”或 `/build` 命令执行完成后执行。**请勿在构建完成之前执行此步骤**。
license: MIT
metadata:
  author: fortunto2
  version: "1.2.1"
  openclaw:
    emoji: "🚀"
allowed-tools: Read, Grep, Bash, Glob, Write, Edit, mcp__solograph__session_search, mcp__solograph__project_code_search, mcp__solograph__codegraph_query
argument-hint: "[platform]"
---
# /deploy

将项目部署到其托管平台。系统会读取堆栈模板 YAML 文件（`templates/stacks/{stack}.yaml`），以获取详细的部署配置（包括平台、命令行工具、基础设施层、持续集成/持续交付（CI/CD）以及监控配置）。系统会检测已安装的命令行工具，配置数据库和环境，推送代码，并验证部署是否成功生效。

## 参考文档

- `templates/principles/dev-principles.md` — 持续集成/持续交付（CI/CD）相关原则、密钥管理、DNS 设置以及共享基础设施规则
- `templates/stacks/*.yaml` — 包含部署、基础设施、CI/CD 和监控配置的堆栈模板

> 文件路径是相对于技能插件的根目录的。如果文件不在预期位置，可以使用全局搜索（Glob）来查找。

## 使用时机

在 `/build` 阶段完成所有任务后执行此步骤（即构建阶段结束后）。这是项目的部署引擎。

部署流程：`/build` → **`/deploy`** → `/review`

## 可用的 MCP 工具（如可用，请使用）

- `session_search(query)` — 查找之前类似项目的部署方式
- `project_code_search(query, project)` — 在不同项目中查找部署模式
- `codegraph_query(query)` — 检查项目依赖关系和堆栈配置

如果 MCP 工具不可用，可以退而使用全局搜索（Glob）+ 正则表达式匹配（Grep）+ 读取文件（Read）的组合方法。

## 部署前的检查

### 1. 验证构建是否完成（可选）
- 如果存在管道状态跟踪文件（`.solo/states/` 目录），请检查 `.solo/states/build` 文件。
- 如果 `.solo/states/` 目录存在但缺少 `build` 标记：提示“构建可能未完成，请先运行 `/build` 命令”。
- 如果 `.solo/states/` 目录不存在：跳过此检查，直接进行部署。

### 2. 检测可用的命令行工具

并行执行以下操作，以检测本地安装的命令行工具：
```bash
vercel --version 2>/dev/null && echo "VERCEL_CLI=yes" || echo "VERCEL_CLI=no"
wrangler --version 2>/dev/null && echo "WRANGLER_CLI=yes" || echo "WRANGLER_CLI=no"
npx supabase --version 2>/dev/null && echo "SUPABASE_CLI=yes" || echo "SUPABASE_CLI=no"
fly version 2>/dev/null && echo "FLY_CLI=yes" || echo "FLY_CLI=no"
sst version 2>/dev/null && echo "SST_CLI=yes" || echo "SST_CLI=no"
gh --version 2>/dev/null && echo "GH_CLI=yes" || echo "GH_CLI=no"
```

记录所有可用的命令行工具。如果工具已经全局安装，可以直接使用，无需通过 `npx` 来调用它们。

### 3. 加载项目配置信息（并行读取）
- `CLAUDE.md` — 堆栈名称、架构和部署平台
- `docs/prd.md` — 产品需求和部署说明
- `docs/workflow.md` — 持续集成/持续交付（CI/CD）策略（如果存在）
- `package.json` 或 `pyproject.toml` — 项目依赖关系和脚本
- `fly.toml`, `wrangler.toml`, `sst.config.ts` — 平台配置文件（如果存在）
- `docs/plan/*/plan.md` — 当前的部署计划（查找与部署相关的阶段或任务）

**基于计划的部署：** 如果当前部署计划中包含具体的部署步骤或任务（例如“将 Python 后端部署到 VPS 上”、“运行 deploy.sh 命令”或“在服务器上设置 Docker”），这些应被视为主要的部署指令。部署计划会指定项目特有的部署目标，而这些目标可能不在通用的堆栈 YAML 文件中。除了标准的平台部署操作外，还需要执行计划中的部署任务。

### 4. 读取堆栈模板 YAML 文件

从 `CLAUDE.md` 文件中提取堆栈名称（查找 `stack:` 字段或相关的技术堆栈信息）。

读取堆栈模板文件以获取详细的部署配置：

**查找顺序**（先找到哪个文件就用哪个）：
1. `templates/stacks/{stack}.yaml` — 相对于技能插件的根目录
2. `.solo/stacks/{stack}.yaml` — 用户本地自定义的配置（来自 `/init` 文件）
3. 使用全局搜索在项目目录或其父目录中查找 `**/stacks/{stack}.yaml` 文件

从 YAML 文件中提取以下配置信息：
- `deploy` — 部署目标平台（例如 `vercel`, `cloudflare_workers`, `cloudflare_pages`, `fly.io`, `docker`, `app_store`, `play_store`, `local`）
- `deploy_cli` — 命令行工具及其使用场景（例如 `vercel (用于本地预览、环境变量设置、部署推送)`）
- `infra` — 基础设施工具和层级（例如 `sst (sst.config.ts)`）
- `ci_cd` — 持续集成/持续交付系统（例如 `github_actions`）
- `monitoring` — 监控/分析工具（例如 `posthog`）
- `database` / `orm` — 数据库和对象关系映射（ORM）配置（如果有的话，会影响迁移过程）
- `storage` — 存储服务配置（例如 R2、D1、KV 等）
- `notes` — 与堆栈相关的部署说明

**以下的所有部署决策都应以 YAML 文件中的配置为准。YAML 文件中的配置会覆盖默认的配置设置。**

### 5. 检测部署平台（如果没有 YAML 文件，则使用默认配置）

如果未找到堆栈 YAML 文件，使用以下默认配置矩阵：

| 堆栈名称 | 部署平台 | 基础设施层级 |
|---------|-----------|-----------|
| `nextjs-supabase` / `nextjs-ai-agents` | Vercel + Supabase | 第 1 层 |
| `cloudflare-workers` | Cloudflare Workers | 第 1 层 |
| `astro-static` / `astro-hybrid` | Cloudflare Pages | 第 1 层 |
| `python-api` | Fly.io（快速部署）或 Pulumi + Hetzner（生产环境） | 第 2/4 层 |
| `python-ml` | 跳过（无需使用命令行工具，因为无需托管） | — |
| `ios-swift` | 跳过（应用发布需要手动操作） | — |
| `kotlin-android` | 跳过（应用发布需要手动操作） | — |

如果 `$ARGUMENTS` 参数指定了具体的部署平台，请使用该参数，而不是依赖默认配置。

**自动部署平台**（根据 YAML 文件中的 `deploy` 字段或默认配置）：
- `vercel` / `cloudflare_pages`：通过推送代码即可自动部署。如果项目已经关联到相应的平台，只需执行推送操作即可。初次设置时需要手动执行部署。
- `cloudflare-workers`：需要使用 `wrangler deploy` 命令进行部署。
- `fly.io`：需要执行 `fly deploy` 命令进行部署。

## 部署步骤

### 步骤 1. Git — 清理代码并推送更改

```bash
git status
git log --oneline -5
```

如果代码有未提交的更改，请提交这些更改：
```bash
git add -A
git commit -m "chore: pre-deploy cleanup"
```

确保远程仓库存在，并执行推送操作：
```bash
git remote -v
git push origin main
```

如果远程仓库不存在，请创建一个新的 GitHub 仓库：
```bash
gh repo create {project-name} --private --source=. --push
```

**对于支持自动部署的平台（如 Vercel、Cloudflare Pages）：** 如果项目已经关联到相应的平台，推送代码后部署会自动触发。此时可以跳过手动部署命令。

### 步骤 2. 设置数据库

**如果项目中包含 `supabase/` 目录或检测到 Supabase 依赖关系：** 执行相应的数据库配置操作：
```bash
# If supabase CLI available:
supabase db push          # apply migrations
supabase gen types --lang=typescript --local > db/types.ts  # optional: regenerate types
```
如果没有命令行工具，请引导用户通过 Supabase 控制台进行数据库迁移。

**如果项目中包含 `drizzle.config.ts` 文件：** 执行相应的数据库配置操作：
```bash
npx drizzle-kit push      # push schema to database
npx drizzle-kit generate  # generate migration files (if needed)
```

**如果 `wrangler.toml` 文件中配置了 Cloudflare D1 服务：** 执行相应的数据库配置操作：
```bash
wrangler d1 migrations apply {db-name}
```

如果数据库尚未配置，列出所需的信息后继续下一步操作——不要因为数据库配置问题而阻塞部署流程。

### 步骤 3. 设置环境变量

读取 `.env.example` 或 `.env.local.example` 文件以确定所需的环境变量。

生成针对特定平台的配置指令：

**Vercel：**
```bash
# If vercel CLI is available and project is linked:
vercel env ls  # show current env vars

# Guide user:
echo "Set env vars: vercel env add VARIABLE_NAME"
echo "Or via dashboard: https://vercel.com/[team]/[project]/settings/environment-variables"
```

**Cloudflare：**
```bash
wrangler secret put VARIABLE_NAME  # interactive prompt for value
# Or in wrangler.toml [vars] section for non-secret values
```

**Fly.io：**
```bash
fly secrets set VARIABLE_NAME=value
fly secrets list
```

**注意：** **不要直接创建或修改 `.env` 文件，因为其中可能包含敏感信息**。请让用户自行设置环境变量。

### 步骤 4. 执行平台部署

**Vercel（非自动部署情况）：**
```bash
vercel link          # first time: link to project
vercel               # deploy preview
vercel --prod        # deploy production (after verifying preview)
```

**Cloudflare Workers/Pages：**
```bash
wrangler deploy              # Workers
wrangler pages deploy ./out  # Pages (check build output dir)
```

**Fly.io：**
```bash
fly launch   # first time — creates app, sets region
fly deploy   # subsequent deploys
```

**如果项目中包含 `sst.config.ts` 文件：** 执行相应的配置操作：
```bash
sst deploy --stage prod    # production
sst deploy --stage dev     # staging
```

### 步骤 5. 验证部署结果

部署完成后，需要验证项目是否真正生效：

```bash
# 1. HTTP status check
STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://{deployment-url})

# 2. Check for runtime errors in page body
BODY=$(curl -s https://{deployment-url} | head -200)

# 3. Check Vercel deployment logs for errors
vercel logs --output=short 2>&1 | tail -30
```

**如果 HTTP 状态码不是 200，或者页面显示错误信息：**
1. 检查 `vercel env ls` 命令，确认所有必要的环境变量是否都已设置。
2. 如果有环境变量缺失，使用 `vercel env add NAME production <<< "value"` 命令添加它们。
3. 如果环境变量设置错误，使用 `vercel env rm NAME production` 命令删除错误的变量，然后再添加正确的值。
4. 更正环境变量后，使用 `vercel --prod --yes` 命令重新部署项目。
5. 重新检查 HTTP 状态码和页面内容。

**常见的运行时错误及解决方法：**
- “需要 Supabase URL/Key”：在 Vercel 配置中添加 `NEXT_PUBLIC_supABASE_URL` 和 `NEXT_PUBLIC_supABASE_ANON_KEY`。
- “DATABASE_URL 未设置”：在 Vercel 配置中添加 `DATABASE_URL`。
- “缺少 Stripe 密钥”：根据实际情况添加相应的密钥或删除相关代码。
- 页面显示空白或出现 hydration 错误：检查构建日志，可能需要使用 `vercel --prod` 命令重新部署项目。

**只有在页面加载成功且返回 HTTP 200 状态码时，才能输出 `<solo:done/>`。** 如果问题无法解决，请输出 `<solo:redo/>` 以返回到构建阶段。只有当 `.solo/states/` 目录存在时，才输出相应的管道状态信息。**

### 步骤 6. 部署后的日志监控

验证部署成功后，需要监控运行时的错误（例如环境变量缺失、数据库连接问题、服务器崩溃或 API 超时等问题）。

从堆栈 YAML 文件中读取与平台相关的日志命令：

**Vercel（Next.js）：**
```bash
vercel logs --output=short 2>&1 | tail -50
```
检查以下错误信息：`Error`, `FUNCTION_INVOCATION_FAILED`, `EDGE_FUNCTION_INVOCATION_FAILED`, `504 GATEWAY_TIMEOUT`, unhandled rejections`。

**Cloudflare Workers：**
```bash
wrangler tail --format=pretty 2>&1 | head -100
```
检查以下错误信息：`Error`, uncaught exceptions, D1 query failures, R2 access errors`。

**Cloudflare Pages（Astro）：**
```bash
wrangler pages deployment tail --project-name={name} 2>&1 | head -100
```

**Fly.io（Python API）：**
```bash
fly logs --app {name} 2>&1 | tail -50
fly status --app {name}
```
检查以下错误信息：`ERROR`, `CRITICAL`, unhealthy instances, OOM kills, connection refused`。

**如果使用了 Supabase Edge Functions：**
```bash
supabase functions logs --scroll 2>&1 | tail -30
```

**处理日志错误的方法：**
- **环境变量缺失**：使用相应的平台命令行工具进行修复，然后重新部署。
- **数据库连接错误**：检查连接字符串和 IP 允许列表。
- **运行时崩溃或未处理的错误**：如果 `.solo/states/` 目录存在，输出 `<solo:redo/>` 以返回到构建阶段进行修复；否则修复错误后重新部署。
- **如果 30 行日志中没有任何错误**：继续执行后续步骤。

**如果新部署后没有请求记录：** 发送几个测试请求，然后再次检查日志以确认是否存在问题。

### 步骤 7. 部署后的报告

```
Deployment: {project-name}

  Platform:  {platform}
  URL:       {deployment-url}
  Branch:    main
  Commit:    {sha}

  Done:
    - [x] Code pushed to GitHub
    - [x] Deployed to {platform}
    - [x] Database migrations applied (or N/A)

  Manual steps remaining:
    - [ ] Set environment variables (listed above)
    - [ ] Custom domain (optional)
    - [ ] PostHog / analytics setup (optional)

  Next: /review — final quality gate
```

## 部署完成

### 发出完成信号

如果 `.solo/states/` 目录存在，仅输出一次完成信号：
```
<solo:done/>
```
**请勿在响应的其他部分重复输出此完成信号。** 只输出一次。
如果 `.solo/states/` 目录不存在，则跳过完成信号的输出。

## 错误处理

### 命令行工具未找到
**原因：** 相应的命令行工具未安装。
**解决方法：** 安装相应的工具：`npm i -g vercel`, `npm i -g wrangler`, `brew install flyctl`, `brew install supabase/tap/supabase`。

### 部署失败 — 构建成功但部署失败
**原因：** 在本地构建成功，但在目标平台上出现错误（例如 Node 版本不同、环境变量缺失）。
**解决方法：** 查看平台的构建日志，确保 `package.json` 中指定的构建工具与目标平台匹配，并设置缺失的环境变量。

### 数据库连接失败
**原因：** `DATABASE_URL` 未设置或网络连接出现问题。
**解决方法：** 检查连接字符串和平台的数据库配置信息，以及 IP 允许列表。

### Git 推送失败
**原因：** 远程仓库与本地代码不一致。
**解决方法：** 执行 `git pull --rebase origin main` 命令解决冲突，然后再推送代码。

## 部署验证

在报告“部署成功”之前，请执行以下操作：
1. 使用 `curl -s -o /dev/null -w "%{http_code}"` 命令检查部署目标的 HTTP 状态。
2. 确保 HTTP 状态码为 200（而不是 404、500 或重定向循环）。
3. 确认页面内容符合预期（不是空白页面或显示错误信息）。
**只有在确认以上条件都满足时，才能报告部署成功。**

**重要规则：**
1. **必须使用已安装的命令行工具**：在尝试使用 `npx` 之前，确保已经安装了 `vercel`, `wrangler`, `supabase`, `fly`, `sst` 等工具。
2. **了解自动部署机制**：如果平台支持自动部署，只需执行推送操作，无需手动执行部署命令。
3. **切勿在代码中存储敏感信息**：不要在 `.env` 文件中存储敏感环境变量或 API 密钥。
4. **先进行预览部署**：在正式部署之前，先进行预览部署，确认无误后再切换到生产环境。
5. **先在本地进行构建验证**：在部署之前，使用 `pnpm build` 或 `uv build`（或其他等效命令）进行构建验证。
6. **部署后务必查看日志**：在确认部署成功之前，务必查看日志以捕获运行时的错误。
7. **报告所有相关的部署信息**：包括部署 URL 和平台控制台的链接。
8. **优先使用配置文件**：建议使用 `sst.config.ts` 或 `fly.toml` 等配置文件，而不是手动配置。
9. **确认部署成功后再宣布**：只有在确认部署 URL 返回 HTTP 200 状态码且日志正常后，才能宣布部署成功。

**关键注意事项：**
1. **务必使用已安装的命令行工具**。
2. **了解自动部署机制**：如果平台支持自动部署，只需执行推送操作。
3. **切勿在代码中存储敏感信息**。
4. **先进行预览部署**。
5. **先在本地进行构建验证**。
6. **务必查看部署后的日志**。
7. **报告所有相关的部署信息**。
8. **优先使用配置文件**。
9. **确认部署成功后再宣布**。